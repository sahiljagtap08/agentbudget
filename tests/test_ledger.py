"""Tests for the budget ledger."""

import pytest

from agentbudget.exceptions import BudgetExhausted
from agentbudget.ledger import Ledger
from agentbudget.types import CostEvent, CostType


def test_initial_state():
    ledger = Ledger(budget=5.0)
    assert ledger.budget == 5.0
    assert ledger.spent == 0.0
    assert ledger.remaining == 5.0
    assert ledger.events == []


def test_record_event():
    ledger = Ledger(budget=5.0)
    event = CostEvent(cost=1.0, cost_type=CostType.LLM, model="gpt-4o")
    ledger.record(event)
    assert ledger.spent == 1.0
    assert ledger.remaining == 4.0
    assert len(ledger.events) == 1


def test_record_multiple_events():
    ledger = Ledger(budget=5.0)
    ledger.record(CostEvent(cost=1.0, cost_type=CostType.LLM, model="gpt-4o"))
    ledger.record(CostEvent(cost=0.5, cost_type=CostType.TOOL, tool_name="serp"))
    ledger.record(CostEvent(cost=2.0, cost_type=CostType.LLM, model="gpt-4o"))
    assert ledger.spent == 3.5
    assert ledger.remaining == 1.5
    assert len(ledger.events) == 3


def test_budget_exhausted():
    ledger = Ledger(budget=1.0)
    ledger.record(CostEvent(cost=0.5, cost_type=CostType.LLM))
    with pytest.raises(BudgetExhausted) as exc_info:
        ledger.record(CostEvent(cost=0.6, cost_type=CostType.LLM))
    assert exc_info.value.budget == 1.0
    assert exc_info.value.spent == 1.1


def test_exact_budget_allowed():
    ledger = Ledger(budget=1.0)
    ledger.record(CostEvent(cost=1.0, cost_type=CostType.LLM))
    assert ledger.remaining == 0.0


def test_would_exceed():
    ledger = Ledger(budget=1.0)
    ledger.record(CostEvent(cost=0.8, cost_type=CostType.LLM))
    assert ledger.would_exceed(0.3) is True
    assert ledger.would_exceed(0.2) is False
    assert ledger.would_exceed(0.1) is False


def test_breakdown():
    ledger = Ledger(budget=10.0)
    ledger.record(CostEvent(cost=1.0, cost_type=CostType.LLM, model="gpt-4o"))
    ledger.record(CostEvent(cost=0.5, cost_type=CostType.LLM, model="gpt-4o-mini"))
    ledger.record(CostEvent(cost=2.0, cost_type=CostType.LLM, model="gpt-4o"))
    ledger.record(CostEvent(cost=0.01, cost_type=CostType.TOOL, tool_name="serp_api"))
    ledger.record(CostEvent(cost=0.25, cost_type=CostType.TOOL, tool_name="scrape"))

    bd = ledger.breakdown()
    assert bd["llm"]["total"] == 3.5
    assert bd["llm"]["calls"] == 3
    assert bd["llm"]["by_model"]["gpt-4o"] == 3.0
    assert bd["llm"]["by_model"]["gpt-4o-mini"] == 0.5
    assert bd["tools"]["total"] == 0.26
    assert bd["tools"]["calls"] == 2
    assert bd["tools"]["by_tool"]["serp_api"] == 0.01


def test_events_returns_copy():
    ledger = Ledger(budget=5.0)
    ledger.record(CostEvent(cost=1.0, cost_type=CostType.LLM))
    events = ledger.events
    events.clear()
    assert len(ledger.events) == 1
