#!/usr/bin/env python3
"""Clean up duplicates, finish Page 09, build Pages 10-12 with proper rate limiting."""

import json
import time
import urllib.request
import urllib.error
from pathlib import Path

API = (Path.home() / ".config" / "craft" / "connect-url").read_text().strip()
AUTH = (Path.home() / ".config" / "craft" / "token").read_text().strip()
SLEEP_BETWEEN = 1.2  # seconds between API calls

def call(method, path, body=None, max_retries=4):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(max_retries):
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
            if e.code == 429 and attempt < max_retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  [rate-limited; waiting {wait}s]")
                time.sleep(wait)
                continue
            raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode()}")

# ============================================================
# STEP 1: Cleanup duplicates and test doc
# ============================================================
DUPLICATES_TO_DELETE = [
    "cd485673-1b8b-f248-45fd-bb89a25647d6",  # Test Collection Doc
    "146ae85a-7081-a903-2a92-8762ee9d08af",  # dupe Page 02
    "64d66867-fdb6-bb0c-15ed-fdb4733d4079",  # dupe Page 03
    "179dbd7a-3a44-b014-edaa-29039f1287db",  # dupe Page 04
    "e92249d8-9036-b9e2-f7cb-6e4b4c32b82c",  # dupe Page 05
    "f19352ed-cee5-8afd-e04c-7758920c72ed",  # dupe Page 06
    "da07fb61-90a8-f640-34ed-0b2b6b78b81d",  # dupe Page 07
    "9c3ade54-ce71-6a2b-e9d5-293f1ad3d298",  # dupe Page 08
    "47374407-0c49-89ca-705f-9326d3c9a3d9",  # dupe Page 09 (newer empty doc)
]

print("[Cleanup] Deleting duplicates + test doc...")
r = call("DELETE", "/documents", {"documentIds": DUPLICATES_TO_DELETE})
print(f"  Deleted: {len(r.get('items', []))} docs")

# ============================================================
# STEP 2: Finish Page 09 (existing doc id, needs collection+cards)
# ============================================================
PAGE_09_DOC_ID = "2261b5e7-dc0b-7e31-487f-e37c1f2fab40"
FOLDER_ID = "50527e79-f818-7a20-700f-d6d0596216ac"

KANBAN_CALLOUT = """<callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>"""

