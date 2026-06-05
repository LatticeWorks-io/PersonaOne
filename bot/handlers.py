"""Telegram handlers: /start, paywall, Stars payment flow, paid-state message loop."""
from __future__ import annotations

import logging
import uuid

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    Update,
)
from telegram.ext import ContextTypes

from bot.claude_client import ClaudeClient
from bot.nowpayments import NowPaymentsClient
from bot.persona import Persona
from bot.storage import Storage

log = logging.getLogger(__name__)


def _build_paywall_keyboard(persona: Persona, np_enabled: bool) -> InlineKeyboardMarkup:
    rows = []
    for offer in persona.offers:
        rows.append(
            [InlineKeyboardButton(f"{offer.name} — {offer.stars_price}⭐", callback_data=f"buy_stars:{offer.name}")]
        )
        if np_enabled:
            rows.append(
                [InlineKeyboardButton(f"{offer.name} — ${offer.usd_price:.0f} crypto", callback_data=f"buy_crypto:{offer.name}")]
            )
    return InlineKeyboardMarkup(rows)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    persona: Persona = context.application.bot_data["persona"]
    np_enabled = context.application.bot_data.get("np") is not None
    await update.message.reply_text(
        persona.greeting,
        reply_markup=_build_paywall_keyboard(persona, np_enabled),
    )


async def on_buy_stars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    persona: Persona = context.application.bot_data["persona"]
    offer_name = query.data.split(":", 1)[1]
    offer = next((o for o in persona.offers if o.name == offer_name), None)
    if not offer:
        await query.message.reply_text("Offer no longer available.")
        return
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=offer.name,
        description=offer.description,
        payload=f"stars:{offer.name}:{uuid.uuid4().hex}",
        currency="XTR",  # Telegram Stars
        prices=[LabeledPrice(label=offer.name, amount=offer.stars_price)],
    )


async def on_buy_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    np: NowPaymentsClient | None = context.application.bot_data.get("np")
    if not np:
        await query.message.reply_text("Crypto rail not configured yet.")
        return
    persona: Persona = context.application.bot_data["persona"]
    offer_name = query.data.split(":", 1)[1]
    offer = next((o for o in persona.offers if o.name == offer_name), None)
    if not offer:
        return
    order_id = f"lw-{query.from_user.id}-{uuid.uuid4().hex[:8]}"
    invoice = await np.create_invoice(
        price_amount=offer.usd_price,
        order_id=order_id,
        order_description=f"{persona.handle}: {offer.name}",
    )
    await query.message.reply_text(
        f"Pay with crypto: {invoice['invoice_url']}\n\n(Bot unlocks the moment NowPayments confirms.)"
    )


async def on_precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.pre_checkout_query.answer(ok=True)


async def on_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage: Storage = context.application.bot_data["storage"]
    sp = update.message.successful_payment
    # payload format: "stars:<offer_name>:<uuid>"
    parts = sp.invoice_payload.split(":", 2)
    offer_name = parts[1] if len(parts) >= 2 else "unknown"
    storage.mark_paid(
        tg_user_id=update.message.from_user.id,
        offer_name=offer_name,
        rail="stars",
        external_id=sp.telegram_payment_charge_id,
    )
    persona: Persona = context.application.bot_data["persona"]
    await update.message.reply_text(f"Payment received. {persona.paywall_message}")


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage: Storage = context.application.bot_data["storage"]
    claude: ClaudeClient = context.application.bot_data["claude"]
    persona: Persona = context.application.bot_data["persona"]
    user_id = update.message.from_user.id

    if not storage.has_active_payment(user_id):
        np_enabled = context.application.bot_data.get("np") is not None
        await update.message.reply_text(
            persona.paywall_message,
            reply_markup=_build_paywall_keyboard(persona, np_enabled),
        )
        return

    user_text = update.message.text or ""
    history = storage.recent_turns(user_id, limit=20)
    try:
        reply = await claude.reply(history, user_text)
    except Exception:
        log.exception("Claude call failed")
        await update.message.reply_text("Give me a sec, network blipped. Send again.")
        return
    storage.append_turn(user_id, "user", user_text)
    storage.append_turn(user_id, "assistant", reply)
    await update.message.reply_text(reply)
