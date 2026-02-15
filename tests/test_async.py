"""Tests for async session support."""

import asyncio

import pytest

from agentbudget import AgentBudget, AsyncBudgetSession, BudgetExhausted
from agentbudget.ledger import Ledger


class FakeUsage:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class FakeResponse:
    def __init__(self, model, prompt_tokens, completion_tokens):
        self.model = model
        self.usage = FakeUsage(prompt_tokens, completion_tokens)


@pytest.mark.asyncio
async def test_async_context_manager():
    budget = AgentBudget(max_spend="$5.00")
    async with budget.async_session() as session:
        assert isinstance(session, AsyncBudgetSession)
        assert session.remaining == 5.0


@pytest.mark.asyncio
async def test_async_wrap_sync_response():
    budget = AgentBudget(max_spend="$5.00")
    async with budget.async_session() as session:
        response = FakeResponse("gpt-4o", prompt_tokens=1000, completion_tokens=500)
        result = session.wrap(response)
        assert result is response
        assert session.spent > 0


@pytest.mark.asyncio
async def test_async_wrap_async_coroutine():
    async def fake_llm_call():
        return FakeResponse("gpt-4o", prompt_tokens=500, completion_tokens=200)

    budget = AgentBudget(max_spend="$5.00")
    async with budget.async_session() as session:
        response = await session.wrap_async(fake_llm_call())
        assert response.model == "gpt-4o"
        assert session.spent > 0


@pytest.mark.asyncio
async def test_async_track():
    budget = AgentBudget(max_spend="$5.00")
    async with budget.async_session() as session:
        session.track({"data": "result"}, cost=0.01, tool_name="api")
        assert session.spent == 0.01


@pytest.mark.asyncio
async def test_async_budget_enforcement():
    budget = AgentBudget(max_spend="$0.05")
    with pytest.raises(BudgetExhausted):
        async with budget.async_session() as session:
            session.track("a", cost=0.03)
            session.track("b", cost=0.03)


@pytest.mark.asyncio
async def test_async_report():
    budget = AgentBudget(max_spend="$5.00")
    async with budget.async_session() as session:
        session.track("x", cost=0.50, tool_name="tool")

    report = session.report()
    assert report["total_spent"] == 0.50
    assert report["remaining"] == 4.50


@pytest.mark.asyncio
async def test_async_track_tool_decorator():
    budget = AgentBudget(max_spend="$5.00")
    async with budget.async_session() as session:

        @session.track_tool(cost=0.02, tool_name="async_search")
        async def search(query):
            return {"results": [query]}

        result = await search("test")
        assert result == {"results": ["test"]}
        assert session.spent == 0.02
