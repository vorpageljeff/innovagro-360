# Arquitetura

## Visão geral

O InnovAgro 360 é um monorepo com frontend Next.js implantado na Vercel e API FastAPI implantada em VPS. PostgreSQL é a fonte de verdade; Redis sustenta filas, rate limiting e cache. Todas as entidades de negócio pertencem a uma organização.

```text
Browser → Next.js/Vercel → FastAPI (/api/v1) → PostgreSQL
                                  ├──────────→ Redis
                                  └──────────→ Celery worker
```

## Fronteiras

- `apps/web`: apresentação, navegação, validação de experiência e controle de visibilidade.
- `apps/api`: regras de negócio, autorização, isolamento por tenant e auditoria.
- O frontend nunca é a autoridade de permissão.
- Ações de domínio relevantes usam endpoints explícitos e transações.

## Segurança

Tokens de acesso têm curta duração. Refresh tokens são rotacionáveis e armazenados apenas como hash. Senhas usam Argon2id. Toda consulta de negócio recebe `organization_id` do contexto autenticado, nunca do corpo fornecido pelo cliente.

## Observabilidade

Cada resposta recebe `X-Request-ID`; logs são estruturados. `/health` mede vida do processo e `/ready` mede dependências. Erros da API usam um envelope estável.

## Implantação

Produção separa web e API. PostgreSQL e Redis ficam em rede privada e não expõem portas públicas. HTTPS termina no provedor/reverse proxy. Backups PostgreSQL são diários, externos ao VPS e testados periodicamente.

