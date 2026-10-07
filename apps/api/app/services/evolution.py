from urllib.parse import quote
import httpx
from fastapi import HTTPException
from app.core.config import settings


def configured():
    return all((settings.evolution_api_url, settings.evolution_api_key,
                settings.evolution_instance, settings.evolution_organization_id,
                settings.evolution_webhook_secret))


async def evolution_request(method, endpoint, payload=None):
    if not configured():
        raise HTTPException(503, 'Evolution ainda não configurado no servidor.')
    url = f"{settings.evolution_api_url.rstrip('/')}/{endpoint}/{quote(settings.evolution_instance, safe='')}"
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=False) as client:
            response = await client.request(method, url, headers={'apikey': settings.evolution_api_key}, json=payload)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError):
        raise HTTPException(502, 'Não foi possível confirmar a operação no Evolution.') from None


def incoming_message(payload):
    if str(payload.get('event', '')).lower().replace('_', '.') != 'messages.upsert':
        return None
    data = payload.get('data')
    if not isinstance(data, dict):
        return None
    key = data.get('key', {})
    if not isinstance(key, dict) or key.get('fromMe') is not False:
        return None
    jid = key.get('remoteJid', '')
    if not isinstance(jid, str) or not jid.endswith('@s.whatsapp.net'):
        return None
    phone = jid.split('@')[0]
    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        return None
    message = data.get('message', {})
    if not isinstance(message, dict):
        return None
    extended = message.get('extendedTextMessage', {})
    text = message.get('conversation') or (extended.get('text') if isinstance(extended, dict) else None)
    message_id = key.get('id')
    if not isinstance(text, str) or not text.strip() or not isinstance(message_id, str) or not 1 <= len(message_id) <= 200:
        return None
    return phone, message_id, text[:10000]


def matching_rule(rules, text):
    # First matching rule wins, in creation order.
    return next((rule for rule in rules if rule.enabled and rule.contains.casefold() in text.casefold()), None)
