"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, ArrowRight, CalendarDays, CheckCircle2, ChevronDown, CircleDot, Clock3, Filter, LayoutGrid, List, MoreHorizontal, Plus, Search, TrendingUp, Users, X } from "lucide-react";

type Status = "backlog" | "planned" | "doing" | "validation" | "done";
type Task = { id: number; title: string; project: string; status: Status; priority: "Crítica" | "Alta" | "Média"; owner: string; due: string; estimate: number; logged: number; tags: string[]; blocked?: boolean };

const statusMeta: { id: Status; label: string; tone: string }[] = [
  { id: "backlog", label: "Backlog", tone: "neutral" },
  { id: "planned", label: "Planejado", tone: "info" },
  { id: "doing", label: "Em execução", tone: "accent" },
  { id: "validation", label: "Em validação", tone: "warning" },
  { id: "done", label: "Concluído", tone: "success" },
];

const initialTasks: Task[] = [
  { id: 101, title: "Mapear jornada do produtor", project: "Portal Santé", status: "backlog", priority: "Média", owner: "LV", due: "18 set", estimate: 8, logged: 0, tags: ["Discovery"] },
  { id: 102, title: "Validar integração de pagamentos", project: "Portal Santé", status: "planned", priority: "Alta", owner: "MS", due: "15 set", estimate: 12, logged: 3, tags: ["Backend"], blocked: true },
  { id: 103, title: "Construir dashboard comercial", project: "CRM InnovAgro", status: "planned", priority: "Média", owner: "JV", due: "19 set", estimate: 16, logged: 2, tags: ["Frontend"] },
  { id: 104, title: "Revisar regras de comissão", project: "CRM InnovAgro", status: "doing", priority: "Alta", owner: "CS", due: "Hoje", estimate: 6, logged: 4, tags: ["Regra de negócio"] },
  { id: 105, title: "Implementar cadastro de propriedades", project: "Portal Santé", status: "doing", priority: "Crítica", owner: "MS", due: "13 set", estimate: 20, logged: 17, tags: ["Backend", "API"] },
  { id: 106, title: "Teste responsivo do onboarding", project: "Academia Agro", status: "validation", priority: "Alta", owner: "AB", due: "Hoje", estimate: 5, logged: 6, tags: ["QA"] },
  { id: 107, title: "Aprovar identidade da campanha", project: "Safra Digital", status: "validation", priority: "Média", owner: "LV", due: "14 set", estimate: 4, logged: 3, tags: ["Design"] },
  { id: 108, title: "Publicar landing page", project: "Safra Digital", status: "done", priority: "Alta", owner: "JV", due: "10 set", estimate: 8, logged: 7, tags: ["Frontend"] },
];
const STORAGE_KEY = "innovagro.projects.board.v1";

const projects = [
  { name: "Portal Santé", client: "Santé Agrícola", health: 68, progress: 54, due: "02 out", hours: "78%", margin: "31%", tone: "danger" },
  { name: "CRM InnovAgro", client: "InnovAgro", health: 91, progress: 72, due: "18 out", hours: "63%", margin: "48%", tone: "success" },
  { name: "Academia Agro", client: "Cooperativa Oeste", health: 82, progress: 64, due: "27 set", hours: "69%", margin: "42%", tone: "warning" },
  { name: "Safra Digital", client: "Grupo Vale", health: 88, progress: 83, due: "20 set", hours: "81%", margin: "39%", tone: "success" },
];

function TaskCard({ task, onOpen }: { task: Task; onOpen: (task: Task) => void }) {
  return <article className="task-card" draggable onDragStart={(event) => event.dataTransfer.setData("text/task-id", String(task.id))} onClick={() => onOpen(task)} tabIndex={0} onKeyDown={(event) => event.key === "Enter" && onOpen(task)} aria-label={`Abrir atividade ${task.title}`}><div className="task-card-top"><span className={`priority priority-${task.priority.toLowerCase().replace("í", "i").replace("é", "e")}`}>{task.priority}</span><button className="icon-button" aria-label="Mais ações" onClick={(event) => event.stopPropagation()}><MoreHorizontal size={16} /></button></div><h3>{task.title}</h3><p className="task-project">{task.project}</p><div className="task-tags">{task.blocked && <span className="tag blocked"><AlertTriangle size={12} /> Bloqueada</span>}{task.tags.map((tag) => <span className="tag" key={tag}>{tag}</span>)}</div><div className="task-footer"><span className="avatar-mini">{task.owner}</span><span className={task.due === "Hoje" ? "due today" : "due"}><CalendarDays size={13} /> {task.due}</span><span className="hours"><Clock3 size={13} /> {task.logged}/{task.estimate}h</span></div></article>;
}

