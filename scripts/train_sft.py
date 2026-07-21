from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    Trainer,
    TrainingArguments,
    set_seed,
)

from src.data.sft import load_sft_items
from src.data.sft_dataset import SFTDataCollator, build_sft_dataset


@dataclass
class SFTTrainingConfig:
    model_path: str
    train_data_path: str
    output_dir: str
    max_length: int
    num_train_epochs: int
    per_device_train_batch_size: int
    gradient_accumulation_steps: int
    learning_rate: float
    logging_steps: int
    save_steps: int
    seed: int
    lora_r: int
    lora_alpha: int
    lora_dropout: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run QLoRA supervised fine-tuning."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/sft/qwen3_1_7b_qlora.json"),
    )
    return parser.parse_args()


def load_config(path: Path) -> SFTTrainingConfig:
    if not path.is_file():
        raise FileNotFoundError(f"Training config not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        record: dict[str, Any] = json.load(file)

    return SFTTrainingConfig(**record)


def load_tokenizer(model_path: str):
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    return tokenizer


def load_qlora_model(config: SFTTrainingConfig):
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        config.model_path,
        quantization_config=quantization_config,
        device_map="auto",
        dtype=torch.bfloat16,
    )

    model.config.use_cache = False

    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=True,
    )

    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
    )

    model = get_peft_model(
        model,
        lora_config,
    )

    return model


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    set_seed(config.seed)

    tokenizer = load_tokenizer(config.model_path)

    items = load_sft_items(
        config.train_data_path
    )

    train_dataset = build_sft_dataset(
        items=items,
        tokenizer=tokenizer,
        max_length=config.max_length,
    )

    data_collator = SFTDataCollator(
        tokenizer=tokenizer,
        pad_to_multiple_of=8,
    )

    model = load_qlora_model(config)
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=(
            config.per_device_train_batch_size
        ),
        gradient_accumulation_steps=(
            config.gradient_accumulation_steps
        ),
        learning_rate=config.learning_rate,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        save_total_limit=2,
        bf16=True,
        fp16=False,
        optim="paged_adamw_8bit",
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.01,
        gradient_checkpointing=True,
        report_to="none",
        remove_unused_columns=False,
        seed=config.seed,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        processing_class=tokenizer,
    )

    train_result = trainer.train()

    trainer.save_model(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)

    print("\nTraining completed")
    print(f"Training loss: {train_result.training_loss:.6f}")
    print(f"Adapter saved to: {config.output_dir}")


if __name__ == "__main__":
    main()