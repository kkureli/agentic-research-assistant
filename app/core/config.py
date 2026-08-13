from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Research Assistant"
    app_env: str = "development"
    debug: bool = False

    openai_api_key: str

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "research_documents"
    tavily_api_key: str

    research_timeout_seconds: int = 120
    research_max_question_length: int = 2000
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
    )


settings = Settings()
