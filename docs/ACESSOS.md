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


## IA conversacional no WhatsApp — 07/10/2026

Integração preparada e publicada a partir de `3ec96f4`. Backend release `/opt/innovagro/apps/crm360/releases/3ec96f4`, imagem `voragon-crm-api:ai-3ec96f4`; CURRENT_RELEASE atualizado. Frontend Vercel `dpl_3W3B17ZdAXAZU6jeKJUpkPAb7dgG`, promovido após consulta autenticada à nova rota no deployment protegido. Status disponível em WhatsApp → Fluxos e bot.

Sem migração ou alteração dos dados existentes. API saudável e Evolution conectado (`open`); `EVOLUTION_BOT_ENABLED=false` e `WHATSAPP_AI_ENABLED=false` confirmados após deploy. Configuração pendente: chave da API, modelo e informações da empresa. Não foram realizadas chamadas reais à OpenAI nem envios de mensagens. Referência e comportamento: `docs/WHATSAPP_IA.md`.

Validação: 50 testes passaram (provedor simulado), build Next.js aprovado, preview autenticado aprovado, navegador em produção verificou autenticação, painel IA pendente, pausa global, conexão, layout de 390px e ausência de erros JavaScript. Primeiro login do CRM durante a promoção falhou transitoriamente; a nova sessão posterior passou. Instruções privadas de configuração estão em `deploy/whatsapp-ai.env.example`; arquivo local privado sem chave preparado em `~/.config/voragon-crm/ai.env`, fora do Git. Uso real e custos dependem da conta do titular; ainda não foi validada geração real.


## Lista de leads para WhatsApp — 07/10/2026

Código publicado `499b6ef22b3aa1552d7012b33844c9ef54a3da56`, enviado à branch `feature/crm-evolution-20261007` e confirmado no remoto. Backend release `/opt/innovagro/apps/crm360/releases/499b6ef`, imagem `voragon-crm-api:leads-499b6ef`, CURRENT_RELEASE atualizado. Frontend Vercel `dpl_CbSCYXWK1tUABg19iSmWDCsEwxHt`, promovido após consulta autenticada no deployment protegido. Acessar https://innovagro-360.vercel.app/whatsapp → Leads para contato.

Sem migração ou alteração de leads existentes. Leitura real confirmou 32 leads, 1 com telefone disponível e 31 sem telefone. Configuração privada de exclusões atualizada com o número pessoal solicitado, incluindo a variante brasileira sem nono dígito; cópia privada da configuração anterior preservada no servidor. API saudável, Evolution `open`, bot e IA desabilitados após publicação.

57 testes passaram; build Next.js local e Vercel aprovados; API real verificou disponibilidade, telefones ausentes, filtros, paginação e exclusões. Navegador em produção conferiu autenticação, lista real e filtros; fixtures interceptadas apenas no navegador validaram seleção, bloqueios, link de mensagem individual e formulário de telefone sem modificar o banco. Layout de 390px e ausência de erros JavaScript confirmados. Nenhuma mensagem enviada. Comportamento e limites em `WHATSAPP_LEADS.md`.


## Qualificação e site Voragon — 07/10/2026

Código publicado `a4eb3bc2133e9c1331f554865dd5240d84a6a767`, árvore `3ff90b641dd47da863d16a30201a51a2d04e802a`, branch `feature/crm-evolution-20261007`. Release `/opt/innovagro/apps/crm360/releases/a4eb3bc`, imagem `voragon-crm-api:qualify-a4eb3bc`, CURRENT_RELEASE atualizado; schema `20261007_0004` sem migração. Frontend `dpl_G2zs79z6rfF97jHJBv4qZzk4Sydj`, promovido após status autenticado no preview.

Nome, serviço e necessidade são os campos essenciais (`WHATSAPP_AI_REQUIRED_FIELDS`); empresa opcional. Mensagem completa preparada pelo site, efetivamente recebida no webhook, gera nota de qualificação persistente e deduplicada, prioridade alta e fila humana com bot pausado no contato. Funciona mesmo com pausa global; telefones excluídos e leads encerrados não são encaminhados por esse caminho. Painel de conversa exibe o resumo. IA preparada coleta os mesmos campos antes do encaminhamento; fluxos de atendimento humano continuam prioritários.

