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
    lead = SimpleNamespace(id=lead_id, status='sem_interesse' if terminal else 'aguardando', priority='media', next_contact_on=None, bot_paused=False)
    receipt = SimpleNamespace(state='received', reply='')
    rule = SimpleNamespace(enabled=True, contains='orçamento', reply='Olá!', priority='alta', status=None, name='Orçamento', handoff=False)
    sends = []
    class DB:
        calls = 0
        commits = 0
        async def execute(self, query):
            if 'count(' in str(query):
                assert org in query.compile().params.values()
                return SimpleNamespace(scalar_one=lambda: 0)
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


def test_normalized_synonyms_and_exact_menu_option():
    rule = SimpleNamespace(enabled=True, contains='orçamento|preço|1', position=10)
    fallback = SimpleNamespace(enabled=True, contains='', position=100)
    assert matching_rule([fallback, rule], 'ORCAMENTO') is rule
    assert matching_rule([fallback, rule], '1') is rule
    assert matching_rule([fallback, rule], '123') is fallback


def test_lid_with_explicit_phone_alternative():
    assert incoming_message(payload(remoteJid='123@lid', remoteJidAlt='5511999999999@s.whatsapp.net'))[0] == '5511999999999'


def test_terminal_transition_does_not_claim_a_reply():
    from app.services.evolution import rule_plan
    rule = SimpleNamespace(name='Encerrar', priority='baixa', status='sem_interesse', reply='Não enviar', handoff=False)
    assert rule_plan(rule)['reply'] == ''


def test_complete_commercial_paths():
    from app.services.bot_templates import commercial_templates
    from app.services.evolution import rule_plan
    rules = [SimpleNamespace(**data) for data in commercial_templates()]
    cases = [('Oi', 'Boas-vindas e menu', False), ('1', 'Orçamento — atendimento inicial', True),
             ('2', 'Conhecer serviços', False), ('3', 'Falar com atendente', True),
             ('Estou com um problema', 'Suporte e dúvidas', True), ('não quero', 'Não contatar', True)]
    for text, name, handoff in cases:
        plan = rule_plan(matching_rule(rules, text))
        assert plan['name'] == name and plan['handoff'] == handoff
    assert rule_plan(matching_rule(rules, 'nao quero'))['reply'] == ''


def test_stop_keyword_does_not_match_preparar():
    from app.services.bot_templates import commercial_templates
    rules = [SimpleNamespace(**data) for data in commercial_templates()]
    assert matching_rule(rules, 'Quero preparar um site').name == 'Conhecer serviços'


def test_budget_continues_ai_but_human_and_terminal_rules_do_not():
    from types import SimpleNamespace
    from app.services.evolution import ai_may_handle_rule
    def rule(contains, status=None):
        return SimpleNamespace(contains=contains, status=status, handoff=True)
    assert ai_may_handle_rule(rule('1|orçamento|preço|valor'))
    assert not ai_may_handle_rule(rule('atendente|humano'))
    assert not ai_may_handle_rule(rule('suporte|erro'))
    assert not ai_may_handle_rule(rule('orcamento|humano'))
    assert not ai_may_handle_rule(rule('orcamento', 'sem_interesse'))
    assert not ai_may_handle_rule(rule(''))
