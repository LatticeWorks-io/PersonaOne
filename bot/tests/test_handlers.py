"""End-to-end handler wiring tests.

These exercise each Telegram handler with mocked Update/Context objects so
we catch wiring bugs the per-module unit tests miss (paywall not shown,
Stars payload format wrong, paid-state not respected, Claude failure not
caught, etc.).

Mocks: Anthropic AsyncAnthropic is replaced with a MagicMock whose
`reply` is an AsyncMock returning "test reply"; Telegram Update + Context
are built ad-hoc with the minimum attributes each handler actually reads.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from bot import handlers


def _msg_update(user_id: int = 42, text: str = "") -> MagicMock:
    upd = MagicMock()
    upd.message.from_user.id = user_id
    upd.message.text = text
    upd.message.chat_id = user_id
    upd.message.reply_text = AsyncMock()
    return upd


def _cb_update(user_id: int = 42, data: str = "") -> MagicMock:
    upd = MagicMock()
    upd.callback_query.from_user.id = user_id
    upd.callback_query.data = data
    upd.callback_query.message.chat_id = user_id
    upd.callback_query.message.reply_text = AsyncMock()
    upd.callback_query.answer = AsyncMock()
    return upd


@pytest.mark.asyncio
async def test_start_renders_greeting_with_paywall(context):
    upd = _msg_update()
    await handlers.cmd_start(upd, context)
    upd.message.reply_text.assert_awaited_once()
    args, kwargs = upd.message.reply_text.call_args
    assert "AI" in args[0]  # greeting discloses AI status
    assert kwargs.get("reply_markup") is not None


@pytest.mark.asyncio
async def test_start_paywall_omits_crypto_when_np_disabled(context):
    upd = _msg_update()
    await handlers.cmd_start(upd, context)
    kwargs = upd.message.reply_text.call_args.kwargs
    markup = kwargs["reply_markup"]
    # Inspect inline keyboard rows for callback_data prefixes
    all_data = [btn.callback_data for row in markup.inline_keyboard for btn in row]
    assert any(d.startswith("buy_stars:") for d in all_data)
    assert not any(d.startswith("buy_crypto:") for d in all_data)


@pytest.mark.asyncio
async def test_start_includes_crypto_when_np_enabled(context):
    context.application.bot_data["np"] = MagicMock()  # presence is enough
    upd = _msg_update()
    await handlers.cmd_start(upd, context)
    kwargs = upd.message.reply_text.call_args.kwargs
    all_data = [btn.callback_data for row in kwargs["reply_markup"].inline_keyboard for btn in row]
    assert any(d.startswith("buy_stars:") for d in all_data)
    assert any(d.startswith("buy_crypto:") for d in all_data)


@pytest.mark.asyncio
async def test_buy_stars_sends_invoice_with_xtr_currency(context):
    upd = _cb_update(data="buy_stars:hour")
    await handlers.on_buy_stars(upd, context)
    upd.callback_query.answer.assert_awaited_once()
    context.bot.send_invoice.assert_awaited_once()
    kwargs = context.bot.send_invoice.call_args.kwargs
    assert kwargs["currency"] == "XTR"
    assert kwargs["title"] == "hour"
    assert kwargs["payload"].startswith("stars:hour:")


@pytest.mark.asyncio
async def test_buy_stars_unknown_offer_replies_gracefully(context):
    upd = _cb_update(data="buy_stars:does-not-exist")
    await handlers.on_buy_stars(upd, context)
    upd.callback_query.message.reply_text.assert_awaited_once()
    context.bot.send_invoice.assert_not_called()


@pytest.mark.asyncio
async def test_buy_crypto_when_np_disabled_replies_and_no_invoice(context):
    upd = _cb_update(data="buy_crypto:hour")
    await handlers.on_buy_crypto(upd, context)
    upd.callback_query.message.reply_text.assert_awaited_once()
    msg = upd.callback_query.message.reply_text.call_args.args[0]
    assert "not configured" in msg.lower()


@pytest.mark.asyncio
async def test_buy_crypto_when_np_enabled_creates_invoice_and_sends_link(context):
    fake_np = MagicMock()
    fake_np.create_invoice = AsyncMock(return_value={"invoice_url": "https://np.test/inv/abc"})
    context.application.bot_data["np"] = fake_np
    upd = _cb_update(user_id=42, data="buy_crypto:hour")
    await handlers.on_buy_crypto(upd, context)
    fake_np.create_invoice.assert_awaited_once()
    args, kwargs = fake_np.create_invoice.call_args
    assert kwargs["price_amount"] == 25.0
    assert kwargs["order_id"].startswith("lw-42-")
    upd.callback_query.message.reply_text.assert_awaited_once()
    msg = upd.callback_query.message.reply_text.call_args.args[0]
    assert "https://np.test/inv/abc" in msg


@pytest.mark.asyncio
async def test_precheckout_always_oks(context):
    upd = MagicMock()
    upd.pre_checkout_query.answer = AsyncMock()
    await handlers.on_precheckout(upd, context)
    upd.pre_checkout_query.answer.assert_awaited_once_with(ok=True)


@pytest.mark.asyncio
async def test_successful_payment_marks_paid(context, storage):
    upd = _msg_update(user_id=42)
    upd.message.successful_payment.invoice_payload = "stars:hour:deadbeef"
    upd.message.successful_payment.telegram_payment_charge_id = "tg_charge_1"
    await handlers.on_successful_payment(upd, context)
    assert storage.has_active_payment(42) is True
    upd.message.reply_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_message_unpaid_shows_paywall_not_claude(context, storage, fake_claude):
    upd = _msg_update(user_id=42, text="hello")
    await handlers.on_message(upd, context)
    fake_claude.reply.assert_not_called()
    upd.message.reply_text.assert_awaited_once()
    args, kwargs = upd.message.reply_text.call_args
    assert "pay" in args[0].lower()
    assert kwargs.get("reply_markup") is not None


@pytest.mark.asyncio
async def test_message_paid_calls_claude_and_persists_turns(context, storage, fake_claude):
    storage.mark_paid(42, "hour", "stars", "charge_x")
    upd = _msg_update(user_id=42, text="hello")
    await handlers.on_message(upd, context)
    fake_claude.reply.assert_awaited_once()
    upd.message.reply_text.assert_awaited_once_with("test reply")
    turns = storage.recent_turns(42)
    assert [t["content"] for t in turns] == ["hello", "test reply"]


@pytest.mark.asyncio
async def test_message_claude_failure_returns_friendly_message_and_no_persist(
    context, storage, fake_claude
):
    storage.mark_paid(42, "hour", "stars", "charge_x")
    fake_claude.reply = AsyncMock(side_effect=RuntimeError("network blip"))
    upd = _msg_update(user_id=42, text="hello")
    await handlers.on_message(upd, context)
    upd.message.reply_text.assert_awaited_once()
    msg = upd.message.reply_text.call_args.args[0]
    assert "sec" in msg.lower() or "blipped" in msg.lower()
    # On Claude failure, no turns persisted (avoid corrupting history)
    assert storage.recent_turns(42) == []


@pytest.mark.asyncio
async def test_message_paid_uses_recent_history(context, storage, fake_claude):
    storage.mark_paid(42, "hour", "stars", "charge_x")
    # Seed prior conversation
    storage.append_turn(42, "user", "earlier")
    storage.append_turn(42, "assistant", "earlier reply")
    upd = _msg_update(user_id=42, text="now")
    await handlers.on_message(upd, context)
    # Claude received the prior turns as history
    call = fake_claude.reply.call_args
    history = call.args[0]
    assert [h["content"] for h in history] == ["earlier", "earlier reply"]
    assert call.args[1] == "now"