# Card data (lifted from the original; trimmed for brevity to fit one file)
# Page 09 - Twitter account creation
page09_cards = [
    {"title": "81 — Pick the persona's Twitter handle + display name", "body": "## What to do\n\nDecide on the persona's identity on Twitter. Document in 1Password under `LW-Persona Twitter identity`:\n\n- **Handle** (`@username`): short, memorable, matches Telegram bot username pattern. E.g., `@lily_xo` or `@itslilybabe`.\n- **Display name:** persona's stage name (e.g., `Lily 💋`)\n- **Niche:** which audience (alt / gym / Latina / etc.) — should match your earlier persona-niche pick\n\n### Handle availability check\n\nIn LatticeWorks Chrome profile (LOGGED OUT of any Twitter), go to https://x.com/[candidate_handle].\n\n- 404 page = available\n- Profile shown = taken; try variants\n\nAvoid:\n- Numbers in handle (`lily123`) — looks scammy/AI\n- Underscores at start/end (`_lily_`) — looks fake\n- Trying to match an existing real OnlyFans creator's vibe too closely (risk of trademark/impersonation claims)\n\n## Verification\n\nHandle picked, available, documented."},
    {"title": "82 — Sign up new Twitter account", "body": "## What to do\n\nIn LatticeWorks Chrome profile, go to https://x.com → **Sign Up**.\n\n- **Name:** persona's display name from Card 81\n- **Email:** `twitter@latticeworks.<TLD>` (works via Migadu catch-all)\n- **Date of birth:** persona's stated age — must be 18+. Pick a believable date (e.g., 22-30 range).\n- Click Next\n\nTwitter sends verification email — check Migadu inbox, click verify link.\n\n## Verification\n\nAccount created, email verified."},
    {"title": "83 — Phone verify with LW-Phone", "body": "## What to do\n\nTwitter will prompt for phone verification (sometimes immediately, sometimes after first post or first reply).\n\n- Use `LW-Phone` from Page 01 Card 6 (MySudo recommended — Twitter is increasingly rejecting Google Voice)\n- Enter the SMS code from MySudo\n\nIf Twitter rejects the number as VoIP:\n- Try a real burner SIM (e.g., $20 prepaid SIM from Mint Mobile, Visible, or similar)\n- Use the SIM in an old phone or via an eSIM in your existing iPhone (configure eSIM with a separate plan)\n\n## Verification\n\nPhone verified on Twitter."},
    {"title": "84 — Set the @handle and finalize username", "body": "## What to do\n\nIn Twitter → Profile → Edit Profile:\n- Set @handle from Card 81\n- Twitter sometimes auto-generates an ugly one — change it to your picked handle now\n\n## Verification\n\nProfile URL is `x.com/<your-picked-handle>`."},
    {"title": "85 — Set placeholder bio (NO NSFW yet, NO AI disclosure yet)", "body": "## What to do\n\nEdit Profile → Bio.\n\n**For the warmup phase (Page 10), the bio should be:**\n- Innocuous: hobby, vibe, location-ish hints\n- NO sexual language\n- NO links yet (no Telegram, no OnlyFans, no Throne)\n- NO `#AI` hashtag (that comes at Page 11 ACC enrollment)\n\nExample for an alt-niche persona:\n```\n22 · NYC · coffee + cat ppl · 🖤\n```\n\n**Why no AI disclosure yet?** Twitter ACC requirements only apply once you start posting NSFW. During SFW warmup, you're just an account. ACC disclosure comes at Page 11.\n\n## Verification\n\nBio set, vanilla, no NSFW signals."},
    {"title": "86 — Add placeholder profile pic and banner", "body": "## What to do\n\n- **Profile pic:** use a generic abstract image (sunset, texture, non-face avatar). NOT a final persona image — those come post-ACC.\n- **Banner:** similar — a generic vibey image.\n\nPlaceholders via:\n- Unsplash / Pexels stock photos\n- DALL-E for SFW landscapes via your Anthropic API\n- canva.com gradient\n\n## Why placeholders?\n\nTwitter algorithms flag profile changes during warmup as suspicious. Start with clearly-placeholder branding and update to real persona content AFTER ACC approval.\n\n## Verification\n\nProfile pic and banner set. Both SFW placeholders."},
    {"title": "87 — Enable 2FA on Twitter", "body": "## What to do\n\nSettings → Security and account access → Security → Two-factor authentication.\n\n- Choose **Authentication app** (NOT SMS — SMS 2FA is vulnerable to SIM swaps)\n- Use 1Password's TOTP feature: in `LW-Twitter account` item, add the OTP field by scanning Twitter's QR code\n\nSave backup codes Twitter provides in 1Password under `LW-Twitter account` → Secure Note.\n\n## Verification\n\nLogging out and back in requires 1Password TOTP. Backup codes saved."},
    {"title": "88 — Configure email + notifications", "body": "## What to do\n\nSettings → Notifications:\n- Email notifications: ON (security alerts reach `me@latticeworks.<TLD>` via Migadu)\n- Push notifications: OFF (no phone buzzes for every like during automation)\n\nSettings → Privacy and Safety:\n- Protected mode: OFF (persona must be discoverable)\n- DM settings: Allow message requests from everyone (the inbox the bot will work)\n\n## Verification\n\nSettings configured for autonomous operation."},
    {"title": "89 — DO NOT post anything yet", "body": "## What to do\n\nResist the urge.\n\nFor the next 7-14 days (Page 10's warmup), the account looks slightly suspicious to Twitter:\n- New account\n- New IP (Hostwinds server, if you ever log in from there)\n- New phone\n\nPost NSFW in the first 24-48 hours → Twitter's automated systems shadowban or suspend. Patience pays exponentially.\n\n## What you CAN do today\n\n- Follow 5-10 accounts in your niche (max 5-10 in first 24 hours)\n- 'Like' a few of their tweets\n- That's it. No tweets, no replies, no DMs sent.\n\n## Verification\n\nAccount exists. Zero original tweets. Following ~5-10 niche accounts."},
    {"title": "90 — Final check before Page 10 (Twitter warmup)", "body": "## Confirm\n\n- [ ] Twitter handle + display name picked + documented in 1Password\n- [ ] Account created with `twitter@latticeworks.<TLD>` email\n- [ ] Phone verified via LW-Phone\n- [ ] Placeholder bio (SFW, no NSFW signals, no AI disclosure yet)\n- [ ] Placeholder profile pic and banner (generic)\n- [ ] 2FA enabled with authenticator app, backup codes in 1Password\n- [ ] Email notifications ON to `me@latticeworks.<TLD>`\n- [ ] DMs open to message requests\n- [ ] Zero tweets posted. Following 5-10 niche accounts MAX.\n\n## All 9 boxes checked?\n\nDrag to Done. Open **Page 10 — Twitter warmup (7-14 days)**."},
]

