import secrets
from uuid import UUID, uuid4
from fastapi import APIRouter, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.api.dependencies import Auth, DB
from app.api.v1.crm import get_lead
from app.core.config import settings
from app.models.crm import Lead, AutomationRule, AutomationReceipt
from app.schemas.crm import RuleInput, RuleOutput, ReceiptOutput
from app.services.evolution import configured, evolution_request, incoming_message, matching_rule

router = APIRouter(prefix='/crm', tags=['Automações'])


def owns_integration(auth):
    if str(auth.organization_id) != settings.evolution_organization_id:
        raise HTTPException(404, 'Integração não configurada para esta organização.')


@router.get('/evolution/status')
async def status(auth: Auth):
    if not configured() or str(auth.organization_id) != settings.evolution_organization_id:
        return {'configured': False, 'bot_enabled': False, 'state': 'not_configured'}
    result = await evolution_request('GET', 'instance/connectionState')
    return {'configured': True, 'bot_enabled': settings.evolution_bot_enabled,
            'state': result.get('instance', {}).get('state', 'unknown')}


@router.post('/evolution/connect')
async def connect(auth: Auth):
    owns_integration(auth)
    result = await evolution_request('GET', 'instance/connect')
    return {'base64': result.get('base64'), 'code': result.get('code')}


@router.get('/automations', response_model=list[RuleOutput])
async def list_rules(db: DB, auth: Auth):
    return (await db.execute(select(AutomationRule).where(AutomationRule.organization_id == auth.organization_id)
                            .order_by(AutomationRule.created_at, AutomationRule.id))).scalars().all()


@router.post('/automations', response_model=RuleOutput)
async def create_rule(data: RuleInput, db: DB, auth: Auth):
    rule = AutomationRule(organization_id=auth.organization_id, **data.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.post('/automations/{rule_id}', response_model=RuleOutput)
async def update_rule(rule_id: UUID, data: RuleInput, db: DB, auth: Auth):
    rule = (await db.execute(select(AutomationRule).where(AutomationRule.id == rule_id,
                AutomationRule.organization_id == auth.organization_id).with_for_update())).scalar_one_or_none()
    if rule is None:
        raise HTTPException(404, 'Fluxo não encontrado.')
    for key, value in data.model_dump().items():
        setattr(rule, key, value)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.get('/leads/{lead_id}/messages', response_model=list[ReceiptOutput])
async def messages(lead_id: UUID, db: DB, auth: Auth):
    await get_lead(db, auth, lead_id)
    return (await db.execute(select(AutomationReceipt).where(AutomationReceipt.organization_id == auth.organization_id,
        AutomationReceipt.lead_id == lead_id).order_by(AutomationReceipt.created_at.desc()).limit(100))).scalars().all()


@router.post('/evolution/webhook')
async def webhook(request: Request, db: DB, x_webhook_secret: str = Header(default='')):
    if not configured() or not secrets.compare_digest(x_webhook_secret, settings.evolution_webhook_secret):
        raise HTTPException(401, 'Webhook não autorizado.')
    raw = await request.body()
    if len(raw) > 100_000:
        raise HTTPException(413, 'Evento muito grande.')
    try:
        import json
        payload = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise HTTPException(422, 'Evento inválido.') from None
    if not isinstance(payload, dict) or payload.get('instance') != settings.evolution_instance:
        raise HTTPException(422, 'Instância inválida.')
    incoming = incoming_message(payload)
    if incoming is None:
        return {'state': 'ignored'}
    phone, message_id, text = incoming
    org = UUID(settings.evolution_organization_id)
    lead = (await db.execute(select(Lead).where(Lead.organization_id == org, Lead.phone == phone)
                            .with_for_update())).scalar_one_or_none()
    receipt_id = uuid4()
    inserted = (await db.execute(insert(AutomationReceipt).values(id=receipt_id, organization_id=org,
        message_id=message_id, lead_id=lead.id if lead else None, incoming=text, reply='', state='received')
        .on_conflict_do_nothing(constraint='uq_crm_webhook_message').returning(AutomationReceipt.id))).scalar_one_or_none()
    if inserted is None:
        return {'state': 'duplicate'}
    receipt = (await db.execute(select(AutomationReceipt).where(AutomationReceipt.id == receipt_id))).scalar_one()
    if lead is None or lead.status in ('sem_interesse', 'convertido') or not settings.evolution_bot_enabled:
        receipt.state = 'unmatched' if lead is None else 'paused'
        await db.commit()
        return {'state': receipt.state}
    rules = (await db.execute(select(AutomationRule).where(AutomationRule.organization_id == org,
        AutomationRule.enabled.is_(True)).order_by(AutomationRule.created_at, AutomationRule.id))).scalars().all()
    rule = matching_rule(rules, text)
    if rule is None:
        receipt.state = 'no_rule'
        await db.commit()
        return {'state': receipt.state}
    if rule.priority:
        lead.priority = rule.priority
    lead.status = rule.status or 'respondeu'
    lead.next_contact_on = None
    receipt.reply = rule.reply
    receipt.state = 'sending' if rule.reply and lead.status not in ('sem_interesse', 'convertido') else 'completed'
    # Persist BEFORE external send. Duplicate delivery must never send twice.
    await db.commit()
    if receipt.state == 'sending':
        try:
            await evolution_request('POST', 'message/sendText', {'number': phone, 'text': rule.reply})
            receipt.state = 'sent'
        except HTTPException:
            receipt.state = 'uncertain'
        await db.commit()
    return {'state': receipt.state}
