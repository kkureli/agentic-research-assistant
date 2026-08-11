from app.schemas.query import DecomposedQuery
from app.services.llm import generate_structured_output

DECOMPOSITION_SYSTEM_PROMPT = """
You are a research query planner.

Break complex research questions into smaller, independent queries
that can each be answered through document retrieval.

Rules:
- Preserve the meaning of the original question.
- Create separate queries only when the question requires information
  about multiple entities, periods, topics, or distinct subproblems.
- If the original question is already focused and independently retrievable,
  return it as a single query.
- Do not create unnecessary subqueries.
- Keep each query focused and independently retrievable.
- Do not answer the question.
"""


def decompose_query(query: str) -> list[str]:
    result = generate_structured_output(
        system_prompt=DECOMPOSITION_SYSTEM_PROMPT,
        user_prompt=query,
        output_type=DecomposedQuery,
    )

    return result.queries
