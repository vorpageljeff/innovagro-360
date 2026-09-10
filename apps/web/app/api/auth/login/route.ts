import { NextResponse } from "next/server";

const DEMO_EMAIL = process.env.DEMO_EMAIL ?? "demo@innovagro.local";
const DEMO_PASSWORD = process.env.DEMO_PASSWORD ?? "InnovAgro360!";
const SESSION_TOKEN = process.env.DEMO_SESSION_TOKEN ?? "innovagro-demo-session-v1";

export async function POST(request: Request) {
  const body = (await request.json()) as { email?: string; password?: string };
  if (body.email?.toLowerCase() !== DEMO_EMAIL.toLowerCase() || body.password !== DEMO_PASSWORD) {
    return NextResponse.json({ message: "E-mail ou senha inválidos." }, { status: 401 });
  }
  const response = NextResponse.json({ authenticated: true });
  response.cookies.set("innovagro_session", SESSION_TOKEN, { httpOnly: true, sameSite: "lax", secure: process.env.NODE_ENV === "production", maxAge: 28800, path: "/" });
  return response;
}
