from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any


FINAL_ANSWER_PATTERN = re.compile(
    r"####\s*([-+]?\d[\d,]*(?:\.\d+)?)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sample GSM8K training records deterministically and "
            "convert them into the existing evaluation-data format."
        )
    )

    parser.add_argument(
        "--input-path",
        type=Path,
        default=Path("data/sft/gsm8k/train.jsonl"),
        help="Processed GSM8K SFT training JSONL.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/dpo_candidates_1000.jsonl"
        ),
        help="Output candidate JSONL used by evaluate_base.py.",
    )

    parser.add_argument(
        "--metadata-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/"
            "dpo_candidates_1000_metadata.jsonl"
        ),
        help=(
            "Output file preserving the full reference responses "
            "for later preference-pair construction."
        ),
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Number of training examples to sample.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used for deterministic sampling.",
    )

    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Input file not found: {path}"
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
                    f"Line {line_number} must contain a JSON object."
                )

            required_fields = {
                "id",
                "problem",
                "response",
            }

            missing_fields = required_fields - record.keys()

            if missing_fields:
                raise ValueError(
                    f"Missing fields at line {line_number}: "
                    f"{sorted(missing_fields)}"
                )

            records.append(record)

    if not records:
        raise ValueError(
            f"Input file is empty: {path}"
        )

    return records


def extract_reference_answer(response: str) -> str:
    matches = list(
        FINAL_ANSWER_PATTERN.finditer(response)
    )

    if not matches:
        raise ValueError(
            "Reference response does not contain "
            "a valid '#### number' answer."
        )

    return (
        matches[-1]
        .group(1)
        .replace(",", "")
        .strip()
    )


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

    if args.limit <= 0:
        raise ValueError(
            "--limit must be greater than 0."
        )

    source_records = load_jsonl(
        args.input_path
    )

    if args.limit > len(source_records):
        raise ValueError(
            f"Requested {args.limit} records, but only "
            f"{len(source_records)} are available."
        )

    random_generator = random.Random(
        args.seed
    )

    selected_records = random_generator.sample(
        source_records,
        k=args.limit,
    )

    # 按原始 ID 排序，方便后续人工查找和结果对齐。
    selected_records.sort(
        key=lambda record: str(record["id"])
    )

    evaluation_records: list[
        dict[str, str]
    ] = []

    metadata_records: list[
        dict[str, str]
    ] = []

    for record in selected_records:
        item_id = str(record["id"])
        problem = str(record["problem"])
        response = str(record["response"])

        reference_answer = extract_reference_answer(
            response
        )

        # evaluate_base.py 当前需要：
        # id / problem / answer
        evaluation_records.append(
            {
                "id": item_id,
                "problem": problem,
                "answer": reference_answer,
            }
        )

        # 完整标准回答单独保存，
        # 后续构建 chosen/rejected 时通过 id 合并。
        metadata_records.append(
            {
                "id": item_id,
                "problem": problem,
                "reference_response": response,
                "reference_answer": reference_answer,
            }
        )

    save_jsonl(
        records=evaluation_records,
        path=args.output_path,
    )

    save_jsonl(
        records=metadata_records,
        path=args.metadata_path,
    )

    print(f"Source records: {len(source_records)}")
    print(f"Selected records: {len(selected_records)}")
    print(f"Random seed: {args.seed}")
    print(f"Evaluation data: {args.output_path}")
    print(f"Metadata data: {args.metadata_path}")


if __name__ == "__main__":
    main()