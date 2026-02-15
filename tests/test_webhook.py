"""Tests for webhook event streaming."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

from agentbudget import AgentBudget
from agentbudget.webhook import WebhookEmitter, send_webhook


class RecordingHandler(BaseHTTPRequestHandler):
    """HTTP handler that records received requests."""
    received = []

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        RecordingHandler.received.append(json.loads(body))
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress logs


def test_webhook_emitter_soft_limit():
    emitter = WebhookEmitter("http://localhost:19876")
    report = {"session_id": "sess_test", "total_spent": 4.50}
    # This will fail to connect, but should not raise
    result = emitter.on_soft_limit(report)
    assert result is False  # connection refused, returns False


def test_webhook_emitter_formats_payload():
    """Verify payload structure without needing a server."""
    emitter = WebhookEmitter("http://localhost:19876")

    # We can't easily test the payload without a server,
    # but we can test the emit method doesn't raise
    report = {"session_id": "sess_abc", "total_spent": 3.0}
    result = emitter.emit("test_event", report)
    assert result is False  # no server, returns False gracefully


def test_send_webhook_invalid_url():
    result = send_webhook("http://localhost:19999", {"test": True})
    assert result is False


def test_webhook_with_real_server():
    """Spin up a local HTTP server and verify webhook delivery."""
    RecordingHandler.received.clear()
    server = HTTPServer(("127.0.0.1", 19877), RecordingHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    try:
        emitter = WebhookEmitter("http://127.0.0.1:19877")
        report = {"session_id": "sess_123", "total_spent": 2.50}
        result = emitter.on_soft_limit(report)
        assert result is True
    finally:
        thread.join(timeout=5)
        server.server_close()

    assert len(RecordingHandler.received) == 1
    payload = RecordingHandler.received[0]
    assert payload["event_type"] == "soft_limit"
    assert payload["session_id"] == "sess_123"
    assert payload["data"]["total_spent"] == 2.50


def test_webhook_url_in_agent_budget():
    """Verify webhook_url param is accepted without error."""
    budget = AgentBudget(
        max_spend="$5.00",
        webhook_url="http://localhost:19999/events",
    )
    assert budget.max_spend == 5.0
