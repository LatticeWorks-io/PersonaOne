#!/usr/bin/env python3
"""Fetch LatticeWorks Craft docs as markdown into craft-content/.

Reads page IDs from ../craft-pages.json and writes one .md per page plus
start-here.md. Run from anywhere; output dir is resolved relative to this
script.
"""

import json
import urllib.request
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IDS_FILE = REPO / "craft-pages.json"
OUT_DIR = REPO / "craft-content"

API = (Path.home() / ".config" / "craft" / "connect-url").read_text().strip()
TOKEN = (Path.home() / ".config" / "craft" / "token").read_text().strip()


def fetch_markdown(block_id: str) -> str:
    url = f"{API}/blocks?id={block_id}&maxDepth=-1"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "text/markdown")
    req.add_header("User-Agent", "curl/8.5.0")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GET /blocks?id={block_id} -> {e.code}: {e.read().decode()}")


def main() -> None:
    ids = json.loads(IDS_FILE.read_text())
    OUT_DIR.mkdir(exist_ok=True)

    targets = [("start-here", ids["start_here_doc_id"])]
    for key, page in sorted(ids["pages"].items()):
        targets.append((key.replace("_", "-"), page["doc_id"]))

    for name, doc_id in targets:
        out_path = OUT_DIR / f"{name}.md"
        md = fetch_markdown(doc_id)
        out_path.write_text(md)
        print(f"[OK] {name} -> {out_path.relative_to(REPO)} ({len(md)} bytes)")


if __name__ == "__main__":
    main()
