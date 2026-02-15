"""Tests for nested budget sessions."""

import pytest

from agentbudget import AgentBudget, BudgetExhausted


def test_child_session_basic():
    budget = AgentBudget(max_spend="$10.00")
    with budget.session() as parent:
        child = parent.child_session(max_spend=2.0)
        with child:
            child.track("result", cost=0.50, tool_name="sub_task")

        # Child spend should roll up to parent
        assert child.spent == 0.50
        assert parent.spent == 0.50


def test_child_session_capped_by_parent_remaining():
    budget = AgentBudget(max_spend="$5.00")
    with budget.session() as parent:
        parent.track("x", cost=4.50)
        child = parent.child_session(max_spend=2.0)
        # Child budget should be capped at parent's remaining $0.50
        assert child.remaining == 0.50


def test_child_session_enforces_own_budget():
    budget = AgentBudget(max_spend="$10.00")
    with budget.session() as parent:
        child = parent.child_session(max_spend=0.10)
        with pytest.raises(BudgetExhausted):
            with child:
                child.track("a", cost=0.06)
                child.track("b", cost=0.06)  # exceeds child's $0.10


def test_child_spend_rolls_up_to_parent():
    budget = AgentBudget(max_spend="$10.00")
    with budget.session() as parent:
        parent.track("direct", cost=1.00)

        child1 = parent.child_session(max_spend=3.0)
        with child1:
            child1.track("a", cost=0.50, tool_name="tool_a")
            child1.track("b", cost=0.25, tool_name="tool_b")

        child2 = parent.child_session(max_spend=3.0)
        with child2:
            child2.track("c", cost=1.00, tool_name="tool_c")

        # parent: 1.00 direct + 0.75 child1 + 1.00 child2 = 2.75
        assert abs(parent.spent - 2.75) < 1e-10


def test_child_report_independent():
    budget = AgentBudget(max_spend="$10.00")
    with budget.session() as parent:
        child = parent.child_session(max_spend=2.0, session_id="sess_child")
        with child:
            child.track("x", cost=0.30, tool_name="sub")

        child_report = child.report()
        assert child_report["session_id"] == "sess_child"
        assert child_report["budget"] == 2.0
        assert child_report["total_spent"] == 0.30

        parent_report = parent.report()
        assert parent_report["total_spent"] == 0.30


def test_nested_three_levels():
    budget = AgentBudget(max_spend="$10.00")
    with budget.session() as grandparent:
        child = grandparent.child_session(max_spend=5.0)
        with child:
            grandchild = child.child_session(max_spend=2.0)
            with grandchild:
                grandchild.track("deep", cost=0.10, tool_name="deep_tool")

            assert child.spent == 0.10

        assert grandparent.spent == 0.10
