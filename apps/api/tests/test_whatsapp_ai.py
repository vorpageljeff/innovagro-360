import asyncio
import json
from types import SimpleNamespace
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import whatsapp_ai as service


def test_history_excludes_undelivered_replies_and_is_bounded():
    rows = [SimpleNamespace(incoming=str(i), reply='never delivered', state='uncertain') for i in range(10)]
    rows[-1] = SimpleNamespace(incoming='latest', reply='delivered', state='sent')
    messages = service.conversation_input(rows, 'x' * 5000)
    assert messages[0]['content'] == '4'
    assert sum(row['role'] == 'assistant' for row in messages) == 1
    assert len(messages[-1]['content']) == 2000


@pytest.mark.parametrize('response_data, status, succeeds', [
    ({'status': 'completed', 'output': [{'type': 'message', 'role': 'assistant', 'content': [
        {'type': 'output_text', 'text': json.dumps({'reply': 'Como posso ajudar?', 'handoff': False, 'priority': 'media'})}]}]}, 200, True),
    ({'status': 'incomplete', 'output': []}, 200, False),
    ({'status': 'completed', 'output': []}, 200, False),
    ({'error': {'message': 'private provider detail'}}, 401, False),
])
def test_provider_contract_and_failure(monkeypatch, response_data, status, succeeds):
    monkeypatch.setattr(service.settings, 'whatsapp_ai_enabled', True)
    monkeypatch.setattr(service.settings, 'whatsapp_ai_model', 'configured-model')
    monkeypatch.setattr(service.settings, 'whatsapp_ai_knowledge', 'Empresa de teste; não informar preços.')
    monkeypatch.setattr(service.settings, 'openai_api_key', 'private-test-key')
    original = httpx.AsyncClient
    def respond(request):
        assert str(request.url) == 'https://api.openai.com/v1/responses'
        body = json.loads(request.content)
        assert body['store'] is False and body['max_output_tokens'] == 1024
        assert body['text']['format']['strict'] is True
        assert body['model'] == 'configured-model'
        assert body['input'] == [{'role': 'user', 'content': 'Olá'}]
        return httpx.Response(status, json=response_data)
    monkeypatch.setattr(service.httpx, 'AsyncClient', lambda **kwargs: original(transport=httpx.MockTransport(respond), **kwargs))
    if succeeds:
        assert asyncio.run(service.answer([], 'Olá')).reply == 'Como posso ajudar?'
    else:
        with pytest.raises(service.AIUnavailable) as caught:
            asyncio.run(service.answer([], 'Olá'))
        assert 'private' not in str(caught.value)


def test_disabled_ai_never_calls_provider(monkeypatch):
    monkeypatch.setattr(service.settings, 'whatsapp_ai_enabled', False)
    monkeypatch.setattr(service.httpx, 'AsyncClient', lambda **kwargs: pytest.fail('Unexpected provider call'))
    with pytest.raises(service.AIUnavailable):
        asyncio.run(service.answer([], 'oi'))
    with TestClient(app) as client:
        assert client.get('/api/v1/crm/evolution/ai/status').status_code == 401


@pytest.mark.parametrize('mode, expected, generations, sends', [
    ('reply', 'sent', 1, 1), ('failure', 'ai_handoff', 1, 0),
    ('limit', 'ai_handoff', 0, 0), ('paused', 'paused', 0, 0),
    ('duplicate', 'duplicate', 0, 0), ('human', 'sent', 0, 1),
])
def test_ai_webhook_preserves_pause_deduplication_handoff_and_tenant(monkeypatch, mode, expected, generations, sends):
    import app.api.v1.automations as module
    org, lead_id, receipt_id = uuid4(), uuid4(), uuid4()
    for name, value in {'evolution_api_url': 'http://evolution:8080', 'evolution_api_key': 'test',
                        'evolution_instance': 'crm', 'evolution_organization_id': str(org),
                        'evolution_webhook_secret': 'secret', 'evolution_bot_enabled': mode != 'paused',
                        'whatsapp_ai_enabled': True, 'whatsapp_ai_daily_limit': 100}.items():
        monkeypatch.setattr(module.settings, name, value)
    lead = SimpleNamespace(id=lead_id, status='respondeu', priority='media', next_contact_on=None, bot_paused=False)
    receipt = SimpleNamespace(state='received', reply='')
    rule = SimpleNamespace(enabled=True, contains='', reply='Encaminhando à equipe.', priority='alta', status=None, name='rule', handoff=mode == 'human')
    class DB:
        calls = 0
        commits = 0
        async def execute(self, query):
            self.calls += 1
            values = query.compile().params
            if self.calls != 3:
                assert org in values.values(), 'Every tenant query must be scoped'
            if self.calls == 1: return SimpleNamespace(scalar_one_or_none=lambda: lead)
            if self.calls == 2: return SimpleNamespace(scalar_one_or_none=lambda: None if mode == 'duplicate' else receipt_id)
            if self.calls == 3: return SimpleNamespace(scalar_one=lambda: receipt)
            if self.calls == 4: return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: [rule]))
            if self.calls == 5: return SimpleNamespace(scalar_one=lambda: lead)
            if self.calls == 6: return SimpleNamespace(scalar_one=lambda: 101 if mode == 'limit' else 1)
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []))
        async def commit(self): self.commits += 1
        async def refresh(self, obj): pass
    db = DB()
    calls = {'ai': 0, 'send': 0}
    async def generate(history, text):
        calls['ai'] += 1
        assert db.commits == 1 and receipt.state == 'ai_generating'
        if mode == 'failure': raise service.AIUnavailable()
        return service.Answer(reply='Olá!', priority='media', handoff=False)
    async def send(*args):
        calls['send'] += 1
        assert db.commits >= 1
        return {}
    monkeypatch.setattr(module, 'ai_answer', generate)
    monkeypatch.setattr(module, 'evolution_request', send)
    class Request:
        async def body(self):
            return json.dumps({'event': 'messages.upsert', 'instance': 'crm', 'data': {
                'key': {'fromMe': False, 'remoteJid': '5511999999999@s.whatsapp.net', 'id': 'test-1'},
                'message': {'conversation': 'Olá'}}}).encode()
    assert asyncio.run(module.webhook(Request(), db, 'secret'))['state'] == expected
    assert calls == {'ai': generations, 'send': sends}
    if mode in ('failure', 'limit'): assert lead.bot_paused is True
