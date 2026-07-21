import json
from pathlib import Path

import pytest

from scripts.prepare_gsm8k_evaluation import (
    convert_file,
    extract_reference_answer,
)


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        ("The answer is 42.\n#### 42", "42"),
        ("Final result.\n#### 1,250", "1250"),
        ("Final result.\n#### -3.5", "-3.5"),
    ],
)
def test_extract_reference_answer(
    response: str,
    expected: str,
) -> None:
    assert extract_reference_answer(response) == expected


def test_extract_reference_answer_rejects_missing_marker() -> None:
    with pytest.raises(ValueError, match="Could not extract"):
        extract_reference_answer("The answer is 42.")


def test_convert_file(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "test.jsonl"
    output_path = tmp_path / "evaluation.jsonl"

    input_record = {
        "id": "gsm8k_test_00001",
        "problem": "What is 20 + 22?",
        "response": "20 + 22 = 42.\n#### 42",
    }

    input_path.write_text(
        json.dumps(input_record) + "\n",
        encoding="utf-8",
    )

    count = convert_file(
        input_path=input_path,
        output_path=output_path,
    )

    output_record = json.loads(
        output_path.read_text(
            encoding="utf-8"
        ).strip()
    )

    assert count == 1
    assert output_record == {
        "id": "gsm8k_test_00001",
        "problem": "What is 20 + 22?",
        "answer": "42",
    }


def test_convert_file_respects_limit(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "test.jsonl"
    output_path = tmp_path / "evaluation.jsonl"

    records = [
        {
            "id": f"item_{index}",
            "problem": f"Problem {index}",
            "response": f"Solution.\n#### {index}",
        }
        for index in range(1, 4)
    ]

    input_path.write_text(
        "".join(
            json.dumps(record) + "\n"
            for record in records
        ),
        encoding="utf-8",
    )

    count = convert_file(
        input_path=input_path,
        output_path=output_path,
        limit=2,
    )

    output_lines = output_path.read_text(
        encoding="utf-8"
    ).splitlines()

    assert count == 2
    assert len(output_lines) == 2


@pytest.mark.parametrize(
    "limit",
    [0, -1],
)
def test_convert_file_rejects_invalid_limit(
    tmp_path: Path,
    limit: int,
) -> None:
    input_path = tmp_path / "test.jsonl"
    output_path = tmp_path / "evaluation.jsonl"

    input_path.write_text(
        json.dumps(
            {
                "id": "item_1",
                "problem": "Problem 1",
                "response": "Solution.\n#### 1",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="limit must be greater than zero",
    ):
        convert_file(
            input_path=input_path,
            output_path=output_path,
            limit=limit,
        )