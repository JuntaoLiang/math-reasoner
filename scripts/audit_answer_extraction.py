from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CATEGORY_NAMES = (
    "correct_complete",
    "correct_truncated",
    "incorrect_complete",
    "incorrect_truncated",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Classify evaluation results into temporary files "
            "for manual review."
        )
    )
    parser.add_argument(
        "--input-path",
        type=Path,
        required=True,
        help="Path to the evaluation result JSONL file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tmp/base_evaluation_review"),
        help="Directory used to store classified review files.",
    )
    return parser.parse_args()


def load_jsonl(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Evaluation result file not found: {path}"
        )

    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {error}"
                ) from error

            if not isinstance(record, dict):
                raise ValueError(
                    f"Record at line {line_number} "
                    "must be a JSON object."
                )

            required_fields = {
                "id",
                "problem",
                "model_output",
                "predicted_answer",
                "correct",
                "truncated",
            }

            missing_fields = required_fields - record.keys()

            if missing_fields:
                missing_text = ", ".join(
                    sorted(missing_fields)
                )
                raise ValueError(
                    f"Missing required fields at line "
                    f"{line_number}: {missing_text}"
                )

            records.append(record)

    if not records:
        raise ValueError(
            f"Evaluation result file is empty: {path}"
        )

    return records


def classify_record(
    record: dict[str, Any],
) -> str:
    correct = bool(record["correct"])
    truncated = bool(record["truncated"])

    if correct and not truncated:
        return "correct_complete"

    if correct and truncated:
        return "correct_truncated"

    if not correct and not truncated:
        return "incorrect_complete"

    return "incorrect_truncated"


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


def build_review_record(
    record: dict[str, Any],
    category: str,
) -> dict[str, Any]:
    return {
        "id": record["id"],
        "category": category,
        "problem": record["problem"],
        "reference_answer": get_reference_answer(record),
        "predicted_answer": record.get(
            "predicted_answer"
        ),
        "correct": bool(record["correct"]),
        "truncated": bool(record["truncated"]),
        "generated_tokens": record.get(
            "generated_tokens"
        ),
        "model_output": record["model_output"],
        "manual_review": {
            "reasoning_correct": None,
            "final_answer_explicit": None,
            "extraction_correct": None,
            "error_type": None,
            "notes": "",
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


def save_markdown(
    records: list[dict[str, Any]],
    path: Path,
    category: str,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("w", encoding="utf-8") as file:
        file.write(f"# {category}\n\n")
        file.write(f"样本数量：{len(records)}\n\n")

        for index, record in enumerate(records, start=1):
            file.write(
                f"## {index}. {record['id']}\n\n"
            )

            file.write("### Problem\n\n")
            file.write(
                f"{record['problem']}\n\n"
            )

            file.write("### Reference answer\n\n")
            file.write(
                f"{record['reference_answer']}\n\n"
            )

            file.write("### Predicted answer\n\n")
            file.write(
                f"{record['predicted_answer']}\n\n"
            )

            file.write("### Metadata\n\n")
            file.write(
                f"- Correct: {record['correct']}\n"
            )
            file.write(
                f"- Truncated: {record['truncated']}\n"
            )
            file.write(
                "- Generated tokens: "
                f"{record['generated_tokens']}\n\n"
            )

            file.write("### Model output\n\n")
            file.write("```text\n")
            file.write(
                str(record["model_output"])
            )
            file.write("\n```\n\n")

            file.write("### Manual review\n\n")
            file.write(
                "- Reasoning correct: \n"
                "- Final answer explicit: \n"
                "- Extraction correct: \n"
                "- Error type: \n"
                "- Notes: \n\n"
            )

            file.write("---\n\n")


def main() -> None:
    args = parse_args()

    records = load_jsonl(args.input_path)

    categories: dict[str, list[dict[str, Any]]] = {
        category: []
        for category in CATEGORY_NAMES
    }

    for record in records:
        category = classify_record(record)

        review_record = build_review_record(
            record=record,
            category=category,
        )

        categories[category].append(
            review_record
        )

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = 0

    for category, category_records in categories.items():
        jsonl_path = (
            args.output_dir
            / f"{category}.jsonl"
        )

        markdown_path = (
            args.output_dir
            / f"{category}.md"
        )

        save_jsonl(
            records=category_records,
            path=jsonl_path,
        )

        save_markdown(
            records=category_records,
            path=markdown_path,
            category=category,
        )

        count = len(category_records)
        total += count

        print(
            f"{category}: {count}"
        )

    print(f"\nTotal classified records: {total}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()