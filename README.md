# AgentBudget SDK 

### Real-time cost enforcement for AI agent sessions.

https://pypi.org/project/agentbudget/ 

---

## What is AgentBudget?

AgentBudget is an open-source SDK that gives developers a dead-simple way to put a dollar limit on any AI agent session. It wraps LLM calls, tool calls, and external API requests with real-time cost tracking and automatic circuit breaking — so your agent can never silently burn through your budget.

```python
from agentbudget import AgentBudget

budget = AgentBudget(max_spend="$5.00")

with budget.session() as session:
    # Every LLM call is tracked and costed automatically
    response = session.wrap(openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Research competitors in the CRM space"}]
    ))

    # Tool calls and external APIs get custom cost annotations
    result = session.track(call_serp_api(query="CRM market"), cost=0.01)

    # When the $5 limit is hit, the session raises BudgetExhausted
    # No silent overruns. No surprise bills.

print(session.report())
# Total spend: $3.42 | Remaining: $1.58 | LLM: $3.12 | Tools: $0.30 | Calls: 14
```

**One line to set a budget. Zero infrastructure to manage. Works with any LLM provider.**

---

## The Problem

AI agents are unpredictable by design. Unlike traditional software where you know exactly how many API calls a function makes, an agent decides at runtime how many LLM calls to make, which tools to invoke, and how many retries to attempt. This creates a class of cost failures that didn't exist before:

### The Loop Problem
An agent gets stuck in a reasoning loop — retrying the same failed tool call, rephrasing the same query, or recursing through subtasks. A single stuck agent can make hundreds of LLM calls in minutes. At $0.03–$0.15 per call, a 10-minute loop can cost $50–$200 before anyone notices.

### The Invisible Spend Problem
Most agent frameworks track token counts, but tokens aren't dollars. A GPT-4o call costs 15x more than a GPT-4o-mini call for similar token counts. A Serp API call costs $0.01. A Stripe API call is free. A premium data enrichment call costs $0.50. Agents chain all of these together, and no single system tracks the combined real-dollar cost of a session.

### The Multi-Provider Problem
A single agent session might call OpenAI for reasoning, Anthropic for analysis, Google for search, and three different SaaS APIs for data. Each provider has its own pricing model, its own billing dashboard, and its own latency before costs appear. There's no unified real-time view of what a single agent run actually cost.

### The Scaling Problem
When you go from 1 agent to 1,000 concurrent agent sessions serving customers, a 5% failure rate on cost control means 50 runaway sessions. Without per-session budget enforcement, your monthly bill becomes a function of your worst-case agent behavior multiplied by your user count.

---

## Who is AgentBudget For?

### 1. Developers building AI agent products

If you're shipping an AI agent to customers — a support bot, a research assistant, a coding agent, a workflow automation tool — you need to guarantee that each customer session stays within a cost envelope. Your margins depend on it.

**Your pain today:** You set `max_tokens` on LLM calls and hope for the best. You find out about cost overruns from your cloud bill 24 hours later. You've been burned at least once by a stuck agent loop.

**With AgentBudget:** Every customer session gets a budget. If a session costs more than expected, it's killed automatically. You see per-session cost breakdowns in real time. Your unit economics become predictable.

### 2. Teams deploying internal AI agents

Engineering teams using AI agents for code review, data analysis, document processing, or internal tooling. The agents work great 95% of the time, but the other 5% produce surprise bills that make finance teams nervous.

**Your pain today:** No one knows which internal agent costs what. The shared OpenAI API key gets a $2,000 bill and nobody can attribute it. Leadership asks "what's the ROI on our AI spend?" and you can't answer per-workflow.

**With AgentBudget:** Each workflow gets a budget. Costs are attributed to specific tasks. Monthly spend becomes forecastable. You can finally answer "this document processing agent costs $0.12 per document on average, with a hard cap at $0.50."

### 3. AI platform builders (the AirStitch / Zapier / n8n use case)

If you're building a platform where users create their own agents or automations, you need to prevent any single user's workflow from consuming disproportionate resources — and you need to meter their usage for billing.

**Your pain today:** User-created agents are black boxes. A user builds a workflow that accidentally loops and it eats your infrastructure budget. You can't meter individual workflow costs for usage-based billing because cost data is fragmented across providers.

