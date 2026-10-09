from uuid import uuid4
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.crm import LeadInput
from app.api.v1.site_intake import SiteIntake, intake_note


def payload(**changes):
    return dict(submission_id=str(uuid4()),name='Pessoa Exemplo',company='',email='exemplo@example.com',phone='(45) 99828-7556',city='Toledo',state='PR',service='Site',need='Apresentar serviços',current='',timing='Estou conhecendo as possibilidades',consent=True,**changes)


def test_phone_normalization_and_complete_note():
    data=SiteIntake(**payload())
    assert data.phone=='5545998287556'
    note=intake_note(data)
    assert 'E-mail: exemplo@example.com' in note and 'Origem: site Voragon' in note

@pytest.mark.parametrize('field,value',[('email','errado'),('phone','123'),('phone','++abc5545998287556'),('consent',False),('name',' '),('need',' '),('timing','qualquer')])
def test_rejects_incomplete_or_unconsented_request(field,value):
    p=payload();p[field]=value
    with pytest.raises(ValidationError):SiteIntake(**p)


def test_origin_and_honeypot_rejected_without_db_write():
    from app.db.session import get_db
    async def no_db():yield None
    app.dependency_overrides[get_db]=no_db
    try:
        with TestClient(app) as c:
            assert c.post('/api/v1/public/site-leads',json=payload(),headers={'Origin':'https://other.example'}).status_code==403
            p=payload();p['website']='spam'
            assert c.post('/api/v1/public/site-leads',json=p,headers={'Origin':'https://voragon.vercel.app'}).status_code==422
            r=c.options('/api/v1/public/site-leads',headers={'Origin':'https://voragon.vercel.app','Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type'})
            assert r.status_code==200 and r.headers['access-control-allow-origin']=='https://voragon.vercel.app'
    finally:app.dependency_overrides.clear()
