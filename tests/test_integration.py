"""End-to-end integration tests for AgentBudget."""

import json

import pytest

from agentbudget import AgentBudget, BudgetExhausted


class FakeUsage:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class FakeLLMResponse:
    def __init__(self, model, prompt_tokens, completion_tokens):
        self.model = model
        self.usage = FakeUsage(prompt_tokens, completion_tokens)


def test_full_session_lifecycle():
    """Test the complete workflow from README example."""
    budget = AgentBudget(max_spend="$5.00")

    with budget.session() as session:
        # Simulate an LLM call
        response = FakeLLMResponse("gpt-4o", prompt_tokens=500, completion_tokens=200)
        session.wrap(response)

        # Simulate tool calls
        session.track({"results": ["a", "b"]}, cost=0.01, tool_name="serp_api")
        session.track("<html>...</html>", cost=0.25, tool_name="scrape")

    report = session.report()

    assert report["budget"] == 5.0
    assert report["total_spent"] > 0
    assert report["remaining"] < 5.0
    assert report["terminated_by"] is None
    assert report["duration_seconds"] >= 0
    assert len(report["events"]) == 3
    assert report["breakdown"]["llm"]["calls"] == 1
    assert report["breakdown"]["tools"]["calls"] == 2


def test_budget_enforcement_end_to_end():
    """Test that budget is enforced across mixed LLM and tool calls."""
    budget = AgentBudget(max_spend="$0.10")

    with pytest.raises(BudgetExhausted):
        with budget.session() as session:
            session.track("result1", cost=0.04, tool_name="api_a")
            session.track("result2", cost=0.04, tool_name="api_b")
            session.track("result3", cost=0.04, tool_name="api_c")  # exceeds $0.10


def test_report_is_json_serializable():
    """Cost reports should be serializable for logging/webhooks."""
    budget = AgentBudget(max_spend="$5.00")

    with budget.session() as session:
        response = FakeLLMResponse("gpt-4o", prompt_tokens=100, completion_tokens=50)
        session.wrap(response)
        session.track("data", cost=0.01, tool_name="my_tool")

    report = session.report()
    json_str = json.dumps(report)
    parsed = json.loads(json_str)
    assert parsed["session_id"] == report["session_id"]
    assert parsed["total_spent"] == report["total_spent"]


def test_import_from_top_level():
    """Verify the public API is importable from the top-level package."""
    from agentbudget import (
        AgentBudget,
        AgentBudgetError,
        BudgetExhausted,
        BudgetSession,
        InvalidBudget,
    )
    assert AgentBudget is not None
    assert BudgetExhausted is not None


def test_shorthand_constructor():
    """AgentBudget('$2.00') should work as a quick one-liner."""
    budget = AgentBudget("$2.00")
    assert budget.max_spend == 2.0
