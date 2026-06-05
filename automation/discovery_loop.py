"""Discovery loop. Runs daily as a systemd timer.

Three jobs per run:

1. Pull shoutout candidates from Apify (Twitter followers of seed accounts in
   the persona's niche, filtered to 10k–100k followers). Append to
   `data/shoutout_candidates.jsonl`, deduped by handle.

2. Pull viral reply targets from Apify (last-24h tweets in niche, >1k likes).
   Write to `data/reply_queue.jsonl` — the operator reviews and picks 15–20 per day.

3. Print a short summary so the systemd journal carries the day's numbers.

Both lists are append-only; review and shoutout-outreach happen in the operator's
hands (or in v1.1, the shoutout management module).

Run:
    LW_APIFY_TOKEN=apify_xxx \
    LW_DISCOVERY_SEEDS="@bigaccount,@anotherone" \
    LW_DISCOVERY_KEYWORDS="late night dms,parasocial,gf simulator" \
    python -m automation.discovery_loop
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from automation.apify_client import ApifyDiscovery

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("lw-discovery")

DATA_DIR = Path("data")
CANDIDATES_PATH = DATA_DIR / "shoutout_candidates.jsonl"
REPLIES_PATH = DATA_DIR / "reply_queue.jsonl"
APIFY_RUNS_PATH = DATA_DIR / "apify_runs.jsonl"

# Per-result + startup cost estimates per actor, in USD.
# Verified 2026-06-05 against Apify Store pricing.
ACTOR_COST: dict[str, dict[str, float]] = {
    "xquik/x-follower-scraper": {"per_result": 0.00015, "startup": 0.0},
    "api-ninja/x-twitter-advanced-search": {"per_result": 0.00035, "startup": 0.01},
}


def _estimate_cost(actor: str, results: int) -> float:
    p = ACTOR_COST.get(actor, {"per_result": 0.0, "startup": 0.0})
    return results * p["per_result"] + p["startup"]


def _log_apify_run(actor: str, results: int) -> None:
    """Append a run row to data/apify_runs.jsonl for the weekly cost report."""
    APIFY_RUNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "results_count": int(results),
        "cost_usd_estimate": round(_estimate_cost(actor, results), 6),
    }
    with APIFY_RUNS_PATH.open("a") as f:
        f.write(json.dumps(row) + "\n")


def _append_dedup(path: Path, items: list[dict], dedup_key: str) -> int:
    """Append new items to a JSONL file, skipping ones whose dedup_key already exists. Returns count added."""
    path.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                seen.add(json.loads(line)[dedup_key])
            except (json.JSONDecodeError, KeyError):
                continue
    added = 0
    with path.open("a") as f:
        for item in items:
            key = item.get(dedup_key)
            if not key or key in seen:
                continue
            f.write(json.dumps(item) + "\n")
            seen.add(key)
            added += 1
    return added


async def main() -> None:
    token = os.environ["LW_APIFY_TOKEN"]
    seeds = [s.strip().lstrip("@") for s in os.environ["LW_DISCOVERY_SEEDS"].split(",") if s.strip()]
    keywords = [k.strip() for k in os.environ["LW_DISCOVERY_KEYWORDS"].split(",") if k.strip()]

    discovery = ApifyDiscovery(api_token=token)

    log.info("Pulling shoutout candidates from %d seed handles…", len(seeds))
    candidates = await discovery.find_shoutout_candidates(seeds)
    _log_apify_run("xquik/x-follower-scraper", len(candidates))
    added_c = _append_dedup(
        CANDIDATES_PATH,
        [asdict(c) for c in candidates],
        dedup_key="handle",
    )
    log.info("  +%d new candidates (total file: %s)", added_c, CANDIDATES_PATH)

    log.info("Pulling reply targets for %d keywords…", len(keywords))
    targets = await discovery.find_reply_targets(keywords)
    _log_apify_run("api-ninja/x-twitter-advanced-search", len(targets))
    added_r = _append_dedup(
        REPLIES_PATH,
        [asdict(t) for t in targets],
        dedup_key="tweet_id",
    )
    log.info("  +%d new reply targets (total file: %s)", added_r, REPLIES_PATH)

    log.info("Discovery loop done. Review %s and queue 15–20 replies today.", REPLIES_PATH)


if __name__ == "__main__":
    asyncio.run(main())
