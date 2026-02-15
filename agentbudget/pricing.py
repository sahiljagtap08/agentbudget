"""Model pricing data for LLM cost calculation.

Prices are per token in USD. Updated as of early 2025.
"""

from typing import Optional

# Mapping of model name -> (input_price_per_token, output_price_per_token)
MODEL_PRICING: dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "gpt-4o-2024-11-20": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "gpt-4o-2024-08-06": (2.50 / 1_000_000, 10.00 / 1_000_000),
    "gpt-4o-mini": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "gpt-4o-mini-2024-07-18": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "gpt-4-turbo": (10.00 / 1_000_000, 30.00 / 1_000_000),
    "gpt-4-turbo-2024-04-09": (10.00 / 1_000_000, 30.00 / 1_000_000),
    "gpt-4": (30.00 / 1_000_000, 60.00 / 1_000_000),
    "gpt-3.5-turbo": (0.50 / 1_000_000, 1.50 / 1_000_000),
    "o1": (15.00 / 1_000_000, 60.00 / 1_000_000),
    "o1-mini": (3.00 / 1_000_000, 12.00 / 1_000_000),
    "o1-preview": (15.00 / 1_000_000, 60.00 / 1_000_000),
    "o3-mini": (1.10 / 1_000_000, 4.40 / 1_000_000),
    # Anthropic
    "claude-3-5-sonnet-20241022": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-3-5-sonnet-20240620": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-3-5-haiku-20241022": (0.80 / 1_000_000, 4.00 / 1_000_000),
    "claude-3-opus-20240229": (15.00 / 1_000_000, 75.00 / 1_000_000),
    "claude-3-sonnet-20240229": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-3-haiku-20240307": (0.25 / 1_000_000, 1.25 / 1_000_000),
}


def get_model_pricing(model: str) -> Optional[tuple[float, float]]:
    """Look up per-token pricing for a model.

    Returns (input_price_per_token, output_price_per_token) or None if unknown.
    """
    return MODEL_PRICING.get(model)


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
