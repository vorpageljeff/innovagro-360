# INNOVAGRO 360 — Especificação Mestre de Produto, UX, Regras de Negócio e Arquitetura

**Versão:** 1.0  
**Data:** 10/09/2026  
**Status:** Documento mestre para execução pelo Codex  
**Produto:** Plataforma de Gestão Integrada de Serviços, Projetos, CRM e Financeiro  
**Uso inicial:** InnovAgro  
**Visão de produto:** multiempresa / SaaS para empresas de serviços, software, marketing, consultoria e educação.

---

# 0. INSTRUÇÃO PRINCIPAL PARA O CODEX

Este documento é a **fonte principal de verdade do projeto**.

O objetivo não é criar um conjunto de telas genéricas de ERP, CRM ou Kanban. O objetivo é construir um **sistema operacional gerencial da empresa**, com experiência visual premium, fluida, rápida e coerente, conectando todo o ciclo:

**Pré-lead → Lead → Oportunidade → Proposta → Contrato → Projeto → Entregas → Atividades → Horas → Custos → Faturamento → Recebimento → Resultado → Pós-venda → Nova oportunidade**

O sistema deve permitir que a direção enxergue a organização de forma holística e, ao mesmo tempo, faça drill-down até a origem de cada indicador.

## Regras de execução

1. Não criar UI de template administrativo genérico.
2. Não criar dashboard composto apenas por dezenas de cards idênticos.
3. Não usar ícones decorativos sem função.
4. Não usar gradientes excessivos, sombras pesadas, glassmorphism gratuito ou cores saturadas como decoração.
5. Não copiar visualmente nenhum produto do benchmarking; usar os princípios identificados.
6. Priorizar velocidade, legibilidade, hierarquia visual e densidade informacional controlada.
7. Todo indicador clicável deve permitir aprofundamento.
8. Todo módulo deve compartilhar o mesmo modelo conceitual de dados.
9. Não duplicar informações entre CRM, projetos e financeiro.
10. Toda ação relevante deve ser auditável.
11. A implementação deve ser responsiva.
12. A aplicação deve possuir autenticação e controle de acesso desde o MVP.
13. A arquitetura deve nascer multiempresa, mesmo que a primeira organização seja a InnovAgro.
14. As funcionalidades devem ser implementadas por fases, conforme roadmap deste documento.
15. Antes de alterar uma regra de negócio definida aqui, registrar a decisão em `docs/DECISIONS.md`.

---

# 1. VISÃO DO PRODUTO

## 1.1 Problema

Pequenas e médias empresas de serviços normalmente espalham sua operação entre:

- planilhas;
- WhatsApp;
- e-mail;
- ferramentas de tarefas;
- documentos;
- sistemas financeiros;
- CRMs;
- agendas;
- relatórios manuais.

Isso gera perda de contexto e impede que a gestão responda rapidamente perguntas simples:

- Quanto temos de receita contratada?
- Quanto devemos receber?
- O que provavelmente vai fechar no comercial?
- Quais clientes estão parados?
- Qual vendedor está performando?
- Qual projeto está consumindo mais horas que deveria?
- Qual cliente ou projeto realmente dá lucro?
- Quem está sobrecarregado?
- O que está atrasado?
- Quais riscos podem atingir o caixa?
- O que precisa da atenção da direção hoje?

A InnovAgro 360 deve responder essas perguntas usando os próprios dados operacionais.

## 1.2 Proposta de valor

> **Da primeira prospecção ao resultado financeiro, em uma única plataforma.**

A plataforma deve conectar quatro níveis de gestão:

1. **Empresa** — saúde global.
2. **Portfólio** — distribuição de recursos e resultados.
3. **Projeto/Cliente** — execução, prazo, escopo e margem.
4. **Pessoa/Atividade** — trabalho que precisa ser feito agora.

## 1.3 Princípio central

> **Nenhuma informação gerencial importante deve existir isolada.**

Exemplos:

- Uma proposta aceita pode gerar contrato e projeto.
- Um projeto utiliza horas.
- Horas têm custo.
- Custos reduzem margem.
- Faturas vêm de contratos/projetos.
- Recebimentos alimentam caixa.
- Resultados alimentam indicadores executivos.
- Cliente concluído retorna ao CRM como pós-venda/expansão.

---

# 2. BENCHMARKING DE PRODUTO E UX

O benchmarking foi realizado em setembro de 2026 com foco em produtos de referência em CRM, projetos e finanças.

Não deve haver clonagem visual. O objetivo é extrair padrões de produto e interação.

---

## 2.1 Linear — referência de foco, consistência e velocidade

**Referência:** https://linear.app/  
**UI refresh 2026:** https://linear.app/changelog/2026-03-12-ui-refresh

Pontos observados:

- interface visualmente calma;
- navegação e controles consistentes entre diferentes contextos;
- sidebar propositalmente discreta para destacar a área principal;
- iconografia pequena e coerente;
- alta densidade informacional sem sensação de poluição;
- atalhos e command menu como parte central da experiência;
- detalhes abertos sem obrigar o usuário a abandonar seu contexto;
- velocidade percebida extremamente alta.

### Aplicação na InnovAgro 360

Adotar:

- sidebar escura/neutra e pouco dominante;
- cabeçalhos previsíveis;
- command palette;
- quick create;
- detalhes em painel lateral quando possível;
- transições discretas;
- tipografia forte;
- linhas e bordas sutis;
- redução de elementos decorativos.

Evitar:

- um card para cada informação;
- botões grandes para ações secundárias;
- barras coloridas por toda parte;
- ícones gigantes.

---

## 2.2 Attio — referência de CRM moderno orientado a dados

**Referência:** https://attio.com/  
**Lists:** https://attio.com/help/reference/managing-your-data/lists/create-lists

Pontos observados:

- registros de empresas e contatos funcionam como objetos ricos;
- uma mesma informação pode ser visualizada por tabela ou Kanban;
- propriedades configuráveis permitem adaptação a diferentes processos;
- CRM tem aparência de workspace, não de software legado;
- contexto da conta é priorizado;
- registros concentram relacionamentos e atividades.

### Aplicação

O CRM da InnovAgro deve parecer um **workspace comercial vivo**, não uma ficha cadastral.

A página de um cliente deve reunir:

- dados;
- contatos;
- negócios;
- histórico;
- reuniões;
- propostas;
- contratos;
- projetos;
- financeiro;
- arquivos;
- próximas ações.

A mesma coleção deve suportar:

- tabela;
- pipeline;
- filtros salvos;
- agrupamentos.

---

## 2.3 monday CRM — referência de funil, metas e forecast

**Referências:**  
https://monday.com/crm/use-cases/sales-pipeline  
https://monday.com/crm/product-features

Pontos observados:

- estágios claros;
- owners e próximas ações integrados ao funil;
- automações entre estágios;
- forecast com valor e probabilidade;
- metas individuais e de equipe;
- activity tracking;
- visualização de funil e conversão.

### Aplicação

O CRM deve obrigatoriamente possuir:

- estágio;
- responsável;
- próxima ação;
- prazo da próxima ação;
- valor;
- probabilidade;
- data provável de fechamento;
- aging;
- metas;
- forecast;
- histórico de atividades;
- motivo de ganho/perda.

---

## 2.4 Ramp — referência de gestão financeira orientada a exceções

