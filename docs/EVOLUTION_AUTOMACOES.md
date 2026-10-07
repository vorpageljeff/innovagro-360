# Evolution e automações internas — 07/10/2026

O CRM inclui Kanban com prioridades baixa, média, alta e urgente, telefone WhatsApp por contato e fluxos persistidos na API. Nenhum dado depende de localStorage. O editor inicial é sequencial: mensagem recebida → condição de texto → alteração de prioridade/situação → resposta opcional. Não é um editor completo de grafos, não executa código arbitrário e não inclui IA, áudio, agendamento ou integrações HTTP genéricas.

Fluxos criados manualmente começam pausados. Os seis fluxos iniciais de atendimento comercial são configurados ativos na instalação completa. A primeira regra ativa que corresponder ao texto, por ordem de execução e, em caso de empate, por criação, é executada. Números novos recebidos por webhook criam contatos com telefone e nome informado pelo WhatsApp; Instagram fica vazio. O índice único por organização/telefone evita duplicatas. Contatos antigos continuam podendo receber vínculo de telefone manual. Grupos, mensagens do próprio bot e identificadores LID sem alternativa explícita de telefone são ignorados. Contatos convertidos e sem interesse não recebem respostas automáticas. Mensagens e respostas confirmadas aparecem no histórico do contato; a consulta retorna as 100 mais recentes.

## Configuração no servidor

Variáveis privadas da API: `EVOLUTION_API_URL`, `EVOLUTION_API_KEY`, `EVOLUTION_INSTANCE`, `EVOLUTION_ORGANIZATION_ID`, `EVOLUTION_WEBHOOK_SECRET`, `EVOLUTION_BOT_ENABLED`. Segredos ficam fora do Git. A integração atual atende uma instância e uma organização; as rotas autenticadas isolam as organizações. O QR é solicitado ao backend autenticado, sem expor a chave do Evolution no navegador.

Combine os arquivos `deploy/compose.hostinger-crm.yml` e `deploy/compose.evolution.yml`. O segundo instala Evolution v2.3.7, seu PostgreSQL e Redis em rede Docker sem novas portas públicas. O banco do Evolution armazena sessões/mensagens da integração; os contatos do CRM continuam no banco original. Crie `.env.evolution` privado com credenciais aleatórias e configuração compatível com o exemplo oficial. Inclua os volumes do Evolution na política de backup.

Configure o webhook por instância em `/webhook/set/{instance}` com `webhook.enabled=true`, URL da API `/api/v1/crm/evolution/webhook`, `webhookByEvents=false`, `webhookBase64=false`, evento `MESSAGES_UPSERT` e header privado `x-webhook-secret`. O receptor valida segredo e nome da instância. O ID da mensagem é único por organização. O registro é confirmado no banco antes de qualquer envio externo.

Falha ou timeout de envio gera estado `uncertain`; queda entre confirmação do registro e envio pode deixar `sending`. Nenhum desses casos dispara reenvio automático: conferir o WhatsApp antes de intervir. Isso evita respostas duplicadas, mas não garante entrega de toda resposta em caso de queda. `sent` significa aceitação pela API Evolution, não confirmação de leitura ou entrega no celular.

Fontes oficiais verificadas: [rotas de instância](https://github.com/evolution-foundation/evolution-api/blob/main/src/api/routes/instance.router.ts), [webhooks](https://github.com/evolution-foundation/docs-evolution/blob/main/v2/en/configuration/webhooks.mdx), [configuração](https://github.com/evolution-foundation/evolution-api/blob/main/.env.example), [release 2.3.7](https://github.com/evolution-foundation/evolution-api/releases/tag/2.3.7).

## Validação inicial

30 testes da API passaram, incluindo normalização do telefone, prioridade inválida, autenticação, regras pausadas, condição sem distinção de maiúsculas, isolamento do webhook, eventos duplicados e bloqueio de contatos sem interesse. TypeScript e build Next.js passaram. Falta validação de mensagens reais após vinculação do telefone pelo usuário.

Backup anterior à migração: `crm-20261007T115746Z.dump`, checksum SHA-256 `343d0864e320537e52fb7e2a52781e54abe34e845b33c8056480eef2db93a6cb`. Cópia fora da VPS em diretório privado local; restauração testada em banco temporário, com schema `20260921_0002`, 31 leads e 31 atividades. Banco de teste removido após a conferência. Upload externo periódico permanece pendente.


## Resultado publicado

API/interface `5a03d43`, deploy Vercel `dpl_GURJjmDDawjeA3BYJ4yqHcxubksy` promovido. Migração validada também em uma restauração temporária do banco real, preservando 31 leads e 31 atividades; aplicada em produção. Instância Evolution criada, webhook confirmado, QR exibido no navegador. Login, consultas e escrita autenticada de prioridade verificados em produção, com releitura após recarregar. Fluxo inicial de orçamento salvo pausado para revisão do usuário. Nenhum envio real foi realizado. O usuário deve conectar o WhatsApp e revisar/ativar o fluxo para concluir a validação de mensagens.


## Instalação completa do atendimento

Schema `20261007_0004`: Instagram opcional para contatos originados no WhatsApp, pausa do bot por contato, ordem de execução e encaminhamento humano por fluxo. Atendente, orçamento e suporte encaminham para humano e pausam futuras respostas do bot; é possível retomar no contato. A mensagem do encaminhamento ainda é enviada uma única vez. Pedido de não contatar marca sem interesse e não responde.

Seis templates editáveis: não contatar, atendente, orçamento, serviços, suporte e boas-vindas/menu. O menu usa 1 para orçamento, 2 para serviços e 3 para atendente. Condições aceitam alternativas separadas por `|`, desconsideram acentos/maiúsculas e respeitam limites de palavra; opções numéricas exigem igualdade. A simulação na tela usa as regras ativas e mostra resposta e ações sem gravar contatos nem enviar mensagens. O bot não é baseado em IA; trabalha com os fluxos de atendimento configurados.


Validação da instalação completa: 35 testes, build Next.js e teste de execução em PostgreSQL isolado passaram. Produção `29b3422` / Vercel `dpl_dGLKLc6Hw6k9zJc1ZdXJU8FGbBw6`, com seis fluxos ativos e 31 contatos preservados. QR, simulações, assumir/retomar atendimento e persistência após recarregar conferidos no navegador. Nenhum envio real foi usado como teste. Ainda é necessário escanear o QR em CRM → Automações → Conectar WhatsApp por QR.


## Pausa solicitada em 07/10/2026

Após confirmar o WhatsApp conectado, Jefferson solicitou suspender os envios da própria instância. `EVOLUTION_BOT_ENABLED=false` foi gravado na configuração privada persistente, e a API foi recriada e conferida com bot desabilitado. O WhatsApp permanece conectado para receber e registrar mensagens. Os fluxos existentes foram preservados; o bloqueio global impede suas respostas automáticas. Não reativar os envios sem nova instrução explícita do usuário. Novos deployments devem preservar esta configuração.