Conhecimento da empresa configurado a partir do conteúdo comercial aprovado do site. Faltam chave e modelo de IA. `EVOLUTION_BOT_ENABLED=false` e `WHATSAPP_AI_ENABLED=false` preservados, incluindo exclusões privadas do número pessoal. Evolution conectado; sem chamadas reais à OpenAI ou mensagens enviadas nesta entrega.

61 testes passaram; builds Next.js local e Vercel aprovados. Teste adicional em cópia restaurada do PostgreSQL confirmou resumo persistido, prioridade alta, fila humana e evento duplicado ignorado, com envio e IA substituídos por funções que falhariam se chamadas. Banco temporário removido. Backup anterior `crm-20261007T165929Z.dump`, Evolution e instâncias copiados para diretório privado fora da VPS. Preview autenticado e navegador público conferiram parametrização, configuração pendente e pausa global.

O push Git tradicional retornou erro interno remoto em três tentativas. O código foi salvo pelo conector GitHub, usando árvore idêntica conferida por hash e atualização da branch sem force, com SHA anterior esperado. Fetch posterior confirmou o commit remoto. Alterações locais não relacionadas foram preservadas e excluídas da publicação.

Site público https://voragon.vercel.app e demonstração fictícia https://voragon.vercel.app/demo publicados no projeto original `voragon`, deployment `dpl_2RNKA1rqw8NhTJVQrZHz8gBaPP4m`. Formulário prepara rascunho local e exige confirmação do visitante no WhatsApp. Cinco testes do site, build/lint e navegador na produção aprovados; demonstração sem login, sem banco real e sem envio. Fontes e histórico dessa entrega documentados no README do projeto Voragon_Site.

## Entrada direta de contatos pelo site — 08/10/2026

API publicada a partir de `73b32ba7573a288347553eee5eb10fa80dd0044b`, confirmada no remoto `feature/crm-evolution-20261007`. Release `/opt/innovagro/apps/crm360/releases/73b32ba`, imagem `voragon-crm-api:intake-73b32ba`, CURRENT_RELEASE atualizado. Sem migração de schema. Contato recebido pelo endpoint público do site grava telefone no cadastro e e-mail/resumo no histórico, com prevenção de duplicatas e bot pausado. Referência: `SITE_INTAKE.md`.

70 testes da API passaram. Backup anterior `crm-20261009T012345Z.dump` (nome UTC; realizado em 08/10 no horário de São Paulo) copiado para diretório privado externo. Restauração em banco temporário confirmou contato persistente em nova sessão, notas completas, idempotência, deduplicação de variante de telefone, conflito de chave e limite por contato; banco temporário removido. Nenhum lead fictício gravado na produção. API pública verificou health 200, preflight 200 e rejeição de dados incompletos 422. Bot e IA continuam desabilitados; nenhuma mensagem enviada.

Site Voragon publicado READY `dpl_GoNHsRAHARFc73S71ELDtQmZBghQ`, com página `/conversar`, e-mail/telefone, autorização e envio explícito ao CRM. WhatsApp opcional. Nenhuma alteração ou publicação do frontend do CRM necessária. Dados do contato aparecem no histórico de atendimento.

## Número empresarial para bot — 08/10/2026 (vinculação pendente)

Jefferson autorizou usar o WhatsApp empresarial (45) 99103-8233 e ativar o bot nessa conta. Instância separada `crm360-business` criada; webhook configurado com segredo existente e evento MESSAGES_UPSERT. EVOLUTION_INSTANCE aponta para essa instância. API da release 73b32ba recriada. Instância pessoal crm360 preservada, sem ativar respostas nessa conta. Exclusões privadas do número pessoal preservadas.

QR exibido ao titular; última consulta connecting, ownerJid vazio. EVOLUTION_BOT_ENABLED=false até verificar connectionStatus=open e ownerJid do empresarial (5545991038233 ou variante 554591038233). Depois dessa conferência, a autorização atual permite habilitar os fluxos existentes nesse número, sem pedir autorização novamente. WHATSAPP_AI_ENABLED=false; chave e modelo ausentes. Não declarar bot ativo ou envio testado enquanto vinculação não for confirmada. Nenhuma mensagem externa enviada pelo agente.

### Bot empresarial ativado — 08/10/2026

