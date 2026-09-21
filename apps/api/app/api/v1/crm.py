from datetime import timedelta
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.api.dependencies import Auth, DB
from app.models.crm import Lead, LeadActivity
from app.schemas.crm import ActivityInput, ActivityOutput, ImportInput, LeadInput, LeadOutput
from app.services.crm import apply_activity

router = APIRouter(prefix='/crm', tags=['CRM'])

async def get_lead(db, auth, lead_id):
    lead = (await db.execute(select(Lead).where(Lead.id == lead_id, Lead.organization_id == auth.organization_id).with_for_update())).scalar_one_or_none()
    if lead is None:
        raise HTTPException(404, 'Contato não encontrado.')
    return lead

async def add_contact(data, db, auth):
    await db.execute(insert(Lead).values(id=uuid4(), organization_id=auth.organization_id, name=data.name, instagram=data.instagram, city=data.city, status='aguardando', last_contact_on=data.contacted_on, next_contact_on=data.contacted_on + timedelta(days=7)).on_conflict_do_nothing(constraint='uq_crm_lead_profile'))
    lead = (await db.execute(select(Lead).where(Lead.organization_id == auth.organization_id, Lead.instagram == data.instagram).with_for_update())).scalar_one()
    existing = (await db.execute(select(LeadActivity).where(LeadActivity.organization_id == auth.organization_id, LeadActivity.event_key == data.event_key))).scalar_one_or_none()
    if existing:
        if existing.lead_id != lead.id or existing.occurred_on != data.contacted_on or existing.note != data.note or existing.kind != 'contato':
            raise HTTPException(409, 'Identificador de evento já utilizado com outros dados.')
        return lead
    activity = ActivityInput(kind='contato', occurred_on=data.contacted_on, event_key=data.event_key, note=data.note or 'Contato registrado')
    db.add(LeadActivity(organization_id=auth.organization_id, lead_id=lead.id, event_key=data.event_key, kind='contato', occurred_on=data.contacted_on, note=data.note))
    apply_activity(lead, activity)
    return lead

@router.get('/leads', response_model=list[LeadOutput])
async def list_leads(db: DB, auth: Auth, offset: int = 0, limit: int = 100):
    if offset < 0 or not 1 <= limit <= 100:
        raise HTTPException(422, 'Paginação inválida.')
    return (await db.execute(select(Lead).where(Lead.organization_id == auth.organization_id).order_by(Lead.created_at.desc(), Lead.id).offset(offset).limit(limit))).scalars().all()

@router.post('/leads', response_model=LeadOutput)
async def create_lead(data: LeadInput, db: DB, auth: Auth):
    lead = await add_contact(data, db, auth)
    await db.commit()
    await db.refresh(lead)
    return lead

@router.post('/import')
async def import_leads(data: ImportInput, db: DB, auth: Auth):
    ids = []
    for item in data.leads:
        lead = await add_contact(item, db, auth)
        await db.flush()
        ids.append(str(lead.id))
    await db.commit()
    return {'processed': len(ids), 'lead_ids': ids}

@router.get('/leads/{lead_id}/activities', response_model=list[ActivityOutput])
async def activities(lead_id: UUID, db: DB, auth: Auth):
    await get_lead(db, auth, lead_id)
    return (await db.execute(select(LeadActivity).where(LeadActivity.organization_id == auth.organization_id, LeadActivity.lead_id == lead_id).order_by(LeadActivity.occurred_on.desc(), LeadActivity.created_at.desc()))).scalars().all()

@router.post('/leads/{lead_id}/activities', response_model=LeadOutput)
async def record_activity(lead_id: UUID, data: ActivityInput, db: DB, auth: Auth):
    lead = await get_lead(db, auth, lead_id)
    existing = (await db.execute(select(LeadActivity).where(LeadActivity.organization_id == auth.organization_id, LeadActivity.event_key == data.event_key))).scalar_one_or_none()
    if existing:
        if existing.lead_id != lead.id or existing.kind != data.kind or existing.occurred_on != data.occurred_on or existing.note != data.note or existing.requested_status != data.status or existing.requested_next_contact_on != data.next_contact_on:
            raise HTTPException(409, 'Evento já registrado com outros dados.')
        return lead
    db.add(LeadActivity(organization_id=auth.organization_id, lead_id=lead.id, event_key=data.event_key, kind=data.kind, occurred_on=data.occurred_on, note=data.note, requested_status=data.status, requested_next_contact_on=data.next_contact_on))
    apply_activity(lead, data)
    await db.commit()
    await db.refresh(lead)
    return lead
