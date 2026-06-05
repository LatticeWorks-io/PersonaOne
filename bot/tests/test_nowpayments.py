import hashlib
import hmac
import json

import pytest

from bot.nowpayments import NowPaymentsClient


@pytest.fixture
def client():
    return NowPaymentsClient(api_key="k", ipn_secret="secret", webhook_host="https://x")


def _sign(payload: dict, secret: str) -> tuple[bytes, str]:
    canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    sig = hmac.new(secret.encode(), canonical.encode(), hashlib.sha512).hexdigest()
    raw = json.dumps(payload).encode()  # NOT canonical — emulate live IPN body
    return raw, sig


def test_verify_ipn_accepts_valid(client):
    raw, sig = _sign({"payment_status": "finished", "order_id": "lw-1"}, "secret")
    assert client.verify_ipn(raw, sig) is True


def test_verify_ipn_rejects_wrong_secret(client):
    raw, sig = _sign({"payment_status": "finished", "order_id": "lw-1"}, "wrong")
    assert client.verify_ipn(raw, sig) is False


def test_verify_ipn_rejects_tampered_body(client):
    raw, sig = _sign({"payment_status": "finished", "order_id": "lw-1"}, "secret")
    tampered = raw.replace(b"finished", b"refunded")
    assert client.verify_ipn(tampered, sig) is False


def test_verify_ipn_rejects_garbage(client):
    assert client.verify_ipn(b"not json", "deadbeef") is False