**Referências:**  
https://support.ramp.com/ramps-spend-management-platform-enhancing-your-companys-expense-control/  
https://support.ramp.com/real-time-reporting/  
https://ramp.com/new-on-ramp-q2-2026

Pontos observados:

- financeiro não é somente histórico; há controles antes do gasto;
- aprovações e políticas ficam incorporadas ao fluxo;
- dashboards permitem ir do agregado à transação;
- anomalias e exceções recebem destaque;
- relatórios são reutilizáveis;
- foco em responder “o que precisa da minha atenção?”.

### Aplicação

O dashboard financeiro não deve mostrar apenas números.

Deve separar:

**Situação**
- saldo;
- receitas;
- despesas;
- contas futuras.

**Exceções**
- vencidos;
- despesas sem categoria;
- custos acima do esperado;
- caixa projetado crítico;
- projeto com margem caindo.

---

## 2.5 ClickUp — referência de drill-down e múltiplas perspectivas operacionais

**Referência:** https://help.clickup.com/hc/en-us/articles/6312197753239-Intro-to-Dashboards

Pontos observados:

- dashboards usam dados reais do trabalho;
- tempo registrado e desempenho do projeto aparecem juntos;
- filtros e drill-down são centrais;
- diferentes visualizações servem diferentes níveis da empresa.

### Aplicação

Todo indicador operacional relevante deverá ter drill-down.

Exemplo:

`Projetos críticos: 3`
→ lista dos três projetos
→ seleciona projeto
→ mostra dimensões que causam criticidade
→ seleciona dimensão
→ mostra eventos/atividades responsáveis.

---

## 2.6 Notion — referência de flexibilidade de visualização

**Referências:**  
https://www.notion.com/product/projects  
https://www.notion.com/help/timelines

Pontos observados:

- uma mesma base pode ser representada em diferentes perspectivas;
- timeline permite visão temporal ampla;
- dados e contexto documental coexistem;
- organização flexível reduz silos.

### Aplicação

Projetos e CRM devem permitir:

- tabela;
- Kanban;
- timeline quando aplicável;
- visão resumida;
- visualizações salvas.

Não tentar reproduzir o conceito de páginas livres do Notion no MVP.

---

## 2.7 Stripe Dashboard — referência de clareza operacional

**Referência:** https://support.stripe.com/topics/dashboard?locale=pt-BR

Ponto relevante:

A home prioriza informação operacional rápida e deixa funções administrativas e detalhadas em níveis inferiores.

### Aplicação

A home da InnovAgro deve responder em poucos segundos:

1. Como estamos?
2. O que mudou?
3. O que requer ação?
4. O que vence em breve?
5. Onde clicar para entender a causa?

---

# 3. DIREÇÃO DE DESIGN

## 3.1 Personalidade visual

Palavras-chave:

**preciso, moderno, confiável, leve, tecnológico, executivo, inteligente, premium.**

Não deve parecer:

- ERP tradicional;
- painel Bootstrap;
- template ThemeForest;
- sistema acadêmico;
- clone de Monday;
- clone de ClickUp;
- aplicativo excessivamente colorido.

## 3.2 Estética

Base:

- fundos neutros;
- superfícies brancas/acinzentadas no light mode;
- dark mode profundo e neutro;
- acento de marca inspirado em tecnologia/agro, sem transformar a tela em “verde agrícola”;
- bordas de 1px discretas;
- pouco uso de sombras;
- radius moderado;
- tipografia nítida;
- áreas vazias usadas para hierarquia, não para desperdiçar espaço.

## 3.3 Tipografia

Preferência:

- `Geist` ou `Inter` para interface;
- números financeiros em fonte com tabular numbers;
- evitar fontes decorativas.

Escala sugerida:

- título de página: 24–28px;
- título de seção: 16–18px;
- conteúdo principal: 14px;
- metadado: 12–13px;
- KPI principal: 26–34px.

## 3.4 Cores semânticas

As cores devem comunicar significado.

- verde: saudável / recebido / ganho;
- amarelo: atenção;
- vermelho: crítico / vencido / perdido;
- azul: informação / andamento;
- roxo ou acento secundário: automação/IA;
- cinza: inativo / neutro.

Nunca depender somente da cor. Usar rótulo, ícone discreto ou texto.

## 3.5 Iconografia

Usar biblioteca consistente, como Lucide.

Regras:

- 16–18px na maior parte da interface;
- ícone precisa significar algo;
- não colocar ícone em todos os títulos;
- evitar ilustrações genéricas em dashboards;
- ícones de módulos podem existir na sidebar.

## 3.6 Densidade

Oferecer visualização:

- confortável;
- compacta.

Tabela comercial e financeira deve suportar alta densidade sem perder legibilidade.

---

# 4. PADRÃO DE NAVEGAÇÃO

## 4.1 Sidebar principal

Desktop:

```text
[InnovAgro 360]

Início

COMERCIAL
CRM
Agenda
Propostas
Metas

OPERAÇÃO
Clientes
Projetos
Atividades
Equipe

FINANCEIRO
Visão financeira
Receber
Pagar
Fluxo de caixa
DRE

GESTÃO
Indicadores
Relatórios
Riscos

IA
Copiloto

ADMINISTRAÇÃO
Configurações
```

A sidebar deve poder recolher para modo icon-only.

## 4.2 Barra superior

Elementos:

- breadcrumb;
- busca global;
- botão `+ Criar`;
- notificações;
- avatar/perfil.

Não repetir o nome da página desnecessariamente.

## 4.3 Command palette

Atalho:

`⌘ K` / `Ctrl K`

Ações:

- buscar cliente;
- abrir projeto;
- abrir oportunidade;
- criar atividade;
- registrar contato;
- criar proposta;
- lançar despesa;
- iniciar timer;
- navegar para módulo.

## 4.4 Quick Create

Botão `+ Criar`:

- Pré-lead
- Lead
- Oportunidade
- Atividade
- Projeto
- Proposta
- Despesa
- Receita
- Cliente

O formulário deve abrir em drawer/modal sem trocar de página quando possível.

---

# 5. HOME — COCKPIT EXECUTIVO

Não criar uma grade de vinte cards.

A composição deve ser editorial e hierárquica.

## 5.1 Primeira faixa — estado da empresa

Exemplo:

```text
Receita do mês     Resultado      Caixa disponível      Forecast comercial
R$ 42.800          R$ 18.900      R$ 31.200             R$ 94.500
+12,4%             44,1% margem   61 dias runway        94% da meta
```

KPIs em linha, com divisores sutis.

## 5.2 Seção principal — Atenção da gestão

Lista priorizada por impacto:

```text
CRÍTICO  Projeto Santé consumiu 78% das horas e entregou 54%.
ALERTA   R$ 5.800 vencidos há mais de 7 dias.
ALERTA   Oportunidade ACME de R$ 32 mil sem interação há 6 dias.
RISCO    Equipe de desenvolvimento projetada em 118% de capacidade.
```

Cada item deve abrir sua causa.

## 5.3 Comercial

Visual:

- meta x realizado;
- pipeline ponderado;
- negócios por estágio;
- negócios que precisam de follow-up.

## 5.4 Projetos

Lista compacta:

```text
Projeto        Saúde   Progresso   Prazo       Horas   Margem
Santé          68      54%         -8 dias     78%     31%
DR Performance 91      72%         no prazo    63%     48%
```

