export function StarHistory() {
  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 pt-20 pb-16">
        <p className="mb-3 font-mono text-[11px] font-medium uppercase tracking-widest text-accent-bright">
          Community
        </p>
        <h2 className="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">
          Star History
        </h2>
        <p className="mb-12 max-w-md text-[15px] text-muted-foreground">
          Watch our growth on GitHub. Star the repo to stay updated.
        </p>

        <div className="flex justify-center">
          <a href="https://www.star-history.com/#sahiljagtap08/agentbudget&type=date&legend=top-left">
            <picture>
              <source
                media="(prefers-color-scheme: light)"
                srcSet="https://api.star-history.com/svg?repos=sahiljagtap08/agentbudget&type=date&theme=dark&legend=top-left"
              />
              <img
                alt="Star History Chart"
                src="https://api.star-history.com/svg?repos=sahiljagtap08/agentbudget&type=date&theme=dark&legend=top-left"
                className="w-full max-w-[700px]"
              />
            </picture>
          </a>
        </div>
      </div>
    </section>
  );
}
