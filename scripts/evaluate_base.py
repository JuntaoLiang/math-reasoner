from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from transformers import (
        AutoModelForCausalLM, 
        AutoTokenizer,
        PreTrainedModel,
        PreTrainedTokenizerBase,
        )

from src.evaluation.data import EvaluationItem, load_evaluation_items
from src.evaluation.scoring import extract_final_answer, is_correct


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
        description="Evaluate a local causal language model on a JSONL dataset."
    )

    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path("/root/autodl-tmp/models/Qwen3-1.7B-Base"),
    )
    parser.add_argument(
        "--dataset-path",
        type=Path,
        default=Path("data/evaluation/math_baseline.jsonl"),
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("outputs/evaluation/base_results.jsonl"),
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=128,
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
        "Solve the problem and provide the final numeric answer.\n"
        "Answer:"
    )


def load_model(
    model_path: Path,
    device: str,
) -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA was requested, but no CUDA device is available."
        )

    dtype = (
        torch.bfloat16
        if device.startswith("cuda")
        else torch.float32
    )

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=dtype,
    )
    model.to(device)
    model.eval()

    return tokenizer, model


def evaluate_item(
    item: EvaluationItem,
    tokenizer: PreTrainedTokenizerBase,
    model: PreTrainedModel,
    device: str,
    max_new_tokens: int,
) -> EvaluationResult:
    prompt = build_prompt(item)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(device)

    prompt_length = inputs["input_ids"].shape[1]

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.1,
            no_repeat_ngram_size=4,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_ids = outputs[0][prompt_length:]

    model_output = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True,
    ).strip()

    predicted_answer = extract_final_answer(model_output)

    correct = is_correct(
        predicted_answer,
        item.answer,
    )

    return EvaluationResult(
        id=item.id,
        problem=item.problem,
        reference_answer=item.answer,
        model_output=model_output,
        predicted_answer=predicted_answer,
        correct=correct,
        generated_tokens=generated_ids.numel(),
        truncated=generated_ids.numel() >= max_new_tokens,

        )


def save_results(
    results: list[EvaluationResult],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open("w", encoding="utf-8") as file:
        for result in results:
            record = asdict(result)
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


def print_summary(results: list[EvaluationResult]) -> None:
    total = len(results)
    correct_count = sum(result.correct for result in results)
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
    average_generated_tokens = total_generated_tokens / total

    print("\nEvaluation summary")
    print(f"Total items: {total}")
    print(f"Correct items: {correct_count}")
    print(f"Answer accuracy: {accuracy:.2%}")
    print(f"Parsed answers: {parsed_count}")
    print(f"Answer parse rate: {parse_rate:.2%}")
    print(
        "Average generated tokens: "
        f"{average_generated_tokens:.2f}"
    )
    print(f"Truncated outputs:{truncated_count}")
    print(f"Truncated rate:{truncated_count / total:.2%}")


def main() -> None:
    args = parse_args()

    items = load_evaluation_items(args.dataset_path)

    print(f"Loading model from: {args.model_path}")

    tokenizer, model = load_model(
        model_path=args.model_path,
        device=args.device,
    )

    results: list[EvaluationResult] = []

    for index, item in enumerate(items, start=1):
        print(
            f"[{index}/{len(items)}] "
            f"Evaluating {item.id}"
        )

        result = evaluate_item(
            item=item,
            tokenizer=tokenizer,
            model=model,
            device=args.device,
            max_new_tokens=args.max_new_tokens,
        )

        results.append(result)

        print(f"Predicted answer: {result.predicted_answer}")
        print(f"Reference answer: {result.reference_answer}")
        print(f"Correct: {result.correct}")

    save_results(
        results=results,
        output_path=args.output_path,
    )

    print_summary(results)

    print(f"\nResults saved to: {args.output_path}")


if __name__ == "__main__":
    main()
