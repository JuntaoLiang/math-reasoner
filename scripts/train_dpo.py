from __future__ import annotations

import argparse
import inspect
import json
import random
from pathlib import Path
from typing import Any

import torch
from datasets import Dataset
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    set_seed,
)
from trl import DPOConfig, DPOTrainer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Continue training an existing SFT LoRA adapter "
            "with GSM8K DPO preference pairs."
        )
    )

    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the DPO JSON configuration file.",
    )

    parser.add_argument(
        "--resume-from-checkpoint",
        type=str,
        default=None,
        help=(
            "Optional Trainer checkpoint path. "
            "Use 'latest' to resume from the last checkpoint."
        ),
    )

    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "Configuration root must be a JSON object."
        )

    return data


def validate_config(config: dict[str, Any]) -> None:
    required_fields = {
        "model_path",
        "sft_adapter_path",
        "train_data_path",
        "output_dir",
        "train_ratio",
        "seed",
        "max_length",
        "beta",
        "loss_type",
        "num_train_epochs",
        "per_device_train_batch_size",
        "per_device_eval_batch_size",
        "gradient_accumulation_steps",
        "learning_rate",
        "weight_decay",
        "warmup_ratio",
        "lr_scheduler_type",
        "logging_steps",
        "eval_steps",
        "save_steps",
        "save_total_limit",
        "gradient_checkpointing",
        "bf16",
        "report_to",
    }

    missing_fields = required_fields - config.keys()

    if missing_fields:
        raise ValueError(
            f"Missing configuration fields: "
            f"{sorted(missing_fields)}"
        )

    train_ratio = float(config["train_ratio"])

    if not 0.0 < train_ratio < 1.0:
        raise ValueError(
            "train_ratio must be between 0 and 1."
        )

    if int(config["max_length"]) <= 0:
        raise ValueError(
            "max_length must be greater than 0."
        )

    if float(config["beta"]) <= 0:
        raise ValueError(
            "beta must be greater than 0."
        )


def load_preference_records(
    path: Path,
) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Preference dataset not found: {path}"
        )

    records: list[dict[str, str]] = []
    seen_ids: set[str] = set()

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(
            file,
            start=1,
        ):
            line = line.strip()

            if not line:
                continue

            try:
                source_record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: "
                    f"{error}"
                ) from error

            if not isinstance(source_record, dict):
                raise ValueError(
                    f"Line {line_number} must contain "
                    "a JSON object."
                )

            required_fields = {
                "id",
                "prompt",
                "chosen",
                "rejected",
            }

            missing_fields = (
                required_fields
                - source_record.keys()
            )

            if missing_fields:
                raise ValueError(
                    f"Missing fields at line {line_number}: "
                    f"{sorted(missing_fields)}"
                )

            item_id = str(source_record["id"])

            if item_id in seen_ids:
                raise ValueError(
                    f"Duplicate preference ID: {item_id}"
                )

            seen_ids.add(item_id)

            prompt = str(
                source_record["prompt"]
            ).strip()

            chosen = str(
                source_record["chosen"]
            ).strip()

            rejected = str(
                source_record["rejected"]
            ).strip()

            if not prompt:
                raise ValueError(
                    f"Empty prompt for item: {item_id}"
                )

            if not chosen:
                raise ValueError(
                    f"Empty chosen response for item: "
                    f"{item_id}"
                )

            if not rejected:
                raise ValueError(
                    f"Empty rejected response for item: "
                    f"{item_id}"
                )

            if chosen == rejected:
                raise ValueError(
                    f"Chosen and rejected are identical: "
                    f"{item_id}"
                )

            # DPOTrainer 只需要这三个标准字段。
            records.append(
                {
                    "prompt": prompt,
                    "chosen": chosen,
                    "rejected": rejected,
                }
            )

    if not records:
        raise ValueError(
            f"Preference dataset is empty: {path}"
        )

    return records


def split_records(
    records: list[dict[str, str]],
    train_ratio: float,
    seed: int,
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
]:
    shuffled_records = list(records)

    random_generator = random.Random(seed)
    random_generator.shuffle(shuffled_records)

    train_count = int(
        len(shuffled_records) * train_ratio
    )

    # 确保训练集和验证集都不为空。
    train_count = max(
        1,
        min(
            train_count,
            len(shuffled_records) - 1,
        ),
    )

    train_records = shuffled_records[
        :train_count
    ]

    eval_records = shuffled_records[
        train_count:
    ]

    return train_records, eval_records


def load_policy_model(
    model_path: Path,
    adapter_path: Path,
    use_bf16: bool,
) -> tuple[
    PreTrainedTokenizerBase,
    PreTrainedModel,
]:
    if not model_path.is_dir():
        raise FileNotFoundError(
            f"Base model directory not found: "
            f"{model_path}"
        )

    if not adapter_path.is_dir():
        raise FileNotFoundError(
            f"SFT adapter directory not found: "
            f"{adapter_path}"
        )

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA is required for this DPO run, "
            "but no CUDA device is available."
        )

    dtype = (
        torch.bfloat16
        if use_bf16
        else torch.float32
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_path
    )

    # DPOTrainer 的处理器要求左侧 Padding。
    tokenizer.padding_side = "left"

    if tokenizer.pad_token_id is None:
        if tokenizer.eos_token_id is None:
            raise ValueError(
                "Tokenizer has neither pad_token_id "
                "nor eos_token_id."
            )

        tokenizer.pad_token = tokenizer.eos_token

    base_model = (
        AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=dtype,
        )
    )

    # 继续训练现有 SFT Adapter。
    # is_trainable=True 是关键，否则 Adapter 参数会被冻结。
    policy_model = PeftModel.from_pretrained(
        base_model,
        adapter_path,
        is_trainable=True,
    )

    policy_model.config.use_cache = False

    return tokenizer, policy_model


