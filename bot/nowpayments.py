"""NowPayments client + IPN HMAC verification.

NowPayments signs every IPN callback with HMAC-SHA512 over a JSON payload whose
keys are sorted alphabetically. We re-sort the parsed body, recompute, and compare.
Docs: https://documenter.getpostman.com/view/7907941/2s93JusNJt
"""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

import httpx

API_BASE = "https://api.nowpayments.io/v1"


class NowPaymentsClient:
    def __init__(self, api_key: str, ipn_secret: str, webhook_host: str):
        self._api_key = api_key
        self._ipn_secret = ipn_secret.encode("utf-8")
        self._webhook_host = webhook_host.rstrip("/")

    async def create_invoice(
        self,
        *,
        price_amount: float,
        price_currency: str = "usd",
        order_id: str,
        order_description: str,
    ) -> dict[str, Any]:
        payload = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            "order_id": order_id,
            "order_description": order_description,
            "ipn_callback_url": f"{self._webhook_host}/nowpayments/ipn",
            "success_url": f"{self._webhook_host}/paid/success",
            "cancel_url": f"{self._webhook_host}/paid/cancel",
        }
        async with httpx.AsyncClient(timeout=15) as http:
            r = await http.post(
                f"{API_BASE}/invoice",
                headers={"x-api-key": self._api_key, "Content-Type": "application/json"},
                json=payload,
            )
            r.raise_for_status()
            return r.json()

    def verify_ipn(self, raw_body: bytes, signature_header: str) -> bool:
        """Return True iff the IPN signature matches the body under our secret."""
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return False
        canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        digest = hmac.new(self._ipn_secret, canonical.encode("utf-8"), hashlib.sha512).hexdigest()
        return hmac.compare_digest(digest, signature_header.strip().lower())
