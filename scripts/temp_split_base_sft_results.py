from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CATEGORY_FILE_NAMES = {
    "base_correct_sft_wrong": "base_correct_sft_wrong.jsonl",
    "base_wrong_sft_correct": "base_wrong_sft_correct.jsonl",
    "both_correct": "both_correct.jsonl",
    "both_wrong": "both_wrong.jsonl",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Split Base and SFT evaluation results into four "
            "comparison categories."
        )
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        required=True,
        help="Path to Base evaluation result JSONL.",
    )
    parser.add_argument(
        "--sft-path",
        type=Path,
        required=True,
        help="Path to SFT evaluation result JSONL.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tmp/base_sft_comparison"),
        help="Output directory for classified JSONL files.",
    )
    return parser.parse_args()


def load_results(
    path: Path,
) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Evaluation result file not found: {path}"
        )

    results: dict[str, dict[str, Any]] = {}

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

            if not isinstance(record, dict):
                raise ValueError(
                    f"Record at line {line_number} in {path} "
                    "must be a JSON object."
                )

            if "id" not in record:
                raise ValueError(
                    f"Missing id at line {line_number} in {path}."
                )

            if "correct" not in record:
                raise ValueError(
                    f"Missing correct field at line "
                    f"{line_number} in {path}."
                )

            item_id = str(record["id"])

            if item_id in results:
                raise ValueError(
                    f"Duplicate id in {path}: {item_id}"
                )

            results[item_id] = record

    if not results:
        raise ValueError(
            f"Evaluation result file is empty: {path}"
        )

    return results


def get_reference_answer(
    record: dict[str, Any],
) -> str | None:
    value = record.get(
        "reference_answer",
        record.get("answer"),
    )

    if value is None:
        return None

    return str(value)


def classify_result(
    base_correct: bool,
    sft_correct: bool,
) -> str:
    if base_correct and not sft_correct:
        return "base_correct_sft_wrong"

    if not base_correct and sft_correct:
        return "base_wrong_sft_correct"

    if base_correct and sft_correct:
        return "both_correct"

    return "both_wrong"


def build_comparison_record(
    item_id: str,
    base_record: dict[str, Any],
    sft_record: dict[str, Any],
    category: str,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "category": category,
        "problem": base_record.get(
            "problem",
            sft_record.get("problem"),
        ),
        "reference_answer": get_reference_answer(
            base_record
        )
        or get_reference_answer(sft_record),
        "base": {
            "predicted_answer": base_record.get(
                "predicted_answer"
            ),
            "correct": bool(base_record["correct"]),
            "generated_tokens": base_record.get(
                "generated_tokens"
            ),
            "truncated": base_record.get("truncated"),
            "model_output": base_record.get(
                "model_output"
            ),
        },
        "sft": {
            "predicted_answer": sft_record.get(
                "predicted_answer"
            ),
            "correct": bool(sft_record["correct"]),
            "generated_tokens": sft_record.get(
                "generated_tokens"
            ),
            "truncated": sft_record.get("truncated"),
            "model_output": sft_record.get(
                "model_output"
            ),
        },
    }


def save_jsonl(
    records: list[dict[str, Any]],
    path: Path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


def main() -> None:
    args = parse_args()

    base_results = load_results(args.base_path)
    sft_results = load_results(args.sft_path)

    base_ids = set(base_results)
    sft_ids = set(sft_results)

    if base_ids != sft_ids:
        missing_in_sft = sorted(
            base_ids - sft_ids
        )
        missing_in_base = sorted(
            sft_ids - base_ids
        )

        raise ValueError(
            "Base and SFT result IDs do not match. "
            f"Missing in SFT: {missing_in_sft}; "
            f"missing in Base: {missing_in_base}"
        )

    categories: dict[str, list[dict[str, Any]]] = {
        category: []
        for category in CATEGORY_FILE_NAMES
    }

    for item_id in base_results:
        base_record = base_results[item_id]
        sft_record = sft_results[item_id]

        category = classify_result(
            base_correct=bool(base_record["correct"]),
            sft_correct=bool(sft_record["correct"]),
        )

        comparison_record = build_comparison_record(
            item_id=item_id,
            base_record=base_record,
            sft_record=sft_record,
            category=category,
        )

        categories[category].append(
            comparison_record
        )

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = 0

    for category, file_name in CATEGORY_FILE_NAMES.items():
        records = categories[category]
        output_path = args.output_dir / file_name

        save_jsonl(
            records=records,
            path=output_path,
        )

        total += len(records)

        print(
            f"{category}: {len(records)} "
            f"-> {output_path}"
        )

    print(f"\nTotal records: {total}")


if __name__ == "__main__":
    main()