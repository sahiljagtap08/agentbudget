"""Budget ledger — tracks running totals and event history."""

import threading
from typing import Any

from .exceptions import BudgetExhausted
from .types import CostEvent, CostType


class Ledger:
    """Thread-safe running balance tracker for a budget session."""

    def __init__(self, budget: float):
        self._budget = budget
        self._spent = 0.0
        self._events: list[CostEvent] = []
        self._lock = threading.Lock()

    @property
    def budget(self) -> float:
        return self._budget

    @property
    def spent(self) -> float:
        with self._lock:
            return self._spent

    @property
    def remaining(self) -> float:
        with self._lock:
            return self._budget - self._spent

    @property
    def events(self) -> list[CostEvent]:
        with self._lock:
            return list(self._events)

    def record(self, event: CostEvent) -> None:
        """Record a cost event. Raises BudgetExhausted if budget exceeded."""
        with self._lock:
            new_total = self._spent + event.cost
            if new_total > self._budget:
                raise BudgetExhausted(budget=self._budget, spent=new_total)
            self._spent = new_total
            self._events.append(event)

    def would_exceed(self, cost: float) -> bool:
        """Check if a cost would exceed the budget without recording it."""
        with self._lock:
            return (self._spent + cost) > self._budget

    def breakdown(self) -> dict[str, Any]:
        """Return a cost breakdown by type and model/tool."""
        with self._lock:
            llm_total = 0.0
            llm_calls = 0
            by_model: dict[str, float] = {}
            tool_total = 0.0
            tool_calls = 0
            by_tool: dict[str, float] = {}

            for event in self._events:
                if event.cost_type == CostType.LLM:
                    llm_total += event.cost
                    llm_calls += 1
                    if event.model:
                        by_model[event.model] = by_model.get(event.model, 0.0) + event.cost
                elif event.cost_type == CostType.TOOL:
                    tool_total += event.cost
                    tool_calls += 1
                    if event.tool_name:
                        by_tool[event.tool_name] = by_tool.get(event.tool_name, 0.0) + event.cost

            return {
                "llm": {
                    "total": round(llm_total, 6),
                    "calls": llm_calls,
                    "by_model": {k: round(v, 6) for k, v in by_model.items()},
                },
                "tools": {
                    "total": round(tool_total, 6),
                    "calls": tool_calls,
                    "by_tool": {k: round(v, 6) for k, v in by_tool.items()},
                },
            }
