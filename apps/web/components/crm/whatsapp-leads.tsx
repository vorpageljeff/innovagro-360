"use client";

import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import styles from "./whatsapp-leads.module.css";

type Lead = { id: string; name: string; instagram: string | null; city: string; status: string; priority: string; phone: string | null; can_message: boolean; blocked_reason: string | null };
type Result = { items: Lead[]; total: number; offset: number; limit: number; summary: { all: number; ready: number; missing_phone: number } };
const priorities: Record<string, string> = { baixa: "Baixa", media: "Média", alta: "Alta", urgente: "Urgente" };
const statuses: Record<string, string> = { aguardando: "Aguardando", respondeu: "Respondeu", sem_interesse: "Sem interesse", convertido: "Convertido" };
async function request(path: string, signal?: AbortSignal, body?: unknown) {
  const response = await fetch(`/api/crm/${path}`, { cache: "no-store", signal, ...(body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {}) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message ?? "Não foi possível consultar os leads.");
  return data;
}

export function WhatsAppLeads() {
  const [q, setQ] = useState("");
  const [audience, setAudience] = useState("all");
  const [priority, setPriority] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [data, setData] = useState<Result | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [selected, setSelected] = useState<Record<string, Lead>>({});
  const [editing, setEditing] = useState<Lead | null>(null);
  const [composing, setComposing] = useState<Lead | null>(null);
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);
  const phoneDialog = useRef<HTMLDialogElement | null>(null);
  const messageDialog = useRef<HTMLDialogElement | null>(null);
  const controller = useRef<AbortController | null>(null);
  const load = useCallback(async () => {
    controller.current?.abort();
    const abort = new AbortController(); controller.current = abort;
    setLoading(true); setError("");
    const params = new URLSearchParams({ q, audience, offset: String(offset), limit: "25" });
    if (priority) params.set("priority", priority);
    if (status) params.set("status", status);
    try {
      const result: Result = await request(`evolution/leads?${params}`, abort.signal);
      if (abort.signal.aborted) return;
      setData(result);
      setSelected(old => {
        const next = { ...old };
        for (const row of result.items) {
          if (next[row.id]) { if (row.can_message) next[row.id] = row; else delete next[row.id]; }
        }
        return next;
      });
    } catch (e) { if (!abort.signal.aborted) { setError((e as Error).message); setData(null); } }
    finally { if (!abort.signal.aborted) setLoading(false); }
  }, [q, audience, priority, status, offset]);
  useEffect(() => { const timer = setTimeout(() => void load(), 250); return () => { clearTimeout(timer); controller.current?.abort(); }; }, [load]);
  useEffect(() => { if (editing && phoneDialog.current && !phoneDialog.current.open) phoneDialog.current.showModal(); }, [editing]);
  useEffect(() => { if (composing && messageDialog.current && !messageDialog.current.open) messageDialog.current.showModal(); }, [composing]);
  function toggle(lead: Lead) {
    if (!lead.can_message) return;
    setSelected(old => { const next = { ...old }; if (next[lead.id]) delete next[lead.id]; else next[lead.id] = lead; return next; });
  }
  async function savePhone(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); if (!editing || busy) return;
    const phone = new FormData(event.currentTarget).get("phone");
    setBusy(true); setError("");
    try {
      await request(`leads/${editing.id}/settings`, undefined, { phone });
      setEditing(null); setNotice("Telefone salvo no CRM."); await load();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  const rows = data?.items ?? [];
  const ready = rows.filter(row => row.can_message);
  const selection = Object.values(selected);
  const allSelected = ready.length > 0 && ready.every(row => selected[row.id]);
  const text = composing ? drafts[composing.id] ?? "" : "";
  return <section className={`panel ${styles.panel}`}>
    <div className={styles.heading}><div><h2>Leads para contato</h2><p>Selecione contatos e prepare uma mensagem individual para revisar e enviar no WhatsApp.</p></div><button className="btn" disabled={loading} onClick={() => void load()}>Atualizar lista</button></div>
    <div className={styles.metrics}><span><strong>{data?.summary.all ?? "—"}</strong> leads nos filtros</span><span><strong>{data?.summary.ready ?? "—"}</strong> com telefone disponível</span><span><strong>{data?.summary.missing_phone ?? "—"}</strong> sem telefone</span></div>
    <div className={styles.filters}>
      <label className="field">Buscar lead<input value={q} maxLength={160} placeholder="Nome, cidade, Instagram ou telefone" onChange={e => { setQ(e.target.value); setOffset(0); setData(null); }} /></label>
      <label className="field">Lista<select value={audience} onChange={e => { setAudience(e.target.value); setOffset(0); setData(null); }}><option value="all">Todos os leads</option><option value="ready">Com telefone disponível</option><option value="missing_phone">Sem telefone</option></select></label>
      <label className="field">Prioridade<select value={priority} onChange={e => { setPriority(e.target.value); setOffset(0); setData(null); }}><option value="">Todas</option>{Object.entries(priorities).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
      <label className="field">Situação<select value={status} onChange={e => { setStatus(e.target.value); setOffset(0); setData(null); }}><option value="">Todas</option>{Object.entries(statuses).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
    </div>
    {error && !editing && <p role="alert" className={styles.error}>{error}</p>}
    {notice && <p role="status">{notice}</p>}
    {loading ? <p role="status">Carregando leads…</p> : data && <>
      <div className={styles.tableWrap}><table><thead><tr><th><input type="checkbox" aria-label="Selecionar contatos disponíveis nesta página" disabled={!ready.length} checked={allSelected} onChange={() => setSelected(old => { const next = { ...old }; ready.forEach(row => { if (allSelected) delete next[row.id]; else next[row.id] = row; }); return next; })} /></th><th>Lead</th><th>Telefone</th><th>Prioridade</th><th>Situação</th><th>Contato</th><th>Ações</th></tr></thead><tbody>{rows.map(lead => <tr key={lead.id}>
        <td><input type="checkbox" aria-label={`Selecionar ${lead.name}`} checked={!!selected[lead.id]} disabled={!lead.can_message} onChange={() => toggle(lead)} /></td>
        <td><strong>{lead.name}</strong><small>{[lead.city, lead.instagram ? `@${lead.instagram}` : ""].filter(Boolean).join(" · ") || "Contato WhatsApp"}</small></td>
        <td>{lead.phone ?? "Não cadastrado"}</td><td>{priorities[lead.priority]}</td><td>{statuses[lead.status]}</td><td><span className={lead.can_message ? styles.available : styles.blocked}>{lead.blocked_reason ?? "Telefone disponível"}</span></td>
        <td><div className={styles.actions}><button className="btn" onClick={() => { setError(""); setEditing(lead); }}>{lead.phone ? "Editar telefone" : "Cadastrar telefone"}</button><button className="btn" disabled={!lead.can_message} onClick={() => setComposing(lead)}>Preparar mensagem</button></div></td>
      </tr>)}</tbody></table></div>
      {!rows.length && <p className={styles.empty}>Nenhum lead encontrado com estes filtros.</p>}
      <div className={styles.pagination}><span>{data.total ? `${offset + 1}–${Math.min(offset + rows.length, data.total)} de ${data.total}` : "0 leads"}</span><button className="btn" disabled={offset === 0} onClick={() => { setOffset(Math.max(0, offset - 25)); setData(null); }}>Anterior</button><button className="btn" disabled={offset + 25 >= data.total} onClick={() => { setOffset(offset + 25); setData(null); }}>Próxima</button></div>
    </>}
    {!!selection.length && <div className={styles.selection}><div className={styles.heading}><h3>{selection.length} contatos selecionados</h3><button className="btn" onClick={() => setSelected({})}>Limpar seleção</button></div>{selection.map(lead => <div key={lead.id} className={styles.selectedRow}><span>{lead.name} <small>{lead.phone}</small></span><button className="btn" onClick={() => setComposing(lead)}>Preparar mensagem</button><button className="btn" aria-label={`Remover ${lead.name} da seleção`} onClick={() => toggle(lead)}>Remover</button></div>)}</div>}
    <p className={styles.hint}>Telefone cadastrado não confirma que a conta usa WhatsApp. O bot continua com a configuração atual; abrir uma conversa não envia nem registra uma mensagem automaticamente.</p>
    {editing && <dialog className={styles.dialog} ref={phoneDialog} aria-labelledby="phone-title" onCancel={event => { if (busy) event.preventDefault(); else setEditing(null); }} onClose={() => setEditing(null)}><form onSubmit={e => void savePhone(e)}><h2 id="phone-title">Telefone de {editing.name}</h2><label className="field">WhatsApp com código do país e DDD<input name="phone" type="tel" defaultValue={editing.phone ?? ""} placeholder="55 + DDD + número" maxLength={25} required /></label><p className={styles.hint}>O telefone será salvo no contato existente, preservando seu histórico.</p>{error && <p role="alert" className={styles.error}>{error}</p>}<div className={styles.actions}><button type="button" className="btn" disabled={busy} onClick={() => setEditing(null)}>Cancelar</button><button className="btn primary" disabled={busy}>Salvar telefone</button></div></form></dialog>}
    {composing && <dialog className={styles.dialog} ref={messageDialog} aria-labelledby="message-title" onCancel={() => setComposing(null)} onClose={() => setComposing(null)}><h2 id="message-title">Mensagem para {composing.name}</h2><p>{composing.phone}</p><label className="field">Mensagem individual<textarea value={text} rows={6} maxLength={1500} placeholder="Escreva sua mensagem para este contato" onChange={e => setDrafts(old => ({ ...old, [composing.id]: e.target.value }))} /></label><p className={styles.hint}>A conversa abre com o texto preenchido. Revise o destinatário e confirme o envio no seu WhatsApp.</p><div className={styles.actions}><button className="btn" onClick={() => setComposing(null)}>Fechar</button>{text.trim() && composing.can_message && composing.phone ? <a className="btn primary" href={`https://wa.me/${composing.phone}?text=${encodeURIComponent(text.trim())}`} target="_blank" rel="noopener noreferrer">Abrir conversa no WhatsApp</a> : <button className="btn primary" disabled>Escreva a mensagem</button>}</div></dialog>}
  </section>;
}
