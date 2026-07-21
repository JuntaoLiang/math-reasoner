import torch

from src.data.sft import SFTItem
from src.data.sft_dataset import (
    SFTDataCollator,
    build_sft_dataset,
)
from src.data.sft_formatting import IGNORE_INDEX


class FakeTokenizer:
    eos_token = "<eos>"
    eos_token_id = 0
    pad_token_id = 99

    def __call__(
        self,
        text: str,
        add_special_tokens: bool = False,
    ) -> dict[str, list[int]]:
        del add_special_tokens

        return {
            "input_ids": [
                ord(character)
                for character in text
            ]
        }


def create_items() -> list[SFTItem]:
    return [
        SFTItem(
            id="item_001",
            problem="Compute 2 + 2.",
            response="2 + 2 = 4.",
        ),
        SFTItem(
            id="item_002",
            problem="Compute 10 + 15.",
            response="10 + 15 = 25.",
        ),
    ]


def test_build_sft_dataset() -> None:
    tokenizer = FakeTokenizer()

    dataset = build_sft_dataset(
        items=create_items(),
        tokenizer=tokenizer,
        max_length=256,
    )

    assert len(dataset) == 2
    assert set(dataset.column_names) == {
        "input_ids",
        "attention_mask",
        "labels",
    }

    assert len(dataset[0]["input_ids"]) == len(
        dataset[0]["labels"]
    )


def test_sft_data_collator() -> None:
    tokenizer = FakeTokenizer()

    features = [
        {
            "input_ids": [1, 2, 3],
            "attention_mask": [1, 1, 1],
            "labels": [IGNORE_INDEX, 2, 3],
        },
        {
            "input_ids": [4, 5],
            "attention_mask": [1, 1],
            "labels": [IGNORE_INDEX, 5],
        },
    ]

    collator = SFTDataCollator(
        tokenizer=tokenizer,
        pad_to_multiple_of=4,
    )

    batch = collator(features)

    assert batch["input_ids"].shape == (2, 4)
    assert batch["attention_mask"].shape == (2, 4)
    assert batch["labels"].shape == (2, 4)

    assert batch["input_ids"][1].tolist() == [
        4,
        5,
        99,
        99,
    ]

    assert batch["attention_mask"][1].tolist() == [
        1,
        1,
        0,
        0,
    ]

    assert batch["labels"][1].tolist() == [
        IGNORE_INDEX,
        5,
        IGNORE_INDEX,
        IGNORE_INDEX,
    ]

    assert batch["input_ids"].dtype == torch.long


def test_sft_data_collator_rejects_empty_batch() -> None:
    tokenizer = FakeTokenizer()
    collator = SFTDataCollator(tokenizer=tokenizer)

    try:
        collator([])
    except ValueError as error:
        assert "must not be empty" in str(error)
    else:
        raise AssertionError("Expected ValueError.")