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
  title: {
    default: "AgentBudget - Real-time cost enforcement for AI agents",
    template: "%s | AgentBudget",
  },
  description:
    "Open-source Python SDK that puts a hard dollar limit on any AI agent session. One line to set a budget. Zero infrastructure to manage.",
  metadataBase: new URL("https://agentbudget.dev"),
  keywords: [
    "AI agent budget",
    "LLM cost tracking",
    "AI cost control",
    "OpenAI budget limit",
    "agent cost enforcement",
    "LLM spend limit",
    "AI agent cost management",
    "python AI budget",
    "GPT cost tracker",
    "anthropic budget",
    "runaway agent prevention",
    "AI agent loop detection",
  ],
  authors: [{ name: "Sahil Jagtap" }],
  creator: "Sahil Jagtap",
  openGraph: {
    title: "AgentBudget - The ulimit for AI agents",
    description:
      "Real-time cost enforcement for AI agent sessions. Stop runaway LLM spend with one line of code.",
    url: "https://agentbudget.dev",
    siteName: "AgentBudget",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AgentBudget - The ulimit for AI agents",
    description:
      "Real-time cost enforcement for AI agent sessions. Stop runaway LLM spend with one line of code.",
    creator: "@twtofsahil",
  },
  alternates: {
    canonical: "https://agentbudget.dev",
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "AgentBudget",
  applicationCategory: "DeveloperApplication",
  operatingSystem: "Any",
  description:
    "Open-source Python SDK that puts a hard dollar limit on any AI agent session. Real-time cost enforcement with circuit breaking and loop detection.",
  url: "https://agentbudget.dev",
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "USD",
  },
  author: {
    "@type": "Person",
    name: "Sahil Jagtap",
  },
  programmingLanguage: "Python",
  softwareRequirements: "Python 3.9+",
  license: "https://opensource.org/licenses/Apache-2.0",
  codeRepository: "https://github.com/sahiljagtap08/agentbudget",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <PostHogProvider>{children}</PostHogProvider>
      </body>
    </html>
  );
}
