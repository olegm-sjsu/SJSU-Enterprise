# Author: Oleg Mrynskyi

import hmac
import hashlib
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.webhook import verify_webhook_signature, parse_webhook_payload

client = TestClient(app)
SECRET = "test_secret_123"

def test_verify_webhook_signature_valid():
    body = b'{"action":"opened"}'
    computed = hmac.new(SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
    sig_header = f"sha256={computed}"

    assert verify_webhook_signature(body, sig_header, SECRET) is True


def test_verify_webhook_signature_invalid():
    body = b'{"action":"opened"}'
    sig_header = "sha256=invalid_hash_value"
    assert verify_webhook_signature(body, sig_header, SECRET) is False


def test_verify_webhook_signature_missing_prefix():
    body = b'{"action":"opened"}'
    assert verify_webhook_signature(body, "raw_hash_without_sha256", SECRET) is False


def test_parse_webhook_payload_issue():
    raw = b'{"action":"closed","issue":{"number":99}}'
    action, issue_number, data = parse_webhook_payload("issues", raw)
    assert action == "closed"
    assert issue_number == 99


def test_parse_webhook_payload_ping():
    raw = b'{"zen":"Design for failure."}'
    action, issue_number, data = parse_webhook_payload("ping", raw)
    assert action == "ping"
    assert issue_number is None


@patch("app.main.get_settings")
def test_webhook_endpoint_unauthorized(mock_settings):
    mock_settings.return_value.WEBHOOK_SECRET = SECRET
    response = client.post(
        "/webhook",
        headers={"X-GitHub-Event": "issues", "X-Hub-Signature-256": "sha256=wrong"},
        content=b'{"action":"opened"}'
    )
    assert response.status_code == 401


@patch("app.main.get_settings")
def test_webhook_endpoint_unsupported_event(mock_settings):
    mock_settings.return_value.WEBHOOK_SECRET = SECRET
    body = b'{"action":"push"}'
    computed = hmac.new(SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
    
    response = client.post(
        "/webhook",
        headers={
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": f"sha256={computed}"
        },
        content=body
    )
    assert response.status_code == 400
