"""Tests for the pricing module."""

from agentbudget.pricing import (
    MODEL_PRICING,
    _custom_pricing,
    calculate_llm_cost,
    get_model_pricing,
    register_model,
    register_models,
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


# ── Custom model registration ─────────────────────────────────────


def test_register_model():
    _custom_pricing.clear()
    register_model("gpt-5", input_price_per_million=5.00, output_price_per_million=20.00)
    pricing = get_model_pricing("gpt-5")
    assert pricing is not None
    inp, out = pricing
    assert abs(inp - 5.00 / 1_000_000) < 1e-15
    assert abs(out - 20.00 / 1_000_000) < 1e-15
    _custom_pricing.clear()


def test_register_model_overrides_builtin():
    _custom_pricing.clear()
    # Override gpt-4o with custom pricing
    register_model("gpt-4o", input_price_per_million=99.00, output_price_per_million=99.00)
    pricing = get_model_pricing("gpt-4o")
    assert pricing is not None
    inp, out = pricing
    assert abs(inp - 99.00 / 1_000_000) < 1e-15
    _custom_pricing.clear()


def test_register_models_batch():
    _custom_pricing.clear()
    register_models({
        "gpt-5": (5.00, 20.00),
        "gpt-5-mini": (0.50, 2.00),
    })
    assert get_model_pricing("gpt-5") is not None
    assert get_model_pricing("gpt-5-mini") is not None
    cost = calculate_llm_cost("gpt-5", input_tokens=1000, output_tokens=500)
    assert cost is not None
    expected = (1000 * 5.00 / 1_000_000) + (500 * 20.00 / 1_000_000)
    assert abs(cost - expected) < 1e-10
    _custom_pricing.clear()


def test_register_model_works_with_calculate():
    _custom_pricing.clear()
    register_model("my-custom-model", input_price_per_million=10.00, output_price_per_million=30.00)
    cost = calculate_llm_cost("my-custom-model", input_tokens=1_000_000, output_tokens=500_000)
    assert cost is not None
    assert abs(cost - (10.00 + 15.00)) < 1e-10
    _custom_pricing.clear()


# ── Fuzzy matching ─────────────────────────────────────────────────


def test_fuzzy_match_dated_variant():
    # gpt-4o exists in built-in pricing, so gpt-4o-2025-03-01 should match
    pricing = get_model_pricing("gpt-4o-2025-03-01")
    assert pricing is not None
    base_pricing = get_model_pricing("gpt-4o")
    assert pricing == base_pricing


def test_fuzzy_match_custom_model():
    _custom_pricing.clear()
    register_model("my-model", input_price_per_million=1.00, output_price_per_million=3.00)
    # my-model-v2 should fuzzy match to my-model
    pricing = get_model_pricing("my-model-v2")
    assert pricing is not None
    assert pricing == get_model_pricing("my-model")
    _custom_pricing.clear()


def test_fuzzy_match_no_match():
    _custom_pricing.clear()
    assert get_model_pricing("totally-unknown-model-2025") is None


def test_fuzzy_match_gemini_dated():
    # gemini-1.5-pro exists as a base, so a dated variant should match
    pricing = get_model_pricing("gemini-1.5-pro-002")
    assert pricing is not None
    assert pricing == get_model_pricing("gemini-1.5-pro")
