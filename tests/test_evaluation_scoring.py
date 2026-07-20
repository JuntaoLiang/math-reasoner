import pytest

from src.evaluation.scoring import (
    extract_final_answer,
    is_correct,
    normalize_answer,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("The answer is 4.", "4"),
        ("x = -3", "-3"),
        ("First 2, then the final answer is 7.5", "7.5"),
        ("No numeric answer", None),
    ],
)
def test_extract_final_answer(
    text: str,
    expected: str | None,
) -> None:
    assert extract_final_answer(text) == expected


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        ("4", "4"),
        ("4.0", "4"),
        (" 4 ", "4"),
        ("-3.50", "-3.5"),
        ("YES", "yes"),
    ],
)
def test_normalize_answer(
    answer: str,
    expected: str,
) -> None:
    assert normalize_answer(answer) == expected


@pytest.mark.parametrize(
    ("predicted", "reference", "expected"),
    [
        ("4", "4", True),
        ("4.0", "4", True),
        ("-3", "-3.0", True),
        ("5", "4", False),
        (None, "4", False),
    ],
)
def test_is_correct(
    predicted: str | None,
    reference: str,
    expected: bool,
) -> None:
    assert is_correct(predicted, reference) is expected
