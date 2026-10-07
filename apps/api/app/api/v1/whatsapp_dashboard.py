from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Query
from sqlalchemy import and_, case, func, or_, select
from app.api.dependencies import Auth, DB
from app.models.crm import AutomationReceipt, AutomationRule, Lead

router = APIRouter(prefix='/crm/evolution', tags=['Painel WhatsApp'])
ZONE = ZoneInfo('America/Sao_Paulo')


def period_start(now, days):
    today = now.astimezone(ZONE).date()
    return datetime.combine(today - timedelta(days=days - 1), time.min, ZONE)


@router.get('/dashboard')
async def dashboard(db: DB, auth: Auth, days: int = Query(default=7, ge=1, le=30)):
    now = datetime.now(ZONE)
    since = period_start(now, days)
    org = auth.organization_id
    receipt_scope = [AutomationReceipt.organization_id == org, AutomationReceipt.created_at >= since]
    counts = dict((await db.execute(select(AutomationReceipt.state, func.count())
        .where(*receipt_scope).group_by(AutomationReceipt.state))).all())
    active_rules = (await db.execute(select(func.count()).select_from(AutomationRule)
        .where(AutomationRule.organization_id == org, AutomationRule.enabled.is_(True)))).scalar_one()
    new_contacts = (await db.execute(select(func.count()).select_from(Lead)
        .where(Lead.organization_id == org, Lead.phone.is_not(None), Lead.created_at >= since))).scalar_one()
    queue_scope = [Lead.organization_id == org, Lead.phone.is_not(None), Lead.bot_paused.is_(True), Lead.status == 'respondeu']
    waiting = (await db.execute(select(func.count()).select_from(Lead).where(*queue_scope))).scalar_one()
    attention = or_(AutomationReceipt.state == 'uncertain', and_(AutomationReceipt.state == 'sending',
                                                              AutomationReceipt.created_at < now - timedelta(minutes=2)))
    attention_count = (await db.execute(select(func.count()).select_from(AutomationReceipt)
        .where(*receipt_scope, attention))).scalar_one()
    bucket = func.date(func.timezone('America/Sao_Paulo', AutomationReceipt.created_at))
    rows = (await db.execute(select(bucket.label('day'), func.count().label('received'),
        func.sum(case((AutomationReceipt.state == 'sent', 1), else_=0)).label('sent'))
        .where(*receipt_scope).group_by(bucket).order_by(bucket))).all()
    daily = {row.day.isoformat(): {'received': row.received, 'sent': row.sent} for row in rows}
    series = [{'day': (since.date() + timedelta(days=i)).isoformat(),
               **daily.get((since.date() + timedelta(days=i)).isoformat(), {'received': 0, 'sent': 0})}
              for i in range(days)]
    recent = (await db.execute(select(AutomationReceipt, Lead).outerjoin(Lead,
        and_(Lead.id == AutomationReceipt.lead_id, Lead.organization_id == org))
        .where(*receipt_scope).order_by(AutomationReceipt.created_at.desc(), AutomationReceipt.id).limit(20))).all()
    priority_rank = case((Lead.priority == 'urgente', 0), (Lead.priority == 'alta', 1), else_=2)
    queue = (await db.execute(select(Lead).where(*queue_scope)
        .order_by(priority_rank, Lead.updated_at.desc(), Lead.id).limit(20))).scalars().all()
    return {
        'days': days, 'since': since, 'updated_at': now,
        'summary': {'received': sum(counts.values()), 'sent': counts.get('sent', 0),
                    'new_contacts': new_contacts, 'waiting_human': waiting,
                    'attention': attention_count, 'active_rules': active_rules},
        'series': series,
        'recent': [{'id': receipt.id, 'lead_id': receipt.lead_id,
                    'name': lead.name if lead else 'Contato não associado',
                    'phone': lead.phone if lead else None, 'priority': lead.priority if lead else 'media',
                    'bot_paused': lead.bot_paused if lead else True, 'status': lead.status if lead else None,
                    'incoming': receipt.incoming, 'reply': receipt.reply, 'state': receipt.state,
                    'created_at': receipt.created_at} for receipt, lead in recent],
        'queue': [{'id': lead.id, 'name': lead.name, 'phone': lead.phone,
                   'priority': lead.priority, 'updated_at': lead.updated_at} for lead in queue],
    }
