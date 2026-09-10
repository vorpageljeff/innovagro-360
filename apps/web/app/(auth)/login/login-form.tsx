"use client";
import { FormEvent, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(""); setLoading(true);
    const form = new FormData(event.currentTarget);
    const response = await fetch("/api/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: form.get("email"), password: form.get("password") }) });
    setLoading(false);
    if (!response.ok) { const body = await response.json() as {message?:string}; setError(body.message ?? "Não foi possível entrar."); return; }
    router.replace(searchParams.get("next") ?? "/dashboard"); router.refresh();
  }
  return <form className="panel login-card" onSubmit={submit}><p className="eyebrow">INNOVAGRO 360</p><h1 className="title">Entre no seu workspace</h1><p className="subtitle">Use as credenciais de demonstração para continuar.</p><label className="field">E-mail<input name="email" type="email" autoComplete="email" defaultValue="demo@innovagro.local" required /></label><label className="field">Senha<input name="password" type="password" autoComplete="current-password" defaultValue="InnovAgro360!" required /></label>{error && <p className="form-error" role="alert">{error}</p>}<button className="btn primary login-submit" disabled={loading}>{loading ? "Entrando…" : "Entrar"}</button><p className="demo-hint">Ambiente de demonstração • dados fictícios</p></form>;
}
