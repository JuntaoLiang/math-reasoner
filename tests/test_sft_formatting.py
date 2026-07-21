from src.data.sft import SFTItem
from src.data.sft_formatting import (
    IGNORE_INDEX,
    build_sft_prompt,
    format_sft_text,
    tokenize_sft_item,
)


class FakeTokenizer:
    eos_token = "<eos>"

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


def create_item() -> SFTItem:
    return SFTItem(
        id="algebra_sft_001",
        problem="Solve for x: 2x + 3 = 11.",
        response="2x = 8, so x = 4.",
    )


def test_build_sft_prompt() -> None:
    item = create_item()

    prompt = build_sft_prompt(item)

    assert item.problem in prompt
    assert "step-by-step solution" in prompt
    assert prompt.endswith("Response:")


def test_format_sft_text() -> None:
    item = create_item()

    text = format_sft_text(
        item,
        eos_token="<eos>",
    )

    assert text.startswith("Problem:")
    assert item.response in text
    assert text.endswith("<eos>")


def test_tokenize_sft_item() -> None:
    item = create_item()
    tokenizer = FakeTokenizer()

    tokenized = tokenize_sft_item(
        item=item,
        tokenizer=tokenizer,
        max_length=1024,
    )

    prompt_length = len(
        build_sft_prompt(item)
    )

    assert len(tokenized["input_ids"]) == len(
        tokenized["attention_mask"]
    )
    assert len(tokenized["input_ids"]) == len(
        tokenized["labels"]
    )

    assert tokenized["labels"][:prompt_length] == (
        [IGNORE_INDEX] * prompt_length
    )

    assert tokenized["labels"][prompt_length:] == (
        tokenized["input_ids"][prompt_length:]
    )

    assert all(
        value == 1
        for value in tokenized["attention_mask"]
    )


def test_tokenize_sft_item_truncates() -> None:
    item = create_item()
    tokenizer = FakeTokenizer()

    prompt_length = len(
        build_sft_prompt(item)
    )

    max_length = prompt_length + 5

    tokenized = tokenize_sft_item(
        item=item,
        tokenizer=tokenizer,
        max_length=max_length,
    )

    assert len(tokenized["input_ids"]) == max_length
    assert len(tokenized["labels"]) == max_length


def test_tokenize_sft_item_rejects_prompt_only() -> None:
    item = create_item()
    tokenizer = FakeTokenizer()

    prompt_length = len(
        build_sft_prompt(item)
    )

    try:
        tokenize_sft_item(
            item=item,
            tokenizer=tokenizer,
            max_length=prompt_length,
        )
    except ValueError as error:
        assert "too small" in str(error)
    else:
        raise AssertionError("Expected ValueError.")