## 5.5 Financeiro

Mostrar:

- contas vencidas;
- próximos 7 dias;
- próximos 30 dias;
- menor saldo projetado;
- data de maior pressão de caixa.

## 5.6 Equipe

Mostrar apenas exceções inicialmente:

- sobrecarga;
- ausência de apontamento;
- horas excessivas;
- tarefas vencidas.

---

# 6. CRM — MODELO COMPLETO

## 6.1 Entidades comerciais

- organização/tenant;
- empresa/conta;
- contato;
- pré-lead;
- lead;
- oportunidade;
- interação;
- tarefa comercial;
- reunião;
- proposta;
- versão de proposta;
- produto/serviço;
- meta;
- campanha/origem;
- motivo de perda;
- contrato.

---

# 7. PRÉ-LEADS

## RN-CRM-001

Pré-lead representa uma empresa ou pessoa ainda não qualificada para entrada formal no funil.

Campos:

- id;
- organization_id;
- empresa;
- contato;
- telefone;
- WhatsApp;
- e-mail;
- cidade;
- estado;
- país;
- segmento;
- site;
- origem;
- campanha;
- responsável;
- interesse potencial;
- observação;
- data de entrada;
- próximo contato;
- status;
- created_by;
- created_at;
- updated_at.

Status:

- Novo;
- A pesquisar;
- Contato planejado;
- Tentativa de contato;
- Contato realizado;
- Convertido;
- Descartado.

## RN-CRM-002

Pré-lead convertido não deve ser apagado.

Registrar:

- data da conversão;
- usuário;
- lead gerado.

## RN-CRM-003

Deve existir deduplicação por:

- CNPJ;
- e-mail;
- telefone;
- domínio;
- combinação aproximada nome + cidade.

Não bloquear automaticamente casos incertos. Sinalizar possível duplicidade.

---

# 8. LEADS E QUALIFICAÇÃO

## RN-CRM-010

Um lead deve possuir:

- responsável;
- status;
- fonte;
- data de entrada;
- última interação;
- próxima ação;
- prazo da próxima ação.

## RN-CRM-011

Nenhum lead ativo pode permanecer sem próxima ação.

Se usuário tentar salvar como ativo sem próxima ação:

- impedir;
- informar motivo;
- solicitar ação + data.

## RN-CRM-012

Lead qualificado precisa conter:

- problema ou necessidade;
- potencial de solução;
- contato válido;
- nível de interesse;
- estimativa inicial de oportunidade.

---

# 9. FUNIL COMERCIAL

Pipeline padrão:

```text
Pré-lead
→ Lead
→ Qualificação
→ Oportunidade
→ Diagnóstico
→ Proposta
→ Negociação
→ Ganho
→ Perdido
```

Administradores poderão configurar pipelines no futuro.

## Critérios de estágio

### Lead
Contato identificável.

### Qualificação
Dor/necessidade e aderência mínima identificadas.

### Oportunidade
Possibilidade real de negócio.

Obrigatório:

- serviço;
- valor estimado;
- probabilidade;
- data prevista de fechamento;
- owner.

### Diagnóstico
Levantamento ou reunião de descoberta em andamento/concluída.

### Proposta
Deve existir proposta registrada.

### Negociação
Cliente respondeu ou existe tratativa ativa sobre condições.

### Ganho
Obrigatório:

- valor final;
- serviço;
- forma de pagamento;
- data provável de início;
- contato decisor.

### Perdido
Obrigatório:

- motivo;
- comentário;
- concorrente se conhecido.

---

# 10. OPORTUNIDADE

Campos:

```text
id
organization_id
account_id
primary_contact_id
owner_id
pipeline_id
stage_id
title
service_id
estimated_value
probability
weighted_value
expected_close_date
source
campaign
priority
temperature
last_activity_at
next_action_type
next_action_at
next_action_owner_id
lost_reason_id
won_at
lost_at
created_at
updated_at
```

## RN-CRM-020

`weighted_value = estimated_value * probability / 100`

## RN-CRM-021

Probabilidade pode ser:

- padrão por estágio;
- sobrescrita manualmente por usuário autorizado.

Histórico da mudança deve ser mantido.

## RN-CRM-022

O sistema deve medir:

- dias desde criação;
- dias no estágio atual;
- dias sem interação;
- ciclo total;
- tempo médio por estágio.

---

# 11. AGING E SLA COMERCIAL

Configuração padrão inicial:

- novo lead sem primeiro contato > 2 dias: atenção;
- > 5 dias: crítico;
- oportunidade sem interação > 5 dias: atenção;
- proposta sem follow-up > 4 dias: atenção;
- próxima ação vencida: crítico operacional.

Os limites devem ser configuráveis.

---

# 12. INTERAÇÕES COM CLIENTE

Tipos:

- ligação;
- WhatsApp;
- e-mail;
- reunião presencial;
- reunião online;
- mensagem;
- visita;
- observação;
- outro.

Campos:

```text
date_time
owner
account
contact
opportunity
channel
direction
result
summary
sentiment (optional)
next_action
next_action_at
attachments
```

## RN-CRM-030

Toda interação deve ficar na timeline do cliente.

## RN-CRM-031

Editar uma interação já registrada deve gerar auditoria.

## RN-CRM-032

Interações podem gerar automaticamente a próxima atividade.

---

# 13. PÁGINA DA CONTA / CLIENTE — UX PRINCIPAL DO CRM

Layout inspirado em CRM moderno orientado a contexto.

## Cabeçalho

```text
Empresa ACME                       [Ativa]  [•••]
Tecnologia • Toledo/PR
Responsável: Caio
```

Linha de indicadores:

- pipeline aberto;
- receita histórica;
- projetos ativos;
- saldo a receber.

Tabs:

```text
Visão geral
Timeline
Contatos
Negócios
Propostas
Contratos
Projetos
Financeiro
Arquivos
```

Lateral contextual:

- próximo compromisso;
- responsável;
- relacionamento;
- tags;
- informações-chave.

---

# 14. PROPOSTAS

Identificação:

`PROP-AAAA-NNNN`

Exemplo:

`PROP-2026-0042`

Campos:

- cliente;
- oportunidade;
- versão;
- comercial;
- responsável técnico;
- escopo;
- itens;
- descontos;
- impostos estimados;
- valor total;
- forma de pagamento;
- validade;
- prazo estimado;
- observações;
- termos.

Status:

- Rascunho;
- Em aprovação;
- Aprovada internamente;
- Enviada;
- Visualizada;
- Em negociação;
- Aceita;
- Recusada;
- Expirada;
- Cancelada.

## RN-CRM-040

Proposta não pode ser considerada `Enviada` sem:

- versão imutável;
- valor;
- validade;
- destinatário.

## RN-CRM-041

Alteração após envio gera nova versão.

Nunca sobrescrever a versão enviada.

## RN-CRM-042

Proposta aceita permite:

- criar contrato;
- converter oportunidade em ganha;
- criar projeto após aprovação contratual.

---

# 15. CICLO DE VENDAS E MÉTRICAS

Calcular:

- tempo pré-lead → lead;
- lead → oportunidade;
- oportunidade → proposta;
- proposta → ganho/perda;
- ciclo comercial total;
- ticket médio;
- conversão geral;
- conversão por estágio;
- conversão por vendedor;
- conversão por origem;
- conversão por serviço;
- forecast;
- aging.

