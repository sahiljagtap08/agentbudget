"""Tests for the pricing module."""

from agentbudget.pricing import (
    MODEL_PRICING,
    calculate_llm_cost,
    get_model_pricing,
)


def test_gpt4o_pricing_exists():
    pricing = get_model_pricing("gpt-4o")
    assert pricing is not None
    input_price, output_price = pricing
    assert input_price > 0
    assert output_price > 0


def test_claude_sonnet_pricing_exists():
    pricing = get_model_pricing("claude-3-5-sonnet-20241022")
    assert pricing is not None


def test_unknown_model_returns_none():
    assert get_model_pricing("nonexistent-model-xyz") is None


def test_calculate_llm_cost_gpt4o():
    # gpt-4o: $2.50/1M input, $10.00/1M output
    cost = calculate_llm_cost("gpt-4o", input_tokens=1000, output_tokens=500)
    assert cost is not None
    expected = (1000 * 2.50 / 1_000_000) + (500 * 10.00 / 1_000_000)
    assert abs(cost - expected) < 1e-10


def test_calculate_llm_cost_gpt4o_mini():
    cost = calculate_llm_cost("gpt-4o-mini", input_tokens=1000, output_tokens=500)
    assert cost is not None
    expected = (1000 * 0.15 / 1_000_000) + (500 * 0.60 / 1_000_000)
    assert abs(cost - expected) < 1e-10


def test_calculate_cost_unknown_model():
    cost = calculate_llm_cost("unknown-model", input_tokens=100, output_tokens=50)
    assert cost is None


def test_gpt4o_cheaper_than_gpt4():
    cost_4o = calculate_llm_cost("gpt-4o", input_tokens=1000, output_tokens=1000)
    cost_4 = calculate_llm_cost("gpt-4", input_tokens=1000, output_tokens=1000)
    assert cost_4o < cost_4


def test_zero_tokens():
    cost = calculate_llm_cost("gpt-4o", input_tokens=0, output_tokens=0)
    assert cost == 0.0


def test_pricing_table_has_both_providers():
    models = list(MODEL_PRICING.keys())
    has_openai = any(m.startswith("gpt") or m.startswith("o1") or m.startswith("o3") for m in models)
    has_anthropic = any(m.startswith("claude") for m in models)
    assert has_openai
    assert has_anthropic
