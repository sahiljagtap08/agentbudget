"""AgentBudget — top-level API for creating budget-enforced sessions."""

from typing import Callable, Optional

from .circuit_breaker import CircuitBreaker, LoopDetectorConfig
from .exceptions import InvalidBudget
from .ledger import Ledger
from .session import AsyncBudgetSession, BudgetSession


def parse_budget(value: str | float | int) -> float:
    """Parse a budget value into a float.

    Accepts:
        "$5.00", "$5", "5.00", "5", 5.0, 5
    """
    if isinstance(value, (int, float)):
        if value <= 0:
            raise InvalidBudget(str(value))
        return float(value)

    if isinstance(value, str):
        cleaned = value.strip().lstrip("$").strip()
        try:
            amount = float(cleaned)
        except ValueError:
            raise InvalidBudget(value)
        if amount <= 0:
            raise InvalidBudget(value)
        return amount

    raise InvalidBudget(str(value))


class AgentBudget:
    """Create budget-enforced agent sessions.

    Usage:
        budget = AgentBudget(max_spend="$5.00")
        with budget.session() as session:
            response = session.wrap(llm_call(...))
            session.track(tool_call(), cost=0.01)
        print(session.report())
    """

    def __init__(
        self,
        max_spend: str | float | int,
        soft_limit: float = 0.9,
        max_repeated_calls: int = 10,
        loop_window_seconds: float = 60.0,
        on_soft_limit: Optional[Callable] = None,
        on_hard_limit: Optional[Callable] = None,
        on_loop_detected: Optional[Callable] = None,
    ):
        self._budget = parse_budget(max_spend)
        self._soft_limit = soft_limit
        self._loop_config = LoopDetectorConfig(
            max_repeated_calls=max_repeated_calls,
            time_window_seconds=loop_window_seconds,
        )
        self._on_soft_limit = on_soft_limit
        self._on_hard_limit = on_hard_limit
        self._on_loop_detected = on_loop_detected

    @property
    def max_spend(self) -> float:
        return self._budget

    def session(self, session_id: Optional[str] = None) -> BudgetSession:
        """Create a new budget session."""
        ledger = Ledger(budget=self._budget)
        circuit_breaker = CircuitBreaker(
            soft_limit_fraction=self._soft_limit,
            loop_config=self._loop_config,
        )
        return BudgetSession(
            ledger=ledger,
            session_id=session_id,
            circuit_breaker=circuit_breaker,
            on_soft_limit=self._on_soft_limit,
            on_hard_limit=self._on_hard_limit,
            on_loop_detected=self._on_loop_detected,
        )

    def async_session(self, session_id: Optional[str] = None) -> AsyncBudgetSession:
        """Create a new async budget session."""
        ledger = Ledger(budget=self._budget)
        circuit_breaker = CircuitBreaker(
            soft_limit_fraction=self._soft_limit,
            loop_config=self._loop_config,
        )
        return AsyncBudgetSession(
            ledger=ledger,
            session_id=session_id,
            circuit_breaker=circuit_breaker,
            on_soft_limit=self._on_soft_limit,
            on_hard_limit=self._on_hard_limit,
            on_loop_detected=self._on_loop_detected,
        )
