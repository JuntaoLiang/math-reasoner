from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from datasets import load_dataset


CALCULATION_PATTERN = re.compile(r"<<.*?>>")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert GSM8K into the project SFT JSONL format."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/sft/gsm8k"),
    )
    parser.add_argument(
        "--train-limit",
        type=int,
        default=None,
        help="Optional maximum number of training records.",
    )
    parser.add_argument(
        "--test-limit",
        type=int,
        default=None,
        help="Optional maximum number of test records.",
    )
    return parser.parse_args()


def clean_response(answer: str) -> str:
    cleaned = CALCULATION_PATTERN.sub("", answer)
    return cleaned.strip()


def convert_split(
    split,
    output_path: Path,
    id_prefix: str,
    limit: int | None,
) -> int:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    selected_split = split

    if limit is not None:
        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        selected_split = split.select(
            range(min(limit, len(split)))
        )

    with output_path.open("w", encoding="utf-8") as file:
        for index, record in enumerate(selected_split, start=1):
            converted = {
                "id": f"{id_prefix}_{index:05d}",
                "problem": record["question"].strip(),
                "response": clean_response(record["answer"]),
            }

            file.write(
                json.dumps(
                    converted,
                    ensure_ascii=False,
                )
                + "\n"
            )

    return len(selected_split)


def main() -> None:
    args = parse_args()

    dataset = load_dataset(
        "openai/gsm8k",
        "main",
    )

    train_count = convert_split(
        split=dataset["train"],
        output_path=args.output_dir / "train.jsonl",
        id_prefix="gsm8k_train",
        limit=args.train_limit,
    )

    test_count = convert_split(
        split=dataset["test"],
        output_path=args.output_dir / "test.jsonl",
        id_prefix="gsm8k_test",
        limit=args.test_limit,
    )

    print(f"Training records written: {train_count}")
    print(f"Test records written: {test_count}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()