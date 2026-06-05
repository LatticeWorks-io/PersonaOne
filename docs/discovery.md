# Discovery — how a brand-new account gets found from zero

> The unanswered question from the original 120-step playbook. Warmup posts on a fresh account get ~0 organic reach. The link-in-bio funnel doesn't fire if no one sees the bio. This doc closes that gap.

## The four channels (in order of cost-per-eyeball)

| # | Channel | Cost | Speed | Notes |
|---|---|---|---|---|
| 1 | Reply guy | $0 | Slow (compounds over weeks) | Daily, 15–30 thoughtful replies to large in-niche accounts. Algorithm learns your niche, you borrow their audience. Automated via `automation/discovery_loop.py` → `data/reply_queue.jsonl`. |
| 2 | SFS (shoutout-for-shoutout) | $0 | Medium | Once you've got ~100+ followers from #1, trade promo with similar-sized accounts. Free but peer-locked. |
| 3 | Paid shoutouts from aged accounts | $50–500 each | Fast (24-hr spike) | The unlock. Buy 2–3 placements from 10k–100k-follower in-niche accounts, time them to land same day as your "DM me" hook. Vendor DB builds itself via `automation/discovery_loop.py` → `data/shoutout_candidates.jsonl`. |
| 4 | Twitter ACC discoverability | KYC + 14-day warmup | Compounding | Once enrolled, Twitter surfaces you to adult-content viewers. **Strongly consider keeping this in MVP** despite the original cut — without ACC, the bio stays SFW and conversion is much lower for adult-leaning offers. |

## The MVP discovery sequence

**Warmup days 1–4 (reply guy only)**
- Daily: 15–30 replies on large in-niche accounts (`automation/discovery_loop.py` populates `data/reply_queue.jsonl`; operator picks).
- Target: 50–200 first followers organic.

**Warmup days 4–6 (start shoutout outreach)**
- Daily: review `data/shoutout_candidates.jsonl`, DM 5 of them with a shoutout proposal (template below).
- Negotiate price (typical: $50–200 for ~30k followers, $200–500 for ~100k).
- Lock 2–3 placements for launch day (day 7 in the compressed warmup).

**Launch day 7**
- Paid shoutouts land in a 4-hour window (operator coordinates).
- Your own "DM me on Telegram" post lands at the start of that window.
- Bio link active, points to landing → Telegram bot.

**Days 8+ (ongoing)**
- `discovery_loop.py` runs daily at 09:07. Operator reviews queues over coffee.
- Reinvest first revenue: every $X earned → $X/2 back into shoutouts for week 2.

## Cold-outreach shoutout DM template

> hey — i've been following you and your aesthetic is exactly the lane i'm in. just spun up, building from scratch. looking to buy 1 shoutout from you this week if you do paid placements. what's your rate for a single tweet + a quote-retweet 24h later? happy to pay via crypto or [your preference]. timing is flexible to your queue.

Adjust voice to match the persona. Send via Twitter DM (not email).

## Tracking what works

In `data/shoutout_log.csv` (operator-maintained for v1; v1.1 = pipe directly from NowPayments/Stars webhooks):

```
date,vendor_handle,vendor_followers,amount_usd,impressions_estimated,clicks_to_landing,dms_to_bot,paid_conversions,revenue_usd
2026-06-15,@example,45000,150,12000,80,18,3,225
```

Keep this even at MVP scale. After 5–10 placements, you can compute cost-per-paid-conversion per vendor and know which placements to re-up. This is the data that makes shoutouts a flywheel rather than a tax.

## Anti-patterns to avoid

- **Bot networks / follower-buy services** — instant ban or shadowban. Don't.
- **Spammy reply-guy** (one-liners, generic "this!"). Looks bot-shaped; algorithm de-prioritizes.
- **Cold DMing buyers directly** before they've shown intent. Wastes the persona's "i don't push" voice and is a TOS gray zone.
- **Going broad** (multi-niche). The algorithm rewards narrow niches in the warmup window. Pick one and stay tight.
