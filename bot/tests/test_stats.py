"""Tests for /stats handler + revenue_summary helper."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from bot import handlers


# ---------- revenue_summary aggregation ----------


def test_revenue_summary_empty(storage):
    s = storage.revenue_summary(days=7)
    assert s == {
        "paid_users_total": 0,
        "payments_total": 0,
        "stars_xtr": 0,
        "crypto_usd": 0.0,
        "new_buyers_window": 0,
        "window_days": 7,
    }


def test_revenue_summary_aggregates_both_rails(storage):
    storage.mark_paid(1, "hour", "stars", "tg_a", amount_xtr=100)
    storage.mark_paid(1, "bundle", "stars", "tg_b", amount_xtr=500)
    storage.mark_paid(2, "hour", "crypto", "np_x", amount_usd=25.0)
    storage.mark_paid(3, "bundle", "crypto", "np_y", amount_usd=75.0)
    s = storage.revenue_summary(days=7)
    assert s["paid_users_total"] == 3
    assert s["payments_total"] == 4
    assert s["stars_xtr"] == 600
    assert s["crypto_usd"] == 100.0


def test_revenue_summary_new_buyers_window_counts_first_payment_only(storage):
    long_ago = int(time.time()) - 30 * 86400
    # Patch in an "old" payment via raw SQL since mark_paid stamps NOW.
    with storage._conn() as c:
        c.execute(
            "INSERT INTO paid_users (tg_user_id, offer_name, paid_at, rail, external_id, amount_xtr, amount_usd) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, "hour", long_ago, "stars", "old", 100, 0.0),
        )
    storage.mark_paid(1, "hour", "stars", "new", amount_xtr=100)  # user 1's first was OLD
    storage.mark_paid(2, "hour", "stars", "fresh", amount_xtr=100)  # user 2's first is NOW
    s = storage.revenue_summary(days=7)
    # Only user 2 counts as a "new buyer in last 7d" — user 1's first payment was 30d ago
    assert s["new_buyers_window"] == 1


# ---------- /stats handler auth ----------


def _msg_update(user_id: int) -> MagicMock:
    upd = MagicMock()
    upd.message.from_user.id = user_id
    upd.message.reply_text = AsyncMock()
    return upd


@pytest.mark.asyncio
async def test_stats_silent_when_operator_id_unset(context, monkeypatch):
    monkeypatch.delenv("LW_OPERATOR_USER_ID", raising=False)
    upd = _msg_update(user_id=42)
    await handlers.cmd_stats(upd, context)
    upd.message.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_stats_silent_for_non_operator(context, monkeypatch):
    monkeypatch.setenv("LW_OPERATOR_USER_ID", "999")
    upd = _msg_update(user_id=42)  # not the operator
    await handlers.cmd_stats(upd, context)
    upd.message.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_stats_replies_to_operator(context, storage, monkeypatch):
    monkeypatch.setenv("LW_OPERATOR_USER_ID", "42")
    storage.mark_paid(1, "hour", "stars", "tg_a", amount_xtr=100)
    storage.mark_paid(2, "bundle", "crypto", "np_x", amount_usd=75.0)
    upd = _msg_update(user_id=42)
    await handlers.cmd_stats(upd, context)
    upd.message.reply_text.assert_awaited_once()
    msg = upd.message.reply_text.call_args.args[0]
    assert "100 ⭐" in msg
    assert "$75" in msg
    assert "Paid users (lifetime): 2" in msg


@pytest.mark.asyncio
async def test_stats_silent_when_operator_id_garbage(context, monkeypatch):
    monkeypatch.setenv("LW_OPERATOR_USER_ID", "not-a-number")
    upd = _msg_update(user_id=42)
    await handlers.cmd_stats(upd, context)
    upd.message.reply_text.assert_not_called()
