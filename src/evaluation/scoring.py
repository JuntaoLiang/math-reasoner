from __future__ import annotations

import re


NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")


def extract_final_answer(text: str) -> str | None:
    matches = NUMBER_PATTERN.findall(text)

    if not matches:
        return None

    return matches[-1]


def normalize_answer(answer: str) -> str:
    normalized = answer.strip()

    try:
        number = float(normalized)
    except ValueError:
        return normalized.lower()

    if number.is_integer():
        return str(int(number))

    return str(number)


def is_correct(
    predicted_answer: str | None,
    reference_answer: str,
) -> bool:
    if predicted_answer is None:
        return False

    return normalize_answer(predicted_answer) == normalize_answer(
        reference_answer
    )
