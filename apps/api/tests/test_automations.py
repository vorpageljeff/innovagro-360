import asyncio
from types import SimpleNamespace
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.main import app
from app.schemas.crm import LeadUpdate, RuleInput
from app.services.evolution import incoming_message, matching_rule


def payload(**key):
    return {'event': 'messages.upsert', 'instance': 'crm', 'data': {
        'key': {'fromMe': False, 'remoteJid': '5511999999999@s.whatsapp.net', 'id': 'msg-1', **key},
        'message': {'conversation': 'Quero um ORÇAMENTO'}}}


def test_incoming_text():
    assert incoming_message(payload()) == ('5511999999999', 'msg-1', 'Quero um ORÇAMENTO')


@pytest.mark.parametrize('key', [{'fromMe': True}, {'remoteJid': '123@g.us'}, {'remoteJid': '123@lid'}, {'id': None}, {'remoteJid': None}])
def test_echo_groups_and_invalid_messages_are_ignored(key):
    assert incoming_message(payload(**key)) is None


def test_rule_order_and_case_insensitive_condition():
    paused = SimpleNamespace(enabled=False, contains='', name='paused')
    specific = SimpleNamespace(enabled=True, contains='orçamento', name='specific')
    catchall = SimpleNamespace(enabled=True, contains='', name='catchall')
    assert matching_rule([paused, specific, catchall], 'ORÇAMENTO por favor') is specific
    assert matching_rule([paused, specific, catchall], 'oi') is catchall


def test_rules_start_paused_and_validate_priority():
    assert RuleInput(name='Orçamento').enabled is False
    with pytest.raises(ValidationError):
        RuleInput(name='Teste', priority='invalida')


def test_phone_normalization_and_clear():
    assert LeadUpdate(phone='+55 (11) 99999-9999').phone == '5511999999999'
    assert LeadUpdate(phone='').phone is None
    with pytest.raises(ValidationError):
        LeadUpdate(phone='abc')


def test_authentication_required_and_webhook_secret():
    with TestClient(app) as client:
        assert client.get('/api/v1/crm/automations').status_code == 401
        assert client.get('/api/v1/crm/evolution/status').status_code == 401
        assert client.post('/api/v1/crm/evolution/webhook', json=payload()).status_code == 401


@pytest.mark.parametrize('duplicate, terminal, expected', [(True, False, 'duplicate'), (False, True, 'paused'), (False, False, 'sent')])
def test_webhook_deduplication_and_terminal_contacts(monkeypatch, duplicate, terminal, expected):
    import app.api.v1.automations as module
    org, lead_id, receipt_id = uuid4(), uuid4(), uuid4()
    monkeypatch.setattr(module.settings, 'evolution_api_url', 'http://evolution:8080')
    monkeypatch.setattr(module.settings, 'evolution_api_key', 'test')
    monkeypatch.setattr(module.settings, 'evolution_instance', 'crm')
    monkeypatch.setattr(module.settings, 'evolution_organization_id', str(org))
    monkeypatch.setattr(module.settings, 'evolution_webhook_secret', 'secret')
    monkeypatch.setattr(module.settings, 'evolution_bot_enabled', True)
    lead = SimpleNamespace(id=lead_id, status='sem_interesse' if terminal else 'aguardando', priority='media', next_contact_on=None)
    receipt = SimpleNamespace(state='received', reply='')
    rule = SimpleNamespace(enabled=True, contains='orçamento', reply='Olá!', priority='alta', status=None)
    sends = []
    class DB:
        calls = 0
        commits = 0
        async def execute(self, query):
            self.calls += 1
            values = query.compile().params
            if self.calls == 1:
                assert org in values.values()
                return SimpleNamespace(scalar_one_or_none=lambda: lead)
            if self.calls == 2:
                return SimpleNamespace(scalar_one_or_none=lambda: None if duplicate else receipt_id)
            if self.calls == 3:
                return SimpleNamespace(scalar_one=lambda: receipt)
            assert org in values.values()
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: [rule]))
        async def commit(self): self.commits += 1
    db = DB()
    async def send(*args):
        assert db.commits == 1, 'Receipt must be durable before sending'
        sends.append(args)
        return {}
    monkeypatch.setattr(module, 'evolution_request', send)
    class Request:
        async def body(self):
            import json
            return json.dumps(payload()).encode()
    result = asyncio.run(module.webhook(Request(), db, 'secret'))
    assert result['state'] == expected
    assert len(sends) == (1 if expected == 'sent' else 0)
