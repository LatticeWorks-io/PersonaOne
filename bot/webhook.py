"""HTTP webhook server for NowPayments IPN callbacks.

NowPayments POSTs a JSON body with the `x-nowpayments-sig` header (HMAC-SHA512
of the canonical-JSON body under the IPN secret). On payment_status="finished"
we flip the buyer to paid in storage.

The pure handler lives in `handle_ipn_payload` so tests can drive it without
spinning up a server. The aiohttp wiring is intentionally minimal.

Runs alongside the Telegram polling loop in main.py via asyncio.
"""
from __future__ import annotations

import json
import logging

from aiohttp import web

from bot.nowpayments import NowPaymentsClient
from bot.storage import Storage

log = logging.getLogger(__name__)

PAID_STATUSES = {"finished"}


def handle_ipn_payload(
    raw_body: bytes,
    signature: str,
    storage: Storage,
    np: NowPaymentsClient,
) -> tuple[int, str]:
    """Pure handler. Returns (http_status, log_message).

    200 = signature ok, processed (paid or non-final status ignored)
    400 = signature missing or invalid
    """
    if not signature:
        return 400, "missing signature"
    if not np.verify_ipn(raw_body, signature):
        return 400, "invalid signature"
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return 400, "invalid json"

    status = payload.get("payment_status", "")
    if status not in PAID_STATUSES:
        return 200, f"ignored status: {status}"

    # order_id format: "lw-<tg_user_id>-<uuid8>" (set in handlers.on_buy_crypto)
    order_id = payload.get("order_id", "")
    parts = order_id.split("-")
    if len(parts) < 3 or parts[0] != "lw":
        return 200, f"bad order_id format: {order_id!r}"
    try:
        tg_user_id = int(parts[1])
    except ValueError:
        return 200, f"bad user id in order_id: {order_id!r}"

    # order_description format: "<persona handle>: <offer name>"
    desc = payload.get("order_description", "")
    offer_name = desc.split(": ", 1)[1] if ": " in desc else "unknown"

    amount_usd = 0.0
    try:
        amount_usd = float(payload.get("price_amount") or 0.0)
    except (TypeError, ValueError):
        amount_usd = 0.0
    storage.mark_paid(
        tg_user_id=tg_user_id,
        offer_name=offer_name,
        rail="crypto",
        external_id=str(payload.get("payment_id") or order_id),
        amount_usd=amount_usd,
    )
    return 200, f"marked paid: user={tg_user_id} offer={offer_name!r} amount=${amount_usd:.2f}"


def _build_app(storage: Storage, np: NowPaymentsClient) -> web.Application:
    async def ipn(request: web.Request) -> web.Response:
        raw = await request.read()
        sig = request.headers.get("x-nowpayments-sig", "")
        status, msg = handle_ipn_payload(raw, sig, storage, np)
        log.info("ipn: %s", msg)
        return web.Response(status=status, text=msg)

    async def health(_: web.Request) -> web.Response:
        return web.Response(text="ok")

    app = web.Application()
    app.router.add_post("/nowpayments/ipn", ipn)
    app.router.add_get("/healthz", health)
    return app


async def start_webhook_runner(
    storage: Storage,
    np: NowPaymentsClient,
    *,
    host: str = "127.0.0.1",
    port: int = 8081,
) -> web.AppRunner:
    """Start the aiohttp server, return the runner. Caller must `await runner.cleanup()` on shutdown."""
    app = _build_app(storage, np)
    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    log.info("webhook listening on http://%s:%d/nowpayments/ipn", host, port)
    return runner
