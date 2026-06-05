# personas/

One YAML file per persona. The bot loads exactly one (set by `LW_PERSONA_PATH`). Multi-persona is v1.1.

Use `_template.yaml` as the starting point — copy to e.g. `persona-one.yaml`, fill in.

The `system_prompt` is what shapes Claude's voice. Treat it like a contract: clearer prompt → tighter persona → higher conversion. The `voice_rules` array is documentation for the operator, not loaded by the bot — paste rules into the `system_prompt` directly.

**AI disclosure is non-negotiable.** Three places it must be present:
1. The Twitter bio (per ACC policy).
2. The bot greeting — see the `greeting` field in `_template.yaml`.
3. The system prompt — the persona must answer honestly if asked "are you AI?"

The persona can stay in character about *name, vibe, voice, mood*. It cannot deny being AI when the buyer probes. Disclosure in the bio plus a bot that denies being AI in chat is a fig-leaf disclosure and would push the product into deceptive-marketing territory — we don't build that.

Pricing notes (per README, NOT monthly subscription):
- `stars_price` is in Telegram XTR units. 1 ⭐ ≈ $0.013, so $5 ≈ 380⭐, $25 ≈ 1900⭐, $100 ≈ 7700⭐.
- `usd_price` mirrors the offer for the crypto rail. Keep them roughly aligned so both rails feel like the same product.
- Offers are **per-engagement / per-bundle**, not recurring. "Hour of chat", "5 custom pieces", "voice note bundle" — that shape.
