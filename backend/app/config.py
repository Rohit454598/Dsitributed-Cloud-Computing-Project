from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_embedding_model: str = "gemini-embedding-001"
    chroma_dir: str = str(BASE_DIR / "data" / "chroma")
    upload_dir: str = str(BASE_DIR / "data" / "uploads")
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    top_k: int = 5
    chunk_size: int = 1200
    chunk_overlap: int = 150
    max_textbooks_per_user: int = 5

    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    mongodb_db: str = "textbookgrade"

    firebase_project_id: str = ""
    firebase_credentials_file: str = str(BASE_DIR / "firebase-service-account.json")
    firebase_credentials_json: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
    return settings
