from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# 每个类别默认最多选择 150 条。
# 四个类别去重后，预计得到约 400～600 条候选样本。
DEFAULT_CATEGORY_LIMIT = 150
DEFAULT_MAX_TOTAL = 600
DEFAULT_SEED = 42


@dataclass(frozen=True)
class MatchResult:
    """某条样本对一个强化类别的匹配结果。"""

    category: str
    score: int
    reasons: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a small and controlled GSM8K V2 candidate set "
            "using strict composite matching rules."
        )
    )

    parser.add_argument(
        "--input-path",
        type=Path,
        default=Path("data/sft/gsm8k/train.jsonl"),
        help="Processed GSM8K training JSONL file.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/sft/gsm8k_v2_candidates"),
        help="Directory used to save candidate subsets.",
    )

    parser.add_argument(
        "--category-limit",
        type=int,
        default=DEFAULT_CATEGORY_LIMIT,
        help="Maximum number of selected samples per category.",
    )

    parser.add_argument(
        "--max-total",
        type=int,
        default=DEFAULT_MAX_TOTAL,
        help="Maximum number of unique candidates.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed used for deterministic tie-breaking.",
    )

    parser.add_argument(
        "--review-limit",
        type=int,
        default=30,
        help="Number of samples written to each Markdown review file.",
    )

    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Input file does not exist: {path}"
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


def contains_any(
    text: str,
    patterns: tuple[str, ...],
) -> list[str]:
    """返回实际匹配到的正则表达式。"""

    matched: list[str] = []

    for pattern in patterns:
        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            matched.append(pattern)

    return matched


def count_arithmetic_operations(response: str) -> int:
    """
    统计回答中的显式算术运算数量。

    这里只作为多步骤计算的辅助判断，不直接作为唯一筛选条件。
    """

    operation_patterns = (
        r"\d[\d,.]*\s*\+\s*\d",
        r"\d[\d,.]*\s*-\s*\d",
        r"\d[\d,.]*\s*[×x*]\s*\d",
        r"\d[\d,.]*\s*[÷/]\s*\d",
        r"\d[\d,.]*\s*=\s*\d",
    )

    count = 0

    for pattern in operation_patterns:
        count += len(
            re.findall(
                pattern,
                response,
                flags=re.IGNORECASE,
            )
        )

    return count


def match_percentage_fraction(
    problem: str,
    response: str,
) -> MatchResult | None:
    """
    百分比、比例和分数关系。

    这类表达具有较高区分度，因此允许单个强信号命中。
    """

    strong_patterns = (
        r"\bpercent\b",
        r"\bpercentage\b",
        r"\d+(?:\.\d+)?\s*%",
        r"\bone[- ]half\b",
        r"\bone[- ]third\b",
        r"\bone[- ]quarter\b",
        r"\bthree[- ]quarters\b",
        r"\bhalf of\b",
        r"\bthird of\b",
        r"\bquarter of\b",
        r"\bfraction of\b",
        r"\bratio of\b",
    )

    relation_patterns = (
        r"\bmore than\b",
        r"\bless than\b",
        r"\bincrease(?:d)? by\b",
        r"\bdecrease(?:d)? by\b",
        r"\bof the total\b",
        r"\bof them\b",
    )

    strong_matches = contains_any(
        problem,
        strong_patterns,
    )

    if not strong_matches:
        return None

    relation_matches = contains_any(
        problem,
        relation_patterns,
    )

    operation_count = count_arithmetic_operations(
        response
    )

    score = 3
    reasons = ["strong_percentage_or_fraction_signal"]

    if relation_matches:
        score += 2
        reasons.append("contains_relation_expression")

    if operation_count >= 2:
        score += 1
        reasons.append("multi_step_calculation")

    return MatchResult(
        category="percentage_fraction",
        score=score,
        reasons=tuple(reasons),
    )


