from __future__ import annotations

import argparse
import math
from pathlib import Path

from transformers import AutoTokenizer

from src.data.sft import load_sft_items
from src.data.sft_formatting import format_sft_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze token lengths of SFT samples."
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="/root/autodl-tmp/models/Qwen3-1.7B-Base",
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("data/sft/gsm8k/train.jsonl"),
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=512,
    )
    return parser.parse_args()


def percentile(
    values: list[int],
    percentage: float,
) -> int:
    if not values:
        raise ValueError("Values must not be empty.")

    sorted_values = sorted(values)
    index = math.ceil(
        percentage / 100 * len(sorted_values)
    ) - 1
    index = max(0, min(index, len(sorted_values) - 1))

    return sorted_values[index]


def main() -> None:
    args = parse_args()

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_path
    )

    if tokenizer.eos_token is None:
        raise ValueError("Tokenizer does not define an EOS token.")

    items = load_sft_items(args.data_path)

    lengths: list[int] = []

    for item in items:
        text = format_sft_text(
            item=item,
            eos_token=tokenizer.eos_token,
        )

        token_ids = tokenizer(
            text,
            add_special_tokens=False,
        )["input_ids"]

        lengths.append(len(token_ids))

    truncated_count = sum(
        length > args.max_length
        for length in lengths
    )

    print(f"Samples: {len(lengths)}")
    print(f"Minimum length: {min(lengths)}")
    print(f"Average length: {sum(lengths) / len(lengths):.2f}")
    print(f"P50 length: {percentile(lengths, 50)}")
    print(f"P90 length: {percentile(lengths, 90)}")
    print(f"P95 length: {percentile(lengths, 95)}")
    print(f"P99 length: {percentile(lengths, 99)}")
    print(f"Maximum length: {max(lengths)}")
    print(f"Configured max length: {args.max_length}")
    print(f"Truncated samples: {truncated_count}")
    print(
        f"Truncation rate: "
        f"{truncated_count / len(lengths):.2%}"
    )


if __name__ == "__main__":
    main()