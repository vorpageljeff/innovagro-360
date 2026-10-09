# Caixa de saída do Instagram

A página `/instagram` preserva o módulo do WhatsApp e lista apenas leads com perfil confirmado. O operador pode abrir o perfil correto, revisar a primeira abordagem e consultar o histórico de envios registrado no CRM.

O CRM não afirma integração direta com a caixa de mensagens do Instagram. A mensagem é enviada na sessão autenticada do Instagram e só depois confirmada no botão **Confirmar que enviei no Instagram**. Essa confirmação cria uma atividade idempotente, atualiza a data real do contato e agenda a próxima revisão em sete dias. Abrir o perfil ou editar o texto não registra contato.

A mensagem padrão apresenta a Voragon como parceira de presença digital, sites, sistemas e orientação em tecnologia, sem preço, link ou promessa de faturamento. A primeira abordagem deve ser revisada para o contexto da empresa. Contatos convertidos ou marcados sem interesse ficam bloqueados para novos registros.

API autenticada: `GET /api/v1/crm/instagram/leads`, `GET /api/v1/crm/instagram/leads/{id}/conversation` e `POST /api/v1/crm/instagram/leads/{id}/sent`. O histórico usa as atividades existentes do lead, sem tabela ou migração adicional.

## Publicação e primeira campanha — 09/10/2026

Backend `c89ba65`, release `/opt/innovagro/apps/crm360/releases/c89ba65`, imagem `voragon-crm-api:instagram-c89ba65`. Frontend corrigido em `1fcbff0`, deployment Vercel `dpl_8FHut3BDy2wucjzTBHpUg9sW9R5Y`, promovido para produção. Build Next.js aprovado; API saudável; navegador autenticado confirmou 18 perfis e 17 envios persistidos.

Dezessete DMs foram confirmadas visualmente no Instagram e registradas como contato no CRM. A PRONMED devolveu resposta automática, mas a mensagem de saída não permaneceu visível; o caso ficou como nota de resultado incerto e não foi repetido. Estética Thayane Leite e Rennove Estética continuam sem perfil confirmado e não receberam DM. Uma mensagem destinada à Dra. Poliana foi inserida por engano numa conversa pessoal do WhatsApp quando a aba ativa mudou; ela foi apagada para todos imediatamente, antes de retomar os envios numa aba do Instagram fixada por índice.

Primeiras DMs para contas sem conversa anterior podem aparecer em solicitações de mensagens. O CRM registra envio confirmado, não leitura. Silêncio não deve ser interpretado como desinteresse. Conferir o Direct antes de qualquer follow-up e realizar no máximo um após sete dias.
