from typing import Literal

from pydantic import BaseModel

DocumentType = Literal[
    "analyst_notes",
    "annual_report",
    "earnings_report",
    "industry_report",
    "market_summary",
    "methodology",
    "strategy_memo",
]


class RetrievalFilter(BaseModel):
    company_query: str | None = None
    year: int | None = None
    quarter: int | None = None
    document_type: DocumentType | None = None


class RankedDocument(BaseModel):
    chunk_id: str
    score: float


class RerankResult(BaseModel):
    results: list[RankedDocument]
