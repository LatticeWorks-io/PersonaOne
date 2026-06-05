# MVP runbook — zero → first paid customer

> This is the day-by-day execution doc derived from `~/.claude/plans/glittery-stirring-flask.md`. The 120-step Craft playbook is the source of truth for *steps*; this runbook is the source of truth for *order* and *what to cut*.

## Critical-path phases

| Phase | What | Time | Refs |
|---|---|---|---|
| A | Operator surface (finish Page 01, do Pages 02 + 03) | 1 sitting, ~3 hr | `craft-content/page-01.md` cards 4–10, `page-02.md`, `page-03.md` |
| B | Persona + content pre-stage | 1 sitting, ~3 hr | `personas/_template.yaml`, `content/warmup-template.md` |
| C | Infra + crypto KYC kickoff | 1 sitting, ~4 hr | `craft-content/page-04.md` (trimmed to VPS), Claude card 51-53, full Page 07 KYC submission so it overlaps Phase D |
| D | Bot build | (already shipped — `bot/`) | — |
| D2 | Automation wiring (Apify + late.dev) | 1 sitting, ~2 hr | `automation/.env.example`, `automation/README.md` |
| E | Telegram + Twitter accounts | 1 sitting, ~2 hr | `craft-content/page-08.md`, `page-09.md` |
| F | Warmup + discovery in parallel | 7 days | `content/warmup-template.md`, `docs/discovery.md` |
| G | Launch | day 7 | paid shoutouts land + bio link goes hot |
| H | Final smoke test | 1 sitting, ~1 hr | `craft-content/page-12.md` card 117 |

## Cuts vs the original 120 steps

| Page | Status in MVP |
|---|---|
| 01 — Workspace | **Keep** (7 cards left) |
| 02 — Domain | **Keep** (10 cards) |
| 03 — Migadu | **Keep** (10 cards) |
| 04 — Hostwinds dedicated | **Replace** with $5–10/mo VPS (Hostinger/DO) |
| 05 — RunPod + B2 + Bunny | **Cut** — no image gen, no media in v1 |
| 06 — Claude + OpenRouter + Postmark | **Trim** — Claude only |
| 07 — NowPayments + crypto + KYC | **Keep, parallel** — KYC submit during Phase C so wait overlaps Phase D |
| 08 — Telegram | **Keep** |
| 09 — Twitter account | **Keep** |
| 10 — Twitter warmup 14d | **Compress** to 7d (see `content/warmup-template.md`) |
| 11 — Twitter ACC | **Reopen for review** — was deferred, but without ACC the Twitter side stays SFW indefinitely, which crushes conversion for adult-leaning offers. Decide before Phase E. |
| 12 — Voice + smoke test | **Defer voice; keep smoke test** |

## Discovery built into Phase F

The original plan assumed warmup posts → organic reach → followers. They don't. See `docs/discovery.md`. Phase F runs **two loops in parallel**:

1. **Content loop** — pre-staged posts in `content/warmup-template.md` go out 1–2/day. Scheduled via `automation/content_loop.py` → late.dev.
2. **Discovery loop** — `automation/discovery_loop.py` runs daily via `lw-discovery.timer`, populating `data/reply_queue.jsonl` and `data/shoutout_candidates.jsonl`.

Operator daily work during warmup:
- 30 min: pick 15–20 reply targets from the queue, post replies.
- 15 min: review shoutout candidates, DM 5 with the template in `docs/discovery.md`, negotiate placements for launch day.

## End-to-end verification (after Phase G)

1. From a separate device, open the persona's Twitter, click bio link, land on domain, click through to Telegram.
2. `/start` the bot. Confirm persona greeting + paywall buttons.
3. Pay smallest Stars offer from a test Telegram account. Confirm Claude-driven convo begins.
4. End the conversation. Confirm session closes; re-engagement requires a new payment.
5. Repeat 3 via crypto rail: send a NowPayments invoice, pay from operator wallet, confirm IPN webhook flips paid state.

If all 5 pass with at least one **inbound** stranger-paid conversion in the launch week, MVP is validated.

## What this runbook does NOT cover

Deferred to v1.1 with intent:

- Hostwinds dedicated (when bot load justifies migration off the VPS)
- RunPod + Flux image gen (when persona needs custom imagery)
- ElevenLabs voice (when conversion data shows voice notes drive revenue)
- Multi-persona scaling (prove with one)
- Shoutout management module proper (operator playbook in `docs/discovery.md` is the v1 version)
- Postmark transactional email (only when ACC subscriptions want receipts)
