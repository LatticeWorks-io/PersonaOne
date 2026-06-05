# bot/

Telegram bot for the LatticeWorks MVP. Routes Twitter → Telegram → payment (Stars or crypto) → Claude-driven conversation.

## Layout

- `main.py` — entry point. Reads env, wires services, starts polling.
- `handlers.py` — Telegram handlers (`/start`, paywall buttons, payment success, message loop).
- `claude_client.py` — async Anthropic SDK wrapper using the persona's system prompt + conversation history.
- `nowpayments.py` — invoice creation + IPN HMAC-SHA512 verification.
- `persona.py` — pydantic-validated YAML persona loader.
- `storage.py` — SQLite: `paid_users` + `session_turns`.
- `tests/` — pytest suite for storage, NowPayments verification, persona loader.
- `systemd/lw-bot.service` — production unit file.

## Run locally

```bash
cd /opt/latticeworks.io
python3 -m venv .venv && source .venv/bin/activate
pip install -r bot/requirements.txt
cp bot/.env.example bot/.env       # fill in tokens
set -a; . bot/.env; set +a
python -m bot.main
```

## Run tests

```bash
cd /opt/latticeworks.io
pip install pytest pytest-asyncio
PYTHONPATH=. pytest bot/tests -v
```

The handler tests (`test_handlers.py`) use mocked Telegram Update + Context objects and a mocked Claude client — no network, no Telegram bot token required.

## What this bot does NOT do (v1.1+)

- No image gen (deferred Flux on RunPod)
- No voice notes (deferred ElevenLabs)
- No NowPayments IPN HTTP listener (the `verify_ipn` function exists; binding a webhook server is the next addition)
- No multi-persona routing — one process, one persona
