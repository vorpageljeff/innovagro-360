from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, or_, select

from app.api.dependencies import Auth, DB
from app.api.v1.automations import owns_integration
from app.models.crm import Lead, LeadActivity
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

async def get_lead(db: DB, organization_id: UUID, lead_id: UUID, lock: bool = False) -> Lead:
    query = select(Lead).where(Lead.organization_id == organization_id, Lead.id == lead_id)
    if lock: query = query.with_for_update()
    lead = (await db.execute(query)).scalar_one_or_none()
    if not lead: raise HTTPException(404, "Contato não encontrado.")
    return lead

@router.get("/leads")
async def leads(db: DB, auth: Auth, q: str = Query(default="", max_length=160)):
    owns_integration(auth)
    query = select(Lead).where(Lead.organization_id == auth.organization_id, Lead.instagram.is_not(None))
    if q.strip():
        term = q.strip()
        query = query.where(or_(Lead.name.icontains(term, autoescape=True), Lead.city.icontains(term, autoescape=True), Lead.instagram.icontains(term, autoescape=True)))
    rows = (await db.execute(query.order_by(Lead.updated_at.desc(), Lead.name).limit(100))).scalars().all()
    counts = dict((await db.execute(select(LeadActivity.lead_id, func.count(LeadActivity.id)).where(
        LeadActivity.organization_id == auth.organization_id,
        LeadActivity.event_key.startswith("instagram-send:", autoescape=True)).group_by(LeadActivity.lead_id))).all())
    return {"items": [{"id": row.id, "name": row.name, "instagram": row.instagram, "city": row.city,
        "status": row.status, "priority": row.priority, "sent_count": counts.get(row.id, 0),
        "can_message": row.status not in {"sem_interesse", "convertido"}} for row in rows], "template": DEFAULT_MESSAGE}

@router.get("/leads/{lead_id}/conversation")
async def conversation(lead_id: UUID, db: DB, auth: Auth):
    owns_integration(auth); lead = await get_lead(db, auth.organization_id, lead_id)
    rows = (await db.execute(select(LeadActivity).where(LeadActivity.organization_id == auth.organization_id,
        LeadActivity.lead_id == lead.id, LeadActivity.event_key.startswith("instagram-send:", autoescape=True))
        .order_by(LeadActivity.created_at, LeadActivity.id).limit(100))).scalars().all()
    marker = "Mensagem enviada pelo Instagram:\n"
    return {"lead_id": lead.id, "instagram": lead.instagram, "status": lead.status, "messages": [
        {"id": row.id, "direction": "outgoing", "text": row.note.split(marker, 1)[1] if marker in row.note else row.note, "at": row.created_at}
        for row in rows]}

@router.post("/leads/{lead_id}/sent")
async def record_sent(lead_id: UUID, data: SentInput, db: DB, auth: Auth):
    owns_integration(auth); lead = await get_lead(db, auth.organization_id, lead_id, True)
    if lead.instagram != data.expected_instagram: raise HTTPException(409, "O perfil mudou. Reabra a conversa antes de registrar o envio.")
    if lead.status in {"sem_interesse", "convertido"}: raise HTTPException(409, "Este contato está encerrado no CRM.")
    event_key = "instagram-send:" + str(data.request_id)
    note = "Mensagem enviada pelo Instagram:\n" + data.text
    existing = (await db.execute(select(LeadActivity).where(LeadActivity.organization_id == auth.organization_id, LeadActivity.event_key == event_key))).scalar_one_or_none()
    if existing:
        if existing.lead_id != lead.id or existing.note != note: raise HTTPException(409, "Este registro já foi usado com outros dados.")
        return {"state": "sent", "id": existing.id}
    today = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    activity = LeadActivity(organization_id=auth.organization_id, lead_id=lead.id, event_key=event_key, kind="contato", occurred_on=today, note=note)
    db.add(activity); apply_activity(lead, ActivityInput(kind="contato", occurred_on=today, event_key=event_key, note=note))
    await db.commit(); await db.refresh(activity)
    return {"state": "sent", "id": activity.id}
