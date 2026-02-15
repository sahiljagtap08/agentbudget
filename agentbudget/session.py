"""Budget session — context manager that wraps LLM and tool calls."""

import time
from typing import Any, Optional, TypeVar

from .ledger import Ledger
from .pricing import calculate_llm_cost
from .types import CostEvent, CostType, generate_session_id

T = TypeVar("T")


class BudgetSession:
    """Tracks costs for a single agent session.

    Used as a context manager:
        with budget.session() as session:
            response = session.wrap(openai_call(...))
            session.track(tool_call(), cost=0.01)
    """

    def __init__(self, ledger: Ledger, session_id: Optional[str] = None):
        self._ledger = ledger
        self._session_id = session_id or generate_session_id()
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._terminated_by: Optional[str] = None

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def spent(self) -> float:
        return self._ledger.spent

    @property
    def remaining(self) -> float:
        return self._ledger.remaining

    def __enter__(self) -> "BudgetSession":
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._end_time = time.time()
        if exc_type and exc_type.__name__ == "BudgetExhausted":
            self._terminated_by = "budget_exhausted"

    def wrap(self, response: T) -> T:
        """Wrap an LLM API response and record its cost.

        Extracts model and token usage from the response object.
        Supports OpenAI-style response objects with a `usage` attribute.
        """
        model = _extract_model(response)
        input_tokens, output_tokens = _extract_usage(response)

        cost = None
        if model and input_tokens is not None and output_tokens is not None:
            cost = calculate_llm_cost(model, input_tokens, output_tokens)

        if cost is not None:
            event = CostEvent(
                cost=cost,
                cost_type=CostType.LLM,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )
            self._ledger.record(event)

        return response

    def track(
        self,
        result: T,
        cost: float,
        tool_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> T:
        """Track a tool/API call with a known cost.

        Returns the result passthrough so it can be used inline:
            data = session.track(call_api(), cost=0.01, tool_name="my_api")
        """
        event = CostEvent(
            cost=cost,
            cost_type=CostType.TOOL,
            tool_name=tool_name,
            metadata=metadata,
        )
        self._ledger.record(event)
        return result

    def report(self) -> dict[str, Any]:
        """Generate a structured cost report for this session."""
        duration = None
        if self._start_time:
            end = self._end_time or time.time()
            duration = round(end - self._start_time, 2)

        return {
            "session_id": self._session_id,
            "budget": self._ledger.budget,
            "total_spent": round(self._ledger.spent, 6),
            "remaining": round(self._ledger.remaining, 6),
            "breakdown": self._ledger.breakdown(),
            "duration_seconds": duration,
            "terminated_by": self._terminated_by,
            "events": [e.to_dict() for e in self._ledger.events],
        }


def _extract_model(response: Any) -> Optional[str]:
    """Extract model name from an LLM response object."""
    return getattr(response, "model", None)


def _extract_usage(response: Any) -> tuple[Optional[int], Optional[int]]:
    """Extract token usage from an LLM response object."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return None, None
    input_tokens = getattr(usage, "prompt_tokens", None)
    output_tokens = getattr(usage, "completion_tokens", None)
    return input_tokens, output_tokens
