# Publicação do CRM na VPS existente

O destino ativo é Hostinger, usuário SSH `innovagro`, aplicação `/opt/innovagro/apps/crm360`. Consulte `../docs/ACESSOS.md`.

Use `docker compose -f deploy/compose.hostinger-crm.yml`. O compose usa Traefik e a rede externa `proxy` já existentes; não execute o compose antigo com Caddy em produção, pois disputaria as portas 80/443.

Sequência: Git push do código revisado; backup externo com recuperação verificada; transferir a versão exata sem sobrescrever `.env.production`; build da API; `docker compose -f deploy/compose.hostinger-crm.yml run --rm api alembic upgrade head`; `docker compose -f deploy/compose.hostinger-crm.yml up -d`; conferir HTTPS, autenticação e banco; preview Vercel e promoção validada. Nunca remover o volume `voragon-crm_crm_postgres`.

Na Vercel a raiz é o repositório, com `vercel.json` configurando `apps/web`. `CRM_API_URL` é variável privada de servidor; não expor JWT ou senha via NEXT_PUBLIC. O login usa a organização `CRM_ORGANIZATION_SLUG`.

Backup: `bash deploy/backup-crm.sh`. O agendamento diário guarda snapshots na VPS; manter também cópias externas. Credenciais, dumps e relatórios comerciais ficam fora do Git.
