"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, BriefcaseBusiness, Building2, CalendarDays, ChartNoAxesCombined, CircleDollarSign, FolderKanban, LayoutDashboard, Plus, Search, Settings, Sparkles, UsersRound, type LucideIcon } from "lucide-react";

type NavItem = { label: string; href: string; icon: LucideIcon };
const groups: { label: string; items: NavItem[] }[] = [
  { label: "", items: [{ label: "Início", href: "/dashboard", icon: LayoutDashboard }] },
  { label: "COMERCIAL", items: [{ label: "CRM", href: "/crm", icon: BriefcaseBusiness }, { label: "Agenda", href: "/agenda", icon: CalendarDays }] },
  { label: "OPERAÇÃO", items: [{ label: "Clientes", href: "/clientes", icon: Building2 }, { label: "Projetos", href: "/projetos", icon: FolderKanban }, { label: "Equipe", href: "/equipe", icon: UsersRound }] },
  { label: "FINANCEIRO", items: [{ label: "Visão financeira", href: "/financeiro", icon: CircleDollarSign }] },
  { label: "GESTÃO", items: [{ label: "Indicadores", href: "/indicadores", icon: ChartNoAxesCombined }] },
  { label: "IA", items: [{ label: "Copiloto", href: "/copiloto", icon: Sparkles }] },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const current = groups.flatMap((group) => group.items).find((item) => pathname.startsWith(item.href))?.label ?? (pathname === "/configuracoes" ? "Configurações" : "Workspace");
  return <div className="shell"><aside className="sidebar"><div className="brand"><b className="brand-mark">360</b><span>InnovAgro</span></div><nav>{groups.map((group) => <div key={group.label || "home"}>{group.label ? <div className="nav-label">{group.label}</div> : null}{group.items.map((item) => { const Icon = item.icon; const active = pathname === item.href || pathname.startsWith(`${item.href}/`); return <Link className={`nav-item ${active ? "active" : ""}`} href={item.href} key={item.href} aria-current={active ? "page" : undefined}><Icon /><span>{item.label}</span></Link>; })}</div>)}</nav><Link className="sidebar-foot" href="/configuracoes"><Settings size={16} /><span>Configurações</span></Link></aside><main className="main"><header className="topbar"><span className="muted">Workspace / {current}</span><div className="top-actions"><button className="btn"><Search size={15} /> Buscar <kbd>⌘ K</kbd></button><Link className="btn primary" href="/crm?new=1"><Plus size={15} /> Criar</Link><button className="btn" aria-label="Notificações"><Bell size={16} /></button></div></header>{children}</main></div>;
}
