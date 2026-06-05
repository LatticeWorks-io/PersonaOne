import hashlib
import hmac
import json

import pytest

from bot.nowpayments import NowPaymentsClient
from bot.storage import Storage
from bot.webhook import handle_ipn_payload

SECRET = "test-secret"


@pytest.fixture
def np():
    return NowPaymentsClient(api_key="k", ipn_secret=SECRET, webhook_host="https://x")


@pytest.fixture
def storage(tmp_path):
    return Storage(tmp_path / "t.db")


def _sign(payload: dict) -> tuple[bytes, str]:
    canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    sig = hmac.new(SECRET.encode(), canonical.encode(), hashlib.sha512).hexdigest()
    raw = json.dumps(payload).encode()  # NOT canonical — emulate live IPN body
    return raw, sig


def test_finished_payment_marks_paid(storage, np):
    payload = {
        "payment_status": "finished",
        "order_id": "lw-42-abc12345",
        "order_description": "personaone: 30 min",
        "payment_id": "np-xyz-1",
    }
    raw, sig = _sign(payload)
    code, _ = handle_ipn_payload(raw, sig, storage, np)
    assert code == 200
    assert storage.has_active_payment(42) is True


def test_non_final_status_does_not_mark_paid(storage, np):
    payload = {
        "payment_status": "waiting",
        "order_id": "lw-42-abc12345",
        "order_description": "personaone: 30 min",
        "payment_id": "np-xyz-1",
    }
    raw, sig = _sign(payload)
    code, msg = handle_ipn_payload(raw, sig, storage, np)
    assert code == 200
    assert "waiting" in msg
    assert storage.has_active_payment(42) is False


def test_confirming_status_also_skipped(storage, np):
    payload = {
        "payment_status": "confirming",
        "order_id": "lw-42-abc",
        "order_description": "p: o",
        "payment_id": "np-1",
    }
    raw, sig = _sign(payload)
    code, _ = handle_ipn_payload(raw, sig, storage, np)
    assert code == 200
    assert storage.has_active_payment(42) is False


def test_missing_signature_rejected(storage, np):
    payload = {"payment_status": "finished", "order_id": "lw-42-abc"}
    raw = json.dumps(payload).encode()
    code, _ = handle_ipn_payload(raw, "", storage, np)
    assert code == 400
    assert storage.has_active_payment(42) is False


def test_invalid_signature_rejected(storage, np):
    payload = {"payment_status": "finished", "order_id": "lw-42-abc"}
    raw, _ = _sign(payload)
    code, _ = handle_ipn_payload(raw, "deadbeef", storage, np)
    assert code == 400
    assert storage.has_active_payment(42) is False


def test_bad_order_id_format_accepted_but_no_credit(storage, np):
    payload = {
        "payment_status": "finished",
        "order_id": "garbage",
        "order_description": "p: o",
        "payment_id": "np-xyz",
    }
    raw, sig = _sign(payload)
    code, msg = handle_ipn_payload(raw, sig, storage, np)
    # 200 so NowPayments doesn't retry forever; no credit issued.
    assert code == 200
    assert "bad order_id" in msg
    assert storage.has_active_payment(42) is False


def test_offer_name_parsed_from_description(storage, np):
    payload = {
        "payment_status": "finished",
        "order_id": "lw-99-deadbeef",
        "order_description": "personaone: voice note bundle",
        "payment_id": "np-99",
    }
    raw, sig = _sign(payload)
    code, msg = handle_ipn_payload(raw, sig, storage, np)
    assert code == 200
    assert "voice note bundle" in msg
    assert storage.has_active_payment(99) is True