---

# 16. METAS COMERCIAIS

Metas podem existir por:

- pessoa;
- time;
- unidade;
- empresa.

Tipos:

- receita;
- número de vendas;
- leads;
- leads qualificados;
- reuniões;
- propostas;
- conversão;
- ticket médio;
- follow-ups no prazo.

Períodos:

- semanal;
- mensal;
- trimestral;
- anual.

---

# 17. GAMIFICAÇÃO

Gamificação deve incentivar **comportamentos úteis**.

Não criar mecânica manipulativa.

Pontuação inicial sugerida:

```text
Lead qualificado                    +5 XP
Reunião realizada                  +10 XP
Proposta enviada                   +15 XP
Venda fechada                     +100 XP
Follow-up feito dentro do prazo     +5 XP
Registro completo de perda          +2 XP
```

Não pontuar:

- edição de campo;
- criação e exclusão;
- ações repetitivas sem valor;
- interações duplicadas.

## Ranking

Score mensal sugerido:

```text
40% receita fechada
20% conversão
15% follow-ups no prazo
10% leads qualificados
10% reuniões qualificadas
 5% qualidade dos registros
```

## Conquistas

- Primeira venda;
- 10 follow-ups consecutivos no prazo;
- Meta batida;
- 110% da meta;
- R$100 mil vendidos;
- Venda em até 7 dias;
- Cliente recorrente;
- 10 clientes conquistados.

Gamificação pode ser desativada pela organização.

---

# 18. CLIENTES

Cliente é entidade única.

Não criar um cliente diferente no CRM e outro nos projetos.

Dados:

- razão social;
- nome fantasia;
- CNPJ/identificação;
- contatos;
- endereços;
- segmento;
- origem;
- status;
- owner;
- contratos;
- projetos;
- oportunidades;
- faturamento;
- recebimentos.

---

# 19. CONTRATOS

Identificação:

`CONT-AAAA-NNNN`

Tipos:

- preço fechado;
- por hora;
- mensalidade;
- recorrente;
- pacote;
- comissão;
- participação;
- híbrido.

Campos:

- cliente;
- proposta de origem;
- vigência;
- valor;
- modelo;
- recorrência;
- reajuste;
- horas contratadas;
- responsável;
- faturamento;
- datas importantes;
- anexos.

---

# 20. CONVERSÃO COMERCIAL → PROJETO

Ao fechar oportunidade:

```text
Pré-lead
→ Lead
→ Oportunidade
→ Proposta
→ Contrato
→ Projeto
```

O projeto herda, quando aplicável:

- cliente;
- contatos;
- comercial;
- proposta;
- escopo;
- valor;
- prazo;
- modalidade;
- forma de cobrança;
- anexos relevantes.

Nunca exigir redigitação desnecessária.

---

# 21. PROJETOS

Entidades:

- projeto;
- fase;
- sprint;
- milestone;
- entrega;
- atividade;
- subatividade;
- dependência;
- checklist;
- comentário;
- arquivo;
- apontamento;
- risco;
- impedimento;
- mudança;
- decisão;
- baseline.

## Código

`PROJ-AAAA-NNNN`

---

# 22. ESTRUTURA DO PROJETO

Tabs:

```text
Visão geral
Planejamento
Board
Timeline
Entregas
Atividades
Horas
Equipe
Custos
Financeiro
Riscos
Mudanças
Decisões
Documentos
Histórico
```

Não carregar todas as tabs de uma vez.

---

# 23. ATIVIDADES

Hierarquia:

```text
Projeto
  → Fase
    → Sprint
      → Entrega
        → Atividade
          → Subatividade
```

Nem todo projeto precisa usar Sprint.

Campos:

- título;
- descrição;
- owner;
- participantes;
- prazo;
- início;
- prioridade;
- estimativa;
- horas realizadas;
- status;
- entrega;
- dependências;
- critérios de aceite;
- evidências.

Status padrão:

```text
Backlog
Planejado
Em execução
Bloqueado
Em validação
Concluído
Cancelado
```

## RN-PROJ-001

Atividade `Concluída` deve ter critério de aceite satisfeito quando este estiver configurado.

## RN-PROJ-002

Bloqueio deve exigir motivo.

## RN-PROJ-003

Dependência impedida deve ser sinalizada.

---

# 24. BASELINE E REPLANEJAMENTO

Planejado original nunca deve ser sobrescrito.

Manter:

- baseline v1;
- baseline v2;
- motivo da revisão;
- aprovador;
- data;
- impacto.

Comparações:

```text
Original
Atual
Realizado
Forecast
```

---

# 25. SAÚDE DO PROJETO

Score 0–100.

Pesos iniciais:

```text
Prazo       30%
Financeiro  30%
Entregas    20%
Riscos      20%
```

Faixas:

```text
85–100 Saudável
70–84  Atenção
0–69   Crítico
```

`Paralisado` é status independente.

Os pesos devem ser configuráveis futuramente.

---

# 26. INDICADORES DE PROJETO

- progresso;
- atraso;
- planned vs actual;
- horas estimadas;
- horas realizadas;
- horas forecast;
- custo previsto;
- custo realizado;
- receita;
- margem;
- burn rate;
- SPI;
- CPI quando dados permitirem;
- tarefas vencidas;
- entregas vencidas;
- risco.

---

# 27. CAPACIDADE DA EQUIPE

Pessoa:

```text
capacidade semanal
- indisponibilidade
- férias
- feriados
= capacidade líquida
```

Planejamento:

```text
horas alocadas / capacidade líquida
```

Estados:

- < 70%: subalocado;
- 70–100%: adequado;
- 101–115%: atenção;
- >115%: sobrecarga.

Faixas configuráveis.

---

# 28. TIMESHEET

Apontamento:

- usuário;
- projeto;
- atividade;
- data;
- duração;
- tipo;
- descrição;
- billable;
- origem manual/timer.

## Regras

- atividade precisa pertencer a projeto salvo exceções autorizadas;
- apontamento nunca pode possuir duração negativa;
- edições após fechamento mensal devem exigir permissão;
- hora aprovada deve ser auditada em alteração.

---

# 29. RISCOS

Campos:

- título;
- descrição;
- probabilidade 1–5;
- impacto 1–5;
- score;
- categoria;
- owner;
- resposta;
- prazo;
- status.

`score = probabilidade * impacto`

---

# 30. IMPEDIMENTOS

Diferenciar risco de impedimento.

Risco = pode acontecer.  
Impedimento = já impacta a execução.

Campos:

- início;
- impacto;
- owner;
- dependência;
- prazo de resolução;
- data resolvida.

---

# 31. GESTÃO DE MUDANÇAS

Código:

`CR-AAAA-NNNN`

Fluxo:

```text
Solicitada
→ Em análise
→ Aguardando aprovação
→ Aprovada
→ Rejeitada
→ Implementada
```

Campos:

- solicitante;
- descrição;
- justificativa;
- impacto em horas;
- impacto financeiro;
- impacto de prazo;
- impacto de escopo;
- aprovador.

Mudança aprovada pode gerar:

- nova baseline;
- atividades;
- aditivo;
- ajuste financeiro.

---

# 32. DECISION LOG

Código:

`DEC-AAAA-NNNN`

Campos:

