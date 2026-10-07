"use client";

import { useEffect, useState } from "react";

type Status = { configured: boolean; enabled: boolean; bot_enabled: boolean; missing: string[]; model: string; daily_limit: number };

export function WhatsAppAIPanel() {
  const [status, setStatus] = useState<Status | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    const abort = new AbortController();
    void fetch("/api/crm/evolution/ai/status", { cache: "no-store", signal: abort.signal })
      .then(async response => { const data = await response.json(); if (!response.ok) throw new Error(data.message ?? "Não foi possível consultar a IA."); return data; })
      .then(data => { if (!abort.signal.aborted) setStatus(data); })
      .catch(e => { if (!abort.signal.aborted) setError(e.message); });
    return () => abort.abort();
  }, []);
  return <section className="panel" style={{ padding: 24, marginBottom: 20 }}>
    <h2>Assistente com IA</h2>
    <p>Conversa em linguagem natural, com o histórico do contato e as informações da sua empresa. Pedidos de atendimento humano e encerramento continuam seguindo seus fluxos.</p>
    {error ? <p role="alert">{error}</p> : !status ? <p>Consultando configuração…</p> : <>
      <p><strong>{!status.configured ? "Configuração pendente" : !status.enabled ? "IA desabilitada" : !status.bot_enabled ? "IA preparada · envio pausado" : "IA habilitada"}</strong></p>
      {!!status.missing.length && <p>Falta configurar: {status.missing.join(", ")}.</p>}
      {status.model && <p>Modelo: {status.model}</p>}
      <p>Limite: até {status.daily_limit} mensagens processadas a cada 24 horas. Se a IA falhar ou atingir o limite, o contato entra na fila de atendimento humano.</p>
      {!status.bot_enabled && <p>As respostas automáticas do WhatsApp continuam pausadas.</p>}
    </>}
  </section>;
}
