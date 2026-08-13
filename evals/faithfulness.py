from app.schemas.agent import AgentResult
from app.schemas.evaluation import (
    FaithfulnessEvaluation,
    FaithfulnessJudgeResult,
)
from app.services.llm import generate_structured_output


JUDGE_SYSTEM_PROMPT = """
You are an evaluation judge.

Determine whether the agent's final answer is fully supported by the evidence
that was available to the agent.

Rules:

- Evaluate factual claims in the agent answer against the provided evidence.
- A factual claim is supported only if the evidence directly supports it.
- Tool results are valid evidence.
- Treat calculator tool outputs as valid evidence.
- A calculated claim is supported when the calculator result follows directly
  from values and operations present in the provided tool evidence.
- Do not use outside knowledge.
- Do not infer facts that are not present in the evidence.
- Do not allow broader claims than the evidence supports.
- Do not allow unsupported superlatives, comparisons, dates, numbers,
  entities, or causal claims.
- If all factual claims are supported, faithful must be true.
- If any factual claim is unsupported, faithful must be false and include
  the unsupported claim in unsupported_claims.
"""


def evaluate_faithfulness(
    agent_result: AgentResult,
) -> FaithfulnessEvaluation:
    if not agent_result.traces:
        return FaithfulnessEvaluation(
            applicable=False,
            faithful=None,
            unsupported_claims=[],
            passed=None,
        )

    evidence_parts = []

    for trace in agent_result.traces:
        evidence_parts.append(f"Tool: {trace.tool_name}\nResult:\n{trace.result}")

    evidence = "\n\n".join(evidence_parts)

    judge_result = generate_structured_output(
        system_prompt=JUDGE_SYSTEM_PROMPT,
        user_prompt=(f"EVIDENCE:\n{evidence}\n\nAGENT ANSWER:\n{agent_result.answer}"),
        output_type=FaithfulnessJudgeResult,
    )

    return FaithfulnessEvaluation(
        applicable=True,
        faithful=judge_result.faithful,
        unsupported_claims=judge_result.unsupported_claims,
        passed=judge_result.faithful,
    )
