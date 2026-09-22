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
    const next = searchParams.get("next");
    router.replace(next?.startsWith("/") && !next.startsWith("//") && !next.includes("\\") ? next : "/crm"); router.refresh();
  }
  return <form className="panel login-card" onSubmit={submit}><p className="eyebrow">INNOVAGRO 360</p><h1 className="title">Entre no seu workspace</h1><p className="subtitle">Acesse com seu e-mail e senha.</p><label className="field">E-mail<input name="email" type="email" autoComplete="email" required /></label><label className="field">Senha<input name="password" type="password" autoComplete="current-password" required /></label>{error && <p className="form-error" role="alert">{error}</p>}<button className="btn primary login-submit" disabled={loading}>{loading ? "Entrando…" : "Entrar"}</button><p className="demo-hint">Seus contatos e retornos em um só lugar.</p></form>;
}
