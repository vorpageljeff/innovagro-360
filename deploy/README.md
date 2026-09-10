# Implantação de produção

## DNS

- `app.seudominio.com` aponta para a Vercel.
- `api.seudominio.com` possui registro A para o IP público do VPS Hostinger.

## Backend no VPS

Pré-requisitos: Docker Engine, Compose plugin, Git e portas 80/443 abertas.

1. Clone o repositório em um usuário sem privilégios de root.
2. Copie `.env.production.example` para `.env` e gere segredos fortes.
3. Execute `docker compose -f docker-compose.prod.yml config`.
4. Execute `docker compose -f docker-compose.prod.yml up -d --build`.
5. Verifique `https://api.seudominio.com/health` e os logs.

PostgreSQL e Redis não publicam portas no host. Caddy emite e renova HTTPS automaticamente após o DNS apontar para o VPS.

## Frontend na Vercel

Crie/vincule um projeto cujo Root Directory seja `apps/web`. Cadastre `NEXT_PUBLIC_API_URL` para Production e Preview. Faça primeiro um preview, valide-o e depois promova o mesmo artefato para produção.

## Atualização e rollback

Atualização do backend exige `git pull`, rebuild e verificação do health endpoint. Antes de migrations destrutivas, produza backup externo. O frontend pode ser revertido instantaneamente pela Vercel.

