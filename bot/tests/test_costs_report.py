"""Tests for scripts/costs_report.py."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from scripts.costs_report import (
    claude_call_cost,
    load_jsonl,
    render_markdown,
    summarize,
    window_runs,
)


# ---------- load_jsonl ----------


def test_load_jsonl_missing_file_returns_empty(tmp_path):
    assert load_jsonl(tmp_path / "nope.jsonl") == []


def test_load_jsonl_skips_blank_and_malformed_lines(tmp_path):
    p = tmp_path / "x.jsonl"
    p.write_text('{"a": 1}\n\n  \nnot json\n{"a": 2}\n')
    rows = load_jsonl(p)
    assert rows == [{"a": 1}, {"a": 2}]


# ---------- window_runs ----------


def test_window_runs_filters_by_timestamp():
    now = datetime(2026, 6, 5, tzinfo=timezone.utc)
    rows = [
        {"timestamp": (now - timedelta(days=10)).isoformat(), "x": "old"},
        {"timestamp": (now - timedelta(days=3)).isoformat(), "x": "in"},
        {"timestamp": (now - timedelta(hours=1)).isoformat(), "x": "in"},
        {"timestamp": "garbage", "x": "skipped"},
    ]
    out = window_runs(rows, since=now - timedelta(days=7))
    assert [r["x"] for r in out] == ["in", "in"]


# ---------- claude_call_cost ----------


def test_claude_call_cost_uses_explicit_when_present():
    assert claude_call_cost({"cost_usd": 1.23, "input_tokens": 999, "output_tokens": 999}) == 1.23


def test_claude_call_cost_computes_from_tokens_with_default_pricing():
    # 1M input * $15/Mtok = $15; 1M output * $75/Mtok = $75; total $90
    assert claude_call_cost({"input_tokens": 1_000_000, "output_tokens": 1_000_000}) == pytest.approx(90.0)


def test_claude_call_cost_handles_missing_keys():
    assert claude_call_cost({}) == 0.0


# ---------- summarize ----------


def test_summarize_empty_inputs_returns_only_fixed_costs():
    s = summarize([], [], late_monthly=30.0, vps_monthly=10.0, window_days=7)
    expected_fixed = (30.0 + 10.0) * (7 / 30)
    assert s["apify_total"] == 0.0
    assert s["claude_total"] == 0.0
    assert s["claude_calls"] == 0
    assert s["grand_total"] == pytest.approx(expected_fixed)


def test_summarize_aggregates_apify_by_actor():
    apify = [
        {"actor": "a/x", "results_count": 100, "cost_usd_estimate": 0.05},
        {"actor": "a/x", "results_count": 50, "cost_usd_estimate": 0.025},
        {"actor": "b/y", "results_count": 200, "cost_usd_estimate": 0.07},
    ]
    s = summarize(apify, [], late_monthly=0, vps_monthly=0, window_days=7)
    assert s["apify_total"] == pytest.approx(0.145)
    assert s["apify_by_actor"]["a/x"] == {"runs": 2, "results": 150, "cost_usd": pytest.approx(0.075)}
    assert s["apify_by_actor"]["b/y"] == {"runs": 1, "results": 200, "cost_usd": pytest.approx(0.07)}


def test_summarize_sums_claude_token_costs():
    claude = [
        {"input_tokens": 1_000_000, "output_tokens": 0},  # $15
        {"input_tokens": 0, "output_tokens": 1_000_000},  # $75
        {"cost_usd": 0.50},                                # $0.50
    ]
    s = summarize([], claude, late_monthly=0, vps_monthly=0, window_days=7)
    assert s["claude_total"] == pytest.approx(15.0 + 75.0 + 0.5)
    assert s["claude_calls"] == 3
    assert s["claude_input_tokens"] == 1_000_000
    assert s["claude_output_tokens"] == 1_000_000


def test_summarize_grand_total_includes_fixed_pro_rated():
    apify = [{"actor": "a/x", "results_count": 1, "cost_usd_estimate": 1.0}]
    claude = [{"cost_usd": 2.0}]
    s = summarize(apify, claude, late_monthly=30.0, vps_monthly=15.0, window_days=7)
    fixed = (30.0 + 15.0) * (7 / 30)
    assert s["grand_total"] == pytest.approx(1.0 + 2.0 + fixed)


# ---------- render_markdown ----------


def test_render_markdown_includes_total_and_per_actor():
    apify = [{"actor": "xquik/x-follower-scraper", "results_count": 200, "cost_usd_estimate": 0.03}]
    s = summarize(apify, [], late_monthly=25.0, vps_monthly=7.0, window_days=7)
    md = render_markdown(s, now=datetime(2026, 6, 5, tzinfo=timezone.utc))
    assert "# LatticeWorks cost report — 2026-06-05" in md
    assert "Total (7d):" in md
    assert "xquik/x-follower-scraper" in md
    assert "200" in md
    # Fixed costs surface in the breakdown
    assert "late.dev" in md
    assert "VPS" in md


def test_render_markdown_omits_per_actor_table_when_no_apify():
    s = summarize([], [], late_monthly=25.0, vps_monthly=7.0, window_days=7)
    md = render_markdown(s, now=datetime(2026, 6, 5, tzinfo=timezone.utc))
    assert "Apify per-actor" not in md