**With AgentBudget:** Each user workflow gets a budget envelope. If a user's automation exceeds their plan limit, it's halted gracefully. You get structured cost events you can pipe into your billing system.

### 4. Researchers and hobbyists

Anyone experimenting with agents who has accidentally left a LangChain agent running overnight and woke up to a $300 OpenAI bill. You just want a safety net.

**With AgentBudget:** `budget = AgentBudget("$2.00")` — that's it. Two-dollar hard cap. Sleep peacefully.

---

## Why Existing Tools Don't Solve This

| Tool | What it does | What's missing |
|---|---|---|
| **LangSmith** | Tracks token usage and cost *after the fact*. Dashboard shows what you spent. | No real-time enforcement. It's observability, not prevention. By the time you see the cost, you've already paid it. |
| **LangChain ModelCallLimitMiddleware** | Limits the *number* of LLM calls per session. | Counts calls, not dollars. 10 cheap calls and 10 expensive calls look the same. Doesn't track tool/API costs at all. |
| **Langfuse** | Open-source LLM observability. Tracks cost per trace. | Same as LangSmith — it's a monitoring tool, not an enforcement tool. No circuit breaking. |
| **Lava AI Spend** | Per-API-key spend caps with auto-cutoff. | Operates at the API key level, not the session level. Can't give User A a $5 budget and User B a $10 budget on the same key. Doesn't track non-LLM costs (tool calls, external APIs). |
| **OpenAI/Anthropic usage limits** | Monthly org-level spend caps. | Way too coarse. A monthly cap doesn't help when one session burns $200 in 10 minutes. No per-session granularity. |
| **DIY callbacks** | Custom LangChain callbacks that track `total_cost` and raise exceptions. | Everyone rebuilds this from scratch. No standard interface. Usually OpenAI-only. Doesn't handle tool costs, multi-provider, or async agents. Breaks when you switch frameworks. |

**The gap AgentBudget fills:** Real-time, dollar-denominated, per-session budget enforcement that spans LLM calls + tool calls + external APIs, works across providers, and kills runaway sessions automatically.

---

## Core Concepts

### Budget Envelope
A budget envelope is a dollar amount assigned to a unit of work — a session, a task, a user request, or a workflow run. Every cost incurred within that envelope is tracked in real time. When the budget is exhausted, the session terminates.

### Cost Sources
AgentBudget tracks three categories of cost:

1. **LLM calls** — Automatically costed using a built-in pricing table that maps model names to per-token input/output prices. Updated regularly. Supports OpenAI, Anthropic, Google, Mistral, Cohere, and open-source models via common inference providers.

2. **Tracked tool calls** — External API calls where the developer annotates the cost. Example: `session.track(serp_api_call(), cost=0.01)`. This is for APIs with known per-call pricing.

3. **Estimated costs** — For tool calls where cost isn't deterministic, developers can provide cost estimation functions. Example: a database query where cost depends on rows scanned.

### Circuit Breaker
When remaining budget drops below a configurable threshold, the circuit breaker activates:

- **Soft limit** (default 90% spent): Emits a warning event. Agent can choose to wrap up gracefully.
- **Hard limit** (default 100% spent): Raises `BudgetExhausted` exception. No more calls allowed.
- **Loop detection**: If the same tool is called N times with similar arguments within a time window, the circuit breaker trips early — even if budget remains. This catches infinite loops before they drain the budget.

### Cost Report
Every session produces a structured cost report:

```python
{
    "session_id": "sess_abc123",
    "budget": 5.00,
    "total_spent": 3.42,
    "remaining": 1.58,
    "breakdown": {
        "llm": {"total": 3.12, "calls": 8, "by_model": {"gpt-4o": 2.80, "gpt-4o-mini": 0.32}},
        "tools": {"total": 0.30, "calls": 6, "by_tool": {"serp_api": 0.05, "scrape": 0.25}},
    },
    "duration_seconds": 34.2,
    "terminated_by": null,  # or "budget_exhausted" or "loop_detected"
    "events": [...]  # Full timeline of every costed action
}
```

