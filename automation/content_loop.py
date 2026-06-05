"""Content loop. Reads `content/warmup-template.md`'s schedule + the persona file,
generates a draft for each unfilled slot via Claude, and schedules approved drafts
through late.dev.

Mode of operation:

- `--dry-run`: prints proposed drafts, does NOT call late.dev.
- `--commit`: schedules everything in `data/content_queue.jsonl` whose `approved=true`
  flag is set. The operator approves by editing the JSONL (or via a future UI).

This split keeps Claude's drafts in front of human eyes before they hit Twitter.
The loop never auto-publishes.

Run:
    LW_CLAUDE_KEY=sk-ant-... LW_PERSONA_PATH=personas/persona-one.yaml \
    python -m automation.content_loop --dry-run
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from anthropic import AsyncAnthropic

from automation.late_client import LateClient
from bot.persona import load_persona

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("lw-content")

QUEUE_PATH = Path("data/content_queue.jsonl")


async def draft_post(claude: AsyncAnthropic, model: str, persona_prompt: str, slot_intent: str) -> str:
    resp = await claude.messages.create(
        model=model,
        max_tokens=200,
        system=persona_prompt + "\n\nWhen given a content slot intent, return ONLY the post text. No commentary, no quotes around it. Stay under 280 chars. Match the persona's voice.",
        messages=[{"role": "user", "content": slot_intent}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print drafts, don't schedule.")
    parser.add_argument("--commit", action="store_true", help="Schedule approved drafts via late.dev.")
    parser.add_argument(
        "--slots-file",
        default="content/warmup-template.md",
        help="Path to the warmup template — slot intents are extracted from its checklist lines.",
    )
    args = parser.parse_args()

    persona = load_persona(os.environ.get("LW_PERSONA_PATH", "personas/persona-one.yaml"))

    if args.commit:
        late = LateClient(
            api_key=os.environ["LW_LATE_API_KEY"],
            twitter_profile_id=os.environ["LW_LATE_TWITTER_PROFILE_ID"],
        )
        QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not QUEUE_PATH.exists():
            log.info("No queue at %s — nothing to commit. Run --dry-run first.", QUEUE_PATH)
            return
        scheduled = 0
        for line in QUEUE_PATH.read_text().splitlines():
            item = json.loads(line)
            if not item.get("approved"):
                continue
            if item.get("scheduled_id"):
                continue
            sp = await late.schedule_post(
                content=item["draft"],
                scheduled_at_iso=item["scheduled_at"],
            )
            item["scheduled_id"] = sp.id
            scheduled += 1
        # Rewrite with scheduled IDs back-filled.
        QUEUE_PATH.write_text("\n".join(json.dumps(item) for item in (json.loads(l) for l in QUEUE_PATH.read_text().splitlines())) + "\n")
        log.info("Scheduled %d posts.", scheduled)
        return

    # Dry-run path
    claude = AsyncAnthropic(api_key=os.environ["LW_CLAUDE_KEY"])
    model = os.environ.get("LW_CLAUDE_MODEL", "claude-sonnet-4-6")
    slots = [
        line.strip()
        for line in Path(args.slots_file).read_text().splitlines()
        if line.strip().startswith("- [ ]")
    ]
    log.info("Found %d unfilled slots in %s", len(slots), args.slots_file)
    drafts: list[dict] = []
    now_iso = datetime.now(timezone.utc).isoformat()
    for slot in slots:
        draft = await draft_post(claude, model, persona.system_prompt, slot)
        log.info("SLOT: %s\n  → %s", slot, draft)
        drafts.append(
            {
                "slot_intent": slot,
                "draft": draft,
                "scheduled_at": now_iso,  # operator updates per slot before --commit
                "approved": False,
                "scheduled_id": None,
            }
        )
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text("\n".join(json.dumps(d) for d in drafts) + "\n")
    log.info("Wrote %d drafts to %s. Edit, set approved=true, then run --commit.", len(drafts), QUEUE_PATH)


if __name__ == "__main__":
    asyncio.run(main())
