#!/usr/bin/env python3
"""Build LatticeWorks folder + Start Here + Page 01 demo in Craft."""

import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE = Path.home() / ".config" / "craft" / "connect-url"
TOKEN = Path.home() / ".config" / "craft" / "token"

API = BASE.read_text().strip()
AUTH = TOKEN.read_text().strip()

def call(method, path, body=None):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {AUTH}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "curl/8.5.0")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_resp = e.read().decode()
        raise RuntimeError(f"{method} {path} -> {e.code}: {body_resp}")

# ---------- 1. Create LatticeWorks folder ----------
r = call("POST", "/folders", {"folders": [{"name": "LatticeWorks"}]})
folder_id = r["items"][0]["id"]
print(f"[OK] Folder created: id={folder_id}")

# ---------- 2. Create Start Here doc ----------
r = call("POST", "/documents", {
    "documents": [{"title": "Start Here — LatticeWorks Setup"}],
    "destination": {"folderId": folder_id},
})
start_doc_id = r["items"][0]["id"]
print(f"[OK] Start Here doc: id={start_doc_id}")

# ---------- 3. Fill Start Here doc ----------
start_md = """# LatticeWorks Setup

Welcome. This is the build playbook for the LatticeWorks project. You work through it linearly — page by page, microstep by microstep — and you do not move to the next page until every card on the current page is in the Done column.

## How to use this

1. Each page below is a Craft document containing **one kanban collection**.
2. Each card on the kanban is **one microstep**, with the prose, links, and sub-instructions baked into the card itself. Click into a card to read it.
3. When you start a card, drag it from **Todo → In Progress**.
4. When you finish, drag it to **Done**.
5. When the entire page's cards are in Done, open the next page.
6. If a card depends on a previous one being complete, the prose says so.

## First time on each page

Open the page, then click the kanban collection block → "..." menu → **View** → **Kanban**. Craft defaults to list view; switching to kanban once per page makes the drag-to-Done workflow work as intended.

## Setup pages (work in order)

- **Page 01 — Set up isolated workspace** (~30 min)
- Page 02 — Register your domain (next, not yet built)
- Page 03 — Email at Migadu + DNS (next, not yet built)
- ... (Pages 04-12 will be built once Page 01 is validated)

## What lives outside this playbook

- Architecture / system design — discussed separately with Claude.
- Cost expectations — separately tracked.
- Operating procedures — built once the bot is running.

This doc is the build runbook. Once setup is complete, you may never open it again."""

call("POST", "/blocks", {
    "markdown": start_md,
    "position": {"position": "end", "pageId": start_doc_id},
})
print(f"[OK] Start Here doc populated")

# ---------- 4. Create Page 01 doc ----------
r = call("POST", "/documents", {
    "documents": [{"title": "Page 01 — Set up isolated workspace"}],
    "destination": {"folderId": folder_id},
})
page01_id = r["items"][0]["id"]
print(f"[OK] Page 01 doc: id={page01_id}")

# ---------- 5. Fill Page 01 intro ----------
page01_intro = """# Page 01 — Set up isolated workspace

**Goal:** Create a clean dev surface for the LatticeWorks project, fully isolated from your UpfrontOps / personal stack.

**Time:** ~30 minutes.

**Why this page exists:** You can't sign up for vendors without virtual cards, a clean browser, a fresh email anchor, and a phone number that doesn't trace back to UpfrontOps. This page sets all of that up.

**You can't open Page 02 until every card below is in Done.**

---

Switch the kanban below to **Board view** (collection's `...` menu → View → Kanban). Then work the cards left-to-right."""

call("POST", "/blocks", {
    "markdown": page01_intro,
    "position": {"position": "end", "pageId": page01_id},
})
print(f"[OK] Page 01 intro populated")

# ---------- 6. Create kanban collection inside Page 01 ----------
r = call("POST", "/collections", {
    "schema": {
        "name": "Page 01 Microsteps",
        "properties": [
            {
                "type": "singleSelect",
                "name": "Status",
                "options": [
                    {"name": "Todo", "color": "gray"},
                    {"name": "In Progress", "color": "sky-blue"},
                    {"name": "Done", "color": "mint-green"},
                ],
            },
            {"type": "number", "name": "Step"},
        ],
    },
    "position": {"position": "end", "pageId": page01_id},
})
coll_id = r["collectionBlockId"]
print(f"[OK] Kanban collection: id={coll_id}")

