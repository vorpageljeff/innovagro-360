# Design system

## Direção

Interface precisa, calma e densa, com superfícies neutras, tipografia Geist e acento esmeralda moderado. Cores têm significado; nenhum estado depende apenas delas.

## Primitivos

Tokens vivem em `apps/web/app/globals.css`. Componentes consomem variáveis sem hex codes locais. Radius é moderado, bordas são sutis e sombras aparecem somente em camadas elevadas.

## Acessibilidade

WCAG AA, foco visível, navegação por teclado, labels persistentes e alvos touch de pelo menos 40px. Em mobile, tabelas densas viram listas estruturadas.

## Componentes iniciais

`AppShell`, `Sidebar`, `Topbar`, `MetricStrip`, `AttentionFeed`, `StatusPill`, `EmptyState`, `Skeleton` e `CommandPalette`.

