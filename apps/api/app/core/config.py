from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "development"
    app_secret_key: str = "development-only-secret-change-me-please"
    database_url: str = "postgresql+asyncpg://innovagro:innovagro@localhost:5432/innovagro"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000"]
    access_token_minutes: int = 15
    refresh_token_days: int = 30

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        return value.split(",") if isinstance(value, str) else value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

