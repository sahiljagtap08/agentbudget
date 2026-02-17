"""AgentBudget - Real-time cost enforcement for AI agent sessions."""

__version__ = "0.2.2"

from .budget import AgentBudget
from .exceptions import AgentBudgetError, BudgetExhausted, InvalidBudget
from .session import AsyncBudgetSession, BudgetSession, LoopDetected
from .pricing import register_model, register_models

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
    # Pricing
    "register_model",
    "register_models",
    # Drop-in API
    "init",
    "teardown",
    "get_session",
    "spent",
    "remaining",
    "report",
    "track",
]
