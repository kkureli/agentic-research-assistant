import json
from pathlib import Path

from app.schemas.evaluation import EvaluationCase


def load_evaluation_cases(
    path: Path = Path("evals/agent_cases.json"),
) -> list[EvaluationCase]:
    data = json.loads(path.read_text(encoding="utf-8"))

    return [EvaluationCase.model_validate(item) for item in data]
