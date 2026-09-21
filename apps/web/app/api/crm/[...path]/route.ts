import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
const options = { httpOnly: true, secure: process.env.NODE_ENV === "production", sameSite: "strict" as const, path: "/api/crm", maxAge: 900 };
const error = (message: string, status: number) => NextResponse.json({ message }, { status, headers: { "Cache-Control": "no-store" } });

async function handle(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params;
  const route = path.join("/");
  if (!/^(session|import|leads(?:\/[0-9a-f-]{36}\/activities)?)$/.test(route)) return error("Recurso não encontrado.", 404);
  if (request.method === "POST" && request.headers.get("origin") !== request.nextUrl.origin) return error("Origem inválida.", 403);
  const base = process.env.CRM_API_URL?.replace(/\/$/, "");
  if (!base) return error("O CRM ainda não está conectado ao servidor. Nenhum dado será salvo neste navegador.", 503);
  const session = route === "session";
  if (session && request.method !== "POST") return error("Método não permitido.", 405);
  const jar = await cookies();
  const token = jar.get("crm_access")?.value;
  if (!session && !token) return error("Entre com sua conta do servidor para acessar os contatos.", 401);
  try {
    const raw = request.method === "POST" ? await request.text() : undefined;
    if (raw && new TextEncoder().encode(raw).length > 1_000_000) return error("Arquivo muito grande. Importe até 100 contatos por lote.", 413);
    if (raw) JSON.parse(raw);
    const query = request.method === "GET" ? request.nextUrl.search : "";
    const upstream = await fetch(`${base}/${session ? "auth/login" : `crm/${route}`}${query}`, {
      method: request.method, cache: "no-store", redirect: "error", signal: AbortSignal.timeout(15000),
      headers: { "Content-Type": "application/json", ...(!session ? { Authorization: `Bearer ${token}` } : {}) }, body: raw,
    });
    const data = await upstream.json();
    if (!upstream.ok) {
      if (upstream.status === 401) jar.set("crm_access", "", { ...options, maxAge: 0 });
      return error(typeof data.detail === "string" ? data.detail : "Não foi possível concluir a operação. Confira os dados e tente novamente.", upstream.status);
    }
    if (session) {
      if (typeof data.access_token !== "string") return error("Resposta de autenticação inválida.", 502);
      const response = NextResponse.json({ authenticated: true }, { headers: { "Cache-Control": "no-store" } });
      response.cookies.set("crm_access", data.access_token, options);
      return response;
    }
    return NextResponse.json(data, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return error("Não foi possível confirmar a operação no servidor. Recarregue os contatos antes de tentar novamente.", 502);
  }
}
export const GET = handle;
export const POST = handle;
