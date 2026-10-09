from datetime import datetime
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "development"
    app_secret_key: str = "development-only-secret-change-me-please"
    database_url: str = "postgresql+asyncpg://innovagro:innovagro@localhost:5432/innovagro"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000"]
    evolution_api_url: str = ''
    evolution_api_key: str = ''
    evolution_instance: str = ''
    evolution_organization_id: str = ''
    evolution_webhook_secret: str = ''
    evolution_bot_enabled: bool = False
    evolution_excluded_phones: str = ''
    openai_api_key: str = ''
    gemini_api_key: str = ''
    whatsapp_ai_provider: Literal['openai', 'gemini'] = 'openai'
    whatsapp_ai_test_mode: bool = False
    whatsapp_ai_test_phones: str = ''
    whatsapp_ai_test_since: datetime | None = None
    whatsapp_ai_enabled: bool = False
    whatsapp_ai_model: str = ''
    whatsapp_ai_knowledge: str = Field(default='', max_length=8000)
    whatsapp_ai_daily_limit: int = Field(default=100, ge=1, le=1000)
    whatsapp_ai_required_fields: str = 'name,service,need'
    access_token_minutes: int = 15
    refresh_token_days: int = 30

    @field_validator('whatsapp_ai_required_fields')
    @classmethod
    def qualification_fields(cls, value):
        fields = [field.strip() for field in value.split(',')]
        if not fields or any(field not in ('name', 'company', 'service', 'need') for field in fields):
            raise ValueError('Campos de qualificação inválidos.')
        return ','.join(dict.fromkeys(fields))

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        return value.split(",") if isinstance(value, str) else value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
