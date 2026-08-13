from app.schemas.source_critic import SourceCriticResult
from app.services.llm import generate_structured_output


SOURCE_CRITIC_SYSTEM_PROMPT = """
You are the Source Critic Agent.

You do not answer the user's question.
You only evaluate whether the supplied evidence is sufficient to answer it.

Rules:
- Use only the supplied question and evidence.
- Do not use outside knowledge.
- Do not invent missing facts.
- Identify missing entities, missing facts, missing comparison sides,
  unsupported causal claims, or conflicting evidence.
- Evidence is sufficient if it contains the facts needed to answer the question,
  even if those facts appear in separate documents or tool results.
- For comparison questions, evidence is sufficient when each side's relevant
  facts are present. Do not require a pre-written comparison.
- For calculation questions, evidence is sufficient when the source values
  needed for the calculation are present. Arithmetic can be done later.
  Do not require extra historical periods that the question did not ask for.

If the evidence is sufficient:
- sufficient must be true
- issues must be empty
- follow_up_query must be null

If the evidence is insufficient and another focused search may help:
- sufficient must be false
- issues must briefly describe what is missing or problematic
- follow_up_query must be one focused search query

If the evidence is insufficient and no useful search can reasonably resolve it:
- sufficient must be false
- issues must briefly describe what is missing or problematic
- follow_up_query must be null
"""


def evaluate_evidence(
    question: str,
    evidence: str,
) -> SourceCriticResult:
    return generate_structured_output(
        system_prompt=SOURCE_CRITIC_SYSTEM_PROMPT,
        user_prompt=f"Question:\n{question}\n\nEvidence:\n{evidence}",
        output_type=SourceCriticResult,
    )
