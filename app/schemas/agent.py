from pydantic import BaseModel


class AgentToolTrace(BaseModel):
    step: int
    tool_name: str
    arguments: dict
    result: str


class AgentResult(BaseModel):
    answer: str
    traces: list[AgentToolTrace]
    llm_call_count: int = 0


class EvidenceAssessment(BaseModel):
    sufficient: bool
    reason: str
    follow_up_query: str | None = None
