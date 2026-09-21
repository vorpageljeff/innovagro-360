import re
from datetime import date, datetime
from zoneinfo import ZoneInfo
from typing import Literal
from uuid import UUID
from urllib.parse import urlsplit
from pydantic import BaseModel, ConfigDict, Field, field_validator

Status = Literal['aguardando', 'respondeu', 'sem_interesse', 'convertido']

class LeadInput(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=160)
    instagram: str
    city: str = Field(default='', max_length=160)
    contacted_on: date
    event_key: str = Field(min_length=1, max_length=120)
    note: str = Field(default='', max_length=5000)

    @field_validator('contacted_on')
    @classmethod
    def past_date(cls, value: date) -> date:
        if value > datetime.now(ZoneInfo('America/Sao_Paulo')).date():
            raise ValueError('O contato realizado não pode estar no futuro.')
        return value

    @field_validator('instagram')
    @classmethod
    def profile(cls, value: str) -> str:
        value = value.strip().lower()
        if value.startswith(('https://', 'http://')):
            url = urlsplit(value)
            if url.hostname not in ('instagram.com', 'www.instagram.com'):
                raise ValueError('Informe um perfil do Instagram.')
            value = url.path.strip('/')
        value = value.removeprefix('@')
        if not re.fullmatch(r'[a-z0-9_](?:[a-z0-9_.]{0,28}[a-z0-9_])?', value) or '..' in value or value in {'p', 'reel', 'reels', 'stories', 'explore', 'direct'}:
            raise ValueError('Perfil do Instagram inválido.')
        return value

class ActivityInput(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    kind: Literal['contato', 'retorno', 'nota']
    occurred_on: date
    event_key: str = Field(min_length=1, max_length=120)
    note: str = Field(min_length=1, max_length=5000)
    status: Status | None = None
    next_contact_on: date | None = None

    @field_validator('occurred_on')
    @classmethod
    def past_date(cls, value: date) -> date:
        return LeadInput.past_date(value)

class ActivityOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    kind: str
    occurred_on: date
    note: str
    created_at: datetime

class LeadOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    instagram: str
    city: str
    status: str
    last_contact_on: date | None
    next_contact_on: date | None

class ImportInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    leads: list[LeadInput] = Field(min_length=1, max_length=100)
