import secrets
from datetime import datetime, timezone
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, or_, select
from sqlalchemy.dialects.postgresql import insert

from app.api.dependencies import Auth, DB
from app.api.v1.automations import owns_integration
from app.core.config import settings
from app.models.crm import InstagramMessage, Lead, LeadActivity
from app.schemas.crm import ActivityInput
from app.services.crm import apply_activity

router = APIRouter(prefix="/crm/instagram", tags=["Instagram"])
DEFAULT_MESSAGE = ("Oi, equipe da {empresa}! Vi o trabalho de vocês e percebi uma oportunidade para organizar melhor "
    "a presença digital e facilitar o caminho de novos clientes até o atendimento. Trabalho com sites, "
    "sistemas e orientação em tecnologia. Posso compartilhar a ideia que pensei para vocês?")


class SentInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    request_id: UUID
    expected_instagram: str = Field(min_length=1, max_length=30)
    text: str = Field(min_length=1, max_length=1500)


class WebhookMessage(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    message_id: str = Field(min_length=1, max_length=200)
    instagram_scoped_user_id: str = Field(min_length=1, max_length=64)
    username: str | None = Field(default=None, max_length=30, pattern=r"^[a-zA-Z0-9._]+$")
    name: str | None = Field(default=None, max_length=160)
    direction: str = Field(pattern=r"^(incoming|outgoing)$")
    text: str = Field(default="", max_length=10000)
    attachment_type: str | None = Field(default=None, max_length=30)
    sent_at: datetime


class WebhookInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    messages: list[WebhookMessage] = Field(min_length=1, max_length=100)


def webhook_configured():
    try:
        return bool(settings.instagram_webhook_secret and UUID(settings.instagram_organization_id))
    except ValueError:
        return False


async def get_lead(db: DB, organization_id: UUID, lead_id: UUID, lock: bool = False) -> Lead:
    query = select(Lead).where(Lead.id == lead_id, Lead.organization_id == organization_id)
    if lock:
        query = query.with_for_update()
    lead = (await db.execute(query)).scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Contato não encontrado.")
    return lead


@router.get("/leads")
async def leads(db: DB, auth: Auth, q: str = Query(default="", max_length=160)):
    owns_integration(auth)
    query = select(Lead).where(Lead.organization_id == auth.organization_id,
        Lead.instagram.is_not(None))
    if q.strip():
        term = q.strip()
        query = query.where(or_(Lead.name.icontains(term, autoescape=True),
            Lead.city.icontains(term, autoescape=True),
            Lead.instagram.icontains(term, autoescape=True)))
    rows = (await db.execute(query.order_by(
        Lead.updated_at.desc(), Lead.name).limit(100))).scalars().all()
    counts = dict((await db.execute(select(LeadActivity.lead_id, func.count(LeadActivity.id)).where(
        LeadActivity.organization_id == auth.organization_id,
        LeadActivity.event_key.startswith("instagram-send:", autoescape=True))
        .group_by(LeadActivity.lead_id))).all())
    received = dict((await db.execute(select(InstagramMessage.lead_id,
        func.count(InstagramMessage.id)).where(
        InstagramMessage.organization_id == auth.organization_id,
        InstagramMessage.direction == "incoming", InstagramMessage.lead_id.is_not(None))
        .group_by(InstagramMessage.lead_id))).all())
    return {"items": [{"id": row.id, "name": row.name, "instagram": row.instagram,
        "city": row.city, "status": row.status, "priority": row.priority,
        "sent_count": counts.get(row.id, 0), "received_count": received.get(row.id, 0),
        "can_message": row.status not in {"sem_interesse", "convertido"}} for row in rows],
        "template": DEFAULT_MESSAGE}


@router.get("/leads/{lead_id}/conversation")
async def conversation(lead_id: UUID, db: DB, auth: Auth):
    owns_integration(auth)
    lead = await get_lead(db, auth.organization_id, lead_id)
    rows = (await db.execute(select(LeadActivity).where(
        LeadActivity.organization_id == auth.organization_id,
        LeadActivity.lead_id == lead.id,
        LeadActivity.event_key.startswith("instagram-send:", autoescape=True))
        .order_by(LeadActivity.created_at, LeadActivity.id).limit(100))).scalars().all()
    marker = "Mensagem enviada pelo Instagram:\n"
    messages = [{"id": row.id, "direction": "outgoing",
        "text": row.note.split(marker, 1)[1] if marker in row.note else row.note,
        "at": row.created_at, "source": "manual"} for row in rows]
    live = (await db.execute(select(InstagramMessage).where(
        InstagramMessage.organization_id == auth.organization_id,
        InstagramMessage.lead_id == lead.id).order_by(
        InstagramMessage.sent_at, InstagramMessage.id).limit(200))).scalars().all()
    messages.extend({"id": row.id, "direction": row.direction,
        "text": row.text or (f"Anexo recebido: {row.attachment_type}"
            if row.attachment_type else "Mensagem sem texto"),
        "at": row.sent_at, "source": "webhook"} for row in live)
    messages.sort(key=lambda item: (item["at"], str(item["id"])))
    return {"lead_id": lead.id, "instagram": lead.instagram, "status": lead.status,
        "messages": messages[-200:]}


@router.post("/leads/{lead_id}/sent")
async def record_sent(lead_id: UUID, data: SentInput, db: DB, auth: Auth):
    owns_integration(auth)
    lead = await get_lead(db, auth.organization_id, lead_id, True)
    if lead.instagram != data.expected_instagram:
        raise HTTPException(409, "O perfil mudou. Reabra a conversa antes de registrar o envio.")
    if lead.status in {"sem_interesse", "convertido"}:
        raise HTTPException(409, "Este contato está encerrado no CRM.")
    event_key = "instagram-send:" + str(data.request_id)
    note = "Mensagem enviada pelo Instagram:\n" + data.text
    existing = (await db.execute(select(LeadActivity).where(
        LeadActivity.organization_id == auth.organization_id,
        LeadActivity.event_key == event_key))).scalar_one_or_none()
    if existing:
        if existing.lead_id != lead.id or existing.note != note:
            raise HTTPException(409, "Este registro já foi usado com outros dados.")
        return {"state": "sent", "id": existing.id}
    today = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    activity = LeadActivity(organization_id=auth.organization_id, lead_id=lead.id,
        event_key=event_key, kind="contato", occurred_on=today, note=note)
    db.add(activity)
    apply_activity(lead, ActivityInput(kind="contato", occurred_on=today,
        event_key=event_key, note=note))
    await db.commit()
    await db.refresh(activity)
    return {"state": "sent", "id": activity.id}


@router.post("/webhook")
async def webhook(data: WebhookInput, db: DB,
                  x_instagram_webhook_secret: str = Header(default="")):
    if not webhook_configured() or not secrets.compare_digest(
            x_instagram_webhook_secret, settings.instagram_webhook_secret):
        raise HTTPException(401, "Webhook inválido.")
    organization_id = UUID(settings.instagram_organization_id)
    inserted = 0
    for item in data.messages:
        username = item.username.lower() if item.username else None
        lead = None
        if username:
            lead = (await db.execute(select(Lead).where(
                Lead.organization_id == organization_id, Lead.instagram == username)
                .with_for_update())).scalar_one_or_none()
        if not lead:
            lead_id = (await db.execute(select(InstagramMessage.lead_id).where(
                InstagramMessage.organization_id == organization_id,
                InstagramMessage.instagram_scoped_user_id == item.instagram_scoped_user_id,
                InstagramMessage.lead_id.is_not(None)).limit(1))).scalar_one_or_none()
            if lead_id:
                lead = await db.get(Lead, lead_id)
        if not lead and username and item.direction == "incoming":
            await db.execute(insert(Lead).values(id=uuid4(), organization_id=organization_id,
                name=item.name or f"@{username}", instagram=username, city="",
                status="respondeu", priority="alta", bot_paused=True)
                .on_conflict_do_nothing(constraint="uq_crm_lead_profile"))
            lead = (await db.execute(select(Lead).where(
                Lead.organization_id == organization_id, Lead.instagram == username)
                .with_for_update())).scalar_one()
        result = await db.execute(insert(InstagramMessage).values(
            id=uuid4(), organization_id=organization_id, message_id=item.message_id,
            lead_id=lead.id if lead else None,
            instagram_scoped_user_id=item.instagram_scoped_user_id, username=username,
            direction=item.direction, text=item.text, attachment_type=item.attachment_type,
            sent_at=item.sent_at.astimezone(timezone.utc)).on_conflict_do_nothing(
            constraint="uq_crm_instagram_message").returning(InstagramMessage.id))
        if result.scalar_one_or_none():
            inserted += 1
            if lead and item.direction == "incoming":
                lead.status = "respondeu"
                lead.priority = "alta"
                lead.next_contact_on = None
                lead.bot_paused = True
    await db.commit()
    return {"state": "received", "inserted": inserted}
