from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SFTItem:
    id: str
    problem: str
    response: str


def load_sft_items(file_path: str | Path) -> list[SFTItem]:
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"SFT file not found: {path}")

    items: list[SFTItem] = []
    required_fields = {"id", "problem", "response"}

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {error}"
                ) from error

            if not isinstance(record, dict):
                raise ValueError(
                    f"SFT record at line {line_number} must be a JSON object."
                )

            missing_fields = required_fields - record.keys()

            if missing_fields:
                missing_text = ", ".join(sorted(missing_fields))
                raise ValueError(
                    f"Missing required fields at line {line_number}: "
                    f"{missing_text}"
                )

            item = SFTItem(
                id=str(record["id"]).strip(),
                problem=str(record["problem"]).strip(),
                response=str(record["response"]).strip(),
            )

            if not item.id:
                raise ValueError(f"Empty id at line {line_number}.")

            if not item.problem:
                raise ValueError(f"Empty problem at line {line_number}.")

            if not item.response:
                raise ValueError(f"Empty response at line {line_number}.")

            items.append(item)

    if not items:
        raise ValueError(f"SFT file is empty: {path}")

    return items