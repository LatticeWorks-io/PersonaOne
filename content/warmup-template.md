# Twitter content — first 7 days for a disclosed AI companion

> Builds initial follower count for a disclosed-AI product on Twitter. This is NOT a human-account warmup — every image is visibly AI-generated and labeled, every post leads with "AI companion." There is no "act human first" phase; the disclosure is the marketing.

## Operating rules

- **Every image is overtly AI-generated.** Stylized, clearly not photo-realistic, or watermarked/labeled. No mistaken-identity risk.
- **Every post leads with the product nature.** "AI companion," "AI girlfriend," "AI [whatever the angle is]" — first words.
- **Bio is live from day 1** with the AI label + the Telegram link + the price. No bait, no later-reveal.
- **Reply targets** are AI-companion-adjacent communities (r/replika, r/CharacterAI, AI-art Twitter, candy.ai discourse), not generic lifestyle accounts.
- **DO NOT post lifestyle / aesthetic content that implies a real person.** That's the predatory shape this product is explicitly not.

---

## Day 1 — launch (3 slots)

- [ ] 09:00 — launch post: "I built an AI companion. Here's what she does." 1 AI-generated portrait (labeled), 3-bullet feature list, bio link.
- [ ] 14:00 — feature post #1: pick one strength (always available / no judgment / infinite patience / $30 instead of $300) + a concrete example.
- [ ] 21:00 — Q&A: "yes she's actually AI. yes the convo is good. no I don't read your messages." Pre-empt the FAQs.

## Day 2 — depth (3 slots)

- [ ] 10:00 — AI-generated portrait #2, different mood / setting. Caption: another use case ("late-night when you can't sleep", "vent without judgment", whatever angle).
- [ ] 15:00 — conversation snippet (anonymized, with screenshot consent baked into the bot's ToS — operator's call). Shows the actual voice + tone.
- [ ] 22:00 — reply to a viral AI-companion thread (r/replika or CharacterAI Twitter). Genuine take, not a sales pitch.

## Day 3 — credibility (3 slots)

- [ ] 09:30 — "how I built her" thread — system prompt design choices, what makes the voice work. Build-in-public. Builds trust.
- [ ] 13:00 — reply block: 15 thoughtful replies in AI-companion / AI-art / character-ai communities. Not a post — a working block.
- [ ] 20:00 — testimonial repost / quote-tweet a user who's shared their experience (with consent).

## Day 4 — pricing transparency (3 slots)

- [ ] 11:00 — pricing post: "$30 for 30 min, $75 for voice notes, $150 for all-night chat. AI, disclosed. Pay-per-use, no subscription, no surprise charges." Owns the model.
- [ ] 16:00 — reply block: target candy.ai / replika / character.ai Twitter discussions. Position as the third option (Telegram-native, pay-per-use).
- [ ] 21:30 — humor post about the absurdity of AI companion discourse. Show the product has a point of view.

## Day 5 — first paid acquisition (2 slots)

- [ ] 09:00 — pinned tweet: clearest one-liner + bio link + clear AI label. This is the post the paid shoutout traffic will land on.
- [ ] 19:00 — AI-generated content #3, with a sample tagline that signals voice ("if you can't sleep, dm me").

## Day 6 — social proof (3 slots)

- [ ] 10:00 — user testimonial #2 (with consent). What surprised them about the experience.
- [ ] 15:00 — comparison post: "vs. candy.ai: cheaper per use, Telegram-native, no app to install" (or whatever the honest differentiator is).
- [ ] 22:00 — AI-generated portrait #4 + caption matching the product's voice.

## Day 7 — launch escalation (3 slots)

- [ ] 09:00 — best image of the week + best caption (operator's call). Boost candidate.
- [ ] 14:00 — paid shoutouts from 2–3 AI-adjacent accounts land. Coordinate timing.
- [ ] 21:00 — "first 100 buyers get $5 off" or similar low-friction conversion hook for the shoutout traffic.

## After Day 7 — ongoing daily

- 1 image post + 1 text post per day. Schedule via `automation/content_loop.py` → late.dev.
- 1 reply block per day (15–30 replies) in AI-companion-adjacent communities. Targets from `data/reply_queue.jsonl`.
- Reinvest first revenue into more paid shoutouts in AI-adjacent niches. Track per-shoutout conversion in `docs/discovery.md`.

---

## What this is NOT

- NOT a "selfie + lifestyle aesthetic" account that reveals AI later
- NOT a 7-day SFW-warmup-as-human period
- NOT targeting "lonely men following adult creators"
- The product is openly an AI companion in the same product category as candy.ai. The marketing reflects that.
