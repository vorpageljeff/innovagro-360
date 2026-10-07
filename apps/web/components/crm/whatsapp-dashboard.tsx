"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { ArrowDownLeft, ArrowUpRight, CheckCircle2, MessageCircle, RefreshCw, ShieldAlert, UsersRound, Workflow } from "lucide-react";
import { AutomationPanel } from "./automation-panel";
import styles from "./whatsapp-dashboard.module.css";

type Connection = { configured: boolean; bot_enabled: boolean; state: string };
type Message = { id: string; incoming: string; reply: string; state: string; created_at: string };
type Conversation = Message & { lead_id: string | null; name: string; phone: string | null; priority: string; bot_paused: boolean; status: string | null };
type QueueItem = { id: string; name: string; phone: string; priority: string; updated_at: string };
type Dashboard = {
  days: number; since: string; updated_at: string;
  summary: { received: number; sent: number; new_contacts: number; waiting_human: number; attention: number; active_rules: number };
  series: { day: string; received: number; sent: number }[];
  recent: Conversation[]; queue: QueueItem[];
};
const priorities: Record<string, string> = { urgente: "Urgente", alta: "Alta", media: "Média", baixa: "Baixa" };
const states: Record<string, string> = { sent: "Aceita pelo Evolution", paused: "Bot pausado", uncertain: "Envio sem confirmação", sending: "Envio iniciado", completed: "Fluxo concluído", no_rule: "Sem fluxo correspondente", received: "Recebida", unmatched: "Sem contato associado" };
const connectionLabels: Record<string, string> = { open: "WhatsApp conectado", close: "WhatsApp desconectado", connecting: "Conectando ao WhatsApp", not_configured: "Configuração pendente" };
const number = (value: number) => value.toLocaleString("pt-BR");
function timestamp(value: string) { return new Date(value).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }); }
async function api(path: string, signal?: AbortSignal, body?: unknown) {
  const response = await fetch(`/api/crm/${path}`, { signal, cache: "no-store", ...(body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {}) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message ?? "Não foi possível atualizar o painel.");
  return data;
}

export function WhatsAppDashboard() {
  const [days, setDays] = useState(7);
  const [tab, setTab] = useState("overview");
  const [data, setData] = useState<Dashboard | null>(null);
  const [connection, setConnection] = useState<Connection | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState("");
  const [selected, setSelected] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [messageError, setMessageError] = useState("");
  const [messageLoading, setMessageLoading] = useState(false);
  const controller = useRef<AbortController | null>(null);
  const dialog = useRef<HTMLDialogElement | null>(null);
  const requestId = useRef(0);
  const load = useCallback(async () => {
    controller.current?.abort();
    const abort = new AbortController(); controller.current = abort;
    const current = ++requestId.current;
    setLoading(true);
    const results = await Promise.allSettled([api(`evolution/dashboard?days=${days}`, abort.signal), api("evolution/status", abort.signal)]);
    if (current !== requestId.current || abort.signal.aborted) return;
    const errors: string[] = [];
    if (results[0].status === "fulfilled") setData(results[0].value);
    else errors.push(results[0].reason.message);
    if (results[1].status === "fulfilled") setConnection(results[1].value);
    else { setConnection(null); errors.push("Conexão não confirmada: " + results[1].reason.message); }
    setError(errors.join(" ")); setLoading(false);
  }, [days]);
  useEffect(() => {
    void load();
    const interval = setInterval(() => { if (!document.hidden) void load(); }, 30000);
    const visible = () => { if (!document.hidden) void load(); };
    document.addEventListener("visibilitychange", visible);
    return () => { clearInterval(interval); document.removeEventListener("visibilitychange", visible); ++requestId.current; controller.current?.abort(); };
  }, [load]);
  useEffect(() => {
    if (!selected?.lead_id) return;
    const abort = new AbortController();
    setMessages([]); setMessageError(""); setMessageLoading(true);
    if (dialog.current && !dialog.current.open) dialog.current.showModal();
    void api(`leads/${selected.lead_id}/messages`, abort.signal).then(rows => {
      if (!abort.signal.aborted) setMessages(rows);
    }).catch(e => { if (!abort.signal.aborted) setMessageError(e.message); }).finally(() => { if (!abort.signal.aborted) setMessageLoading(false); });
    return () => abort.abort();
  }, [selected?.lead_id]);
  async function setHuman(id: string, paused: boolean) {
    if (busyId) return; setBusyId(id); setNotice("");
    try {
      const lead = await api(`leads/${id}/settings`, undefined, { bot_paused: paused });
      setSelected(old => old?.lead_id === id ? { ...old, bot_paused: lead.bot_paused, status: lead.status } : old);
      setNotice(paused ? "Atendimento assumido. O bot está pausado neste contato." : connection?.bot_enabled ? "Bot retomado neste contato." : "Contato liberado para o bot. As respostas automáticas continuam pausadas no servidor.");
      await load();
    } catch (e) { setError((e as Error).message); }
    finally { setBusyId(""); }
  }
  const connected = connection?.state === "open";
  const summary = data?.summary;
  const max = Math.max(1, ...(data?.series.map(day => day.received) ?? []));
  return <div className={`content ${styles.dashboard}`}>
    <div className="page-heading"><div><p className="eyebrow">ATENDIMENTO</p><h1 className="title">Controle do WhatsApp</h1><p className="subtitle">Acompanhe as conversas, o bot e a fila da sua equipe.</p></div><div className={styles.actions}><Link href="/crm" className="btn">Abrir Kanban</Link><button className="btn" disabled={loading} onClick={() => void load()}><RefreshCw size={15} className={loading ? styles.spin : ""} /> Atualizar</button></div></div>
    <section className={styles.connection}><div className={styles.connectionIcon}><MessageCircle size={27} /></div><div><span className={styles.connectionLabel}>SEU CANAL DE ATENDIMENTO</span><h2>{connection ? connectionLabels[connection.state] ?? "Estado da conexão desconhecido" : loading ? "Verificando conexão" : "Conexão não confirmada"}</h2><p>{connected ? connection?.bot_enabled ? "Canal disponível para receber mensagens e executar seus fluxos." : "Canal conectado. As respostas automáticas estão pausadas." : "Confira a conexão antes de usar o atendimento automático."}</p></div><div className={styles.connectionRight}><span className={`${styles.badge} ${connected ? styles.online : styles.offline}`}><i />{connected ? "Conectado" : "Não confirmado"}</span><button className="btn" onClick={() => setTab("flows")}>{connected ? "Gerenciar bot" : "Conectar WhatsApp"}</button></div></section>
    <div className={styles.toolbar}><div className={styles.tabs}><button aria-pressed={tab === "overview"} onClick={() => setTab("overview")}>Visão geral</button><button aria-pressed={tab === "flows"} onClick={() => setTab("flows")}>Fluxos e bot</button></div><label>Período <select aria-label="Período do painel" value={days} onChange={e => { setData(null); setDays(Number(e.target.value)); }}><option value={1}>Hoje</option><option value={7}>Últimos 7 dias</option><option value={30}>Últimos 30 dias</option></select></label></div>
    {error && <p className={styles.error} role="alert">{error} {data && "Os dados abaixo são da última atualização confirmada."}</p>}
    {notice && <p className={styles.notice} role="status">{notice}</p>}
    {tab === "flows" ? <AutomationPanel /> : <>
      <div className={styles.metrics}>
        <article className={styles.metric}><span><ArrowDownLeft size={18} /> Mensagens recebidas</span><strong>{summary ? number(summary.received) : "—"}</strong><small>No período selecionado</small></article>
        <article className={styles.metric}><span><ArrowUpRight size={18} /> Respostas do bot</span><strong>{summary ? number(summary.sent) : "—"}</strong><small>Aceitas pelo Evolution no período</small></article>
        <article className={styles.metric}><span><UsersRound size={18} /> Atendimento humano</span><strong>{summary ? number(summary.waiting_human) : "—"}</strong><small>Contatos na fila atual</small></article>
        <article className={`${styles.metric} ${summary?.attention ? styles.attention : ""}`}><span><ShieldAlert size={18} /> Envios para verificar</span><strong>{summary ? number(summary.attention) : "—"}</strong><small>Sem confirmação ou iniciados há mais de 2 min</small></article>
      </div>
      <div className={styles.columns}>
        <section className={`panel ${styles.chartPanel}`}><div className={styles.sectionHeading}><div><h2>Movimento das conversas</h2><p>Mensagens de texto e respostas registradas no CRM</p></div><span className={styles.legend}><i />Recebidas <b />Respostas</span></div>{!data ? <p className={styles.empty}>{loading ? "Carregando atividade…" : "Dados ainda indisponíveis."}</p> : <><div className={styles.chart} role="img" aria-label={`Atividade diária: ${data.series.map(day => `${day.day}: ${day.received} recebidas e ${day.sent} respostas`).join("; ")}`}>{data.series.map((day, i) => <div className={styles.chartDay} key={day.day} title={`${day.day.split("-").reverse().join("/")}: ${day.received} recebidas, ${day.sent} respostas`}><div className={styles.bars}><div className={styles.receivedBar} style={{ height: `${day.received / max * 100}%` }} /><div className={styles.sentBar} style={{ height: `${day.sent / max * 100}%` }} /></div><small>{data.days <= 7 || i % 5 === 0 || i === data.days - 1 ? day.day.slice(8) + "/" + day.day.slice(5, 7) : ""}</small></div>)}</div>{summary?.received === 0 && <p className={styles.hint}>Nenhuma mensagem de texto recebida neste período. Para testar, envie “Oi” de outro número para o WhatsApp conectado.</p>}</>}</section>
        <section className={`panel ${styles.botPanel}`}><div className={styles.sectionHeading}><h2>Operação do bot</h2><Workflow size={19} /></div><div className={styles.botStat}><span>Fluxos ativos</span><strong>{summary?.active_rules ?? "—"}</strong></div><div className={styles.botStat}><span>Novos contatos no período</span><strong>{summary?.new_contacts ?? "—"}</strong></div><div className={styles.botStat}><span>Bot no servidor</span><strong>{connection ? connection.bot_enabled ? "Habilitado" : "Pausado" : "Não confirmado"}</strong></div><p className={styles.hint}>A equipe assume a conversa quando o fluxo encaminha para uma pessoa. O bot fica pausado naquele contato até você retomá-lo.</p><button className="btn primary" onClick={() => setTab("flows")}>Editar fluxos e testar bot</button></section>
      </div>
      <section className={`panel ${styles.queue}`}><div className={styles.sectionHeading}><div><h2>Fila de atendimento humano</h2><p>Prioridades mais altas aparecem primeiro · até 20 contatos</p></div><UsersRound size={20} /></div>{!data ? <p className={styles.empty}>Carregando fila…</p> : !data.queue.length ? <div className={styles.empty}><CheckCircle2 size={24} /><p>Nenhum contato aguardando atendimento humano.</p></div> : data.queue.map(item => <article className={styles.queueRow} key={item.id}><span className={`${styles.priority} ${styles[item.priority]}`}>{priorities[item.priority]}</span><div><strong>{item.name}</strong><small>{item.phone} · {timestamp(item.updated_at)}</small></div><button className="btn" disabled={!!busyId} onClick={() => void setHuman(item.id, false)}>Retomar bot</button></article>)}</section>
      <section className={`panel ${styles.recent}`}><div className={styles.sectionHeading}><div><h2>Mensagens recentes</h2><p>As 20 mais recentes no período selecionado</p></div><MessageCircle size={20} /></div>{!data ? <p className={styles.empty}>Carregando mensagens…</p> : !data.recent.length ? <p className={styles.empty}>As conversas aparecerão aqui quando chegarem pelo WhatsApp.</p> : <div className={styles.tableWrap}><table><thead><tr><th>Contato</th><th>Mensagem</th><th>Processamento</th><th>Recebida em</th><th aria-label="Ações" /></tr></thead><tbody>{data.recent.map(item => <tr key={item.id}><td><strong>{item.name}</strong><small>{item.phone ?? "—"}</small></td><td><span className={styles.preview}>{item.incoming}</span></td><td><span className={`${styles.state} ${["uncertain", "sending"].includes(item.state) ? styles.warning : ""}`}>{states[item.state] ?? item.state}</span></td><td>{timestamp(item.created_at)}</td><td><button className="btn" disabled={!item.lead_id} onClick={() => setSelected(item)}>Ver conversa</button></td></tr>)}</tbody></table></div>}</section>
    </>}
    <p className={styles.updated}>{data ? `Atualizado em ${timestamp(data.updated_at)} · horário de Brasília` : "Aguardando dados do servidor"} · atualização automática a cada 30 segundos</p>
    {selected && <dialog ref={dialog} aria-labelledby="conversation-title" className={styles.dialog} onCancel={() => setSelected(null)} onClose={() => setSelected(null)}><div className={styles.sectionHeading}><div><h2 id="conversation-title">{selected.name}</h2><p>{selected.phone}</p></div><button className="btn" onClick={() => setSelected(null)}>Fechar</button></div>{messageError && <p role="alert" className={styles.error}>{messageError}</p>}{messageLoading ? <p>Carregando conversa…</p> : messages.slice().reverse().map(message => <article className={styles.message} key={message.id}><small>{timestamp(message.created_at)}</small><p><strong>Contato</strong><br />{message.incoming}</p>{message.reply && <p className={styles.reply}><strong>Bot</strong><br />{message.reply}</p>}<small>{states[message.state] ?? message.state}</small></article>)}{selected.lead_id && !["sem_interesse", "convertido"].includes(selected.status ?? "") && <button className="btn primary" disabled={!!busyId} onClick={() => void setHuman(selected.lead_id!, !selected.bot_paused)}>{selected.bot_paused ? "Retomar bot" : "Assumir atendimento"}</button>}</dialog>}
  </div>;
}