This report can be piped to your observability stack, your billing system, or simply logged.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Agent Code                       │
│                                                         │
│   budget = AgentBudget("$5.00")                         │
│   with budget.session() as s:                           │
│       s.wrap(llm.chat(...))     # Auto-costed           │
│       s.track(api_call(), cost=0.01)  # Manual cost     │
│                                                         │
└─────────────┬───────────────────────────┬───────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────┐     ┌─────────────────────────────┐
│   LLM Cost Engine   │     │   Tool Cost Registry        │
│                     │     │                             │
│ • Pricing table     │     │ • Per-call fixed costs      │
│   (model → $/token) │     │ • Estimation functions      │
│ • Auto-detect model │     │ • Custom cost annotations   │
│ • Cache-aware       │     │                             │
│   pricing           │     │                             │
└─────────┬───────────┘     └──────────────┬──────────────┘
          │                                │
          ▼                                ▼
┌─────────────────────────────────────────────────────────┐
│                   Budget Ledger                          │
│                                                         │
│  Running total │ Remaining balance │ Event timeline      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Circuit Breaker                        │   │
│  │                                                   │   │
│  │  • Soft limit warning (configurable threshold)    │   │
│  │  • Hard limit enforcement (budget exhausted)      │   │
│  │  • Loop detection (repeated similar calls)        │   │
│  │  • Callback hooks for custom handling             │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  Events → Webhook / Logger / Billing system             │
└─────────────────────────────────────────────────────────┘
```

### What it is NOT
- **Not an LLM proxy.** It doesn't sit between you and OpenAI. It wraps your existing client calls.
- **Not an observability platform.** It produces cost data, but it doesn't store dashboards. Pipe the output to LangSmith, Datadog, or wherever.
- **Not a billing system.** It enforces budgets, but it doesn't invoice customers. Pipe cost reports to Stripe/Orb/Lago for that.
- **Not infrastructure.** No Redis, no servers, no cloud account. It's a library that runs in your process.

---

## Integration Points

### Framework Support
```python
# LangChain / LangGraph
from agentbudget.integrations import LangChainBudgetCallback
agent.run(callbacks=[LangChainBudgetCallback(budget="$5.00")])

# CrewAI
from agentbudget.integrations import CrewAIBudgetMiddleware
crew = Crew(agents=[...], middleware=[CrewAIBudgetMiddleware(budget="$3.00")])

# Raw OpenAI / Anthropic SDK
from agentbudget import AgentBudget
budget = AgentBudget("$5.00")
with budget.session() as s:
    response = s.wrap(client.chat.completions.create(...))

# MCP Tool Calls
@session.track_tool(cost=0.02)
def my_mcp_tool(params):
    return mcp_client.call_tool("search", params)
```

### Event Hooks
```python
budget = AgentBudget(
    max_spend="$5.00",
    on_soft_limit=lambda report: logger.warning(f"90% budget used: {report}"),
    on_hard_limit=lambda report: alert_ops_team(report),
    on_loop_detected=lambda report: logger.error(f"Loop detected: {report}"),
    webhook_url="https://your-app.com/api/budget-events",  # Optional
)
```

---

## Why Open Source?

1. **Trust.** A budget enforcement SDK that you can't audit is worthless. You need to see exactly how costs are calculated and when circuit breakers trip.

2. **Adoption.** The agent ecosystem is fragmented — LangChain, CrewAI, AutoGen, custom frameworks, raw SDK calls. An open-source library gets adopted across all of them. A proprietary service gets adopted by none.

3. **Community pricing data.** Model pricing changes constantly. An open-source project with community contributions keeps the pricing table accurate across hundreds of models and providers.

4. **Composability.** AgentBudget should be a building block, not a platform. It produces structured cost data that feeds into whatever observability, billing, or alerting stack you already use.


---

## Summary

AgentBudget exists because AI agents have made software cost unpredictable for the first time. Traditional software has deterministic resource usage — you know how many database queries a request makes. Agent software doesn't. An agent might make 3 LLM calls or 300, use cheap models or expensive ones, invoke 1 tool or 50. This unpredictability is a feature of agents, not a bug — but it requires a new primitive for cost control.

That primitive is a per-session budget with real-time enforcement. AgentBudget is that primitive — nothing more, nothing less.

**Ship your agents with confidence. Set a budget. Move on.**
