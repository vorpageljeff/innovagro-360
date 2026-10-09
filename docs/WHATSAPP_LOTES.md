# Envios selecionados — 09/10/2026

Interface `4a55746`: em /whatsapp, selecionar até cinco contatos elegíveis nas caixas ao lado das conversas, revisar o lote personalizado com {empresa} e disparar pelo número empresarial. Cada envio usa a API manual existente, autorização da organização, destino esperado e identificador próprio. A seleção não envia mensagens. Lotes são sequenciais, separados por 2,5 segundos, e interrompem em falha/resultado incerto; consultar mantém os identificadores e pula os envios já aceitos. Histórico individual persiste no banco; seleção e resumo do lote pertencem à sessão da página.

“Sent” na API atual significa aceitação pelo Evolution, não confirmação de entrega. A consulta de 09/10 confirmou DELIVERY_ACK para os cinco primeiros contatos da prospecção e ERROR para os cinco restantes; o CRM não reconcilia automaticamente esses estados posteriores do Evolution. Não reenviar automaticamente.

Validação: build e TypeScript, navegador no preview com requisições de envio interceptadas, limite de cinco, revisão sem disparo, personalização, interrupção no segundo envio simulado, reutilização do identificador e ausência de repetição do primeiro. Nenhuma mensagem real enviada nesses testes. Backend e esquema permanecem na versão existente.

Frontend publicado em `dpl_GLeSbSXt6kEWEqqgjCVbGjF9Bpah`, READY, alias https://innovagro-360.vercel.app associado ao commit `4a55746`. Preview validado `dpl_fXSjRR1hVbPKRpTkAwpLEgJvZZmW`.
Validação final no alias de produção: cinco contatos selecionados, sexto bloqueado, revisão personalizada e cinco chamadas simuladas únicas; nenhum envio real.
