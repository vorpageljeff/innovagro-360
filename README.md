# InnovAgro 360

Monorepo da plataforma integrada de CRM, projetos, financeiro e gestão.

## Estrutura

- `apps/web`: Next.js, TypeScript e Tailwind CSS
- `apps/api`: FastAPI, SQLAlchemy 2 e Alembic
- `docs`: especificação, arquitetura, modelo de dados e roadmap

## Desenvolvimento

1. Copie `.env.example` para `.env`.
2. Execute `docker compose up --build` para API, worker, PostgreSQL e Redis.
3. Em outro terminal, execute `npm install` e `npm run dev:web` (Node 20+).

API: `http://localhost:8000`  
OpenAPI: `http://localhost:8000/docs`  
Web: `http://localhost:3000`

As instruções de produção para Hostinger e Vercel estão em `deploy/README.md`.
