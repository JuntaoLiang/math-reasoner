from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class EvaluationItem:
    id: str
    problem: str
    answer: str

def load_evaluation_items(file_path: str | Path) -> list[EvaluationItem]:
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Evaluation file not found:{path}")
    
    items: list[EvaluationItem] = []
    with path.open("r", encoding = "utf-8") as file:
        for line_number,line in enumerate(file, start = 1):
            line = line.strip()

            if not line:
                continue
            
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {error}"
                        ) from error
            required_fields = {"id", "problem", "answer"}
            missing_fields = required_fields -record.keys()

            if missing_fields:
                missing_text = ",".join(sorted(missing_fields))
                raise ValueError(
                        f"Missing required fields at line {line_number}:"
                        f"{missing_text}"
                        )

            item = EvaluationItem(
                    id = record["id"],
                    problem = record["problem"],
                    answer = record["answer"]
                    )
            items.append(item)
    if not items:
        raise ValueError(f"Evaluation file is empty:{path}")


    return items

