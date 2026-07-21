import json
from pathlib import Path


def load_results(path: str) -> dict[str, dict]:
    records: dict[str, dict] = {}

    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                record = json.loads(line)
                records[record["id"]] = record

    return records


base_results = load_results(
    "outputs/evaluation/base_results.jsonl"
)
sft_results = load_results(
    # "outputs/evaluation/sft_smoke_results.jsonl"
    "outputs/evaluation/gsm8k_100_results.jsonl"
)

for item_id in base_results:
    base_output = base_results[item_id]["model_output"]
    sft_output = sft_results[item_id]["model_output"]

    print(f"\nItem: {item_id}")
    print(f"Exactly equal: {base_output == sft_output}")
    print(f"Base length: {len(base_output)}")
    print(f"SFT length: {len(sft_output)}")