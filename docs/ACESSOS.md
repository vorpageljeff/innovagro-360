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


## Evolution, Kanban e fluxos — 07/10/2026

Código da API/interface: `5a03d438672ba27603a18c59973c0d9c5ba8ccf9`, enviado à branch `feature/crm-evolution-20261007`. Produção Vercel `dpl_GURJjmDDawjeA3BYJ4yqHcxubksy`, promovida para o endereço principal. A cópia limpa usada na publicação excluiu alterações locais de outras tarefas.

Backend em `/opt/innovagro/apps/crm360/releases/5a03d43`, imagem `voragon-crm-api:evolution-5a03d43`; `CURRENT_RELEASE` aponta essa versão. O diretório raiz histórico não foi sobrescrito. Usar os compose da release, incluindo `deploy/compose.evolution.yml` e o override privado `deploy/runtime-image.yml`, nas próximas operações. Schema `20261007_0003`, 31 contatos e 31 atividades preservados. API e bancos saudáveis.

Evolution v2.3.7 instalado no mesmo projeto Docker, rede privada da integração sem novas portas públicas. Instância `crm360`, organização `voragon`, webhook interno configurado e autenticado. Chaves em `.env.production` e `.env.evolution`, fora do Git; configuração anterior preservada para recuperação. A integração ainda aguarda o usuário escanear o QR pelo painel Automações. Um fluxo “Orçamento — atendimento inicial” foi salvo pausado; nenhuma mensagem comercial foi enviada.

Verificação em navegador na produção: login, 31 contatos, gravação da prioridade existente e persistência após reload, cadastro/leitura do fluxo pausado, QR renderizado, telas desktop e 390px; zero erros JavaScript. Envio/recebimento reais ainda dependem da vinculação do WhatsApp. A rota pública `/health` retornou 404 no proxy nesta conferência; o health interno Docker está saudável, e as rotas públicas autenticadas responderam 200 após login.

Backup recuperável anterior à migração e limites estão em `EVOLUTION_AUTOMACOES.md`. O script diário foi estendido para incluir banco e instâncias do Evolution. Cópias externas automáticas continuam pendentes.


## Atendimento completo configurado — 07/10/2026

Código publicado `29b3422e274eafd0ab00aa7e83649da3f447ccb6`, branch `feature/crm-evolution-20261007`. Release backend `/opt/innovagro/apps/crm360/releases/29b3422`, imagem `voragon-crm-api:bot-29b3422`, schema `20261007_0004`; `CURRENT_RELEASE` atualizado. Frontend produção `dpl_dGLKLc6Hw6k9zJc1ZdXJU8FGbBw6`, promovido após validação da API autenticada e simulação através da Vercel.

Seis fluxos comerciais foram cadastrados ativos, com ordem de execução, menu 1/2/3, serviços, orçamento, atendente, suporte e encerramento. Respostas não incluem preços, prazos ou promessas comerciais inventadas. Contatos novos por WhatsApp entram no Kanban sem Instagram fictício. Encaminhamento humano pausa novas respostas automáticas por contato; bot pode ser retomado pela interface.

35 testes passaram. Teste adicional em PostgreSQL restaurado e isolado confirmou criação de contato, menu, orçamento, encaminhamento humano, rejeição de evento duplicado e pausa das mensagens seguintes. Os dois envios desse teste foram substituídos por função simulada; zero mensagens externas. Banco temporário removido.

Produção verificada no navegador: login, 31 contatos, assumir/retomar atendimento, cinco caminhos no simulador, seis fluxos persistentes após reload, QR e tela de 390px; zero erros JavaScript. `/health` público retornou 200 após o container ficar saudável. Os 404 observados durante substituição da API ocorreram antes da liberação do container pelo proxy; não persistiram. Evolution permanece aguardando vinculação pelo QR. A entrega não comprova envio real, que depende do aparelho vinculado e de uma mensagem recebida.

Backup antes da migração: `crm-20261007T121119Z.dump`, acompanhado do banco e instâncias Evolution; cópias privadas fora da VPS. Restauração e migração desse backup foram usadas no teste PostgreSQL descrito acima. Backup final da configuração também gerado e copiado para fora da VPS. Permanecem pendentes cópias externas automáticas, em vez da cópia manual realizada nesta sessão.


### Respostas automáticas pausadas por Jefferson — 07/10/2026

Evolution confirmou conexão `open` com a conta indicada pelo usuário. Em seguida, a pedido explícito de Jefferson, a configuração persistente da API foi alterada para `EVOLUTION_BOT_ENABLED=false`; API recriada e flag conferida. Manter essa pausa nos próximos deployments. A conexão e os fluxos foram preservados. Não reativar envios sem nova instrução do usuário.


## Painel de controle WhatsApp — 07/10/2026

URL https://innovagro-360.vercel.app/whatsapp, com acesso pelo menu comercial e pelo CRM. API/interface publicadas a partir de `6050e62`; release backend `/opt/innovagro/apps/crm360/releases/6050e62`, imagem `voragon-crm-api:dashboard-6050e62`. Deploy Vercel `dpl_EZZFMbNVDzEpNfgrTcFs6Lyt8zQZ` promovido após consulta autenticada à nova API. Nenhuma migração de banco foi necessária.

Painel consulta mensagens reais, respostas aceitas pelo Evolution, contatos novos, fila atual de atendimento humano, fluxos ativos e envios sem confirmação. Períodos de 1 a 30 dias usam calendário de São Paulo; fila humana é atual. Traz gráfico diário, últimas 20 mensagens, conversa com até 100 registros, assumir/retomar por contato e editor/simulador de fluxos. Pausa global solicitada pelo usuário foi mantida: conexão `open`, `EVOLUTION_BOT_ENABLED=false` antes e depois do deploy. Liberar um contato para bot não remove a pausa global.

Validação: 38 testes passaram; build Next.js concluído; consulta ao PostgreSQL real conferida; navegador em produção verificou autenticação obrigatória, indicadores, períodos, conversa, versão de 390px sem overflow da página, fluxos e atualização automática a cada 30 segundos. Zero erros JavaScript. Nenhum envio foi realizado nesta entrega. Backup final `crm-20261007T150127Z.dump`, banco e instâncias Evolution copiados para diretório privado fora da VPS.
