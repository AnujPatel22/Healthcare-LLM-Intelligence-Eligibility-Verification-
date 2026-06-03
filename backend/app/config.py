from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Healthcare LLM Eligibility Service"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://healthcare:healthcare@db:5432/healthcare_llm"
    frontend_origin: str = "http://localhost:5173"
    llm_provider: str = "mock"
    llm_api_key: str | None = None
    seed_on_startup: bool = True
    embedding_dimensions: int = 16

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
