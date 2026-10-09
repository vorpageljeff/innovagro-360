import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from uuid import UUID, uuid4, uuid5
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.api.dependencies import Auth, DB
from app.api.v1.automations import owns_integration
from app.models.crm import Lead, LeadActivity
from app.models.whatsapp_messages import WhatsAppDraft, WhatsAppOutbound
from app.services.evolution import configured, evolution_request
from app.services.whatsapp_leads import blocked_reason
from app.services.crm import apply_activity

router = APIRouter(prefix='/crm/evolution', tags=['Envio WhatsApp'])
DEFAULT_MESSAGE = 'Olá, equipe da {empresa}! Sou Jefferson, da Voragon. Encontrei a empresa de vocês e gostaria de conversar sobre uma página profissional para apresentar seus serviços e facilitar novos contatos pela internet. Posso explicar a ideia?'
class TextInput(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    text: str = Field(min_length=1, max_length=1500)
class DraftInput(TextInput):
    request_id: UUID

def template_id(org):
    return uuid5(org, 'whatsapp-message-template')
def output(draft, outbound=None):
    return {'text': draft.text, 'request_id': draft.request_id, 'state': outbound.state if outbound else None}
async def get_lead(db, org, lead_id):
    lead=(await db.execute(select(Lead).where(Lead.organization_id==org, Lead.id==lead_id).with_for_update())).scalar_one_or_none()
    if not lead: raise HTTPException(404, 'Contato não encontrado.')
    return lead
async def existing_send(db, org, request_id):
    return (await db.execute(select(WhatsAppOutbound).where(WhatsAppOutbound.organization_id==org, WhatsAppOutbound.request_id==request_id))).scalar_one_or_none()
async def upsert_draft(db, org, lead_id, data):
    draft_id=template_id(org) if lead_id is None else uuid5(org, 'whatsapp-draft:'+str(lead_id))
    await db.execute(insert(WhatsAppDraft).values(id=draft_id, organization_id=org, lead_id=lead_id, text=data.text, request_id=data.request_id).on_conflict_do_update(index_elements=['id'], set_={'text':data.text, 'request_id':data.request_id, 'updated_at':datetime.now(ZoneInfo('America/Sao_Paulo'))}, where=WhatsAppDraft.organization_id==org))

@router.get('/message-template')
async def message_template(db: DB, auth: Auth):
    owns_integration(auth)
    row=(await db.execute(select(WhatsAppDraft).where(WhatsAppDraft.organization_id==auth.organization_id, WhatsAppDraft.id==template_id(auth.organization_id)))).scalar_one_or_none()
    return {'text':row.text if row else DEFAULT_MESSAGE}
@router.post('/message-template')
async def save_template(data: TextInput, db: DB, auth: Auth):
    owns_integration(auth)
    await upsert_draft(db, auth.organization_id, None, DraftInput(text=data.text, request_id=uuid4()))
    await db.commit()
    return {'text':data.text}

@router.get('/leads/{lead_id}/draft')
async def draft(lead_id: UUID, db: DB, auth: Auth):
    owns_integration(auth);lead=await get_lead(db,auth.organization_id,lead_id)
    row=(await db.execute(select(WhatsAppDraft).where(WhatsAppDraft.organization_id==auth.organization_id,WhatsAppDraft.lead_id==lead.id))).scalar_one_or_none()
    if row: return output(row,await existing_send(db,auth.organization_id,row.request_id))
    note=(await db.execute(select(LeadActivity).where(LeadActivity.organization_id==auth.organization_id,LeadActivity.lead_id==lead.id,LeadActivity.event_key.startswith('prospect-draft:',autoescape=True)).order_by(LeadActivity.created_at.desc()).limit(1))).scalar_one_or_none()
    marker='Mensagem preparada (sem preço):\n'
    template=await message_template(db,auth)
    text=note.note.split(marker,1)[1].strip() if note and marker in note.note else template['text'].replace('{empresa}',lead.name)
    return {'text':text,'request_id':uuid4(),'state':None}
@router.post('/leads/{lead_id}/draft')
async def save_draft(lead_id: UUID, data: DraftInput, db: DB, auth: Auth):
    owns_integration(auth);lead=await get_lead(db,auth.organization_id,lead_id)
    existing=await existing_send(db,auth.organization_id,data.request_id)
    if existing and (existing.lead_id!=lead.id or existing.text!=data.text): raise HTTPException(409,'Este envio já foi iniciado com outro texto. Prepare uma nova mensagem.')
    await upsert_draft(db,auth.organization_id,lead.id,data);await db.commit()
    return output(data,existing)

@router.post('/leads/{lead_id}/send')
async def send(lead_id: UUID, data: DraftInput, db: DB, auth: Auth):
    owns_integration(auth);org=auth.organization_id;lead=await get_lead(db,org,lead_id)
    existing=await existing_send(db,org,data.request_id)
    if existing:
        if existing.lead_id!=lead.id or existing.text!=data.text: raise HTTPException(409,'Envio já registrado com outros dados.')
        return {'state':existing.state,'id':existing.id}
    reason=blocked_reason(lead)
    if reason: raise HTTPException(409,reason)
    if not re.fullmatch(r'[1-9][0-9]{9,14}',lead.phone): raise HTTPException(422,'Telefone inválido.')
    if not configured(): raise HTTPException(503,'WhatsApp empresarial não configurado.')
    connection=await evolution_request('GET','instance/connectionState')
    if connection.get('instance',{}).get('state')!='open': raise HTTPException(409,'Conecte o WhatsApp empresarial antes de enviar.')
    row_id=uuid4()
    inserted=(await db.execute(insert(WhatsAppOutbound).values(id=row_id,organization_id=org,lead_id=lead.id,request_id=data.request_id,phone=lead.phone,text=data.text,state='sending').on_conflict_do_nothing(constraint='uq_whatsapp_outbound_request').returning(WhatsAppOutbound.id))).scalar_one_or_none()
    if not inserted:
        existing=await existing_send(db,org,data.request_id)
        if existing.lead_id!=lead.id or existing.text!=data.text: raise HTTPException(409,'Envio já registrado com outros dados.')
        return {'state':existing.state,'id':existing.id}
    await upsert_draft(db,org,lead.id,data)
    activity=LeadActivity(organization_id=org,lead_id=lead.id,event_key='manual-send:'+str(data.request_id),kind='nota',occurred_on=datetime.now(ZoneInfo('America/Sao_Paulo')).date(),note='Envio iniciado pelo WhatsApp empresarial. Confira o resultado antes de repetir.\n'+data.text)
    db.add(activity)
    phone=lead.phone
    await db.commit() # Claim is durable before the external send; no automatic retries.
    row=(await db.execute(select(WhatsAppOutbound).where(WhatsAppOutbound.organization_id==org,WhatsAppOutbound.id==row_id))).scalar_one()
    try:
        await evolution_request('POST','message/sendText',{'number':phone,'text':data.text})
        row.state='sent';activity.kind='contato';activity.note='Mensagem enviada pelo WhatsApp empresarial:\n'+data.text
        lead=await get_lead(db,org,lead.id)
        apply_activity(lead,activity)
    except HTTPException:
        row.state='uncertain';activity.note='Envio sem confirmação. Verifique no WhatsApp empresarial antes de tentar novamente:\n'+data.text
    await db.commit()
    return {'state':row.state,'id':row.id}


@router.get('/leads/{lead_id}/conversation')
async def conversation(lead_id: UUID, db: DB, auth: Auth):
    from app.models.crm import AutomationReceipt
    owns_integration(auth);lead=await get_lead(db,auth.organization_id,lead_id)
    # Release the read lock before polling Evolution.
    phone=lead.phone;paused=lead.bot_paused;status=lead.status
    await db.commit()
    messages=[];source='evolution';warning=''
    try:
        if not phone: raise HTTPException(409,'Telefone não cadastrado.')
        result=await evolution_request('POST','chat/findMessages',{'where':{'key':{'remoteJid':phone+'@s.whatsapp.net'}},'page':1,'offset':100})
        records=result.get('messages',{}).get('records',[])
        if not isinstance(records,list): raise HTTPException(502,'Histórico inválido.')
        for row in records[:100]:
            key=row.get('key',{});body=row.get('message',{})
            text=body.get('conversation') or body.get('extendedTextMessage',{}).get('text')
            if not text:
                for kind,label in [('imageMessage','Imagem'),('videoMessage','Vídeo'),('audioMessage','Áudio'),('documentMessage','Documento')]:
                    if kind in body: text='['+label+'] '+str(body[kind].get('caption',''));break
            if not text: text='[Mensagem não textual]'
            try: at=datetime.fromtimestamp(int(row.get('messageTimestamp',0)),timezone.utc)
            except (ValueError,TypeError,OverflowError): continue
            messages.append({'id':str(key.get('id') or row.get('id')),'direction':'outgoing' if key.get('fromMe') else 'incoming','text':str(text)[:10000],'at':at,'state':'recorded'})
    except (HTTPException,AttributeError,TypeError):
        source='crm';warning='WhatsApp indisponível agora. Exibindo o histórico salvo no CRM.'
        receipts=(await db.execute(select(AutomationReceipt).where(AutomationReceipt.organization_id==auth.organization_id,AutomationReceipt.lead_id==lead.id).order_by(AutomationReceipt.created_at.desc()).limit(100))).scalars().all()
        for r in receipts:
            messages.append({'id':str(r.id)+':in','direction':'incoming','text':r.incoming,'at':r.created_at,'state':'recorded'})
            if r.reply: messages.append({'id':str(r.id)+':out','direction':'outgoing','text':r.reply,'at':r.created_at,'state':r.state})
    outbox=(await db.execute(select(WhatsAppOutbound).where(WhatsAppOutbound.organization_id==auth.organization_id,WhatsAppOutbound.lead_id==lead.id).order_by(WhatsAppOutbound.created_at.desc()).limit(100))).scalars().all()
    for r in outbox:
        if source=='crm' or r.state!='sent':messages.append({'id':str(r.id),'direction':'outgoing','text':r.text,'at':r.created_at,'state':r.state})
    messages.sort(key=lambda m:(m['at'],m['id']))
    return {'messages':messages[-100:],'bot_paused':paused,'status':status,'source':source,'warning':warning}
