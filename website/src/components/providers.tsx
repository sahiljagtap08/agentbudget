const providers = [
  {
    name: "OpenAI",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855l-5.833-3.387L15.119 7.2a.076.076 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.667zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z" />
      </svg>
    ),
  },
  {
    name: "Anthropic",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M17.304 3.541h-3.48l6.15 16.918h3.48zm-10.56 0L.594 20.459h3.523l1.271-3.596h6.224l1.271 3.596h3.523L10.256 3.541zm.007 10.08l2.263-6.404 2.263 6.404z" />
      </svg>
    ),
  },
  {
    name: "Google Gemini",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 24A14.304 14.304 0 0 0 0 12 14.304 14.304 0 0 0 12 0a14.305 14.305 0 0 0 12 12 14.305 14.305 0 0 0-12 12" />
      </svg>
    ),
  },
  {
    name: "Mistral",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M3.428 0h4.114v4.114H3.428zM16.457 0h4.114v4.114h-4.114zM3.428 4.971h4.114v4.114H3.428zM16.457 4.971h4.114v4.114h-4.114zM9.943 4.971h4.114v4.114H9.943zM0 9.943h4.114v4.114H0zm3.428 0h4.114v4.114H3.428zm6.515 0h4.114v4.114H9.943zm6.514 0h4.114v4.114h-4.114zm3.429 0H24v4.114h-4.114zM3.428 14.914h4.114v4.114H3.428zm6.515 0h4.114v4.114H9.943zm6.514 0h4.114v4.114h-4.114zM3.428 19.886h4.114V24H3.428zm6.515 0h4.114V24H9.943zm6.514 0h4.114V24h-4.114z" />
      </svg>
    ),
  },
  {
    name: "Cohere",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M8.864 17.637c2.618 0 6.107-.422 8.47-2.285 2.856-2.25 3.291-5.735 3.291-7.614C20.625 3.39 17.236 0 12.886 0H6.093C3.07 0 .62 2.45.62 5.473v.14c0 2.053.813 4.022 2.261 5.47l.118.118c2.404 2.404 3.44 3.15 3.44 4.55v.065c0 1.001.782 1.82 1.782 1.82z" />
      </svg>
    ),
  },
  {
    name: "LangChain",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
      </svg>
    ),
  },
  {
    name: "CrewAI",
    logo: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="9" cy="7" r="4" />
        <path d="M2 21v-2a4 4 0 014-4h6a4 4 0 014 4v2" />
        <circle cx="19" cy="7" r="3" />
        <path d="M22 21v-1.5a3 3 0 00-3-3" />
      </svg>
    ),
  },
];

export function Providers() {
  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-12">
        <p className="mb-8 font-mono text-[11px] font-medium uppercase tracking-widest text-muted">
          Works with every LLM provider
        </p>
        <div className="flex flex-wrap items-center gap-x-10 gap-y-5">
          {providers.map((p) => (
            <div
              key={p.name}
              className="flex items-center gap-2.5 text-muted-foreground/50 transition-colors hover:text-muted-foreground"
            >
              {p.logo}
              <span className="text-[14px] font-semibold tracking-tight">
                {p.name}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
