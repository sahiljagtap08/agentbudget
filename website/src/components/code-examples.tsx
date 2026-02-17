"use client";

import { useState } from "react";

const tabs = [
  { label: "Drop-in Mode", accent: "text-accent-green", borderColor: "border-accent-green" },
  { label: "Manual Session", accent: "text-accent-orange", borderColor: "border-accent-orange" },
  { label: "Async Agent", accent: "text-accent-pink", borderColor: "border-accent-pink" },
  { label: "Nested Budgets", accent: "text-accent-yellow", borderColor: "border-accent-yellow" },
];

const codeBlocks = [
  // Drop-in Mode
  `import agentbudget
import openai

agentbudget.init("$5.00")

# Your existing code. Zero changes needed.
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze this market..."}]
)
# ^ Automatically tracked. Budget enforced.

print(agentbudget.spent())       # 0.0035
print(agentbudget.remaining())   # 4.9965
print(agentbudget.report())      # Full cost breakdown

agentbudget.teardown()`,

  // Manual Session
  `from agentbudget import AgentBudget

budget = AgentBudget(max_spend="$5.00")

with budget.session() as session:
    # Auto-cost LLM responses
    response = session.wrap(
        client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}]
        )
    )

    # Track tool calls with known costs
    data = session.track(call_api(query), cost=0.01, tool_name="serp")

    # Decorate functions for auto-tracking
    @session.track_tool(cost=0.02, tool_name="search")
    def my_search(query):
        return api.search(query)

print(session.report())`,

  // Async Agent
  `from agentbudget import AgentBudget

budget = AgentBudget(max_spend="$5.00")

async with budget.async_session() as session:
    # Await and auto-cost in one call
    response = await session.wrap_async(
        client.chat.completions.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Research this topic"}]
        )
    )

    # Works with both sync and async functions
    @session.track_tool(cost=0.01)
    async def async_search(query):
        return await api.search(query)

    result = await async_search("AI market trends")`,

  // Nested Budgets
  `from agentbudget import AgentBudget

budget = AgentBudget(max_spend="$10.00")

with budget.session() as parent:
    # Allocate $2 for a research sub-task
    research = parent.child_session(max_spend=2.0)
    with research:
        research.wrap(client.chat.completions.create(...))
        research.track(serp_api(), cost=0.05, tool_name="search")

    # Allocate $3 for an analysis sub-task
    analysis = parent.child_session(max_spend=3.0)
    with analysis:
        analysis.wrap(client.chat.completions.create(...))

    # Both child costs roll up to parent automatically
    print(parent.remaining)  # Budget minus all child spend`,
];

function highlightPython(code: string): string {
  const keywords = ["import", "from", "def", "async", "await", "with", "as", "return", "class", "for", "in", "if", "else", "print", "None", "True", "False"];
  const lines = code.split("\n");

  return lines
    .map((line) => {
      // Comments
      const commentIdx = line.indexOf("#");
      let mainPart = line;
      let commentPart = "";
      if (commentIdx !== -1) {
        // Make sure # is not inside a string
        const beforeHash = line.substring(0, commentIdx);
        const singleQuotes = (beforeHash.match(/'/g) || []).length;
        const doubleQuotes = (beforeHash.match(/"/g) || []).length;
        if (singleQuotes % 2 === 0 && doubleQuotes % 2 === 0) {
          mainPart = line.substring(0, commentIdx);
          commentPart = `<span class="tok-cm">${escapeHtml(line.substring(commentIdx))}</span>`;
        }
      }

      // Strings
      mainPart = mainPart.replace(/("""[\s\S]*?"""|'''[\s\S]*?'''|"[^"]*"|'[^']*')/g, '<span class="tok-str">$1</span>');

      // Numbers
      mainPart = mainPart.replace(/\b(\d+\.?\d*)\b/g, '<span class="tok-num">$1</span>');

      // Keywords
      for (const kw of keywords) {
        const re = new RegExp(`\\b(${kw})\\b`, "g");
        mainPart = mainPart.replace(re, '<span class="tok-kw">$1</span>');
      }

      // Decorators
      mainPart = mainPart.replace(/(@\w+)/g, '<span class="tok-op">$1</span>');

      // Function calls
      mainPart = mainPart.replace(/(\w+)\(/g, '<span class="tok-fn">$1</span>(');

      return mainPart + commentPart;
    })
    .join("\n");
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

export function CodeExamples() {
  const [active, setActive] = useState(0);

  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-20">
        <p className="mb-3 font-mono text-[11px] font-medium uppercase tracking-widest text-accent-green">
          Code Examples
        </p>
        <h2 className="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">
          A few lines. Full control.
        </h2>
        <p className="mb-10 max-w-md text-[15px] text-muted-foreground">
          Drop-in auto-tracking, manual wrapping, async agents, and nested budgets.
        </p>

        {/* Tabs */}
        <div className="flex border-b border-border">
          {tabs.map((tab, i) => (
            <button
              key={tab.label}
              onClick={() => setActive(i)}
              className={`border-b-2 px-5 py-3 font-mono text-[12px] font-medium transition-colors ${
                active === i
                  ? `${tab.accent} ${tab.borderColor}`
                  : "border-transparent text-muted hover:text-muted-foreground"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Code block */}
        <div className="overflow-x-auto rounded-b-lg border-x border-b border-border bg-code-bg p-6">
          <pre className="font-mono text-[13px] leading-7">
            <code
              dangerouslySetInnerHTML={{
                __html: highlightPython(codeBlocks[active]),
              }}
            />
          </pre>
        </div>
      </div>
    </section>
  );
}
