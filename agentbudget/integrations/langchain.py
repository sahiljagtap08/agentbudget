"""LangChain/LangGraph integration for AgentBudget.

Provides a callback handler that tracks LLM costs automatically.

Usage:
    from agentbudget.integrations.langchain import LangChainBudgetCallback

    callback = LangChainBudgetCallback(budget="$5.00")
    agent.run(callbacks=[callback])

    print(callback.session.report())

Requires: langchain-core (optional dependency)
"""

from __future__ import annotations

from typing import Any, Optional

from ..budget import AgentBudget, parse_budget
from ..ledger import Ledger
from ..pricing import calculate_llm_cost
from ..session import BudgetSession
from ..types import CostEvent, CostType

try:
    from langchain_core.callbacks import BaseCallbackHandler

    _HAS_LANGCHAIN = True
except ImportError:
    _HAS_LANGCHAIN = False

    # Provide a stub so the class definition doesn't fail at import
    class BaseCallbackHandler:  # type: ignore[no-redef]
        pass


class LangChainBudgetCallback(BaseCallbackHandler):
    """LangChain callback handler that enforces a per-run budget.

    Tracks LLM call costs in real time and raises BudgetExhausted
    when the budget is exceeded.
    """

    def __init__(
        self,
        budget: str | float | int,
        session: Optional[BudgetSession] = None,
        **kwargs: Any,
    ):
        if not _HAS_LANGCHAIN:
            raise ImportError(
                "langchain-core is required for LangChainBudgetCallback. "
                "Install it with: pip install langchain-core"
            )
        super().__init__(**kwargs)
        self._agent_budget = AgentBudget(max_spend=budget)
        self.session = session or self._agent_budget.session()
        self.session.__enter__()

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Called when an LLM call finishes. Records the cost."""
        llm_output = getattr(response, "llm_output", None) or {}
        token_usage = llm_output.get("token_usage", {})
        model_name = llm_output.get("model_name")

        input_tokens = token_usage.get("prompt_tokens")
        output_tokens = token_usage.get("completion_tokens")

        if model_name and input_tokens is not None and output_tokens is not None:
            cost = calculate_llm_cost(model_name, input_tokens, output_tokens)
            if cost is not None:
                event = CostEvent(
                    cost=cost,
                    cost_type=CostType.LLM,
                    model=model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                )
                self.session._ledger.record(event)
                self.session._check_after_record(call_key=model_name)

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Called when a tool finishes. Override to add cost tracking."""
        pass

    def get_report(self) -> dict[str, Any]:
        """Get the cost report for this callback's session."""
        return self.session.report()
