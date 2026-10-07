import asyncio
from datetime import date
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.services.whatsapp_leads import blocked_reason


def test_exclusions_and_contact_states(monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, 'evolution_excluded_phones', '5511999999999, 5511888888888')
    def lead(phone='5511777777777', status='aguardando'):
        return SimpleNamespace(phone=phone, status=status)
    assert blocked_reason(lead()) is None
    assert blocked_reason(lead(phone=None)) == 'Telefone não cadastrado'
    assert blocked_reason(lead(phone='5511999999999')) == 'Número excluído do envio'
    assert blocked_reason(lead(status='sem_interesse')) == 'Contato sem interesse'
    assert blocked_reason(lead(status='convertido')) == 'Contato convertido'


def test_list_requires_authentication_and_valid_filters():
    with TestClient(app) as client:
        assert client.get('/api/v1/crm/evolution/leads').status_code == 401


@pytest.mark.parametrize('audience', ['all', 'ready', 'missing_phone'])
def test_query_scopes_every_count_and_page_to_tenant(monkeypatch, audience):
    from app.api.v1 import whatsapp_leads as module
    from app.core.config import settings
    org = uuid4()
    monkeypatch.setattr(settings, 'evolution_organization_id', str(org))
    monkeypatch.setattr(settings, 'evolution_excluded_phones', '5511999999999')
    lead = SimpleNamespace(id=uuid4(), name='Example', instagram='example', city='Example City',
        status='aguardando', priority='alta', phone=None if audience == 'missing_phone' else '5511777777777',
        bot_paused=False, last_contact_on=date(2026, 1, 1), next_contact_on=None)
    class DB:
        queries = []
        async def execute(self, query):
            self.queries.append(query)
            params = query.compile().params
            assert org in params.values()
            assert '100/%' in params.values(), 'Search wildcard must be escaped'
            if len(self.queries) <= 4: return SimpleNamespace(scalar_one=lambda: 1)
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: [lead]))
    db = DB()
    result = asyncio.run(module.leads(db, SimpleNamespace(organization_id=org), q='100%', audience=audience,
                                       priority='alta', status='aguardando', offset=25, limit=25))
    assert len(db.queries) == 5 and result['offset'] == 25
    assert result['items'][0]['can_message'] is (audience != 'missing_phone')
    page = str(db.queries[-1])
    if audience == 'ready':
        assert 'IS NOT NULL' in page and 'NOT IN' in page
        params = db.queries[-1].compile().params
        assert ['5511999999999'] in params.values()
    elif audience == 'missing_phone':
        assert 'IS NULL' in page
    assert 'ORDER BY CASE' in page


def test_other_organization_cannot_read_integration(monkeypatch):
    from app.api.v1 import whatsapp_leads as module
    from app.core.config import settings
    monkeypatch.setattr(settings, 'evolution_organization_id', str(uuid4()))
    with pytest.raises(HTTPException) as error:
        asyncio.run(module.leads(None, SimpleNamespace(organization_id=uuid4())))
    assert error.value.status_code == 404
