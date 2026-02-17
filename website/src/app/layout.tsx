import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { PostHogProvider } from "@/components/posthog-provider";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AgentBudget - Real-time cost enforcement for AI agents",
  description:
    "Open-source Python SDK that puts a hard dollar limit on any AI agent session. One line to set a budget. Zero infrastructure to manage.",
  metadataBase: new URL("https://agentbudget.dev"),
  openGraph: {
    title: "AgentBudget - The ulimit for AI agents",
    description:
      "Real-time cost enforcement for AI agent sessions. Stop runaway LLM spend with one line of code.",
    url: "https://agentbudget.dev",
    siteName: "AgentBudget",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AgentBudget - The ulimit for AI agents",
    description:
      "Real-time cost enforcement for AI agent sessions. Stop runaway LLM spend with one line of code.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <PostHogProvider>{children}</PostHogProvider>
      </body>
    </html>
  );
}