# ---------- 7. Add 10 cards as items, batched ----------
cards = [
    {
        "title": "1 — Create LatticeWorks Chrome profile (Mac)",
        "step": 1,
        "body": """## What to do

Open Chrome on your Mac → click the **profile circle** (top right) → **Add** → create a new profile named exactly `LatticeWorks`.

- Pick a **distinct dark color/icon** so you can tell at a glance which profile you're in (avoid colors you already use for personal / UpfrontOps).
- **SKIP** "Sign in to sync" — leave this profile signed out of Google entirely.
- Pin the profile to its own dock spot (right-click → Pin) so you can launch it directly.

## Why this matters

Browser profile isolation is the cheapest possible insulation between LatticeWorks activity and the rest of your identity. Sessions, cookies, autofill, history — none of it crosses over.

## Verification

When you open the LatticeWorks Chrome profile, you should see:
- Zero bookmarks
- Zero extensions (we'll add 1Password in Card 3)
- Zero browser history
- Not signed into any Google account

If anything got auto-imported from your other profiles, delete it now. Treat this profile as a quarantine.""",
    },
    {
        "title": "2 — Install Brave Browser on iPhone",
        "step": 2,
        "body": """## What to do

App Store → search **Brave Browser** → install.

From here on, **all LatticeWorks-related mobile activity happens in Brave**, not Safari/Chrome.

- Don't sign in to Brave Sync (keep it ephemeral)
- Don't import bookmarks
- Treat it as a quarantine, same as the Mac Chrome profile

## Why this matters

iOS doesn't support Safari profile separation the way macOS Chrome does. Using a different browser app (Brave) is the cleanest mobile isolation available. Your personal Safari stays clean for personal use.

## Verification

Open Brave on iPhone. The home screen should be empty (no bookmarks, no recent sites). That's correct.""",
    },
    {
        "title": "3 — Create LatticeWorks vault in 1Password",
        "step": 3,
        "body": """## What to do

Open 1Password (you already have it). In the sidebar → click **+** next to Vaults → **New Vault**.

- **Name:** `LatticeWorks`
- **Description:** `All credentials for the LatticeWorks project. Will be exported and handed off.`
- Color: pick one you don't use elsewhere

Then in the LatticeWorks Chrome profile:
- Go to https://1password.com/downloads/browser → install the 1Password extension
- Sign in with your existing 1Password account
- In the extension settings → set **Default vault** to `LatticeWorks`

## Why this matters

This vault is the deed of sale at handoff. Every credential for every LatticeWorks vendor account goes here — and **nothing else** goes here. When you hand the project off to the client, you export this one vault and they have everything.

## Verification

In the LatticeWorks Chrome profile, click the 1Password extension icon → confirm the active vault is `LatticeWorks`. New items saved from this profile should land in this vault by default.""",
    },
    {
        "title": "4 — Sign up Privacy.com (or confirm existing access)",
        "step": 4,
        "body": """## What to do

**If you already use Privacy.com** for other UpfrontOps work:
- Log in (via your LatticeWorks Chrome profile)
- Create a Group or use a card-name convention like `LW-<vendor>` to keep LatticeWorks cards separate from other clients

**If you don't:**
- Go to https://privacy.com → Sign up
- Use your existing real identity (Privacy.com requires KYC: name + SSN last 4) — this is fine, Privacy.com is a legitimate financial service, not contamination
- Link your existing personal or business checking account (Privacy only sees balance, not transaction history)

Save your Privacy.com login in 1Password under `LW-Privacy.com`.

## Why this matters

Virtual cards are how you sign up for every subsequent vendor without exposing your real card number or letting any single vendor have charge-back leverage on your bank account. Privacy is also US-only and adult-vendor-friendly.

## Verification

You should be able to land on the Privacy.com dashboard with a "Create New Card" button visible. Don't create one yet — that's Card 5.""",
    },
    {
        "title": "5 — Create your first test virtual card",
        "step": 5,
        "body": """## What to do

In Privacy.com dashboard → **Create New Card**:

- **Type:** Merchant Locked
- **Name:** `LW-Test`
- **Spend limit:** $1
- **Merchant lock:** leave blank for now (this is a smoke test)
- Click create

Save the card details (number, expiry, CVV) in 1Password under a new item called `LW-Test virtual card`.

**Don't actually use this card for anything.** It's just proof that Privacy.com is working end-to-end (account → bank link → card generation).

## Why this matters

Confirming Privacy.com works BEFORE you need it (Page 02 onward) means you don't get stuck at the Porkbun checkout page wondering why your card won't generate.

## Verification

Card appears in your Privacy.com dashboard with status `Active`. Card details copied to 1Password.""",
    },
    {
        "title": "6 — Get a burner phone number",
        "step": 6,
        "body": """## What to do

Pick **ONE** of these (recommendation: MySudo since Twitter has been increasingly rejecting Google Voice as VoIP):

### Option A — MySudo (recommended)

You've used MySudo before. Open the app → create a new **Sudo persona** named `LatticeWorks` → assign it a new phone number ($5/mo plan if you need a fresh paid number).

### Option B — Google Voice

Note: you can't get a Google Voice number until you have a Gmail to attach it to. You'll need to come back to this card AFTER Card 8 if you go this route.

In the LatticeWorks Chrome profile (signed into the throwaway Gmail from Card 8): https://voice.google.com → claim a US number with an area code that isn't yours.

### Either way

Save the number in 1Password under `LW-Phone`.

## Why this matters

You'll use this number for Telegram signup (Page 08), Twitter signup (Page 09), and any other vendor that requires SMS verification. Critically: **Twitter ACC enrollment** (Page 11) requires a real, working phone number. Google Voice numbers get rejected at ACC enrollment with rising frequency in 2026.

## Verification

You have a phone number. It can receive SMS. It's saved in 1Password.""",
    },
    {
        "title": "7 — Decide tax structure for this engagement",
        "step": 7,
        "body": """## What to do

This is a **decision**, not a signup. You don't form anything new yet — you just commit to a path so you know how to set up the next pages.

You have UpfrontOps LLC already. Three options:

| Option | Pros | Cons |
|---|---|---|
| **A. Flow revenue through UpfrontOps LLC** | Simplest. Clean tax filing. Reuses existing bank account. | UpfrontOps' books show adult-industry revenue (only visible to your accountant, IRS, and you, but still). |
| **B. Form new LLC just for LatticeWorks** | Cleanest isolation. UpfrontOps stays squeaky. Best liability separation. | ~$200-500 setup + annual fees. New EIN, new bank account, takes 1-2 weeks. |
| **C. 1099 personal income** | Zero setup. | No LLC liability protection. Adult work tied directly to your personal name on tax filings. |

**Recommendation:** A or B depending on how much adult-industry exposure you want on UpfrontOps' books. If client is paying $5-10K/mo, B starts to pay for itself in liability terms.

## Write the decision in 1Password

Open 1Password → LatticeWorks vault → **+ New Item** → Secure Note → title `LW-Tax structure`.

Write: `Option chosen: A/B/C`. If B, also write: `Action: form WY/DE LLC by [date]`.

## Why this matters

Pages 04 (NowPayments KYC) and 11 (Twitter ACC enrollment) both ask for tax / business identity. If you're going B (new LLC), you need to form it BEFORE those pages, which means starting now in parallel.""",
    },
    {
        "title": "8 — Create throwaway Gmail for bootstrap",
        "step": 8,
        "body": """## What to do

In the LatticeWorks Chrome profile, go to https://accounts.google.com → **Create account** → For my personal use.

- **Username:** `latticeworks.dev@gmail.com` (or `latticeworks.setup@gmail.com` or variant if taken)
- **Phone verification:** use your real personal phone for the SMS code (one-time use; Google won't link it to anything else automatically)
- **Recovery email:** skip
- **Save** the login in 1Password under `LW-Gmail (bootstrap)`

## Why this matters

Porkbun (Page 02) and Migadu (Page 03) need an email address for their account holder records. You can't use your real email (contamination) and you can't use `me@latticeworks.io` yet (it doesn't exist yet — chicken and egg).

This throwaway Gmail has **one job**: receive verification emails for Porkbun + Migadu, then sit dormant. Once `me@latticeworks.io` is live (after Page 03), you'll update Porkbun and Migadu's account-holder emails to `me@`, and this Gmail goes dormant forever.

## Why Gmail and not another throwaway service

Porkbun and Migadu both occasionally flag freshly-created accounts on Tutanota/Proton/etc. as fraud risk. Gmail at signup has the lowest friction. Use it for THIS purpose only.

## Verification

You can log into the throwaway Gmail. Login is in 1Password.""",
    },
    {
        "title": "9 — Sterilize the LatticeWorks Chrome profile",
        "step": 9,
        "body": """## What to do

Open the LatticeWorks Chrome profile and confirm:

- [ ] Zero bookmarks (Bookmarks bar empty, Bookmarks Manager shows no items)
- [ ] Zero extensions except **1Password** (chrome://extensions)
- [ ] Zero history (chrome://history — clear if anything)
- [ ] No Google account signed in at the Chrome browser level (top-right profile circle)
- [ ] No saved passwords from other profiles (chrome://settings/passwords)
- [ ] No autofill addresses or payment methods (chrome://settings/payments and chrome://settings/addresses)

If anything's there, delete it.

## Why this matters

The whole point of the isolation is that NO part of your existing identity bleeds into LatticeWorks activity. A bookmark to your UpfrontOps Slack, a cached login to your personal email, an autofill address with your real name — any of those, leaked via a bug or a screen-share, blows the isolation.

## Verification

You opened all six chrome:// settings listed above and confirmed each was empty. The only extension is 1Password.""",
    },
    {
        "title": "10 — Final verification + open Page 02",
        "step": 10,
        "body": """## Confirm all of these are true

- [ ] LatticeWorks Chrome profile exists on Mac, pinned, signed out of Google, sterile
- [ ] Brave Browser installed on iPhone
- [ ] `LatticeWorks` vault exists in 1Password
- [ ] 1Password extension installed in LatticeWorks Chrome profile, default vault set
- [ ] Privacy.com active, bank linked (or existing access confirmed)
- [ ] `LW-Test` virtual card created (saved in 1Password as `LW-Test virtual card`)
- [ ] `LW-Phone` number active and saved in 1Password (MySudo or Google Voice)
- [ ] Tax structure decided and noted in 1Password as `LW-Tax structure`
- [ ] `LW-Gmail (bootstrap)` account created and saved in 1Password

## All 9 boxes checked?

Drag this card to **Done** alongside the others. Then open **Page 02 — Register your domain** (it'll be the next document in the LatticeWorks folder).

## Why this matters

Page 02 makes zero sense without these foundations. Specifically:
- You need the LW Chrome profile to sign up for Porkbun in isolation
- You need the throwaway Gmail to receive Porkbun's verification email
- You need a Privacy.com card to pay for the domain
- You need 1Password to save Porkbun credentials

If any box above is unchecked, Page 02 will dead-end on you. Finish them all first.""",
    },
]

# Add items batched
items_payload = [
    {
        "title": c["title"],
        "properties": {"status": "Todo", "step": c["step"]},
    }
    for c in cards
]
r = call("POST", f"/collections/{coll_id}/items", {"items": items_payload})
item_ids = [item["id"] for item in r["items"]]
print(f"[OK] {len(item_ids)} kanban cards created")

# Add body content to each card
for i, (card, item_id) in enumerate(zip(cards, item_ids), 1):
    call("POST", "/blocks", {
        "markdown": card["body"],
        "position": {"position": "end", "pageId": item_id},
    })
    print(f"[OK] Card {i}/10 body content added")

print()
print("=" * 60)
print("BUILD COMPLETE")
print("=" * 60)
print(f"Folder: LatticeWorks (id={folder_id})")
print(f"Start Here doc id: {start_doc_id}")
print(f"Page 01 doc id:    {page01_id}")
print(f"Page 01 kanban id: {coll_id}")
print(f"Cards created:     {len(item_ids)}")
print()
print("Open Craft → LatticeWorks → Page 01 → click the collection block")
print("→ View → Kanban → drag cards left-to-right as you work them.")
