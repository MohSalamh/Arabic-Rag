from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-5.6-luna"
    embed_dim: int = 1536

    # PostgresSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str
    table_name: str = "documents_store"

    # Inngest
    inngest_api_base_url: str = "http://127.0.0.1:8288/v1"

    # Application
    app_name: str = "RAG Application"


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()