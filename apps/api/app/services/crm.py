from datetime import timedelta


def apply_activity(lead, activity):
    # Datas civis evitam deslocamento de dia por timezone. Histórico antigo não
    # deve reabrir um lead que já recebeu retorno.
    if activity.kind == 'contato':
        if lead.last_contact_on is None or activity.occurred_on > lead.last_contact_on:
            lead.last_contact_on = activity.occurred_on
            if lead.status == 'aguardando':
                lead.next_contact_on = activity.occurred_on + timedelta(days=7)
    if activity.kind == 'retorno':
        lead.status = activity.status or 'respondeu'
        lead.next_contact_on = activity.next_contact_on
    elif activity.status is not None:
        lead.status = activity.status
        if lead.status != 'aguardando':
            lead.next_contact_on = None
    if activity.next_contact_on is not None:
        lead.next_contact_on = activity.next_contact_on
    if lead.status in ('sem_interesse', 'convertido'):
        lead.next_contact_on = None