def match_price_quantity_total(
    problem: str,
    response: str,
) -> MatchResult | None:
    """
    单价、数量、总价和找零。

    必须同时命中：
    1. 金额信号；
    2. 交易或单价关系信号。
    """

    money_patterns = (
        r"\$\s*\d",
        r"\b\d+(?:\.\d+)?\s*dollars?\b",
        r"\b\d+(?:\.\d+)?\s*cents?\b",
        r"\bdollars?\b",
        r"\bcents?\b",
    )

    transaction_patterns = (
        r"\bbuy\b",
        r"\bbuys\b",
        r"\bbought\b",
        r"\bpurchase",
        r"\bcosts?\b",
        r"\bprice\b",
        r"\bpaid\b",
        r"\bpays?\b",
        r"\bspends?\b",
        r"\bspent\b",
        r"\bsells?\b",
        r"\bsold\b",
        r"\bchange\b",
        r"\bprofit\b",
        r"\bfee\b",
        r"\bdiscount\b",
    )

    unit_price_patterns = (
        r"\beach\b",
        r"\bper\b",
        r"\bapiece\b",
        r"\bfor every\b",
        r"\bunit price\b",
    )

    change_patterns = (
        r"\bchange\b",
        r"\bpaid\b.*\bcost\b",
        r"\bspent\b.*\bleft\b",
        r"\bhow much money.*left\b",
    )

    money_matches = contains_any(
        problem,
        money_patterns,
    )

    transaction_matches = contains_any(
        problem,
        transaction_patterns,
    )

    if not money_matches or not transaction_matches:
        return None

    unit_matches = contains_any(
        problem,
        unit_price_patterns,
    )

    change_matches = contains_any(
        problem,
        change_patterns,
    )

    operation_count = count_arithmetic_operations(
        response
    )

    score = 3
    reasons = [
        "contains_money_signal",
        "contains_transaction_signal",
    ]

    if unit_matches:
        score += 2
        reasons.append("contains_unit_price_relation")

    if change_matches:
        score += 2
        reasons.append("contains_payment_or_change_relation")

    if operation_count >= 2:
        score += 1
        reasons.append("multi_step_calculation")

    return MatchResult(
        category="price_quantity_total",
        score=score,
        reasons=tuple(reasons),
    )


def match_remaining_change(
    problem: str,
    response: str,
) -> MatchResult | None:
    """
    剩余量、增加量、减少量和连续变化。

    必须同时具有变化信号和顺序/结果信号。
    """

    change_patterns = (
        r"\bremaining\b",
        r"\bremains?\b",
        r"\bleft\b",
        r"\bincrease(?:d|s)?\b",
        r"\bdecrease(?:d|s)?\b",
        r"\badded\b",
        r"\badds?\b",
        r"\bremoved\b",
        r"\bremoves?\b",
        r"\blost\b",
        r"\bloses?\b",
        r"\bgained\b",
        r"\bgains?\b",
        r"\bused\b",
        r"\buses?\b",
        r"\bgave away\b",
        r"\bsold\b",
        r"\bate\b",
        r"\bspent\b",
    )

    sequence_patterns = (
        r"\bafter\b",
        r"\bbefore\b",
        r"\bthen\b",
        r"\beach day\b",
        r"\bevery day\b",
        r"\bfirst\b.*\bthen\b",
        r"\bhow many.*(?:left|remain)",
        r"\bhow much.*(?:left|remain)",
    )

    quantity_relation_patterns = (
        r"\bmore than\b",
        r"\bless than\b",
        r"\btwice\b",
        r"\bdouble\b",
        r"\btriple\b",
        r"\btimes as many\b",
    )

    change_matches = contains_any(
        problem,
        change_patterns,
    )

    sequence_matches = contains_any(
        problem,
        sequence_patterns,
    )

    relation_matches = contains_any(
        problem,
        quantity_relation_patterns,
    )

    # 单独出现 left、after 等词不能入选。
    if not change_matches:
        return None

    if not sequence_matches and not relation_matches:
        return None

    operation_count = count_arithmetic_operations(
        response
    )

    # 为了保证是真正的多步骤变化题，
    # 回答中至少应存在两个显式计算操作。
    if operation_count < 2:
        return None

    score = 4
    reasons = [
        "contains_quantity_change",
        "contains_sequence_or_relation",
        "multi_step_calculation",
    ]

    if sequence_matches and relation_matches:
        score += 2
        reasons.append("contains_both_sequence_and_relation")

    if operation_count >= 3:
        score += 1
        reasons.append("three_or_more_operations")

    return MatchResult(
        category="remaining_change",
        score=score,
        reasons=tuple(reasons),
    )


def match_equation_multistep(
    problem: str,
    response: str,
) -> MatchResult | None:
    """
    方程关系、倍数关系和多步骤算术。

    不通过普通的 total、after 等词判断，
    而是要求出现明确关系表达，并具有多步运算。
    """

    equation_relation_patterns = (
        r"\btwice\b",
        r"\bdouble\b",
        r"\btriple\b",
        r"\bthree times\b",
        r"\bfour times\b",
        r"\btimes as many\b",
        r"\bmore than\b",
        r"\bless than\b",
        r"\bcombined\b",
        r"\btogether.*(?:have|has|had)\b",
        r"\bthe sum of\b",
        r"\bthe difference between\b",
        r"\bthe same number\b",
        r"\bequally\b",
    )

    equation_text_patterns = (
        r"\blet\s+[a-z]\s*=",
        r"\bsolve\b",
        r"\bequation\b",
        r"\bunknown\b",
    )

    relation_matches = contains_any(
        problem,
        equation_relation_patterns,
    )

    equation_matches = contains_any(
        response,
        equation_text_patterns,
    )

    operation_count = count_arithmetic_operations(
        response
    )

    if not relation_matches:
        return None

    if operation_count < 2:
        return None

    score = 3
    reasons = [
        "contains_explicit_quantity_relation",
        "multi_step_calculation",
    ]

    if equation_matches:
        score += 2
        reasons.append("response_uses_equation")

    if operation_count >= 3:
        score += 2
        reasons.append("three_or_more_operations")

    if len(relation_matches) >= 2:
        score += 1
        reasons.append("multiple_relation_signals")

    return MatchResult(
        category="equation_multistep",
        score=score,
        reasons=tuple(reasons),
    )


