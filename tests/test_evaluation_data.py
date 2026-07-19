import json
from pathlib import Path

import pytest

from src.evaluation.data import EvaluationItem, load_evaluation_items


def test_load_evaluation_items(tmp_path: Path) -> None:
    file_path = tmp_path / "evaluation.jsonl"

    records = [
        {
            "id": "algebra_001",
            "problem": "Solve for x: 2x + 3 = 11.",
            "answer": "4",
        },
        {
            "id": "arithmetic_001",
            "problem": "Compute: 37 + 58.",
            "answer": "95",
        },
    ]

    with file_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

    items = load_evaluation_items(file_path)

    assert items == [
        EvaluationItem(
            id="algebra_001",
            problem="Solve for x: 2x + 3 = 11.",
            answer="4",
        ),
        EvaluationItem(
            id="arithmetic_001",
            problem="Compute: 37 + 58.",
            answer="95",
        ),
    ]


def test_load_evaluation_items_missing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.jsonl"

    with pytest.raises(FileNotFoundError):
        load_evaluation_items(file_path)


def test_load_evaluation_items_missing_field(tmp_path: Path) -> None:
    file_path = tmp_path / "evaluation.jsonl"

    record = {
        "id": "algebra_001",
        "problem": "Solve for x: 2x + 3 = 11.",
    }

    file_path.write_text(
        json.dumps(record) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Missing required fields",
    ):
        load_evaluation_items(file_path)


def test_load_evaluation_items_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "evaluation.jsonl"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Evaluation file is empty",
    ):
        load_evaluation_items(file_path)
