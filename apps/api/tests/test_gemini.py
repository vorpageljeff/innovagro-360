import asyncio
import json
from types import SimpleNamespace
import httpx
import pytest
from app.services import whatsapp_ai as service

@pytest.mark.parametrize('state,status,success', [('STOP',200,True),('MAX_TOKENS',200,False),('SAFETY',200,False),('STOP',429,False),('BAD_JSON',200,False)])
def test_gemini_contract_safe_errors_and_history(monkeypatch,state,status,success):
    for key,value in {'whatsapp_ai_enabled':True,'whatsapp_ai_provider':'gemini','gemini_api_key':'secret-fixture','whatsapp_ai_model':'gemini-2.5-flash-lite','whatsapp_ai_knowledge':'Empresa de teste'}.items():monkeypatch.setattr(service.settings,key,value)
    original=httpx.AsyncClient
    def respond(request):
        assert request.url.host=='generativelanguage.googleapis.com'
        assert 'secret-fixture' not in str(request.url)
        assert request.headers['x-goog-api-key']=='secret-fixture'
        body=json.loads(request.content)
        assert body['generationConfig']['responseMimeType']=='application/json'
        assert body['generationConfig']['responseJsonSchema']['additionalProperties'] is False
        assert body['contents'][1]['role']=='model'
        output=json.dumps({'reply':'Olá! Como posso ajudar?','handoff':False,'priority':'media'}) if state!='BAD_JSON' else 'invalid'
        return httpx.Response(status,json={'candidates':[{'finishReason':state,'content':{'parts':[{'text':output}]}}]})
    monkeypatch.setattr(service.httpx,'AsyncClient',lambda **kwargs:original(transport=httpx.MockTransport(respond),**kwargs))
    history=[SimpleNamespace(incoming='Olá',reply='Sou o assistente.',state='sent')]
    if success:assert asyncio.run(service.answer(history,'Quero um site')).handoff is False
    else:
        with pytest.raises(service.AIUnavailable) as caught:asyncio.run(service.answer(history,'Quero um site'))
        assert 'secret' not in str(caught.value)


def test_test_mode_only_selected_phone_and_variants(monkeypatch):
    monkeypatch.setattr(service.settings,'whatsapp_ai_test_mode',True)
    monkeypatch.setattr(service.settings,'whatsapp_ai_test_phones','5545999991234')
    assert service.test_contact_allowed('5545999991234')
    assert service.test_contact_allowed('554599991234')
    assert not service.test_contact_allowed('5585999991234')
    monkeypatch.setattr(service.settings,'whatsapp_ai_test_phones','')
    assert not service.test_contact_allowed('5545999991234')