# Page 10 - Twitter warmup
page10_cards = [
    {"title": "91 — Days 1-2: Set the lifestyle baseline", "body": "## What to do\n\nYou're inhabiting the persona. Twitter wants to see a HUMAN, not a bot.\n\n**Day 1:**\n- Post 1 SFW tweet (e.g., `coffee or no work today ☕`)\n- Like 5-10 tweets from accounts you followed in Page 09 Card 89\n- DO NOT reply to anyone yet\n\n**Day 2:**\n- Post 1-2 SFW tweets\n- Like 10-15 tweets\n- Reply to ONE tweet (low-effort: 'lol' or 'saame')\n\n## Why this pacing\n\nNew accounts that immediately spam get flagged. Real humans post sporadically and engage casually as they 'find their voice'.\n\n## Verification\n\nDay 1-2: 1-2 tweets, casual likes, 1 reply. No NSFW. No automation."},
    {"title": "92 — Days 3-5: Grow engagement signal", "body": "## What to do\n\n**Day 3-5:**\n- 2-3 SFW tweets per day\n- Reply to 3-5 tweets per day (real, substantive replies — 'your cat is gorgeous omg' not '🔥🔥🔥')\n- Follow 5-10 more niche accounts per day\n- Quote-tweet 1 tweet per day with a real opinion\n\n## SFW content ideas\n\n- Outfit posts (clothed, vibe descriptors)\n- Aesthetic photos (room, coffee shop, sunset)\n- Hot-take tweets (e.g., for alt-niche: `tattoos > piercings dont @ me`)\n- Engagement bait (e.g., `last person you dmd, post their pfp`)\n\n## Anti-pattern\n\nDon't post a selfie yet. Hold for Day 6+.\n\n## Verification\n\nBy end of Day 5: ~10-15 tweets, ~20-30 replies, ~50-100 likes, following ~30-50 accounts."},
    {"title": "93 — Day 6: First selfie", "body": "## What to do\n\nDay 6: post a first persona 'selfie' that should be:\n- SFW, from your persona's reference library (image set you'll train IPAdapter on)\n- Slightly imperfect (a tiny blur, off-center crop, 'candid' feel) — looks real, not AI-perfect\n- Innocuous caption (`finally a no-makeup day`, `cant sleep`)\n\n## Why Day 6\n\nLong enough that account feels established (8-12 tweets of personality). Short enough audience still curious.\n\n## Verification\n\nFirst selfie posted. Caption casual. SFW."},
    {"title": "94 — Days 7-10: Ramp posting cadence", "body": "## What to do\n\n**Day 7-10:**\n- 3-4 SFW tweets per day\n- 5-8 replies per day\n- 1 additional SFW selfie per day (variety of poses, settings — all SFW)\n- Start using niche hashtags on 30-50% of posts\n\n## Hashtag strategy\n\nGoal: discoverability without spamminess.\n- 2-3 niche tags per tweet, NOT 10+\n- Mix specific tags with broader (e.g., `#altgirl` + `#nyc`)\n- Don't use `#nsfw` or explicit-signal tags yet — that's post-ACC\n\n## Verification\n\nDays 7-10: 12-16 more tweets. Engagement starting to compound."},
    {"title": "95 — Day 10: Audit account health", "body": "## What to do\n\nCheck for shadowban / restriction signals:\n\n### Visibility test\n- Search Twitter for one of your tweets exactly — does it appear?\n- Yes: good. No after 24 hrs: possible shadowban.\n\n### Impressions test\n- Tweets should get 50-300+ impressions each (Twitter analytics)\n- Flat-lining at 0-20: possible shadowban\n\n### DM test\n- Send yourself a test DM from a separate real Twitter account\n- Does it land in inbox or message requests?\n- Neither: possible DM restriction\n\n### Algorithmic surface test\n- Search a niche keyword you'd want to be found for\n- Scroll 'People' tab — do you appear?\n- Never after 30 min scroll: not in algo graph yet\n\n## If shadowbanned\n\nDon't panic. Common for new accounts:\n- Stop posting 24-48 hours\n- Reduce reply frequency\n- Wait 3-7 days, recheck\n\n## Verification\n\nAudit results documented in 1Password under `LW-Twitter warmup audit Day 10`."},
    {"title": "96 — Days 11-14: Higher engagement", "body": "## What to do\n\nFinal warmup days.\n\n**Day 11-14:**\n- 4-5 SFW tweets per day\n- 10-15 replies per day, including replies to bigger accounts (10K+ followers)\n- 1-2 selfies per day, more curated\n- Begin liking adult-creator accounts (NOT NSFW posts yet — their SFW posts only)\n\n## Why 'begin liking adult-creator accounts'\n\nTwitter's recommendation engine looks at WHO you engage with. Liking adult creators' SFW posts signals 'this account is interested in this niche' — improves visibility to that audience LATER once you post NSFW.\n\n## Anti-pattern\n\nDon't follow 100 NSFW accounts in one sitting. 5-10 per day. Looking organic matters.\n\n## Verification\n\nDays 11-14: 16-20 more tweets, 40-60 replies, organic engagement growth."},
    {"title": "97 — Day 13-14: Build out the link-tree", "body": "## What to do\n\nBefore ACC enrollment in Page 11, need a 'link in bio' landing page.\n\n### Option A — Custom one-page site (recommended)\n- Subdomain on your domain: `links.latticeworks.<TLD>` — on Hostwinds box\n- Simple HTML: persona pic, 3-4 buttons (Telegram, Throne wishlist, NowPayments tip link)\n- AI disclosure at bottom\n\n### Option B — Bento.me\n- Free, no setup\n- Risk: Bento can ban adult creators\n\n### Option C — Linktree\n- DON'T USE. Linktree explicitly bans adult content.\n\n**Recommendation: Option A.** Spin a basic page on Hostwinds box (Nginx + static index.html).\n\nSave the URL in 1Password under `LW-Persona link in bio`.\n\n## Verification\n\nLink-in-bio URL ready to drop into Twitter bio at ACC enrollment (Page 11)."},
    {"title": "98 — Day 14: Verify ACC eligibility", "body": "## What to do\n\nConfirm Twitter ACC eligibility:\n\n- [ ] Account is at least 14 days old\n- [ ] No suspensions or violations in account history\n- [ ] Active engagement (14 days of organic content)\n- [ ] Phone verified (Page 09 Card 83)\n- [ ] Email verified (Page 09 Card 82)\n- [ ] You can provide government-issued ID for KYC\n- [ ] You can provide tax documents (W-9 if 1099, or LLC docs)\n\nIf any missing, fix before Page 11.\n\n## Verification\n\nAll 7 boxes checked. Eligible to apply for ACC."},
    {"title": "99 — Document warmup observations", "body": "## What to do\n\nCapture warmup phase lessons. In 1Password under `LW-Twitter warmup observations`:\n\n- Which post types got most engagement?\n- Which hashtags drove most discovery?\n- Followers per day rate?\n- Restriction signals + how you handled them?\n\n## Why this matters\n\nWhen scaling to multiple personas later, warmup learnings from persona #1 are gold. Document while fresh.\n\n## Verification\n\nNotes captured in 1Password."},
    {"title": "100 — Final check before Page 11 (ACC enrollment)", "body": "## Confirm\n\n- [ ] Account has 14 days of SFW activity\n- [ ] No shadowban / restriction signals\n- [ ] Phone + email verified, 2FA enabled\n- [ ] Link-in-bio URL ready (on your domain, not Linktree)\n- [ ] Government ID + tax documents ready for KYC\n- [ ] Real photo of operator (yourself) holding ID for ACC verification\n- [ ] Warmup observations documented in 1Password\n\n## All 7 boxes checked?\n\nDrag to Done. Open **Page 11 — Twitter ACC enrollment**."},
]

