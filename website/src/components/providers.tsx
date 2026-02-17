export function Providers() {
  const providers = [
    "OpenAI",
    "Anthropic",
    "Google Gemini",
    "Mistral",
    "Cohere",
    "LangChain",
    "CrewAI",
  ];

  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-12">
        <p className="mb-8 font-mono text-[11px] font-medium uppercase tracking-widest text-muted">
          Works with every LLM provider
        </p>
        <div className="flex flex-wrap items-center gap-x-10 gap-y-4">
          {providers.map((name) => (
            <span
              key={name}
              className="text-[14px] font-semibold tracking-tight text-muted-foreground/50"
            >
              {name}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
