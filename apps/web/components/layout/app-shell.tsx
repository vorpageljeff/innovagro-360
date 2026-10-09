"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { Bell, BriefcaseBusiness, Building2, CalendarDays, ChartNoAxesCombined, CircleDollarSign, FolderKanban, LayoutDashboard, MessageCircle, Plus, Search, Settings, Sparkles, UsersRound, type LucideIcon } from "lucide-react";

type NavItem = { label: string; href: string; icon: LucideIcon };
const groups: { label: string; items: NavItem[] }[] = [
  { label: "", items: [{ label: "Início", href: "/dashboard", icon: LayoutDashboard }] },
  { label: "COMERCIAL", items: [{ label: "CRM", href: "/crm", icon: BriefcaseBusiness }, { label: "WhatsApp", href: "/whatsapp", icon: MessageCircle }, { label: "Agenda", href: "/agenda", icon: CalendarDays }] },
  { label: "OPERAÇÃO", items: [{ label: "Clientes", href: "/clientes", icon: Building2 }, { label: "Projetos", href: "/projetos", icon: FolderKanban }, { label: "Equipe", href: "/equipe", icon: UsersRound }] },
  { label: "FINANCEIRO", items: [{ label: "Visão financeira", href: "/financeiro", icon: CircleDollarSign }] },
  { label: "GESTÃO", items: [{ label: "Indicadores", href: "/indicadores", icon: ChartNoAxesCombined }] },
  { label: "IA", items: [{ label: "Copiloto", href: "/copiloto", icon: Sparkles }] },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [unread, setUnread] = useState(0);
  useEffect(() => {
    let stopped = false, running = false;
    const originalTitle = document.title;
    const refresh = async () => {
      if (stopped || running || document.hidden) return;
      running = true;
      try {
        const response = await fetch("/api/crm/evolution/inbox", { cache: "no-store" });
        if (!response.ok) return;
        const data = await response.json();
        if (!stopped) { setUnread(data.unread); document.title = data.unread ? `(${data.unread}) WhatsApp · Voragon CRM` : originalTitle; }
      } catch { /* The inbox shows connection errors; keep the last known badge. */ }
      finally { running = false; }
    };
    void refresh(); const timer = setInterval(refresh, 10000);
    document.addEventListener("visibilitychange", refresh);
    return () => { stopped = true; clearInterval(timer); document.removeEventListener("visibilitychange", refresh); document.title = originalTitle; };
  }, []);
  const current = groups.flatMap((group) => group.items).find((item) => pathname.startsWith(item.href))?.label ?? (pathname === "/configuracoes" ? "Configurações" : "Workspace");
  return <div className="shell"><aside className="sidebar"><div className="brand"><b className="brand-mark">360</b><span>InnovAgro</span></div><nav>{groups.map((group) => <div key={group.label || "home"}>{group.label ? <div className="nav-label">{group.label}</div> : null}{group.items.map((item) => { const Icon = item.icon; const active = pathname === item.href || pathname.startsWith(`${item.href}/`); return <Link className={`nav-item ${active ? "active" : ""}`} href={item.href} key={item.href} aria-current={active ? "page" : undefined}><Icon /><span>{item.label}</span>{item.href === "/whatsapp" && unread > 0 && <strong aria-label={`${unread} mensagens não lidas`} style={{ background: "#237449", color: "white", borderRadius: 20, padding: "2px 7px", fontSize: 11 }}>{unread}</strong>}</Link>; })}</div>)}</nav><Link className="sidebar-foot" href="/configuracoes"><Settings size={16} /><span>Configurações</span></Link></aside><main className="main"><header className="topbar"><span className="muted">Workspace / {current}</span><div className="top-actions"><button className="btn"><Search size={15} /> Buscar <kbd>⌘ K</kbd></button><Link className="btn primary" href="/crm?new=1"><Plus size={15} /> Criar</Link><Link className="btn" href="/whatsapp" aria-label={`WhatsApp: ${unread} mensagens não lidas`}><Bell size={16} />{unread > 0 && <strong>{unread}</strong>}</Link></div></header>{children}</main></div>;
}
