from pydantic import BaseModel


class DecomposedQuery(BaseModel):
    queries: list[str]


class RewrittenQuery(BaseModel):
    query: str
