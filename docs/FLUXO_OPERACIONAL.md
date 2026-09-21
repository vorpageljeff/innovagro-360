# Procedimento de execução e automação

Aprovado como diretriz por Jefferson em 21/09/2026.

## Como iniciar

Exemplo: “OK, execute o fluxo para integrar a pesquisa de leads ao CRM”. O OK cobre o escopo discutido e suas etapas necessárias. O agente consulta AGENTS.md e este procedimento, verifica o ambiente e executa o trabalho autorizado. Informações indispensáveis ausentes devem ser identificadas com precisão; não repetir pedidos de autorização já concedida.

## Sequência e critérios de conclusão

1. **Inspecionar:** ler instruções; conferir Git, mudanças existentes, branch, remoto, aplicação e destinos de produção. Confirmar domínio da API, servidor, diretório da aplicação, banco e mecanismo real de deploy. Não expor segredos.
2. **Implementar:** salvar alterações no projeto, conectar frontend à API autenticada e persistir dados no servidor. Arquivos locais de pesquisa são temporários até importação confirmada. Não apagar esses arquivos antes da confirmação.
3. **Validar:** executar checks proporcionais à mudança. Para leads, verificar isolamento por organização, campos, fontes e prevenção de duplicatas por perfil normalizado. Candidatos não verificados devem continuar identificados como pendentes.
4. **Proteger dados:** antes de mudanças no banco, confirmar backup externo, data e procedimento de restauração testado. Aplicar migrações compatíveis com a versão anterior quando possível. Nunca usar reset nem `docker compose down -v` como deploy.
5. **Versionar:** revisar diff, selecionar apenas arquivos do escopo, commit e push. Confirmar SHA no remoto. Não incluir `.env`, credenciais, backups ou dados comerciais no Git.
6. **Backend:** publicar o SHA autorizado na hospedagem existente pelo mecanismo confirmado. Executar migrações previstas e verificar health, autenticação, conexão ao banco e operação necessária. Se falhar, não promover frontend dependente.
7. **Frontend:** gerar preview na Vercel, conferir URL da API e validar a interface. Promover a versão validada para produção. Preservar o vínculo e a configuração do monorepo registrados em ACESSOS.md.
8. **Verificação completa:** criar/consultar registro autorizado pela API, recarregar a tela e verificar acesso em uma nova sessão autorizada. Confirmar que o dado vem do servidor. Não criar leads fictícios como se fossem clientes reais.
9. **Encerrar:** registrar SHA, resultados dos checks, deployments, domínio da API, contagem de importações e pendências. Não registrar segredos nem dados pessoais desnecessários.

Mudanças somente em documentação passam por revisão e Git; não exigem deploy manual do backend/frontend. Uma integração Git existente pode disparar build automaticamente, devendo isso ser observado.

## Recuperação

Guardar a versão anterior do backend e do frontend. Rollback de código só é seguro se compatível com o schema atual. Restauração de banco pode apagar gravações posteriores ao backup: avaliar impacto antes de executar. Falha no push ou deploy não autoriza sobrescrever trabalho remoto.

## Automação desejada

O agente pode executar as etapas após o OK durante a sessão. Para execução reproduzível em CI, preparar um workflow de acionamento manual (`workflow_dispatch`) com SHA/escopo explícitos, concorrência limitada a um deploy por ambiente, checks, backup/migrações, backend, frontend e verificação final. Usar segredos do ambiente de CI e registrar resultado de cada etapa. Reexecuções não devem duplicar leads nem reaplicar migrações já realizadas.

A automação não está instalada por este documento. Antes de criar o workflow, confirmar:

- Hospedagem real: HostGator informado pelo usuário versus Hostinger na documentação histórica.
- Acesso de deploy já existente, domínio da API, diretório remoto e tipo de hospedagem; não presumir VPS, Docker ou SSH disponíveis.
- Banco em uso, migrações e destino de backups com restauração testada.
- Integração Git da Vercel para evitar deploy duplicado e garantir ordem de publicação.
- Autenticação real do CRM e como importar os leads por API.

## Situação verificada em 21/09/2026

- Git remoto: https://github.com/vorpageljeff/innovagro-360.git; branch local main.
- Frontend: https://innovagro-360.vercel.app; projeto Vercel innovagro-360.
- Backend remoto e banco: ainda não verificados. Não concluir ausência com base somente na cópia local.
- A versão local inspecionada anteriormente tinha CRM em localStorage e autenticação de demonstração. Há alterações locais em andamento: reavaliar antes de implementar.
- Pesquisa de leads: Nordeste, cidades até 60 mil habitantes, Instagram ativo e ausência de site próprio após verificação. Usar como referência ../Voragon_Comercial; não publicar seus dados no Git.
