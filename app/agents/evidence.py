from app.schemas.agent import EvidenceAssessment
from app.services.llm import generate_structured_output


EVIDENCE_ASSESSMENT_PROMPT = """
You evaluate whether retrieved evidence is sufficient to answer a research question.

Rules:
- Determine whether the evidence directly supports the information needed to answer the question.
- Do not assume facts that are missing from the evidence.
- If evidence is insufficient, explain what is missing.
- When useful, provide one focused follow-up search query that could retrieve the missing evidence.
"""


def assess_evidence(
    question: str,
    evidence: str,
) -> EvidenceAssessment:
    user_prompt = f"""
Question:
{question}

Evidence:
{evidence}
"""

    return generate_structured_output(
        system_prompt=EVIDENCE_ASSESSMENT_PROMPT,
        user_prompt=user_prompt,
        output_type=EvidenceAssessment,
    )


if __name__ == "__main__":
    assessment = assess_evidence(
        question="What was Nova's employee headcount in Q2 2026?",
        evidence="Nova's Q2 revenue was $224 million.",
    )

    print(assessment)
