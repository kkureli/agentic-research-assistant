from pydantic import BaseModel, field_validator

from app.core.config import settings


class ResearchRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        if len(value) > settings.max_question_length:
            raise ValueError("Question is too long.")

        return value


class ResearchResponse(BaseModel):
    answer: str
    citations: list[str]
    tool_calls: int
    research_llm_calls: int
    critic_llm_calls: int
    critic_rounds: int
