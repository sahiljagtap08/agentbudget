const problems = [
  {
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M21 12a9 9 0 11-6.219-8.56" />
        <polyline points="21 3 21 9 15 9" />
      </svg>
    ),
    title: "The Loop Problem",
    description:
      "Agent gets stuck retrying the same call. 200 LLM calls in 10 minutes. $50\u2013$200 before anyone notices.",
    accent: "border-accent/30 text-accent-bright",
    bg: "bg-accent/10",
  },
  {
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <line x1="12" y1="1" x2="12" y2="23" />
        <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
      </svg>
    ),
    title: "The Invisible Spend",
    description:
      "Tokens aren\u2019t dollars. GPT-4o costs 15x more than GPT-4o-mini. Mix in tool calls, nobody knows the real cost.",
    accent: "border-accent/30 text-accent-bright",
    bg: "bg-accent/10",
  },
  {
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="2" y1="12" x2="22" y2="12" />
        <path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" />
      </svg>
    ),
    title: "Multi-Provider Chaos",
    description:
      "One session calls OpenAI, Anthropic, Google, and 3 APIs. Each has its own billing. No unified real-time view.",
    accent: "border-accent/30 text-accent-bright",
    bg: "bg-accent/10",
  },
  {
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
      </svg>
    ),
    title: "The Scaling Problem",
    description:
      "1,000 concurrent sessions. 5% failure rate = 50 runaway agents. Your bill becomes your worst case times your user count.",
    accent: "border-accent/30 text-accent-bright",
    bg: "bg-accent-yellow/10",
  },
];

export function Problems() {
  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-20">
        <p className="mb-3 font-mono text-[11px] font-medium uppercase tracking-widest text-accent-bright">
          The Problem
        </p>
        <h2 className="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">
          Agents are unpredictable by design.
          <br />
          <span className="text-muted-foreground">Your bill shouldn&apos;t be.</span>
        </h2>
        <p className="mb-12 max-w-lg text-[15px] text-muted-foreground">
          Traditional software has deterministic costs. Agent software doesn&apos;t.
          An agent might make 3 LLM calls or 300.
        </p>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {problems.map((p) => (
            <div
              key={p.title}
              className="group rounded-xl border border-border bg-surface p-6 transition-colors hover:border-border-bright"
            >
              <div
                className={`mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg border ${p.accent} ${p.bg}`}
              >
                {p.icon}
              </div>
              <h3 className="mb-2 text-[15px] font-semibold">{p.title}</h3>
              <p className="text-[13px] leading-relaxed text-muted-foreground">
                {p.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
