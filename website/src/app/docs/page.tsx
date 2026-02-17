"use client";

import { Nav } from "@/components/nav";
import { CodeBlock } from "@/components/code-block";
import { useState } from "react";

const sidebarSections = [
  {
    title: "Getting Started",
    items: [
      { label: "Installation", id: "installation" },
      { label: "Quickstart", id: "quickstart" },
      { label: "Drop-in Mode", id: "drop-in" },
      { label: "Manual Mode", id: "manual" },
    ],
  },
  {
    title: "Core Concepts",
    items: [
      { label: "Budget Envelope", id: "budget-envelope" },
      { label: "Cost Sources", id: "cost-sources" },
      { label: "Circuit Breaker", id: "circuit-breaker" },
      { label: "Cost Report", id: "cost-report" },
    ],
  },
  {
    title: "Features",
    items: [
      { label: "Async Support", id: "async" },
      { label: "Nested Budgets", id: "nested-budgets" },
      { label: "Webhooks", id: "webhooks" },
      { label: "Event Callbacks", id: "callbacks" },
    ],
  },
  {
    title: "Integrations",
    items: [
      { label: "LangChain", id: "langchain" },
      { label: "CrewAI", id: "crewai" },
    ],
  },
  {
    title: "Reference",
    items: [
      { label: "API Reference", id: "api-reference" },
      { label: "Supported Models", id: "supported-models" },
      { label: "Exceptions", id: "exceptions" },
    ],
  },
];

