"""Tests for the AgentBudget main class."""

import pytest

from agentbudget.budget import AgentBudget, parse_budget
from agentbudget.exceptions import BudgetExhausted, InvalidBudget


class TestParseBudget:
    def test_dollar_string(self):
        assert parse_budget("$5.00") == 5.0

    def test_dollar_string_no_cents(self):
        assert parse_budget("$5") == 5.0

    def test_plain_string(self):
        assert parse_budget("5.00") == 5.0

    def test_float(self):
        assert parse_budget(5.0) == 5.0

    def test_int(self):
        assert parse_budget(5) == 5.0

    def test_with_spaces(self):
        assert parse_budget("  $5.00  ") == 5.0

    def test_zero_raises(self):
        with pytest.raises(InvalidBudget):
            parse_budget("$0.00")

    def test_negative_raises(self):
        with pytest.raises(InvalidBudget):
            parse_budget("-5.00")

    def test_invalid_string_raises(self):
        with pytest.raises(InvalidBudget):
            parse_budget("banana")

    def test_negative_float_raises(self):
        with pytest.raises(InvalidBudget):
            parse_budget(-1.0)


class TestAgentBudget:
    def test_create_with_string(self):
        budget = AgentBudget(max_spend="$5.00")
        assert budget.max_spend == 5.0

    def test_create_with_float(self):
        budget = AgentBudget(max_spend=10.0)
        assert budget.max_spend == 10.0

    def test_session_creates_budget_session(self):
        budget = AgentBudget(max_spend="$5.00")
        with budget.session() as session:
            assert session.remaining == 5.0

    def test_session_custom_id(self):
        budget = AgentBudget(max_spend="$5.00")
        with budget.session(session_id="sess_custom") as session:
            assert session.session_id == "sess_custom"

    def test_session_enforces_budget(self):
        budget = AgentBudget(max_spend="$0.05")
        with pytest.raises(BudgetExhausted):
            with budget.session() as session:
                session.track("a", cost=0.03)
                session.track("b", cost=0.03)

    def test_multiple_sessions_independent(self):
        budget = AgentBudget(max_spend="$5.00")
        with budget.session() as s1:
            s1.track("a", cost=1.0)
        with budget.session() as s2:
            assert s2.remaining == 5.0  # fresh session
