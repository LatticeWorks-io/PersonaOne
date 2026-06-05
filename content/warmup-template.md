# Warmup content — 7-day compressed schedule

> 22 slots covering day 1 through day 7, mapped to Page 10's compressed warmup. Pre-stage these BEFORE day 1 so warmup is drag-and-drop, not write-as-you-go. Schedule via late.dev (see `automation/late_client.py`) or post manually.

## Operating rules during warmup

- **NO NSFW.** Period. Bio is SFW. Posts are SFW. Tags are SFW. ACC happens later if at all.
- **NO bio link to Telegram yet** until day 5 — Twitter penalises new accounts pointing offsite immediately.
- **DO reply daily** to 10–20 large accounts in your aesthetic neighbourhood. This is where the algorithm learns who you are and where your first followers come from. (See `docs/discovery.md` for the reply-guy playbook.)
- **DO take a selfie on day 6.** Phone, natural light, real face on the operator. Builds non-bot signal.

---

## Day 1 — set the lifestyle baseline (3 slots)

- [ ] 09:00 — soft-launch post. Image + 1-line caption matching the persona's aesthetic. No call to action, no link. Just vibe.
- [ ] 14:00 — reply to 1 large account (50k+ followers) in the persona's niche with something genuine and quote-worthy.
- [ ] 21:00 — late-night text post (no image). 1–2 lines that hint at the persona's voice.

## Day 2 — voice + visual rhythm (3 slots)

- [ ] 10:00 — image post #2, different angle / setting / mood from Day 1's. Caption should sound like the same person.
- [ ] 15:00 — short opinion post. Something mildly contrarian about the persona's niche. Invites replies.
- [ ] 22:00 — quote-retweet a viral post in-niche, with a 1-line take.

## Day 3 — grow engagement signal (3 slots)

- [ ] 09:30 — text post phrased as a question to the audience. Invites comments.
- [ ] 13:00 — reply-guy block: 15 thoughtful replies to large in-niche accounts. (Not a post — a working block.)
- [ ] 20:00 — image post. Caption: a tiny vulnerable detail. Builds parasocial signal.

## Day 4 — first identifiable hook (2 slots + 1 working block)

- [ ] 11:00 — image post. Start of a recurring visual hook — same caption format you'll reuse weekly (e.g. "weekend mood:", "currently:", whatever lands).
- [ ] 16:00 — reply-guy block: 15 replies, target slightly smaller accounts (10k–50k) so your replies sit higher in their thread.
- [ ] 21:30 — text post: a one-line truth that lands. No image.

## Day 5 — bio link goes live (2 slots)

- [ ] 09:00 — UPDATE BIO: add the link to your domain landing page (which routes to Telegram). Tweet "fixed the link in bio :)"
- [ ] 19:00 — image post. Caption should match where you're sending people (curiosity hook, not a sales pitch).

## Day 6 — first selfie + DM-friendly signal (3 slots)

- [ ] 10:00 — selfie. Phone, natural light, on the operator. Crucial non-bot signal.
- [ ] 15:00 — text post that invites DMs in a non-thirsty way. Something like "my dm's are unhinged this week, ask me anything."
- [ ] 22:00 — image post matching the selfie's energy.

## Day 7 — launch eve (3 slots + paid shoutouts land)

- [ ] 09:00 — image post: best one of the week. Caption hooks at what's "coming" without specifying.
- [ ] 14:00 — paid shoutouts from 2–3 aged accounts land in this window (see `docs/discovery.md`).
- [ ] 21:00 — explicit "DM me on Telegram" post timed to ride the shoutout traffic.

## After Day 7 — daily ongoing

- 1 image post + 1 text post per day, scheduled via late.dev.
- 1 reply-guy block per day (15–30 replies in 30 min).
- Reinvest first revenue into more paid shoutouts; track conversion in `discovery.md`.

---

## What to write into each slot

Each slot is a placeholder until the operator (or a Claude pass) fills it in. The persona's `system_prompt` should be able to generate a draft for any of these — pass the slot's intent + the persona file, get a draft. Iterate before scheduling.
