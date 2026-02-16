"""Tests for drop-in auto-instrumentation."""

from __future__ import annotations

import sys
import types
from unittest import mock

import pytest

import agentbudget
from agentbudget._global import _get_session


class FakeUsage:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class FakeResponse:
    def __init__(self, model="gpt-4o", prompt_tokens=100, completion_tokens=50):
        self.model = model
        self.usage = FakeUsage(prompt_tokens, completion_tokens)


# ---- Tests for global API without patching ----

class TestGlobalAPI:
    def setup_method(self):
        agentbudget.teardown()

    def teardown_method(self):
        agentbudget.teardown()

    def test_init_returns_session(self):
        session = agentbudget.init(budget="$5.00")
        assert session is not None
        assert session.remaining == 5.0

    def test_spent_and_remaining(self):
        agentbudget.init(budget="$5.00")
        assert agentbudget.spent() == 0.0
        assert agentbudget.remaining() == 5.0

    def test_track_via_global(self):
        agentbudget.init(budget="$5.00")
        agentbudget.track(cost=0.50, tool_name="my_api")
        assert agentbudget.spent() == 0.50
        assert agentbudget.remaining() == 4.50

    def test_report_via_global(self):
        agentbudget.init(budget="$5.00")
        agentbudget.track(cost=1.0, tool_name="tool")
        r = agentbudget.report()
        assert r is not None
        assert r["total_spent"] == 1.0
        assert r["budget"] == 5.0

    def test_teardown_returns_report(self):
        agentbudget.init(budget="$5.00")
        agentbudget.track(cost=0.25, tool_name="api")
        r = agentbudget.teardown()
        assert r is not None
        assert r["total_spent"] == 0.25

    def test_teardown_clears_state(self):
        agentbudget.init(budget="$5.00")
        agentbudget.teardown()
        assert agentbudget.get_session() is None
        assert agentbudget.spent() == 0.0
        assert agentbudget.report() is None

    def test_double_init_tears_down_first(self):
        agentbudget.init(budget="$5.00")
        agentbudget.track(cost=1.0, tool_name="api")
        # Second init should start fresh
        agentbudget.init(budget="$10.00")
        assert agentbudget.spent() == 0.0
        assert agentbudget.remaining() == 10.0

    def test_track_without_init_raises(self):
        with pytest.raises(RuntimeError, match="init"):
            agentbudget.track(cost=0.01)

    def test_budget_enforcement(self):
        agentbudget.init(budget="$0.10")
        agentbudget.track(cost=0.05)
        with pytest.raises(agentbudget.BudgetExhausted):
            agentbudget.track(cost=0.06)

    def test_get_session_for_manual_use(self):
        agentbudget.init(budget="$5.00")
        session = agentbudget.get_session()
        assert session is not None
        # Can use session.wrap() manually alongside auto-tracking
        response = FakeResponse("gpt-4o", 100, 50)
        session.wrap(response)
        assert agentbudget.spent() > 0


# ---- Tests for monkey-patching mechanism ----

class TestPatching:
    def setup_method(self):
        agentbudget.teardown()

    def teardown_method(self):
        agentbudget.teardown()
        # Clean up fake modules
        for key in list(sys.modules.keys()):
            if key.startswith("openai") or key.startswith("anthropic"):
                if "fake" in str(type(sys.modules[key])):
                    del sys.modules[key]

    def _install_fake_openai(self):
        """Install a fake openai module that mimics the real SDK structure."""
        # Create fake module hierarchy
        openai_mod = types.ModuleType("openai")
        resources_mod = types.ModuleType("openai.resources")
        chat_mod = types.ModuleType("openai.resources.chat")
        completions_mod = types.ModuleType("openai.resources.chat.completions")

        class Completions:
            def create(self, **kwargs):
                return FakeResponse(
                    model=kwargs.get("model", "gpt-4o"),
                    prompt_tokens=100,
                    completion_tokens=50,
                )

        completions_mod.Completions = Completions
        chat_mod.completions = completions_mod
        resources_mod.chat = chat_mod
        openai_mod.resources = resources_mod

        sys.modules["openai"] = openai_mod
        sys.modules["openai.resources"] = resources_mod
        sys.modules["openai.resources.chat"] = chat_mod
        sys.modules["openai.resources.chat.completions"] = completions_mod

        return Completions

    def test_openai_patching(self):
        FakeCompletions = self._install_fake_openai()

        agentbudget.init(budget="$5.00")

        client = FakeCompletions()
        response = client.create(model="gpt-4o")

        assert response.model == "gpt-4o"
        assert agentbudget.spent() > 0

    def test_openai_unpatching(self):
        FakeCompletions = self._install_fake_openai()
        original_create = FakeCompletions.create

        agentbudget.init(budget="$5.00")
        assert FakeCompletions.create is not original_create  # patched

        agentbudget.teardown()
        assert FakeCompletions.create is original_create  # restored

    def test_no_tracking_after_teardown(self):
        FakeCompletions = self._install_fake_openai()

        agentbudget.init(budget="$5.00")
        agentbudget.teardown()

        # After teardown, calls should work but not be tracked
        client = FakeCompletions()
        response = client.create(model="gpt-4o")
        assert response.model == "gpt-4o"
        assert agentbudget.spent() == 0.0

    def test_budget_enforcement_through_patch(self):
        FakeCompletions = self._install_fake_openai()

        agentbudget.init(budget="$0.001")  # very small budget

        client = FakeCompletions()
        # gpt-4o: ~$0.0025 + $0.0005 per call with 100/50 tokens
        # Should exceed $0.001 budget
        with pytest.raises(agentbudget.BudgetExhausted):
            for _ in range(10):
                client.create(model="gpt-4o")