MATCH_FUNCTIONS = (
    match_percentage_fraction,
    match_price_quantity_total,
    match_remaining_change,
    match_equation_multistep,
)


def find_matches(
    record: dict[str, Any],
) -> list[MatchResult]:
    problem = str(record["problem"])
    response = str(record["response"])

    matches: list[MatchResult] = []

    for match_function in MATCH_FUNCTIONS:
        result = match_function(
            problem,
            response,
        )

        if result is not None:
            matches.append(result)

    return matches


def build_candidate_record(
    record: dict[str, Any],
    matches: list[MatchResult],
) -> dict[str, Any]:
    return {
        "id": str(record["id"]),
        "problem": str(record["problem"]),
        "response": str(record["response"]),
        "v2_categories": [
            match.category
            for match in matches
        ],
        "v2_scores": {
            match.category: match.score
            for match in matches
        },
        "v2_reasons": {
            match.category: list(match.reasons)
            for match in matches
        },
        "v2_max_score": max(
            match.score
            for match in matches
        ),
    }


def select_category_records(
    records: list[dict[str, Any]],
    category: str,
    limit: int,
    random_generator: random.Random,
) -> list[dict[str, Any]]:
    """
    先按匹配分数降序排列。

    相同分数的样本使用固定随机种子打乱，
    避免总是选择原数据靠前的样本。
    """

    grouped_by_score: dict[
        int,
        list[dict[str, Any]],
    ] = {}

    for record in records:
        score = int(
            record["v2_scores"][category]
        )

        grouped_by_score.setdefault(
            score,
            [],
        ).append(record)

    selected: list[dict[str, Any]] = []

    for score in sorted(
        grouped_by_score,
        reverse=True,
    ):
        score_records = grouped_by_score[score]
        random_generator.shuffle(score_records)

        remaining = limit - len(selected)

        if remaining <= 0:
            break

        selected.extend(
            score_records[:remaining]
        )

    return selected


def build_balanced_unique_set(
    category_records: dict[
        str,
        list[dict[str, Any]],
    ],
    max_total: int,
) -> list[dict[str, Any]]:
    """
    通过轮询各类别建立最终去重集合。

    避免某一个类别占据全部样本。
    """

    category_names = list(category_records)
    positions = {
        category: 0
        for category in category_names
    }

    selected_by_id: dict[
        str,
        dict[str, Any],
    ] = {}

    while len(selected_by_id) < max_total:
        added_in_round = False

        for category in category_names:
            records = category_records[category]
            position = positions[category]

            while position < len(records):
                record = records[position]
                position += 1

                item_id = str(record["id"])

                if item_id in selected_by_id:
                    continue

                selected_by_id[item_id] = record
                added_in_round = True
                break

            positions[category] = position

            if len(selected_by_id) >= max_total:
                break

        if not added_in_round:
            break

    return list(selected_by_id.values())


