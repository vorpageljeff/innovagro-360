# Controle de prospecção e retornos

## Comportamento

Cada loja tem nome, perfil normalizado/link do Instagram, cidade, situação, último contato e próximo acompanhamento. O histórico mantém data civil do evento e observações. Não são inventados horários quando o relatório só confirma o dia.

Registrar um contato inicial sugere acompanhamento em sete dias corridos. Exemplo: 21/09/2026 → 28/09/2026. Registrar um retorno cancela o lembrete automático; o usuário pode definir outra data. Sem interesse e convertido ficam sem lembrete. Nenhuma mensagem é enviada pelo CRM e nenhuma resposta é inferida automaticamente.

A interface permite busca, filtros, registro de novo contato, anotação de retorno e importação JSON. A lista carrega páginas de 100; os filtros operam sobre os contatos carregados e há botão para carregar mais.

## Armazenamento e autenticação

A API FastAPI usa o banco PostgreSQL existente e a organização da sessão autenticada. As tabelas novas são `crm_leads` e `crm_lead_activities`. Não utiliza localStorage como fallback. Os registros antigos do navegador não são apagados nem migrados automaticamente: conferir/exportar o legado antes de substituir a versão em produção.

O frontend faz proxy em `/api/crm/*`. Configure `CRM_API_URL` no servidor da Vercel com a base real, terminada em `/api/v1`. Credenciais da organização são validadas em `/auth/login`; o access token fica em cookie HTTP-only separado, válido por até 15 minutos, sem exportação para o JavaScript. A sessão demonstrativa existente não concede acesso ao banco: o CRM exige autenticação real. Após expiração é necessário reconectar. Não incluir token de acesso nas variáveis públicas.

## Endpoints

- GET/POST `/api/v1/crm/leads`
- GET/POST `/api/v1/crm/leads/{id}/activities`
- POST `/api/v1/crm/import`

Importação: `{ "leads": [{ "name": "Loja exemplo", "instagram": "@loja_exemplo", "city": "Cidade/UF", "contacted_on": "2026-09-21", "event_key": "relatorio-unico-loja-exemplo", "note": "Contato realizado; retorno não conferido." }] }`.

`event_key` é obrigatório e estável por envio, não por tentativa de importação. Reimportar o mesmo evento não cria novo histórico. O perfil é único dentro de cada organização. Importar registro histórico não deve apagar respostas já anotadas. Erro de importação impede commit do lote.

## Histórico: pendências antes da instalação

O domínio, acesso e banco do backend existente ainda precisam ser verificados. Não aplicar a migração nem importar leads antes de conferir o ambiente e backup externo. A existência da hospedagem foi informada pelo usuário; sua ausência não foi presumida.

1. Confirmar backend, organização, usuários e banco de produção.
2. Conferir backup recuperável e registros legados do navegador.
3. Publicar código do backend e executar `alembic upgrade head` no ambiente correto.
4. Testar autenticação, migração, isolamento e persistência com PostgreSQL real.
5. Configurar `CRM_API_URL`, validar preview e só então promover o frontend.
6. Importar `Voragon_Comercial/teste-10/importacao-crm.json` através da sessão autenticada, conferir dez perfis e as datas e repetir a consulta em outra sessão.

O arquivo de importação contém dados comerciais e permanece fora do repositório. Não é registro de importação concluída. A importação e o deploy em produção ainda não foram executados.

## Validação da implementação

Em 21/09/2026: build Next.js e TypeScript passaram; 16 testes de regras, validação e proteção das rotas passaram em Python 3.11 (o projeto declara Python >=3.12). A tela foi conferida no navegador em desktop e largura de 390px, sem erros JavaScript e sem armazenamento local de contatos. O estado sem API impede gravações e informa a ausência de conexão.

A migração não foi executada contra PostgreSQL real. Autenticação, gravação e importação completas no ambiente remoto permanecem pendentes. O código será mantido em branch separada até a conexão com o backend ser validada.

## Prévia publicada em 21/09/2026

Código: `255354fc147d8ac17619f133879a05ff499030dc`, disponível no Git remoto em `feat/crm-acompanhamento`.

Prévia Vercel Ready: https://innovagro-360-1okwr2cpr-vorpageljeffs-projects.vercel.app/crm (protegida pelo acesso da equipe Vercel). Build remoto passou. `/login` respondeu HTTP 200; `/api/crm/leads` respondeu HTTP 503 com aviso de backend não conectado, como esperado sem `CRM_API_URL`.

Produção não foi promovida: backend remoto, banco e acesso de deploy continuam sem identificação confirmada. Vercel production não possui variáveis de ambiente configuradas. Nenhum contato foi importado. Não declarar esta prévia como CRM operacional.

## Instalação realizada

Backend instalado na Hostinger e importação dos dez contatos confirmada. Consulte `ACESSOS.md` para endpoints, armazenamento, backup e versão. Os bloqueios descritos anteriormente são históricos.
