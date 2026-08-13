from typing import Literal

from pydantic import BaseModel, Field

ToolName = Literal[
    "search_knowledge_base",
    "search_web",
    "calculate",
]

CitationPrefix = Literal[
    "S",
    "W",
]

EvaluationCategory = Literal[
    "internal_retrieval",
    "web_research",
    "calculation",
    "multi_tool",
    "insufficient_evidence",
]


class EvaluationCase(BaseModel):
    id: str
    question: str
    category: EvaluationCategory

    required_tools: list[ToolName] = Field(default_factory=list)
    forbidden_tools: list[ToolName] = Field(default_factory=list)

    relevant_sources: list[str] = Field(default_factory=list)

    expected_facts: list[str] = Field(default_factory=list)

    expected_citation_prefixes: list[CitationPrefix] = Field(default_factory=list)

    should_answer: bool = True


class ToolRoutingEvaluation(BaseModel):
    required_tools: list[ToolName]
    actual_tools: list[ToolName]
    forbidden_tools_used: list[ToolName]

    missing_required_tools: list[ToolName]

    passed: bool


class RetrievalEvaluation(BaseModel):
    relevant_sources: list[str]
    retrieved_sources: list[str]
    missing_sources: list[str]

    applicable: bool
    passed: bool | None

    recall: float | None
    precision: float | None
    reciprocal_rank: float | None
    ndcg: float | None


class FactEvaluation(BaseModel):
    fact: str
    supported: bool


class AnswerEvaluation(BaseModel):
    applicable: bool
    fact_results: list[FactEvaluation]
    correctness_score: float | None
    passed: bool | None


class FactJudgeResult(BaseModel):
    supported: bool


class InsufficientEvidenceEvaluation(BaseModel):
    applicable: bool
    correctly_declined: bool | None
    passed: bool | None


class InsufficientEvidenceJudgeResult(BaseModel):
    correctly_declined: bool


class FaithfulnessJudgeResult(BaseModel):
    faithful: bool
    unsupported_claims: list[str]


class FaithfulnessEvaluation(BaseModel):
    applicable: bool
    faithful: bool | None
    unsupported_claims: list[str]
    passed: bool | None


class CitationEvaluation(BaseModel):
    applicable: bool
    found_citations: list[str] = Field(default_factory=list)
    available_citations: list[str] = Field(default_factory=list)
    invalid_citations: list[str] = Field(default_factory=list)
    missing_prefixes: list[str] = Field(default_factory=list)
    passed: bool | None


class TrajectoryEvaluation(BaseModel):
    applicable: bool
    tool_call_count: int
    max_step: int
    duplicate_tool_calls: int
    excessive_tool_calls: bool
    passed: bool | None


class ObservabilityMetrics(BaseModel):
    latency_seconds: float
    tool_call_count: int
    llm_call_count: int


class CriticEvaluation(BaseModel):
    applicable: bool
    critic_rounds: int
    retry_count: int
    initially_sufficient: bool | None
    eventually_sufficient: bool | None
    passed: bool | None


class EvaluationResult(BaseModel):
    case_id: str
    question: str
    answer: str
    tool_routing: ToolRoutingEvaluation
    retrieval: RetrievalEvaluation
    answer_evaluation: AnswerEvaluation
    insufficient_evidence_evaluation: InsufficientEvidenceEvaluation
    faithfulness: FaithfulnessEvaluation
    citation_evaluation: CitationEvaluation
    trajectory_evaluation: TrajectoryEvaluation
    observability: ObservabilityMetrics
    critic_evaluation: CriticEvaluation
