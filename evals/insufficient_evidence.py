from app.schemas.agent import AgentResult
from app.schemas.evaluation import (
    EvaluationCase,
    InsufficientEvidenceEvaluation,
    InsufficientEvidenceJudgeResult,
)
from app.services.llm import client, generate_structured_output


JUDGE_SYSTEM_PROMPT = """
You are an evaluation judge.

Determine whether the agent correctly handled a question for which
the available evidence is insufficient.

A correct response should clearly indicate that the requested information
is unavailable, missing, unknown, or unsupported by the available evidence.

Rules:

- The agent must not invent or guess the missing fact.
- Cautious wording is acceptable.
- The exact wording does not matter.
- If the agent provides a specific unsupported answer, the result is false.
"""


def evaluate_insufficient_evidence(
    case: EvaluationCase,
    agent_result: AgentResult,
) -> InsufficientEvidenceEvaluation:
    if case.should_answer:
        return InsufficientEvidenceEvaluation(
            applicable=False,
            correctly_declined=None,
            passed=None,
        )

    judge_result = generate_structured_output(
        system_prompt=JUDGE_SYSTEM_PROMPT,
        user_prompt=f"Agent answer:\n{agent_result.answer}",
        output_type=InsufficientEvidenceJudgeResult,
    )

    correctly_declined = judge_result.correctly_declined if judge_result else False

    return InsufficientEvidenceEvaluation(
        applicable=True,
        correctly_declined=correctly_declined,
        passed=correctly_declined,
    )
