from pydantic import BaseModel


class RetrievalFilter(BaseModel):
    company_query: str | None = None
    year: int | None = None
    quarter: int | None = None
    document_type: str | None = None


class RankedDocument(BaseModel):
    chunk_id: str
    score: float


class RerankResult(BaseModel):
    results: list[RankedDocument]
