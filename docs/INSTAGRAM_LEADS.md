# Caixa de saída do Instagram

A página `/instagram` preserva o módulo do WhatsApp e lista apenas leads com perfil confirmado. O operador pode abrir o perfil correto, revisar a primeira abordagem e consultar o histórico de envios registrado no CRM.

As mensagens recebidas pela conta profissional chegam pelo webhook oficial da Meta e aparecem automaticamente na conversa do CRM. A tela atualiza a conversa aberta a cada cinco segundos e os contadores da lista a cada dez segundos. O envio continua manual na sessão autenticada do Instagram e só depois é confirmado no botão **Confirmar que enviei no Instagram**. Essa confirmação cria uma atividade idempotente, atualiza a data real do contato e agenda a próxima revisão em sete dias. Abrir o perfil ou editar o texto não registra contato.

A mensagem padrão apresenta a Voragon como parceira de presença digital, sites, sistemas e orientação em tecnologia, sem preço, link ou promessa de faturamento. A primeira abordagem deve ser revisada para o contexto da empresa. Contatos convertidos ou marcados sem interesse ficam bloqueados para novos registros.

API autenticada: `GET /api/v1/crm/instagram/leads`, `GET /api/v1/crm/instagram/leads/{id}/conversation` e `POST /api/v1/crm/instagram/leads/{id}/sent`. A entrada servidor a servidor usa `POST /api/v1/crm/instagram/webhook`, protegido por segredo dedicado. A migração `20261009_0007` adiciona mensagens recebidas com deduplicação pelo identificador da Meta. Uma resposta real muda o lead para `respondeu`, prioridade alta e remove o acompanhamento automático.

## Conversas em tempo real — 09/10/2026

Código `c448521`, branch `feat/instagram-realtime-20261009`. Backend em `/opt/innovagro/apps/crm360/releases/c448521`, imagem `voragon-crm-api:instagram-c448521`, schema `20261009_0007`. Frontend Vercel `dpl_9fPvHHL6ufXkYYREB2BAT2Nw3z4B`, promovido para `https://innovagro-360.vercel.app/instagram`. Receptor Meta publicado em `https://voragon-instagram.vercel.app/api/instagram-webhook`, deployment `dpl_H2h5R1NsPYdUAU8MTujqChyzvdzT`.

Meta confirmou a assinatura do aplicativo para o campo `messages`. Challenge público e POST com assinatura válida responderam 200. O histórico foi recuperado somente para os 23 perfis já existentes no CRM: quatro mensagens recebidas foram importadas, em três contatos (Clínica Dell Med, Love Laser e PRONMED), sem repetir abordagens. Os três ficaram com status `respondeu` e prioridade alta. Novos remetentes passam a ser cadastrados automaticamente quando enviarem uma mensagem.

Validação: 100 testes da API, build Next.js e cinco testes do receptor aprovados. Backup anterior à migração: `/opt/innovagro/backups/crm360/crm-20261009T185124Z.dump`, com cópia privada externa. A interface usa consulta periódica; não depende de WebSocket. A API da Meta informa recebimento, mas leitura da DM e pasta principal/solicitações continuam sob controle do Instagram.

## Publicação e primeira campanha — 09/10/2026

Backend `c89ba65`, release `/opt/innovagro/apps/crm360/releases/c89ba65`, imagem `voragon-crm-api:instagram-c89ba65`. Frontend corrigido em `1fcbff0`, deployment Vercel `dpl_8FHut3BDy2wucjzTBHpUg9sW9R5Y`, promovido para produção. Build Next.js aprovado; API saudável; navegador autenticado confirmou 18 perfis e 17 envios persistidos.

Dezessete DMs foram confirmadas visualmente no Instagram e registradas como contato no CRM. A PRONMED devolveu resposta automática, mas a mensagem de saída não permaneceu visível; o caso ficou como nota de resultado incerto e não foi repetido. Estética Thayane Leite e Rennove Estética continuam sem perfil confirmado e não receberam DM. Uma mensagem destinada à Dra. Poliana foi inserida por engano numa conversa pessoal do WhatsApp quando a aba ativa mudou; ela foi apagada para todos imediatamente, antes de retomar os envios numa aba do Instagram fixada por índice.

Primeiras DMs para contas sem conversa anterior podem aparecer em solicitações de mensagens. O CRM registra envio confirmado, não leitura. Silêncio não deve ser interpretado como desinteresse. Conferir o Direct antes de qualquer follow-up e realizar no máximo um após sete dias.
