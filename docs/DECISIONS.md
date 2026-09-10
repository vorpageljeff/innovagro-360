# Registro de decisões

## ADR-001 — Monorepo por aplicações

**Status:** aceita — 10/09/2026

Web e API ficam em `apps/`, com documentação central em `docs/`. Isso mantém implantação independente sem separar o modelo conceitual.

## ADR-002 — Tenant derivado da sessão

**Status:** aceita — 10/09/2026

O `organization_id` efetivo é obtido da sessão autenticada. IDs enviados pelo cliente não definem escopo. Repositórios e serviços aplicam o filtro de organização e testes verificam vazamento entre tenants.

## ADR-003 — Celery no worker inicial

**Status:** aceita — 10/09/2026

Foi escolhido Celery com Redis por maturidade operacional e suporte amplo. Pode ser reavaliado antes de existirem contratos públicos de tarefas.

## ADR-004 — Tokens bearer no esqueleto de API

**Status:** provisória — 10/09/2026

O backend inicia com access/refresh tokens e rotação de refresh. Antes da interface de login produtiva, será decidida a custódia em cookie HttpOnly com CSRF ou BFF do Next.js.

