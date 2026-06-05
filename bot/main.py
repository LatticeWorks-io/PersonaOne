"""Entry point. Reads env, wires services, registers handlers, starts polling."""
from __future__ import annotations

import logging
import os

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)

from bot import handlers
from bot.claude_client import ClaudeClient
from bot.nowpayments import NowPaymentsClient
from bot.persona import load_persona
from bot.storage import Storage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
log = logging.getLogger("lw-bot")


def _build_app() -> Application:
    bot_token = os.environ["LW_BOT_TOKEN"]
    claude_key = os.environ["LW_CLAUDE_KEY"]
    claude_model = os.environ.get("LW_CLAUDE_MODEL", "claude-sonnet-4-6")
    persona_path = os.environ.get("LW_PERSONA_PATH", "personas/persona-one.yaml")
    db_path = os.environ.get("LW_DB_PATH", "bot/data/bot.db")

    persona = load_persona(persona_path)
    storage = Storage(db_path)
    claude = ClaudeClient(api_key=claude_key, model=claude_model, persona=persona)

    np_key = os.environ.get("LW_NOWPAYMENTS_API_KEY")
    np_secret = os.environ.get("LW_NOWPAYMENTS_IPN_SECRET")
    np_host = os.environ.get("LW_NOWPAYMENTS_WEBHOOK_HOST")
    np_client = (
        NowPaymentsClient(api_key=np_key, ipn_secret=np_secret, webhook_host=np_host)
        if np_key and np_secret and np_host
        else None
    )
    if not np_client:
        log.warning("NowPayments env not fully set; crypto rail disabled.")

    app = Application.builder().token(bot_token).build()
    app.bot_data["persona"] = persona
    app.bot_data["storage"] = storage
    app.bot_data["claude"] = claude
    app.bot_data["np"] = np_client

    app.add_handler(CommandHandler("start", handlers.cmd_start))
    app.add_handler(CallbackQueryHandler(handlers.on_buy_stars, pattern=r"^buy_stars:"))
    app.add_handler(CallbackQueryHandler(handlers.on_buy_crypto, pattern=r"^buy_crypto:"))
    app.add_handler(PreCheckoutQueryHandler(handlers.on_precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, handlers.on_successful_payment))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.on_message))
    return app


def main() -> None:
    app = _build_app()
    log.info("Bot online. Listening for updates.")
    app.run_polling(allowed_updates=["message", "callback_query", "pre_checkout_query"])


if __name__ == "__main__":
    main()