# Page 11 - Twitter ACC enrollment
page11_cards = [
    {"title": "101 — Open the ACC application in Twitter settings", "body": "## What to do\n\nIn LatticeWorks Chrome profile, log into persona's Twitter.\n\nNavigate to: Settings → Monetization → look for **Adult Content Creator**.\n\nIf you can't find it:\n- ACC is sometimes invite-only / regional rollout\n- Apply via public form: https://help.x.com/en/forms/account-access/regain-access/adult-content-creator-application\n\n## Verification\n\nACC application form open in browser."},
    {"title": "102 — Submit identity verification (YOUR ID)", "body": "## What to do\n\nACC requires VERIFIED IDENTITY of the operator. Your real ID, not the persona's.\n\nUpload:\n- **Government-issued photo ID** (US driver's license, passport, state ID)\n- **Selfie holding the ID** (Twitter prompts with overlay guides)\n\nMake sure:\n- ID clear, all corners visible\n- Selfie shows your face + ID readable\n- Good lighting\n\n## Why your real ID\n\nACC is the platform's KYC for adult creators. They need a real human accountable. Your real identity is on the BACK END (creator records). FRONT END (persona profile) stays anonymous — followers see persona's stage name only.\n\n## Verification\n\nID + selfie submitted. ACC dashboard shows `Pending`."},
    {"title": "103 — Submit tax documents", "body": "## What to do\n\nPer Page 01 Card 7 decision:\n\n### Option A (UpfrontOps LLC):\n- W-9 with UpfrontOps LLC name + EIN\n- LLC formation document\n\n### Option B (new LLC):\n- W-9 with new LLC name + EIN\n- LLC formation document\n- Best if you formed the LLC during Pages 02-10 in parallel\n\n### Option C (1099 personal):\n- W-9 with your personal name + SSN\n- Ties adult-creator income directly to your personal name on Twitter records\n\nUpload via ACC application.\n\n## Why now\n\nWithout tax docs, Twitter can't pay you for ACC revenue. They require before approval.\n\n## Verification\n\nTax docs uploaded."},
    {"title": "104 — Set content sensitivity tier", "body": "## What to do\n\nACC tiers:\n- **Adult** — nudity, suggestive content, sexual themes (less restrictive)\n- **Explicit** — actual sexual acts, hardcore (most restrictive labeling)\n\nFor synthetic AI persona, tip+custom model:\n- Most content fits **Adult**\n- Reserve Explicit for hardcore customs (Page 12)\n\nPick Adult for now. Request Explicit later.\n\n## Verification\n\nSensitivity tier set to Adult."},
    {"title": "105 — Update bio with AI disclosure (per ACC policy)", "body": "## What to do\n\nACC requires clear AI disclosure for AI personas.\n\nUpdate Twitter bio (Profile → Edit Profile → Bio):\n\n**Format that complies with ACC but preserves fiction:**\n\nExample alt-niche:\n```\n22 · NYC · alt baddie · AI 💋 still treat me like the real thing tho · 🔗 [link-in-bio URL]\n```\n\n**Required:**\n- Word 'AI' visible in bio (not in collapsed section)\n- `#AI` hashtag pattern in posts (Card 107)\n\n**Optional:** link in bio (Page 10 Card 97).\n\n## Verification\n\nBio updated, AI disclosure present, link active."},
    {"title": "106 — Configure profile for adult content", "body": "## What to do\n\nSettings → Privacy and Safety → Your posts:\n- **Sensitivity Settings:** Mark media as containing sensitive content (default ON for all posts)\n\nSettings → Privacy and Safety → Discoverability:\n- **Discoverable by phone:** OFF (don't let LW-Phone unmask)\n- **Discoverable by email:** OFF (don't let Migadu address leak)\n\nSettings → Privacy and Safety → Audience and tagging:\n- **Protect your posts:** OFF (want public discoverability)\n- **Photo tagging:** Off or Only people I follow\n\n## Verification\n\nSettings configured."},
    {"title": "107 — Set up posting templates with required hashtags", "body": "## What to do\n\nACC requires AI-generated content tagged. The pattern (as of 2026):\n- Every NSFW post: `#AI` or `#Generated` hashtag\n- Caption mentions 'AI' once at start of more explicit content\n\nDocument standard templates in 1Password under `LW-Posting templates`:\n\n**Template A — selfie / softcore:**\n```\n[caption text]\n\n#alt #nyc #AI\n```\n\n**Template B — explicit / hardcore (once Explicit tier approved):**\n```\n[caption text] — AI persona ✨\n\n#AI #Generated\n```\n\nUse in bot's posting logic later.\n\n## Verification\n\nTemplates documented for future bot use."},
    {"title": "108 — Submit application + wait for review", "body": "## What to do\n\nIn ACC dashboard, click **Submit**.\n\nReview timeline:\n- Typical: 24-72 hours\n- Sometimes: 5-7 days during high-volume\n- Rarely: over 2 weeks (email Twitter support)\n\nWhile waiting:\n- DO NOT post NSFW\n- DO continue SFW posting at warmup pace (3-5 posts/day) to keep account 'alive'\n- DO NOT switch to bot automation yet\n\n## Verification\n\nApplication submitted. Status `Under review`."},
    {"title": "109 — On approval: enable monetization features", "body": "## What to do\n\nWhen approval email arrives at `me@latticeworks.<TLD>`:\n\nIn Twitter Monetization settings:\n- Enable Creator Subscriptions (if you want subscription tier — most LatticeWorks personas skip, doing tips + customs)\n- Enable Tips (Twitter's native tip feature)\n- Verify Adult-tier posting capabilities active\n\nUpdate bio once more to reflect monetization (NowPayments tip link + Telegram bot link).\n\n## What to NOT enable\n\n- Twitter 'Verified' (blue check) — don't need for ACC, adds friction\n- Twitter Ads — irrelevant\n\n## Verification\n\nACC monetization enabled. Bio reflects active operation."},
    {"title": "110 — Final check before Page 12 (voice + smoke test)", "body": "## Confirm\n\n- [ ] ACC application submitted and approved\n- [ ] Identity verified (real ID + selfie)\n- [ ] Tax docs submitted matching tax structure decision\n- [ ] Sensitivity tier set to Adult\n- [ ] AI disclosure in bio\n- [ ] Adult content sensitivity setting ON\n- [ ] Posting templates documented for future bot use\n- [ ] Monetization features (tips, etc.) enabled\n\n## All 8 boxes checked?\n\nDrag to Done. Open **Page 12 — Voice + final smoke test**."},
]

