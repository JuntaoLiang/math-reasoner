from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare Base and SFT evaluation results."
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--sft-path",
        type=Path,
        required=True,
    )
    return parser.parse_args()


def load_results(
    path: Path,
) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Evaluation file not found: {path}"
        )

    records: dict[str, dict[str, Any]] = {}

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number} in {path}: "
                    f"{error}"
                ) from error

            item_id = str(record["id"])

            if item_id in records:
                raise ValueError(
                    f"Duplicate evaluation id: {item_id}"
                )

            records[item_id] = record

    if not records:
        raise ValueError(f"Evaluation file is empty: {path}")

    return records


def calculate_summary(
    records: dict[str, dict[str, Any]],
) -> dict[str, float | int]:
    total = len(records)

    correct = sum(
        bool(record["correct"])
        for record in records.values()
    )

    parsed = sum(
        record.get("predicted_answer") is not None
        for record in records.values()
    )

    truncated = sum(
        bool(record.get("truncated", False))
        for record in records.values()
    )

    average_tokens = sum(
        int(record.get("generated_tokens", 0))
        for record in records.values()
    ) / total

    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total,
        "parsed": parsed,
        "parse_rate": parsed / total,
        "truncated": truncated,
        "truncation_rate": truncated / total,
        "average_generated_tokens": average_tokens,
    }


def print_summary(
    name: str,
    summary: dict[str, float | int],
) -> None:
    print(f"\n{name}")

    print(f"Total: {summary['total']}")
    print(f"Correct: {summary['correct']}")
    print(f"Accuracy: {summary['accuracy']:.2%}")
    print(f"Parsed: {summary['parsed']}")
    print(f"Parse rate: {summary['parse_rate']:.2%}")
    print(f"Truncated: {summary['truncated']}")
    print(
        "Truncation rate: "
        f"{summary['truncation_rate']:.2%}"
    )
    print(
        "Average generated tokens: "
        f"{summary['average_generated_tokens']:.2f}"
    )


def main() -> None:
    args = parse_args()

    base_results = load_results(args.base_path)
    sft_results = load_results(args.sft_path)

    if set(base_results) != set(sft_results):
        missing_in_sft = sorted(
            set(base_results) - set(sft_results)
        )
        missing_in_base = sorted(
            set(sft_results) - set(base_results)
        )

        raise ValueError(
            "Evaluation IDs do not match. "
            f"Missing in SFT: {missing_in_sft}; "
            f"missing in Base: {missing_in_base}"
        )

    print_summary(
        "Base summary",
        calculate_summary(base_results),
    )

    print_summary(
        "SFT summary",
        calculate_summary(sft_results),
    )

    improved: list[str] = []
    regressed: list[str] = []
    unchanged: list[str] = []

    for item_id in base_results:
        base_correct = bool(
            base_results[item_id]["correct"]
        )
        sft_correct = bool(
            sft_results[item_id]["correct"]
        )

        if not base_correct and sft_correct:
            improved.append(item_id)
        elif base_correct and not sft_correct:
            regressed.append(item_id)
        else:
            unchanged.append(item_id)

    print("\nPer-item changes")
    print(f"Improved: {len(improved)} {improved}")
    print(f"Regressed: {len(regressed)} {regressed}")
    print(f"Unchanged: {len(unchanged)}")


if __name__ == "__main__":
    main()