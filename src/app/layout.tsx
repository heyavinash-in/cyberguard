import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/layout/app-shell";

export const metadata: Metadata = {
  title: "CyberGuard | Security Intelligence",
  description: "AI-Powered Cyber Threat, Phishing & Digital Impersonation Detection",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased h-screen overflow-hidden bg-background text-foreground flex">
        <AppShell>
          {children}
        </AppShell>
      </body>
    </html>
  );
}
