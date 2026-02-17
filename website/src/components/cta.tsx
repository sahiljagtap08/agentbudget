import Link from "next/link";

export function CTA() {
  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-24 text-center">
        <h2 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">
          Ship your agents with confidence.
        </h2>
        <p className="mb-10 text-[17px] text-muted-foreground">
          Set a budget. Move on.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Link
            href="https://github.com/sahiljagtap08/agentbudget"
            className="inline-flex items-center gap-2 bg-gradient-accent px-6 py-2.5 text-[14px] font-semibold text-white transition-opacity hover:opacity-90 hover:no-underline"
          >
            Get Started
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </Link>
          <Link
            href="/docs"
            className="inline-flex items-center gap-2 border border-border-bright px-6 py-2.5 text-[14px] font-medium text-foreground transition-colors hover:bg-surface hover:no-underline"
          >
            Read the Docs
          </Link>
        </div>
      </div>

      {/* Large gradient watermark text */}
      <div
        className="select-none text-center text-[clamp(60px,12vw,140px)] font-extrabold leading-none tracking-tighter"
        style={{
          background: "linear-gradient(180deg, rgba(139,92,246,0.12) 0%, rgba(139,92,246,0) 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
        }}
      >
        AGENTBUDGET
      </div>
    </section>
  );
}
