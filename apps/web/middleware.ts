import { NextRequest, NextResponse } from "next/server";
const SESSION_TOKEN = process.env.DEMO_SESSION_TOKEN ?? "innovagro-demo-session-v1";
export function middleware(request: NextRequest) {
  if (request.cookies.get("innovagro_session")?.value !== SESSION_TOKEN) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("next", request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}
export const config = { matcher: ["/dashboard/:path*", "/crm/:path*", "/agenda/:path*", "/clientes/:path*", "/projetos/:path*", "/equipe/:path*", "/financeiro/:path*", "/indicadores/:path*", "/copiloto/:path*", "/configuracoes/:path*"] };