# Page 12 - Voice + smoke test
page12_cards = [
    {"title": "111 — Sign up ElevenLabs Creator tier", "body": "## What to do\n\nIn LatticeWorks Chrome profile, go to https://elevenlabs.io.\n\n- Sign Up with `eleven@latticeworks.<TLD>`\n- Choose **Creator plan** ($22/mo) — unlocks Professional Voice Cloning\n- Save login to `LW-ElevenLabs account` in 1Password\n\n## Why Creator (not Starter)\n\n- Starter ($5/mo): only Instant Voice Clone (lower quality, won't match persona consistency)\n- Creator ($22/mo): Professional Voice Clone (trained on 30+ sec, much higher fidelity)\n\nFor a 'feels real' persona experience, Creator is the floor.\n\n## Verification\n\nAccount active on Creator tier."},
    {"title": "112 — Pay with Privacy.com card", "body": "## What to do\n\nCreate Privacy.com card: `LW-ElevenLabs`, lock to `elevenlabs.io`, $50/mo limit.\n\nSave to `LW-ElevenLabs virtual card` in 1Password.\n\nPay $22/mo with this card.\n\n## Verification\n\nSubscription active."},
    {"title": "113 — Source reference audio for voice clone", "body": "## What to do\n\nProfessional Voice Cloning needs 30+ sec (ideally 1-2 min) of clean reference audio.\n\n**Sources for persona's voice:**\n\n### Option A — Generate via TTS (zero-shot)\n- Use OpenAI's TTS API or similar to generate ~60 sec clean speech in a voice you like\n- Save as `.mp3` / `.wav`\n- Reference for ElevenLabs\n\n### Option B — Record a voice actor\n- Hire on Fiverr (~$30-80) for 1-2 min read-out clean audio\n- Get rights to use as AI voice reference (specify in contract)\n\n### Option C — Sample from public domain / royalty-free\n- CC0 / royalty-free podcast audio\n- More complex for 'consistent persona voice'\n\n**Recommendation: Option B.** Voice actors give unique, ownable voice with proper rights. ~$50 well spent.\n\n## Verification\n\n30+ sec audio file ready to upload to ElevenLabs."},
    {"title": "114 — Train the persona's voice clone in ElevenLabs", "body": "## What to do\n\nIn ElevenLabs → Voices → Add Voice → **Professional Voice Clone**.\n\n- **Name:** persona's stage name (e.g., `Lily`)\n- **Description:** 'AI persona voice for LatticeWorks'\n- Upload reference audio from Card 113\n- Click Create\n\nTraining: 2-5 minutes.\n\n## Verification\n\nVoice clone in your Voices list. Generate a test phrase to confirm."},
    {"title": "115 — Test voice quality", "body": "## What to do\n\nElevenLabs → Voices → click persona's voice → Generate.\n\nTest phrases (3-5):\n- 'Hi babe, just thinking about you 💋'\n- 'want to see what i'm doing right now?'\n- 'tip me $30 and i'll send you something special'\n\nListen on headphones. Check:\n- Matches persona's 'feel' (age, accent, vibe)?\n- Robotic / glitchy moments?\n- Pacing natural?\n\nIf off:\n- Re-upload with cleaner reference\n- Adjust stability + similarity settings\n\n## Verification\n\nVoice sounds natural, matches persona vibe."},
    {"title": "116 — Get ElevenLabs API key", "body": "## What to do\n\nElevenLabs → Profile → API Key.\n\nCopy the key (long string starting `sk_...`).\n\nSave in 1Password as `LW-ElevenLabs API key`.\n\nTest from Hostwinds server:\n\n```\nLW_EL_KEY=\"your_key\"\nLW_VOICE_ID=\"your_voice_id\"\n\ncurl --request POST \\\\\n  --url \"https://api.elevenlabs.io/v1/text-to-speech/${LW_VOICE_ID}\" \\\\\n  --header \"xi-api-key: ${LW_EL_KEY}\" \\\\\n  --header \"Content-Type: application/json\" \\\\\n  --data '{\"text\":\"hey baby\",\"model_id\":\"eleven_multilingual_v2\"}' \\\\\n  --output /tmp/test.mp3\n\n# Play it\nafplay /tmp/test.mp3\n```\n\n## Verification\n\nAPI call returns audio. Plays cleanly."},
    {"title": "117 — Full pipeline smoke test: Twitter → Telegram → payment", "body": "## What to do\n\nEnd-to-end smoke test simulating a real customer journey.\n\n### Step 1 — Twitter side\nFrom operator account (or friend's), DM persona's Twitter: `hi cutie`\n\n### Step 2 — Telegram bridge (manual for now; bot will automate)\nFrom persona's Twitter, reply: `hey 💋 come find me on telegram, that's where i play → [bot deep-link]`\n\nDeep-link format: `https://t.me/[your_bot_username]?start=test_user_001`\n\n### Step 3 — Telegram conversation\n'Customer' (you) clicks link → opens Telegram → starts the bot.\n- Bot doesn't reply yet (no code yet)\n- Chat established\n\n### Step 4 — Manually issue Stars invoice\nFrom Hostwinds server, send Stars invoice to customer chat (curl from Page 08 Card 78).\n\n### Step 5 — Customer pays\nYou click 'Pay 1 Star' → enter PIN → confirm\n\n### Step 6 — Confirm receipt\nIn bot owner view, Stars balance increments by 1.\n\n## Verification\n\nEnd-to-end customer journey works manually. Plumbing proven."},
    {"title": "118 — Final pipeline smoke test: content generation", "body": "## What to do\n\nFinal smoke test of CONTENT path.\n\n### Step 1 — Generate one image (RunPod)\nSSH into Hostwinds. Start ComfyUI pod on RunPod with Flux + AIDMA NSFW Unlock LoRA.\n\n(Detailed ComfyUI setup in build phase 2 — for smoke test just verify a pod with Flux starts and generates one test image.)\n\n### Step 2 — Upload to B2\n```\nb2 file upload lw-content-prod /tmp/test.png test/smoke.png\n```\n\n### Step 3 — Serve via Bunny\nOpen `https://lw-content.b-cdn.net/test/smoke.png` — image renders.\n\n### Step 4 — Send via Telegram\n```\ncurl \"https://api.telegram.org/bot${LW_BOT_TOKEN}/sendPhoto\" \\\\\n  -d \"chat_id=${LW_CHAT_ID}\" \\\\\n  -d \"photo=https://lw-content.b-cdn.net/test/smoke.png\"\n```\n\nImage arrives in Telegram chat.\n\n## Verification\n\nFull content path works end-to-end: generate → store → CDN → deliver."},
    {"title": "119 — Backup audit + 1Password export rehearsal", "body": "## What to do\n\nVerify handoff mechanism works.\n\n### Export 1Password vault test\n- 1Password → LatticeWorks vault → `...` → Export → 1Password Unencrypted Format (1pux) or CSV\n- Save to Mac temporarily as `latticeworks-vault-test-export.1pux`\n- Open (with 1Password import tool) into TEST vault to verify export integrity\n- Delete test export and test vault immediately\n\n### Verify backups of seed phrase locations\n- Confirm hardware-wallet seed phrase (Page 07 Card 63) in BOTH physical locations\n- Confirm 1Password split-saved seeds (words 1-6, 7-12) intact\n\n### Document handoff process\nIn 1Password under `LW-Handoff playbook`:\n- 'To hand off to client: export this vault as 1pux → send via Signal or secure file transfer → recipient imports.'\n- 'Then change all credentials' (passwords, API keys) AFTER handoff, so old exports become useless.\n\n## Verification\n\nVault export works. Backup integrity confirmed."},
    {"title": "120 — Setup complete. You're ready to build.", "body": "## Final checklist\n\n- [ ] All previous 119 microsteps complete\n- [ ] Every vendor account active, credentials in 1Password\n- [ ] Domain + email working\n- [ ] Server provisioned + hardened\n- [ ] All APIs (Claude, OpenRouter, ElevenLabs, etc.) tested with smoke tests\n- [ ] NowPayments + crypto wallet tested with $1 transaction\n- [ ] Telegram bot created + responding to API calls\n- [ ] Twitter persona warmed (14 days SFW) + ACC enrolled and approved\n- [ ] Voice clone trained + voice quality verified\n- [ ] End-to-end pipeline smoke tested: Twitter → Telegram → payment\n- [ ] End-to-end content pipeline smoke tested: gen → B2 → Bunny → Telegram\n- [ ] 1Password export rehearsed (handoff mechanism verified)\n\n## What's next (outside this setup playbook)\n\nThis page completes the **setup phase** — every account and account-to-account pipe exists, smoke-tested.\n\n**Build phase** is separate:\n- Wire orchestration code (Claude API as brain)\n- Build conversational layer (OpenRouter for explicit chat)\n- Build content generation pipeline (ComfyUI on RunPod)\n- Build Twitter posting + reply-guy bot\n- Build Telegram chat handler with memory + customer profiling\n- Build shoutout management module\n- Wire detection-evasion post-processing\n- Wire payment-handling + custom-request flow\n\n~9-13 weeks of engineering, separate from this playbook.\n\n## All boxes checked?\n\nDrag this card to Done. LatticeWorks setup complete.\n\nWelcome to the build phase. 🎯"},
]


