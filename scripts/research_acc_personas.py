"""Run the ACC persona market-research prompt against the Anthropic Messages API
with web_search, output to a markdown file with citations.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/research_acc_personas.py \\
        prompts/acc-personas-research.md \\
        > reports/acc-personas-$(date +%Y%m%d).md

Cost envelope (rough): ~$0.08 in web_search fees (8 searches × $0.01 each) +
~$0.30 in Opus tokens. Under $0.50 per run.
"""
from __future__ import annotations

import sys
from pathlib import Path

import anthropic

PROMPT_PATH = Path(sys.argv[1])
prompt = PROMPT_PATH.read_text()

client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=8192,
    messages=[{"role": "user", "content": prompt}],
    tools=[
        {
            "type": "web_search_20260209",
            "name": "web_search",
            "max_uses": 8,  # cap spend
        }
    ],
)

sources: list[str] = []
for block in resp.content:
    if block.type == "text":
        print(block.text)
        for cite in getattr(block, "citations", None) or []:
            url = getattr(cite, "url", None)
            title = getattr(cite, "title", None) or url
            if url and not any(url in s for s in sources):
                sources.append(f"- [{title}]({url})")

if sources:
    print("\n\n---\n\n## Sources\n")
    print("\n".join(sources))

u = resp.usage
print(
    f"\n# tokens: in={u.input_tokens} out={u.output_tokens} "
    f"cache_read={getattr(u, 'cache_read_input_tokens', 0)}",
    file=sys.stderr,
)
