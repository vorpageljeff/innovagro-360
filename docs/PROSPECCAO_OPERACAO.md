# Aplicação das regras de prospecção

Atualizado em 22/09/2026. A política integral de Jefferson está em [AGENTE_PROSPECCAO_VORAGON.md](AGENTE_PROSPECCAO_VORAGON.md). Esta orientação aplica a política às próximas pesquisas e abordagens; não altera históricos de envios.

## Procedimento

1. Conferir o escopo autorizado da campanha, histórico e duplicatas por organização/perfil. Recorte vigente confirmado por Jefferson: Nordeste e MATOPIBA, municípios com menos de 100 mil habitantes, todos os segmentos prioritários da política (não somente agro). Consultar fonte demográfica e registrar o ano de referência. Campanha atual autorizada: pesquisar 25 leads, abordar apenas os qualificados e registrar os contatos confirmados no CRM.
2. Investigar cada empresa e registrar fontes, data da consulta e observações. Informação desconhecida recebe “não identificado”. Site não encontrado não comprova que a empresa não possui site. Não pontuar ausência sem evidência suficiente.
3. Manter memória do cálculo: critério, pontos e evidência. Ticket médio e alto são alternativas. Não deduzir capacidade financeira, conversão ou processos internos somente de seguidores ou aparência. Critérios subjetivos precisam de justificativa observável; critérios de recência/frequência devem explicitar datas e amostra usadas.
4. Produzir o JSON de cada lead com todos os campos da seção 15 da política. Guardar fontes e cálculo em registro auxiliar associado ao perfil. O exemplo de clínica é fictício, não deve ser importado. `abordar` deve refletir a decisão real, nunca ser preenchido automaticamente com true.
5. Só abordar com score elegível, pelo menos dois sinais distintos e observáveis de oportunidade e contexto específico para personalização. Duas descrições do mesmo fato não são dois sinais. Empresas encerradas e perfis pessoais são excluídos independentemente da soma.
6. Preparar uma DM individual, idealmente 150–350 caracteres, sem links, portfólio, proposta ou lista de serviços. Interpretação operacional do princípio “a primeira mensagem NÃO deve vender”: reservar a arte publicitária para depois de resposta com abertura; ela deixa de anteceder automaticamente a primeira DM. Escolher uma única solução inicial.
7. Enviar somente dentro do lote autorizado. Conferir a conversa antes e após o envio; resultado incerto não autoriza repetir. Registrar contato realizado apenas com evidência de envio, preservando a data real e uma chave de evento idempotente.
8. No CRM registrar empresa, link do Instagram, data do contato e próxima revisão em sete dias. Jefferson verifica respostas no Instagram e registra o retorno manualmente. Ausência de retorno registrado não comprova ausência de resposta: conferir a conversa antes de qualquer follow-up.
9. Permitir no máximo um follow-up, após sete dias e conferência do histórico, se não houve resposta, recusa ou pedido para parar. Após esse follow-up, não enviar novas cobranças. Quando verificada a ausência de resposta, registrar encerramento sem presumir desinteresse explícito.

## Persistência e limites atuais

- CRM de produção: https://innovagro-360.vercel.app/crm. A API e o banco persistem na VPS Hostinger, conforme ACESSOS.md. O antigo relato de CRM somente em localStorage é histórico.
- Não importar candidatos ainda não contatados como se tivessem recebido mensagem. O importador de contatos não substitui um cadastro de análises prévias.
- Esta entrega documenta as regras; não instala motor de pontuação, novos campos de qualificação, contador automático de follow-up ou agendador de mensagens no CRM.
- Até haver suporte específico, preservar a análise JSON e evidências em arquivo comercial privado com cópia externa; quando houver contato confirmado, registrar a qualificação nas notas do contato, respeitando o limite da API. Não publicar dados de leads no Git.
- Registrar follow-up efetivamente enviado no histórico, com data e chave estável. Conferir o histórico para impedir um segundo follow-up. Encerramento sem resposta pode ser descrito em nota; não usar “sem interesse” para representar uma recusa que não ocorreu.
- Código e documentos operacionais: salvar, revisar, commit e push. Documentação não exige deploy de backend/frontend. Dados reais: servidor e backup externo recuperável, seguindo FLUXO_OPERACIONAL.md.
- Nenhuma mensagem nova é autorizada apenas pela atualização desta política. Os lotes anteriores mantêm seus registros originais.

## Novo lote solicitado — 09/10/2026

Pesquisa de mais vinte contatos solicitada pelo titular após ausência de respostas humanas no lote anterior. Vinte novos candidatos cadastrados sem contato realizado, sem data de follow-up e com nota de fonte pública e diagnóstico pendente. Vinte e cinco números pesquisados, vinte e quatro reconhecidos pelo Evolution; seleção final de vinte sem repetição no CRM. Municípios do CE/MA/BA no recorte, fonte demográfica IBGE Censo 2022 preservada nos arquivos privados. Nenhuma mensagem enviada. Site não identificado não foi convertido em ausência de site; score conservador 5 e prioridade baixa, sem autorização automática pela qualificação. Dados e fontes comerciais fora do Git em Voragon_Comercial/prospeccao-whatsapp-20-20261009; cópia na VPS. Backup anterior externo crm-before-prospects-20-20261009.dump, arquivo pg_restore legível; nova sessão confirmou persistência dos vinte registros. Sem mudança de código, schema ou deploy.

Posteriormente, Jefferson autorizou expressamente abordar esse lote pelo Instagram. Dezoito perfis foram confirmados; dezessete DMs individualizadas tiveram envio visível e foram registradas no CRM em 09/10/2026. PRONMED ficou com resultado incerto após resposta automática e não foi repetida. Thayane Leite e Rennove continuaram sem perfil seguro e não foram abordadas. Próxima revisão dos envios confirmados: 16/10/2026, sempre após conferir o Direct. Não presumir leitura ou ausência de resposta, pois a primeira DM pode estar em solicitações de mensagens.