- decisão;
- contexto;
- alternativas;
- responsável;
- participantes;
- data;
- impactos;
- relação com projeto.

---

# 33. FINANCEIRO

Módulos:

- receitas;
- despesas;
- contas a receber;
- contas a pagar;
- pagamentos;
- recebimentos;
- centros de custo;
- categorias;
- fluxo de caixa;
- DRE;
- orçamento;
- rentabilidade de projeto.

---

# 34. REGRA FINANCEIRA CENTRAL

Toda movimentação deve possuir origem ou classificação.

Possíveis origens:

- contrato;
- projeto;
- cliente;
- centro de custo;
- fornecedor;
- despesa administrativa;
- investimento;
- ajuste.

Não permitir lançamentos “soltos” sem categoria.

---

# 35. CONTAS A RECEBER

Campos:

- cliente;
- contrato;
- projeto;
- documento;
- parcela;
- emissão;
- vencimento;
- valor;
- recebido;
- saldo;
- status;
- forma de pagamento.

Status:

- prevista;
- faturada;
- aberta;
- parcialmente recebida;
- recebida;
- vencida;
- cancelada.

---

# 36. CONTAS A PAGAR

Campos:

- fornecedor;
- categoria;
- projeto;
- centro de custo;
- competência;
- vencimento;
- valor;
- pago;
- status;
- recorrência;
- anexos.

---

# 37. FLUXO DE CAIXA

Horizontes:

- hoje;
- 7 dias;
- 15 dias;
- 30 dias;
- 60 dias;
- 90 dias.

Mostrar:

- saldo atual;
- entradas;
- saídas;
- saldo projetado;
- menor saldo;
- data de maior pressão.

---

# 38. DRE GERENCIAL

Estrutura inicial:

```text
Receita Bruta
(-) Impostos e deduções
= Receita Líquida

(-) Custos Diretos
= Margem de Contribuição

(-) Despesas Comerciais
(-) Despesas Administrativas
(-) Infraestrutura
(-) Outras despesas
= Resultado Operacional
```

Filtros:

- período;
- organização;
- unidade;
- cliente;
- projeto;
- serviço.

---

# 39. P&L POR PROJETO

Cada projeto deve responder:

```text
Receita contratada
Receita faturada
Receita recebida
Custos diretos
Horas × custo-hora
Outros custos
Margem
Margem %
```

---

# 40. PREVISTO × REALIZADO × FORECAST

Princípio obrigatório.

Sempre que fizer sentido, apresentar:

```text
Planejado
Realizado
Forecast
Desvio
```

Aplicável a:

- receita;
- custo;
- horas;
- prazo;
- margem;
- caixa.

---

# 41. PÓS-VENDA E EXPANSÃO

Projeto concluído não encerra relacionamento.

Criar eventos:

- satisfação;
- revisão de resultado;
- renovação;
- upsell;
- cross-sell;
- reativação.

Cliente pode voltar automaticamente para agenda CRM.

---

# 42. USUÁRIOS E LOGIN

Perfis iniciais:

- Administrador;
- Diretor/Gestor;
- Comercial;
- Gerente de Projetos;
- Colaborador;
- Financeiro.

Um usuário pode possuir múltiplos papéis.

---

# 43. RBAC

Permissões granulares:

```text
crm.view
crm.create
crm.edit
crm.delete

proposal.view
proposal.create
proposal.approve

project.view
project.create
project.edit
project.manage

time.view
time.create
time.approve

finance.view
finance.create
finance.edit
finance.approve

dre.view

reports.view

users.view
users.create
users.edit

settings.admin
```

Backend sempre valida permissão.

Nunca confiar somente em bloqueio de frontend.

---

# 44. MULTIEMPRESA

Todas as tabelas de negócio devem ter:

```text
organization_id
```

Exceções apenas para tabelas realmente globais.

Regra:

> uma organização nunca pode consultar registros de outra.

Adicionar testes automatizados de isolamento.

---

# 45. AUDITORIA

Tabela `audit_logs`.

Registrar:

- organização;
- usuário;
- ação;
- entidade;
- entity_id;
- valores antes;
- valores depois;
- timestamp;
- IP quando aplicável;
- user agent quando aplicável.

Eventos obrigatórios:

- alteração de estágio;
- valor de oportunidade;
- proposta;
- contrato;
- financeiro;
- baseline;
- usuário/permissões;
- exclusões lógicas.

---

# 46. NOTIFICAÇÕES

Tipos:

- próxima ação comercial;
- atividade vencendo;
- atividade vencida;
- proposta expirando;
- conta vencida;
- risco crítico;
- sobrecarga;
- mudança aguardando aprovação;
- meta próxima;
- projeto crítico.

Canais MVP:

- in-app;
- e-mail.

Futuro:

- WhatsApp;
- push;
- Slack/Teams.

---

# 47. IA — COPILOTO GERENCIAL

IA deve responder usando dados da organização.

Perguntas:

- Como está a empresa?
- Quais projetos precisam da minha atenção?
- Por que a margem caiu?
- Quais oportunidades podem fechar este mês?
- O que o Caio precisa fazer hoje?
- Quais clientes estão sem contato?
- Qual projeto está consumindo mais horas?
- Quanto teremos em caixa em 30 dias?

Nunca permitir que IA ignore permissões.

O usuário só pode receber via IA dados aos quais já teria acesso manual.

---

# 48. DAILY EXECUTIVO

Gerar briefing:

```text
Bom dia.

ATENÇÃO
• 2 projetos críticos.
• R$ 5.800 vencidos.
• 3 oportunidades sem follow-up.
• Capacidade de desenvolvimento em 112%.

COMERCIAL
Meta: R$ 80 mil
Fechado: R$ 52 mil
Forecast ponderado: R$ 74 mil

FINANCEIRO
Recebimentos próximos 7 dias: R$ 18.400
Pagamentos próximos 7 dias: R$ 11.900

PRIORIDADES
1. Aprovar CR-0012.
2. Cobrar Cliente X.
3. Revisar proposta PROP-2026-0042.
```

---

# 49. DASHBOARD PESSOAL — COMERCIAL

Ao entrar:

```text
Bom dia, Caio

Hoje
8 follow-ups
2 reuniões
1 proposta para enviar
3 oportunidades paradas

Meta
R$ 28.000 / R$ 40.000

Pipeline
R$ 87.000

Próximas ações
09:00 Empresa A
11:00 Empresa B
14:00 Empresa C
```

A home muda conforme perfil.

---

# 50. DASHBOARD PESSOAL — COLABORADOR

Mostrar:

- minhas atividades;
- prioridades;
- prazos;
- bloqueios;
- agenda;
- timer;
- horas da semana.

Não mostrar KPIs executivos irrelevantes.

---

# 51. UX DO PIPELINE

Kanban comercial deve possuir cards enxutos.

Card:

```text
ACME
Portal Comercial
R$ 32.000
Caio
Fechamento 24 set

Próxima ação
Hoje • 14:00

6 dias no estágio
```

Cor apenas como pequeno marcador de temperatura/SLA.

Não pintar cada coluna com uma cor forte.

Drawer de oportunidade abre ao clicar no card.

---

# 52. UX DE TABELAS

Recursos:

- colunas ajustáveis;
- pin;
- ordenação;
- filtros;
- filtros salvos;
- agrupamento;
- busca;
- seleção múltipla;
- ações em lote;
- exportação;
- densidade.

