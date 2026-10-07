# Lista de leads para contato no WhatsApp

Acessar `/whatsapp` → **Leads para contato**. A lista lê contatos existentes do banco do CRM; não importa candidatos de pesquisa nem presume contato realizado. Busca por nome, cidade, Instagram e telefone, filtros de prioridade/situação e disponibilidade, ordenação por prioridade e paginação de 25 registros.

Pode cadastrar/editar telefone no contato existente pela API de settings, mantendo o histórico e a prevenção de duplicatas por organização/telefone. País e DDD são obrigatórios. O cadastro de telefone não confirma que a conta existe no WhatsApp nem representa qualificação comercial.

Seleção permite organizar contatos e preparar uma mensagem individual por destinatário. O link oficial `wa.me` abre a conversa com o texto preenchido; quem opera confirma o envio no próprio WhatsApp. Não há disparo pelo Evolution, envio em lote ou registro automático de contato realizado. Seleção e rascunhos são temporários na tela; contatos/telefones permanecem no banco. Não tratar abertura de conversa como evidência de entrega.

Contatos sem telefone, sem interesse, convertidos ou com número na exclusão privada não podem ser selecionados para mensagem. Para prospecção, a disponibilidade técnica do telefone não substitui a análise e personalização descritas em `AGENTE_PROSPECCAO_VORAGON.md` e `PROSPECCAO_OPERACAO.md`.

`EVOLUTION_EXCLUDED_PHONES` é uma lista privada de números em formato internacional, separados por vírgula, na `.env.production` do servidor. As variantes do número pessoal indicado por Jefferson foram excluídas; não registrar esses números no Git. A mesma exclusão é respeitada pelo webhook de respostas automáticas. A pausa global `EVOLUTION_BOT_ENABLED=false` foi preservada, assim como `WHATSAPP_AI_ENABLED=false`. Abrir conversas manualmente não altera essas flags.

API autenticada: `GET /api/v1/crm/evolution/leads`, parâmetros `q`, `audience=all|ready|missing_phone`, `priority`, `status`, `offset`, `limit` (1–100). Todas as contagens e páginas usam a organização autenticada. `can_message` significa telefone disponível e ausência dos bloqueios acima; não significa consentimento, qualificação, conta WhatsApp validada ou campanha autorizada.

Referência oficial para abertura de conversa: https://faq.whatsapp.com/5913398998672934/?locale=pt_BR.
