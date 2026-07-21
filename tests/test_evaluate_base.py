import json
from pathlib import Path

from scripts.evaluate_base import (
    EvaluationResult,
    build_prompt,
    print_summary,
    save_results,
)
from src.evaluation.data import EvaluationItem


def test_build_prompt() -> None:
    item = EvaluationItem(
        id="algebra_001",
        problem="Solve for x: 2x + 3 = 11.",
        answer="4",
    )

    prompt = build_prompt(item)

    assert "Problem: Solve for x: 2x + 3 = 11." in prompt
    assert "step-by-step solution" in prompt
    assert prompt.endswith("Response:")


def test_save_results(tmp_path: Path) -> None:
    output_path = tmp_path / "evaluation" / "results.jsonl"

    results = [
        EvaluationResult(
            id="algebra_001",
            problem="Solve for x: 2x + 3 = 11.",
            reference_answer="4",
            model_output="Therefore x = 4.",
            predicted_answer="4",
            correct=True,
            generated_tokens=8,
            truncated=False,
        )
    ]

    save_results(results, output_path)

    assert output_path.is_file()

    record = json.loads(
        output_path.read_text(encoding="utf-8").strip()
    )

    assert record["id"] == "algebra_001"
    assert record["predicted_answer"] == "4"
    assert record["correct"] is True
    assert record["truncated"] is False


def test_print_summary(capsys) -> None:
    results = [
        EvaluationResult(
            id="item_001",
            problem="Problem 1",
            reference_answer="4",
            model_output="4",
            predicted_answer="4",
            correct=True,
            generated_tokens=10,
            truncated=False,
        ),
        EvaluationResult(
            id="item_002",
            problem="Problem 2",
            reference_answer="5",
            model_output="6",
            predicted_answer="6",
            correct=False,
            generated_tokens=20,
            truncated=True,
        ),
    ]

    print_summary(results)

    captured = capsys.readouterr().out

    assert "Total items: 2" in captured
    assert "Correct items: 1" in captured
    assert "Answer accuracy: 50.00%" in captured
    assert "Answer parse rate: 100.00%" in captured
    assert "Average generated tokens: 15.00" in captured
    assert "Truncated outputs: 1" in captured
    assert "Truncation rate: 50.00%" in captured