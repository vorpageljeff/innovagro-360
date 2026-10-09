# Diagnóstico e correção do envio — 09/10/2026

Instância empresarial conectada, mas ACK de teste pessoal retornou `error=463`. Cinco contatos anteriores têm DELIVERY_ACK; doze pedidos comerciais seguintes têm ERROR. A aceitação de sendText não confirma entrega. Jefferson informou que mensagens manuais pelo celular também não chegaram. Restrição da conta e falha de token são hipóteses distintas; não concluir resolução pela conexão `open`.

Backup anterior: crm/evolution/evolution-instances de 20261009T125336Z, arquivos validados e copiados para diretório privado externo à VPS. Não incluir dados comerciais ou sessão no Git. Preservar volumes e credenciais.

Atualização preparada em `deploy/Dockerfile.evolution`: base Evolution 2.3.7 fixada por digest e Baileys 7.0.0-rc14. Build e importação dos exports usados passaram. Aplicar `deploy/compose.evolution-protocol.yml` como último override, somente ao serviço evolution, com `--no-deps`. A atualização não remove restrições da conta e não instala retentativa automática de mensagens. Fonte da correção oficial: https://github.com/WhiskeySockets/Baileys/pull/2517 .

Rollback: recriar somente evolution com os compose anteriores, sem override de protocolo. Não apagar instâncias ou banco, nem desconectar a conta como tentativa de contornar a restrição. Histórico, dados e configuração de API/frontend permanecem preservados.

Atualização aplicada a partir de `65e1d7c`, enviada ao remoto. Imagem ativa `voragon-evolution:2.3.7-baileys-rc14`, build digest `sha256:9831037e8f05640403b26d77ab045cb9987d9bc45bdb411f82fa1defc7ad0163`. Compose ativo da integração continua no diretório histórico `releases/5a03d43/deploy`, com o novo override como último arquivo. API permanece f2a62f6 e frontend 4a55746; nenhum novo deploy destas aplicações foi necessário.

Teste pessoal autorizado código edc63c: mensagem 3EB0DA50F77B2E21D011A7 apresentou ERROR inicial seguido de DELIVERY_ACK. Segunda leitura confirmou a entrega e conexão open, sem novo envio. Isso confirma entrega deste teste; não comprova liberação de todos os destinatários nem corrige os registros comerciais anteriores. Nenhuma mensagem comercial foi reenviada.

Limitação existente do CRM: estados sent/recorded não reconciliam os ACK posteriores de falha. A interface de lote explicita aceitação pela API, mas a conversa ainda não apresenta o ERROR do provedor. Correção desse acompanhamento permanece pendente, sem declarar entrega dos pedidos antigos. Preservar o override de protocolo nos próximos deployments da integração.

Após solicitação para reenviar todos, a conferência identificou doze envios comerciais com ERROR e cinco com DELIVERY_ACK. Os cinco entregues foram excluídos do reenvio. O primeiro reenvio controlado, para BMTX Engenharia e Construções, recebeu novamente `463: account restricted or missing tctoken for contact`; foi registrado como sem confirmação e o processo parou. Os outros onze não foram disparados. O contraste com o teste pessoal entregue indica que a sessão funciona, mas novas conversas comerciais continuam recusadas. Não contornar a restrição nem reiniciar o lote enquanto o WhatsApp não liberar novas conversas.
