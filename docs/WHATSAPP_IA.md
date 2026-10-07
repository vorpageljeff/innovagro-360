# Atendimento com IA no WhatsApp

Integração OpenAI Responses no backend Python existente, via HTTPS/httpx. Sem dependência de SDK no frontend. A chave nunca chega ao navegador. O painel WhatsApp → Fluxos e bot consulta o estado e as configurações pendentes, sem exibir a chave nem o contexto interno.

## Configuração privada

Referência sem segredos: `deploy/whatsapp-ai.env.example`. Adicionar os campos ao `/opt/innovagro/apps/crm360/.env.production` (permissão 600). Chave obtida na própria conta OpenAI, com cobrança da API configurada pelo titular. Escolher um modelo disponível na conta que suporte Responses + Structured Outputs; não há modelo pré-selecionado nem chamadas pagas de descoberta. `WHATSAPP_AI_KNOWLEDGE` recebe fatos da empresa aprovados pelo usuário (até 8.000 caracteres); valores multiline devem ser devidamente cotados no arquivo env.

`WHATSAPP_AI_ENABLED` e `EVOLUTION_BOT_ENABLED` começam false. Preparar credencial e contexto não autoriza remover a pausa global solicitada. Preservar `EVOLUTION_BOT_ENABLED=false` até instrução explícita de Jefferson. Recriar somente API usando a release registrada em CURRENT_RELEASE e seu compose/runtime-image; não recriar ou desconectar Evolution. A flag de um contato não substitui a pausa global.

## Comportamento

- Pausas globais/individuais e contatos encerrados impedem geração e envio.
- Fluxos que encerram ou encaminham para humano prevalecem sobre IA. Se habilitada, a IA substitui respostas de outros fluxos e o menu genérico.
- Histórico restrito à mesma organização e contato: seis mensagens anteriores, com respostas anteriores apenas quando aceitas pelo Evolution. Texto e saída limitados; não é memória ilimitada.
- Geração retorna resposta, prioridade e encaminhamento validados. Sem ferramentas para pagamentos, agenda ou operações externas.
- O recibo é persistido antes de gerar; webhooks repetidos não geram nem enviam novamente. Timeout/API indisponível/saída inválida/limite encaminham o contato à fila humana sem mensagem automática de erro. Não há retry automático de cobrança ou envio.
- Limite conservador em janela móvel de 24h, até 100 mensagens por padrão, também contando fluxos fixos e geração em andamento. Não é limite monetário: custos dependem do modelo/token; definir também controles de consumo na conta provedora. Gerações abandonadas aparecem como atenção após dois minutos, para revisão humana.
- `store=false` no provedor; histórico do atendimento permanece no banco do CRM. Limite por resposta: 1.024 tokens de saída; entrada atual até 2.000 caracteres. A IA não substitui os fatos comerciais da empresa.

## Verificação

Testes de contrato HTTP usam provedor simulado; não fazem chamadas pagas. Verificam geração estruturada, falha/refusal/saída incompleta, histórico limitado, isolamento de organização, deduplicação, limite, pausa global e precedência do atendimento humano. Ainda é necessário configurar a conta e validar respostas reais antes de habilitar envios. A ausência de chave/contexto é exibida como configuração pendente.

Fontes oficiais: https://developers.openai.com/api/docs/guides/conversation-state e https://developers.openai.com/api/docs/guides/structured-outputs.