export function ProjectsWorkspace() {
  const [tasks, setTasks] = useState(initialTasks);
  const [view, setView] = useState<"board" | "portfolio">("board");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Task | null>(null);
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) setTasks(JSON.parse(saved) as Task[]);
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, []);
  const visibleTasks = useMemo(() => { const normalized = query.trim().toLowerCase(); return normalized ? tasks.filter((task) => `${task.title} ${task.project} ${task.tags.join(" ")}`.toLowerCase().includes(normalized)) : tasks; }, [query, tasks]);
  function moveTask(taskId: number, status: Status) {
    setTasks((current) => {
      const next = current.map((task) => task.id === taskId ? { ...task, status } : task);
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }

  return <div className="content projects-page"><div className="page-heading"><div><p className="eyebrow">OPERAÇÃO</p><h1 className="title">Projetos</h1><p className="subtitle">Entregas, esforço, prazo e margem conectados em uma visão operacional.</p></div><button className="btn primary"><Plus size={16} /> Novo projeto</button></div><section className="project-kpis"><div><span>Projetos ativos</span><strong>6</strong><small><TrendingUp size={13} /> 2 encerram este mês</small></div><div><span>Saúde média</span><strong>82</strong><small className="warning-text"><AlertTriangle size={13} /> 1 projeto crítico</small></div><div><span>Entregas no prazo</span><strong>87%</strong><small>+4 p.p. no período</small></div><div><span>Capacidade da equipe</span><strong>94%</strong><small className="warning-text"><Users size={13} /> 2 pessoas sobrecarregadas</small></div></section><div className="project-toolbar"><div className="segmented" aria-label="Visualização"><button className={view === "board" ? "active" : ""} onClick={() => setView("board")}><LayoutGrid size={15} /> Board</button><button className={view === "portfolio" ? "active" : ""} onClick={() => setView("portfolio")}><List size={15} /> Portfólio</button></div><div className="toolbar-actions"><label className="search-field"><Search size={15} /><input aria-label="Buscar atividades" placeholder="Buscar atividade..." value={query} onChange={(event) => setQuery(event.target.value)} /></label><button className="btn"><Filter size={15} /> Filtros</button><button className="btn">Todos os projetos <ChevronDown size={14} /></button></div></div>{view === "board" ? <section className="kanban" aria-label="Board de atividades">{statusMeta.map((status) => { const columnTasks = visibleTasks.filter((task) => task.status === status.id); return <div className="kanban-column" key={status.id} onDragOver={(event) => event.preventDefault()} onDrop={(event) => moveTask(Number(event.dataTransfer.getData("text/task-id")), status.id)}><div className="column-head"><span className={`status-dot ${status.tone}`} /><strong>{status.label}</strong><span>{columnTasks.length}</span><button aria-label={`Adicionar em ${status.label}`}><Plus size={15} /></button></div><div className="column-body">{columnTasks.map((task) => <TaskCard task={task} onOpen={setSelected} key={task.id} />)}{columnTasks.length === 0 && <div className="column-empty">Arraste uma atividade para cá.</div>}</div></div>; })}</section> : <section className="portfolio panel"><div className="portfolio-head"><span>Projeto</span><span>Saúde</span><span>Progresso</span><span>Prazo</span><span>Horas</span><span>Margem</span></div>{projects.map((project) => <div className="portfolio-row" key={project.name}><div><strong>{project.name}</strong><small>{project.client}</small></div><span className={`health health-${project.tone}`}>{project.health}</span><div className="progress-cell"><span>{project.progress}%</span><i><b style={{ width: `${project.progress}%` }} /></i></div><span>{project.due}</span><span>{project.hours}</span><strong>{project.margin}</strong></div>)}</section>}{selected && <div className="drawer-backdrop" onMouseDown={() => setSelected(null)}><aside className="task-drawer" onMouseDown={(event) => event.stopPropagation()} aria-label="Detalhes da atividade"><div className="drawer-head"><span className="eyebrow">ATIVIDADE #{selected.id}</span><button className="icon-button" aria-label="Fechar" onClick={() => setSelected(null)}><X size={18} /></button></div><h2>{selected.title}</h2><p className="subtitle">{selected.project}</p><div className="drawer-section"><label>Status</label><select value={selected.status} onChange={(event) => { const next = event.target.value as Status; moveTask(selected.id, next); setSelected({ ...selected, status: next }); }}>{statusMeta.map((status) => <option value={status.id} key={status.id}>{status.label}</option>)}</select></div><div className="drawer-grid"><div><label>Responsável</label><span><span className="avatar-mini">{selected.owner}</span> Equipe</span></div><div><label>Prazo</label><span>{selected.due}</span></div><div><label>Estimativa</label><span>{selected.estimate} horas</span></div><div><label>Realizado</label><span>{selected.logged} horas</span></div></div><div className="drawer-section"><label>Progresso de horas</label><div className="hours-progress"><i style={{ width: `${Math.min(100, selected.logged / selected.estimate * 100)}%` }} /></div></div><button className="btn primary drawer-action">Abrir atividade completa <ArrowRight size={15} /></button></aside></div>}</div>;
}
