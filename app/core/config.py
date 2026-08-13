from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Research Assistant"
    app_env: str = "development"
    debug: bool = False
    log_level: str | None = None

    openai_api_key: str
    openai_timeout_seconds: float = 30
    openai_max_retries: int = 2

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "research_documents"
    qdrant_timeout_seconds: float = 10

    tavily_api_key: str
    tavily_timeout_seconds: float = 15

    api_key: str = ""
    rate_limit_per_minute: int = 10

    max_agent_steps: int = 8
    max_critic_rounds: int = 2
    research_timeout_seconds: int = 120
    max_question_length: int = Field(
        default=2000,
        validation_alias=AliasChoices(
            "MAX_QUESTION_LENGTH",
            "RESEARCH_MAX_QUESTION_LENGTH",
        ),
    )
    max_tool_calls_per_request: int = 8

    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:8000",
        ]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized not in {"development", "test", "production"}:
            raise ValueError("APP_ENV must be development, test, or production")
        return normalized

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_test(self) -> bool:
        return self.app_env == "test"

    @property
    def auth_required(self) -> bool:
        return bool(self.api_key) or self.is_production

    @property
    def docs_enabled(self) -> bool:
        return not self.is_production

    @property
    def resolved_log_level(self) -> str:
        if self.log_level:
            return self.log_level.upper()
        if self.is_production:
            return "INFO"
        return "DEBUG" if self.debug else "INFO"

    @property
    def resolved_cors_origins(self) -> list[str]:
        if self.is_production and self.cors_origins == [
            "http://localhost:3000",
            "http://localhost:8000",
        ]:
            return []
        return self.cors_origins


settings = Settings()
