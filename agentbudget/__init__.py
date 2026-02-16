"""AgentBudget - Real-time cost enforcement for AI agent sessions."""

__version__ = "0.1.0"

from .budget import AgentBudget
from .exceptions import AgentBudgetError, BudgetExhausted, InvalidBudget
from .session import AsyncBudgetSession, BudgetSession, LoopDetected

# Drop-in auto-instrumentation API
from ._global import (
    init,
    teardown,
    get_session,
    spent,
    remaining,
    report,
    track,
)

__all__ = [
    # Core classes
    "AgentBudget",
    "AgentBudgetError",
    "AsyncBudgetSession",
    "BudgetExhausted",
    "BudgetSession",
    "InvalidBudget",
    "LoopDetected",
    # Drop-in API
    "init",
    "teardown",
    "get_session",
    "spent",
    "remaining",
    "report",
    "track",
]
