from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import case, func, or_, select

from app.api.dependencies import Auth, DB
from app.api.v1.automations import owns_integration
from app.models.crm import Lead
from app.schemas.crm import LeadOutput, Priority, Status
from app.services.whatsapp_leads import blocked_reason, excluded_phones

router = APIRouter(prefix='/crm/evolution', tags=['Leads WhatsApp'])


@router.get('/leads')
async def leads(db: DB, auth: Auth, q: str = Query(default='', max_length=160),
                audience: Literal['all', 'ready', 'missing_phone'] = 'all', lead_id: UUID | None = None,
                priority: Priority | None = None, status: Status | None = None,
                offset: int = Query(default=0, ge=0), limit: int = Query(default=25, ge=1, le=100)):
    owns_integration(auth)
    scope = [Lead.organization_id == auth.organization_id]
    if lead_id is not None:
        scope.append(Lead.id == lead_id)
    if q.strip():
        term = q.strip()
        scope.append(or_(Lead.name.icontains(term, autoescape=True), Lead.city.icontains(term, autoescape=True),
                         Lead.instagram.icontains(term, autoescape=True), Lead.phone.icontains(term, autoescape=True)))
    if priority:
        scope.append(Lead.priority == priority)
    if status:
        scope.append(Lead.status == status)
    ready = [Lead.phone.is_not(None), Lead.status.notin_(['sem_interesse', 'convertido'])]
    exclusions = excluded_phones()
    if exclusions:
        ready.append(Lead.phone.notin_(sorted(exclusions)))
    total_all = (await db.execute(select(func.count(Lead.id)).where(*scope))).scalar_one()
    total_ready = (await db.execute(select(func.count(Lead.id)).where(*scope, *ready))).scalar_one()
    missing = (await db.execute(select(func.count(Lead.id)).where(*scope, Lead.phone.is_(None)))).scalar_one()
    if audience == 'ready':
        scope.extend(ready)
    elif audience == 'missing_phone':
        scope.append(Lead.phone.is_(None))
    total = (await db.execute(select(func.count(Lead.id)).where(*scope))).scalar_one()
    rank = case((Lead.priority == 'urgente', 0), (Lead.priority == 'alta', 1), (Lead.priority == 'media', 2), else_=3)
    rows = (await db.execute(select(Lead).where(*scope)
            .order_by(rank, Lead.name, Lead.id).offset(offset).limit(limit))).scalars().all()
    return {'total': total, 'offset': offset, 'limit': limit,
            'summary': {'all': total_all, 'ready': total_ready, 'missing_phone': missing},
            'items': [{**LeadOutput.model_validate(row).model_dump(),
                       'can_message': blocked_reason(row) is None, 'blocked_reason': blocked_reason(row)} for row in rows]}
