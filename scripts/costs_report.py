"""Weekly cost report.

Reads:
  - data/apify_runs.jsonl   (rows appended by automation/discovery_loop.py)
  - data/claude_calls.jsonl (optional; rows appended by bot/claude_client.py
    when token-usage logging is enabled — file may be absent)

Adds fixed monthly costs from env (with defaults):
  - LW_LATE_MONTHLY_USD  (default 25.0)
  - LW_VPS_MONTHLY_USD   (default 7.0)

Outputs a markdown report to stdout. Operator runs weekly:

    python3 scripts/costs_report.py > reports/costs-$(date +%G-W%V).md

Pure-ish: load_jsonl / window_runs / summarize are importable and tested.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

APIFY_LOG = Path("data/apify_runs.jsonl")
CLAUDE_LOG = Path("data/claude_calls.jsonl")

# Anthropic public pricing (Opus 4.7 baseline, USD per 1M tokens).
# Override per-call by including {"cost_usd": x} in the log row.
CLAUDE_INPUT_PER_MTOK = 15.0
CLAUDE_OUTPUT_PER_MTOK = 75.0


@dataclass
class ApifyRun:
    timestamp: str
    actor: str
    results_count: int
    cost_usd_estimate: float


@dataclass
class ClaudeCall:
    timestamp: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def window_runs(rows: list[dict], *, since: datetime) -> list[dict]:
    out = []
    for r in rows:
        t = _parse_iso(r.get("timestamp", ""))
        if t and t >= since:
            out.append(r)
    return out


def claude_call_cost(row: dict) -> float:
    """Return USD cost for one Claude call.

    Priority: explicit cost_usd > computed from tokens with default pricing.
    """
    if "cost_usd" in row:
        try:
            return float(row["cost_usd"])
        except (TypeError, ValueError):
            pass
    inp = int(row.get("input_tokens") or 0)
    out = int(row.get("output_tokens") or 0)
    return inp / 1_000_000 * CLAUDE_INPUT_PER_MTOK + out / 1_000_000 * CLAUDE_OUTPUT_PER_MTOK


def summarize(
    apify_rows: list[dict],
    claude_rows: list[dict],
    *,
    late_monthly: float,
    vps_monthly: float,
    window_days: int = 7,
) -> dict:
    """Compute totals + per-service breakdown for the window.

    Fixed monthly costs are pro-rated to the window so the comparison is fair.
    """
    apify_total = sum(float(r.get("cost_usd_estimate") or 0.0) for r in apify_rows)
    by_actor: dict[str, dict] = {}
    for r in apify_rows:
        actor = str(r.get("actor", "unknown"))
        b = by_actor.setdefault(actor, {"runs": 0, "results": 0, "cost_usd": 0.0})
        b["runs"] += 1
        b["results"] += int(r.get("results_count") or 0)
        b["cost_usd"] += float(r.get("cost_usd_estimate") or 0.0)

    claude_total = sum(claude_call_cost(r) for r in claude_rows)
    claude_calls = len(claude_rows)
    claude_in_tokens = sum(int(r.get("input_tokens") or 0) for r in claude_rows)
    claude_out_tokens = sum(int(r.get("output_tokens") or 0) for r in claude_rows)

    pro_rate = window_days / 30.0  # rough month length
    late_window = late_monthly * pro_rate
    vps_window = vps_monthly * pro_rate

    grand_total = apify_total + claude_total + late_window + vps_window
    return {
        "window_days": window_days,
        "apify_total": apify_total,
        "apify_by_actor": by_actor,
        "claude_total": claude_total,
        "claude_calls": claude_calls,
        "claude_input_tokens": claude_in_tokens,
        "claude_output_tokens": claude_out_tokens,
        "late_window": late_window,
        "vps_window": vps_window,
        "grand_total": grand_total,
        "late_monthly": late_monthly,
        "vps_monthly": vps_monthly,
    }


def render_markdown(summary: dict, *, now: datetime) -> str:
    lines: list[str] = []
    lines.append(f"# LatticeWorks cost report — {now.date().isoformat()}")
    lines.append("")
    lines.append(f"Window: last {summary['window_days']} days. Fixed monthly costs pro-rated.")
    lines.append("")
    lines.append(f"**Total ({summary['window_days']}d): ${summary['grand_total']:.2f}**")
    lines.append("")
    lines.append("## Breakdown")
    lines.append("")
    lines.append("| Service | Window cost | Notes |")
    lines.append("|---|---|---|")
    lines.append(f"| Apify | ${summary['apify_total']:.2f} | {sum(b['runs'] for b in summary['apify_by_actor'].values())} runs |")
    lines.append(
        f"| Claude | ${summary['claude_total']:.2f} | {summary['claude_calls']} calls, "
        f"{summary['claude_input_tokens']:,} in / {summary['claude_output_tokens']:,} out tokens |"
    )
    lines.append(f"| late.dev | ${summary['late_window']:.2f} | ${summary['late_monthly']:.0f}/mo pro-rated |")
    lines.append(f"| VPS | ${summary['vps_window']:.2f} | ${summary['vps_monthly']:.0f}/mo pro-rated |")
    lines.append("")
    if summary["apify_by_actor"]:
        lines.append("## Apify per-actor")
        lines.append("")
        lines.append("| Actor | Runs | Results | Cost |")
        lines.append("|---|---|---|---|")
        for actor, b in sorted(summary["apify_by_actor"].items()):
            lines.append(f"| `{actor}` | {b['runs']} | {b['results']} | ${b['cost_usd']:.2f} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=7)
    apify_rows = window_runs(load_jsonl(APIFY_LOG), since=since)
    claude_rows = window_runs(load_jsonl(CLAUDE_LOG), since=since)
    late_monthly = float(os.environ.get("LW_LATE_MONTHLY_USD", "25.0"))
    vps_monthly = float(os.environ.get("LW_VPS_MONTHLY_USD", "7.0"))
    summary = summarize(
        apify_rows,
        claude_rows,
        late_monthly=late_monthly,
        vps_monthly=vps_monthly,
        window_days=7,
    )
    sys.stdout.write(render_markdown(summary, now=now))


if __name__ == "__main__":
    main()
