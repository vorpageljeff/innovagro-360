"""Public, write-only website intake. No contact data is returned to callers."""
import hashlib
import re
from datetime import datetime, timedelta
from typing import Literal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert

from app.api.dependencies import DB
from app.core.config import settings
from app.models.crm import Lead, LeadActivity

router = APIRouter(prefix='/public', tags=['Site'])
SITE_ORIGIN = 'https://voragon.vercel.app'


class SiteIntake(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    submission_id: UUID
    name: str = Field(min_length=2, max_length=100)
    company: str = Field(default='', max_length=120)
    email: EmailStr = Field(max_length=254)
    phone: str = Field(max_length=25)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=80)
    service: str = Field(min_length=2, max_length=150)
    need: str = Field(min_length=3, max_length=1000)
    current: str = Field(default='', max_length=500)
    timing: Literal['Quero pedir um orçamento e começar em breve', 'Quero planejar para os próximos meses', 'Estou conhecendo as possibilidades']
    consent: Literal[True]
    website: str = Field(default='', max_length=200)  # Honeypot
    campaign: str = Field(default='', max_length=200)

    @field_validator('phone')
    @classmethod
    def phone_number(cls, value):
        if not re.fullmatch(r'[+()\d\s-]+', value):
            raise ValueError('Telefone inválido.')
        value = re.sub(r'\D', '', value)
        if len(value) in (10, 11):
            value = '55' + value
        if not re.fullmatch(r'55[1-9]\d[2-9]\d{7,8}', value):
            raise ValueError('Informe um telefone brasileiro com DDD.')
        return value


def intake_note(data):
    return '\n'.join([
        'Origem: site Voragon · cadastro solicitado pelo visitante',
        f'Nome: {data.name}', f'Empresa: {data.company or "Não informada"}',
        f'E-mail: {data.email}', f'Telefone: {data.phone}',
        f'Cidade: {data.city}', f'Estado ou país: {data.state}',
        f'Serviço: {data.service}', f'Necessidade: {data.need}',
        f'Situação atual: {data.current or "Não informada"}', f'Momento: {data.timing}',
        f'Campanha: {data.campaign or "Não informada"}',
        'Autorização: visitante solicitou contato sobre este projeto e armazenamento no CRM.',
    ])


async def persist_intake(data, db, organization_id):
    # Serialize intake for the configured tenant, including concurrent retries.
    lock = int.from_bytes(hashlib.sha256(str(organization_id).encode()).digest()[:8], 'big', signed=True)
    await db.execute(text('SELECT pg_advisory_xact_lock(:key)'), {'key': lock})
    key = f'site:{data.submission_id}'
    existing = (await db.execute(select(LeadActivity).where(
        LeadActivity.organization_id == organization_id, LeadActivity.event_key == key
    ))).scalar_one_or_none()
    note = intake_note(data)
    if existing:
        if existing.note != note:
            raise HTTPException(409, 'Este envio já foi recebido. Atualize a página para iniciar outra solicitação.')
        return {'received': True}
    now = datetime.now(ZoneInfo('America/Sao_Paulo'))
    recent = (await db.execute(select(func.count()).select_from(LeadActivity).where(
        LeadActivity.organization_id == organization_id,
        LeadActivity.event_key.like('site:%'),
        LeadActivity.created_at >= now - timedelta(hours=1),
    ))).scalar_one()
    if recent >= 100:
        raise HTTPException(429, 'Muitas solicitações. Tente novamente mais tarde ou fale pelo WhatsApp.')
    phones = [data.phone]
    if len(data.phone) == 13 and data.phone[4] == '9':
        phones.append(data.phone[:4] + data.phone[5:])
    elif len(data.phone) == 12:
        phones.append(data.phone[:4] + '9' + data.phone[4:])
    lead = (await db.execute(select(Lead).where(
        Lead.organization_id == organization_id, Lead.phone.in_(phones)
    ).order_by(Lead.created_at).with_for_update())).scalars().first()
    if lead:
        count = (await db.execute(select(func.count()).select_from(LeadActivity).where(
            LeadActivity.organization_id == organization_id, LeadActivity.lead_id == lead.id,
            LeadActivity.event_key.like('site:%'), LeadActivity.created_at >= now - timedelta(hours=1),
        ))).scalar_one()
        if count >= 3:
            raise HTTPException(429, 'Sua solicitação já foi recebida. Aguarde nosso contato ou continue pelo WhatsApp.')
    else:
        await db.execute(insert(Lead).values(
            id=uuid4(), organization_id=organization_id, name=data.name, instagram=None,
            city=f'{data.city} / {data.state}', phone=data.phone, status='respondeu',
            priority='alta' if data.timing.startswith('Quero pedir') else 'media',
            bot_paused=True, last_contact_on=now.date(), next_contact_on=None,
        ).on_conflict_do_nothing())
        lead = (await db.execute(select(Lead).where(
            Lead.organization_id == organization_id, Lead.phone == data.phone
        ).with_for_update())).scalar_one()
    # Preserve closed leads and existing names/history. New request is a note.
    if lead.status not in ('convertido', 'sem_interesse'):
        lead.bot_paused = True
        if data.timing.startswith('Quero pedir') and lead.priority != 'urgente':
            lead.priority = 'alta'
    db.add(LeadActivity(organization_id=organization_id, lead_id=lead.id, event_key=key,
                        kind='nota', occurred_on=now.date(), note=note))
    await db.commit()
    return {'received': True}


@router.post('/site-leads')
async def website_intake(data: SiteIntake, request: Request, db: DB):
    if request.headers.get('origin') != SITE_ORIGIN:
        raise HTTPException(403, 'Origem não permitida.')
    if data.website:
        raise HTTPException(422, 'Solicitação inválida.')
    try:
        organization_id = UUID(settings.evolution_organization_id)
    except ValueError:
        raise HTTPException(503, 'Cadastro indisponível. Continue pelo WhatsApp.')
    return await persist_intake(data, db, organization_id)
