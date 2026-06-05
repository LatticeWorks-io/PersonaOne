# prompts/

Long-form research and analysis prompts that get run against the Anthropic API (or pasted into claude.ai Research mode). Reports land in `reports/` alongside the prompt that produced them.

## acc-personas-research.md

Market research for disclosed-AI ACC persona angles. Two ways to run it.

### Option A: claude.ai Research mode
1. Open claude.ai, new chat, enable Research.
2. Paste the contents of `acc-personas-research.md`.
3. Wait 5–10 min. Copy the report to `reports/acc-personas-YYYYMMDD.md`.

### Option B: API (headless, ~$0.50 per run)
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
mkdir -p reports
python scripts/research_acc_personas.py prompts/acc-personas-research.md \
    > reports/acc-personas-$(date +%Y%m%d).md
```

Iterate the prompt, re-run, diff the reports. Sub-$1 per iteration so don't hesitate to refine.
