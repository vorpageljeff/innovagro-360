# Diagnóstico e correção do envio — 09/10/2026

Instância empresarial conectada, mas ACK de teste pessoal retornou `error=463`. Cinco contatos anteriores têm DELIVERY_ACK; doze pedidos comerciais seguintes têm ERROR. A aceitação de sendText não confirma entrega. Jefferson informou que mensagens manuais pelo celular também não chegaram. Restrição da conta e falha de token são hipóteses distintas; não concluir resolução pela conexão `open`.

Backup anterior: crm/evolution/evolution-instances de 20261009T125336Z, arquivos validados e copiados para diretório privado externo à VPS. Não incluir dados comerciais ou sessão no Git. Preservar volumes e credenciais.

Atualização preparada em `deploy/Dockerfile.evolution`: base Evolution 2.3.7 fixada por digest e Baileys 7.0.0-rc14. Build e importação dos exports usados passaram. Aplicar `deploy/compose.evolution-protocol.yml` como último override, somente ao serviço evolution, com `--no-deps`. A atualização não remove restrições da conta e não instala retentativa automática de mensagens. Fonte da correção oficial: https://github.com/WhiskeySockets/Baileys/pull/2517 .

Rollback: recriar somente evolution com os compose anteriores, sem override de protocolo. Não apagar instâncias ou banco, nem desconectar a conta como tentativa de contornar a restrição. Histórico, dados e configuração de API/frontend permanecem preservados.

Validação de entrega após atualização ainda pendente. Testar somente no número pessoal expressamente autorizado; não reenviar mensagens comerciais.
