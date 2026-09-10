import { Suspense } from "react";
import { LoginForm } from "./login-form";

export default function Login() {
  return <main className="login-page"><Suspense fallback={<div className="panel login-card">Carregando…</div>}><LoginForm /></Suspense></main>;
}
