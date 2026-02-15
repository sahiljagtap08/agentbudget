"""Webhook event streaming for budget events."""

import json
import logging
import urllib.request
import urllib.error
from typing import Any, Optional

logger = logging.getLogger("agentbudget.webhook")


def send_webhook(url: str, payload: dict[str, Any], timeout: float = 5.0) -> bool:
    """Send a JSON payload to a webhook URL.

    Returns True if the request succeeded, False otherwise.
    Failures are logged but never raise — webhooks should not break your agent.
    """
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, OSError, ValueError) as e:
        logger.warning("Webhook delivery failed to %s: %s", url, e)
        return False


class WebhookEmitter:
    """Emits budget events to a webhook URL."""

    def __init__(self, url: str, timeout: float = 5.0):
        self._url = url
        self._timeout = timeout

    def emit(self, event_type: str, report: dict[str, Any]) -> bool:
        """Send a budget event to the webhook."""
        payload = {
            "event_type": event_type,
            "session_id": report.get("session_id"),
            "data": report,
        }
        return send_webhook(self._url, payload, timeout=self._timeout)

    def on_soft_limit(self, report: dict[str, Any]) -> bool:
        return self.emit("soft_limit", report)

    def on_hard_limit(self, report: dict[str, Any]) -> bool:
        return self.emit("hard_limit", report)

    def on_loop_detected(self, report: dict[str, Any]) -> bool:
        return self.emit("loop_detected", report)
