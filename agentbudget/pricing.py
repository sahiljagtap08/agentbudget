"""Model pricing data for LLM cost calculation.

Prices are per token in USD. Updated February 2026.
"""

from __future__ import annotations

from typing import Optional

# Mapping of model name -> (input_price_per_token, output_price_per_token)
MODEL_PRICING: dict[str, tuple[float, float]] = {
    # ── OpenAI ──────────────────────────────────────────────
    "gpt-4o": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "gpt-4o-2024-11-20": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "gpt-4o-2024-08-06": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "gpt-4o-mini": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "gpt-4o-mini-2024-07-18": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "gpt-4.1": (2.00 / 1_000_000, 8.00 / 1_000_000),
    "gpt-4.1-mini": (0.40 / 1_000_000, 1.60 / 1_000_000),
    "gpt-4.1-nano": (0.10 / 1_000_000, 0.40 / 1_000_000),
    "gpt-4-turbo": (10.00 / 1_000_000, 30.00 / 1_000_000),
    "gpt-4-turbo-2024-04-09": (10.00 / 1_000_000, 30.00 / 1_000_000),
    "gpt-4": (30.00 / 1_000_000, 60.00 / 1_000_000),
    "gpt-3.5-turbo": (0.50 / 1_000_000, 1.50 / 1_000_000),
    "o1": (15.00 / 1_000_000, 60.00 / 1_000_000),
    "o1-mini": (3.00 / 1_000_000, 12.00 / 1_000_000),
    "o1-preview": (15.00 / 1_000_000, 60.00 / 1_000_000),
    "o3": (2.00 / 1_000_000, 8.00 / 1_000_000),
    "o3-mini": (1.10 / 1_000_000, 4.40 / 1_000_000),
    "o3-pro": (20.00 / 1_000_000, 80.00 / 1_000_000),
    "o4-mini": (1.10 / 1_000_000, 4.40 / 1_000_000),
    # ── Anthropic ───────────────────────────────────────────
    "claude-opus-4-6": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-opus-4-5": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-sonnet-4-5-20250929": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-sonnet-4": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-haiku-4-5-20251001": (1.00 / 1_000_000, 5.00 / 1_000_000),
    "claude-opus-4-20250514": (15.00 / 1_000_000, 75.00 / 1_000_000),
    "claude-3-5-sonnet-20241022": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-3-5-sonnet-20240620": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-3-5-haiku-20241022": (0.80 / 1_000_000, 4.00 / 1_000_000),
    "claude-3-opus-20240229": (15.00 / 1_000_000, 75.00 / 1_000_000),
    "claude-3-sonnet-20240229": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-3-haiku-20240307": (0.25 / 1_000_000, 1.25 / 1_000_000),
    # ── Google Gemini ───────────────────────────────────────
    "gemini-2.5-pro": (1.25 / 1_000_000, 10.00 / 1_000_000),
    "gemini-2.5-flash": (0.30 / 1_000_000, 2.50 / 1_000_000),
    "gemini-2.5-flash-lite": (0.10 / 1_000_000, 0.40 / 1_000_000),
    "gemini-2.0-flash": (0.10 / 1_000_000, 0.40 / 1_000_000),
    "gemini-2.0-flash-lite": (0.075 / 1_000_000, 0.30 / 1_000_000),
    "gemini-1.5-pro": (1.25 / 1_000_000, 5.00 / 1_000_000),
    "gemini-1.5-pro-latest": (1.25 / 1_000_000, 5.00 / 1_000_000),
    "gemini-1.5-flash": (0.075 / 1_000_000, 0.30 / 1_000_000),
    "gemini-1.5-flash-latest": (0.075 / 1_000_000, 0.30 / 1_000_000),
    "gemini-1.0-pro": (0.50 / 1_000_000, 1.50 / 1_000_000),
    # ── Mistral ─────────────────────────────────────────────
    "mistral-large-latest": (0.50 / 1_000_000, 1.50 / 1_000_000),
    "mistral-small-latest": (0.03 / 1_000_000, 0.11 / 1_000_000),
    "mistral-medium-latest": (0.40 / 1_000_000, 2.00 / 1_000_000),
    "codestral-latest": (0.30 / 1_000_000, 0.90 / 1_000_000),
    "open-mistral-nemo": (0.02 / 1_000_000, 0.04 / 1_000_000),
    # ── Cohere ──────────────────────────────────────────────
    "command-r-plus": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "command-r": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "command-light": (0.30 / 1_000_000, 0.60 / 1_000_000),
    "command": (1.00 / 1_000_000, 2.00 / 1_000_000),
}


_custom_pricing: dict[str, tuple[float, float]] = {}


def register_model(
    model: str,
    input_price_per_million: float,
    output_price_per_million: float,
) -> None:
    """Register custom pricing for a model.

    Use this when a new model launches before AgentBudget ships an update,
    or to override built-in pricing.

    Args:
        model: Model name exactly as passed to the provider SDK.
        input_price_per_million: Cost in USD per 1M input tokens.
        output_price_per_million: Cost in USD per 1M output tokens.

    Example::

        agentbudget.register_model("gpt-5", input_price_per_million=5.00, output_price_per_million=15.00)
    """
    _custom_pricing[model] = (
        input_price_per_million / 1_000_000,
        output_price_per_million / 1_000_000,
    )


def register_models(models: dict[str, tuple[float, float]]) -> None:
    """Register pricing for multiple models at once.

    Args:
        models: Dict of model name -> (input_price_per_million, output_price_per_million).

    Example::

        agentbudget.register_models({
            "gpt-5": (5.00, 15.00),
            "gpt-5-mini": (0.50, 1.50),
        })
    """
    for model, (inp, out) in models.items():
        register_model(model, inp, out)


def _fuzzy_match(model: str) -> Optional[tuple[float, float]]:
    """Try to match a dated model variant to its base model.

    For example, 'gpt-4o-2025-03-01' matches 'gpt-4o'.
    """
    # Try progressively shorter prefixes by stripping trailing segments
    parts = model.rsplit("-", 1)
    while len(parts) == 2:
        prefix = parts[0]
        # Check custom first, then built-in
        if prefix in _custom_pricing:
            return _custom_pricing[prefix]
        if prefix in MODEL_PRICING:
            return MODEL_PRICING[prefix]
        parts = prefix.rsplit("-", 1)
    return None


def get_model_pricing(model: str) -> Optional[tuple[float, float]]:
    """Look up per-token pricing for a model.

    Resolution order:
    1. Custom pricing (registered via register_model)
    2. Built-in pricing table
    3. Fuzzy match (strip date suffixes to find base model)

    Returns (input_price_per_token, output_price_per_token) or None if unknown.
    """
    # 1. Custom pricing takes priority
    if model in _custom_pricing:
        return _custom_pricing[model]
    # 2. Built-in table
    if model in MODEL_PRICING:
        return MODEL_PRICING[model]
    # 3. Fuzzy match dated variants
    return _fuzzy_match(model)


def calculate_llm_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> Optional[float]:
    """Calculate the cost of an LLM call in USD.

    Returns None if model pricing is not found.
    """
    pricing = get_model_pricing(model)
    if pricing is None:
        return None
    input_price, output_price = pricing
    return (input_tokens * input_price) + (output_tokens * output_price)
