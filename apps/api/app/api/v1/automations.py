import secrets
from uuid import UUID, uuid4
from fastapi import APIRouter, Header, HTTPException, Request
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from app.api.dependencies import Auth, DB
from app.api.v1.crm import get_lead
from app.core.config import settings
from app.models.crm import Lead, LeadActivity, AutomationRule, AutomationReceipt
from app.schemas.crm import RuleInput, RuleOutput, ReceiptOutput, SimulationInput
from app.services.evolution import configured, evolution_request, incoming_message, matching_rule, rule_plan
from app.services.whatsapp_ai import AIUnavailable, answer as ai_answer, readiness, qualification_complete, qualification_note, site_intake, test_contact_allowed
from app.services.whatsapp_leads import excluded_phones

router = APIRouter(prefix='/crm', tags=['Automações'])


@router.get('/evolution/ai/status')
async def ai_status(auth: Auth):
    owns_integration(auth)
    missing = readiness()
    return {'configured': not missing, 'enabled': settings.whatsapp_ai_enabled,
            'bot_enabled': settings.evolution_bot_enabled, 'missing': missing,
            'provider': settings.whatsapp_ai_provider, 'test_mode': settings.whatsapp_ai_test_mode,
            'model': settings.whatsapp_ai_model, 'daily_limit': settings.whatsapp_ai_daily_limit,
            'qualification_fields': settings.whatsapp_ai_required_fields.split(',')}


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
                            .order_by(AutomationRule.position, AutomationRule.created_at, AutomationRule.id))).scalars().all()


