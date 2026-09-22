# Acessos — InnovAgro 360

Verificados em 21/09/2026.

- Dashboard: https://innovagro-360.vercel.app/dashboard
- CRM: https://innovagro-360.vercel.app/crm
- Login: https://innovagro-360.vercel.app/login
- Projeto na Vercel: https://vercel.com/vorpageljeffs-projects/innovagro-360
- Equipe: vorpageljeffs-projects
- Projeto: innovagro-360
- ID: prj_6sMieg2q9g2H1Vfb5z1oYnJhiAMn

## Desenvolvimento e publicação

A raiz deste repositório está vinculada ao projeto por `.vercel/project.json` (ignorado pelo Git). Execute a CLI a partir de `360_CRM_Gestao`. O frontend fica em `apps/web`; o `vercel.json` da raiz define Next.js, `npm run build:web` e saída `apps/web/.next`. A configuração remota informa raiz `.`; não alterar para `apps/web` sem ajustar os comandos de build.

A CLI disponível nesta máquina usa o Node em `/Users/jeffersonvorpagel/.local/share/techa-publish-tools/node-v22.23.2-darwin-arm64/bin`. Acrescente esse diretório ao PATH antes de usar `npx vercel`.

A vinculação gerou `.env.local`, ignorado pelo Git. Não compartilhar seu conteúdo nem copiar credenciais para documentação.

## Histórico anterior à primeira instalação

Deploy de produção Ready; fluxo login → dashboard → CRM verificado. O login atual é de demonstração. A versão publicada usa o CRM demonstrativo. A adaptação em desenvolvimento agora possui rotas autenticadas de leads e histórico, descritas em `CRM_PROSPECCAO.md`; ainda não foi publicada nem conectada ao backend existente. A vinculação Vercel não conecta um banco de dados nem implementa importação de leads.

Critérios e candidatos da prospecção estão em `../Voragon_Comercial` (pasta irmã deste repositório). Antes de importar dados reais, implementar armazenamento central autenticado, isolamento por organização e prevenção de duplicatas. Nenhum lead foi importado nesta configuração de acesso.

## VPS confirmada após acesso ao console (antes da instalação)

Hostinger: `srv1964191.hstgr.cloud`, IP `2.25.189.129`. SSH funciona com usuário `innovagro` e a chave existente `~/.ssh/transboes_hostinger`. Login SSH como root é desabilitado; preservar essa proteção. O usuário pertence ao grupo Docker; sudo requer senha.

Inventário remoto: aplicações `/opt/innovagro/apps/techa` e `/opt/innovagro/apps/transboes`, além de Traefik, Portainer e Uptime Kuma. Nenhum container, volume ou diretório do CRM 360 foi localizado nos caminhos inspecionados (`/opt/innovagro`, `/home/innovagro`, `/srv`). As instâncias PostgreSQL ativas listam apenas `techa_db` e `transboes`, além de `postgres`. Isso não comprova ausência em outro servidor ou serviço externo. Backend e banco específicos do CRM ainda precisam ser identificados; nenhuma migração/importação foi feita.

## Primeira instalação autorizada — 21/09/2026 (22/09 UTC)

Jefferson confirmou que se trata da primeira instalação e autorizou criar o backend nesta VPS.

- Aplicação: `/opt/innovagro/apps/crm360`; compose `deploy/compose.hostinger-crm.yml`, projeto `voragon-crm`.
- API HTTPS: https://crm-api.2.25.189.129.nip.io/api/v1 ; health em `/health`.
- Containers: `voragon-crm-api-1` e `voragon-crm-db-1`; volume persistente `voragon-crm_crm_postgres`. Banco sem porta pública.
- Migrações: `20260921_0002`, aplicadas. Organização `voragon`. Credenciais fora do Git em `~/.config/voragon-crm/`; configuração do servidor em `.env.production` com permissão restrita.
- Vercel: `CRM_API_URL`, `CRM_ORGANIZATION_SLUG`, `DEMO_SESSION_TOKEN` configuradas em Preview e Production. Apesar do nome legado, o último é um segredo aleatório para a sessão da interface; o acesso aos leads exige também JWT da API. Login agora valida o usuário no banco.
- Fonte do código publicado: `0d46005`; backup operacional adicionado em `e8f4d1b`.
- Importação real: dez lojas, dez eventos de contato, contato em 21/09 e acompanhamento em 28/09. Reimportação idempotente e leitura em nova sessão verificadas. Nenhum retorno foi presumido.
- Backup completo após importação: https://drive.google.com/file/d/1Fb967C4_UYL_rWtqKvHHLvCGn8R7SEyp/view ; restaurado em banco temporário isolado e conferido (10 leads/10 eventos). Banco temporário removido após teste.
- Backup diário na VPS às 04:30 no fuso do servidor; script `deploy/backup-crm.sh`, saída `/opt/innovagro/backups/crm360/`. Upload externo periódico ainda não automatizado. Não confundir snapshots na mesma VPS com backup externo.
- O CRM de contatos/histórico persiste no servidor. Os demais módulos de demonstração não foram migrados nesta entrega.

### Produção verificada

Vercel produção Ready: `dpl_BHzAjdy72MkS5KVyUrd3Eqx14P7p`, URL https://innovagro-360.vercel.app/crm. Login real → CRM testado no navegador; dez contatos e seus históricos visíveis, campos de retorno presentes, sem erros JavaScript e sem localStorage do CRM. Layout conferido em desktop e largura de 390px. O usuário verifica as respostas no Instagram e as anota manualmente.

Identificador de login inicial: `jefferson@voragon.vercel.app` (não representa caixa postal criada). Senha inicial aleatória em arquivo privado `~/.config/voragon-crm/ACESSO-CRM.txt`, fora do repositório.
