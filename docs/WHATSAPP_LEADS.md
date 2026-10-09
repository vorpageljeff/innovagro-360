# Leads e conversa do WhatsApp empresarial

Acessar `/whatsapp` → **Leads para contato** → **Abrir conversa**. Busca, filtros de prioridade/situação, paginação e edição de telefone continuam usando o banco do CRM e a organização autenticada.

A mensagem padrão fica salva no servidor. `{empresa}` insere o nome do lead. O modal carrega o rascunho persistido ou a mensagem preparada na nota de prospecção, permite editar e salvar, e envia individualmente pelo Evolution conectado ao número empresarial. Abrir a conversa e salvar rascunhos não enviam mensagens. Seleção organiza contatos; não dispara um lote.

O histórico consulta as últimas 100 mensagens do Evolution a cada 5 segundos enquanto a página está visível. Inclui mensagens do cliente e do empresarial, mesmo enviadas pelo celular. Áudio, imagem, vídeo e documento aparecem como indicação textual; reprodução/download de mídia não foi implementado. Se o Evolution estiver indisponível, exibe o histórico que o CRM possui e avisa que a fonte é o CRM.

**Assumir atendimento** pausa a IA nesse lead. Envio manual não retoma o bot nem consome as três respostas automáticas permitidas. A última mensagem manual confirmada entra no contexto da IA, permitindo entender respostas à oferta inicial. A configuração atual permite clientes reais, com limite automático de três respostas por contato e passagem ao humano por qualificação/pedido explícito.

Contatos com telefone podem ter seu histórico aberto, incluindo os bloqueados para envio. Sem interesse, convertidos, excluídos na configuração privada ou sem telefone não podem receber mensagem por esse botão. Disponibilidade técnica não significa consentimento, qualificação comercial ou conta WhatsApp validada. A análise de prospecção permanece em `AGENTE_PROSPECCAO_VORAGON.md` e `PROSPECCAO_OPERACAO.md`.

Cada envio tem um UUID e uma reserva persistida antes da chamada externa. Repetir o mesmo UUID consulta o resultado sem chamar novamente o Evolution. O telefone deve corresponder ao destinatário revisado. Em resultado incerto, conferir a conversa; o sistema não repete automaticamente. Após confirmação, **Preparar nova mensagem** cria um novo envio explícito. Contato realizado só é registrado após confirmação do Evolution, que não garante leitura ou entrega ao destinatário.

API autenticada sob `/api/v1/crm/evolution`: `GET/POST /message-template`, `GET/POST /leads/{id}/draft`, `POST /leads/{id}/send` (text, request_id, expected_phone), `GET /leads/{id}/conversation`. Dados e credenciais do Evolution ficam no servidor; cookies de acesso são HttpOnly, e escrita exige origem válida.

Atualização 09/10/2026: backend `29694dd`, frontend `ae927df`, migração aditiva `20261009_0005`. Backup externo anterior à migração disponível na configuração privada. Validação: 87 testes API, compilação Next.js, banco restaurado isolado com os 10 leads preservados, persistência de rascunhos, registro de contato, duplicidade e resultado incerto. Evolution substituído por fixture nos testes de envio; nenhuma mensagem comercial enviada durante a validação.

Verificação no navegador: leitura real das conversas pelo Evolution, rascunho salvo e relido no servidor, botão de envio com requisição interceptada (sem disparo), modal em tela de 390 px e ausência de erros JavaScript.

## Caixa de entrada e alertas — 09/10/2026

A tela WhatsApp agora abre na aba Leads para contato. Conversas ficam à esquerda e o chat com composer à direita. Em celular, selecionar o contato abre o chat; Voltar à lista retorna aos contatos. Campos de envio, rascunhos, mensagem padrão, edição de telefone e assumir atendimento continuam disponíveis.

O contador é de mensagens de texto recebidas pelo webhook e registradas no CRM, independentemente de a IA responder. Leituras persistem por usuário/organização no banco. O cliente envia apenas IDs dos recibos que correspondem às mensagens exibidas no histórico, após abrir a conversa com a página visível. Não usa a leitura do aplicativo WhatsApp como leitura do operador CRM. Reabrir/recarregar preserva leituras; mensagens chegadas posteriormente e mensagens de outras conversas continuam não lidas. Marcar leitura não pausa o bot e não envia mensagem ao cliente.

Menu WhatsApp, sino e título da aba mostram o total global. Lista mostra contador por contato, prévia da resposta e destaque de seleção; contatos não lidos têm preferência dentro da página atual. Filtros e paginação continuam disponíveis. A lista e os contadores são consultados a cada 10 segundos, e o histórico aberto a cada 5 segundos. Alertas funcionam enquanto o CRM está aberto; não há push do sistema operacional com o navegador fechado. Mídias aparecem no histórico Evolution como indicação textual, mas não entram no contador baseado em recibos de texto do CRM.

API: GET /api/v1/crm/evolution/inbox retorna totais e contadores por lead; POST /leads/{id}/read aceita até 100 receipt_ids validados contra lead/organização autenticados. Nenhum user_id pode ser informado pelo cliente. Repetir a leitura é idempotente. GET /conversation inclui lead_id e read_ids dos recibos visíveis.

Backend 1bab60c e migração aditiva 20261009_0006. Backup crm-before-inbox-20261009.dump copiado para armazenamento privado fora da VPS. Teste PostgreSQL em restauração isolada confirmou persistência, isolamento de leitura por usuário, leitura somente de mensagens exibidas, mensagem posterior não lida e repetição idempotente. Dez leads e dez envios anteriores preservados. 90 testes API aprovados; nenhuma mensagem WhatsApp enviada durante esta atualização.
