"use client";
import { FormEvent, useCallback, useEffect, useState } from "react";
import styles from "./crm.module.css";

type Rule = { id: string; name: string; enabled: boolean; contains: string; reply: string; position: number; handoff: boolean; priority: string | null; status: string | null };
type Connection = { configured: boolean; bot_enabled: boolean; state: string };
async function request(path: string, body?: unknown) {
  const response = await fetch(`/api/crm/${path}`, { cache: "no-store", ...(body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {}) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message ?? "Falha ao acessar automações.");
  return data;
}
export function AutomationPanel() {
  const [rules, setRules] = useState<Rule[]>([]);
  const [connection, setConnection] = useState<Connection | null>(null);
  const [error, setError] = useState("");
  const [simulation, setSimulation] = useState<{ matched: boolean; name?: string; reply?: string; priority?: string; handoff?: boolean } | null>(null);
  const [qr, setQr] = useState("");
  const [busy, setBusy] = useState(false);
  const [editing, setEditing] = useState<Rule | null>(null);
  const [creating, setCreating] = useState(false);
  const load = useCallback(async () => {
    setError("");
    const results = await Promise.allSettled([request("automations"), request("evolution/status")]);
    if (results[0].status === "fulfilled") setRules(results[0].value);
    else setError(results[0].reason.message);
    if (results[1].status === "fulfilled") setConnection(results[1].value);
    else { setConnection(null); setError(results[1].reason.message); }
  }, []);
  useEffect(() => { void load(); }, [load]);
  async function simulate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    const form = new FormData(event.currentTarget);
    try { setSimulation(await request("automations/simulate", { text: form.get("text") })); }
    catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  async function connect() {
    setBusy(true); setError(""); setQr("");
    try {
      const data = await request("evolution/connect", {});
      if (typeof data.base64 === "string" && /^data:image\/png;base64,[A-Za-z0-9+/=]+$/.test(data.base64)) setQr(data.base64);
      else setError("QR indisponível. Verifique a conexão ou tente gerar novamente.");
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); if (busy) return;
    const form = new FormData(event.currentTarget);
    setBusy(true); setError("");
    try {
      await request(editing ? `automations/${editing.id}` : "automations", {
        name: form.get("name"), position: Number(form.get("position")), handoff: form.get("handoff") === "on", contains: form.get("contains"), reply: form.get("reply"),
        priority: form.get("priority") || null, status: form.get("status") || null,
        enabled: form.get("enabled") === "on",
      });
      setCreating(false); setEditing(null); await load();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  async function toggle(rule: Rule) {
    if (busy) return; setBusy(true); setError("");
    try { const { id, ...body } = rule; await request(`automations/${id}`, { ...body, enabled: !rule.enabled }); await load(); }
    catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  return <section className={`panel ${styles.automation}`}>
    <div className={styles.actions}><h2>WhatsApp e automações</h2><button className="btn" disabled={busy} onClick={() => void load()}>Verificar conexão</button><button className="btn primary" onClick={() => { setEditing(null); setCreating(true); }}>Criar fluxo</button></div>
    <p role="status">{connection ? connection.configured ? `Evolution: ${connection.state} · Bot ${connection.bot_enabled ? "habilitado" : "pausado no servidor"}` : "Evolution aguardando instalação e configuração no servidor." : "Conexão ainda não confirmada."}</p>
    {connection?.configured && connection.state !== "open" && <button className="btn" disabled={busy} onClick={() => void connect()}>Conectar WhatsApp por QR</button>}
    {qr && <div><p>No WhatsApp, abra Aparelhos conectados → Conectar aparelho. Depois verifique a conexão acima.</p>{/* QR is a data URL returned by the authenticated backend. */}<img src={qr} alt="QR para conectar o WhatsApp ao CRM" width={240} height={240} /></div>}
    <p className={styles.hint}>Mensagem recebida → condição → prioridade / situação → resposta. Os fluxos seguem a ordem definida. Novos contatos recebidos pelo WhatsApp entram automaticamente no Kanban. Contatos sem interesse ou convertidos não recebem respostas automáticas.</p>
    {error && <p role="alert" className={styles.error}>{error}</p>}
    <form className={styles.flow} onSubmit={e => void simulate(e)}><h3>Testar conversa</h3><label className="field">Mensagem de teste<input name="text" placeholder="Ex.: quero um orçamento" maxLength={10000} required /></label><button className="btn" disabled={busy}>Simular fluxo</button><p className={styles.hint}>A simulação mostra o resultado sem enviar mensagens ou alterar contatos.</p>{simulation && <div role="status">{simulation.matched ? <><strong>{simulation.name}</strong><p>Prioridade: {simulation.priority ?? "manter"} · {simulation.handoff ? "encaminhar para humano" : "continuar com bot"}</p><p>{simulation.reply || "Sem resposta automática."}</p></> : <p>Nenhum fluxo ativo corresponde à mensagem.</p>}</div>}</form>
    {rules.length === 0 && <p>Nenhum fluxo cadastrado.</p>}
    {rules.map(rule => <article className={styles.flow} key={rule.id}><strong>{rule.name}</strong><span>{rule.enabled ? "Ativo" : "Pausado"}</span><p>Ordem {rule.position} · Receber mensagem → {rule.contains ? `contém “${rule.contains}”` : "qualquer texto"} → {rule.priority ? `prioridade ${rule.priority}` : "manter prioridade"} → {rule.reply ? "enviar resposta" : "atualizar contato"}{rule.handoff ? " → atendimento humano" : ""}</p><button className="btn" disabled={busy} onClick={() => { setEditing(rule); setCreating(true); }}>Editar</button> <button className="btn" disabled={busy} onClick={() => void toggle(rule)}>{rule.enabled ? "Pausar" : "Ativar"}</button></article>)}
    {creating && <form key={editing?.id ?? "new"} className={styles.flow} onSubmit={e => void save(e)}><h3>{editing ? "Editar fluxo" : "Novo fluxo"}</h3><label className="field">Nome<input name="name" defaultValue={editing?.name} maxLength={120} required /></label><label className="field">Ordem de execução<input name="position" type="number" min={0} max={10000} defaultValue={editing?.position ?? 100} required /></label><label className="field">Quando a mensagem contiver<input name="contains" defaultValue={editing?.contains} maxLength={200} placeholder="Ex.: orçamento|preço|1 (vazio = qualquer texto)" /></label><label className="field">Definir prioridade<select name="priority" defaultValue={editing?.priority ?? ""}><option value="">Manter prioridade</option><option value="baixa">Baixa</option><option value="media">Média</option><option value="alta">Alta</option><option value="urgente">Urgente</option></select></label><label className="field">Definir situação<select name="status" defaultValue={editing?.status ?? ""}><option value="">Respondeu</option><option value="aguardando">Aguardando retorno</option><option value="respondeu">Respondeu</option><option value="sem_interesse">Sem interesse</option><option value="convertido">Convertido</option></select></label><label className="field">Resposta do bot<textarea name="reply" defaultValue={editing?.reply} maxLength={4000} placeholder="Deixe vazio para apenas atualizar o contato" /></label><label><input type="checkbox" name="handoff" defaultChecked={editing?.handoff ?? false} /> Encaminhar para humano e pausar o bot neste contato</label><br /><label><input type="checkbox" name="enabled" defaultChecked={editing?.enabled ?? false} /> Ativar fluxo</label><div className={styles.actions}><button type="button" className="btn" disabled={busy} onClick={() => setCreating(false)}>Cancelar</button><button className="btn primary" disabled={busy}>Salvar fluxo</button></div></form>}
  </section>;
}
