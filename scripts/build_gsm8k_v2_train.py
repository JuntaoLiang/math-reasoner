from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build GSM8K SFT V2 training data by combining the "
            "original training set with a controlled reinforcement subset."
        )
    )

    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path("data/sft/gsm8k/train.jsonl"),
        help="Original GSM8K SFT training JSONL.",
    )

    parser.add_argument(
        "--candidate-path",
        type=Path,
        default=Path(
            "data/sft/gsm8k_v2_candidates/all_candidates.jsonl"
        ),
        help="Validated V2 candidate JSONL.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("data/sft/gsm8k/train_v2.jsonl"),
        help="Output V2 training JSONL.",
    )

    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help=(
            "Number of extra copies added for each candidate. "
            "repeat=1 means each candidate appears twice in total: "
            "once in the original set and once as reinforcement."
        ),
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used to shuffle the final dataset.",
    )

    return parser.parse_args()


def load_jsonl(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"JSONL file not found: {path}"
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
                    f"Invalid JSON at line {line_number} "
                    f"in {path}: {error}"
                ) from error

            if not isinstance(record, dict):
                raise ValueError(
                    f"Line {line_number} in {path} "
                    "must contain a JSON object."
                )

            required_fields = {
                "id",
                "problem",
                "response",
            }

            missing_fields = required_fields - record.keys()

            if missing_fields:
                raise ValueError(
                    f"Missing fields at line {line_number} "
                    f"in {path}: {sorted(missing_fields)}"
                )

            records.append(record)

    if not records:
        raise ValueError(
            f"JSONL file is empty: {path}"
        )

    return records


def normalize_training_record(
    record: dict[str, Any],
) -> dict[str, str]:
    """
    删除候选筛选阶段添加的 v2_categories、v2_scores 等字段，
    保留训练流程实际需要的三个字段。
    """

    return {
        "id": str(record["id"]),
        "problem": str(record["problem"]),
        "response": str(record["response"]),
    }


def validate_unique_base_ids(
    records: list[dict[str, Any]],
) -> None:
    id_counter = Counter(
        str(record["id"])
        for record in records
    )

    duplicate_ids = sorted(
        item_id
        for item_id, count in id_counter.items()
        if count > 1
    )

    if duplicate_ids:
        preview = duplicate_ids[:10]

        raise ValueError(
            "Duplicate IDs found in original training data. "
            f"Examples: {preview}"
        )


def validate_candidates(
    base_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
) -> None:
    base_by_id = {
        str(record["id"]): record
        for record in base_records
    }

    candidate_ids: set[str] = set()

    for record in candidate_records:
        item_id = str(record["id"])

        if item_id in candidate_ids:
            raise ValueError(
                f"Duplicate candidate ID: {item_id}"
            )

        candidate_ids.add(item_id)

        if item_id not in base_by_id:
            raise ValueError(
                f"Candidate ID is not present in base data: {item_id}"
            )

        base_record = normalize_training_record(
            base_by_id[item_id]
        )

        candidate_record = normalize_training_record(
            record
        )

        if base_record != candidate_record:
            raise ValueError(
                "Candidate content does not match the original "
                f"training record: {item_id}"
            )


def build_v2_records(
    base_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
    repeat: int,
    seed: int,
) -> list[dict[str, str]]:
    base_training_records = [
        normalize_training_record(record)
        for record in base_records
    ]

    candidate_training_records = [
        normalize_training_record(record)
        for record in candidate_records
    ]

    reinforced_records: list[dict[str, str]] = []

    for repeat_index in range(repeat):
        for record in candidate_training_records:
            reinforced_records.append(
                {
                    "id": (
                        f"{record['id']}"
                        f"__v2_repeat_{repeat_index + 1}"
                    ),
                    "problem": record["problem"],
                    "response": record["response"],
                }
            )

    final_records = (
        base_training_records
        + reinforced_records
    )

    random_generator = random.Random(seed)
    random_generator.shuffle(final_records)

    return final_records


def save_jsonl(
    records: list[dict[str, str]],
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


def save_summary(
    path: Path,
    base_count: int,
    candidate_count: int,
    repeat: int,
    final_count: int,
    seed: int,
) -> None:
    summary = {
        "base_count": base_count,
        "candidate_unique_count": candidate_count,
        "candidate_extra_repeat": repeat,
        "reinforcement_record_count": (
            candidate_count * repeat
        ),
        "final_count": final_count,
        "reinforcement_rate": (
            candidate_count * repeat / final_count
        ),
        "shuffle_seed": seed,
    }

    summary_path = path.with_name(
        f"{path.stem}_summary.json"
    )

    with summary_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    args = parse_args()

    if args.repeat < 1:
        raise ValueError(
            "--repeat must be at least 1."
        )

    base_records = load_jsonl(
        args.base_path
    )

    candidate_records = load_jsonl(
        args.candidate_path
    )

    validate_unique_base_ids(
        base_records
    )

    validate_candidates(
        base_records=base_records,
        candidate_records=candidate_records,
    )

    final_records = build_v2_records(
        base_records=base_records,
        candidate_records=candidate_records,
        repeat=args.repeat,
        seed=args.seed,
    )

    save_jsonl(
        records=final_records,
        path=args.output_path,
    )

    save_summary(
        path=args.output_path,
        base_count=len(base_records),
        candidate_count=len(candidate_records),
        repeat=args.repeat,
        final_count=len(final_records),
        seed=args.seed,
    )

    reinforcement_count = (
        len(candidate_records) * args.repeat
    )

    print(f"Base records: {len(base_records)}")
    print(
        f"Unique reinforcement candidates: "
        f"{len(candidate_records)}"
    )
    print(f"Extra repeat count: {args.repeat}")
    print(
        f"Added reinforcement records: "
        f"{reinforcement_count}"
    )
    print(f"Final V2 records: {len(final_records)}")
    print(
        f"Reinforcement rate: "
        f"{reinforcement_count / len(final_records):.2%}"
    )
    print(f"Output: {args.output_path}")


if __name__ == "__main__":
    main()