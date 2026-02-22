"""
AgentBudget Demo Agents
========================
Real agent code to test AgentBudget with actual OpenAI API calls.

Usage:
    export OPENAI_API_KEY='sk-...'
    python agentbudget_demo_agents.py

Total cost: ~$0.50-1.00
"""

import openai
import agentbudget
import time
import json


# ============================================================
# DEMO 1: Research Agent (Normal Usage)
# ============================================================
# A simple agent that researches a topic by asking multiple
# questions. AgentBudget tracks cost automatically.

def demo_research_agent():
    print("=" * 60)
    print("DEMO 1: Research Agent with $0.50 Budget")
    print("=" * 60)
    
    # Two lines to add AgentBudget
    agentbudget.init("$0.50")
    client = openai.OpenAI()
    
    questions = [
        "What is x402 payment protocol? One paragraph.",
        "What are the main challenges of AI agent cost control?",
        "How does monkey-patching work in Python? Brief.",
        "What is a circuit breaker pattern in software?",
        "Explain EIP-712 typed data signing briefly.",
    ]
    
    print(f"\nStarting research with ${agentbudget.remaining():.2f} budget\n")
    
    for i, q in enumerate(questions):
        try:
            print(f"Q{i+1}: {q}")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": q}],
                max_tokens=150,
            )
            answer = response.choices[0].message.content[:100]
            print(f"A{i+1}: {answer}...")
            print(f"    Spent so far: ${agentbudget.spent():.6f} | "
                  f"Remaining: ${agentbudget.remaining():.6f}\n")
        except agentbudget.BudgetExhausted:
            print(f"  ⛔ Budget exhausted after {i} questions!")
            break
    
    report = agentbudget.teardown()
    print(f"\n--- Session Report ---")
    print(f"Total spent:  ${report['total_spent']:.6f}")
    print(f"Total calls:  {report['breakdown']['llm']['calls']}")
    print(f"By model:     {json.dumps(report['breakdown']['llm']['by_model'], indent=2)}")
    print(f"Terminated:   {report['terminated_by']}")
    return report


# ============================================================
# DEMO 2: Runaway Agent (Budget Saves You)
# ============================================================
# Simulates an agent stuck in a reasoning loop.
# Without AgentBudget: could cost $50+
# With AgentBudget: capped at $0.10

def demo_runaway_agent():
    print("\n" + "=" * 60)
    print("DEMO 2: Runaway Agent (Budget Cap at $0.10)")
    print("=" * 60)
    
    agentbudget.init("$0.10")
    client = openai.OpenAI()
    
    calls = 0
    total_saved = 0
    
    print(f"\nAgent enters infinite retry loop...")
    print(f"Without AgentBudget: could run 1000+ calls (~$5-10)")
    print(f"With AgentBudget: capped at $0.10\n")
    
    # Simulate agent stuck in loop - keeps retrying same task
    for i in range(1000):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a data analyst."},
                    {"role": "user", "content": "Analyze this dataset and find anomalies: [data not found]"},
                ],
                max_tokens=100,
            )
            calls += 1
            if calls % 10 == 0:
                print(f"  Call {calls}: spent=${agentbudget.spent():.6f}")
        except agentbudget.BudgetExhausted:
            print(f"\n  ⛔ BUDGET EXHAUSTED after {calls} calls!")
            print(f"  Spent: ${agentbudget.spent():.6f}")
            print(f"  Calls prevented: {1000 - calls}")
            # Estimate what it would have cost without budget
            cost_per_call = agentbudget.spent() / calls if calls > 0 else 0
            total_saved = cost_per_call * (1000 - calls)
            print(f"  Estimated savings: ${total_saved:.2f}")
            break
        except agentbudget.LoopDetected:
            print(f"\n  🔄 LOOP DETECTED after {calls} calls!")
            print(f"  AgentBudget caught the infinite retry pattern")
            break
    
    report = agentbudget.teardown()
    return report


