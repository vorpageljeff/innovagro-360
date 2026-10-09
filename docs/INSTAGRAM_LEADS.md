# Caixa de saída do Instagram

A página `/instagram` preserva o módulo do WhatsApp e lista apenas leads com perfil confirmado. O operador pode abrir o perfil correto, revisar a primeira abordagem e consultar o histórico de envios registrado no CRM.

O CRM não afirma integração direta com a caixa de mensagens do Instagram. A mensagem é enviada na sessão autenticada do Instagram e só depois confirmada no botão **Confirmar que enviei no Instagram**. Essa confirmação cria uma atividade idempotente, atualiza a data real do contato e agenda a próxima revisão em sete dias. Abrir o perfil ou editar o texto não registra contato.

A mensagem padrão apresenta a Voragon como parceira de presença digital, sites, sistemas e orientação em tecnologia, sem preço, link ou promessa de faturamento. A primeira abordagem deve ser revisada para o contexto da empresa. Contatos convertidos ou marcados sem interesse ficam bloqueados para novos registros.

API autenticada: `GET /api/v1/crm/instagram/leads`, `GET /api/v1/crm/instagram/leads/{id}/conversation` e `POST /api/v1/crm/instagram/leads/{id}/sent`. O histórico usa as atividades existentes do lead, sem tabela ou migração adicional.
