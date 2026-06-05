# automation/

Loops that run on a schedule and remove the manual taxes from the warmup + ongoing playbook.

## Two loops

### `discovery_loop.py` — Apify
Daily, 09:07 local (systemd `lw-discovery.timer`).

- Pulls followers of seed in-niche accounts, filters to 10k–100k followers band, writes to `data/shoutout_candidates.jsonl`. This is your shoutout vendor DB, building itself.
- Pulls last-24h viral tweets matching niche keywords, writes to `data/reply_queue.jsonl`. Operator reviews each morning and picks 15–20 to reply to.

Both files are append-only and dedup on key (handle / tweet_id).

### `content_loop.py` — late.dev
Operator-triggered, not scheduled (you want eyes on every post before it goes live).

- `--dry-run`: extracts unfilled slots from `content/warmup-template.md`, asks Claude to draft each in the persona's voice, writes proposals to `data/content_queue.jsonl` with `approved=false`.
- `--commit`: reads the same file, schedules anything `approved=true` through late.dev's API.

## Cost envelope

- Apify: ~$5/day for two actor runs (one followers, one search). Scales with `maxItems`; tune in `apify_client.py`.
- late.dev: pricing tier dependent — typically $20–50/mo flat for the volumes here.
- Claude: drafting 22 warmup posts is ~10k output tokens, well under $1.

Total automation: under $200/mo at MVP scale, vs the manual labor it replaces.

## Setup

```bash
cd /opt/latticeworks.io
. .venv/bin/activate
pip install -r automation/requirements.txt
cp automation/.env.example automation/.env
# fill in tokens
sudo cp automation/systemd/lw-discovery.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now lw-discovery.timer
systemctl list-timers lw-discovery.timer
```