@router.post('/automations', response_model=RuleOutput)
async def create_rule(data: RuleInput, db: DB, auth: Auth):
    rule = AutomationRule(organization_id=auth.organization_id, **data.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.post('/automations/simulate')
async def simulate(data: SimulationInput, db: DB, auth: Auth):
    rules = (await db.execute(select(AutomationRule).where(AutomationRule.organization_id == auth.organization_id)
        .order_by(AutomationRule.position, AutomationRule.created_at, AutomationRule.id))).scalars().all()
    return rule_plan(matching_rule(rules, data.text))


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
    if lead is None:
        data = payload.get('data', {})
        name = data.get('pushName') if isinstance(data, dict) else None
        name = name.strip()[:160] if isinstance(name, str) and name.strip() else 'Contato WhatsApp'
        await db.execute(insert(Lead).values(id=uuid4(), organization_id=org, name=name,
            instagram=None, city='', phone=phone, priority='media', status='respondeu', bot_paused=False)
            .on_conflict_do_nothing(index_elements=['organization_id', 'phone']))
        lead = (await db.execute(select(Lead).where(Lead.organization_id == org, Lead.phone == phone)
            .with_for_update())).scalar_one()
    receipt_id = uuid4()
    inserted = (await db.execute(insert(AutomationReceipt).values(id=receipt_id, organization_id=org,
        message_id=message_id, lead_id=lead.id if lead else None, incoming=text, reply='', state='received')
        .on_conflict_do_nothing(constraint='uq_crm_webhook_message').returning(AutomationReceipt.id))).scalar_one_or_none()
    if inserted is None:
        return {'state': 'duplicate'}
    receipt = (await db.execute(select(AutomationReceipt).where(AutomationReceipt.id == receipt_id))).scalar_one()
    intake = site_intake(text)
    if intake and qualification_complete(intake) and lead.status not in ('sem_interesse', 'convertido') and phone not in excluded_phones():
        from zoneinfo import ZoneInfo
        db.add(LeadActivity(organization_id=org, lead_id=lead.id,
            event_key=f'whatsapp-qualification:{receipt_id}', kind='nota',
            occurred_on=datetime.now(ZoneInfo('America/Sao_Paulo')).date(), note=qualification_note(intake)))
        lead.status = 'respondeu'
        lead.priority = 'alta'
        lead.bot_paused = True
        lead.next_contact_on = None
        receipt.state = 'completed'
        await db.commit()
        # Incoming qualification can enter the human queue without re-enabling any outbound bot.
        return {'state': receipt.state}
    if lead is None or lead.status in ('sem_interesse', 'convertido') or lead.bot_paused or phone in excluded_phones() or not settings.evolution_bot_enabled:
        receipt.state = 'unmatched' if lead is None else 'paused'
        await db.commit()
        return {'state': receipt.state}
    rules = (await db.execute(select(AutomationRule).where(AutomationRule.organization_id == org,
        AutomationRule.enabled.is_(True)).order_by(AutomationRule.position, AutomationRule.created_at, AutomationRule.id))).scalars().all()
    rule = matching_rule(rules, text)
    # Explicit human/terminal flows always take precedence over AI.
    if settings.whatsapp_ai_enabled and test_contact_allowed(phone) and (rule is None or
            not rule.handoff and rule.status not in ('sem_interesse', 'convertido')):
        receipt.state = 'ai_generating'
        # Reserve before the paid call; repeated webhooks must not generate twice.
        await db.commit()
        lead = (await db.execute(select(Lead).where(Lead.id == lead.id, Lead.organization_id == org)
            .with_for_update().execution_options(populate_existing=True))).scalar_one()
        if lead.bot_paused or lead.status in ('sem_interesse', 'convertido') or not settings.evolution_bot_enabled:
            receipt.state = 'paused'
            await db.commit()
            return {'state': receipt.state}
        # Conservative rolling cap includes fixed replies and in-flight claims.
        used = (await db.execute(select(func.count(AutomationReceipt.id)).where(
            AutomationReceipt.organization_id == org,
            AutomationReceipt.created_at >= datetime.now(timezone.utc) - timedelta(days=1),
            AutomationReceipt.state.notin_(['paused', 'no_rule', 'unmatched'])))).scalar_one()
        history_query = select(AutomationReceipt).where(
            AutomationReceipt.organization_id == org, AutomationReceipt.lead_id == lead.id,
            AutomationReceipt.id != receipt_id)
        if settings.whatsapp_ai_test_mode and settings.whatsapp_ai_test_since:
            history_query = history_query.where(AutomationReceipt.created_at >= settings.whatsapp_ai_test_since)
        history = (await db.execute(history_query.order_by(
            AutomationReceipt.created_at.desc(), AutomationReceipt.id.desc()).limit(6))).scalars().all()
        try:
            if used > settings.whatsapp_ai_daily_limit:
                raise AIUnavailable()
            qualification_query = select(LeadActivity).where(
                LeadActivity.organization_id == org, LeadActivity.lead_id == lead.id,
                LeadActivity.event_key.startswith('whatsapp-qualification:', autoescape=True))
            if settings.whatsapp_ai_test_mode and settings.whatsapp_ai_test_since:
                qualification_query = qualification_query.where(LeadActivity.created_at >= settings.whatsapp_ai_test_since)
            previous = (await db.execute(qualification_query.order_by(
                LeadActivity.created_at.desc(), LeadActivity.id.desc()).limit(1))).scalar_one_or_none()
            generated = await ai_answer(list(reversed(history)), text, previous.note if previous else '')
            if qualification_complete(generated):
                generated.handoff = True
                generated.reply = 'Obrigado pelas informações! Vou encaminhar sua necessidade para nossa equipe continuar o atendimento.'
                if generated.priority == 'baixa' or generated.priority == 'media':
                    generated.priority = 'alta'
            if any((generated.name, generated.company, generated.service, generated.need, generated.summary)):
                from zoneinfo import ZoneInfo
                db.add(LeadActivity(organization_id=org, lead_id=lead.id,
                    event_key=f'whatsapp-qualification:{receipt_id}', kind='nota',
                    occurred_on=datetime.now(ZoneInfo('America/Sao_Paulo')).date(),
                    note=qualification_note(generated)))
            receipt.reply = generated.reply
            lead.priority = generated.priority
            lead.status = 'respondeu'
            lead.next_contact_on = None
            lead.bot_paused = generated.handoff
        except AIUnavailable:
            lead.bot_paused = True
            lead.priority = 'alta'
            lead.status = 'respondeu'
            lead.next_contact_on = None
            receipt.state = 'ai_handoff'
            await db.commit()
            return {'state': receipt.state}
        receipt.state = 'sending'
        await db.commit()
        await db.refresh(lead)
        if lead.status in ('sem_interesse', 'convertido') or (lead.bot_paused and not generated.handoff):
            receipt.state = 'ai_cancelled'
            receipt.reply = ''
        else:
            try:
                await evolution_request('POST', 'message/sendText', {'number': phone, 'text': receipt.reply})
                receipt.state = 'sent'
            except HTTPException:
                receipt.state = 'uncertain'
        await db.commit()
        return {'state': receipt.state}
    if rule is None:
        receipt.state = 'no_rule'
        await db.commit()
        return {'state': receipt.state}
    if rule.priority:
        lead.priority = rule.priority
    lead.status = rule.status or 'respondeu'
    lead.next_contact_on = None
    lead.bot_paused = rule.handoff
    plan = rule_plan(rule)
    receipt.reply = plan['reply']
    receipt.state = 'sending' if receipt.reply else 'completed'
    # Persist BEFORE external send. Duplicate delivery must never send twice.
    await db.commit()
    if receipt.state == 'sending':
        try:
            await evolution_request('POST', 'message/sendText', {'number': phone, 'text': receipt.reply})
            receipt.state = 'sent'
        except HTTPException:
            receipt.state = 'uncertain'
        await db.commit()
    return {'state': receipt.state}