export default function DocsPage() {
  const [mobileNav, setMobileNav] = useState(false);

  return (
    <div className="min-h-screen bg-noise">
      <Nav />
      <div className="mx-auto flex max-w-[1200px]">
        {/* Sidebar */}
        <aside className="sticky top-14 hidden h-[calc(100vh-56px)] w-[220px] shrink-0 overflow-y-auto border-x border-border py-8 md:block">
          {sidebarSections.map((section) => (
            <div key={section.title} className="mb-6">
              <h4 className="mb-2 px-5 font-mono text-[10px] font-semibold uppercase tracking-widest text-muted">
                {section.title}
              </h4>
              {section.items.map((item) => (
                <a
                  key={item.id}
                  href={`#${item.id}`}
                  className="block px-5 py-1.5 text-[13px] text-muted-foreground transition-colors hover:bg-surface hover:text-foreground hover:no-underline"
                >
                  {item.label}
                </a>
              ))}
            </div>
          ))}
        </aside>

        {/* Mobile nav toggle */}
        <button
          className="fixed bottom-6 right-6 z-50 flex h-10 w-10 items-center justify-center border border-border bg-surface text-muted-foreground md:hidden"
          onClick={() => setMobileNav(!mobileNav)}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {mobileNav && (
          <div className="fixed inset-0 z-40 bg-background/90 backdrop-blur-sm md:hidden" onClick={() => setMobileNav(false)}>
            <div className="mt-14 w-[260px] border-r border-border bg-background p-6" onClick={(e) => e.stopPropagation()}>
              {sidebarSections.map((section) => (
                <div key={section.title} className="mb-5">
                  <h4 className="mb-2 font-mono text-[10px] font-semibold uppercase tracking-widest text-muted">
                    {section.title}
                  </h4>
                  {section.items.map((item) => (
                    <a
                      key={item.id}
                      href={`#${item.id}`}
                      className="block py-1.5 text-[13px] text-muted-foreground hover:text-foreground"
                      onClick={() => setMobileNav(false)}
                    >
                      {item.label}
                    </a>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Content */}
        <main className="min-w-0 flex-1 border-r border-border px-8 py-12 md:px-12">
          <h1 className="mb-3 text-3xl font-bold tracking-tight">Documentation</h1>
          <p className="mb-10 text-[15px] text-muted-foreground">
            Everything you need to add real-time cost enforcement to your AI agents.
          </p>

          {/* Installation */}
          <h2 id="installation" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Installation
          </h2>
          <CodeBlock lang="bash">{`pip install agentbudget`}</CodeBlock>
          <p className="mt-4 text-[14px] text-muted-foreground">
            Requires Python 3.9+. No external dependencies.
          </p>
          <p className="mt-2 text-[14px] text-muted-foreground">
            For LangChain integration:
          </p>
          <CodeBlock lang="bash">{`pip install agentbudget[langchain]`}</CodeBlock>

          {/* Quickstart */}
          <h2 id="quickstart" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Quickstart
          </h2>
          <p className="mb-4 text-[14px] text-muted-foreground">
            AgentBudget offers two modes: <strong className="text-foreground">drop-in</strong> (zero code changes) and{" "}
            <strong className="text-foreground">manual</strong> (explicit wrapping).
          </p>

          {/* Drop-in */}
          <h3 id="drop-in" className="mb-4 mt-10 text-lg font-semibold">
            Drop-in Mode <span className="ml-2 bg-accent/10 px-2 py-0.5 text-[11px] font-medium text-accent-bright">Recommended</span>
          </h3>
          <p className="mb-4 text-[14px] text-muted-foreground">
            Add two lines to the top of your script. Every OpenAI and Anthropic call is tracked automatically.
          </p>
          <CodeBlock>{`import agentbudget
import openai

agentbudget.init("$5.00")

# Your existing code — no changes needed
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

print(agentbudget.spent())      # e.g. 0.0035
print(agentbudget.remaining())  # e.g. 4.9965
print(agentbudget.report())     # Full cost breakdown

agentbudget.teardown()  # Stop tracking, get final report`}</CodeBlock>

          <div className="mt-4 border-l-2 border-accent bg-accent/5 px-4 py-3 text-[13px] text-muted-foreground">
            <strong className="text-foreground">How it works:</strong>{" "}
            <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.init()</code> monkey-patches{" "}
            <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">Completions.create</code> and{" "}
            <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">Messages.create</code> on the OpenAI and Anthropic SDKs.{" "}
            Same pattern used by Sentry, Datadog, and other observability tools.
          </div>

          <h3 className="mb-3 mt-8 text-base font-semibold">Drop-in API</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-[13px]">
              <thead>
                <tr className="border-b-2 border-border">
                  <th className="py-2 pr-4 text-left font-semibold">Function</th>
                  <th className="py-2 text-left font-semibold">Description</th>
                </tr>
              </thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.init(budget)</code></td><td className="py-2">Start tracking. Patches OpenAI/Anthropic. Returns the session.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.spent()</code></td><td className="py-2">Total dollars spent so far.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.remaining()</code></td><td className="py-2">Dollars left in the budget.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.report()</code></td><td className="py-2">Full cost breakdown as a dict.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.track(result, cost, tool_name)</code></td><td className="py-2">Manually track a tool/API call cost.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.get_session()</code></td><td className="py-2">Get the active session for advanced use.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget.teardown()</code></td><td className="py-2">Stop tracking, unpatch SDKs, return final report.</td></tr>
              </tbody>
            </table>
          </div>

          {/* Manual Mode */}
          <h3 id="manual" className="mb-4 mt-10 text-lg font-semibold">Manual Mode</h3>
          <CodeBlock>{`from agentbudget import AgentBudget

budget = AgentBudget(max_spend="$5.00")

with budget.session() as session:
    response = session.wrap(
        client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Analyze this..."}]
        )
    )

    data = session.track(call_serp_api(query), cost=0.01, tool_name="serp")

    @session.track_tool(cost=0.02, tool_name="search")
    def my_search(query):
        return api.search(query)

print(session.report())`}</CodeBlock>

          {/* Budget Envelope */}
          <h2 id="budget-envelope" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Budget Envelope
          </h2>
          <p className="mb-4 text-[14px] text-muted-foreground">
            A budget envelope is a dollar amount assigned to a unit of work. Every cost is tracked in real time. When exhausted, <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">BudgetExhausted</code> is raised.
          </p>
          <CodeBlock>{`# All of these work:
AgentBudget(max_spend="$5.00")
AgentBudget(max_spend="5.00")
AgentBudget(max_spend=5.0)
AgentBudget(max_spend=5)`}</CodeBlock>

          {/* Cost Sources */}
          <h2 id="cost-sources" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Cost Sources
          </h2>
          <ul className="mb-4 list-inside list-disc space-y-2 text-[14px] text-muted-foreground">
            <li><strong className="text-foreground">LLM calls</strong> — Automatically costed using a built-in pricing table. Use <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">session.wrap(response)</code> or drop-in mode.</li>
            <li><strong className="text-foreground">Tool calls</strong> — External APIs with known per-call costs. Use <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">session.track(result, cost=0.01)</code>.</li>
            <li><strong className="text-foreground">Decorated functions</strong> — Annotate with <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">@session.track_tool(cost=0.02)</code> to auto-track on every call.</li>
          </ul>

          {/* Circuit Breaker */}
          <h2 id="circuit-breaker" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Circuit Breaker
          </h2>
          <p className="mb-4 text-[14px] text-muted-foreground">Three levels of protection:</p>
          <CodeBlock>{`budget = AgentBudget(
    max_spend="$5.00",
    soft_limit=0.9,               # Warn at 90%
    max_repeated_calls=10,        # Trip after 10 repeated calls
    loop_window_seconds=60.0,     # Within a 60-second window
    on_soft_limit=lambda r: print("Warning: 90% budget used"),
    on_hard_limit=lambda r: alert_ops_team(r),
    on_loop_detected=lambda r: print("Loop detected!"),
)`}</CodeBlock>
          <ul className="mt-4 list-inside list-disc space-y-2 text-[14px] text-muted-foreground">
            <li><strong className="text-foreground">Soft limit</strong> (default 90%) — Fires a callback. Agent can wrap up gracefully.</li>
            <li><strong className="text-foreground">Hard limit</strong> (100%) — Raises <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">BudgetExhausted</code>. No more calls.</li>
            <li><strong className="text-foreground">Loop detection</strong> — Catches repeated calls before they drain the budget. Raises <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">LoopDetected</code>.</li>
          </ul>

          {/* Cost Report */}
          <h2 id="cost-report" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Cost Report
          </h2>
          <CodeBlock lang="json">{`{
    "session_id": "sess_abc123",
    "budget": 5.00,
    "total_spent": 3.42,
    "remaining": 1.58,
    "breakdown": {
        "llm": {"total": 3.12, "calls": 8, "by_model": {"gpt-4o": 2.80}},
        "tools": {"total": 0.30, "calls": 6, "by_tool": {"serp_api": 0.05}}
    },
    "duration_seconds": 34.2,
    "terminated_by": null,
    "events": [...]
}`}</CodeBlock>

          {/* Async */}
          <h2 id="async" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Async Support
          </h2>
          <CodeBlock>{`from agentbudget import AgentBudget

budget = AgentBudget(max_spend="$5.00")

async with budget.async_session() as session:
    response = await session.wrap_async(
        client.chat.completions.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}]
        )
    )

    @session.track_tool(cost=0.01)
    async def async_search(query):
        return await api.search(query)`}</CodeBlock>

          {/* Nested Budgets */}
          <h2 id="nested-budgets" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Nested Budgets
          </h2>
          <p className="mb-4 text-[14px] text-muted-foreground">
            Parent sessions allocate sub-budgets to child tasks. When the child finishes, its total spend is charged to the parent.
          </p>
          <CodeBlock>{`with budget.session() as parent:
    child = parent.child_session(max_spend=2.0)
    with child:
        child.track("result", cost=1.50, tool_name="sub_task")

    print(parent.spent)      # 1.50
    print(parent.remaining)  # 8.50`}</CodeBlock>
          <div className="mt-4 border-l-2 border-accent bg-accent/5 px-4 py-3 text-[13px] text-muted-foreground">
            The child budget is automatically capped at the lesser of <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">max_spend</code> and the parent&apos;s remaining balance.
          </div>

          {/* Webhooks */}
          <h2 id="webhooks" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Webhooks
          </h2>
          <CodeBlock>{`budget = AgentBudget(
    max_spend="$5.00",
    webhook_url="https://your-app.com/api/budget-events",
)`}</CodeBlock>
          <p className="mt-4 text-[14px] text-muted-foreground">
            Events are sent as JSON POST requests with <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">event_type</code> ({'"'}soft_limit{'"'}, {'"'}hard_limit{'"'}, {'"'}loop_detected{'"'}) and the full cost report. Failures are logged but never raise.
          </p>

          {/* Callbacks */}
          <h2 id="callbacks" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Event Callbacks
          </h2>
          <CodeBlock>{`budget = AgentBudget(
    max_spend="$5.00",
    on_soft_limit=lambda r: logger.warning(f"90% used: {r}"),
    on_hard_limit=lambda r: alert_ops_team(r),
    on_loop_detected=lambda r: logger.error(f"Loop: {r}"),
)`}</CodeBlock>
          <p className="mt-4 text-[14px] text-muted-foreground">
            When <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">webhook_url</code> is also set, both your callback and the webhook fire.
          </p>

          {/* LangChain */}
          <h2 id="langchain" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            LangChain Integration
          </h2>
          <CodeBlock lang="bash">{`pip install agentbudget[langchain]`}</CodeBlock>
          <CodeBlock>{`from agentbudget.integrations.langchain import LangChainBudgetCallback

callback = LangChainBudgetCallback(budget="$5.00")

agent.run(
    "Research competitors in the CRM space",
    callbacks=[callback]
)

print(callback.get_report())`}</CodeBlock>

          {/* CrewAI */}
          <h2 id="crewai" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            CrewAI Integration
          </h2>
          <CodeBlock>{`from agentbudget.integrations.crewai import CrewAIBudgetMiddleware

with CrewAIBudgetMiddleware(budget="$3.00") as middleware:
    result = middleware.track(
        crew.kickoff(),
        cost=0.50,
        tool_name="crew_run"
    )

print(middleware.get_report())`}</CodeBlock>

          {/* API Reference */}
          <h2 id="api-reference" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            API Reference
          </h2>

          <h3 className="mb-3 mt-6 text-base font-semibold">AgentBudget</h3>
          <CodeBlock>{`AgentBudget(
    max_spend: str | float | int,
    soft_limit: float = 0.9,
    max_repeated_calls: int = 10,
    loop_window_seconds: float = 60.0,
    on_soft_limit: Callable = None,
    on_hard_limit: Callable = None,
    on_loop_detected: Callable = None,
    webhook_url: str = None,
)`}</CodeBlock>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Method</th><th className="py-2 pr-4 text-left font-semibold">Returns</th><th className="py-2 text-left font-semibold">Description</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.session()</code></td><td className="py-2 pr-4">BudgetSession</td><td className="py-2">Create a sync budget session</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.async_session()</code></td><td className="py-2 pr-4">AsyncBudgetSession</td><td className="py-2">Create an async budget session</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.max_spend</code></td><td className="py-2 pr-4">float</td><td className="py-2">The configured budget amount</td></tr>
              </tbody>
            </table>
          </div>

          <h3 className="mb-3 mt-8 text-base font-semibold">BudgetSession</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Method / Property</th><th className="py-2 text-left font-semibold">Description</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.wrap(response)</code></td><td className="py-2">Extract model/tokens from LLM response and record cost. Returns response.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.track(result, cost, tool_name)</code></td><td className="py-2">Record a tool call cost. Returns the result.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.track_tool(cost, tool_name)</code></td><td className="py-2">Decorator that tracks cost on every call.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.child_session(max_spend)</code></td><td className="py-2">Create child session with sub-budget. Costs roll up.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.report()</code></td><td className="py-2">Full cost report as a dict.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.spent</code></td><td className="py-2">Total dollars spent (float).</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">.remaining</code></td><td className="py-2">Dollars remaining (float).</td></tr>
              </tbody>
            </table>
          </div>

          {/* Supported Models */}
          <h2 id="supported-models" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Supported Models
          </h2>
          <p className="mb-4 text-[14px] text-muted-foreground">Built-in pricing for 50+ models. Updated February 2026.</p>

          <h3 className="mb-2 mt-6 text-sm font-semibold text-accent-bright">OpenAI</h3>
          <div className="overflow-x-auto">
            <table className="mb-6 w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Model</th><th className="py-2 pr-4 text-left font-semibold">Input / 1M</th><th className="py-2 text-left font-semibold">Output / 1M</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gpt-4.1</td><td className="py-1.5 pr-4">$2.00</td><td className="py-1.5">$8.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gpt-4.1-mini</td><td className="py-1.5 pr-4">$0.40</td><td className="py-1.5">$1.60</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gpt-4.1-nano</td><td className="py-1.5 pr-4">$0.10</td><td className="py-1.5">$0.40</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gpt-4o</td><td className="py-1.5 pr-4">$2.50</td><td className="py-1.5">$10.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gpt-4o-mini</td><td className="py-1.5 pr-4">$0.15</td><td className="py-1.5">$0.60</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">o3</td><td className="py-1.5 pr-4">$2.00</td><td className="py-1.5">$8.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">o3-mini</td><td className="py-1.5 pr-4">$1.10</td><td className="py-1.5">$4.40</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">o4-mini</td><td className="py-1.5 pr-4">$1.10</td><td className="py-1.5">$4.40</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">o1</td><td className="py-1.5 pr-4">$15.00</td><td className="py-1.5">$60.00</td></tr>
              </tbody>
            </table>
          </div>

          <h3 className="mb-2 text-sm font-semibold text-accent-bright">Anthropic</h3>
          <div className="overflow-x-auto">
            <table className="mb-6 w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Model</th><th className="py-2 pr-4 text-left font-semibold">Input / 1M</th><th className="py-2 text-left font-semibold">Output / 1M</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-1.5 pr-4">claude-opus-4-6</td><td className="py-1.5 pr-4">$5.00</td><td className="py-1.5">$25.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">claude-sonnet-4.5</td><td className="py-1.5 pr-4">$3.00</td><td className="py-1.5">$15.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">claude-haiku-4.5</td><td className="py-1.5 pr-4">$1.00</td><td className="py-1.5">$5.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">claude-3.5-sonnet</td><td className="py-1.5 pr-4">$3.00</td><td className="py-1.5">$15.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">claude-3.5-haiku</td><td className="py-1.5 pr-4">$0.80</td><td className="py-1.5">$4.00</td></tr>
              </tbody>
            </table>
          </div>

          <h3 className="mb-2 text-sm font-semibold text-accent-bright">Google Gemini</h3>
          <div className="overflow-x-auto">
            <table className="mb-6 w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Model</th><th className="py-2 pr-4 text-left font-semibold">Input / 1M</th><th className="py-2 text-left font-semibold">Output / 1M</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gemini-2.5-pro</td><td className="py-1.5 pr-4">$1.25</td><td className="py-1.5">$10.00</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gemini-2.5-flash</td><td className="py-1.5 pr-4">$0.30</td><td className="py-1.5">$2.50</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gemini-2.0-flash</td><td className="py-1.5 pr-4">$0.10</td><td className="py-1.5">$0.40</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">gemini-1.5-pro</td><td className="py-1.5 pr-4">$1.25</td><td className="py-1.5">$5.00</td></tr>
              </tbody>
            </table>
          </div>

          <h3 className="mb-2 text-sm font-semibold text-accent-bright">Mistral &amp; Cohere</h3>
          <div className="overflow-x-auto">
            <table className="mb-6 w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Model</th><th className="py-2 pr-4 text-left font-semibold">Input / 1M</th><th className="py-2 text-left font-semibold">Output / 1M</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-1.5 pr-4">mistral-large</td><td className="py-1.5 pr-4">$0.50</td><td className="py-1.5">$1.50</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">mistral-small</td><td className="py-1.5 pr-4">$0.03</td><td className="py-1.5">$0.11</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">codestral</td><td className="py-1.5 pr-4">$0.30</td><td className="py-1.5">$0.90</td></tr>
                <tr className="border-b border-border"><td className="py-1.5 pr-4">command-r-plus</td><td className="py-1.5 pr-4">$2.50</td><td className="py-1.5">$10.00</td></tr>
              </tbody>
            </table>
          </div>

          <div className="border-l-2 border-accent bg-accent/5 px-4 py-3 text-[13px] text-muted-foreground">
            Missing a model? Pricing data is in <code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">agentbudget/pricing.py</code>. PRs welcome.
          </div>

          {/* Exceptions */}
          <h2 id="exceptions" className="mb-4 mt-16 border-t border-border pt-8 text-xl font-semibold">
            Exceptions
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-[13px]">
              <thead><tr className="border-b-2 border-border"><th className="py-2 pr-4 text-left font-semibold">Exception</th><th className="py-2 text-left font-semibold">When</th></tr></thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">BudgetExhausted</code></td><td className="py-2">Session exceeded its dollar budget (hard limit).</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">LoopDetected</code></td><td className="py-2">Repeated calls to the same tool/model detected.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">InvalidBudget</code></td><td className="py-2">Budget string couldn&apos;t be parsed.</td></tr>
                <tr className="border-b border-border"><td className="py-2 pr-4"><code className="bg-code-bg px-1.5 py-0.5 text-[12px] text-accent-bright">AgentBudgetError</code></td><td className="py-2">Base exception for all AgentBudget errors.</td></tr>
              </tbody>
            </table>
          </div>

          <div className="h-24" />
        </main>
      </div>
    </div>
  );
}
