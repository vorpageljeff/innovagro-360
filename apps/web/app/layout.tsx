import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {title: "InnovAgro 360", description: "Gestão integrada do relacionamento ao resultado"};
export default function RootLayout({children}:{children:React.ReactNode}) {
  return <html lang="pt-BR"><body>{children}</body></html>;
}