# ============================================================
# DEMO 3: Multi-Model Agent
# ============================================================
# Agent that uses different models for different tasks
# (cheap model for simple stuff, expensive for complex)

def demo_multi_model_agent():
    print("\n" + "=" * 60)
    print("DEMO 3: Multi-Model Agent with $1.00 Budget")
    print("=" * 60)
    
    agentbudget.init("$1.00")
    client = openai.OpenAI()
    
    tasks = [
        # (model, task description, prompt)
        ("gpt-4o-mini", "Quick classification",
         "Classify this as positive or negative: 'Great product!'"),
        ("gpt-4o-mini", "Simple extraction",
         "Extract the email from: 'Contact us at hello@example.com'"),
        ("gpt-4o", "Complex analysis",
         "Compare REST and GraphQL APIs. Give pros and cons of each in 3 sentences."),
        ("gpt-4o-mini", "Quick formatting",
         "Convert this to JSON: name=John, age=30, city=NYC"),
        ("gpt-4o", "Code generation",
         "Write a Python function to calculate fibonacci numbers with memoization."),
        ("gpt-4o-mini", "Summarization",
         "Summarize in one sentence: Machine learning is a subset of AI that enables systems to learn from data."),
    ]
    
    print(f"\nRunning {len(tasks)} tasks across multiple models\n")
    
    for i, (model, task, prompt) in enumerate(tasks):
        try:
            start = time.perf_counter()
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            elapsed = (time.perf_counter() - start) * 1000
            
            tokens_in = response.usage.prompt_tokens
            tokens_out = response.usage.completion_tokens
            
            print(f"  Task {i+1}: [{model}] {task}")
            print(f"    Tokens: {tokens_in} in / {tokens_out} out | "
                  f"Time: {elapsed:.0f}ms | "
                  f"Total spent: ${agentbudget.spent():.6f}")
        except agentbudget.BudgetExhausted:
            print(f"  ⛔ Budget exhausted at task {i+1}")
            break
    
    report = agentbudget.teardown()
    
    print(f"\n--- Cost Attribution ---")
    print(f"Total: ${report['total_spent']:.6f}")
    if report['breakdown']['llm']['by_model']:
        for model, cost in report['breakdown']['llm']['by_model'].items():
            print(f"  {model}: ${cost:.6f}")
    return report


# ============================================================
# DEMO 4: Agent with Tool Costs
# ============================================================
# Agent that combines LLM calls with external tool costs

def demo_tool_agent():
    print("\n" + "=" * 60)
    print("DEMO 4: Agent with LLM + Tool Costs ($0.50 Budget)")
    print("=" * 60)
    
    agentbudget.init("$0.50", max_repeated_calls=9999)
    client = openai.OpenAI()
    
    # Simulate an agent workflow: search -> analyze -> enrich -> summarize
    workflow = [
        ("llm", "gpt-4o-mini", "Plan a research strategy for finding info about x402 protocol"),
        ("tool", "web_search", 0.01),      # simulated search API cost
        ("tool", "web_search", 0.01),      # second search
        ("llm", "gpt-4o-mini", "Based on search results, what are the key points about x402?"),
        ("tool", "data_enrichment", 0.05),  # simulated enrichment cost
        ("llm", "gpt-4o-mini", "Summarize: x402 enables AI agents to pay for services using HTTP 402"),
        ("tool", "email_api", 0.003),       # simulated email send cost
    ]
    
    print(f"\nRunning 7-step agent workflow\n")
    
    for i, step in enumerate(workflow):
        try:
            if step[0] == "llm":
                _, model, prompt = step
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                )
                print(f"  Step {i+1}: LLM ({model}) - ${agentbudget.spent():.6f} total")
            else:
                _, tool_name, cost = step
                # Track external tool cost
                agentbudget.track(cost=cost, tool_name=tool_name)
                print(f"  Step {i+1}: Tool ({tool_name}, ${cost}) - ${agentbudget.spent():.6f} total")
        except agentbudget.BudgetExhausted:
            print(f"  ⛔ Budget hit at step {i+1}")
            break
    
    report = agentbudget.teardown()
    
    print(f"\n--- Cost Breakdown ---")
    print(f"LLM costs:  ${report['breakdown']['llm']['total']:.6f} ({report['breakdown']['llm']['calls']} calls)")
    print(f"Tool costs: ${report['breakdown']['tools']['total']:.6f} ({report['breakdown']['tools']['calls']} calls)")
    if report['breakdown']['tools']['by_tool']:
        for tool, cost in report['breakdown']['tools']['by_tool'].items():
            print(f"  {tool}: ${cost:.6f}")
    print(f"Total:      ${report['total_spent']:.6f}")
    return report


