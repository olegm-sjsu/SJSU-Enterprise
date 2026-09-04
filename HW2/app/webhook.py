# Author: Oleg Mrynskyi
# CMPE 272 HW2 - GitHub Issues REST API & Webhook Service

import hmac
import hashlib
import json
from typing import Tuple, Optional, Dict, Any

# constant-time compare so a timing attack can't leak the secret byte by byte
def verify_webhook_signature(raw_body: bytes, signature_header: Optional[str], secret: str) -> bool:
    if not signature_header or not secret:
        return False

    if not signature_header.startswith("sha256="):
        return False

    computed_hash = hmac.new(
        key=secret.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    expected_signature = f"sha256={computed_hash}"
    return hmac.compare_digest(expected_signature, signature_header)


def parse_webhook_payload(event_type: str, raw_body: bytes) -> Tuple[Optional[str], Optional[int], Dict[str, Any]]:
    try:
        data = json.loads(raw_body.decode("utf-8"))
    except Exception:
        data = {}

    if event_type == "ping":
        return ("ping", None, data)

    action = data.get("action")
    issue_number = None

    if "issue" in data and isinstance(data["issue"], dict):
        issue_number = data["issue"].get("number")

    return (action, issue_number, data)
