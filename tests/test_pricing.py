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


def test_pricing_table_has_all_providers():
    models = list(MODEL_PRICING.keys())
    has_openai = any(m.startswith("gpt") or m.startswith("o1") or m.startswith("o3") for m in models)
    has_anthropic = any(m.startswith("claude") for m in models)
    has_google = any(m.startswith("gemini") for m in models)
    has_mistral = any("mistral" in m or m.startswith("codestral") for m in models)
    has_cohere = any(m.startswith("command") for m in models)
    assert has_openai
    assert has_anthropic
    assert has_google
    assert has_mistral
    assert has_cohere


def test_gemini_pricing():
    pricing = get_model_pricing("gemini-1.5-pro")
    assert pricing is not None
    cost = calculate_llm_cost("gemini-1.5-pro", input_tokens=1000, output_tokens=500)
    assert cost is not None
    assert cost > 0


def test_mistral_pricing():
    pricing = get_model_pricing("mistral-large-latest")
    assert pricing is not None
    cost = calculate_llm_cost("mistral-large-latest", input_tokens=1000, output_tokens=500)
    assert cost is not None
    assert cost > 0


def test_cohere_pricing():
    pricing = get_model_pricing("command-r-plus")
    assert pricing is not None
    cost = calculate_llm_cost("command-r-plus", input_tokens=1000, output_tokens=500)
    assert cost is not None
    assert cost > 0


def test_gemini_flash_cheaper_than_pro():
    cost_flash = calculate_llm_cost("gemini-1.5-flash", input_tokens=1000, output_tokens=1000)
    cost_pro = calculate_llm_cost("gemini-1.5-pro", input_tokens=1000, output_tokens=1000)
    assert cost_flash < cost_pro
