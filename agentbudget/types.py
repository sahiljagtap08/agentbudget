"""Data types for AgentBudget."""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class CostType(Enum):
    """Category of cost event."""

    LLM = "llm"
    TOOL = "tool"


@dataclass
class CostEvent:
    """A single costed action within a session."""

    cost: float
    cost_type: CostType
    timestamp: float = field(default_factory=time.time)
    model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    tool_name: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "cost": self.cost,
            "cost_type": self.cost_type.value,
            "timestamp": self.timestamp,
        }
        if self.model is not None:
            d["model"] = self.model
        if self.input_tokens is not None:
            d["input_tokens"] = self.input_tokens
        if self.output_tokens is not None:
            d["output_tokens"] = self.output_tokens
        if self.tool_name is not None:
            d["tool_name"] = self.tool_name
        if self.metadata is not None:
            d["metadata"] = self.metadata
        return d


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return f"sess_{uuid.uuid4().hex[:12]}"
