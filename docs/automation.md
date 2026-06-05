# Automation — how the loops wire together

Three things run on schedules or operator triggers. Together they remove the manual taxes that would otherwise stall warmup and discovery.

```
                         ┌──────────────────────┐
                         │  late.dev (Twitter)  │
                         │  scheduled posts     │
                         └──────────▲───────────┘
                                    │ --commit
                                    │
                   ┌──────── content_loop.py ────────┐
                   │  (operator-triggered, never auto)│
                   │  Claude drafts from persona +    │
                   │  warmup-template slots           │
                   └──────────────────────────────────┘

                   ┌──────── discovery_loop.py ───────┐
                   │  systemd timer: daily 09:07 local │
                   │  → reply_queue.jsonl              │
                   │  → shoutout_candidates.jsonl      │
                   └─────────────▲────────────────────┘
                                 │
                       ┌─────────┴─────────┐
                       │  Apify actors      │
                       │  (Twitter scrape)  │
                       └────────────────────┘

                              ┌────────────────────────┐
        Twitter DM ──► bio ──►│  Telegram bot (bot/)   │
                              │  Stars / NowPayments   │
                              │  Claude conversation   │
                              └────────────────────────┘
```

## Why these tools

- **Apify** is the cheapest way to get current Twitter scrape data without running our own Selenium fleet. The actors we use (`twitter-scraper-lite`, `tweet-scraper`) are public, well-maintained, and rate-limit-aware. ~$5/day at MVP scale.
- **late.dev** owns the publish step. It handles X's auth quirks, rate limits, and queue. We hand it scheduled drafts; we don't touch the Twitter API ourselves.
- **systemd timers** over cron because: persistent across reboots (`Persistent=true`), structured logging via journalctl, no lock-file races, the unit can declare `ProtectSystem=strict` for free hardening.

## What lives in `data/`

All loop output. Operator-readable JSONL. Git-ignored.

- `data/shoutout_candidates.jsonl` — handle, followers, bio, last_active_at. Append-only, dedup on `handle`.
- `data/reply_queue.jsonl` — tweet_id, author_handle, text, likes, posted_at. Append-only, dedup on `tweet_id`.
- `data/content_queue.jsonl` — slot_intent, draft, scheduled_at, approved, scheduled_id. Operator-edited; `content_loop --commit` only schedules `approved=true`.

## Safety rails

- **content_loop never auto-publishes.** `--dry-run` is the default. `--commit` only ships posts with `approved=true`. Human in the loop on every tweet.
- **discovery_loop never DMs anyone.** It only populates queues. The operator does the DM-ing.
- **No Apify run > 200 items default.** Tune `max_results` in `apify_client.py` if you want more; the higher you go the higher the run cost.

## Total automation budget at MVP scale

| Service | Monthly | Notes |
|---|---|---|
| Apify | ~$150 | 2 runs/day, ~200 items each |
| late.dev | $20–50 | Single Twitter profile tier |
| Claude (drafts) | <$10 | 22 warmup posts ≈ 10k tokens |
| VPS (Hostinger / DO) | $5–10 | Bot + loops co-located |
| **Total** | **~$200/mo** | vs. ~10 hr/week of operator time it replaces |
