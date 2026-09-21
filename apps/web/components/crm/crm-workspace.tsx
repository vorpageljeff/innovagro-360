"use client";
import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import styles from "./crm.module.css";

type Lead = { id: string; name: string; instagram: string; city: string; status: string; last_contact_on: string | null; next_contact_on: string | null };
type Activity = { id: string; kind: string; occurred_on: string; note: string };
const labels: Record<string, string> = { aguardando: "Aguardando retorno", respondeu: "Respondeu", sem_interesse: "Sem interesse", convertido: "Convertido" };
function today() { return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date()); }
function date(value: string | null) { return value ? value.split("-").reverse().join("/") : "—"; }
async function api(path: string, body?: unknown) {
  const response = await fetch(`/api/crm/${path}`, { cache: "no-store", ...(body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {}) });
  const data = await response.json();
  if (!response.ok) throw Object.assign(new Error(data.message ?? "Falha ao acessar o CRM."), { status: response.status });
  return data;
}
export function CrmWorkspace() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [selected, setSelected] = useState<Lead | null>(null);
  const [history, setHistory] = useState<Activity[]>([]);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [login, setLogin] = useState(false);
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("todos");
  const [creating, setCreating] = useState(false);
  const [kind, setKind] = useState("retorno");
  const [historyLoading, setHistoryLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const [more, setMore] = useState(false);
  const eventKey = useRef("");
  const historyRequest = useRef(0);
  const importFile = useRef<HTMLInputElement>(null);
  const load = useCallback(async (page = 0) => {
    setError("");
    try {
      const rows: Lead[] = await api(`leads?offset=${page}&limit=100`);
      setLeads(old => page ? [...old, ...rows] : rows); setOffset(page); setMore(rows.length === 100); setReady(true); setLogin(false);
    } catch (e) { setReady(false); setLogin((e as { status?: number }).status === 401); setError((e as Error).message); }
  }, []);
  useEffect(() => { void load(); }, [load]);
  async function selectLead(lead: Lead) {
    const current = ++historyRequest.current;
    setSelected(lead); setHistory([]); setHistoryLoading(true); setKind("retorno"); eventKey.current = crypto.randomUUID();
    try { const rows = await api(`leads/${lead.id}/activities`); if (current === historyRequest.current) setHistory(rows); }
    catch (e) { if (current === historyRequest.current) setError((e as Error).message); }
    finally { if (current === historyRequest.current) setHistoryLoading(false); }
  }
  async function submit(event: FormEvent<HTMLFormElement>, action: "login" | "create" | "activity") {
    event.preventDefault(); if (busy) return; setBusy(true); setError(""); setNotice("");
    const form = new FormData(event.currentTarget);
    try {
      if (action === "login") await api("session", Object.fromEntries(form));
      else if (action === "create") {
        await api("leads", { ...Object.fromEntries(form), event_key: eventKey.current }); setCreating(false);
      } else if (selected) {
        await api(`leads/${selected.id}/activities`, { kind, occurred_on: form.get("occurred_on"), note: form.get("note"), event_key: eventKey.current, ...(kind === "retorno" ? { status: form.get("status") } : {}), ...(form.get("next_contact_on") ? { next_contact_on: form.get("next_contact_on") } : {}) });
        setSelected(null); ++historyRequest.current;
      }
      setNotice(action === "login" ? "Conectado ao servidor." : "Registro confirmado no servidor."); await load();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  async function importContacts(file?: File) {
    if (!file || busy) return; setBusy(true); setError(""); setNotice("");
    try {
      if (file.size > 1_000_000) throw new Error("O arquivo deve ter até 1 MB.");
      const data = JSON.parse(await file.text());
      if (!Array.isArray(data.leads) || !data.leads.length || data.leads.length > 100) throw new Error("Use um relatório JSON com 1 a 100 contatos.");
      const result = await api("import", data); setNotice(`${result.processed} registros processados no servidor. Eventos já importados não são duplicados.`); await load();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); if (importFile.current) importFile.current.value = ""; }
  }
  const visible = leads.filter(l => `${l.name} ${l.instagram} ${l.city}`.toLowerCase().includes(query.toLowerCase()) && (filter === "todos" || (filter === "hoje" ? l.next_contact_on && l.next_contact_on <= today() && !["sem_interesse", "convertido"].includes(l.status) : l.status === filter)));
  return <div className="content">
    <div className="page-heading"><div><p className="eyebrow">COMERCIAL</p><h1 className="title">Contatos e retornos</h1><p className="subtitle">Acompanhe as abordagens, registre respostas e organize o próximo contato.</p></div>
      <div className={styles.actions}><button className="btn" disabled={!ready || busy} onClick={() => importFile.current?.click()}>Importar relatório</button><button className="btn primary" disabled={!ready || busy} onClick={() => { eventKey.current = crypto.randomUUID(); setCreating(true); }}>Registrar contato</button></div></div>
    <input ref={importFile} type="file" accept="application/json,.json" hidden onChange={e => void importContacts(e.target.files?.[0])} />
    {error && <p role="alert" className={styles.error}>{error} <button className="btn" disabled={busy} onClick={() => void load()}>Recarregar</button></p>}
    {notice && <p role="status" className={styles.notice}>{notice}</p>}
    {login && <form className={`panel ${styles.login}`} onSubmit={e => void submit(e, "login")}><h2>Acessar sua organização</h2><label className="field">Organização<input name="organization_slug" required /></label><label className="field">E-mail<input name="email" type="email" autoComplete="username" required /></label><label className="field">Senha<input name="password" type="password" autoComplete="current-password" required /></label><button className="btn primary" disabled={busy}>Conectar</button></form>}
    <div className={styles.toolbar}><input aria-label="Buscar loja ou Instagram" placeholder="Buscar loja, Instagram ou cidade" value={query} onChange={e => setQuery(e.target.value)} /><select aria-label="Filtrar contatos" value={filter} onChange={e => setFilter(e.target.value)}><option value="todos">Todos os contatos</option><option value="hoje">Acompanhamento disponível</option>{Object.entries(labels).map(([v, label]) => <option key={v} value={v}>{label}</option>)}</select><span>{visible.length} contatos carregados</span></div>
    <p className={styles.hint}>O próximo contato é sugerido para sete dias após o envio. Você confere o Direct e registra o retorno aqui. Nenhuma mensagem é enviada automaticamente.</p>
    <div className={`panel ${styles.table}`}><table><thead><tr><th>Loja / Instagram</th><th>Último contato</th><th>Próximo contato</th><th>Situação</th><th>Histórico</th></tr></thead><tbody>{visible.map(l => <tr key={l.id}><td><strong>{l.name}</strong><a href={`https://www.instagram.com/${encodeURIComponent(l.instagram)}/`} target="_blank" rel="noopener noreferrer">@{l.instagram}</a><small>{l.city}</small></td><td>{date(l.last_contact_on)}</td><td>{date(l.next_contact_on)}{l.next_contact_on && l.next_contact_on <= today() && <small>Disponível para acompanhamento</small>}</td><td>{labels[l.status] ?? l.status}</td><td><button className="btn" disabled={busy} onClick={() => void selectLead(l)}>Ver / anotar retorno</button></td></tr>)}</tbody></table>{!visible.length && <p className={styles.empty}>{ready ? "Nenhum contato encontrado." : "Conecte o servidor para carregar os contatos."}</p>}</div>
    {more && <button className="btn" onClick={() => void load(offset + 100)}>Carregar mais contatos</button>}
    {creating && <div className="modal-backdrop"><form role="dialog" aria-modal="true" aria-label="Registrar contato" className="create-modal" onSubmit={e => void submit(e, "create")}><h2>Registrar contato realizado</h2><label className="field">Nome da loja<input name="name" maxLength={160} required /></label><label className="field">Instagram<input name="instagram" placeholder="@perfil ou link do Instagram" required /></label><label className="field">Cidade / UF<input name="city" maxLength={160} /></label><label className="field">Data do envio<input name="contacted_on" type="date" defaultValue={today()} max={today()} required /></label><label className="field">Observações<textarea name="note" maxLength={5000} /></label><p>O próximo contato será sugerido para sete dias depois.</p><div className="modal-actions"><button type="button" className="btn" disabled={busy} onClick={() => setCreating(false)}>Cancelar</button><button className="btn primary" disabled={busy}>Salvar contato</button></div></form></div>}
    {selected && <div className="modal-backdrop"><section role="dialog" aria-modal="true" aria-label={`Histórico de ${selected.name}`} className={`create-modal ${styles.history}`}><h2>{selected.name}</h2><p>@{selected.instagram}</p>{historyLoading ? <p>Carregando histórico…</p> : <ol>{history.map(a => <li key={a.id}><strong>{date(a.occurred_on)} · {a.kind === "retorno" ? "Retorno recebido" : a.kind === "contato" ? "Contato realizado" : "Anotação"}</strong><p>{a.note || "Sem observações."}</p></li>)}</ol>}<form onSubmit={e => void submit(e, "activity")}><label className="field">Registrar<select value={kind} onChange={e => setKind(e.target.value)}><option value="retorno">Retorno recebido</option><option value="contato">Novo contato realizado</option><option value="nota">Anotação</option></select></label><label className="field">Data<input type="date" name="occurred_on" defaultValue={today()} max={today()} required /></label>{kind === "retorno" && <label className="field">Resultado<select name="status" defaultValue="respondeu"><option value="respondeu">Respondeu / em conversa</option><option value="sem_interesse">Sem interesse / não contatar</option><option value="convertido">Convertido</option></select></label>}<label className="field">Retorno / observações<textarea name="note" maxLength={5000} required /></label><label className="field">Próximo acompanhamento (opcional)<input type="date" name="next_contact_on" min={today()} /></label><p className={styles.hint}>{kind === "retorno" ? "Registrar uma resposta remove o lembrete automático. Defina uma nova data se quiser acompanhar." : "Um novo envio para quem aguarda retorno sugere acompanhamento em sete dias."}</p><div className="modal-actions"><button className="btn" type="button" disabled={busy} onClick={() => { setSelected(null); ++historyRequest.current; }}>Fechar</button><button className="btn primary" disabled={busy || historyLoading}>Salvar registro</button></div></form></section></div>}
  </div>;
}
