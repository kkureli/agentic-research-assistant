from app.schemas.query import RewrittenQuery
from app.services.llm import generate_structured_output

QUERY_REWRITE_SYSTEM_PROMPT = """
You rewrite queries for retrieval in a corporate research knowledge base.

The knowledge base contains company earnings reports, financial performance,
strategy documents, analyst notes, risks, guidance, revenue growth,
product adoption, and business performance.

Rules:
- Preserve the original meaning and intent.
- Do not introduce a more specific interpretation when the original query is ambiguous.
- Prefer terminology likely to appear in corporate and financial documents.
- Preserve company names, periods, dates, metrics, and other constraints.
- Do not invent specific facts, numbers, dates, causes, or metrics.
- Do not answer the question.
- Return exactly one rewritten retrieval query.
"""


def rewrite_query(query: str) -> str:
    result = generate_structured_output(
        system_prompt=QUERY_REWRITE_SYSTEM_PROMPT,
        user_prompt=query,
        output_type=RewrittenQuery,
    )

    return result.query


if __name__ == "__main__":
    query = "Why did Asteria slow down?"

    rewritten_query = rewrite_query(query)

    print(f"Original: {query}")
    print(f"Rewritten: {rewritten_query}")
