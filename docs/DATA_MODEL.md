# Modelo de dados

## Convenções

- IDs UUID.
- Horários em UTC; exibição em `America/Sao_Paulo`.
- Valores monetários em `numeric`, nunca `float`.
- Entidades de negócio têm `organization_id`, timestamps e soft delete quando aplicável.
- Índices compostos começam por `organization_id` nos acessos por tenant.

## Fundação (Fase 0)

```text
organizations ──< memberships >── users
      │                  └──────── roles ──< role_permissions >── permissions
      └──< audit_logs
users ──< refresh_sessions
```

`memberships` representa a participação de uma pessoa numa organização. Papéis pertencem à organização; permissões são chaves globais estáveis. A auditoria guarda snapshots JSON antes/depois.

## Domínios seguintes

- CRM: accounts, contacts, pre_leads, leads, opportunities, interactions, proposals, contracts.
- Projetos: projects, deliverables, tasks, time_entries, risks, issues, change_requests.
- Financeiro: receivables, payables, payments, categories, cost_centers, budgets.

As relações devem reutilizar `accounts` e projetos; não serão criadas cópias de cliente por módulo.

