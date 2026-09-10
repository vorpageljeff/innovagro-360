import { notFound } from "next/navigation";

const modules: Record<string, { eyebrow: string; title: string; description: string; action: string; items: [string, string][] }> = {
  crm: { eyebrow: "COMERCIAL", title: "CRM", description: "Relacionamentos, oportunidades e próximas ações em um só contexto.", action: "+ Nova oportunidade", items: [["Pipeline aberto", "R$ 187.500"], ["Follow-ups hoje", "8"], ["Oportunidades paradas", "3"]] },
  agenda: { eyebrow: "COMERCIAL", title: "Agenda", description: "Compromissos e próximas ações da equipe comercial.", action: "+ Novo compromisso", items: [["Hoje", "5 compromissos"], ["Esta semana", "18 ações"], ["Vencidas", "2"]] },
  clientes: { eyebrow: "OPERAÇÃO", title: "Clientes", description: "Visão única de contas, contatos, projetos e histórico financeiro.", action: "+ Novo cliente", items: [["Clientes ativos", "8"], ["Projetos ativos", "6"], ["Saldo a receber", "R$ 24.800"]] },
  projetos: { eyebrow: "OPERAÇÃO", title: "Projetos", description: "Acompanhe entregas, prazo, horas, riscos e margem.", action: "+ Novo projeto", items: [["Em andamento", "6"], ["Em atenção", "2"], ["Críticos", "1"]] },
  equipe: { eyebrow: "OPERAÇÃO", title: "Equipe", description: "Capacidade, alocação e exceções que exigem ação.", action: "+ Convidar pessoa", items: [["Pessoas ativas", "12"], ["Capacidade média", "87%"], ["Sobrecarga", "2 pessoas"]] },
  financeiro: { eyebrow: "FINANCEIRO", title: "Visão financeira", description: "Caixa, recebíveis, pagamentos e resultado gerencial.", action: "+ Novo lançamento", items: [["Saldo disponível", "R$ 31.200"], ["A receber", "R$ 24.800"], ["Vencido", "R$ 5.800"]] },
  indicadores: { eyebrow: "GESTÃO", title: "Indicadores", description: "Dados conectados para entender causas e tomar decisões.", action: "Configurar relatório", items: [["Margem", "44,1%"], ["Conversão comercial", "31%"], ["Saúde média", "82"]] },
  copiloto: { eyebrow: "INTELIGÊNCIA", title: "Copiloto", description: "Sínteses e recomendações baseadas nos dados permitidos da organização.", action: "Nova conversa", items: [["Projetos críticos", "1"], ["Oportunidades prováveis", "4"], ["Alertas de caixa", "1"]] },
  configuracoes: { eyebrow: "ADMINISTRAÇÃO", title: "Configurações", description: "Organização, pessoas, permissões e regras do workspace.", action: "Salvar alterações", items: [["Usuários", "12"], ["Perfis", "6"], ["Integrações", "0"]] },
};

export default async function ModulePage({ params }: { params: Promise<{ section: string }> }) {
  const { section } = await params;
  const module = modules[section];
  if (!module) notFound();
  return <div className="content"><div className="page-heading"><div><p className="eyebrow">{module.eyebrow}</p><h1 className="title">{module.title}</h1><p className="subtitle">{module.description}</p></div><button className="btn primary">{module.action}</button></div><section className="module-summary">{module.items.map(([label, value]) => <div className="metric" key={label}><div className="metric-label">{label}</div><div className="metric-value">{value}</div></div>)}</section><section className="panel module-empty"><p className="panel-title">Área inicial preparada</p><p className="muted">Os dados demonstrativos e fluxos completos deste módulo serão adicionados nas próximas entregas.</p><button className="btn">Explorar visão geral</button></section></div>;
}