def save_jsonl(
    records: list[dict[str, Any]],
    path: Path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


def save_review_markdown(
    records: list[dict[str, Any]],
    path: Path,
    title: str,
    review_limit: int,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    review_records = records[:review_limit]

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        file.write(f"# {title}\n\n")
        file.write(
            f"候选总数：{len(records)}\n\n"
        )
        file.write(
            f"当前展示前 {len(review_records)} 条，"
            "用于人工抽查。\n\n"
        )

        for index, record in enumerate(
            review_records,
            start=1,
        ):
            file.write(
                f"## {index}. {record['id']}\n\n"
            )

            file.write("### Categories\n\n")

            categories = ", ".join(
                record["v2_categories"]
            )

            file.write(f"{categories}\n\n")

            file.write("### Scores\n\n")
            file.write("```json\n")
            file.write(
                json.dumps(
                    record["v2_scores"],
                    ensure_ascii=False,
                    indent=2,
                )
            )
            file.write("\n```\n\n")

            file.write("### Match reasons\n\n")
            file.write("```json\n")
            file.write(
                json.dumps(
                    record["v2_reasons"],
                    ensure_ascii=False,
                    indent=2,
                )
            )
            file.write("\n```\n\n")

            file.write("### Problem\n\n")
            file.write(
                f"{record['problem']}\n\n"
            )

            file.write("### Response\n\n")
            file.write("```text\n")
            file.write(
                str(record["response"])
            )
            file.write("\n```\n\n")

            file.write("### Manual review\n\n")
            file.write(
                "- Relevant: \n"
                "- Primary category: \n"
                "- Notes: \n\n"
            )

            file.write("---\n\n")


def save_summary(
    source_count: int,
    matched_before_limit: dict[str, int],
    selected_category_records: dict[
        str,
        list[dict[str, Any]],
    ],
    final_records: list[dict[str, Any]],
    args: argparse.Namespace,
) -> None:
    category_membership_counter: Counter[str] = Counter()

    for record in final_records:
        for category in record["v2_categories"]:
            category_membership_counter[category] += 1

    summary = {
        "source_count": source_count,
        "category_limit": args.category_limit,
        "max_total": args.max_total,
        "seed": args.seed,
        "matched_before_limit": matched_before_limit,
        "selected_per_category_before_deduplication": {
            category: len(records)
            for category, records
            in selected_category_records.items()
        },
        "final_unique_count": len(final_records),
        "final_unique_rate": (
            len(final_records) / source_count
        ),
        "final_category_membership": dict(
            category_membership_counter
        ),
    }

    summary_path = (
        args.output_dir / "summary.json"
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

    if args.category_limit <= 0:
        raise ValueError(
            "--category-limit must be greater than 0."
        )

    if args.max_total <= 0:
        raise ValueError(
            "--max-total must be greater than 0."
        )

    if args.review_limit < 0:
        raise ValueError(
            "--review-limit must not be negative."
        )

    source_records = load_jsonl(
        args.input_path
    )

    matched_records: list[
        dict[str, Any]
    ] = []

    for record in source_records:
        matches = find_matches(record)

        if not matches:
            continue

        matched_records.append(
            build_candidate_record(
                record=record,
                matches=matches,
            )
        )

    random_generator = random.Random(
        args.seed
    )

    category_candidates: dict[
        str,
        list[dict[str, Any]],
    ] = {
        match_function.__name__.replace(
            "match_",
            "",
        ): []
        for match_function in MATCH_FUNCTIONS
    }

    # 使用 MatchResult 中的正式类别名，
    # 避免依赖函数名。
    category_candidates = {
        "percentage_fraction": [],
        "price_quantity_total": [],
        "remaining_change": [],
        "equation_multistep": [],
    }

    for record in matched_records:
        for category in record["v2_categories"]:
            category_candidates[category].append(
                record
            )

    matched_before_limit = {
        category: len(records)
        for category, records
        in category_candidates.items()
    }

    selected_category_records: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    for category, records in (
        category_candidates.items()
    ):
        selected = select_category_records(
            records=records,
            category=category,
            limit=args.category_limit,
            random_generator=random_generator,
        )

        selected_category_records[
            category
        ] = selected

    final_records = build_balanced_unique_set(
        category_records=(
            selected_category_records
        ),
        max_total=args.max_total,
    )

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_jsonl(
        records=final_records,
        path=args.output_dir
        / "all_candidates.jsonl",
    )

    for category, records in (
        selected_category_records.items()
    ):
        save_jsonl(
            records=records,
            path=args.output_dir
            / f"{category}.jsonl",
        )

        save_review_markdown(
            records=records,
            path=args.output_dir
            / f"{category}_review.md",
            title=f"{category} candidate review",
            review_limit=args.review_limit,
        )

    save_review_markdown(
        records=final_records,
        path=args.output_dir
        / "all_candidates_review.md",
        title="SFT V2 all candidate review",
        review_limit=args.review_limit,
    )

    save_summary(
        source_count=len(source_records),
        matched_before_limit=(
            matched_before_limit
        ),
        selected_category_records=(
            selected_category_records
        ),
        final_records=final_records,
        args=args,
    )

    print(
        f"Source records: {len(source_records)}"
    )

    print("\nMatched before limiting:")

    for category, count in (
        matched_before_limit.items()
    ):
        print(f"  {category}: {count}")

    print("\nSelected before deduplication:")

    for category, records in (
        selected_category_records.items()
    ):
        print(
            f"  {category}: {len(records)}"
        )

    print(
        f"\nFinal unique candidates: "
        f"{len(final_records)}"
    )

    print(
        f"Final candidate rate: "
        f"{len(final_records) / len(source_records):.2%}"
    )

    print(
        f"Output directory: "
        f"{args.output_dir}"
    )


if __name__ == "__main__":
    main()