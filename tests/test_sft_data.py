import json
from pathlib import Path

import pytest

from src.data.sft import SFTItem, load_sft_items


def test_load_sft_items(tmp_path: Path) -> None:
    file_path = tmp_path / "train.jsonl"

    records = [
        {
            "id": "algebra_sft_001",
            "problem": "Solve for x: 2x + 3 = 11.",
            "response": "2x = 8, so x = 4.",
        },
        {
            "id": "arithmetic_sft_001",
            "problem": "Compute 37 + 58.",
            "response": "37 + 58 = 95.",
        },
    ]

    content = "\n".join(
        json.dumps(record)
        for record in records
    )

    file_path.write_text(
        content + "\n",
        encoding="utf-8",
    )

    items = load_sft_items(file_path)

    assert items == [
        SFTItem(
            id="algebra_sft_001",
            problem="Solve for x: 2x + 3 = 11.",
            response="2x = 8, so x = 4.",
        ),
        SFTItem(
            id="arithmetic_sft_001",
            problem="Compute 37 + 58.",
            response="37 + 58 = 95.",
        ),
    ]


def test_load_sft_items_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_sft_items(tmp_path / "missing.jsonl")


def test_load_sft_items_missing_field(tmp_path: Path) -> None:
    file_path = tmp_path / "train.jsonl"

    record = {
        "id": "algebra_sft_001",
        "problem": "Solve for x.",
    }

    file_path.write_text(
        json.dumps(record) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Missing required fields",
    ):
        load_sft_items(file_path)


@pytest.mark.parametrize(
    ("field", "record"),
    [
        (
            "id",
            {
                "id": " ",
                "problem": "Solve for x.",
                "response": "x = 4.",
            },
        ),
        (
            "problem",
            {
                "id": "item_001",
                "problem": "",
                "response": "x = 4.",
            },
        ),
        (
            "response",
            {
                "id": "item_001",
                "problem": "Solve for x.",
                "response": " ",
            },
        ),
    ],
)
def test_load_sft_items_empty_required_value(
    tmp_path: Path,
    field: str,
    record: dict[str, str],
) -> None:
    file_path = tmp_path / "train.jsonl"

    file_path.write_text(
        json.dumps(record) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match=f"Empty {field}",
    ):
        load_sft_items(file_path)


def test_load_sft_items_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "train.jsonl"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="SFT file is empty",
    ):
        load_sft_items(file_path)