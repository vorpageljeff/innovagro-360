"""Editable starting flows for inbound commercial service; no outbound campaign."""

def commercial_templates():
    return [
        dict(name='Não contatar', position=0, enabled=True, contains='parar|nao quero|sem interesse|cancelar atendimento', reply='', priority='baixa', status='sem_interesse', handoff=True),
        dict(name='Falar com atendente', position=10, enabled=True, contains='3|atendente|humano|falar com uma pessoa', reply='Vou encaminhar a conversa para nossa equipe. Pode deixar sua dúvida aqui; o atendimento continua com uma pessoa.', priority='alta', status='respondeu', handoff=True),
        dict(name='Orçamento — atendimento inicial', position=20, enabled=True, contains='1|orcamento|preco|valor', reply='Para ajudar com seu orçamento, conte o nome da sua empresa, o serviço que procura e o objetivo do projeto. Nossa equipe continuará o atendimento por aqui.', priority='alta', status='respondeu', handoff=True),
        dict(name='Conhecer serviços', position=30, enabled=True, contains='2|servicos|site|sistema|crm|automacao', reply='Podemos conversar sobre sites, sistemas e automações para sua empresa. Para solicitar orçamento, responda 1. Para falar com nossa equipe, responda 3.', priority='media', status='respondeu', handoff=False),
        dict(name='Suporte e dúvidas', position=40, enabled=True, contains='suporte|erro|problema|ajuda', reply='Vou encaminhar sua solicitação para nossa equipe. Descreva o problema e o serviço envolvido para ajudar no atendimento.', priority='urgente', status='respondeu', handoff=True),
        dict(name='Boas-vindas e menu', position=1000, enabled=True, contains='', reply='Olá! Sou o assistente de atendimento. Como podemos ajudar?\n\n1 — Solicitar orçamento\n2 — Conhecer serviços\n3 — Falar com atendente', priority=None, status='respondeu', handoff=False),
    ]
