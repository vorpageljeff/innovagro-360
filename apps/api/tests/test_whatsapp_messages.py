import asyncio
from types import SimpleNamespace
from uuid import uuid4
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.main import app
from app.core.config import settings
from app.api.v1 import whatsapp_messages as api


def test_message_routes_require_authentication():
    lead=str(uuid4())
    with TestClient(app) as client:
        for path in ['message-template',f'leads/{lead}/draft',f'leads/{lead}/conversation']:
            assert client.get('/api/v1/crm/evolution/'+path).status_code==401
        assert client.post(f'/api/v1/crm/evolution/leads/{lead}/send',json={'text':'Olá','request_id':str(uuid4())}).status_code==401


def test_message_validation_rejects_empty_oversized_and_unknown_fields():
    for text in ['', '   ', 'x'*1501]:
        with pytest.raises(ValidationError):api.TextInput(text=text)
    with pytest.raises(ValidationError):api.DraftInput(text='Olá',request_id=uuid4(),phone='untrusted')
    assert api.TextInput(text=' Olá ').text=='Olá'


def test_other_tenant_cannot_use_message_routes(monkeypatch):
    org=uuid4();monkeypatch.setattr(settings,'evolution_organization_id',str(org))
    with pytest.raises(HTTPException) as error:asyncio.run(api.message_template(None,SimpleNamespace(organization_id=uuid4())))
    assert error.value.status_code==404


def test_repeat_send_returns_prior_state_without_external_call(monkeypatch):
    from app.core.config import settings
    org=uuid4();lead_id=uuid4();req=uuid4();monkeypatch.setattr(settings,'evolution_organization_id',str(org))
    lead=SimpleNamespace(id=lead_id,phone='5511999999999',status='aguardando')
    previous=SimpleNamespace(id=uuid4(),lead_id=lead_id,text='Olá',state='uncertain',phone='5511999999999')
    class DB:
        async def execute(self,query):
            assert org in query.compile().params.values()
            result=lead if 'FROM crm_leads' in str(query) else previous
            return SimpleNamespace(scalar_one_or_none=lambda:result)
    async def fail(*args):pytest.fail('Duplicate must not access Evolution')
    monkeypatch.setattr(api,'evolution_request',fail)
    result=asyncio.run(api.send(lead_id,api.SendInput(text='Olá',request_id=req,expected_phone='5511999999999'),DB(),SimpleNamespace(organization_id=org)))
    assert result['state']=='uncertain'
    with pytest.raises(HTTPException) as error:asyncio.run(api.send(lead_id,api.SendInput(text='Outro texto',request_id=req,expected_phone='5511999999999'),DB(),SimpleNamespace(organization_id=org)))
    assert error.value.status_code==409


@pytest.mark.parametrize('status,phone',[('sem_interesse','5511999999999'),('convertido','5511999999999'),('aguardando',None)])
def test_blocked_contacts_cannot_send(monkeypatch,status,phone):
    from app.core.config import settings
    org=uuid4();lead_id=uuid4();monkeypatch.setattr(settings,'evolution_organization_id',str(org))
    class DB:
        async def execute(self,query):
            assert org in query.compile().params.values()
            return SimpleNamespace(scalar_one_or_none=lambda:SimpleNamespace(id=lead_id,phone=phone,status=status) if 'FROM crm_leads' in str(query) else None)
    async def fail(*args):pytest.fail('Blocked contacts must not access Evolution')
    monkeypatch.setattr(api,'evolution_request',fail)
    with pytest.raises(HTTPException) as error:asyncio.run(api.send(lead_id,api.SendInput(text='Olá',request_id=uuid4(),expected_phone='5511999999999'),DB(),SimpleNamespace(organization_id=org)))
    assert error.value.status_code==409


def test_inbox_and_read_require_authentication():
    with TestClient(app) as client:
        assert client.get('/api/v1/crm/evolution/inbox').status_code == 401
        assert client.post(f'/api/v1/crm/evolution/leads/{uuid4()}/read', json={'receipt_ids':[]}).status_code == 401


def test_read_acknowledgment_is_bounded():
    with pytest.raises(ValidationError): api.ReadInput(receipt_ids=[uuid4() for _ in range(101)])
    with pytest.raises(ValidationError): api.ReadInput(receipt_ids=[],user_id=str(uuid4()))


def test_foreign_organization_cannot_read_inbox(monkeypatch):
    monkeypatch.setattr(settings,'evolution_organization_id',str(uuid4()))
    with pytest.raises(HTTPException) as e:
        asyncio.run(api.inbox(None,SimpleNamespace(organization_id=uuid4())))
    assert e.value.status_code==404


@pytest.mark.parametrize('text', [
    '‎Silva Móveis agradece seu contato. Como podemos ajudar?',
    'Agradecemos o seu contato! Em breve atenderemos.',
    'Mensagem automática: estamos fora do horário.',
    'Sou a assistente virtual da empresa.'
])
def test_automatic_business_replies_are_detected(text):
    from app.services.evolution import is_automatic_reply
    assert is_automatic_reply(text)


@pytest.mark.parametrize('text', ['Oi, como posso ajudar?', 'Quero um orçamento', 'Tenho interesse em sistemas', 'Obrigado, vou falar com meu sócio'])
def test_human_messages_do_not_match_bot_templates(text):
    from app.services.evolution import is_automatic_reply
    assert not is_automatic_reply(text)
