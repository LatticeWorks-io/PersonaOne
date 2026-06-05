# LatticeWorks

Isolated creator platform. The Craft playbook (`craft-content/`) is the operator setup runbook; the code in `bot/` + `automation/` is the actual product.

## What's running

- **`bot/`** — Telegram bot. Routes Twitter → Telegram → payment (Stars or crypto) → Claude conversation. One persona per process for v1.
- **`automation/`** — two loops:
  - `discovery_loop.py` (daily systemd timer) — Apify scrapes shoutout candidates + viral reply targets into operator-reviewed JSONL queues.
  - `content_loop.py` (operator-triggered, never auto) — Claude drafts warmup posts in the persona's voice, late.dev schedules approved drafts to Twitter.
- **`personas/`** — YAML persona files. Loaded into the bot at boot.
- **`content/`** — pre-staged warmup posts (7-day compressed schedule).
- **`docs/`** — runbook, discovery playbook, automation wiring.
- **`craft-content/`** — snapshot of the original 120-step Craft playbook (read-only source for operator setup steps).

## Architecture

- **Conversion path:** Twitter (warmup + paid shoutouts) → bio link → Telegram bot → paywall → Claude-driven conversation.
- **Payment rails:** Telegram Stars (no KYC, instant) + NowPayments crypto invoices (1–3 day KYC, gives a second rail).
- **Pricing:** per-engagement / per-bundle quotes, set in the persona file (`personas/_template.yaml`). NOT recurring monthly.
- **Discovery:** reply-guy strategy (free) + paid shoutouts from aged accounts ($50–500 each) — see `docs/discovery.md`.
- **Market window:** 12–18 months (validated 2026-06-01).

## Quick start

```bash
git clone https://github.com/LatticeWorks-io/PersonaOne.git latticeworks.io
cd latticeworks.io
python3 -m venv .venv && source .venv/bin/activate
pip install -r bot/requirements.txt -r automation/requirements.txt
cp bot/.env.example bot/.env                # fill in tokens
cp automation/.env.example automation/.env  # fill in tokens
cp personas/_template.yaml personas/persona-one.yaml  # fill in persona

# Run tests
PYTHONPATH=. pytest bot/tests -v

# Run the bot
set -a; . bot/.env; set +a
python -m bot.main

# Run discovery loop once (will write into data/)
set -a; . automation/.env; set +a
python -m automation.discovery_loop
```

## Layout

```
/opt/latticeworks.io/
├── bot/                 # Telegram bot (main.py, handlers, claude_client, nowpayments, persona, storage, tests, systemd)
├── automation/          # Apify discovery loop + late.dev content loop, systemd timer
├── personas/            # YAML persona files
├── content/             # warmup post backlog
├── docs/                # mvp-runbook, discovery, automation
├── craft-content/       # snapshot of original 120-step Craft playbook
├── scripts/             # Craft authoring scripts (one-time, kept for reference)
├── craft-pages.json     # Craft folder + page IDs (stale — folder was deleted)
└── README.md
```

## MVP path

See `docs/mvp-runbook.md` for the day-by-day execution. Headline:

- Cut Pages 05, 12-voice from the original 120 steps.
- Trim Page 04 (Hostwinds) to a $5–10/mo VPS.
- Run Page 07 KYC in parallel with the bot build so the wait overlaps the critical path.
- Compress Page 10 warmup from 14 days to 7 days.
- **Re-examine Page 11 (Twitter ACC enrollment)** before launch — without it the Twitter side stays SFW indefinitely, which crushes conversion for adult-leaning offers.

## Status

Brownfield → MVP scaffold. Bot + automation code committed; operator setup steps (Pages 01–09 of the Craft playbook) still need execution.
