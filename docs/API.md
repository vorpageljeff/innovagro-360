# API

Base: `/api/v1`. JSON usa nomes em inglês e datas ISO 8601.

## Respostas e erros

Listas serão paginadas no servidor. Erros seguem:

```json
{"error":{"code":"validation_error","message":"Dados inválidos.","details":[]},"request_id":"uuid"}
```

## Fundação

- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /auth/me`
- `GET|POST /organizations`
- `GET|POST /users`
- `GET|POST /roles`
- `GET /permissions`
- `GET /audit-logs`

## Regras

- O tenant vem do token/sessão.
- `403` indica falta de permissão e `404` evita revelar recurso de outro tenant.
- Idempotência será obrigatória em pagamentos e conversões críticas.
- Mudanças de estado importantes terão endpoints de domínio.

