"""Entry point. Wires services, registers handlers, runs polling + webhook concurrently."""
from __future__ import annotations

import asyncio
import logging
import os
import signal

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
from bot.webhook import start_webhook_runner

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
log = logging.getLogger("lw-bot")


def _build_app() -> tuple[Application, Storage, NowPaymentsClient | None]:
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
    return app, storage, np_client


async def _run() -> None:
    app, storage, np = _build_app()

    webhook_runner = None
    if np:
        host = os.environ.get("LW_WEBHOOK_HOST", "127.0.0.1")
        port = int(os.environ.get("LW_WEBHOOK_PORT", "8081"))
        webhook_runner = await start_webhook_runner(storage, np, host=host, port=port)

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, stop.set)

    async with app:
        await app.start()
        await app.updater.start_polling(
            allowed_updates=["message", "callback_query", "pre_checkout_query"]
        )
        log.info("Bot online.")
        try:
            await stop.wait()
        finally:
            await app.updater.stop()
            await app.stop()
            if webhook_runner:
                await webhook_runner.cleanup()


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