Evitar paginação com recarregamento completo.

---

# 53. DRAWERS CONTEXTUAIS

Usar drawer para:

- oportunidade;
- tarefa;
- contato;
- conta;
- risco;
- mudança.

Benefício:

o usuário mantém o contexto da lista/pipeline.

Drawer deve ter URL navegável quando possível.

---

# 54. FORMULÁRIOS

Regras:

- labels sempre visíveis;
- validação inline;
- agrupamento semântico;
- defaults inteligentes;
- autocomplete;
- seleção pesquisável;
- datas claras;
- ações principais à direita;
- salvar não deve destruir contexto.

Formulários longos devem ser divididos em seções.

---

# 55. ESTADOS VAZIOS

Não usar ilustração genérica.

Exemplo:

```text
Nenhuma oportunidade neste estágio.

Mova uma oportunidade para cá ou crie uma nova.
[+ Nova oportunidade]
```

---

# 56. LOADING E PERFORMANCE PERCEBIDA

Usar:

- skeletons;
- optimistic UI quando seguro;
- cache;
- prefetch;
- atualização parcial;
- debounce em busca.

Evitar spinners de página inteira.

---

# 57. RESPONSIVIDADE

## Desktop >= 1280
Layout completo.

## Tablet 768–1279
Sidebar recolhível.
Tabelas adaptáveis.
Painéis de detalhe ocupam mais largura.

## Mobile < 768
Bottom/compact navigation quando adequado.
Kanban com scroll horizontal local.
Ações principais acessíveis.
Tabelas mudam para lista estruturada quando necessário.

Não tentar mostrar o dashboard desktop comprimido.

---

# 58. ACESSIBILIDADE

Mínimo WCAG AA.

- contraste;
- navegação por teclado;
- foco visível;
- labels;
- aria;
- tooltips não obrigatórios;
- estados não dependentes de cor;
- targets >= 40–44px em touch.

---

# 59. FRONTEND

Destino:

**Vercel**

Stack:

```text
Next.js
TypeScript
React
Tailwind CSS
shadcn/ui como base estrutural, não como identidade visual final
TanStack Query
TanStack Table
React Hook Form
Zod
Recharts
Lucide
date-fns
```

Pode usar Radix primitives diretamente quando necessário.

## Regra visual

shadcn é infraestrutura de componentes.

**Não entregar aparência padrão do shadcn.**

Criar tokens e componentes próprios.

---

# 60. ESTRUTURA FRONTEND

```text
apps/web/
  app/
    (auth)/
      login/
      forgot-password/

    (workspace)/
      dashboard/
      crm/
        pre-leads/
        leads/
        opportunities/
        proposals/
        goals/
      clients/
      projects/
      tasks/
      team/
      finance/
        overview/
        receivables/
        payables/
        cash-flow/
        dre/
      reports/
      ai/
      admin/

  components/
    ui/
    data-table/
    charts/
    crm/
    projects/
    finance/
    layout/

  features/
  hooks/
  lib/
  services/
  types/
```

---

# 61. DESIGN TOKENS

Criar tokens CSS.

Exemplo conceitual:

```css
--background
--surface
--surface-raised
--border
--border-strong

--text-primary
--text-secondary
--text-muted

--accent
--accent-hover
--accent-soft

--success
--warning
--danger
--info

--radius-sm
--radius-md
--radius-lg

--shadow-popover
```

Nunca espalhar hex codes diretamente pelos componentes.

---

# 62. BACKEND

Destino:

**Hostinger VPS**

Stack:

```text
Python
FastAPI
SQLAlchemy 2
Alembic
Pydantic
PostgreSQL
Redis
Celery ou Dramatiq
Docker
Nginx ou Caddy
```

Preferir FastAPI assíncrono onde fizer sentido.

---

# 63. INFRAESTRUTURA

```text
Internet
   │
   ├── app.innovagro... → Vercel / Next.js
   │
   └── api.innovagro... → Hostinger VPS
                             │
                         Reverse Proxy
                             │
                         FastAPI
                         ├── PostgreSQL
                         ├── Redis
                         └── Worker
```

HTTPS obrigatório.

---

# 64. DOCKER COMPOSE

Serviços:

```text
api
worker
postgres
redis
reverse-proxy
```

PostgreSQL e Redis não devem ser expostos publicamente.

---

# 65. AUTENTICAÇÃO

Fluxo:

```text
login
→ access token curto
→ refresh token rotacionado
→ sessão
```

Requisitos:

- hash Argon2id ou equivalente seguro;
- recuperação de senha;
- revogação;
- logout de sessões;
- bloqueio de usuário;
- log de autenticação;
- rate limiting;
- proteção a brute force.

Futuro:

- MFA;
- SSO.

---

# 66. API

Prefixo:

`/api/v1`

Estrutura:

```text
/auth
/users
/organizations
/roles

/accounts
/contacts

/pre-leads
/leads
/opportunities
/interactions
/proposals
/contracts
/goals

/projects
/deliverables
/tasks
/time-entries
/risks
/issues
/change-requests
/decisions

/finance
/receivables
/payables
/cash-flow
/dre

/reports
/notifications
/ai
```

---

# 67. PADRÃO DE ENDPOINT

Exemplo:

```text
GET    /api/v1/opportunities
POST   /api/v1/opportunities
GET    /api/v1/opportunities/{id}
PATCH  /api/v1/opportunities/{id}
DELETE /api/v1/opportunities/{id}

POST   /api/v1/opportunities/{id}/interactions
POST   /api/v1/opportunities/{id}/move-stage
POST   /api/v1/opportunities/{id}/mark-won
POST   /api/v1/opportunities/{id}/mark-lost
```

Ações de domínio relevantes devem usar endpoints explícitos quando isso aumentar a integridade.

---

# 68. BANCO — TABELAS PRINCIPAIS

```text
organizations
organization_settings

users
user_organizations
roles
permissions
role_permissions

accounts
contacts
account_contacts

pre_leads
leads
pipelines
pipeline_stages
opportunities
opportunity_stage_history
interactions
commercial_tasks
goals
gamification_events
badges
user_badges

services
proposals
proposal_versions
proposal_items
contracts
contract_items

projects
project_members
project_phases
project_baselines
sprints
milestones
deliverables
tasks
task_dependencies
task_checklists
time_entries
capacity_plans
risks
issues
change_requests
decisions

cost_centers
finance_categories
accounts_receivable
receivables_payments
accounts_payable
payables_payments
expenses
revenues
budgets

documents
attachments
comments
notifications
audit_logs
```

---

# 69. SOFT DELETE

Entidades importantes não devem ser fisicamente apagadas no uso normal.

Campos:

```text
deleted_at
deleted_by
```

Financeiro e auditoria podem ter regras ainda mais restritivas.

---

# 70. EVENTOS DE DOMÍNIO

Criar mecanismo simples de eventos.

Exemplos:

```text
OpportunityWon
ProposalAccepted
ContractActivated
ProjectCreated
TaskCompleted
RiskBecameCritical
InvoiceOverdue
PaymentReceived
ProjectHealthChanged
GoalAchieved
```

Os eventos podem alimentar:

- notificação;
- auditoria;
- automação;
- gamificação;
- analytics.

---

# 71. OBSERVABILIDADE

Desde o início:

- logs estruturados;
- request id;
- error tracking;
- health endpoint;
- métricas básicas;
- log de worker.

Endpoints:

```text
/health
/ready
```

---

# 72. BACKUP

PostgreSQL:

- backup diário;
- retenção;
- backup externo ao VPS;
- teste periódico de restauração.

Documentos:

- backup separado.

Nunca considerar snapshot do VPS como único backup.

---

# 73. SEGURANÇA

Obrigatório:

- HTTPS;
- CORS restrito;
- CSRF se cookies forem usados;
- headers seguros;
- rate limiting;
- validação backend;
- RBAC;
- isolamento multiempresa;
- secrets fora do repositório;
- `.env.example` sem segredo;
- auditoria;
- queries parametrizadas;
- upload validado;
- limitação de tamanho;
- proteção a path traversal.

---

# 74. LGPD

Preparar:

- base para consentimentos quando necessário;
- exportação de dados;
- anonimização/exclusão conforme política;
- trilha de acesso;
- minimização;
- retenção configurável.

---

# 75. PERFORMANCE

Metas iniciais:

- navegação SPA percebida < 300ms quando dados estiverem em cache;
- primeira renderização útil rápida;
- API padrão p95 < 500ms em operações normais;
- filtros comuns indexados;
- paginação server-side;
- evitar N+1;
- índices por organization_id + filtros frequentes.

---

# 76. BUSCA GLOBAL

Pesquisar:

- clientes;
- contatos;
- oportunidades;
- propostas;
- projetos;
- tarefas.

Resultado agrupado.

Atalho: `⌘K`.

---

# 77. RELATÓRIOS

Comercial:

- funil;
- conversão;
- forecast;
- aging;
- metas;
- origem;
- perdas;
- ciclo de venda.

Projetos:

- saúde;
- horas;
- atrasos;
- capacidade;
- margem;
- risco.

Financeiro:

- DRE;
- caixa;
- recebíveis;
- inadimplência;
- custos;
- margem.

---

# 78. FILTROS GLOBAIS

Dashboard executivo:

- período;
- empresa/unidade;
- cliente;
- serviço;
- responsável.

Manter filtros na URL quando possível.

---

# 79. CONFIGURAÇÕES

- organização;
- identidade visual;
- usuários;
- permissões;
- pipeline;
- SLAs;
- categorias financeiras;
- centros de custo;
- serviços;
- tipos de projeto;
- gamificação;
- notificações.

---

# 80. ROADMAP

## Fase 0 — Fundação

- monorepo;
- ambientes;
- autenticação;
- organização;
- usuários;
- RBAC;
- design system;
- layout;
- auditoria;
- CI/CD.

## Fase 1 — CRM operacional

- contas;
- contatos;
- pré-leads;
- leads;
- oportunidades;
- pipeline;
- interações;
- próxima ação;
- agenda;
- SLAs;
- propostas;
- metas básicas.

**Objetivo:** Caio conseguir trabalhar 100% do comercial no sistema.

## Fase 2 — Projetos

- projetos;
- entregas;
- atividades;
- board;
- timeline;
- apontamento;
- equipe;
- capacidade;
- riscos;
- impedimentos.

## Fase 3 — Financeiro

- receber;
- pagar;
- receitas;
- despesas;
- caixa;
- DRE;
- projeto × financeiro.

## Fase 4 — Gestão

- cockpit executivo;
- Project Health;
- forecast operacional;
- relatórios;
- drill-down;
- alertas.

## Fase 5 — Inteligência

- copiloto;
- daily;
- insights;
- explicação de desvios;
- recomendações.

## Fase 6 — Produto SaaS

- onboarding multiempresa;
- planos;
- billing;
- white-label;
- integrações;
- API externa.

---

# 81. SPRINT 1 RECOMENDADA

Objetivo:

**entrar no sistema, cadastrar equipe e começar a alimentar o CRM.**

Entregas:

1. Repositório e estrutura.
2. Docker backend.
3. PostgreSQL.
4. Alembic.
5. Next.js/Vercel.
6. Login.
7. Organizações.
8. Usuários.
9. Perfis.
10. Layout principal.
11. Command palette inicial.
12. Clientes/contas.
13. Contatos.
14. Pré-leads.
15. Pipeline básico.
16. Auditoria.

---

# 82. SPRINT 2

Objetivo:

**controlar completamente o trabalho comercial.**

- oportunidade;
- interação;
- próxima ação;
- agenda;
- aging;
- SLA;
- filtros;
- views;
- Kanban;
- drawer de oportunidade;
- dashboard comercial;
- metas.

---

# 83. SPRINT 3

Objetivo:

**propostas e fechamento.**

- proposta;
- versões;
- itens;
- aprovação;
- PDF;
- envio;
- histórico;
- ganho/perda;
- contratos;
- conversão em projeto.

---

# 84. CRITÉRIOS DE ACEITE VISUAL

Uma tela não está pronta somente por funcionar.

Validar:

1. hierarquia clara;
2. nenhuma ação quebrada;
3. loading;
4. empty state;
5. erro;
6. responsividade;
7. keyboard;
8. dark mode quando implementado;
9. alinhamento;
10. consistência;
11. densidade;
12. acessibilidade;
13. ausência de overflow;
14. dados grandes;
15. textos longos;
16. datas e moedas brasileiras.

---

# 85. CRITÉRIOS DE ACEITE DE BACKEND

- migrations;
- validações;
- testes;
- autorização;
- tenant isolation;
- auditoria;
- erros padronizados;
- OpenAPI;
- logs;
- índices;
- transações para operações críticas.

---

# 86. DEFINIÇÃO DE PRONTO

Uma feature somente está concluída quando possui:

- regra de negócio;
- backend;
- autorização;
- frontend;
- validação;
- loading;
- erro;
- estado vazio;
- responsividade;
- auditoria quando aplicável;
- testes;
- documentação mínima.

---

# 87. DADOS DE DEMONSTRAÇÃO

Criar seed para desenvolvimento.

Organização:

`InnovAgro`

Usuários fictícios:

- Diretor;
- Comercial;
- Gerente de projeto;
- Financeiro;
- Colaborador.

Popular:

- 8 clientes;
- 20 pré-leads;
- 15 oportunidades;
- 5 propostas;
- 6 projetos;
- 30 atividades;
- financeiro fictício.

Nunca colocar dados reais em seed público.

---

# 88. PRINCÍPIOS DE MICROCOPY

Evitar:

`Operação realizada com sucesso.`

Preferir:

`Proposta enviada.`

Evitar:

`Tem certeza que deseja efetuar essa operação?`

Preferir:

`Arquivar oportunidade? Ela sairá do pipeline, mas o histórico será mantido.`

---

# 89. COMPONENTES DE DESIGN A CONSTRUIR

```text
AppShell
Sidebar
Topbar
CommandPalette
QuickCreate
PageHeader
FilterBar
SmartTable
PipelineBoard
EntityDrawer
Timeline
ActivityComposer
MetricStrip
HealthBadge
StatusPill
ProgressBar
ForecastIndicator
Money
DateTime
UserAvatar
EmptyState
ErrorState
Skeleton
Toast
ConfirmDialog
SearchSelect
DateRangePicker
ChartPanel
AttentionFeed
```

---

# 90. O QUE NÃO FAZER