# ============================================================
# DEMO 5: Soft Limit + Graceful Degradation
# ============================================================
# Agent that switches to cheaper model when approaching budget

def demo_soft_limit_agent():
    print("\n" + "=" * 60)
    print("DEMO 5: Adaptive Agent (Degrades at 80% Budget)")
    print("=" * 60)
    
    model_in_use = {"current": "gpt-4o"}
    
    def on_soft_limit(report):
        print(f"\n  ⚠️  80% budget used! Switching from gpt-4o to gpt-4o-mini\n")
        model_in_use["current"] = "gpt-4o-mini"
    
    agentbudget.init("$0.20", soft_limit=0.8, on_soft_limit=on_soft_limit)
    client = openai.OpenAI()
    
    prompts = [
        "What is distributed computing? Two sentences.",
        "Explain microservices architecture briefly.",
        "What is event-driven architecture? Brief.",
        "Compare SQL and NoSQL in two sentences.",
        "What is CAP theorem? One sentence.",
        "Explain CQRS pattern briefly.",
        "What is serverless computing? Brief.",
        "Compare Kafka and RabbitMQ in one sentence.",
    ]
    
    print(f"\nStarting with {model_in_use['current']}, will degrade at 80%\n")
    
    for i, prompt in enumerate(prompts):
        try:
            model = model_in_use["current"]
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
            )
            print(f"  Q{i+1} [{model}]: spent=${agentbudget.spent():.6f}, "
                  f"remaining=${agentbudget.remaining():.6f}")
        except agentbudget.BudgetExhausted:
            print(f"  ⛔ Budget exhausted after {i} questions")
            break
    
    report = agentbudget.teardown()
    print(f"\n--- Final ---")
    print(f"Total: ${report['total_spent']:.6f}")
    if report['breakdown']['llm']['by_model']:
        for m, c in report['breakdown']['llm']['by_model'].items():
            print(f"  {m}: ${c:.6f}")
    return report


# ============================================================
# RUN ALL DEMOS
# ============================================================
if __name__ == "__main__":
    import os
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Set OPENAI_API_KEY first:")
        print("   export OPENAI_API_KEY='sk-...'")
        exit(1)
    
    print("🚀 AgentBudget Demo Suite")
    print(f"   SDK version: {agentbudget.__version__}")
    print(f"   Estimated total cost: ~$0.50-1.00\n")
    
    all_reports = {}
    
    all_reports["research"] = demo_research_agent()
    all_reports["runaway"] = demo_runaway_agent()
    all_reports["multi_model"] = demo_multi_model_agent()
    all_reports["tools"] = demo_tool_agent()
    all_reports["soft_limit"] = demo_soft_limit_agent()
    
    # Save all reports
    with open("demo_results.json", "w") as f:
        json.dump(all_reports, f, indent=2, default=str)
    
    print("\n" + "=" * 60)
    print("📊 ALL DEMOS COMPLETE")
    print("=" * 60)
    
    total_cost = sum(r.get("total_spent", 0) for r in all_reports.values())
    total_calls = sum(r.get("breakdown", {}).get("llm", {}).get("calls", 0) 
                      for r in all_reports.values())
    
    print(f"\nTotal API cost across all demos: ${total_cost:.4f}")
    print(f"Total LLM calls: {total_calls}")
    print(f"Results saved to demo_results.json")