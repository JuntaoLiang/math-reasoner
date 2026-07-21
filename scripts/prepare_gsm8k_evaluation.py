from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FINAL_ANSWER_PATTERN = re.compile(
    r"####\s*([-+]?(?:\d[\d,]*)(?:\.\d+)?)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert GSM8K SFT data into evaluation JSONL format."
    )
    parser.add_argument(
        "--input-path",
        type=Path,
        default=Path("data/sft/gsm8k/test.jsonl"),
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("data/evaluation/gsm8k_test_20.jsonl"),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of evaluation records.",
    )
    return parser.parse_args()


def extract_reference_answer(response: str) -> str:
    matches = FINAL_ANSWER_PATTERN.findall(response)

    if not matches:
        raise ValueError(
            "Could not extract GSM8K final answer from response."
        )

    return matches[-1].replace(",", "")


def convert_file(
    input_path: Path,
    output_path: Path,
    limit: int | None = None,
) -> int:
    if not input_path.is_file():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    if limit is not None and limit <= 0:
        raise ValueError("limit must be greater than zero.")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    with input_path.open("r", encoding="utf-8") as input_file:
        with output_path.open("w", encoding="utf-8") as output_file:
            for line_number, line in enumerate(input_file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    record: dict[str, Any] = json.loads(line)
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
                    "response",
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

                try:
                    reference_answer = extract_reference_answer(
                        str(record["response"])
                    )
                except ValueError as error:
                    raise ValueError(
                        f"Failed at line {line_number}: {error}"
                    ) from error

                item_id = str(record["id"]).strip()
                problem = str(record["problem"]).strip()

                if not item_id:
                    raise ValueError(
                        f"Empty id at line {line_number}."
                    )

                if not problem:
                    raise ValueError(
                        f"Empty problem at line {line_number}."
                    )

                evaluation_record = {
                    "id": item_id,
                    "problem": problem,
                    "answer": reference_answer,
                }

                output_file.write(
                    json.dumps(
                        evaluation_record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

                count += 1

                if limit is not None and count >= limit:
                    break

    if count == 0:
        raise ValueError(
            f"No evaluation records written from: {input_path}"
        )

    return count


def main() -> None:
    args = parse_args()

    count = convert_file(
        input_path=args.input_path,
        output_path=args.output_path,
        limit=args.limit,
    )

    print(f"Evaluation records written: {count}")
    print(f"Output path: {args.output_path}")


if __name__ == "__main__":
    main()