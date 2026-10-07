import asyncio
from datetime import date, datetime, timezone
from types import SimpleNamespace
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.whatsapp_dashboard import dashboard, period_start


def test_calendar_period_uses_brazilian_day():
    now = datetime(2026, 10, 8, 1, 30, tzinfo=timezone.utc)
    assert period_start(now, 1).date() == date(2026, 10, 7)
    assert period_start(now, 7).date() == date(2026, 10, 1)


def test_dashboard_requires_authentication():
    with TestClient(app) as client:
        assert client.get('/api/v1/crm/evolution/dashboard').status_code == 401


def test_summary_series_and_tenant_scoping():
    org = uuid4()
    today = period_start(datetime.now(timezone.utc), 1).date()
    class DB:
        calls = 0
        async def execute(self, query):
            self.calls += 1
            params = query.compile().params
            assert org in params.values(), 'Every dashboard query must restrict its organization'
            if self.calls == 1:
                return SimpleNamespace(all=lambda: [('sent', 2), ('paused', 3), ('uncertain', 1)])
            if self.calls in (2, 3, 4, 5):
                count = {2: 6, 3: 2, 4: 1, 5: 1}[self.calls]
                return SimpleNamespace(scalar_one=lambda: count)
            if self.calls == 6:
                return SimpleNamespace(all=lambda: [SimpleNamespace(day=today, received=6, sent=2)])
            if self.calls == 7:
                return SimpleNamespace(all=lambda: [])
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []))
    result = asyncio.run(dashboard(DB(), SimpleNamespace(organization_id=org), days=7))
    assert result['summary'] == {'received': 6, 'sent': 2, 'new_contacts': 2, 'waiting_human': 1, 'attention': 1, 'active_rules': 6}
    assert len(result['series']) == 7
    assert result['series'][-1] == {'day': today.isoformat(), 'received': 6, 'sent': 2}
    assert result['series'][0]['received'] == 0
