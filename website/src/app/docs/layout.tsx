import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Documentation",
  description:
    "Complete documentation for AgentBudget — installation, quickstart, API reference, supported models, and integration guides for LangChain and CrewAI.",
  alternates: {
    canonical: "https://agentbudget.dev/docs",
  },
};

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
