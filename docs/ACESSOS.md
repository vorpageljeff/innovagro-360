# Acessos — InnovAgro 360

Verificados em 21/09/2026.

- Dashboard: https://innovagro-360.vercel.app/dashboard
- CRM: https://innovagro-360.vercel.app/crm
- Login: https://innovagro-360.vercel.app/login
- Projeto na Vercel: https://vercel.com/vorpageljeffs-projects/innovagro-360
- Equipe: vorpageljeffs-projects
- Projeto: innovagro-360
- ID: prj_6sMieg2q9g2H1Vfb5z1oYnJhiAMn

## Desenvolvimento e publicação

A raiz deste repositório está vinculada ao projeto por `.vercel/project.json` (ignorado pelo Git). Execute a CLI a partir de `360_CRM_Gestao`. O frontend fica em `apps/web`; o `vercel.json` da raiz define Next.js, `npm run build:web` e saída `apps/web/.next`. A configuração remota informa raiz `.`; não alterar para `apps/web` sem ajustar os comandos de build.

A CLI disponível nesta máquina usa o Node em `/Users/jeffersonvorpagel/.local/share/techa-publish-tools/node-v22.23.2-darwin-arm64/bin`. Acrescente esse diretório ao PATH antes de usar `npx vercel`.

A vinculação gerou `.env.local`, ignorado pelo Git. Não compartilhar seu conteúdo nem copiar credenciais para documentação.

## Verificação e limites

Deploy de produção Ready; fluxo login → dashboard → CRM verificado. O login atual é de demonstração. A versão local do módulo CRM persiste em localStorage e a API não possui rotas de leads. A vinculação Vercel não conecta um banco de dados nem implementa importação de leads.

Critérios e candidatos da prospecção estão em `../Voragon_Comercial` (pasta irmã deste repositório). Antes de importar dados reais, implementar armazenamento central autenticado, isolamento por organização e prevenção de duplicatas. Nenhum lead foi importado nesta configuração de acesso.
