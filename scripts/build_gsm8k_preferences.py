from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build GSM8K DPO preference pairs by combining "
            "reference responses with incorrect SFT model outputs."
        )
    )

    parser.add_argument(
        "--metadata-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/"
            "dpo_candidates_1000_metadata.jsonl"
        ),
        help="JSONL containing reference_response for each candidate.",
    )

    parser.add_argument(
        "--generated-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/generated_v1_outputs.jsonl"
        ),
        help="JSONL containing SFT V1 generated outputs.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/train_dpo_v1.jsonl"
        ),
        help="Output DPO preference dataset.",
    )

    parser.add_argument(
        "--summary-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/"
            "train_dpo_v1_summary.json"
        ),
        help="Output summary JSON.",
    )

    parser.add_argument(
        "--review-path",
        type=Path,
        default=Path(
            "data/preference/gsm8k/"
            "train_dpo_v1_review.md"
        ),
        help="Markdown file used for manual review.",
    )

    parser.add_argument(
        "--review-limit",
        type=int,
        default=30,
        help="Number of preference pairs written to the review file.",
    )

    parser.add_argument(
        "--include-truncated-correct",
        action="store_true",
        help=(
            "Include outputs marked correct but truncated. "
            "Disabled by default because the final answer may still be valid."
        ),
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

            records.append(record)

    if not records:
        raise ValueError(
            f"JSONL file is empty: {path}"
        )

    return records


def index_by_id(
    records: list[dict[str, Any]],
    path: Path,
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}

    for line_number, record in enumerate(records, start=1):
        if "id" not in record:
            raise ValueError(
                f"Missing id at record {line_number} in {path}"
            )

        item_id = str(record["id"])

        if item_id in indexed:
            raise ValueError(
                f"Duplicate id in {path}: {item_id}"
            )

        indexed[item_id] = record

    return indexed


def build_prompt(problem: str) -> str:
    """
    必须与当前 SFT 训练和评测使用的 Prompt 保持一致。
    """

    return (
        f"Problem: {problem}\n"
        "Provide a clear step-by-step solution "
        "and a final answer.\n"
        "Response:"
    )


def should_include_generated_output(
    record: dict[str, Any],
    include_truncated_correct: bool,
) -> tuple[bool, str]:
    correct = bool(record.get("correct", False))
    truncated = bool(record.get("truncated", False))

    if not correct:
        if truncated:
            return True, "incorrect_and_truncated"

        return True, "incorrect_complete"

    if truncated and include_truncated_correct:
        return True, "correct_but_truncated"

    return False, "correct_complete"


def validate_text(
    value: Any,
    field_name: str,
    item_id: str,
) -> str:
    if value is None:
        raise ValueError(
            f"Missing {field_name} for item: {item_id}"
        )

    text = str(value).strip()

    if not text:
        raise ValueError(
            f"Empty {field_name} for item: {item_id}"
        )

    return text


def build_preference_record(
    metadata: dict[str, Any],
    generated: dict[str, Any],
    rejection_reason: str,
) -> dict[str, Any]:
    item_id = str(metadata["id"])

    problem = validate_text(
        metadata.get("problem"),
        "problem",
        item_id,
    )

    reference_response = validate_text(
        metadata.get("reference_response"),
        "reference_response",
        item_id,
    )

    model_output = validate_text(
        generated.get("model_output"),
        "model_output",
        item_id,
    )

    generated_problem = generated.get("problem")

    if (
        generated_problem is not None
        and str(generated_problem).strip() != problem
    ):
        raise ValueError(
            f"Problem mismatch for item: {item_id}"
        )

    if reference_response == model_output:
        raise ValueError(
            f"Chosen and rejected are identical: {item_id}"
        )

    return {
        "id": item_id,
        "prompt": build_prompt(problem),
        "chosen": reference_response,
        "rejected": model_output,
        "metadata": {
            "problem": problem,
            "reference_answer": metadata.get(
                "reference_answer"
            ),
            "predicted_answer": generated.get(
                "predicted_answer"
            ),
            "generated_tokens": generated.get(
                "generated_tokens"
            ),
            "truncated": bool(
                generated.get("truncated", False)
            ),
            "rejection_reason": rejection_reason,
            "source_model": (
                "qwen3-1.7b-gsm8k-full-bs8"
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


def save_summary(
    path: Path,
    metadata_count: int,
    generated_count: int,
    preference_records: list[dict[str, Any]],
    skipped_counts: Counter[str],
) -> None:
    rejection_counts = Counter(
        str(
            record["metadata"]["rejection_reason"]
        )
        for record in preference_records
    )

    truncated_count = sum(
        bool(record["metadata"]["truncated"])
        for record in preference_records
    )

    summary = {
        "metadata_count": metadata_count,
        "generated_count": generated_count,
        "preference_pair_count": len(
            preference_records
        ),
        "preference_pair_rate": (
            len(preference_records)
            / generated_count
        ),
        "rejection_reason_counts": dict(
            rejection_counts
        ),
        "truncated_rejected_count": truncated_count,
        "skipped_counts": dict(skipped_counts),
        "source_adapter": (
            "/root/autodl-tmp/checkpoints/"
            "qwen3-1.7b-gsm8k-full-bs8"
        ),
    }

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            summary,
            file,
            ensure_ascii=False,
            indent=2,
        )


def save_review_markdown(
    records: list[dict[str, Any]],
    path: Path,
    limit: int,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    review_records = records[:limit]

    with path.open("w", encoding="utf-8") as file:
        file.write("# GSM8K DPO V1 Preference Review\n\n")
        file.write(
            f"偏好对总数：{len(records)}\n\n"
        )
        file.write(
            f"当前展示：{len(review_records)} 条\n\n"
        )

        for index, record in enumerate(
            review_records,
            start=1,
        ):
            metadata = record["metadata"]

            file.write(
                f"## {index}. {record['id']}\n\n"
            )

            file.write("### Prompt\n\n")
            file.write("```text\n")
            file.write(record["prompt"])
            file.write("\n```\n\n")

            file.write("### Chosen\n\n")
            file.write("```text\n")
            file.write(record["chosen"])
            file.write("\n```\n\n")

            file.write("### Rejected\n\n")
            file.write("```text\n")
            file.write(record["rejected"])
            file.write("\n```\n\n")

            file.write("### Metadata\n\n")
            file.write(
                f"- Reference answer: "
                f"{metadata.get('reference_answer')}\n"
            )
            file.write(
                f"- Predicted answer: "
                f"{metadata.get('predicted_answer')}\n"
            )
            file.write(
                f"- Truncated: "
                f"{metadata.get('truncated')}\n"
            )
            file.write(
                f"- Rejection reason: "
                f"{metadata.get('rejection_reason')}\n\n"
            )

            file.write("### Manual review\n\n")
            file.write(
                "- Chosen is valid: \n"
                "- Rejected is genuinely worse: \n"
                "- Keep pair: \n"
                "- Notes: \n\n"
            )

            file.write("---\n\n")


def main() -> None:
    args = parse_args()

    if args.review_limit < 0:
        raise ValueError(
            "--review-limit must not be negative."
        )

    metadata_records = load_jsonl(
        args.metadata_path
    )

    generated_records = load_jsonl(
        args.generated_path
    )

    metadata_by_id = index_by_id(
        metadata_records,
        args.metadata_path,
    )

    generated_by_id = index_by_id(
        generated_records,
        args.generated_path,
    )

    metadata_ids = set(metadata_by_id)
    generated_ids = set(generated_by_id)

    if metadata_ids != generated_ids:
        missing_generated = sorted(
            metadata_ids - generated_ids
        )

        missing_metadata = sorted(
            generated_ids - metadata_ids
        )

        raise ValueError(
            "Metadata and generated IDs do not match. "
            f"Missing generated: {missing_generated[:10]}; "
            f"missing metadata: {missing_metadata[:10]}"
        )

    preference_records: list[
        dict[str, Any]
    ] = []

    skipped_counts: Counter[str] = Counter()

    for item_id in sorted(metadata_ids):
        metadata = metadata_by_id[item_id]
        generated = generated_by_id[item_id]

        include, reason = (
            should_include_generated_output(
                record=generated,
                include_truncated_correct=(
                    args.include_truncated_correct
                ),
            )
        )

        if not include:
            skipped_counts[reason] += 1
            continue

        preference_records.append(
            build_preference_record(
                metadata=metadata,
                generated=generated,
                rejection_reason=reason,
            )
        )

    if not preference_records:
        raise ValueError(
            "No valid preference pairs were produced."
        )

    save_jsonl(
        records=preference_records,
        path=args.output_path,
    )

    save_summary(
        path=args.summary_path,
        metadata_count=len(metadata_records),
        generated_count=len(generated_records),
        preference_records=preference_records,
        skipped_counts=skipped_counts,
    )

    save_review_markdown(
        records=preference_records,
        path=args.review_path,
        limit=args.review_limit,
    )

    print(
        f"Metadata records: {len(metadata_records)}"
    )
    print(
        f"Generated records: {len(generated_records)}"
    )
    print(
        f"Preference pairs: {len(preference_records)}"
    )
    print(
        f"Preference pair rate: "
        f"{len(preference_records) / len(generated_records):.2%}"
    )

    print("\nSkipped:")

    for reason, count in skipped_counts.items():
        print(f"  {reason}: {count}")

    print(f"\nOutput: {args.output_path}")
    print(f"Summary: {args.summary_path}")
    print(f"Review: {args.review_path}")


if __name__ == "__main__":
    main()