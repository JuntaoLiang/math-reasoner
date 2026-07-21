from __future__ import annotations

from transformers import PreTrainedTokenizerBase

from src.data.sft import SFTItem


IGNORE_INDEX = -100


def build_sft_prompt(item: SFTItem) -> str:
    return (
        f"Problem: {item.problem}\n"
        "Provide a clear step-by-step solution and a final answer.\n"
        "Response:"
    )


def format_sft_text(
    item: SFTItem,
    eos_token: str,
) -> str:
    prompt = build_sft_prompt(item)

    return f"{prompt}{item.response}{eos_token}"


def tokenize_sft_item(
    item: SFTItem,
    tokenizer: PreTrainedTokenizerBase,
    max_length: int,
) -> dict[str, list[int]]:
    if max_length <= 0:
        raise ValueError("max_length must be greater than zero.")

    if tokenizer.eos_token is None:
        raise ValueError("Tokenizer must define an EOS token.")

    prompt = build_sft_prompt(item)
    response = f"{item.response}{tokenizer.eos_token}"

    prompt_ids = tokenizer(
        prompt,
        add_special_tokens=False,
    )["input_ids"]

    response_ids = tokenizer(
        response,
        add_special_tokens=False,
    )["input_ids"]

    input_ids = (prompt_ids + response_ids)[:max_length]

    prompt_length = min(
        len(prompt_ids),
        len(input_ids),
    )

    if len(input_ids) <= prompt_length:
        raise ValueError(
            "max_length is too small to include response tokens."
        )

    labels = (
        [IGNORE_INDEX] * prompt_length
        + input_ids[prompt_length:]
    )

    attention_mask = [1] * len(input_ids)

    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
    }