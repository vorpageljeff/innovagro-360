from app.core.config import settings


def excluded_phones():
    return {phone.strip() for phone in settings.evolution_excluded_phones.split(',') if phone.strip()}


def blocked_reason(lead):
    if lead.phone in excluded_phones():
        return 'Número excluído do envio'
    if lead.status == 'sem_interesse':
        return 'Contato sem interesse'
    if lead.status == 'convertido':
        return 'Contato convertido'
    if not lead.phone:
        return 'Telefone não cadastrado'
    return None
