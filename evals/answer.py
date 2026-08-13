from app.schemas.evaluation import (
    AnswerEvaluation,
    EvaluationCase,
    FactEvaluation,
    FactJudgeResult,
)
from app.schemas.agent import AgentResult
from app.services.llm import client


JUDGE_SYSTEM_PROMPT = """
You are an evaluation judge.

Determine whether the expected fact is supported by the agent's answer.

Rules:

- Evaluate semantic meaning, not exact wording.
- A fact is supported if the answer clearly communicates the same information.
- Minor wording differences are acceptable.
- Do not give credit if an important value, entity, date, comparison,
  or condition is wrong.
- Do not infer information that is not present in the answer.
"""


def evaluate_answer(
    case: EvaluationCase,
    agent_result: AgentResult,
) -> AnswerEvaluation:
    if not case.should_answer or not case.expected_facts:
        return AnswerEvaluation(
            applicable=False,
            fact_results=[],
            correctness_score=None,
            passed=None,
        )

    fact_results = []

    for expected_fact in case.expected_facts:
        response = client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": JUDGE_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        f"Expected fact:\n{expected_fact}\n\n"
                        f"Agent answer:\n{agent_result.answer}"
                    ),
                },
            ],
            response_format=FactJudgeResult,
            temperature=0,
        )

        judge_result = response.choices[0].message.parsed

        supported = judge_result.supported if judge_result else False

        fact_results.append(
            FactEvaluation(
                fact=expected_fact,
                supported=supported,
            )
        )

    supported_count = sum(1 for result in fact_results if result.supported)

    correctness_score = supported_count / len(fact_results)

    return AnswerEvaluation(
        applicable=True,
        fact_results=fact_results,
        correctness_score=correctness_score,
        passed=correctness_score == 1.0,
    )
