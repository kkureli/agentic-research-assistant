from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Research Assistant"
    app_env: str = "development"
    debug: bool = False

    openai_api_key: str

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "research_documents"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