def build_kanban_in_doc(num, doc_id, cards, start_step):
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
    print(f"[OK] Page {num:02d}: {len(item_ids)} cards in kanban {coll_id[:8]}")
    return coll_id


def build_full_page(num, title, intro, cards, start_step):
    r = call("POST", "/documents", {
        "documents": [{"title": f"Page {num:02d} — {title}"}],
        "destination": {"folderId": FOLDER_ID},
    })
    doc_id = r["items"][0]["id"]
    print(f"[OK] Page {num:02d} doc created: {doc_id[:8]}")
    full_intro = f"# Page {num:02d} — {title}\n\n{KANBAN_CALLOUT}\n\n{intro}"
    call("POST", "/blocks", {
        "markdown": full_intro,
        "position": {"position": "end", "pageId": doc_id},
    })
    coll_id = build_kanban_in_doc(num, doc_id, cards, start_step)
    return {"doc_id": doc_id, "collection_id": coll_id}


# Resume Page 09
print("--- Finishing Page 09 ---")
coll09 = build_kanban_in_doc(9, PAGE_09_DOC_ID, page09_cards, 81)

# Build Pages 10, 11, 12
print("--- Building Page 10 ---")
page10 = build_full_page(
    10, "Twitter warmup (7-14 days)",
    "**Goal:** Age the new Twitter account with 14 days of SFW activity before ACC enrollment. This page spans ~2 weeks — daily small actions, not one sitting.",
    page10_cards, 91,
)

