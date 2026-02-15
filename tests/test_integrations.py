"""Tests for framework integrations."""

import pytest

from agentbudget import AgentBudget, BudgetExhausted
from agentbudget.integrations.crewai import CrewAIBudgetMiddleware


def test_langchain_import_without_langchain():
    """Should raise ImportError when langchain-core is not installed."""
    from agentbudget.integrations.langchain import LangChainBudgetCallback

    with pytest.raises(ImportError, match="langchain-core"):
        LangChainBudgetCallback(budget="$5.00")


class TestCrewAIMiddleware:
    def test_basic_creation(self):
        mw = CrewAIBudgetMiddleware(budget="$5.00")
        assert mw.session.remaining == 5.0

    def test_context_manager(self):
        with CrewAIBudgetMiddleware(budget="$5.00") as mw:
            mw.track("result", cost=0.50, tool_name="search")
            assert mw.session.spent == 0.50

    def test_budget_enforcement(self):
        with pytest.raises(BudgetExhausted):
            with CrewAIBudgetMiddleware(budget="$0.10") as mw:
                mw.track("a", cost=0.06)
                mw.track("b", cost=0.06)

    def test_report(self):
        with CrewAIBudgetMiddleware(budget="$5.00", session_id="sess_crew") as mw:
            mw.track("x", cost=1.0, tool_name="tool")

        report = mw.get_report()
        assert report["session_id"] == "sess_crew"
        assert report["total_spent"] == 1.0

    def test_callbacks(self):
        warnings = []
        with CrewAIBudgetMiddleware(
            budget="$1.00",
            on_soft_limit=lambda r: warnings.append(r),
        ) as mw:
            mw.track("x", cost=0.95, tool_name="tool")

        assert len(warnings) == 1
