"""Monkey-patching for automatic LLM cost tracking.

Patches OpenAI and Anthropic client methods so every API call
is automatically tracked without any code changes.
"""

from __future__ import annotations

import functools
import logging
from typing import Any, Callable, Optional

logger = logging.getLogger("agentbudget.patch")

# Store original methods so we can unpatch cleanly
_originals: dict[str, Any] = {}


def _wrap_method(original: Callable, get_session: Callable) -> Callable:
    """Wrap a sync SDK method to auto-track costs."""

    @functools.wraps(original)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        response = original(*args, **kwargs)
        session = get_session()
        if session is not None:
            try:
                session.wrap(response)
            except Exception:
                logger.debug("Failed to track cost for response", exc_info=True)
                raise
        return response

    wrapper._agentbudget_patched = True  # type: ignore[attr-defined]
    return wrapper


def _wrap_async_method(original: Callable, get_session: Callable) -> Callable:
    """Wrap an async SDK method to auto-track costs."""

    @functools.wraps(original)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        response = await original(*args, **kwargs)
        session = get_session()
        if session is not None:
            try:
                session.wrap(response)
            except Exception:
                logger.debug("Failed to track cost for response", exc_info=True)
                raise
        return response

    wrapper._agentbudget_patched = True  # type: ignore[attr-defined]
    return wrapper


def patch_openai(get_session: Callable) -> bool:
    """Patch OpenAI client to automatically track costs.

    Returns True if patching succeeded, False if openai is not installed.
    """
    try:
        from openai.resources.chat.completions import Completions
    except ImportError:
        logger.debug("openai not installed, skipping patch")
        return False

    if getattr(getattr(Completions, "create", None), "_agentbudget_patched", False):
        return True  # already patched

    _originals["openai.chat.completions.create"] = Completions.create
    Completions.create = _wrap_method(Completions.create, get_session)  # type: ignore[assignment]

    # Patch async if available
    if hasattr(Completions, "acreate"):
        _originals["openai.chat.completions.acreate"] = Completions.acreate
        Completions.acreate = _wrap_async_method(Completions.acreate, get_session)  # type: ignore[assignment]

    # Also patch the async completions class if it exists
    try:
        from openai.resources.chat.completions import AsyncCompletions

        if not getattr(getattr(AsyncCompletions, "create", None), "_agentbudget_patched", False):
            _originals["openai.async_chat.completions.create"] = AsyncCompletions.create
            AsyncCompletions.create = _wrap_async_method(AsyncCompletions.create, get_session)  # type: ignore[assignment]
    except ImportError:
        pass

    logger.debug("Patched OpenAI client")
    return True


def patch_anthropic(get_session: Callable) -> bool:
    """Patch Anthropic client to automatically track costs.

    Returns True if patching succeeded, False if anthropic is not installed.
    """
    try:
        from anthropic.resources.messages import Messages
    except ImportError:
        logger.debug("anthropic not installed, skipping patch")
        return False

    if getattr(getattr(Messages, "create", None), "_agentbudget_patched", False):
        return True  # already patched

    _originals["anthropic.messages.create"] = Messages.create
    Messages.create = _wrap_method(Messages.create, get_session)  # type: ignore[assignment]

    # Patch async messages
    try:
        from anthropic.resources.messages import AsyncMessages

        if not getattr(getattr(AsyncMessages, "create", None), "_agentbudget_patched", False):
            _originals["anthropic.async_messages.create"] = AsyncMessages.create
            AsyncMessages.create = _wrap_async_method(AsyncMessages.create, get_session)  # type: ignore[assignment]
    except ImportError:
        pass

    logger.debug("Patched Anthropic client")
    return True


def unpatch_all() -> None:
    """Restore all original methods."""
    for key, original in _originals.items():
        parts = key.split(".")
        if key == "openai.chat.completions.create":
            try:
                from openai.resources.chat.completions import Completions
                Completions.create = original  # type: ignore[assignment]
            except ImportError:
                pass
        elif key == "openai.chat.completions.acreate":
            try:
                from openai.resources.chat.completions import Completions
                Completions.acreate = original  # type: ignore[assignment]
            except ImportError:
                pass
        elif key == "openai.async_chat.completions.create":
            try:
                from openai.resources.chat.completions import AsyncCompletions
                AsyncCompletions.create = original  # type: ignore[assignment]
            except ImportError:
                pass
        elif key == "anthropic.messages.create":
            try:
                from anthropic.resources.messages import Messages
                Messages.create = original  # type: ignore[assignment]
            except ImportError:
                pass
        elif key == "anthropic.async_messages.create":
            try:
                from anthropic.resources.messages import AsyncMessages
                AsyncMessages.create = original  # type: ignore[assignment]
            except ImportError:
                pass

    _originals.clear()
    logger.debug("Unpatched all methods")
