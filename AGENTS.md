# Instruções permanentes — 360 CRM

## Consulta obrigatória

Antes de modificar, importar dados ou publicar este projeto, leia `docs/FLUXO_OPERACIONAL.md` e `docs/ACESSOS.md`. As instruções atuais de Jefferson prevalecem sobre estes documentos. Mantenha os documentos atualizados com fatos verificados, sem segredos.

## Fluxo definido por Jefferson

1. Desenvolver e salvar o código localmente.
2. Revisar, validar, versionar e enviar as mudanças autorizadas ao Git remoto.
3. Publicar o backend na hospedagem existente, informada por Jefferson como HostGator.
4. Publicar o frontend na Vercel, conectado à API correta.
5. Verificar o fluxo completo e registrar a versão publicada.

Código local é área de trabalho. Dados reais do CRM devem persistir no banco do servidor; localStorage e arquivos desta máquina não são armazenamento definitivo. Git protege o código, não substitui backup do banco. Credenciais, dumps e dados de clientes/leads não devem ser enviados ao repositório.

## Execução e integridade

- Um “OK” ao escopo apresentado autoriza executar o procedimento correspondente sem pedir confirmação a cada etapa. Não ampliar o escopo nem presumir autorização para mensagens comerciais, despesas ou exclusão de dados.
- Preservar alterações existentes de outras tarefas. Versionar somente arquivos revisados e pertencentes ao escopo autorizado.
- Nunca declarar sucesso apenas porque salvou localmente: verificar push, destino e resultado dos deployments e persistência dos dados quando aplicáveis.
- Não substituir a hospedagem existente, criar banco paralelo ou usar valores de `.env.example` em produção por conveniência.
- Confirmar destino real antes de publicar: documentação histórica cita Hostinger, mas o usuário informou HostGator. A conexão real ainda precisa ser verificada.
- Antes de migração/importação que altere dados existentes, conferir backup externo recuperável. Não executar reset, apagar volumes ou sobrescrever banco para resolver deploy.
- Se uma etapa falhar, interromper suas dependentes, preservar o estado e informar o bloqueio específico. Continuar trabalhos independentes possíveis.
- Registrar pendências e resultados; não afirmar que uma automação planejada já está ativa.
