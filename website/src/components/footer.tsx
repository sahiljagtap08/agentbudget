import Link from "next/link";

const columns = [
  {
    title: "Product",
    links: [
      { label: "Documentation", href: "/docs" },
      { label: "PyPI Package", href: "https://pypi.org/project/agentbudget/" },
      { label: "Changelog", href: "https://github.com/sahiljagtap08/agentbudget/releases" },
    ],
  },
  {
    title: "Resources",
    links: [
      { label: "Getting Started", href: "/docs#installation" },
      { label: "API Reference", href: "/docs#api-reference" },
      { label: "Supported Models", href: "/docs#supported-models" },
    ],
  },
  {
    title: "Community",
    links: [
      { label: "GitHub", href: "https://github.com/sahiljagtap08/agentbudget" },
      { label: "Issues", href: "https://github.com/sahiljagtap08/agentbudget/issues" },
    ],
  },
];

export function Footer() {
  return (
    <footer className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-16">
        <div className="grid grid-cols-2 gap-8 sm:grid-cols-4">
          {/* Brand column */}
          <div>
            <span className="text-[15px] font-bold tracking-tight">
              Agent<span className="text-accent-bright">Budget</span>
            </span>
            <p className="mt-3 text-[13px] leading-relaxed text-muted">
              Real-time cost enforcement
              <br />
              for AI agent sessions.
            </p>
            <div className="mt-4 flex gap-3">
              <Link
                href="https://github.com/sahiljagtap08/agentbudget"
                className="text-muted transition-colors hover:text-muted-foreground"
                aria-label="GitHub"
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
                </svg>
              </Link>
            </div>
          </div>

          {/* Link columns */}
          {columns.map((col) => (
            <div key={col.title}>
              <h4 className="mb-3 text-[12px] font-semibold uppercase tracking-wider text-muted-foreground">
                {col.title}
              </h4>
              <ul className="space-y-2">
                {col.links.map((link) => (
                  <li key={link.label}>
                    <Link
                      href={link.href}
                      className="text-[13px] text-muted transition-colors hover:text-muted-foreground hover:no-underline"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 border-t border-border pt-6">
          <p className="text-[12px] text-muted">
            &copy; {new Date().getFullYear()} AgentBudget &middot; Apache 2.0 &middot; Built by{" "}
            <Link href="https://github.com/sahiljagtap08" className="text-muted-foreground hover:text-foreground">
              Sahil Jagtap
            </Link>
          </p>
        </div>
      </div>
    </footer>
  );
}
