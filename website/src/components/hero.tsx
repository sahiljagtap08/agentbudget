import Link from "next/link";

export function Hero() {
  return (
    <section className="border-x border-border">
      <div className="mx-auto max-w-[1200px] px-6 pb-16 pt-24 md:pt-32">
        {/* Badge */}
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-surface px-4 py-1.5 font-mono text-[12px] text-muted-foreground">
          <span
            className="h-1.5 w-1.5 rounded-full bg-accent-green"
            style={{ animation: "pulse-dot 2s ease-in-out infinite" }}
          />
          OPEN SOURCE &middot; PYTHON SDK
        </div>

        {/* Heading */}
        <h1 className="mb-6 max-w-3xl text-4xl font-bold leading-[1.08] tracking-tight sm:text-5xl md:text-6xl lg:text-[68px]">
          <span className="text-muted-foreground">REAL-TIME</span>
          <br />
          <span className="text-accent-green">COST ENFORCEMENT</span>
          <br />
          <span className="text-muted-foreground">FOR AI AGENTS</span>
        </h1>

        {/* Subtitle */}
        <p className="mb-10 max-w-lg text-[16px] leading-relaxed text-muted-foreground">
          Set a hard dollar limit on any AI agent session with one line of code.
          Automatic tracking, circuit breaking, and cost reports across every
          LLM provider.
        </p>

        {/* CTAs */}
        <div className="flex flex-wrap items-center gap-3">
          <Link
            href="https://github.com/sahiljagtap08/agentbudget"
            className="inline-flex items-center gap-2 rounded-lg bg-foreground px-6 py-2.5 text-[14px] font-semibold text-background transition-opacity hover:opacity-90 hover:no-underline"
          >
            Get Started
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </Link>
          <Link
            href="/docs"
            className="inline-flex items-center gap-2 rounded-lg border border-border-bright px-6 py-2.5 text-[14px] font-medium text-foreground transition-colors hover:bg-surface hover:no-underline"
          >
            Read the Docs
          </Link>
        </div>

        {/* Install command */}
        <div className="mt-8 inline-flex items-center gap-3 rounded-lg border border-border bg-code-bg px-4 py-2.5 font-mono text-[13px]">
          <span className="text-muted">$</span>
          <span className="text-accent-green">pip install</span>
          <span className="text-muted-foreground">agentbudget</span>
        </div>
      </div>
    </section>
  );
}
