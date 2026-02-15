"""CrewAI integration for AgentBudget.

Provides middleware that tracks costs for CrewAI agent runs.

Usage:
    from agentbudget.integrations.crewai import CrewAIBudgetMiddleware

    middleware = CrewAIBudgetMiddleware(budget="$3.00")
    # Use middleware.session to track costs in your CrewAI setup

Requires: crewai (optional dependency)
"""

from __future__ import annotations

from typing import Any, Optional

from ..budget import AgentBudget
from ..session import BudgetSession


class CrewAIBudgetMiddleware:
    """Budget middleware for CrewAI agent runs.

    Wraps a CrewAI execution with a budget session. Use the
    `session` attribute to track costs within your CrewAI callbacks.
    """

    def __init__(
        self,
        budget: str | float | int,
        session_id: Optional[str] = None,
        on_soft_limit: Optional[Any] = None,
        on_hard_limit: Optional[Any] = None,
        on_loop_detected: Optional[Any] = None,
    ):
        self._agent_budget = AgentBudget(
            max_spend=budget,
            on_soft_limit=on_soft_limit,
            on_hard_limit=on_hard_limit,
            on_loop_detected=on_loop_detected,
        )
        self.session = self._agent_budget.session(session_id=session_id)

    def __enter__(self) -> "CrewAIBudgetMiddleware":
        self.session.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self.session.__exit__(*args)

    def get_report(self) -> dict[str, Any]:
        """Get the cost report for this middleware's session."""
        return self.session.report()

    def track(
        self,
        result: Any,
        cost: float,
        tool_name: Optional[str] = None,
    ) -> Any:
        """Track a cost within the CrewAI execution."""
        return self.session.track(result, cost=cost, tool_name=tool_name)
