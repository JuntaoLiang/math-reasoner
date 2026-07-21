from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch
from datasets import Dataset
from transformers import PreTrainedTokenizerBase

from src.data.sft import SFTItem
from src.data.sft_formatting import IGNORE_INDEX, tokenize_sft_item


def build_sft_dataset(
    items: list[SFTItem],
    tokenizer: PreTrainedTokenizerBase,
    max_length: int,
) -> Dataset:
    if not items:
        raise ValueError("SFT items must not be empty.")

    records = [
        tokenize_sft_item(
            item=item,
            tokenizer=tokenizer,
            max_length=max_length,
        )
        for item in items
    ]

    return Dataset.from_list(records)


@dataclass
class SFTDataCollator:
    tokenizer: PreTrainedTokenizerBase
    pad_to_multiple_of: int | None = 8

    def __call__(
        self,
        features: list[dict[str, list[int]]],
    ) -> dict[str, torch.Tensor]:
        if not features:
            raise ValueError("Features must not be empty.")

        pad_token_id = self.tokenizer.pad_token_id

        if pad_token_id is None:
            pad_token_id = self.tokenizer.eos_token_id

        if pad_token_id is None:
            raise ValueError(
                "Tokenizer must define a pad token or EOS token."
            )

        max_length = max(
            len(feature["input_ids"])
            for feature in features
        )

        if self.pad_to_multiple_of is not None:
            remainder = max_length % self.pad_to_multiple_of

            if remainder:
                max_length += self.pad_to_multiple_of - remainder

        batch: dict[str, list[list[int]]] = {
            "input_ids": [],
            "attention_mask": [],
            "labels": [],
        }

        for feature in features:
            current_length = len(feature["input_ids"])
            padding_length = max_length - current_length

            batch["input_ids"].append(
                feature["input_ids"]
                + [pad_token_id] * padding_length
            )
            batch["attention_mask"].append(
                feature["attention_mask"]
                + [0] * padding_length
            )
            batch["labels"].append(
                feature["labels"]
                + [IGNORE_INDEX] * padding_length
            )

        return {
            key: torch.tensor(value, dtype=torch.long)
            for key, value in batch.items()
        }