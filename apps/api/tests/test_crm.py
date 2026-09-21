from datetime import date
from types import SimpleNamespace
from uuid import uuid4
import asyncio
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.main import app
from app.schemas.crm import LeadInput, ActivityInput
from app.services.crm import apply_activity
from app.api.v1.crm import get_lead


def lead(**kwargs):
    return SimpleNamespace(status='aguardando', last_contact_on=None, next_contact_on=None, **kwargs)

def event(kind='contato', day=date(2026, 9, 21), **kwargs):
    return ActivityInput(kind=kind, occurred_on=day, note='teste', event_key='event-1', **kwargs)

def test_seven_days_and_year_boundary():
    item=lead()
    apply_activity(item,event(day=date(2025,12,28)))
    assert item.next_contact_on == date(2026,1,4)

def test_response_stops_reminder_and_preserves_last_contact():
    item=lead(); apply_activity(item,event())
    apply_activity(item,event('retorno'))
    assert item.status=='respondeu' and item.next_contact_on is None
    assert item.last_contact_on==date(2026,9,21)

def test_terminal_status_never_schedules_followup():
    item=lead(); apply_activity(item,event('retorno',status='sem_interesse',next_contact_on=date(2026,10,2)))
    apply_activity(item,event())
    assert item.next_contact_on is None

def test_historical_import_does_not_reopen_response_or_move_contact_backwards():
    item=lead(); apply_activity(item,event()); apply_activity(item,event('retorno'))
    apply_activity(item,event(day=date(2026,9,1)))
    assert item.status=='respondeu' and item.next_contact_on is None
    assert item.last_contact_on==date(2026,9,21)

def test_explicit_followup_after_reply():
    item=lead(); apply_activity(item,event('retorno',next_contact_on=date(2026,9,28)))
    assert item.next_contact_on==date(2026,9,28)

@pytest.mark.parametrize('profile', ['@Loja.Exemplo', 'https://www.instagram.com/Loja.Exemplo/?igsh=abc'])
def test_normalized_identity(profile):
    data=LeadInput(name='Loja',instagram=profile,contacted_on='2026-09-21',event_key='1')
    assert data.instagram=='loja.exemplo'

@pytest.mark.parametrize('profile',['https://evil.example/loja','https://instagram.com/p/abc','foo/bar','a..b','javascript:alert(1)'])
def test_invalid_profile(profile):
    with pytest.raises(ValidationError):
        LeadInput(name='Loja',instagram=profile,contacted_on='2026-09-21',event_key='1')

def test_requires_authenticated_backend_session():
    with TestClient(app) as client:
        assert client.get('/api/v1/crm/leads').status_code==401
        assert client.post('/api/v1/crm/import',json={'leads':[]}).status_code in (401,422)

def test_tenant_filter_prevents_cross_organization_access():
    org=uuid4(); target=uuid4()
    class DB:
        async def execute(self, query):
            values=query.compile().params
            assert org in values.values() and target in values.values()
            return SimpleNamespace(scalar_one_or_none=lambda:None)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(get_lead(DB(),SimpleNamespace(organization_id=org),target))
    assert exc.value.status_code==404


def test_duplicate_import_does_not_add_activity_or_replace_response():
    from app.api.v1.crm import add_contact
    target=uuid4()
    item=SimpleNamespace(id=target,status='respondeu',last_contact_on=date(2026,9,21),next_contact_on=None)
    previous=SimpleNamespace(lead_id=target,kind='contato',occurred_on=date(2026,9,21),note='Original')
    class DB:
        calls=0
        async def execute(self, query):
            self.calls+=1
            if self.calls==1:return None
            if self.calls==2:return SimpleNamespace(scalar_one=lambda:item)
            return SimpleNamespace(scalar_one_or_none=lambda:previous)
        def add(self, value):raise AssertionError('Evento duplicado não deve ser inserido')
    data=LeadInput(name='Loja',instagram='@loja',contacted_on='2026-09-21',event_key='original',note='Original')
    result=asyncio.run(add_contact(data,DB(),SimpleNamespace(organization_id=uuid4())))
    assert result.status=='respondeu' and result.next_contact_on is None


def test_event_key_cannot_be_reused_for_another_lead():
    from app.api.v1.crm import add_contact
    item=SimpleNamespace(id=uuid4())
    previous=SimpleNamespace(lead_id=uuid4())
    class DB:
        calls=0
        async def execute(self, query):
            self.calls+=1
            if self.calls==1:return None
            if self.calls==2:return SimpleNamespace(scalar_one=lambda:item)
            return SimpleNamespace(scalar_one_or_none=lambda:previous)
    data=LeadInput(name='Loja',instagram='@loja',contacted_on='2026-09-21',event_key='reused')
    with pytest.raises(HTTPException) as exc:
        asyncio.run(add_contact(data,DB(),SimpleNamespace(organization_id=uuid4())))
    assert exc.value.status_code==409