- dashboard com 4 colunas de cards iguais;
- neon;
- gradiente como identidade;
- glassmorphism em tudo;
- menu com 30 itens de primeiro nível;
- modal para cada ação;
- ícones grandes;
- texto centralizado em sistema de dados;
- formulários de 50 campos em uma tela;
- salvar página inteira;
- reload após CRUD;
- status somente por cor;
- gráficos sem pergunta gerencial;
- IA em todo lugar;
- chat flutuante obstruindo operação;
- animações longas.

---

# 91. DIFERENCIAL DO PRODUTO

O diferencial não será ter:

- CRM;
- Kanban;
- financeiro.

Existem dezenas de produtos que fazem cada parte.

O diferencial será conectar o fluxo econômico e operacional:

```text
Contato
↓
Oportunidade
↓
Receita potencial
↓
Contrato
↓
Projeto
↓
Capacidade
↓
Horas
↓
Custo
↓
Faturamento
↓
Caixa
↓
Margem
```

Assim a plataforma consegue responder:

> **Estamos ocupados ou estamos gerando resultado?**

---

# 92. VISÃO HOLÍSTICA — MODELO DE DRILL-DOWN

Exemplo:

```text
Margem da empresa
44%
   ↓
Margem por unidade
   ↓
Margem por cliente
   ↓
Margem por projeto
   ↓
Custos do projeto
   ↓
Horas / fornecedor / despesa
   ↓
Registro original
```

Outro:

```text
Forecast comercial
R$ 94.500
   ↓
Vendedor
   ↓
Oportunidades
   ↓
Oportunidade
   ↓
Histórico de contato
```

---

# 93. FUTURAS AUTOMAÇÕES

Exemplos:

```text
Quando oportunidade entrar em Proposta
→ criar tarefa de follow-up para +3 dias.

Quando proposta estiver a 3 dias de expirar
→ avisar comercial.

Quando oportunidade for ganha
→ solicitar contrato.

Quando contrato for ativado
→ criar projeto.

Quando conta vencer
→ notificar financeiro.

Quando projeto ficar crítico
→ notificar gerente e direção.

Quando margem prevista cair abaixo de X
→ criar alerta.

Quando não houver interação comercial por X dias
→ destacar oportunidade.
```

---

# 94. INTEGRAÇÕES FUTURAS

- Gmail/Outlook;
- Google Calendar;
- WhatsApp;
- emissão de NFS-e;
- bancos;
- gateways;
- assinatura eletrônica;
- GitHub;
- Google Drive;
- Slack/Teams;
- importação Excel/CSV.

Não bloquear MVP esperando integrações.

---

# 95. NOMENCLATURA

Nome de trabalho:

**InnovAgro 360**

Alternativas futuras:

- Orbit;
- Flux;
- Núcleo;
- Axis;
- Pulse;
- OneFlow.

Não investir tempo em naming antes do produto base estar funcional.

---

# 96. KPIs DA PRÓPRIA PLATAFORMA

Após uso real medir:

- usuários ativos;
- ações comerciais registradas;
- follow-ups no prazo;
- tempo para registrar interação;
- uso da busca;
- tempo para encontrar cliente;
- tarefas vencidas;
- completude CRM;
- porcentagem do financeiro associado a projeto/centro;
- satisfação interna.

---

# 97. PRIORIDADE DE EXPERIÊNCIA

Se houver conflito entre “mais funcionalidades na tela” e “clareza”, priorizar clareza.

Se houver conflito entre animação e velocidade, priorizar velocidade.

Se houver conflito entre customização extrema e consistência inicial, priorizar consistência.

Se houver conflito entre dashboard bonito e indicador útil, priorizar indicador útil.

---

# 98. RESULTADO ESPERADO DO MVP

Ao final das primeiras fases, a InnovAgro deve conseguir:

1. cadastrar equipe;
2. controlar permissões;
3. prospectar;
4. registrar tudo que o comercial falou com o cliente;
5. saber qual é a próxima ação;
6. saber há quanto tempo cada oportunidade está parada;
7. acompanhar metas;
8. gerar propostas;
9. fechar negócio;
10. transformar venda em projeto;
11. planejar entregas;
12. controlar atividades;
13. apontar horas;
14. acompanhar capacidade;
15. controlar custos;
16. controlar recebimentos;
17. analisar margem;
18. visualizar caixa;
19. enxergar riscos;
20. abrir o dashboard e entender o que exige atenção.

---

# 99. PRIMEIRA TAREFA DO CODEX

Antes de implementar features, executar:

1. Criar monorepo.
2. Criar `/docs`.
3. Copiar este arquivo para `/docs/MASTER_SPEC.md`.
4. Criar `/docs/ARCHITECTURE.md`.
5. Criar `/docs/DATA_MODEL.md`.
6. Criar `/docs/API.md`.
7. Criar `/docs/DESIGN_SYSTEM.md`.
8. Criar `/docs/DECISIONS.md`.
9. Criar `/docs/ROADMAP.md`.
10. Criar issues/tarefas da Fase 0 e Fase 1.
11. Implementar design tokens.
12. Implementar shell autenticado.
13. Implementar autenticação e RBAC.
14. Implementar isolamento por `organization_id`.
15. Somente depois iniciar CRM.

---

# 100. ORDEM DE PRIORIDADE PARA O CODEX

```text
Integridade dos dados
> Segurança
> Regra de negócio
> Clareza de UX
> Performance
> Estética
> Animação
```

A estética é importante, mas não pode compensar erro de negócio.

A experiência premium virá de:

- coerência;
- rapidez;
- contexto;
- densidade equilibrada;
- boas decisões;
- excelente tipografia;
- microinterações discretas;
- profundidade de dados;
- ausência de atrito.

---

# 101. FRASE-GUIA

Durante o desenvolvimento, usar esta pergunta:

> **Esta tela ajuda alguém a decidir ou executar algo melhor?**

Se a resposta for não, reconsiderar sua existência.

---

# 102. REFERÊNCIAS DO BENCHMARKING

- Linear — https://linear.app/
- Linear UI Refresh 2026 — https://linear.app/changelog/2026-03-12-ui-refresh
- Attio — https://attio.com/
- Attio Lists — https://attio.com/help/reference/managing-your-data/lists/create-lists
- monday CRM — https://monday.com/crm/use-cases/sales-pipeline
- monday CRM Features — https://monday.com/crm/product-features
- Ramp — https://ramp.com/
- Ramp Reporting — https://support.ramp.com/real-time-reporting/
- ClickUp Dashboards — https://help.clickup.com/hc/en-us/articles/6312197753239-Intro-to-Dashboards
- Notion Projects — https://www.notion.com/product/projects
- Notion Timeline — https://www.notion.com/help/timelines
- Stripe Dashboard — https://support.stripe.com/topics/dashboard?locale=pt-BR

---

# 103. ENCERRAMENTO

A InnovAgro 360 deve funcionar como um **sistema operacional de gestão**, não como uma coleção de módulos.

CRM controla relacionamento e receita futura.

Projetos controlam execução.

Timesheet e capacidade transformam trabalho em informação econômica.

Financeiro transforma contratos e execução em caixa e resultado.

Dashboard transforma dados em decisão.

IA transforma contexto em síntese e recomendação.

A plataforma deve ser simples na superfície e profunda quando o usuário fizer drill-down.

**Este é o norte do produto.**
