from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import torch
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from src.evaluation.data import (
    EvaluationItem,
    load_evaluation_items,
)
from src.evaluation.scoring import (
    extract_final_answer,
    is_correct,
)


@dataclass
class EvaluationResult:
    id: str
    problem: str
    reference_answer: str
    model_output: str
    predicted_answer: str | None
    correct: bool
    generated_tokens: int
    truncated: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate a local causal language model "
            "on a JSONL dataset with batched generation."
        )
    )

    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path(
            "/root/autodl-tmp/models/"
            "Qwen3-1.7B-Base"
        ),
    )

    parser.add_argument(
        "--adapter-path",
        type=Path,
        default=None,
        help="Optional path to a trained PEFT adapter.",
    )

    parser.add_argument(
        "--dataset-path",
        type=Path,
        default=Path(
            "data/evaluation/math_baseline.jsonl"
        ),
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path(
            "outputs/evaluation/base_results.jsonl"
        ),
    )

    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=512,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Number of prompts generated in one batch.",
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
    )

    return parser.parse_args()


def build_prompt(item: EvaluationItem) -> str:
    return (
        f"Problem: {item.problem}\n"
        "Provide a clear step-by-step solution "
        "and a final answer.\n"
        "Response:"
    )


def load_model(
    model_path: Path,
    device: str,
    adapter_path: Path | None = None,
) -> tuple[
    PreTrainedTokenizerBase,
    PreTrainedModel,
]:
    if (
        device.startswith("cuda")
        and not torch.cuda.is_available()
    ):
        raise RuntimeError(
            "CUDA was requested, but no CUDA "
            "device is available."
        )

    dtype = (
        torch.bfloat16
        if device.startswith("cuda")
        else torch.float32
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_path
    )

    # Decoder-only 模型进行批量生成时应使用左侧 Padding。
    # 这样每条 Prompt 的最后一个有效 token 都位于右侧。
    tokenizer.padding_side = "left"

    if tokenizer.pad_token_id is None:
        if tokenizer.eos_token_id is None:
            raise ValueError(
                "Tokenizer has neither pad_token_id "
                "nor eos_token_id."
            )

        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=dtype,
    )

    if adapter_path is not None:
        if not adapter_path.is_dir():
            raise FileNotFoundError(
                "Adapter directory not found: "
                f"{adapter_path}"
            )

        model = PeftModel.from_pretrained(
            model,
            adapter_path,
        )

    model.to(device)
    model.eval()

    return tokenizer, model


def find_effective_generated_length(
    generated_ids: torch.Tensor,
    eos_token_id: int | None,
) -> tuple[int, bool]:
    """
    计算单条输出的有效生成长度。

    返回：
    - effective_length：截至第一个 EOS 的长度；
    - has_eos：是否在生成内容中遇到 EOS。

    批量生成时，较短回答会被补齐到该批次最长长度，
    因此不能直接使用 generated_ids.numel()。
    """

    total_length = generated_ids.numel()

    if eos_token_id is None:
        return total_length, False

    eos_positions = (
        generated_ids == eos_token_id
    ).nonzero(as_tuple=False)

    if eos_positions.numel() == 0:
        return total_length, False

    first_eos_position = int(
        eos_positions[0].item()
    )

    # 生成长度包含 EOS token。
    return first_eos_position + 1, True


