from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.rag.entity_resolution import resolve_company
from app.schemas.retrieval import RetrievalFilter
from app.services.llm import generate_structured_output


KNOWN_COMPANIES = [
    "Asteria Cloud Systems",
    "Nova Mobility",
]


METADATA_FILTER_SYSTEM_PROMPT = f"""
You extract retrieval filters from research questions.

Known companies:
{chr(10).join(f"- {company}" for company in KNOWN_COMPANIES)}

Rules:

- Extract the company mentioned by the user.
- If the company name contains a clear typo, abbreviation, or shortened form,
  map it to the closest known company.
- Do not guess when the company is ambiguous.

- Extract year as an integer only when explicitly present.
- Extract quarter as an integer from 1 to 4 only when explicitly present.

- Extract document_type only when the user explicitly refers to a known document category.

- Allowed document_type values are:
  - analyst_notes
  - annual_report
  - earnings_report
  - industry_report
  - market_summary
  - methodology
  - strategy_memo

- Do not infer document_type from the topic of the question.

- For example, these are topics and must not be treated as document types:
  - bookings
  - revenue
  - growth
  - risks
  - AI adoption
  - margins
  - guidance
  - customers

- If the user asks about a topic without explicitly naming a document category,
  set document_type to None.

- Do not infer missing metadata values.
- Use actual None when a filter is not present.
- Never return the strings "None" or "null".
"""


def extract_retrieval_filter(query: str) -> RetrievalFilter:
    return generate_structured_output(
        system_prompt=METADATA_FILTER_SYSTEM_PROMPT,
        user_prompt=query,
        output_type=RetrievalFilter,
    )


def build_qdrant_filter(
    retrieval_filter: RetrievalFilter,
) -> Filter | None:
    conditions = []

    company_id = resolve_company(retrieval_filter.company_query)

    if company_id is not None:
        conditions.append(
            FieldCondition(
                key="company_id",
                match=MatchValue(value=company_id),
            )
        )

    if retrieval_filter.year is not None:
        conditions.append(
            FieldCondition(
                key="year",
                match=MatchValue(value=retrieval_filter.year),
            )
        )

    if retrieval_filter.quarter is not None:
        conditions.append(
            FieldCondition(
                key="quarter",
                match=MatchValue(value=retrieval_filter.quarter),
            )
        )

    if retrieval_filter.document_type is not None:
        conditions.append(
            FieldCondition(
                key="document_type",
                match=MatchValue(value=retrieval_filter.document_type),
            )
        )

    if not conditions:
        return None

    return Filter(must=conditions)