Titular escaneou QR e confirmou. Evolution crm360-business verificado open, ownerJid correspondente ao empresarial (variante brasileira sem nono dígito). EVOLUTION_BOT_ENABLED=true aplicado somente após essa conferência; API release 73b32ba recriada. Estado open, instância ativa empresarial, webhook habilitado MESSAGES_UPSERT e exclusão do número pessoal confirmados após recriação. Conexão pessoal preservada e sem bot. Autorização desta sessão substitui a pausa global anterior somente para a conta empresarial.

Seis fluxos existentes ativos: boas-vindas/menu, serviços, orçamento, atendente, suporte e não contatar. WHATSAPP_AI_ENABLED=false; falta chave/modelo para IA. Nenhuma mensagem de teste foi enviada pelo agente; resposta real deve ser verificada por mensagem recebida de telefone não excluído. Leads com bot pausado ou encerrados continuam sem resposta automática.

## Gemini publicado para testes — 08/10/2026 (ativação pendente de telefone)

Código `7bd17b4`, branch feature/crm-evolution-20261007, release `/opt/innovagro/apps/crm360/releases/7bd17b4`, imagem `voragon-crm-api:gemini-7bd17b4`. Chave privada no servidor, provedor Gemini e modelo gemini-3.5-flash-lite confirmados. Contexto comercial atualizado para site R$ 450, consultoria R$ 1.000 e mensalidade/projetos sob orçamento. Limite conservador de 50 mensagens por 24h, incluindo fluxos fixos no contador existente. Sem mudança de faturamento Google, sem schema migration.

76 testes passaram. Gemini real respondeu HTTP 200. Teste adicional em PostgreSQL restaurado e isolado confirmou duas respostas com Gemini real e envios WhatsApp simulados, repetição ignorada, qualificação persistente, prioridade alta e pausa humana. Fixture e banco temporário removidos, nenhum cliente fictício cadastrado no banco real. Modelo 2.5 listado, mas indisponível para geração na conta; 3.5 validado. Chave de testes usada por autorização explícita do titular; troca segue pendente.

EVOLUTION_BOT_ENABLED=true no empresarial conectado crm360-business, WHATSAPP_AI_ENABLED=false até titular informar telefone de teste. WHATSAPP_AI_TEST_MODE=true e lista de testes vazia: não enviar conversas de clientes ao plano gratuito. Pergunta enviada ao titular para escolher número pessoal ou outro. Só a confirmação de usar o pessoal autoriza remover sua exclusão para esses testes; não presumir escolha da opção pré-selecionada. Demais exclusões, pausas individuais e contatos encerrados preservados. Após telefone definido, preencher WHATSAPP_AI_TEST_PHONES, habilitar IA, recriar somente API e conferir conexão/flags. Autorização de ativar a IA para testes já dada, não pedir novamente.

## Atualização: IA de teste ativada — 08/10/2026

Autorização posterior confirmou pessoal como remetente e empresarial como destinatário. Release 2f5a777, imagem voragon-crm-api:gemini-2f5a777, somente API recriada. Bot e Gemini habilitados, modo de testes ativo com apenas o pessoal e variante; demais contatos permanecem nos fluxos fixos. Timestamp separa histórico antigo do contexto enviado ao Gemini. Conexão empresarial aberta verificada; geração real e persistência já validadas no banco isolado. A confirmação ponta a ponta no WhatsApp continua pendente de mensagem do titular. Backup externo anterior à ativação: ~/.config/voragon-crm/backups/gemini-test-20261008/crm-20261009T024945Z.dump. Nenhuma migração ou envio WhatsApp pelo agente.

## Continuidade do orçamento — 09/10/2026

Teste real do titular confirmou recebimento/resposta no empresarial. Histórico da sessão registrou duas respostas enviadas, uma de boas-vindas e uma pela regra de orçamento, seguidas de mensagens recebidas sem resposta porque o contato estava pausado. Não foram registrados três envios para o mesmo pedido.

Release 6e3c7dc permite à IA qualificar pedidos de orçamento/preço/valor antes de pausar, preservando encaminhamento imediato para humano, suporte e encerramento. Contatos fora da lista de teste continuam com fluxos fixos. Ao completar nome, serviço e necessidade, uma única resposta confirma encaminhamento ao Jefferson e continuidade por atendente, sem promessa de prazo. 77 testes aprovados; API publicada, sem frontend ou migração. Contato pessoal de teste retomado sem apagar histórico, após backup copiado para diretório privado externo (crm-quote-6e3c7dc.dump). Nenhuma mensagem enviada pelo agente; teste da nova conversa depende do titular.
