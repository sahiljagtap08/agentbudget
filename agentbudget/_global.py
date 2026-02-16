"""Global state for drop-in auto-instrumentation.

Usage:
    import agentbudget
    agentbudget.init(budget="$5.00")

    # All OpenAI/Anthropic calls are now tracked automatically
    client = openai.OpenAI()
    response = client.chat.completions.create(...)

    print(agentbudget.spent())
    print(agentbudget.remaining())
    print(agentbudget.report())

    agentbudget.teardown()
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from .budget import AgentBudget
from .session import BudgetSession
from ._patch import patch_openai, patch_anthropic, unpatch_all

_current_budget: Optional[AgentBudget] = None
_current_session: Optional[BudgetSession] = None


def _get_session() -> Optional[BudgetSession]:
    """Get the active global session. Used by patched methods."""
    return _current_session


def init(
    budget: str | float | int,
    soft_limit: float = 0.9,
    max_repeated_calls: int = 10,
    loop_window_seconds: float = 60.0,
    on_soft_limit: Optional[Callable] = None,
    on_hard_limit: Optional[Callable] = None,
    on_loop_detected: Optional[Callable] = None,
    webhook_url: Optional[str] = None,
    session_id: Optional[str] = None,
) -> BudgetSession:
    """Initialize global budget tracking with auto-instrumentation.

    Patches OpenAI and Anthropic clients so every LLM call is
    automatically tracked. Call teardown() to stop tracking.

    Returns the active BudgetSession for manual tracking if needed.
    """
    global _current_budget, _current_session

    # Teardown any existing session
    if _current_session is not None:
        teardown()

    _current_budget = AgentBudget(
        max_spend=budget,
        soft_limit=soft_limit,
        max_repeated_calls=max_repeated_calls,
        loop_window_seconds=loop_window_seconds,
        on_soft_limit=on_soft_limit,
        on_hard_limit=on_hard_limit,
        on_loop_detected=on_loop_detected,
        webhook_url=webhook_url,
    )
    _current_session = _current_budget.session(session_id=session_id)
    _current_session.__enter__()

    # Patch available SDKs
    patch_openai(_get_session)
    patch_anthropic(_get_session)

    return _current_session


def teardown() -> Optional[dict[str, Any]]:
    """Stop tracking and unpatch all clients.

    Returns the final cost report, or None if not initialized.
    """
    global _current_budget, _current_session

    report = None
    if _current_session is not None:
        _current_session.__exit__(None, None, None)
        report = _current_session.report()

    unpatch_all()
    _current_session = None
    _current_budget = None

    return report


def get_session() -> Optional[BudgetSession]:
    """Get the active global session."""
    return _current_session


def spent() -> float:
    """Get total amount spent in the current session."""
    if _current_session is None:
        return 0.0
    return _current_session.spent


def remaining() -> float:
    """Get remaining budget in the current session."""
    if _current_session is None:
        return 0.0
    return _current_session.remaining


def report() -> Optional[dict[str, Any]]:
    """Get the cost report for the current session."""
    if _current_session is None:
        return None
    return _current_session.report()


def track(
    result: Any = None,
    cost: float = 0.0,
    tool_name: Optional[str] = None,
) -> Any:
    """Track a tool/API call cost in the global session."""
    if _current_session is None:
        raise RuntimeError("agentbudget.init() must be called before tracking costs")
    return _current_session.track(result, cost=cost, tool_name=tool_name)