def build_dpo_config(
    config: dict[str, Any],
) -> DPOConfig:
    available_parameters = set(
        inspect.signature(
            DPOConfig
        ).parameters
    )

    requested_arguments: dict[str, Any] = {
        "output_dir": str(
            config["output_dir"]
        ),
        "num_train_epochs": float(
            config["num_train_epochs"]
        ),
        "per_device_train_batch_size": int(
            config[
                "per_device_train_batch_size"
            ]
        ),
        "per_device_eval_batch_size": int(
            config[
                "per_device_eval_batch_size"
            ]
        ),
        "gradient_accumulation_steps": int(
            config[
                "gradient_accumulation_steps"
            ]
        ),
        "learning_rate": float(
            config["learning_rate"]
        ),
        "weight_decay": float(
            config["weight_decay"]
        ),
        "warmup_ratio": float(
            config["warmup_ratio"]
        ),
        "lr_scheduler_type": str(
            config["lr_scheduler_type"]
        ),
        "logging_steps": int(
            config["logging_steps"]
        ),
        "eval_steps": int(
            config["eval_steps"]
        ),
        "save_steps": int(
            config["save_steps"]
        ),
        "save_total_limit": int(
            config["save_total_limit"]
        ),
        "gradient_checkpointing": bool(
            config["gradient_checkpointing"]
        ),
        "bf16": bool(
            config["bf16"]
        ),
        "report_to": str(
            config["report_to"]
        ),
        "seed": int(
            config["seed"]
        ),
        "beta": float(
            config["beta"]
        ),
        "loss_type": str(
            config["loss_type"]
        ),
        "max_length": int(
            config["max_length"]
        ),
        "eval_strategy": "steps",
        "save_strategy": "steps",
        "logging_strategy": "steps",
        "remove_unused_columns": False,
    }

    unsupported = (
        requested_arguments.keys()
        - available_parameters
    )

    if unsupported:
        raise RuntimeError(
            "The installed TRL DPOConfig does not "
            "support these arguments: "
            f"{sorted(unsupported)}. "
            "Check the installed TRL version."
        )

    return DPOConfig(
        **requested_arguments
    )


def print_trainable_parameters(
    model: PreTrainedModel,
) -> None:
    trainable_parameters = 0
    total_parameters = 0

    for parameter in model.parameters():
        parameter_count = parameter.numel()
        total_parameters += parameter_count

        if parameter.requires_grad:
            trainable_parameters += (
                parameter_count
            )

    trainable_rate = (
        trainable_parameters
        / total_parameters
    )

    print(
        f"Trainable parameters: "
        f"{trainable_parameters:,}"
    )

    print(
        f"Total parameters: "
        f"{total_parameters:,}"
    )

    print(
        f"Trainable rate: "
        f"{trainable_rate:.4%}"
    )


def main() -> None:
    args = parse_args()

    config = load_json(args.config)
    validate_config(config)

    seed = int(config["seed"])
    set_seed(seed)

    records = load_preference_records(
        Path(config["train_data_path"])
    )

    train_records, eval_records = (
        split_records(
            records=records,
            train_ratio=float(
                config["train_ratio"]
            ),
            seed=seed,
        )
    )

    train_dataset = Dataset.from_list(
        train_records
    )

    eval_dataset = Dataset.from_list(
        eval_records
    )

    print(
        f"Preference pairs: {len(records)}"
    )

    print(
        f"Train pairs: {len(train_dataset)}"
    )

    print(
        f"Evaluation pairs: "
        f"{len(eval_dataset)}"
    )

    print(
        f"Base model: {config['model_path']}"
    )

    print(
        "SFT adapter: "
        f"{config['sft_adapter_path']}"
    )

    print(
        f"Output directory: "
        f"{config['output_dir']}"
    )

    tokenizer, policy_model = (
        load_policy_model(
            model_path=Path(
                config["model_path"]
            ),
            adapter_path=Path(
                config["sft_adapter_path"]
            ),
            use_bf16=bool(
                config["bf16"]
            ),
        )
    )

    print_trainable_parameters(
        policy_model
    )

    training_args = build_dpo_config(
        config
    )

    trainer = DPOTrainer(
        model=policy_model,
        ref_model=None,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
    )

    resume_value: str | bool | None

    if (
        args.resume_from_checkpoint
        == "latest"
    ):
        resume_value = True
    else:
        resume_value = (
            args.resume_from_checkpoint
        )

    train_result = trainer.train(
        resume_from_checkpoint=resume_value
    )

    trainer.save_model(
        str(config["output_dir"])
    )

    tokenizer.save_pretrained(
        str(config["output_dir"])
    )

    trainer.save_state()

    trainer.log_metrics(
        "train",
        train_result.metrics,
    )

    trainer.save_metrics(
        "train",
        train_result.metrics,
    )

    eval_metrics = trainer.evaluate()

    trainer.log_metrics(
        "eval",
        eval_metrics,
    )

    trainer.save_metrics(
        "eval",
        eval_metrics,
    )

    print("\nDPO training completed.")
    print(
        f"Adapter saved to: "
        f"{config['output_dir']}"
    )


if __name__ == "__main__":
    main()