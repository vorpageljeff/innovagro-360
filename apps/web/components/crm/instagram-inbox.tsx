"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { ExternalLink, Instagram } from "lucide-react";
import styles from "./whatsapp-leads.module.css";

type Lead = { id: string; name: string; instagram: string; city: string; status: string; priority: string; sent_count: number; received_count: number; can_message: boolean };
type Message = { id: string; direction: "incoming" | "outgoing"; text: string; at: string; source?: "manual" | "webhook" };

async function request(path: string, body?: unknown) {
  const response = await fetch(`/api/crm/${path}`, { cache: "no-store", ...(body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {}) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message ?? "Não foi possível consultar o Instagram.");
  return data;
}

export function InstagramInbox() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [template, setTemplate] = useState("");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Lead | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const [requestId, setRequestId] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = useCallback(async () => {
    setLoading(true); setError("");
    try { const data = await request(`instagram/leads?q=${encodeURIComponent(query)}`); setLeads(data.items); setTemplate(data.template); }
    catch (e) { setError((e as Error).message); }
    finally { setLoading(false); }
  }, [query]);

  useEffect(() => { const timer = setTimeout(() => void load(), 250); return () => clearTimeout(timer); }, [load]);
  useEffect(() => {
    if (!selected) return;
    setError(""); setNotice(""); setText(template.replaceAll("{empresa}", selected.name)); setRequestId(crypto.randomUUID());
    const refresh = () => void request(`instagram/leads/${selected.id}/conversation`).then(data => setMessages(data.messages)).catch(e => setError((e as Error).message));
    refresh(); const timer = setInterval(refresh, 5000); return () => clearInterval(timer);
  }, [selected, template]);
  useEffect(() => { const timer = setInterval(() => void load(), 10000); return () => clearInterval(timer); }, [load]);

  const sentTotal = useMemo(() => leads.reduce((total, lead) => total + lead.sent_count, 0), [leads]);
  async function recordSent() {
    if (!selected || !text.trim() || busy) return;
    setBusy(true); setError(""); setNotice("");
    try {
      await request(`instagram/leads/${selected.id}/sent`, { request_id: requestId, expected_instagram: selected.instagram, text });
      const conversation = await request(`instagram/leads/${selected.id}/conversation`);
      setMessages(conversation.messages); setNotice("Envio confirmado e registrado no CRM."); setText(""); setRequestId(crypto.randomUUID()); await load();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }

  return <>
    <div className="page-heading"><div><p className="eyebrow">COMERCIAL</p><h1 className="title">Instagram</h1><p className="subtitle">Prepare abordagens, abra o perfil correto e acompanhe os envios registrados.</p></div></div>
    <section className={`panel ${styles.panel}`}>
      <div className={styles.metrics}><span><strong>{leads.length}</strong> perfis disponíveis</span><span><strong>{sentTotal}</strong> envios registrados</span></div>
      <label className="field">Buscar por empresa, cidade ou perfil<input value={query} maxLength={160} placeholder="Digite para filtrar" onChange={e => setQuery(e.target.value)} /></label>
      {error && <p role="alert" className={styles.error}>{error}</p>}{notice && <p role="status">{notice}</p>}
      {loading ? <p>Carregando perfis…</p> : <div className={`${styles.inbox} ${selected ? styles.chatOpen : ""}`}>
        <aside className={styles.contactList} aria-label="Perfis do Instagram"><div className={styles.listHeading}><strong>Perfis</strong><span>{leads.length}</span></div>
          {leads.map(lead => <button key={lead.id} className={`${styles.contact} ${selected?.id === lead.id ? styles.activeContact : ""}`} onClick={() => setSelected(lead)}>
            <span className={styles.avatar}><Instagram size={17} /></span><span className={styles.contactInfo}><strong>{lead.name}</strong><small>@{lead.instagram} · {lead.city}</small><span className={styles.preview}>{lead.received_count ? `${lead.received_count} mensagem(ns) recebida(s)` : lead.sent_count ? `${lead.sent_count} envio(s) registrado(s)` : "Ainda não abordado pelo Instagram"}</span></span>
          </button>)}
        </aside>
        <div className={styles.chatPane}>{!selected ? <div className={styles.chatPlaceholder}><h3>Envios pelo Instagram</h3><p>Escolha um perfil para preparar e acompanhar a abordagem.</p></div> : <div className={styles.chatContent}>
          <div className={styles.heading}><div><h2>{selected.name}</h2><p>@{selected.instagram} · {selected.city}</p></div><button className="btn" onClick={() => setSelected(null)}>Voltar à lista</button></div>
          <div className={styles.actions}><a className="btn" href={`https://www.instagram.com/${selected.instagram}/`} target="_blank" rel="noreferrer">Abrir perfil <ExternalLink size={14} /></a></div>
          <div className={styles.chatHistory} aria-label="Conversa do Instagram">{messages.length ? messages.map(message => <article key={message.id} className={`${styles.bubble} ${message.direction === "outgoing" ? styles.outgoing : ""}`}><small>{message.direction === "outgoing" ? "Voragon" : selected.name} · Instagram</small><p>{message.text}</p><small>{new Date(message.at).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo" })}</small></article>) : <p className={styles.empty}>Ainda não há mensagens para este perfil.</p>}</div>
          <label className="field">Mensagem<textarea rows={5} maxLength={1500} value={text} disabled={busy || !selected.can_message} onChange={e => setText(e.target.value)} /></label>
          <div className={styles.actions}><button className="btn" disabled={busy} onClick={() => setText(template.replaceAll("{empresa}", selected.name))}>Usar mensagem padrão</button><button className="btn primary" disabled={busy || !text.trim() || !selected.can_message} onClick={() => void recordSent()}>{busy ? "Registrando…" : "Confirmar que enviei no Instagram"}</button></div>
          <p className={styles.hint}>As respostas recebidas aparecem automaticamente nesta conversa. Para uma nova abordagem manual, abra o perfil e confirme aqui somente depois que o envio aparecer no Instagram.</p>
        </div>}</div>
      </div>}
    </section>
  </>;
}
