#!/usr/bin/env python3
"""Resume LatticeWorks build: finish Page 09, build Pages 10-12."""

import json
import time
import urllib.request
from pathlib import Path

API = (Path.home() / ".config" / "craft" / "connect-url").read_text().strip()
AUTH = (Path.home() / ".config" / "craft" / "token").read_text().strip()

# Sleep between calls to avoid rate limit
SLEEP_BETWEEN = 0.7

def call(method, path, body=None, retries=3):
    for attempt in range(retries):
        url = f"{API}{path}"
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {AUTH}")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "curl/8.5.0")
        try:
            with urllib.request.urlopen(req) as resp:
                time.sleep(SLEEP_BETWEEN)
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 10 * (attempt + 1)
                print(f"  Rate limited; sleeping {wait}s")
                time.sleep(wait)
                continue
            raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode()}")

# Existing Page 09 doc id (built before rate limit hit)
PAGE_09_DOC_ID = "2261b5e7-dc0b-7e31-487f-e37c1f2fab40"
FOLDER_ID = "50527e79-f818-7a20-700f-d6d0596216ac"

KANBAN_CALLOUT = """<callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>"""


def build_page_from_scratch(num, title, intro, cards, start_step):
    """Full build for pages that don't exist yet."""
    r = call("POST", "/documents", {
        "documents": [{"title": f"Page {num:02d} — {title}"}],
        "destination": {"folderId": FOLDER_ID},
    })
    doc_id = r["items"][0]["id"]
    print(f"[OK] Page {num:02d} doc: id={doc_id}")

    full_intro = f"# Page {num:02d} — {title}\n\n{KANBAN_CALLOUT}\n\n{intro}"
    call("POST", "/blocks", {
        "markdown": full_intro,
        "position": {"position": "end", "pageId": doc_id},
    })

    return add_kanban_and_cards(num, doc_id, cards, start_step)


def add_kanban_and_cards(num, doc_id, cards, start_step):
    """Add collection + cards to an existing doc."""
    r = call("POST", "/collections", {
        "schema": {
            "name": f"Page {num:02d} Microsteps",
            "properties": [
                {"type": "singleSelect", "name": "Status", "options": [
                    {"name": "Todo", "color": "gray"},
                    {"name": "In Progress", "color": "sky-blue"},
                    {"name": "Done", "color": "mint-green"},
                ]},
                {"type": "number", "name": "Step"},
            ],
        },
        "position": {"position": "end", "pageId": doc_id},
    })
    coll_id = r["collectionBlockId"]

    items_payload = [
        {"title": c["title"], "properties": {"status": "Todo", "step": start_step + i}}
        for i, c in enumerate(cards)
    ]
    r = call("POST", f"/collections/{coll_id}/items", {"items": items_payload})
    item_ids = [item["id"] for item in r["items"]]

    for i, (card, item_id) in enumerate(zip(cards, item_ids), 1):
        call("POST", "/blocks", {
            "markdown": card["body"],
            "position": {"position": "end", "pageId": item_id},
        })
    print(f"[OK] Page {num:02d}: collection + {len(item_ids)} cards + bodies")

    return {"doc_id": doc_id, "collection_id": coll_id}


# Import card data from the previous script
import sys
sys.path.insert(0, '/tmp')
from build_lw_pages_02_12 import page09_cards, page10_cards, page11_cards, page12_cards

# Resume Page 09
print("--- Resuming Page 09 (doc exists, building collection + cards) ---")
page09_result = add_kanban_and_cards(9, PAGE_09_DOC_ID, page09_cards, 81)

# Build Pages 10, 11, 12
print("--- Building Page 10 ---")
page10_result = build_page_from_scratch(
    10, "Twitter warmup (7-14 days)",
    "**Goal:** Age the new Twitter account with 14 days of SFW activity before ACC enrollment. This page spans ~2 weeks — daily small actions, not one sitting.",
    page10_cards, 91,
)

print("--- Building Page 11 ---")
page11_result = build_page_from_scratch(
    11, "Twitter ACC enrollment",
    "**Goal:** Apply to and get approved for Twitter's Adult Content Creator program. Includes 1-7 day review. Requires Page 10 complete (14-day warmup).",
    page11_cards, 101,
)

print("--- Building Page 12 ---")
page12_result = build_page_from_scratch(
    12, "Voice + final smoke test",
    "**Goal:** Train the persona's voice clone in ElevenLabs and verify all end-to-end pipelines. ~2 hours + voice training time. Requires all prior pages complete.",
    page12_cards, 111,
)

# Update IDs file
IDS_FILE = Path.home() / ".config" / "craft" / "latticeworks-ids.json"
ids = json.loads(IDS_FILE.read_text())
ids["pages"]["page_09"] = {"title": "Page 09 — Twitter account creation", "doc_id": PAGE_09_DOC_ID, "collection_id": page09_result["collection_id"]}
ids["pages"]["page_10"] = {"title": "Page 10 — Twitter warmup (7-14 days)", "doc_id": page10_result["doc_id"], "collection_id": page10_result["collection_id"]}
ids["pages"]["page_11"] = {"title": "Page 11 — Twitter ACC enrollment", "doc_id": page11_result["doc_id"], "collection_id": page11_result["collection_id"]}
ids["pages"]["page_12"] = {"title": "Page 12 — Voice + final smoke test", "doc_id": page12_result["doc_id"], "collection_id": page12_result["collection_id"]}
# Also stub out pages 02-08 which we know exist
for pnum, doc_id in [
    (2, "d7aa9d6a-7fb2-aad1-6ffb-36fc80eb1aef"),
    (3, "da4d46c7-ee25-e5d0-0226-3cbcee320eb5"),
    (4, "b8b8785d-443b-e58b-a547-2090a64a33ca"),
    (5, "02297da2-f2e8-9404-2c28-63098264278c"),
    (6, "e87ecf08-1b77-5d85-9d96-e4cf5d19874b"),
    (7, "b3d122eb-9864-4855-5d0d-cf0331c76926"),
    (8, "397ada36-43cf-9a26-b423-08e3b91ca3d7"),
]:
    if f"page_{pnum:02d}" not in ids["pages"]:
        ids["pages"][f"page_{pnum:02d}"] = {"doc_id": doc_id}

IDS_FILE.write_text(json.dumps(ids, indent=2))
print()
print("ALL 12 PAGES COMPLETE")
