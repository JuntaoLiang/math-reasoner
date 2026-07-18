from __future__ import annotations

import argparse

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="Run a local model inference smoke test."
    )

    parser.add_argument(
        "--model-path",
        type=str,
        default="/root/autodl-tmp/models/Qwen3-1.7B-Base",
        help="本地模型目录",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        default="Solve: 2x+3=179 Answer:",
        help="输入给模型的提示词",
    )

    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=128,
        help="最大生成Token数量",
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="推理设备，例如cuda或cpu",
    )

    return parser.parse_args()


def main() -> None:
    """加载本地模型并执行推理测试。"""
    args = parse_args()

    if args.device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA不可用，请检查PyTorch和GPU环境。")

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)

    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        dtype=torch.bfloat16,
    ).to(args.device)

    model.eval()

    inputs = tokenizer(
        args.prompt,
        return_tensors="pt",
    ).to(args.device)

    if args.device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats()

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    prompt_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][prompt_length:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    print("Prompt:")
    print(args.prompt)

    print("\nModel response:")
    print(response)

    if args.device.startswith("cuda"):
        peak_vram_gb = torch.cuda.max_memory_allocated() / 1024**3
        print(f"\nPeak VRAM: {peak_vram_gb:.2f} GB")


if __name__ == "__main__":
    main()
