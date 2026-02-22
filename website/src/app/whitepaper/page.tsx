import { Footer } from "@/components/footer";
import { Nav } from "@/components/nav";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Whitepaper",
  description:
    "Read the AgentBudget whitepaper — published research on real-time cost enforcement for AI agent sessions.",
  alternates: {
    canonical: "https://agentbudget.dev/whitepaper",
  },
};

export default function WhitepaperPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Nav />

      <main className="flex-1 border-x border-border">
        <div className="mx-auto max-w-[1200px] px-6 py-10">
          {/* Header */}
          <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <div className="mb-2 inline-flex items-center gap-1.5 border border-accent/20 bg-accent/5 px-3 py-1 font-mono text-[11px] text-muted-foreground">
                <span
                  className="h-1.5 w-1.5 rounded-full bg-accent"
                  style={{ animation: "pulse-dot 2s ease-in-out infinite" }}
                />
                PUBLISHED RESEARCH
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                Agent<span className="text-accent-bright">Budget</span> Whitepaper
              </h1>
              <p className="mt-1.5 max-w-lg text-[14px] leading-relaxed text-muted-foreground">
                Real-time cost enforcement for AI agent sessions — design, architecture, and benchmarks.
              </p>
            </div>

            <a
              href="https://doi.org/10.5281/zenodo.18734145"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex shrink-0 items-center gap-2 border border-border-bright px-4 py-2 text-[13px] font-medium text-foreground transition-colors hover:bg-surface hover:no-underline sm:self-end"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
              </svg>
              View on Zenodo (DOI)
            </a>
          </div>

          {/* PDF Viewer */}
          <div className="border border-border bg-surface">
            <iframe
              src="/agentbudget_whitepaper_v1.pdf#toolbar=1&navpanes=1&scrollbar=1"
              className="w-full"
              style={{ height: "82vh", minHeight: "600px" }}
              title="AgentBudget Whitepaper"
              loading="lazy"
            />
          </div>

          {/* Footer note */}
          <p className="mt-4 text-[12px] text-muted">
            If the PDF does not render,{" "}
            <a
              href="/agentbudget_whitepaper_v1.pdf"
              download
              className="text-accent-bright underline-offset-2 hover:underline"
            >
              download it directly
            </a>
            {" "}or{" "}
            <a
              href="https://doi.org/10.5281/zenodo.18734145"
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent-bright underline-offset-2 hover:underline"
            >
              read it on Zenodo
            </a>
            .
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
