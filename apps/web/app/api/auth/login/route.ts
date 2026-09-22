import { NextResponse } from "next/server";

export async function POST(request: Request) {
  if (request.headers.get("origin") !== new URL(request.url).origin) {
    return NextResponse.json({ message: "Origem inválida." }, { status: 403 });
  }
  const base = process.env.CRM_API_URL?.replace(/\/$/, "");
  const session = process.env.DEMO_SESSION_TOKEN;
  if (!base || !session) return NextResponse.json({ message: "Acesso ao servidor ainda não configurado." }, { status: 503 });
  try {
    const body = await request.json();
    if (typeof body.email !== "string" || typeof body.password !== "string") return NextResponse.json({ message: "Informe e-mail e senha." }, { status: 400 });
    const upstream = await fetch(`${base}/auth/login`, {
      method: "POST", cache: "no-store", redirect: "error", signal: AbortSignal.timeout(15000),
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: body.email, password: body.password, organization_slug: process.env.CRM_ORGANIZATION_SLUG ?? "voragon" }),
    });
    const data = await upstream.json();
    if (!upstream.ok || typeof data.access_token !== "string") return NextResponse.json({ message: "Não foi possível entrar. Confira e-mail e senha." }, { status: upstream.status === 401 ? 401 : 502 });
    const response = NextResponse.json({ authenticated: true }, { headers: { "Cache-Control": "no-store" } });
    const options = { httpOnly: true, sameSite: "strict" as const, secure: process.env.NODE_ENV === "production", maxAge: 900 };
    response.cookies.set("innovagro_session", session, { ...options, path: "/" });
    response.cookies.set("crm_access", data.access_token, { ...options, path: "/api/crm" });
    return response;
  } catch {
    return NextResponse.json({ message: "Servidor indisponível. Tente novamente." }, { status: 502 });
  }
}
