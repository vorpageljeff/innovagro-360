# Aplicação das regras de prospecção

Atualizado em 22/09/2026. A política integral de Jefferson está em [AGENTE_PROSPECCAO_VORAGON.md](AGENTE_PROSPECCAO_VORAGON.md). Esta orientação aplica a política às próximas pesquisas e abordagens; não altera históricos de envios.

## Procedimento

1. Conferir o escopo autorizado da campanha, histórico e duplicatas por organização/perfil. O último recorte solicitado foi agro na Bahia, municípios com menos de 100 mil habitantes; consultar fonte demográfica e registrar o ano de referência. A lista geral de segmentos não inicia uma nova campanha.
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