def evaluate_batch(
    items: Sequence[EvaluationItem],
    tokenizer: PreTrainedTokenizerBase,
    model: PreTrainedModel,
    device: str,
    max_new_tokens: int,
) -> list[EvaluationResult]:
    prompts = [
        build_prompt(item)
        for item in items
    ]

    inputs = tokenizer(
        prompts,
        return_tensors="pt",
        padding=True,
        truncation=False,
    )

    inputs = {
        name: tensor.to(device)
        for name, tensor in inputs.items()
    }

    # 左 Padding 后，所有样本共享相同的输入张量宽度。
    # generate() 返回的是：
    # [完整的 padded prompt] + [生成内容]
    padded_prompt_length = (
        inputs["input_ids"].shape[1]
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.1,
            no_repeat_ngram_size=4,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    results: list[EvaluationResult] = []

    for item, output_ids in zip(
        items,
        outputs,
        strict=True,
    ):
        generated_ids = output_ids[
            padded_prompt_length:
        ]

        (
            effective_length,
            has_eos,
        ) = find_effective_generated_length(
            generated_ids=generated_ids,
            eos_token_id=tokenizer.eos_token_id,
        )

        effective_generated_ids = generated_ids[
            :effective_length
        ]

        model_output = tokenizer.decode(
            effective_generated_ids,
            skip_special_tokens=True,
        ).strip()

        predicted_answer = extract_final_answer(
            model_output
        )

        correct = is_correct(
            predicted_answer,
            item.answer,
        )

        # 没有生成 EOS，且生成长度达到上限，
        # 才认为输出被最大长度截断。
        truncated = (
            not has_eos
            and effective_length >= max_new_tokens
        )

        results.append(
            EvaluationResult(
                id=item.id,
                problem=item.problem,
                reference_answer=item.answer,
                model_output=model_output,
                predicted_answer=predicted_answer,
                correct=correct,
                generated_tokens=effective_length,
                truncated=truncated,
            )
        )

    return results


def iter_batches(
    items: Sequence[EvaluationItem],
    batch_size: int,
) -> list[Sequence[EvaluationItem]]:
    return [
        items[start : start + batch_size]
        for start in range(
            0,
            len(items),
            batch_size,
        )
    ]


def prepare_output_file(
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 每次正式评测前清空旧文件，
    # 防止重复执行时结果被追加两次。
    output_path.write_text(
        "",
        encoding="utf-8",
    )


def append_results(
    results: Sequence[EvaluationResult],
    output_path: Path,
) -> None:
    """
    每完成一个 batch 就立即写入文件。

    即使推理中断，已经完成的 batch 仍然保留。
    """

    with output_path.open(
        "a",
        encoding="utf-8",
    ) as file:
        for result in results:
            file.write(
                json.dumps(
                    asdict(result),
                    ensure_ascii=False,
                )
                + "\n"
            )


def print_summary(
    results: Sequence[EvaluationResult],
) -> None:
    total = len(results)

    if total == 0:
        raise ValueError(
            "Cannot summarize empty results."
        )

    correct_count = sum(
        result.correct
        for result in results
    )

    parsed_count = sum(
        result.predicted_answer is not None
        for result in results
    )

    total_generated_tokens = sum(
        result.generated_tokens
        for result in results
    )

    truncated_count = sum(
        result.truncated
        for result in results
    )

    accuracy = correct_count / total
    parse_rate = parsed_count / total
    average_generated_tokens = (
        total_generated_tokens / total
    )

    print("\nEvaluation summary")
    print(f"Total items: {total}")
    print(f"Correct items: {correct_count}")
    print(f"Answer accuracy: {accuracy:.2%}")
    print(f"Parsed answers: {parsed_count}")
    print(
        f"Answer parse rate: {parse_rate:.2%}"
    )
    print(
        "Average generated tokens: "
        f"{average_generated_tokens:.2f}"
    )
    print(
        f"Truncated outputs: {truncated_count}"
    )
    print(
        "Truncation rate: "
        f"{truncated_count / total:.2%}"
    )


def main() -> None:
    args = parse_args()

    if args.batch_size <= 0:
        raise ValueError(
            "--batch-size must be greater than 0."
        )

    if args.max_new_tokens <= 0:
        raise ValueError(
            "--max-new-tokens must be greater than 0."
        )

    items = load_evaluation_items(
        args.dataset_path
    )

    print(f"Loading model from: {args.model_path}")

    if args.adapter_path is not None:
        print(
            f"Loading adapter from: "
            f"{args.adapter_path}"
        )

    print(f"Dataset items: {len(items)}")
    print(f"Batch size: {args.batch_size}")
    print(
        f"Max new tokens: "
        f"{args.max_new_tokens}"
    )

    tokenizer, model = load_model(
        model_path=args.model_path,
        device=args.device,
        adapter_path=args.adapter_path,
    )

    prepare_output_file(
        args.output_path
    )

    results: list[EvaluationResult] = []

    batches = iter_batches(
        items=items,
        batch_size=args.batch_size,
    )

    processed_count = 0

    for batch_index, batch_items in enumerate(
        batches,
        start=1,
    ):
        start_item = processed_count + 1
        end_item = (
            processed_count
            + len(batch_items)
        )

        print(
            f"\n[Batch {batch_index}/{len(batches)}] "
            f"Evaluating items "
            f"{start_item}-{end_item}"
        )

        batch_results = evaluate_batch(
            items=batch_items,
            tokenizer=tokenizer,
            model=model,
            device=args.device,
            max_new_tokens=args.max_new_tokens,
        )

        append_results(
            results=batch_results,
            output_path=args.output_path,
        )

        results.extend(batch_results)
        processed_count += len(batch_results)

        batch_correct = sum(
            result.correct
            for result in batch_results
        )

        print(
            f"Batch completed: "
            f"{len(batch_results)} items"
        )

        print(
            f"Batch correct: "
            f"{batch_correct}/"
            f"{len(batch_results)}"
        )

        print(
            f"Total progress: "
            f"{processed_count}/{len(items)}"
        )

    print_summary(results)

    print(
        f"\nResults saved to: "
        f"{args.output_path}"
    )


if __name__ == "__main__":
    main()