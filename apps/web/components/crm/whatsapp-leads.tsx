"use client";

import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import styles from "./whatsapp-leads.module.css";

type Lead = { id: string; name: string; instagram: string | null; city: string; status: string; priority: string; phone: string | null; can_message: boolean; blocked_reason: string | null };
type Result = { items: Lead[]; total: number; offset: number; limit: number; summary: { all: number; ready: number; missing_phone: number } };
type Draft = { text: string; request_id: string; state: string | null };
type Inbox = { items: { lead_id: string; unread: number; last_incoming: string | null; last_incoming_at: string | null }[]; unread: number; unread_contacts: number };
type Conversation = { lead_id: string; read_ids: string[]; messages: { id: string; direction: string; text: string; at: string; state: string }[]; bot_paused: boolean; status: string; source: string; warning: string };
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
  const [draft, setDraft] = useState<Draft | null>(null);
  const [template, setTemplate] = useState("");
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messageLoading, setMessageLoading] = useState(false);
  const [chatError, setChatError] = useState("");
  const [messageNotice, setMessageNotice] = useState("");
  const [templateBusy, setTemplateBusy] = useState(false);
  const sendLock = useRef(false);
  const chatEnd = useRef<HTMLDivElement | null>(null);
  const [busy, setBusy] = useState(false);
  const phoneDialog = useRef<HTMLDialogElement | null>(null);
  const [inbox, setInbox] = useState<Inbox | null>(null);
  const inboxCount = useRef<number | null>(null);
  const readKeys = useRef(new Set<string>());
  const controller = useRef<AbortController | null>(null);
  const load = useCallback(async () => {
    controller.current?.abort();
    const abort = new AbortController(); controller.current = abort;
    setError("");
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

  useEffect(() => {
    const abort = new AbortController();
    void request("evolution/message-template", abort.signal).then(data => setTemplate(data.text)).catch(e => { if (!abort.signal.aborted) setError((e as Error).message); });
    return () => abort.abort();
  }, []);
  const refreshInbox = useCallback(async () => {
    const next: Inbox = await request("evolution/inbox");
    if (inboxCount.current !== null && next.unread > inboxCount.current) setNotice("Nova resposta recebida. Confira as conversas com o contador verde.");
    inboxCount.current = next.unread; setInbox(next);
  }, []);
  useEffect(() => {
    let active = true, running = false;
    const refresh = async () => {
      if (!active || running || document.hidden) return;
      running = true;
      try { await refreshInbox(); } catch (e) { if (active) setError((e as Error).message); }
      finally { running = false; }
    };
    void refresh(); const timer = setInterval(() => { void refresh(); void load(); }, 10000);
    document.addEventListener("visibilitychange", refresh);
    return () => { active = false; clearInterval(timer); document.removeEventListener("visibilitychange", refresh); };
  }, [refreshInbox, load]);
  const composingId = composing?.id;
  useEffect(() => {
    if (!conversation || conversation.lead_id !== composingId || document.hidden || messageLoading) return;
    const ids = conversation.read_ids.filter(id => !readKeys.current.has(id));
    if (!ids.length) return;
    const abort = new AbortController();
    const frame = requestAnimationFrame(() => {
      void request(`evolution/leads/${composingId}/read`, abort.signal, { receipt_ids: ids })
        .then(() => { ids.forEach(id => readKeys.current.add(id)); return refreshInbox(); })
        .catch(e => { if (!abort.signal.aborted) setChatError("Não foi possível marcar como lida: " + (e as Error).message); });
    });
    return () => { cancelAnimationFrame(frame); abort.abort(); };
  }, [conversation, composingId, messageLoading, refreshInbox]);
  async function openChat(lead: Lead) {
    if (busy || composing?.id === lead.id) return;
    if (composing && draft && !draft.state && draft.text.trim()) {
      setBusy(true);
      try { await request(`evolution/leads/${composing.id}/draft`, undefined, { text: draft.text, request_id: draft.request_id }); }
      catch (e) { setChatError("Salve o rascunho antes de trocar de conversa: " + (e as Error).message); return; }
      finally { setBusy(false); }
    }
    setComposing(lead);
  }
  useEffect(() => {
    if (!composingId) return;
    const abort = new AbortController();
    setDraft(null); setConversation(null); setChatError(""); setMessageNotice(""); setMessageLoading(true);
    void Promise.all([request(`evolution/leads/${composingId}/draft`, abort.signal), request(`evolution/leads/${composingId}/conversation`, abort.signal)])
      .then(([nextDraft, chat]) => { if (!abort.signal.aborted) { setDraft(nextDraft); setConversation(chat); } })
      .catch(e => { if (!abort.signal.aborted) setChatError((e as Error).message); })
      .finally(() => { if (!abort.signal.aborted) setMessageLoading(false); });
    let refreshing = false;
    const interval = setInterval(() => {
      if (document.visibilityState !== "visible" || refreshing) return;
      refreshing = true;
      void request(`evolution/leads/${composingId}/conversation`, abort.signal).then(chat => { if (!abort.signal.aborted) setConversation(chat); }).catch(e => { if (!abort.signal.aborted) setChatError((e as Error).message); }).finally(() => { refreshing = false; });
    }, 5000);
    return () => { abort.abort(); clearInterval(interval); };
  }, [composingId]);
  const messageCount = conversation?.messages.length;
  useEffect(() => { chatEnd.current?.scrollIntoView({ block: "nearest" }); }, [messageCount]);
  async function saveTemplate() {
    if (!template.trim() || templateBusy) return;
    setTemplateBusy(true); setError("");
    try { await request("evolution/message-template", undefined, { text: template }); setNotice("Mensagem padrão salva no servidor."); }
    catch (e) { setError((e as Error).message); }
    finally { setTemplateBusy(false); }
  }
  async function saveMessage() {
    if (!composing || !draft || busy) return;
    setBusy(true); setChatError("");
    try { setDraft(await request(`evolution/leads/${composing.id}/draft`, undefined, { text: draft.text, request_id: draft.request_id })); setMessageNotice("Rascunho salvo no CRM."); }
    catch (e) { setChatError((e as Error).message); }
    finally { setBusy(false); }
  }
  async function sendMessage() {
    if (!composing || !draft || !draft.text.trim() || sendLock.current) return;
    sendLock.current = true; setBusy(true); setChatError(""); setMessageNotice("");
    try {
      const result = await request(`evolution/leads/${composing.id}/send`, undefined, { text: draft.text, request_id: draft.request_id, expected_phone: composing.phone });
      setDraft(old => old ? { ...old, state: result.state } : old);
      setMessageNotice(result.state === "sent" ? "Mensagem enviada pelo número empresarial e registrada no histórico." : "Envio sem confirmação. Confira no WhatsApp empresarial antes de preparar outro envio.");
      setConversation(await request(`evolution/leads/${composing.id}/conversation`));
      await load();
    } catch (e) { setChatError((e as Error).message + " Se o envio ficou sem confirmação, consulte o resultado usando o mesmo botão."); }
    finally { sendLock.current = false; setBusy(false); }
  }
  async function takeOver() {
    if (!composing || busy) return;
    setBusy(true); setChatError("");
    try { await request(`leads/${composing.id}/settings`, undefined, { bot_paused: true }); setConversation(old => old ? { ...old, bot_paused: true } : old); setMessageNotice("Bot pausado. Você pode continuar pelo campo abaixo."); }
    catch (e) { setChatError((e as Error).message); }
    finally { setBusy(false); }
  }
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
  const rows = (data?.items ?? []).slice().sort((a,b) => {
    const ai = inbox?.items.find(x => x.lead_id === a.id), bi = inbox?.items.find(x => x.lead_id === b.id);
    return Number(!!bi?.unread) - Number(!!ai?.unread) || (bi?.last_incoming_at ?? "").localeCompare(ai?.last_incoming_at ?? "");
  });
  const ready = rows.filter(row => row.can_message);
  const selection = Object.values(selected);
  const allSelected = ready.length > 0 && ready.every(row => selected[row.id]);
  const text = draft?.text ?? "";
  return <section className={`panel ${styles.panel}`}>
    <div className={styles.heading}><div><h2>Leads para contato</h2><p>Respostas novas aparecem com um contador. Clique no contato para abrir o chat.</p></div><button className="btn" disabled={loading} onClick={() => void load()}>Atualizar lista</button></div>
    <details className={styles.template}><summary>Mensagem padrão e personalização</summary><div><label className="field">Mensagem padrão<textarea rows={4} value={template} maxLength={1500} placeholder="Escreva a mensagem padrão. Use {empresa} para inserir o nome do lead." onChange={e => setTemplate(e.target.value)} /></label><div className={styles.actions}><button className="btn" disabled={templateBusy || !template.trim()} onClick={() => void saveTemplate()}>{templateBusy ? "Salvando…" : "Salvar mensagem padrão"}</button><small>Use {"{empresa}"} para personalizar o nome. Você revisa o texto antes de cada envio.</small></div></div></details>
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
      <div className={`${styles.inbox} ${composing ? styles.chatOpen : ""}`}>
        <aside className={styles.contactList} aria-label="Lista de conversas">
          <div className={styles.listHeading}><strong>Conversas</strong><span className={styles.badge}>{inbox?.unread ?? 0} não lidas</span></div>
          {rows.map(lead => {
            const item = inbox?.items.find(x => x.lead_id === lead.id);
            return <button key={lead.id} className={`${styles.contact} ${composing?.id === lead.id ? styles.activeContact : ""}`} disabled={busy} onClick={() => void openChat(lead)} aria-label={`Abrir conversa com ${lead.name}${item?.unread ? `, ${item.unread} mensagens não lidas` : ""}`} aria-pressed={composing?.id === lead.id}>
              <span className={styles.avatar}>{lead.name.slice(0,1).toUpperCase()}</span>
              <span className={styles.contactInfo}><strong>{lead.name}</strong><small>{lead.phone ?? "Sem telefone"} · {priorities[lead.priority]}</small><span className={styles.preview}>{item?.last_incoming ?? lead.city ?? "Nenhuma resposta ainda"}</span></span>
              {!!item?.unread && <span className={styles.badge}>{item.unread}</span>}
            </button>;
          })}
        </aside>
        <div className={styles.chatPane}>
          {!composing && <div className={styles.chatPlaceholder}><h3>Sua caixa de entrada</h3><p>Selecione um contato para ver a conversa e enviar uma mensagem.</p><strong>{inbox?.unread ?? 0} mensagens não lidas em {inbox?.unread_contacts ?? 0} conversas</strong></div>}
          {composing && <div className={styles.chatContent}>
      <div className={styles.heading}><div><h2 id="message-title">Conversa com {composing.name}</h2><p>{composing.phone} · Empresarial: (45) 99103-8233</p></div><button className="btn" disabled={busy} onClick={() => setComposing(null)}>Voltar à lista</button></div>
      <div className={styles.actions}><button className="btn" disabled={busy} onClick={() => setEditing(composing)}>{composing.phone ? "Editar telefone" : "Cadastrar telefone"}</button><span>{conversation?.bot_paused ? "Atendimento humano · bot pausado" : "Atendimento com IA"}</span><button className="btn" disabled={busy || !conversation || conversation.bot_paused} onClick={() => void takeOver()}>{conversation?.bot_paused ? "Atendimento com você" : "Assumir atendimento"}</button></div>
      {conversation?.warning && <p role="status" className={styles.hint}>{conversation.warning}</p>}
      <div className={styles.chatHistory} aria-label="Histórico da conversa">{messageLoading ? <p>Carregando conversa…</p> : conversation?.messages.length ? conversation.messages.map(message => <article key={message.id} className={`${styles.bubble} ${message.direction === "outgoing" ? styles.outgoing : ""}`}><small>{message.direction === "outgoing" ? "Voragon" : composing.name}</small><p>{message.text}</p><small>{new Date(message.at).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo" })}{message.state === "uncertain" ? " · Sem confirmação" : message.state === "sending" ? " · Envio em andamento" : ""}</small></article>) : <p className={styles.empty}>Ainda não há mensagens nesta conversa.</p>}<div ref={chatEnd} /></div>
      {chatError && <p role="alert" className={styles.error}>{chatError}</p>}{messageNotice && <p role="status">{messageNotice}</p>}
      <label className="field">Mensagem<textarea value={text} rows={4} maxLength={1500} disabled={busy || !draft || !!draft.state} placeholder="Revise a mensagem para este contato" onChange={e => setDraft(old => old ? { ...old, text: e.target.value } : old)} /></label>
      <div className={styles.actions}>
        {draft?.state ? <button className="btn" disabled={busy || draft.state !== "sent"} onClick={() => { setDraft(old => old ? { ...old, request_id: crypto.randomUUID(), state: null, text: "" } : old); setMessageNotice(""); }}>Preparar nova mensagem</button> : <><button className="btn" disabled={busy || !draft || !template.trim()} onClick={() => setDraft(old => old ? { ...old, text: template.replaceAll("{empresa}", composing.name) } : old)}>Usar mensagem padrão</button><button className="btn" disabled={busy || !draft || !text.trim()} onClick={() => void saveMessage()}>Salvar rascunho</button></>}
        <button className="btn primary" disabled={busy || !draft || !text.trim() || draft.state === "sent" || !composing.can_message || ["sem_interesse", "convertido"].includes(conversation?.status ?? "")} onClick={() => void sendMessage()}>{busy ? "Aguarde…" : draft?.state ? "Consultar resultado do envio" : "Enviar pelo empresarial"}</button>
      </div>
      <p className={styles.hint}>Atualiza a conversa a cada 5 segundos. Envios sem confirmação não são repetidos automaticamente.</p>

          </div>}
        </div>
      </div>
      {!rows.length && <p className={styles.empty}>Nenhum lead encontrado com estes filtros.</p>}
      <div className={styles.pagination}><span>{data.total ? `${offset + 1}–${Math.min(offset + rows.length, data.total)} de ${data.total}` : "0 leads"}</span><button className="btn" disabled={offset === 0} onClick={() => { setOffset(Math.max(0, offset - 25)); setData(null); }}>Anterior</button><button className="btn" disabled={offset + 25 >= data.total} onClick={() => { setOffset(offset + 25); setData(null); }}>Próxima</button></div>
    </>}
    {!!selection.length && <div className={styles.selection}><div className={styles.heading}><h3>{selection.length} contatos selecionados</h3><button className="btn" onClick={() => setSelected({})}>Limpar seleção</button></div>{selection.map(lead => <div key={lead.id} className={styles.selectedRow}><span>{lead.name} <small>{lead.phone}</small></span><button className="btn" onClick={() => setComposing(lead)}>Abrir conversa</button><button className="btn" aria-label={`Remover ${lead.name} da seleção`} onClick={() => toggle(lead)}>Remover</button></div>)}</div>}
    <p className={styles.hint}>O envio usa o WhatsApp empresarial conectado. Abrir a conversa ou salvar um rascunho não envia mensagens. A IA responde até três vezes; assumir atendimento pausa o bot.</p>
    {editing && <dialog className={styles.dialog} ref={phoneDialog} aria-labelledby="phone-title" onCancel={event => { if (busy) event.preventDefault(); else setEditing(null); }} onClose={() => setEditing(null)}><form onSubmit={e => void savePhone(e)}><h2 id="phone-title">Telefone de {editing.name}</h2><label className="field">WhatsApp com código do país e DDD<input name="phone" type="tel" defaultValue={editing.phone ?? ""} placeholder="55 + DDD + número" maxLength={25} required /></label><p className={styles.hint}>O telefone será salvo no contato existente, preservando seu histórico.</p>{error && <p role="alert" className={styles.error}>{error}</p>}<div className={styles.actions}><button type="button" className="btn" disabled={busy} onClick={() => setEditing(null)}>Cancelar</button><button className="btn primary" disabled={busy}>Salvar telefone</button></div></form></dialog>}


  </section>;
}
