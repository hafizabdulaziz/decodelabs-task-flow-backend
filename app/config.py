"""
Application configuration management using Pydantic BaseSettings.
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file explicitly with override=True to prioritize .env over system env vars
load_dotenv(override=True)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/task_flow_db"
    JWT_SECRET_KEY: str = "supersecretkey0123456789abcdefghijklmnopqrstuvwxyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_ENV: str = "development"
    EXTERNAL_API_KEY: str = "mock-api-key"
    EXTERNAL_API_BASE_URL: str = "https://api.open-meteo.com/v1"
    EXTERNAL_API_TIMEOUT: float = 5.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
