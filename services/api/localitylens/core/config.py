"""
Application configuration — validated at startup.
All values come from environment variables (see .env.example).
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    APP_ENV: Literal["development", "staging", "production"] = "development"
    APP_BASE_URL: str = "http://localhost:3000"
    API_BASE_URL: str = "http://localhost:8000"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str

    # AI
    AI_PROVIDER: Literal["ollama", "mock", "remote"] = "mock"
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OLLAMA_MODEL: str = "mistral"
    AI_REQUEST_TIMEOUT_SECONDS: int = 90
    AI_MOCK_MODE: bool = True

    # Remote AI (optional)
    REMOTE_AI_ENABLED: bool = False
    REMOTE_AI_API_KEY: str = ""
    REMOTE_AI_MODEL: str = ""

    # Ingestion
    INGESTION_ENABLED: bool = False
    GEOCODING_PROVIDER: str = "none"
    MAX_SOURCE_DOWNLOAD_BYTES: int = 5_000_000
    SOURCE_FETCH_TIMEOUT_SECONDS: int = 15

    # Evidence storage
    EVIDENCE_STORAGE_BACKEND: Literal["local"] = "local"
    EVIDENCE_STORAGE_PATH: str = "./var/evidence"

    # Blockchain / TrustLayer
    CHAIN_ENABLED: bool = False
    CHAIN_ID: str = ""
    CHAIN_RPC_URL: str = ""
    EVIDENCE_REGISTRY_ADDRESS: str = ""
    ANCHOR_PRIVATE_KEY: str = ""
    ANCHOR_BATCH_SIZE: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
