from pydantic import BaseModel, Field


class SourceCriticResult(BaseModel):
    sufficient: bool
    issues: list[str] = Field(default_factory=list)
    follow_up_query: str | None = None


class SourceCriticTrace(BaseModel):
    round: int
    sufficient: bool
    issues: list[str]
    follow_up_query: str | None
