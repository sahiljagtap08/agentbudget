"""Tests for AgentBudget types."""

import time

from agentbudget.types import CostEvent, CostType, generate_session_id


def test_cost_event_llm():
    event = CostEvent(
        cost=0.005,
        cost_type=CostType.LLM,
        model="gpt-4o",
        input_tokens=100,
        output_tokens=50,
    )
    assert event.cost == 0.005
    assert event.cost_type == CostType.LLM
    assert event.model == "gpt-4o"


def test_cost_event_tool():
    event = CostEvent(
        cost=0.01,
        cost_type=CostType.TOOL,
        tool_name="serp_api",
    )
    assert event.cost == 0.01
    assert event.cost_type == CostType.TOOL
    assert event.tool_name == "serp_api"


def test_cost_event_has_timestamp():
    before = time.time()
    event = CostEvent(cost=0.01, cost_type=CostType.TOOL)
    after = time.time()
    assert before <= event.timestamp <= after


def test_cost_event_to_dict():
    event = CostEvent(
        cost=0.005,
        cost_type=CostType.LLM,
        model="gpt-4o",
        input_tokens=100,
        output_tokens=50,
    )
    d = event.to_dict()
    assert d["cost"] == 0.005
    assert d["cost_type"] == "llm"
    assert d["model"] == "gpt-4o"
    assert "tool_name" not in d


def test_cost_event_to_dict_minimal():
    event = CostEvent(cost=0.01, cost_type=CostType.TOOL)
    d = event.to_dict()
    assert "model" not in d
    assert "input_tokens" not in d


def test_generate_session_id_format():
    sid = generate_session_id()
    assert sid.startswith("sess_")
    assert len(sid) == 17  # "sess_" + 12 hex chars


def test_generate_session_id_unique():
    ids = {generate_session_id() for _ in range(100)}
    assert len(ids) == 100