print("--- Building Page 11 ---")
page11 = build_full_page(
    11, "Twitter ACC enrollment",
    "**Goal:** Apply to and get approved for Twitter's Adult Content Creator program. Includes 1-7 day review. Requires Page 10 complete (14-day warmup).",
    page11_cards, 101,
)

print("--- Building Page 12 ---")
page12 = build_full_page(
    12, "Voice + final smoke test",
    "**Goal:** Train the persona's voice clone in ElevenLabs and verify all end-to-end pipelines. ~2 hours + voice training time. Requires all prior pages complete.",
    page12_cards, 111,
)

# Save IDs
IDS_FILE = Path.home() / ".config" / "craft" / "latticeworks-ids.json"
ids = json.loads(IDS_FILE.read_text())
ids["pages"]["page_02"] = {"doc_id": "d7aa9d6a-7fb2-aad1-6ffb-36fc80eb1aef"}
ids["pages"]["page_03"] = {"doc_id": "da4d46c7-ee25-e5d0-0226-3cbcee320eb5"}
ids["pages"]["page_04"] = {"doc_id": "b8b8785d-443b-e58b-a547-2090a64a33ca"}
ids["pages"]["page_05"] = {"doc_id": "02297da2-f2e8-9404-2c28-63098264278c"}
ids["pages"]["page_06"] = {"doc_id": "e87ecf08-1b77-5d85-9d96-e4cf5d19874b"}
ids["pages"]["page_07"] = {"doc_id": "b3d122eb-9864-4855-5d0d-cf0331c76926"}
ids["pages"]["page_08"] = {"doc_id": "397ada36-43cf-9a26-b423-08e3b91ca3d7"}
ids["pages"]["page_09"] = {"doc_id": PAGE_09_DOC_ID, "collection_id": coll09}
ids["pages"]["page_10"] = page10
ids["pages"]["page_11"] = page11
ids["pages"]["page_12"] = page12
IDS_FILE.write_text(json.dumps(ids, indent=2))

print()
print("=" * 60)
print("ALL 12 PAGES COMPLETE")
print("=" * 60)
