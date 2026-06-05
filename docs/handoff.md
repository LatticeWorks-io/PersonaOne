# Operator handoff — MVP code is shipped, what's left is YOU

The code-buildable path to first dollar is complete on branch `mvp-first-dollar` (PR #1). Tests: 50/50 passing. Everything below is **operator work** — accounts to create, money to spend, decisions only you can make.

## Code state (do not rebuild)

| Component | Path | Status |
|---|---|---|
| Telegram bot | `bot/main.py` + `bot/handlers.py` | ✅ |
| Claude wrapper | `bot/claude_client.py` | ✅ |
| Stars + crypto paywall | `bot/handlers.py` | ✅ |
| NowPayments IPN HTTP webhook | `bot/webhook.py` | ✅ |
| SQLite storage + revenue aggregation | `bot/storage.py` | ✅ |
| Operator `/stats` command | `bot/handlers.py` `cmd_stats` | ✅ |
| Persona YAML loader (disclosed-AI enforced) | `bot/persona.py` + `personas/_template.yaml` | ✅ |
| Apify discovery loop | `automation/discovery_loop.py` + `automation/apify_client.py` | ✅ verified |
| late.dev content scheduler | `automation/content_loop.py` + `automation/late_client.py` | ✅ verified |
| Weekly cost report | `scripts/costs_report.py` | ✅ |
| systemd units | `bot/systemd/`, `automation/systemd/` | ✅ |
| End-to-end tests | `bot/tests/` (50 cases) | ✅ |

## Operator work — in execution order

### Decision before any spend

- [ ] **Persona angle.** Run `prompts/acc-personas-research.md` (claude.ai Research mode or `scripts/research_acc_personas.py`). Pick the top archetype. Without this, every step below is wasted motion.
- [ ] **ACC enrollment in or out?** Page 11 was deferred to v1.1 — but without ACC, Twitter stays SFW indefinitely and conversion for adult-leaning offers collapses. Decide before you start the Twitter warmup.

### Phase A — Operator surface (~3 hr, finishes Craft Pages 01–03)

- [ ] Finish Page 01 cards 4–10 — Gmail, phone, Privacy.com, virtual card, tax structure, sterilize profile, final verify
- [ ] Page 02 — Porkbun domain registration (10 cards)
- [ ] Page 03 — Migadu email + DNS (10 cards)

### Phase B — Persona file + content (~3 hr)

- [ ] Copy `personas/_template.yaml` → `personas/persona-one.yaml`, fill in the angle from research, set offer prices
- [ ] Draft 22 warmup posts matching the slots in `content/warmup-template.md` (drop into `data/content_queue.jsonl` via `automation/content_loop.py --dry-run`, edit, set `approved=true`, then `--commit`)

### Phase C — Infra + KYC kickoff (~4 hr)

- [ ] Spin up $5–10/mo VPS (Hostinger or DigitalOcean) — trims Page 04
- [ ] Page 06 card 51–53: Anthropic Console account + funded + Claude API key
- [ ] Page 07 cards 61–67: Phantom wallet + recovery phrase secured + NowPayments account + KYC submitted (so the 1–3 day wait overlaps the rest of this phase)
- [ ] Deploy `bot/` + `automation/` to the VPS; set up `bot/.env` + `automation/.env` from the `.env.example` files
- [ ] Install systemd units: `sudo cp bot/systemd/lw-bot.service /etc/systemd/system/`, same for `automation/systemd/lw-discovery.{service,timer}`
- [ ] Reverse-proxy on the VPS: nginx forwards `POST /nowpayments/ipn` to `http://127.0.0.1:8081`; UFW keeps 8081 closed publicly

### Phase D — Apify + late.dev accounts (~1 hr)

- [ ] Sign up Apify; fund with $10 starter credit; get `LW_APIFY_TOKEN`
- [ ] Sign up late.dev; connect Twitter (after Phase E); run `LateClient.list_accounts()` once to find the X `accountId`; put it in `LW_LATE_TWITTER_ACCOUNT_ID`

### Phase E — Telegram + Twitter accounts (~2 hr)

- [ ] Page 08 cards 71–80 — Telegram install + account + BotFather bot + cloud password + smoke test
- [ ] Page 09 cards 81–90 — Twitter account, handle, placeholder bio (NO link yet), 2FA

### Phase F — Warmup + discovery (7 days, in parallel)

- [ ] Start the systemd discovery timer (`sudo systemctl enable --now lw-discovery.timer`)
- [ ] Daily 30 min: review `data/reply_queue.jsonl`, post 15–20 thoughtful replies
- [ ] Days 4–6: review `data/shoutout_candidates.jsonl`, DM 5 candidates with the template in `docs/discovery.md`, lock 2–3 paid shoutouts for day 7
- [ ] `content_loop.py --dry-run` + approve + `--commit` schedules the warmup posts via late.dev
- [ ] Resume Page 07 cards 68–70 once NowPayments KYC clears

### Phase G — Launch

- [ ] Update Twitter bio with the disclosed-AI line + the domain link
- [ ] Paid shoutouts land in a 4-hour window
- [ ] First inbound DM → first paid Stars/crypto transaction → MVP validated

### Phase H — Final smoke (~1 hr)

- [ ] Page 12 card 117: full pipeline test Twitter → Telegram → Stars payment → Claude convo
- [ ] Repeat with crypto rail: NowPayments invoice → IPN webhook → paid state flip

## Money math reference

| Service | Setup | Recurring | Source of truth |
|---|---|---|---|
| Domain (Porkbun) | $10/yr | — | Page 02 |
| Migadu email | $19/yr | — | Page 03 |
| VPS | $0 | $5–10/mo | Page 04 trimmed |
| Anthropic | $5 minimum | usage | Page 06 cards 51–53 |
| NowPayments | $0 | 0.5% per tx | Page 07 cards 65–67 |
| Apify | $5 minimum | ~$3/mo (verified 2026-06-05) | `docs/automation.md` |
| late.dev | $0 trial | $25/mo typical | `LW_LATE_MONTHLY_USD` |
| Paid shoutouts | $200–500 launch week | $0–200/mo ongoing | `docs/discovery.md` |
| **First-30-days total** | **~$300** | **~$50/mo** | — |

The weekly cost report (`scripts/costs_report.py`) ingests Apify run logs + Claude call logs + fixed monthly costs and produces a markdown rollup. Run it via cron once the VPS is up.

## What this MVP does NOT include (deferred to v1.1)

- Image gen (RunPod + Flux) — Page 05 cut
- Voice clone (ElevenLabs) — Page 12 voice cards cut
- Hostwinds dedicated box — VPS substitute is fine until load justifies migration
- Multi-persona scaling — prove with one
- Shoutout management module — operator playbook in `docs/discovery.md` is the v1 version
- Postmark transactional email — only needed when ACC subscriptions want receipts

## Where to start when you reopen the repo

```bash
cd /opt/latticeworks.io
git log --oneline mvp-first-dollar ^main
gh pr view 1
cat docs/handoff.md   # this file
```

The PR is the diff; this doc is the path forward.
