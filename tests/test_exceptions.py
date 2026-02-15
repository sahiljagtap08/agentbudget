"""Tests for AgentBudget exceptions."""

import pytest

from agentbudget.exceptions import AgentBudgetError, BudgetExhausted, InvalidBudget


def test_budget_exhausted_is_agent_budget_error():
    exc = BudgetExhausted(budget=5.0, spent=5.01)
    assert isinstance(exc, AgentBudgetError)


def test_budget_exhausted_message():
    exc = BudgetExhausted(budget=5.0, spent=5.0123)
    assert "5.0123" in str(exc)
    assert "5.00" in str(exc)


def test_budget_exhausted_attributes():
    exc = BudgetExhausted(budget=10.0, spent=10.5)
    assert exc.budget == 10.0
    assert exc.spent == 10.5


def test_invalid_budget_message():
    exc = InvalidBudget("banana")
    assert "banana" in str(exc)


def test_invalid_budget_is_agent_budget_error():
    exc = InvalidBudget("bad")
    assert isinstance(exc, AgentBudgetError)


def test_budget_exhausted_is_catchable():
    with pytest.raises(BudgetExhausted):
        raise BudgetExhausted(budget=1.0, spent=1.01)
