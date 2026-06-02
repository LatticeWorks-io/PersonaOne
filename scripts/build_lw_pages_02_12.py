#!/usr/bin/env python3
"""Build LatticeWorks Pages 02-12 in Craft."""

import json
import urllib.request
from pathlib import Path

API = (Path.home() / ".config" / "craft" / "connect-url").read_text().strip()
AUTH = (Path.home() / ".config" / "craft" / "token").read_text().strip()
IDS_FILE = Path.home() / ".config" / "craft" / "latticeworks-ids.json"
IDS = json.loads(IDS_FILE.read_text())
FOLDER_ID = IDS["folder_id"]


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
        raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode()}")


KANBAN_CALLOUT = """<callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>"""


def build_page(num, title, intro, cards, start_step):
    """num: 2..12. title: page title. intro: markdown body. cards: list of {title, body}."""
    # 1. Create the page doc
    r = call("POST", "/documents", {
        "documents": [{"title": f"Page {num:02d} — {title}"}],
        "destination": {"folderId": FOLDER_ID},
    })
    doc_id = r["items"][0]["id"]
    print(f"[OK] Page {num:02d} doc: id={doc_id}")

    # 2. Populate intro with callout + body
    full_intro = f"# Page {num:02d} — {title}\n\n{KANBAN_CALLOUT}\n\n{intro}"
    call("POST", "/blocks", {
        "markdown": full_intro,
        "position": {"position": "end", "pageId": doc_id},
    })

    # 3. Create kanban collection
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

    # 4. Add items (batched)
    items_payload = [
        {"title": c["title"], "properties": {"status": "Todo", "step": start_step + i}}
        for i, c in enumerate(cards)
    ]
    r = call("POST", f"/collections/{coll_id}/items", {"items": items_payload})
    item_ids = [item["id"] for item in r["items"]]

    # 5. Add body content to each item
    for i, (card, item_id) in enumerate(zip(cards, item_ids), 1):
        call("POST", "/blocks", {
            "markdown": card["body"],
            "position": {"position": "end", "pageId": item_id},
        })
    print(f"[OK] Page {num:02d}: {len(item_ids)} cards + body content")

    return {"doc_id": doc_id, "collection_id": coll_id, "item_ids": item_ids}


# =============================================================
# PAGE 02 — Register your domain
# =============================================================
page02_cards = [
    {
        "title": "11 — Open Porkbun in your LatticeWorks Chrome profile",
        "body": """## What to do

In the LatticeWorks Chrome profile, navigate to https://porkbun.com.

## Why this matters

Porkbun in the wrong browser profile = a domain registration tied to your personal Google session, with autofill / saved cards potentially exposing your real identity. Use the LatticeWorks profile or stop here.

## Verification

The browser tab shows porkbun.com, and the profile color indicator (top right Chrome corner) is the LatticeWorks color. You are NOT signed into any Google account at the Chrome level.""",
    },
    {
        "title": "12 — Search for `latticeworks` availability",
        "body": """## What to do

In Porkbun's search bar at the top of the homepage, type `latticeworks` and press search.

You'll see all TLD options with their prices.

## Your TLD priority (pick the first available)

1. **`.io`** — $32.37/yr first year, $51.80/yr renewal. Tech-y, professional, what most SaaS uses.
2. **`.com`** — $9.73/yr. Cheapest if available, but `latticeworks.com` may be taken.
3. **`.dev`** — typically $15-20/yr. Tech-focused, signals "this is a software thing."
4. **`.systems`** — $30-40/yr. Generic SaaS feel.
5. **`.app`** — $15-20/yr. Requires HTTPS (built into the TLD).
6. **`.co`** — $25-35/yr. Short, professional.

Avoid: `.net` (looks dated), country TLDs (`.io` is offshore but treated as global), `.online`/`.xyz` (cheap but lower trust signal).

## Verification

You have a target TLD picked. Don't add to cart yet — that's Card 13 after you have a Privacy.com card ready in Card 14.""",
    },
    {
        "title": "13 — Confirm the TLD decision and document it",
        "body": """## What to do

Open 1Password → LatticeWorks vault → + New Item → Secure Note → title `LW-Domain decision`.

Write: `Chosen domain: latticeworks.<TLD>. Reason: <one line>.`

Example: `Chosen domain: latticeworks.io. Reason: most professional / least likely to confuse vendors.`

## Why this matters

Once you register, you can't easily change your mind (you'd be eating the registration fee). Documenting the decision now means future-you doesn't have to remember why you picked it.

## Verification

Note saved in 1Password. You're committed to a specific TLD.""",
    },
    {
        "title": "14 — Create a Privacy.com card locked to Porkbun",
        "body": """## What to do

Open Privacy.com in your LatticeWorks Chrome profile. Create New Card:

- **Type:** Merchant Locked
- **Name:** `LW-Porkbun`
- **Spend limit:** $80 (covers your domain + first renewal headroom)
- **Merchant lock:** type `porkbun.com` — this prevents the card from being charged by any other vendor
- Click Create

Save the card number, expiry, CVV in 1Password under `LW-Porkbun virtual card`.

## Why this matters

Merchant-locked cards mean even if Porkbun's database is breached, the leaked card can't be used elsewhere. Per-vendor isolation.

## Verification

Card exists in Privacy.com dashboard with status `Active` and merchant `porkbun.com`. Card details in 1Password.""",
    },
    {
        "title": "15 — Add domain to cart with Privacy WHOIS + auto-renew",
        "body": """## What to do

Back on Porkbun's domain search result, click **Add to Cart** on your chosen TLD.

In the cart:
- **Privacy WHOIS:** Confirm ON (it's free with every Porkbun domain). This hides your name/address from public WHOIS lookups.
- **Auto-renew:** Set to **ON**. You do NOT want this domain expiring while the persona is running.
- **Years:** 1 year is fine. You can extend later.

Do NOT click checkout yet — Card 16 covers sign-up + payment.

## Why this matters

If Privacy WHOIS is off, anyone running `whois yourdomain.io` sees your name + address. Auto-renew off = the persona's domain quietly expires one day and the whole operation dies. Both default-on / default-correct settings, but worth confirming.

## Verification

Cart shows: 1 domain, Privacy WHOIS enabled, auto-renew ON, 1 year term.""",
    },
    {
        "title": "16 — Sign up Porkbun account + checkout",
        "body": """## What to do

Click **Checkout**. Porkbun will prompt for account creation.

- **Email:** your throwaway Gmail from Page 01 Card 8 (`latticeworks.dev@gmail.com` or whatever variant you used)
- **Password:** generate a strong unique one with 1Password's password generator → save in 1Password under `LW-Porkbun account`
- **Coupon code:** check r/PorkbunReg or porkbun.com/coupon for current promo (often $1-5 off first year)

At payment:
- **Card:** the `LW-Porkbun` virtual card from Card 14
- Verify total matches expected (domain price + ICANN $0.18 fee)
- Submit

## Verification

Order confirmation page shows. Save the order # in 1Password as a comment under `LW-Porkbun account`.""",
    },
    {
        "title": "17 — Verify the registration confirmation email",
        "body": """## What to do

Open your throwaway Gmail (in the LatticeWorks Chrome profile — DO NOT log into it from your personal profile).

You should receive within 5 minutes:
1. Order confirmation from Porkbun
2. A verification email from Porkbun (REQUIRED — click the link to verify your email)

Click the verification link in email #2. This activates your registration.

## Why this matters

ICANN requires email verification for new registrations. If you skip this for 15 days, the registrar can suspend your domain. Don't forget.

## Verification

You clicked the verification link. The success page on Porkbun confirms `email verified`.""",
    },
    {
        "title": "18 — Enable 2FA on Porkbun",
        "body": """## What to do

In Porkbun account settings, find **Security** or **Two-Factor Authentication**.

- Enable TOTP-based 2FA
- Use 1Password to store the TOTP seed (under `LW-Porkbun account` → add OTP field)
- Save the backup codes Porkbun provides in 1Password under `LW-Porkbun account` → secure note section

## Why this matters

A compromised Porkbun account means an attacker can redirect your DNS to anywhere, including hijacking your persona's traffic. 2FA is non-optional for the domain registrar.

## Verification

Logging out and back in prompts for the 2FA code. 1Password auto-fills the TOTP.""",
    },
    {
        "title": "19 — Confirm domain is Active in Porkbun dashboard",
        "body": """## What to do

In Porkbun → Account → My Domains.

Your new domain should show:
- Status: **Active**
- Expiry: ~1 year from now
- Auto-renew: ON
- Privacy WHOIS: enabled

If status is "Pending" — wait 5-15 minutes and refresh.

If after 30 minutes status is still pending or you see an error — contact Porkbun support (their support is unusually responsive for the price).

## Verification

Domain shows `Active`. You own it.""",
    },
    {
        "title": "20 — Final check before Page 03",
        "body": """## Confirm all of these are true

- [ ] You own a domain: `latticeworks.<TLD>` (note which TLD in 1Password)
- [ ] Domain shows Active in Porkbun dashboard
- [ ] Privacy WHOIS is enabled (your name is hidden from public lookups)
- [ ] Auto-renew is ON
- [ ] Porkbun account 2FA is enabled, TOTP seed in 1Password
- [ ] You can log into Porkbun fresh and 1Password fills credentials + TOTP
- [ ] Domain decision documented in 1Password (`LW-Domain decision`)

## Why these matter for Page 03

Page 03 needs the domain to exist so we can point email at it. Without verified ownership and DNS access (which Porkbun gives you), Migadu can't activate your custom email.

## All 7 boxes checked?

Drag this card to Done. Open **Page 03 — Set up email at Migadu**.""",
    },
]

# =============================================================
# PAGE 03 — Set up email at Migadu + DNS
# =============================================================
page03_cards = [
    {
        "title": "21 — Sign up Migadu (use throwaway Gmail)",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://www.migadu.com/signup.

- **Plan:** select **Mini** ($19/year). It includes: unlimited mailboxes, unlimited aliases, unlimited domains, 30 daily / 200 incoming emails — plenty for a single-persona ops setup.
- **Email for account login:** your throwaway Gmail from Page 01 Card 8 (`latticeworks.dev@gmail.com`)
- **Password:** strong, unique, generated via 1Password
- Save login in 1Password under `LW-Migadu account`

## Why Migadu (not Proton, not Tuta, not Workspace)

Migadu doesn't filter by content. Their TOS is "don't spam." Adult-industry-friendly in practice (won't suspend you for hosting email for an adult persona). Cheap. Founder-run Swiss company.

ProtonMail and Tutanota have suspended accounts associated with adult industries. Google Workspace is strictly prohibited (their TOS catches this fast). Don't use them.

## Verification

Migadu dashboard loads. You're logged in. Account in 1Password.""",
    },
    {
        "title": "22 — Create Privacy.com card for Migadu and pay annual",
        "body": """## What to do

In Privacy.com (LatticeWorks Chrome profile), create new card:
- **Type:** Merchant Locked
- **Name:** `LW-Migadu`
- **Spend limit:** $50 (covers $19/yr + headroom for renewals)
- **Merchant lock:** `migadu.com`

Save card to 1Password under `LW-Migadu virtual card`.

Back in Migadu, complete the payment with this card. Choose **annual** billing ($19/yr) — there's no monthly option on Mini and annual is the recommended pricing.

## Verification

Migadu shows subscription `Active`. Receipt arrived in throwaway Gmail.""",
    },
    {
        "title": "23 — Add your domain to Migadu",
        "body": """## What to do

In Migadu dashboard:
- Navigate to **Domains** in the sidebar
- Click **Add domain**
- Enter your domain: `latticeworks.<TLD>` (the one you registered in Page 02)
- Click Add

Migadu will now show your domain in the list with status `Pending DNS verification`.

## Verification

Domain appears under Domains in Migadu, with status pending DNS config.""",
    },
    {
        "title": "24 — Pull the DNS records Migadu generated",
        "body": """## What to do

Click into your newly-added domain in Migadu. Look for the **DNS** or **Setup** tab.

Migadu shows you records you need to add at your registrar:
- **MX records** (2 of them: aspmx1.migadu.com, aspmx2.migadu.com, priorities 10 and 20)
- **SPF record** (TXT, value `v=spf1 include:spf.migadu.com -all`)
- **DKIM records** (TXT, 3 keys for key1/key2/key3 selectors)
- **DMARC record** (TXT, value something like `v=DMARC1; p=quarantine; rua=mailto:dmarc@<yourdomain>`)

**Open a note** (1Password Secure Note `LW-Migadu DNS records`) and **copy every record's name + type + value** exactly. You'll paste these into Porkbun in Card 25.

## Why this matters

DNS configuration mistakes are the #1 cause of email delivery problems. SPF/DKIM/DMARC alignment determines whether your outbound emails land in inbox vs spam. Get all four right.

## Verification

All MX + SPF + DKIM + DMARC records copied to a 1Password secure note.""",
    },
    {
        "title": "25 — Add MX + TXT records to Porkbun DNS",
        "body": """## What to do

In Porkbun (LatticeWorks Chrome profile), go to your domain → **DNS Records**.

For each record from your 1Password note in Card 24, click **Add Record**:

**MX records (2):**
- Type: MX, Host: (leave blank or @), Answer: `aspmx1.migadu.com`, Priority: 10
- Type: MX, Host: (leave blank or @), Answer: `aspmx2.migadu.com`, Priority: 20

**SPF (1):**
- Type: TXT, Host: (leave blank or @), Answer: `v=spf1 include:spf.migadu.com -all`

**DKIM (3, one per selector key1/key2/key3):**
- Type: TXT, Host: `key1._domainkey`, Answer: (long string from Migadu)
- Same for key2 and key3

**DMARC (1):**
- Type: TXT, Host: `_dmarc`, Answer: `v=DMARC1; p=quarantine; rua=mailto:dmarc@<yourdomain>`

Save each record.

## Verification

Porkbun DNS records show all 7 records (2 MX + 5 TXT) for your domain.""",
    },
    {
        "title": "26 — Wait for DNS propagation (~5-30 min)",
        "body": """## What to do

DNS changes don't take effect instantly. Two ways to check:

**Option A: Terminal (faster, more authoritative)**

On your Mac terminal:
```
dig MX latticeworks.io +short
dig TXT latticeworks.io +short
```

You should see migadu's MX records and the SPF record. If you see nothing or the wrong records, wait 5 min and retry.

**Option B: Browser check (slower, more user-friendly)**

Go to https://www.whatsmydns.net → search your domain → MX records. You'll see propagation status across the world.

Wait until at least 80% of locations show the correct Migadu MX records before continuing.

## Why this matters

If you try to verify Migadu before DNS propagates, verification fails. Patience pays off.

## Verification

`dig MX <yourdomain>` shows Migadu's MX records, OR whatsmydns.net shows MX propagation across most regions.""",
    },
    {
        "title": "27 — Verify domain in Migadu",
        "body": """## What to do

Back in Migadu dashboard → Domains → click your domain → **Verify** or **Refresh status**.

Migadu will run DNS checks against your records. After a few seconds you should see:
- MX records: ✅
- SPF: ✅
- DKIM (key1, key2, key3): ✅
- DMARC: ✅

If anything shows ❌:
- Wait another 5 min (DNS may still be propagating)
- Re-check the record in Porkbun against what Migadu expects (spaces, quotes, casing matter)
- Click Verify again

## Verification

All 6 DNS checks in Migadu show ✅ green.""",
    },
    {
        "title": "28 — Create me@latticeworks.io mailbox",
        "body": """## What to do

In Migadu → your domain → **Mailboxes** → Add mailbox.

- **Local part:** `me`
- **Full address:** `me@latticeworks.<TLD>`
- **Password:** generate strong unique password via 1Password
- **Recovery email:** your throwaway Gmail
- Save in 1Password under `me@latticeworks.<TLD>`

## Why "me@" not "ryan@" or "ops@"

`me@` is:
- Untied to your real name (avoids identity leakage in From: headers)
- Short (memorable)
- Professional-feeling

Don't use a name-based prefix. Don't use the persona's name either (separation of concerns — this is YOUR operator email, not the persona's).

## Verification

Mailbox exists in Migadu. Login + password in 1Password.""",
    },
    {
        "title": "29 — Enable catch-all addressing",
        "body": """## What to do

In Migadu → your domain → **Aliases** (or **Catch-all**).

Configure:
- **Catch-all destination:** `me@latticeworks.<TLD>`
- This means: any email sent to `*@latticeworks.<TLD>` (e.g., `runpod@latticeworks.io`, `hostwinds@latticeworks.io`, `random@latticeworks.io`) routes to your `me@` inbox.

Save.

## Why catch-all is the cleanest practice

For every vendor signup in Pages 04+, you use a vendor-specific alias:
- `hostwinds@latticeworks.<TLD>` for Hostwinds
- `runpod@latticeworks.<TLD>` for RunPod
- `claude@latticeworks.<TLD>` for Anthropic
- etc.

You don't have to create each mailbox in advance — catch-all routes everything to your one inbox. AND if one alias starts getting spam, you know exactly which vendor leaked your address.

## Verification

Catch-all is enabled. (Verify in Card 30.)""",
    },
    {
        "title": "30 — Test the full mail flow + final check",
        "body": """## Test 1: send to me@

From the throwaway Gmail, send an email to `me@latticeworks.<TLD>`. Subject: "Test 1 - direct"

In Migadu webmail (https://webmail.migadu.com), log in as `me@latticeworks.<TLD>` → check inbox. Email should arrive within 1 minute.

## Test 2: catch-all

From the throwaway Gmail, send an email to `random-test-string@latticeworks.<TLD>`. Subject: "Test 2 - catch-all"

In Migadu webmail, refresh inbox. Email should arrive within 1 minute (to the `me@` inbox via catch-all).

## Test 3: outbound

From Migadu webmail, send an email FROM `me@latticeworks.<TLD>` TO your throwaway Gmail. Subject: "Test 3 - outbound"

In throwaway Gmail, check inbox. Verify:
- Email arrives in inbox (not spam)
- "Show original" → headers show SPF=pass, DKIM=pass, DMARC=pass

If any of these fail, DNS isn't fully right yet — wait another 30 min and retry.

## Final check

- [ ] `me@latticeworks.<TLD>` receives direct mail
- [ ] Catch-all routes random aliases to `me@` inbox
- [ ] Outbound mail from `me@` passes SPF + DKIM + DMARC at Gmail

## All 3 boxes checked?

Drag to Done. You now have a working professional email anchor. Open **Page 04 — Provision your server**.""",
    },
]


# =============================================================
# PAGE 04 — Provision Hostwinds dedicated box
# =============================================================
page04_cards = [
    {
        "title": "31 — Decide: Hostwinds or OVH (final pick)",
        "body": """## What to do

Re-confirm the host pick based on your priorities:

| | Hostwinds | OVH (US/Canada) |
|---|---|---|
| Entry dedicated price | $122/mo | $66.50/mo |
| Adult-industry posture | Markets to adult (explicit-friendly heritage) | Allows via AUP (not adult-marketed) |
| Hardware per dollar | Decent | Better |
| Support response | Old-school, slower | Faster, more technical |

**Recommendation: Hostwinds** if you want zero abuse-team risk and don't mind paying ~$60/mo more. **OVH (BHS Canada)** if you want better hardware-per-dollar and accept the slight abuse-team posture difference.

Write your final pick in 1Password under `LW-Host decision`.

## Verification

Decision documented. Move to Card 32 (rest of cards assume Hostwinds; if OVH, the steps are nearly identical but the UI looks different).""",
    },
    {
        "title": "32 — Sign up Hostwinds with hostwinds@latticeworks.<TLD>",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://www.hostwinds.com.

- Click Sign Up / Get Started
- **Email:** `hostwinds@latticeworks.<TLD>` (this works because of catch-all from Page 03 Card 29)
- **Password:** strong unique from 1Password
- Save login in 1Password under `LW-Hostwinds account`
- Verify the confirmation email arrives in your Migadu inbox (it'll route via catch-all to `me@`)

## Verification

Hostwinds dashboard accessible, login in 1Password.""",
    },
    {
        "title": "33 — Pick dedicated server config",
        "body": """## What to do

In Hostwinds dashboard → Servers → **Dedicated Server** → Configure.

**Entry-level dedicated config for LatticeWorks:**
- **CPU:** Xeon E3-1230v6 or equivalent (4 cores, 8 threads) — sufficient for orchestrator + Postgres + bot
- **RAM:** 16 GB minimum, 32 GB ideal
- **Storage:** 240 GB SSD primary + optional 1 TB HDD secondary (for content backups)
- **Bandwidth:** 10 TB/mo unmetered (Hostwinds default)
- **OS:** Ubuntu 24.04 LTS (long-term support, cleanest for Docker)
- **Datacenter:** Seattle (closer to Pacific if you're US West Coast) or Dallas (central US)

Expected price: ~$120-150/mo.

## Why dedicated > VPS for this

You'll run: Postgres, pgvector, Redis, Telegram bot, Twitter bot, scheduled job workers, web-scraping workers, plus ComfyUI orchestration. Together they oversubscribe a VPS's noisy-neighbor I/O. Dedicated = predictable performance.

## Verification

Server config in cart, total ~$120-150/mo. Don't checkout yet — Card 34 covers payment.""",
    },
    {
        "title": "34 — Create Privacy.com card for Hostwinds and pay",
        "body": """## What to do

In Privacy.com (LatticeWorks Chrome profile):
- **Type:** Merchant Locked
- **Name:** `LW-Hostwinds`
- **Spend limit:** $200 (covers monthly + headroom for surprise add-ons)
- **Merchant lock:** `hostwinds.com`

Save in 1Password under `LW-Hostwinds virtual card`.

Back in Hostwinds checkout, pay with this card. Choose monthly billing (annual is cheaper but locks you in before you know if it's the right pick).

## Verification

Order placed. Confirmation email in Migadu inbox.""",
    },
    {
        "title": "35 — Generate a new SSH keypair for LatticeWorks",
        "body": """## What to do

On your Mac terminal (NOT your existing SSH key — generate a NEW one for LatticeWorks isolation):

```
ssh-keygen -t ed25519 -C "latticeworks-admin" -f ~/.ssh/latticeworks_ed25519
```

When prompted for passphrase: **set a strong one** (save in 1Password under `LW-SSH key passphrase`). Don't leave it empty.

This creates:
- `~/.ssh/latticeworks_ed25519` (private key)
- `~/.ssh/latticeworks_ed25519.pub` (public key)

## Save to 1Password

1Password supports SSH keys natively. In LatticeWorks vault:
- New Item → SSH Key
- Drag in `~/.ssh/latticeworks_ed25519` (private key)
- Name: `LW-SSH admin key`
- Save

## Configure SSH agent

Add to `~/.ssh/config`:
```
Host lw-host
  HostName <will-fill-in-Card-37>
  User root
  IdentityFile ~/.ssh/latticeworks_ed25519
  IdentitiesOnly yes
```

## Verification

`ls ~/.ssh/latticeworks_ed25519*` shows both files. 1Password has the SSH key item.""",
    },
    {
        "title": "36 — Wait for provisioning + get server IP",
        "body": """## What to do

Hostwinds dedicated provisioning takes 5-30 minutes (sometimes up to 2 hrs depending on load).

You'll get an email at `me@latticeworks.<TLD>` when provisioning is complete, with:
- Server IP address
- Root password (initial)
- Optional: SSH access details

When the email arrives:
- Save the IP address in 1Password under `LW-Hostwinds server` (Server tab)
- Save the initial root password in 1Password (you'll change it in Card 38)

## Verification

You have the server IP and initial root password in 1Password.""",
    },
    {
        "title": "37 — First SSH connection and add public key",
        "body": """## What to do

Update `~/.ssh/config` with the server IP from Card 36:
```
Host lw-host
  HostName <SERVER-IP-FROM-CARD-36>
  User root
  IdentityFile ~/.ssh/latticeworks_ed25519
  IdentitiesOnly yes
```

In your Mac terminal:
```
# First-time login uses password (not SSH key yet)
ssh root@<SERVER-IP>
# Enter initial root password from Hostwinds email
```

You're in. Now add your SSH public key:
```
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cat >> ~/.ssh/authorized_keys << 'EOF'
<paste contents of ~/.ssh/latticeworks_ed25519.pub here>
EOF
chmod 600 ~/.ssh/authorized_keys
```

Exit SSH session. Try logging in again:
```
ssh lw-host
```

Should login without password (using your SSH key).

## Verification

`ssh lw-host` works without a password. You're in via key auth.""",
    },
    {
        "title": "38 — Harden SSH config and disable password auth",
        "body": """## What to do

On the Hostwinds server (via `ssh lw-host`):

```
# Edit SSH config
sudo nano /etc/ssh/sshd_config
```

Set/change:
- `PermitRootLogin prohibit-password` (allows root via key, blocks password)
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`
- `Port 22` (or change to nonstandard like 2222 if you want — note in 1Password)

Save (Ctrl+O, Enter, Ctrl+X).

Reload SSH:
```
sudo systemctl restart ssh
```

**Before disconnecting**, open a SECOND terminal and verify `ssh lw-host` still works. If it doesn't, the first session is still alive and you can revert.

## Verification

Second SSH session connects via key. Password auth is rejected (`ssh root@<ip>` with no key fails).""",
    },
    {
        "title": "39 — Install firewall + basic hardening",
        "body": """## What to do

On the Hostwinds server:

```
# Update first
sudo apt update && sudo apt upgrade -y

# Install ufw firewall
sudo apt install -y ufw fail2ban

# Default deny incoming, allow outgoing
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (port 22 or whatever you set)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS (for webhook receivers etc.)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status
```

Enable fail2ban (auto-bans IPs that try to brute-force SSH):
```
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Verification

`sudo ufw status` shows active with rules for 22, 80, 443. `sudo systemctl status fail2ban` shows running.""",
    },
    {
        "title": "40 — Final check before Page 05",
        "body": """## Confirm

- [ ] Hostwinds dedicated server provisioned and running
- [ ] Server IP saved in 1Password under `LW-Hostwinds server`
- [ ] SSH key (Ed25519) generated, public key on server, private key in 1Password
- [ ] `ssh lw-host` works via key auth (no password prompt)
- [ ] Password authentication is disabled (only key auth works)
- [ ] Firewall (ufw) is active, allowing 22/80/443
- [ ] fail2ban is running

## Why this matters for Page 05

Page 05 sets up RunPod (GPU compute) + storage (Backblaze B2) + CDN (BunnyCDN). Some of these signups will use your server's IP for whitelisting. Easier to have it provisioned and hardened first.

## All 7 boxes checked?

Drag to Done. Open **Page 05 — RunPod + storage + CDN**.""",
    },
]


# =============================================================
# PAGE 05 — RunPod + Storage + CDN
# =============================================================
page05_cards = [
    {
        "title": "41 — Sign up RunPod (GPU compute)",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://runpod.io.

- Sign up with `runpod@latticeworks.<TLD>`
- Strong password from 1Password, save to `LW-RunPod account`
- Email verification arrives via Migadu catch-all → click verify link

## Verification

RunPod dashboard accessible. Login in 1Password.""",
    },
    {
        "title": "42 — Fund RunPod with starter credit",
        "body": """## What to do

In RunPod dashboard → Billing → Add Credit.

- Create new Privacy.com card: `LW-RunPod`, lock to `runpod.io`, limit $100/mo
- Save to 1Password as `LW-RunPod virtual card`
- Add $30-50 starter credit (you'll use it slowly during build/test phases)

## Why pay-as-you-go (not commit pricing)

RunPod offers Savings Plans (committed monthly spend for discount). Don't commit yet — you don't know your usage pattern. Start with PAYG; commit later if usage justifies it.

## Verification

RunPod shows balance ~$30-50.""",
    },
    {
        "title": "43 — Test-deploy a simple pod (smoke test)",
        "body": """## What to do

In RunPod → Pods → Deploy.

- **GPU:** RTX 4090 (community cloud, ~$0.34/hr — cheapest test)
- **Template:** Pick "PyTorch 2.x" or "RunPod Tensorflow"
- **Container Disk:** 20 GB
- **Volume:** none for now
- **Network Volume:** none for now
- Click Deploy

Pod takes 30-90 seconds to provision. Once running, click **Connect** → use Web Terminal.

In the web terminal, run:
```
nvidia-smi
```

You should see a RTX 4090 with `0%` GPU utilization.

## Verification

You connected to a real GPU. `nvidia-smi` works.

## Cleanup

**Important: stop the pod when done with the test.** RunPod bills per second.
- In Pods → click your test pod → **Stop** (not Terminate yet — Stop preserves the pod for restart later)

Or **Terminate** if you don't need to keep the configuration.""",
    },
    {
        "title": "44 — Sign up Backblaze B2 (object storage)",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://www.backblaze.com/cloud-storage.

- Click "Sign Up" → choose B2 Cloud Storage
- Email: `b2@latticeworks.<TLD>`
- Password from 1Password, save to `LW-Backblaze account`
- Verification email arrives, click verify

## Verification

B2 dashboard accessible.""",
    },
    {
        "title": "45 — Create your first B2 bucket",
        "body": """## What to do

In B2 dashboard → Buckets → Create a Bucket:

- **Bucket Unique Name:** `lw-content-prod` (or `lw-<persona>-content`)
- **Files in Bucket are:** Private (NOT Public — you'll serve via CDN with signed URLs)
- **Default Encryption:** Disable (we'll handle encryption at the app layer if needed)
- **Object Lock:** Disable
- Click Create

## Verification

Bucket exists in B2 dashboard.""",
    },
    {
        "title": "46 — Generate B2 application keys",
        "body": """## What to do

In B2 dashboard → App Keys → Add a New Application Key:

- **Name:** `LW-bucket-rw`
- **Allow access to:** the specific bucket from Card 45 (NOT all buckets)
- **Type of Access:** Read and Write
- **File name prefix:** leave blank
- Click Create New Key

**Important:** the next page shows your `applicationKey` (long string). **This is the ONLY time you'll see it.** Copy it immediately.

Save in 1Password as `LW-B2 keys`:
- keyID: (the short one)
- applicationKey: (the long one)
- bucketName: `lw-content-prod`
- endpoint: shown in bucket settings (e.g., `s3.us-west-001.backblazeb2.com`)

## Verification

Keys saved in 1Password. You cannot recover the applicationKey if you lose it.""",
    },
    {
        "title": "47 — Sign up BunnyCDN",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://bunny.net.

- Sign Up with `bunny@latticeworks.<TLD>`
- Strong password from 1Password, save to `LW-BunnyCDN account`
- Email verification arrives, click verify
- Fund account with $10-20 (Privacy.com card `LW-BunnyCDN`)

## Verification

BunnyCDN dashboard accessible, balance ~$10-20.""",
    },
    {
        "title": "48 — Create a Pull Zone in Bunny connected to B2",
        "body": """## What to do

In BunnyCDN dashboard → Pull Zones → Add Pull Zone:

- **Name:** `lw-content`
- **Origin URL:** the B2 bucket endpoint, e.g., `https://lw-content-prod.s3.us-west-001.backblazeb2.com`
- **Pricing Tier:** Standard (lowest cost)
- **Geographic Regions:** Tick North America + Europe (your audience). Skip Asia/Africa/SA for now (3-12x more expensive).
- Click Add

This creates a Pull Zone with a URL like `lw-content.b-cdn.net`. Files in your B2 bucket are now reachable via that CDN URL.

## Verification

Pull Zone shows in BunnyCDN dashboard with status `Active`.""",
    },
    {
        "title": "49 — Smoke test: upload to B2, fetch via Bunny",
        "body": """## What to do

On the Hostwinds server (`ssh lw-host`):

```
# Install b2 CLI
sudo apt install -y python3-pip
pip3 install b2 --break-system-packages

# Authenticate
b2 account authorize <keyID> <applicationKey>

# Upload a small test file
echo "smoke test $(date)" > /tmp/smoke.txt
b2 file upload lw-content-prod /tmp/smoke.txt smoke.txt
```

From your Mac browser, hit:
```
https://lw-content.b-cdn.net/smoke.txt
```

You should see the contents of the file you uploaded (or be challenged for B2 auth if Pull Zone needs signed URLs).

## Verification

File uploaded to B2, fetchable via Bunny URL.

## If it doesn't work

- Pull Zone may need 2-5 min to propagate config to edge nodes — wait and retry
- B2 bucket may need `Public` if you're not using signed URLs (you'll handle signing in app code later — for smoke test you can temporarily flip to Public)""",
    },
    {
        "title": "50 — Final check before Page 06",
        "body": """## Confirm

- [ ] RunPod account active, ~$30-50 credit
- [ ] Test pod (RTX 4090) successfully deployed, ran `nvidia-smi`, then stopped/terminated
- [ ] Backblaze B2 account active with bucket `lw-content-prod`
- [ ] B2 application keys generated and saved in 1Password
- [ ] BunnyCDN account active, pull zone `lw-content` configured pointing at B2
- [ ] Smoke test: file uploaded to B2, fetched via `lw-content.b-cdn.net/...`
- [ ] All vendor credentials in 1Password under `LW-RunPod / LW-Backblaze / LW-BunnyCDN`

## Why this matters for Page 06

Page 06 sets up the AI APIs (Claude + OpenRouter + Postmark). These are simpler signups, but you'll need API keys saved in the same disciplined pattern.

## All 7 boxes checked?

Drag to Done. Open **Page 06 — AI APIs (Claude, OpenRouter, Postmark)**.""",
    },
]


# =============================================================
# PAGE 06 — AI APIs
# =============================================================
page06_cards = [
    {
        "title": "51 — Sign up Anthropic Console (Claude API)",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://console.anthropic.com.

- Sign Up with `claude@latticeworks.<TLD>`
- Password from 1Password, save to `LW-Anthropic account`
- Email verification via Migadu catch-all
- Phone verification: use `LW-Phone` (Card 6 from Page 01)

## Verification

Console accessible.""",
    },
    {
        "title": "52 — Fund Anthropic with starter credit",
        "body": """## What to do

In Console → Billing → Plans & Billing.

- Create Privacy.com card: `LW-Anthropic`, lock to `anthropic.com`, limit $200/mo
- Save to `LW-Anthropic virtual card` in 1Password
- Pre-pay $20-50 in credits

## Why pre-pay vs pay-as-you-go

Pre-paid credits give you a hard ceiling — runaway API loops can't exceed credit balance. Auto-recharge is convenient but risky for new projects. Set auto-recharge ON later once you know your burn rate.

## Verification

Account shows $20-50 in available credit.""",
    },
    {
        "title": "53 — Create the Claude API key",
        "body": """## What to do

In Console → API Keys → Create Key.

- **Name:** `LW-orchestrator`
- **Permissions:** Full access (default)
- Click Create

**Copy the key IMMEDIATELY** — `sk-ant-api03-...` format. This is the only time you'll see it.

Save in 1Password as `LW-Claude API key` (Secure Note or API Credential type).

## Verification

API key in 1Password. Test it:
```
curl https://api.anthropic.com/v1/messages \\
  -H "x-api-key: $LW_CLAUDE_KEY" \\
  -H "anthropic-version: 2023-06-01" \\
  -H "content-type: application/json" \\
  -d '{"model":"claude-sonnet-4-6","max_tokens":50,"messages":[{"role":"user","content":"Say hi"}]}'
```

Should return a response with "hi" in the content.""",
    },
    {
        "title": "54 — Sign up OpenRouter (for uncensored LLM)",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://openrouter.ai.

- Sign Up with `openrouter@latticeworks.<TLD>`
- Password from 1Password, save to `LW-OpenRouter account`

## Why OpenRouter (not self-hosted vLLM)

For our scale, OpenRouter is ~8x cheaper than self-hosting an uncensored Llama on RunPod 24/7. We confirmed this in cost analysis. Use OpenRouter unless / until usage justifies self-hosting.

## Verification

OpenRouter dashboard accessible.""",
    },
    {
        "title": "55 — Fund OpenRouter + generate API key",
        "body": """## What to do

In OpenRouter:
- Add credits: Privacy.com card `LW-OpenRouter`, lock to `openrouter.ai`, $50 starter
- Save card to `LW-OpenRouter virtual card` in 1Password

Generate API key:
- Settings → API Keys → Create New Key
- **Name:** `LW-uncensored-chat`
- Copy the key (`sk-or-v1-...`), save to `LW-OpenRouter API key` in 1Password

## Verification

Key works. Test:
```
curl https://openrouter.ai/api/v1/chat/completions \\
  -H "Authorization: Bearer $LW_OR_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"model":"sao10k/l3-lunaris-8b","messages":[{"role":"user","content":"hi"}]}'
```

Should return a response.""",
    },
    {
        "title": "56 — Test the uncensored model end-to-end",
        "body": """## What to do

You don't need to actually generate explicit content yet (that's Phase 6+ when the bot is wired). Just verify the uncensored model responds and isn't refusal-trained.

Send a benign but model-personality-revealing prompt via OpenRouter API:

```
curl https://openrouter.ai/api/v1/chat/completions \\
  -H "Authorization: Bearer $LW_OR_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"model":"sao10k/l3-lunaris-8b","messages":[{"role":"system","content":"You are a flirty character named Test."},{"role":"user","content":"hey there"}]}'
```

You should get a response that's flirty, personality-driven, not "I cannot engage in romantic roleplay" refusal.

If it refuses → try `cognitivecomputations/dolphin-2.6-mistral-7b` or another uncensored model on OpenRouter.

## Verification

Model returns in-character response. Save the model identifier you settled on in 1Password under `LW-Uncensored model choice`.""",
    },
    {
        "title": "57 — Sign up Postmark (transactional email)",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://postmarkapp.com.

- Sign Up with `postmark@latticeworks.<TLD>`
- Stay on **Free plan** for now (100 emails/mo, plenty for setup phase)
- Save login to `LW-Postmark account` in 1Password

## Why Postmark vs others

Postmark explicitly allows adult senders (other transactional providers like SendGrid have been known to suspend). Their deliverability is among the highest in the industry.

## Verification

Postmark dashboard accessible.""",
    },
    {
        "title": "58 — Create a Postmark Server + verify sender domain",
        "body": """## What to do

In Postmark dashboard → Servers → Create Server:
- **Name:** `LW-Transactional`
- **Color:** any
- Click Create

Then verify sending domain:
- Sender Signatures → Add Domain → enter `latticeworks.<TLD>`
- Postmark gives you DKIM + Return-Path DNS records to add at Porkbun (similar to what you did in Page 03)
- Add the records at Porkbun → DNS Records
- Click Verify in Postmark

## Verification

Postmark shows domain verified (green checkmarks on DKIM + Return-Path).""",
    },
    {
        "title": "59 — Get the Postmark Server API token",
        "body": """## What to do

In Postmark → your `LW-Transactional` server → API Tokens.

Copy the **Server API Token** (long string).

Save in 1Password as `LW-Postmark API token`.

Test with a curl from your Hostwinds server:

```
curl "https://api.postmarkapp.com/email" \\
  -X POST \\
  -H "Accept: application/json" \\
  -H "Content-Type: application/json" \\
  -H "X-Postmark-Server-Token: $LW_POSTMARK_TOKEN" \\
  -d '{
    "From":"me@latticeworks.<TLD>",
    "To":"<your throwaway Gmail>",
    "Subject":"Postmark test",
    "TextBody":"This is a smoke test from LatticeWorks."
  }'
```

Should return success and the email arrives at the throwaway Gmail within 30 sec.

## Verification

Smoke test email arrived.""",
    },
    {
        "title": "60 — Final check before Page 07",
        "body": """## Confirm

- [ ] Anthropic Console account + $20-50 credit + API key in 1Password
- [ ] Claude API smoke test succeeded
- [ ] OpenRouter account + $50 credit + API key in 1Password
- [ ] Uncensored model smoke test succeeded (model name documented in `LW-Uncensored model choice`)
- [ ] Postmark account on free tier + verified sender domain + API token in 1Password
- [ ] Postmark email smoke test succeeded

## All 6 boxes checked?

Drag to Done. Open **Page 07 — NowPayments + crypto wallet**.""",
    },
]


# =============================================================
# PAGE 07 — NowPayments + crypto wallet
# =============================================================
page07_cards = [
    {
        "title": "61 — Decide crypto wallet strategy",
        "body": """## What to do

Pick ONE wallet pattern (write decision in 1Password under `LW-Wallet strategy`):

### Option A — Hot software wallet (faster setup, less secure for large balances)
- **Phantom** (multi-chain: Solana, Bitcoin, Ethereum) — easy mobile + desktop app
- **MetaMask** (Ethereum/EVM only)
- Used for receiving payments + small balance hold
- Recommendation if you'll convert to fiat weekly

### Option B — Hardware wallet (slower setup, secure for large balances)
- **Ledger** or **Trezor** ($80-200 one-time hardware cost)
- 2-day shipping required
- Used for cold storage; hot wallet still needed for receiving
- Recommendation if you'll hold crypto long-term

### Hybrid (recommended)
- Phantom for receiving (NowPayments payout destination)
- Sweep balances over $1000 to a hardware wallet weekly

## Verification

Strategy documented in 1Password.""",
    },
    {
        "title": "62 — Install + set up your hot wallet (Phantom)",
        "body": """## What to do

Two installs to make it cross-device:

### Mac (LatticeWorks Chrome profile)
- chrome.google.com/webstore → search Phantom → install extension
- Open extension → Create New Wallet (NOT Import)
- Set a strong password (save in 1Password under `LW-Phantom wallet password`)
- Phantom shows your **12-word recovery phrase** — write it down on PAPER (not in 1Password — see Card 63)
- Verify the phrase by typing back into Phantom

### iPhone (Brave browser)
- App Store → install Phantom app
- Sign in using the recovery phrase from above (same wallet across devices)

## Verification

Phantom shows your wallet with $0 balance on both devices. Both show the same wallet address.""",
    },
    {
        "title": "63 — Secure the recovery phrase",
        "body": """## What to do

The 12-word recovery phrase from Card 62 is the **only** key to your wallet. Losing it = funds gone forever. Leaking it = funds stolen instantly.

### Storage best practice (do BOTH)

**Primary storage: physical**
- Write the 12 words on PAPER (not phone notes, not text file)
- Store in a fireproof location or safe deposit box
- Make a SECOND copy in a different physical location

**Secondary storage: 1Password (split)**
- In 1Password LatticeWorks vault → New Item → Secure Note
- Title: `LW-Wallet seed (PARTIAL — words 1-6)`
- Body: words 1-6
- Create a SECOND note `LW-Wallet seed (PARTIAL — words 7-12)` with the other half
- Reason for split: if 1Password vault is ever compromised, attacker still doesn't have full seed in one place

### Anti-pattern (DO NOT do)
- Save full seed in a single 1Password note
- Save in iCloud Notes / Apple Notes
- Photograph the seed (photos auto-sync to cloud)
- Type into ChatGPT / any chat

## Verification

You can demonstrate (to yourself) that you have the seed in two physical locations + split across 2 1Password notes.""",
    },
    {
        "title": "64 — Get your wallet address for NowPayments",
        "body": """## What to do

In Phantom (Mac extension or iPhone app):
- Click your wallet name at top → copy address
- Or use the QR code / share button

Save the wallet address in 1Password under `LW-Wallet address` (Secure Note, separate from seed):
- Solana address: `<base58 string>`
- Bitcoin address: (if you've enabled BTC in Phantom): `<bc1...>`
- Ethereum address: (if you've enabled ETH): `<0x...>`

## Why save all three

NowPayments will let you receive multiple cryptocurrencies. Customers paying in BTC vs USDT vs SOL have different on-chain fees and confirmation times. Supporting multiple chains = better UX.

## Verification

Wallet addresses saved in 1Password. You can paste them into NowPayments in Card 66.""",
    },
    {
        "title": "65 — Sign up NowPayments",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://nowpayments.io.

- Sign Up with `pay@latticeworks.<TLD>`
- **Important:** during signup, choose **Merchant** account type (not Individual)
- Strong password from 1Password, save to `LW-NowPayments account`

## Verification

NowPayments dashboard accessible. Account type shows Merchant.""",
    },
    {
        "title": "66 — Add your crypto wallet as payout destination",
        "body": """## What to do

In NowPayments dashboard → Settings → Payment Settings → Wallets.

For each cryptocurrency you'll accept:
- Click **Add wallet**
- Currency: pick (USDT-TRC20 is recommended for low fees; SOL for instant; BTC for whale tips)
- Address: paste from 1Password (Card 64)
- Click Save

NowPayments will require you to **verify each wallet** by sending a tiny test deposit (1-2 cents worth of crypto).

If you don't have any crypto yet:
- Buy ~$5 worth of USDT or SOL on Coinbase or Cash App
- Send to your Phantom wallet
- Then NowPayments can verify

## Verification

At least one wallet (USDT-TRC20 recommended) verified in NowPayments.""",
    },
    {
        "title": "67 — Submit KYC documents",
        "body": """## What to do

NowPayments requires KYC for merchant accounts (this is the gate to processing real money).

Documents you'll need:
- **Government-issued photo ID** (driver's license or passport)
- **Selfie** with the ID held visible (NowPayments will prompt for this in their KYC flow)
- **Proof of business:** depends on your tax structure from Page 01 Card 7
  - If existing LLC: LLC formation document + EIN
  - If new LLC: same once formed
  - If 1099: your SSN + a recent utility bill

In LatticeWorks Chrome profile, complete NowPayments KYC flow. Upload via their portal.

## Why KYC is required

NowPayments is a regulated MSB (Money Services Business). They must KYC merchants under AML laws. There's no way around this. Your real identity is on the merchant account — but the customer-facing brand can still be the persona.

## Verification

KYC submitted. Status in dashboard shows `Pending review`.""",
    },
    {
        "title": "68 — Wait for KYC approval (1-3 business days)",
        "body": """## What to do

KYC review typically takes 1-3 business days.

While waiting:
- Don't reapply or contact support unless 5+ business days pass
- Don't try to do test transactions yet
- Move on to Page 08 (Telegram setup) — that's independent

When approval email arrives at `me@latticeworks.<TLD>`:
- Save the approval timestamp in 1Password under `LW-NowPayments account` notes
- Status in dashboard updates to `Approved`

## Verification

Email confirming approval. Dashboard status `Approved`.""",
    },
    {
        "title": "69 — Test crypto payment flow end-to-end",
        "body": """## What to do

In NowPayments → Invoices → Create New Invoice:
- **Price:** $1.00 USD
- **Currency to receive:** USDT-TRC20 (or whichever wallet you verified)
- Click Create

NowPayments gives you a payment URL. Open it in another tab (or share with a test customer wallet).

From your Phantom wallet:
- Send $1 worth of USDT to the address shown on the invoice page
- Wait for confirmation (1-3 minutes for TRC20)

In NowPayments dashboard:
- Invoice should flip to `Paid` status
- Funds should appear in your wallet (the Phantom address from Card 64) within 5-10 min

## Verification

End-to-end: invoice created → payment sent → received in your wallet. The full money path works.

## Cost

You paid $1 + ~$0.10 in network fees + ~$0.005 NowPayments fee. Cheap smoke test.""",
    },
    {
        "title": "70 — Final check before Page 08",
        "body": """## Confirm

- [ ] Wallet strategy decided + documented in 1Password
- [ ] Phantom (or chosen wallet) installed on Mac + iPhone, same wallet across both
- [ ] Recovery phrase stored on PAPER in 2 physical locations
- [ ] Recovery phrase split-saved in 1Password (words 1-6, words 7-12 as separate notes)
- [ ] Wallet addresses (USDT/SOL/BTC) saved in 1Password under `LW-Wallet address`
- [ ] NowPayments merchant account created
- [ ] At least one wallet verified in NowPayments
- [ ] KYC submitted and approved
- [ ] Smoke test: $1 invoice → paid → received in wallet

## All 9 boxes checked?

Drag to Done. Open **Page 08 — Telegram setup**.""",
    },
]


# =============================================================
# PAGE 08 — Telegram setup
# =============================================================
page08_cards = [
    {
        "title": "71 — Install Telegram on Mac + iPhone",
        "body": """## What to do

### Mac
- Telegram Desktop: https://desktop.telegram.org → install for macOS
- Open Telegram Desktop

### iPhone
- App Store → Telegram Messenger → install

**Do not log in yet** — we need to do this carefully with the right phone number in Card 72.

## Why both surfaces

Telegram bots are operated through ONE Telegram account (the owner). You'll access the bot from both Mac (for admin / debugging) and iPhone (for mobile alerts). Same account, two devices.

## Verification

Telegram installed on both devices, both showing login screen.""",
    },
    {
        "title": "72 — Sign up Telegram with LW-Phone",
        "body": """## What to do

### On Mac Telegram Desktop:
- Click "Start Messaging"
- Country code: USA (+1)
- Phone number: enter `LW-Phone` (from Page 01 Card 6 — MySudo or Google Voice)
- Click Next
- Telegram sends SMS code to LW-Phone
- Open MySudo (or Google Voice) → retrieve code
- Enter code in Telegram

If Telegram asks for cloud password (2FA): you don't have one yet. Skip.

### Sign up details:
- First name: persona's stage name (e.g., `Lily`)
- Last name: leave blank
- Username (later step): persona's @handle (will match Twitter handle from Page 09)

### iPhone:
- Use the same number — Telegram will detect "already signed up" and let you authorize the second device with a code sent to Telegram Desktop

## Verification

Telegram active on Mac + iPhone, signed in as persona. No profile pic / bio yet.""",
    },
    {
        "title": "73 — Enable Telegram cloud password (2FA)",
        "body": """## What to do

In Telegram Desktop:
- Settings → Privacy and Security → Two-Step Verification (Cloud Password)
- Set Password: strong unique from 1Password
- Set Hint: something only you'd know (don't write the password itself as hint)
- Set Recovery Email: `me@latticeworks.<TLD>`

Save in 1Password as `LW-Telegram cloud password`.

## Why this matters

Without cloud password, anyone who gets your SMS (SIM swap attack, MySudo compromise, GV hijack) can take over the Telegram account, hijack the bot, and start tipping themselves money.

## Verification

Logging out and back in requires both SMS code AND cloud password. 1Password autofills the cloud password.""",
    },
    {
        "title": "74 — Create the persona's Telegram bot via @BotFather",
        "body": """## What to do

In Telegram Desktop:
- Search for `@BotFather` (the official bot for managing bots)
- Click Start

Send commands:
```
/newbot
```

BotFather asks for:
- **Bot name:** persona's full stage name (e.g., `Lily`)
- **Bot username:** must end in `bot` (e.g., `lily_lw_bot` or `lily_persona_bot`). Note: must be unique across Telegram.

BotFather responds with:
- Confirmation message
- **HTTP API token** — looks like `1234567890:AAEhBOweik6ad6PsWHDH7dC9PSnGy8Tcu1U`

**This is the bot's master key.** Copy it immediately. Save in 1Password under `LW-Telegram Bot Token`.

## Verification

Bot appears in your Telegram (search for the bot username, click to chat with it). Token saved in 1Password.""",
    },
    {
        "title": "75 — Configure bot description and about",
        "body": """## What to do

Back in chat with @BotFather, set bot metadata:

```
/setdescription
```
- Select your bot
- Description: short tagline (visible when users start a conversation). E.g., `your spicy AI gf 💋 [AI Persona]`
- Required: include AI disclosure per Twitter ACC alignment

```
/setabouttext
```
- Brief about (~120 chars max). E.g., `AI persona. NSFW chat + customs available.`

```
/setuserpic
```
- Upload a placeholder (e.g., a soft purple gradient — actual persona photos will come once content gen is wired)

## Verification

Bot's profile in Telegram shows description, about, and pic.""",
    },
    {
        "title": "76 — Send /start to your bot from your operator account",
        "body": """## What to do

In Telegram, find your new bot (search the username from Card 74).

Click Start (or send `/start`).

The bot won't reply yet — there's no code running. But Telegram now has a record of you as a user of your own bot. Useful for testing.

## Verification

You see your `/start` message in the bot chat. The bot doesn't reply (expected).""",
    },
    {
        "title": "77 — Smoke test: send a message FROM the bot via API",
        "body": """## What to do

From the Hostwinds server (`ssh lw-host`), run:

```
# Replace with values from 1Password
LW_BOT_TOKEN="your_bot_token_from_card_74"
LW_CHAT_ID="your_user_id"  # see below for how to find this

# Find your chat ID first
curl "https://api.telegram.org/bot${LW_BOT_TOKEN}/getUpdates"
# Look for "chat":{"id": NUMBER ...} — that NUMBER is your chat ID
```

Save your chat ID in 1Password as `LW-Telegram operator chat ID`.

Then send a test message FROM the bot TO you:

```
curl "https://api.telegram.org/bot${LW_BOT_TOKEN}/sendMessage" \\
  -d "chat_id=${LW_CHAT_ID}" \\
  -d "text=smoke test from server $(date)"
```

## Verification

Telegram on your devices receives the message from your bot. Confirms the bot can send programmatically.""",
    },
    {
        "title": "78 — Test Telegram Stars (in-bot payments)",
        "body": """## What to do

Stars are how customers will tip + buy customs. Test that the API can request payment.

From the Hostwinds server, send an invoice:

```
LW_BOT_TOKEN="your_bot_token"
LW_CHAT_ID="your_chat_id"

curl -X POST "https://api.telegram.org/bot${LW_BOT_TOKEN}/sendInvoice" \\
  -H "Content-Type: application/json" \\
  -d '{
    "chat_id": "'${LW_CHAT_ID}'",
    "title": "Test custom",
    "description": "smoke test of Stars payment",
    "payload": "smoke-test-001",
    "currency": "XTR",
    "prices": [{"label":"test","amount":1}]
  }'
```

In Telegram you'll see an invoice for 1 Star (~$0.013). Pay it (or close — both confirm the flow renders).

## Verification

Invoice card appears in your Telegram chat with the bot. You can see the "Pay 1 Star" button. (Actual payment is optional for smoke test.)""",
    },
    {
        "title": "79 — Enable Telegram inline + groups settings",
        "body": """## What to do

Back in @BotFather:

```
/setinline
```
- Select your bot
- Set placeholder text (visible when users type @botname in any chat): e.g., `search me...`
- This enables inline mode (the bot can be invoked from any chat by typing @botname)

```
/setjoingroups
```
- Select your bot → Disable (the bot is 1:1, not for groups)

```
/setprivacy
```
- Select your bot → Disable privacy (bot will receive ALL messages in DMs, not just commands starting with `/`)

## Verification

BotFather confirms each setting.""",
    },
    {
        "title": "80 — Final check before Page 09",
        "body": """## Confirm

- [ ] Telegram installed and signed in on Mac + iPhone using LW-Phone
- [ ] Cloud password (2FA) enabled, saved in 1Password
- [ ] Persona's bot created via @BotFather
- [ ] Bot token saved in 1Password as `LW-Telegram Bot Token`
- [ ] Bot description / about / pic set
- [ ] Operator chat ID saved in 1Password
- [ ] Smoke test: bot can send messages via API
- [ ] Smoke test: bot can issue Stars invoice
- [ ] Inline mode enabled, group joining disabled, privacy disabled

## All 9 boxes checked?

Drag to Done. Open **Page 09 — Twitter account creation**.""",
    },
]


# =============================================================
# PAGE 09 — Twitter setup
# =============================================================
page09_cards = [
    {
        "title": "81 — Pick the persona's Twitter handle + display name",
        "body": """## What to do

Decide on the persona's identity on Twitter. Document in 1Password under `LW-Persona Twitter identity`:

- **Handle** (`@username`): short, memorable, matches Telegram bot username pattern. E.g., `@lily_xo` or `@itslilybabe`.
- **Display name:** persona's stage name (e.g., `Lily 💋`)
- **Niche:** which audience (alt / gym / Latina / etc.) — should match your earlier persona-niche pick

### Handle availability check

In LatticeWorks Chrome profile (LOGGED OUT of any Twitter), go to https://x.com/<candidate_handle>.

- 404 page = available
- Profile shown = taken; try variants

Avoid:
- Numbers in handle (`lily123`) — looks scammy/AI
- Underscores at start/end (`_lily_`) — looks fake
- Trying to match an existing real OnlyFans creator's vibe too closely (risk of trademark/impersonation claims)

## Verification

Handle picked, available, documented.""",
    },
    {
        "title": "82 — Sign up new Twitter account",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://x.com → **Sign Up**.

- **Name:** persona's display name from Card 81
- **Email:** `twitter@latticeworks.<TLD>` (works via Migadu catch-all)
- **Date of birth:** persona's stated age — must be 18+. Pick a believable date (e.g., 22-30 range).
- Click Next

Twitter sends verification email — check Migadu inbox, click verify link.

## Verification

Account created, email verified.""",
    },
    {
        "title": "83 — Phone verify with LW-Phone",
        "body": """## What to do

Twitter will prompt for phone verification (sometimes immediately, sometimes after first post or first reply).

- Use `LW-Phone` from Page 01 Card 6 (MySudo recommended — Twitter is increasingly rejecting Google Voice)
- Enter the SMS code from MySudo

If Twitter rejects the number as VoIP:
- Try a real burner SIM (e.g., $20 prepaid SIM from Mint Mobile, Visible, or similar)
- Use the SIM in an old phone or via an eSIM in your existing iPhone (configure eSIM with a separate plan)

## Verification

Phone verified on Twitter.""",
    },
    {
        "title": "84 — Set the @handle and finalize username",
        "body": """## What to do

In Twitter → Profile → Edit Profile:
- Set @handle from Card 81
- Twitter sometimes auto-generates an ugly one — change it to your picked handle now

## Verification

Profile URL is `x.com/<your-picked-handle>`.""",
    },
    {
        "title": "85 — Set placeholder bio (NO NSFW yet, NO AI disclosure yet)",
        "body": """## What to do

Edit Profile → Bio.

**For the warmup phase (Page 10), the bio should be:**
- Innocuous: hobby, vibe, location-ish hints
- NO sexual language
- NO links yet (no Telegram, no OnlyFans, no Throne)
- NO `#AI` hashtag (that comes at Page 11 ACC enrollment)

Example for an alt-niche persona:
```
22 · NYC · coffee + cat ppl · 🖤
```

**Why no AI disclosure yet?** Twitter ACC requirements only apply once you start posting NSFW. During SFW warmup, you're just an account. ACC disclosure comes at Page 11.

## Verification

Bio set, vanilla, no NSFW signals.""",
    },
    {
        "title": "86 — Add placeholder profile pic and banner",
        "body": """## What to do

- **Profile pic:** use a generic abstract image (e.g., a sunset photo, a textured background, a non-face avatar). NOT a final persona image — those come post-ACC.
- **Banner:** similar — a generic vibey image.

You can generate placeholder images via:
- Existing stock photo sites (Unsplash, Pexels)
- DALL-E (sfw landscape) via your Anthropic API
- A solid color gradient via canva.com

## Why placeholders?

Twitter algorithms flag profile changes during warmup as suspicious. Better to start with clearly-placeholder branding and update to real persona content AFTER ACC approval.

## Verification

Profile pic and banner set. Both are SFW placeholders.""",
    },
    {
        "title": "87 — Enable 2FA on Twitter",
        "body": """## What to do

Settings → Security and account access → Security → Two-factor authentication.

- Choose **Authentication app** (NOT SMS — SMS 2FA is vulnerable to SIM swaps)
- Use 1Password's TOTP feature: in your `LW-Twitter account` item, add the OTP field by scanning Twitter's QR code

Save backup codes Twitter provides: in 1Password under `LW-Twitter account` → Secure Note.

## Verification

Logging out and back in requires 1Password TOTP code. Backup codes saved.""",
    },
    {
        "title": "88 — Configure email + notifications",
        "body": """## What to do

Settings → Notifications:
- Email notifications: ON (so signup/security alerts reach `me@latticeworks.<TLD>` via Migadu)
- Push notifications: OFF (you don't want phone buzzes for every like during automation)

Settings → Privacy and Safety:
- Protected mode: OFF (the persona needs to be discoverable)
- DM settings: Allow message requests from everyone (this is the inbox the bot will work)

## Verification

Settings configured for autonomous operation.""",
    },
    {
        "title": "89 — DO NOT post anything yet",
        "body": """## What to do

Resist the urge.

For the next 7-14 days (Page 10's warmup phase), the account will look slightly suspicious to Twitter:
- New account
- New IP (Hostwinds server, if you ever log in from there)
- New phone

If you post NSFW content in the first 24-48 hours, Twitter's automated systems will likely shadowban or suspend the account. Patience pays exponential dividends.

## What you CAN do today

- Follow 5-10 accounts in your niche (don't go crazy — 5-10 max in the first 24 hours)
- "Like" a few of their tweets (low-engagement signal)
- That's it. No tweets, no replies, no DMs sent.

## Verification

Account exists. Zero original tweets. Following ~5-10 niche-aligned accounts.""",
    },
    {
        "title": "90 — Final check before Page 10 (Twitter warmup)",
        "body": """## Confirm

- [ ] Twitter handle + display name picked + documented in 1Password
- [ ] Account created with `twitter@latticeworks.<TLD>` email
- [ ] Phone verified via LW-Phone
- [ ] Placeholder bio (SFW, no NSFW signals, no AI disclosure yet)
- [ ] Placeholder profile pic and banner (generic)
- [ ] 2FA enabled with authenticator app, backup codes in 1Password
- [ ] Email notifications ON to `me@latticeworks.<TLD>`
- [ ] DMs open to message requests
- [ ] Zero tweets posted. Following 5-10 niche accounts MAX.

## Why these matter for Page 10

Page 10 is the warmup phase — 7-14 days of SFW activity to age the account before ACC enrollment. Doing it from a non-clean baseline (premature NSFW, wrong settings) wastes the warmup.

## All 9 boxes checked?

Drag to Done. Open **Page 10 — Twitter warmup (7-14 days)**.""",
    },
]


# =============================================================
# PAGE 10 — Twitter warmup
# =============================================================
page10_cards = [
    {
        "title": "91 — Days 1-2: Set the lifestyle baseline",
        "body": """## What to do

You're inhabiting the persona. Twitter wants to see a HUMAN, not a bot.

**Day 1:**
- Post 1 SFW tweet (e.g., `coffee or no work today ☕`)
- Like 5-10 tweets from accounts you followed in Page 09 Card 89
- DO NOT reply to anyone yet

**Day 2:**
- Post 1-2 SFW tweets
- Like 10-15 tweets
- Reply to ONE tweet (something low-effort: "lol" or "saame")

## Why this pacing

New accounts that immediately spam are flagged. Real humans post sporadically and engage casually for the first few days as they "find their voice."

## Verification

Day 1-2: 1-2 tweets, casual likes, 1 reply. No NSFW. No automation.""",
    },
    {
        "title": "92 — Days 3-5: Grow engagement signal",
        "body": """## What to do

**Day 3-5:**
- 2-3 SFW tweets per day
- Reply to 3-5 tweets per day (real, substantive replies — "your cat is gorgeous omg" not "🔥🔥🔥")
- Follow 5-10 more niche accounts per day (continue growing your follow graph)
- Quote-tweet 1 tweet per day with a real opinion

## Posting content ideas (still SFW)

- Outfit posts (clothed, with vibe descriptors)
- Aesthetic photos (room, coffee shop, sunset, etc.)
- Hot-take tweets (e.g., for an alt-niche persona: `tattoos > piercings dont @ me`)
- Engagement bait (e.g., `last person you dmd, post their pfp` — this gets replies fast)

## Anti-pattern

Don't post a selfie yet. New accounts posting their first selfie within 5 days look like AI personas. Hold selfies for Day 6+.

## Verification

By end of Day 5: ~10-15 tweets, ~20-30 replies, ~50-100 likes, following ~30-50 accounts.""",
    },
    {
        "title": "93 — Day 6: First selfie",
        "body": """## What to do

Day 6 is when you can post a first persona "selfie" — but it should be:
- A SFW selfie from your persona's reference library (the image set you'll train the IPAdapter on — see your earlier architecture discussions)
- Slightly imperfect (a tiny blur, an off-center crop, "candid" feel) — looks real, not AI-perfect
- Innocuous caption (`finally a no-makeup day`, `cant sleep`, etc.)

## Why Day 6 specifically

Long enough for the account to feel established (8-12 tweets of personality before the first face reveal). Short enough that audience is still curious.

## Verification

First selfie posted. Caption is casual. Photo is SFW.""",
    },
    {
        "title": "94 — Days 7-10: Ramp posting cadence",
        "body": """## What to do

**Day 7-10:**
- 3-4 SFW tweets per day
- 5-8 replies per day
- Post 1 additional SFW selfie per day (variety of poses, settings — but ALL SFW)
- Start using niche hashtags (e.g., for an alt-niche persona: `#altgirl #alternative #gothicstyle`) on 30-50% of posts

## Hashtag strategy

Goal: discoverability without looking spammy.

- 2-3 niche hashtags per tweet, NOT 10+
- Mix specific niche tags with broader ones (e.g., `#altgirl` + `#nyc`)
- Don't use `#nsfw` or any explicit-signal tags yet — that's post-ACC behavior

## Verification

Days 7-10: 12-16 more tweets posted. Engagement starting to compound (likes, replies, follows incoming).""",
    },
    {
        "title": "95 — Day 10: Audit account health",
        "body": """## What to do

Around Day 10, check for signs of shadowban or restriction:

### Visibility test
- Search Twitter for one of your tweets exactly — does it appear in search results?
- If yes: good signal
- If no after 24 hours: possible shadowban

### Impressions test
- Your tweets should be getting 50-300+ impressions each (visible in Twitter analytics)
- If impressions are flat-lining at 0-20: possible shadowban

### DM test
- Send yourself a test DM from a separate (real) Twitter account
- Does it land in inbox or message requests?
- If neither arrives: possible DM restriction

### Algorithmic surface test
- Search a niche keyword you'd want to be found for
- Scroll through the "People" tab — do you appear?
- If never, even after 30 min of scrolling: you're not in the algorithmic graph yet

## What to do if shadowbanned

Don't panic. New accounts often get auto-restricted by Twitter's spam systems.
- Stop posting for 24-48 hours
- Reduce reply frequency
- Wait 3-7 days, recheck

## Verification

Account health checked. Document findings in 1Password under `LW-Twitter warmup audit Day 10`.""",
    },
    {
        "title": "96 — Days 11-14: Higher engagement",
        "body": """## What to do

Final days of warmup.

**Day 11-14:**
- 4-5 SFW tweets per day
- 10-15 replies per day, including replies to bigger accounts (10K+ followers) where appropriate
- 1-2 selfies per day, slightly more curated
- Begin liking adult-creator accounts (NOT NSFW posts yet — just their SFW posts)

## Why "begin liking adult-creator accounts"

Twitter's recommendation engine looks at WHO you engage with. Liking adult creators' SFW posts signals to Twitter "this account is interested in this content niche" — which improves your post visibility to that audience LATER (once you're posting NSFW yourself).

## Anti-pattern

Don't follow 100 NSFW accounts in one sitting. Add 5-10 per day. Looking organic matters.

## Verification

Days 11-14: 16-20 more tweets, 40-60 replies, organic engagement growth.""",
    },
    {
        "title": "97 — Day 13-14: Build out the link-tree",
        "body": """## What to do

Before ACC enrollment in Page 11, you need a "link in bio" landing page. Options:

### Option A — Custom one-page site (recommended)
- Subdomain on your domain: e.g., `links.latticeworks.<TLD>` — hosted on the Hostwinds box
- Simple HTML page: persona pic, 3-4 buttons (Telegram, OnlyFans/Fansly if applicable, Throne wishlist, NowPayments tip link)
- Plus AI disclosure at the bottom

### Option B — Bento.me or similar
- Free, no setup
- Risk: Bento can ban adult creators

### Option C — Linktree
- DON'T USE. Linktree explicitly bans adult content.

**Recommendation:** Option A. Spin up a basic page on your Hostwinds box (Nginx + a static index.html).

Save the URL in 1Password under `LW-Persona link in bio`.

## Verification

You have a link-in-bio URL ready to drop into Twitter bio at ACC enrollment (Page 11).""",
    },
    {
        "title": "98 — Day 14: Verify ACC eligibility",
        "body": """## What to do

Twitter's Adult Content Creator (ACC) program has eligibility requirements. Confirm yours:

- [ ] Account is at least 14 days old (you'll just hit this on Day 14)
- [ ] No suspensions or violations in account history (yours has none — clean signup)
- [ ] Active engagement (you have 14 days of organic content)
- [ ] Phone verified (Page 09 Card 83)
- [ ] Email verified (Page 09 Card 82)
- [ ] You can provide a government-issued ID for KYC (yes, real ID under operator name)
- [ ] You can provide tax documents (W-9 if 1099, or LLC docs)

If any are missing, fix before Page 11.

## Verification

All 7 boxes checked. You're eligible to apply for ACC.""",
    },
    {
        "title": "99 — Document warmup observations",
        "body": """## What to do

Before moving on, capture lessons from the warmup phase. In 1Password under `LW-Twitter warmup observations`:

- Which types of posts got most engagement?
- Which hashtags drove most discovery?
- How fast did followers come in (per day)?
- Any restriction signals you noticed and how you handled them?

## Why this matters

When you scale to multiple personas later, the warmup learnings from persona #1 are gold. Document them now while fresh.

## Verification

Notes captured in 1Password.""",
    },
    {
        "title": "100 — Final check before Page 11 (ACC enrollment)",
        "body": """## Confirm

- [ ] Account has 14 days of SFW activity (posts, replies, follows)
- [ ] No shadowban / restriction signals
- [ ] Phone + email verified, 2FA enabled
- [ ] Link-in-bio URL ready (on your domain, not Linktree)
- [ ] Government ID + tax documents ready for KYC
- [ ] You can produce a real photo of the operator (yourself) holding ID for ACC verification
- [ ] Warmup observations documented in 1Password

## All 7 boxes checked?

Drag to Done. Open **Page 11 — Twitter ACC enrollment**.""",
    },
]


# =============================================================
# PAGE 11 — Twitter ACC enrollment
# =============================================================
page11_cards = [
    {
        "title": "101 — Open the ACC application in Twitter settings",
        "body": """## What to do

In LatticeWorks Chrome profile, log into the persona's Twitter account.

Navigate to:
- Settings → Monetization
- Look for **Adult Content Creator** (or "Creator Subscriptions" with an adult tier)

If you can't find it:
- ACC enrollment is sometimes invite-only or rolled out by region/tier
- Apply via the public form: https://help.x.com/en/forms/account-access/regain-access/adult-content-creator-application (URL may update — search "twitter ACC application")

## Verification

ACC application form is open in your browser.""",
    },
    {
        "title": "102 — Submit identity verification (YOUR ID)",
        "body": """## What to do

The ACC program requires VERIFIED IDENTITY of the account operator. This means YOUR real ID, not the persona's.

Upload:
- **Government-issued photo ID** (US driver's license, passport, or state ID)
- **Selfie holding the ID** (Twitter will prompt with overlay guides)

Make sure:
- ID is clear, all corners visible
- Selfie shows your face + ID readable
- Lighting is good

## Why your real ID

ACC is the platform's KYC for adult creators. They need a real human accountable. Your real identity is on the BACK END (creator program records). The FRONT END (persona's profile) is still anonymous — followers see the persona's stage name, not your real name.

## Verification

ID + selfie submitted. ACC dashboard shows verification status `Pending`.""",
    },
    {
        "title": "103 — Submit tax documents",
        "body": """## What to do

Per your decision in Page 01 Card 7:

### If you chose Option A (UpfrontOps LLC):
- W-9 with UpfrontOps LLC name + EIN
- LLC formation document

### If you chose Option B (new LLC):
- W-9 with new LLC name + EIN
- LLC formation document
- Best if you formed the LLC during Pages 02-10 in parallel

### If you chose Option C (1099 personal):
- W-9 with your personal name + SSN
- This ties adult-creator income directly to your personal name on Twitter's records

Upload the appropriate documents via the ACC application.

## Why now

Without tax docs, Twitter can't pay you for ACC revenue share (creator subscriptions, gated content, etc.). And they require it before approval, not after.

## Verification

Tax docs uploaded. ACC dashboard reflects.""",
    },
    {
        "title": "104 — Set content sensitivity tier",
        "body": """## What to do

ACC has two tiers:
- **Adult** — nudity, suggestive content, sexual themes (less restrictive)
- **Explicit** — actual sexual acts, hardcore content (most restrictive labeling)

For a synthetic AI persona doing tip-based + custom photos model:
- Most content fits **Adult** tier
- Reserve Explicit for hardcore custom videos (Page 12 voice + advanced content)

Pick Adult for now. You can request Explicit later if needed.

## Verification

Sensitivity tier set to Adult.""",
    },
    {
        "title": "105 — Update bio with AI disclosure (per ACC policy)",
        "body": """## What to do

ACC requires clear AI disclosure for AI-generated personas.

Update your Twitter bio (Profile → Edit Profile → Bio):

**Format that complies with ACC but preserves the fiction:**

Example for an alt-niche persona:
```
22 · NYC · alt baddie · AI 💋 still treat me like the real thing tho · 🔗 [link-in-bio URL]
```

**Required elements:**
- The word "AI" must be visible in bio (not hidden in collapsed section)
- A `#AI` hashtag pattern in posts is required by ACC (you'll add this in Card 107)

**Optional:** the link in bio (from Page 10 Card 97) goes here.

## Verification

Bio updated, AI disclosure present, link active.""",
    },
    {
        "title": "106 — Configure profile for adult content",
        "body": """## What to do

Settings → Privacy and Safety → Your posts:
- **Sensitivity Settings:** Mark your media as containing sensitive content (default ON for all posts)

Settings → Privacy and Safety → Discoverability:
- **Discoverable by phone:** OFF (don't let LW-Phone unmask)
- **Discoverable by email:** OFF (don't let Migadu address leak)

Settings → Privacy and Safety → Audience and tagging:
- **Protect your posts:** OFF (you want public discoverability)
- **Photo tagging:** Off or Only people I follow (prevents harassment via tagging)

## Verification

Settings configured for adult creator with sensible privacy.""",
    },
    {
        "title": "107 — Set up posting templates with required hashtags",
        "body": """## What to do

ACC requires AI-generated content to be tagged. The pattern (as of 2026):
- Every NSFW post should include `#AI` or `#Generated` hashtag
- Caption should mention "AI" once at the start of more explicit content

Document your standard posting template in 1Password under `LW-Posting templates`:

**Template A — selfie / softcore:**
```
[caption text]

#alt #nyc #AI
```

**Template B — explicit / hardcore (once Explicit tier approved):**
```
[caption text] — AI persona ✨

#AI #Generated
```

You'll use these in the bot's posting logic later.

## Verification

Templates documented for future bot use.""",
    },
    {
        "title": "108 — Submit application + wait for review",
        "body": """## What to do

In ACC dashboard, click **Submit** (final step).

Review timeline:
- Typical: 24-72 hours
- Sometimes: 5-7 days during high-volume periods
- Rarely: over 2 weeks (in which case email Twitter support)

While waiting:
- DO NOT post NSFW content
- DO continue SFW posting at warmup pace (3-5 posts/day, replies, etc.) to keep the account "alive"
- DO NOT switch to bot automation yet

## Verification

Application submitted. Status `Under review`.""",
    },
    {
        "title": "109 — On approval: enable monetization features",
        "body": """## What to do

When ACC approval email arrives at `me@latticeworks.<TLD>`:

In Twitter Monetization settings:
- Enable Creator Subscriptions (if you want a subscription tier — most LatticeWorks personas skip this, doing tips + customs instead)
- Enable Tips (Twitter's native tip feature)
- Verify Adult-tier posting capabilities active

Update bio one more time to reflect monetization (e.g., link to your tip link from NowPayments + Telegram bot link).

## What to NOT enable

- Twitter "Verified" (blue check) — you don't need it for ACC, and it adds friction
- Twitter Ads — irrelevant for this model

## Verification

ACC monetization features enabled. Bio reflects active operation.""",
    },
    {
        "title": "110 — Final check before Page 12 (voice + smoke test)",
        "body": """## Confirm

- [ ] ACC application submitted and approved
- [ ] Identity verified (your real ID + selfie)
- [ ] Tax documents submitted matching your tax structure decision
- [ ] Sensitivity tier set to Adult
- [ ] AI disclosure in bio
- [ ] Adult content sensitivity setting ON
- [ ] Posting templates documented for future bot use
- [ ] Monetization features (tips, etc.) enabled

## All 8 boxes checked?

Drag to Done. Open **Page 12 — Voice + final smoke test**.""",
    },
]


# =============================================================
# PAGE 12 — Voice + final smoke test
# =============================================================
page12_cards = [
    {
        "title": "111 — Sign up ElevenLabs Creator tier",
        "body": """## What to do

In LatticeWorks Chrome profile, go to https://elevenlabs.io.

- Sign Up with `eleven@latticeworks.<TLD>`
- Choose **Creator plan** ($22/mo) — unlocks Professional Voice Cloning
- Save login to `LW-ElevenLabs account` in 1Password

## Why Creator (not Starter)

- Starter ($5/mo) only has Instant Voice Clone (lower quality, won't match persona consistency)
- Creator ($22/mo) has Professional Voice Clone (trained on 30+ seconds, much higher fidelity)

For a "feels real" persona experience, Creator is the floor.

## Verification

Account active on Creator tier.""",
    },
    {
        "title": "112 — Pay with Privacy.com card",
        "body": """## What to do

Create Privacy.com card: `LW-ElevenLabs`, lock to `elevenlabs.io`, $50/mo limit.

Save to `LW-ElevenLabs virtual card` in 1Password.

Pay the $22/mo plan with this card.

## Verification

Subscription active.""",
    },
    {
        "title": "113 — Source reference audio for voice clone",
        "body": """## What to do

Professional Voice Cloning needs 30+ seconds (ideally 1-2 minutes) of clean reference audio.

**Sources for the persona's voice:**

### Option A — Generate via TTS (zero-shot)
- Use OpenAI's TTS API or similar to generate ~60 sec of clean speech in a voice you like
- Save as `.mp3` or `.wav`
- This becomes the reference for ElevenLabs

### Option B — Record an existing voice actor
- Hire a voice actor on Fiverr (~$30-80) for 1-2 min of read-out clean audio
- Get rights to use as AI voice reference (specify in the contract)

### Option C — Sample from public domain / royalty-free
- Use clean podcast audio from CC0 / royalty-free sources
- More complex from a "consistent persona voice" angle

**Recommendation: Option B.** Voice actors give you a unique, ownable voice with proper rights. ~$50 well spent.

## Verification

You have a 30+ sec audio file ready to upload to ElevenLabs.""",
    },
    {
        "title": "114 — Train the persona's voice clone in ElevenLabs",
        "body": """## What to do

In ElevenLabs → Voices → Add Voice → **Professional Voice Clone**.

- **Name:** persona's stage name (e.g., `Lily`)
- **Description:** "AI persona voice for LatticeWorks"
- Upload your reference audio file from Card 113
- Click Create

Training takes 2-5 minutes.

## Verification

Voice clone available in your Voices list. Generate a test phrase to confirm.""",
    },
    {
        "title": "115 — Test voice quality",
        "body": """## What to do

In ElevenLabs → Voices → click your persona's voice → Generate.

Test phrases (try 3-5):
- "Hi babe, just thinking about you 💋"
- "want to see what i'm doing right now?"
- "tip me $30 and i'll send you something special"

Listen on headphones. Check for:
- Does it match the persona's "feel" (age, accent, vibe)?
- Any robotic / glitchy moments?
- Pacing natural?

If it sounds off:
- Re-upload with cleaner reference audio
- Adjust stability + similarity settings

## Verification

Voice sounds natural and matches the persona's vibe.""",
    },
    {
        "title": "116 — Get ElevenLabs API key",
        "body": """## What to do

ElevenLabs → Profile → API Key.

Copy the key (long string starting with `sk_...`).

Save in 1Password as `LW-ElevenLabs API key`.

Test from your Hostwinds server:

```
LW_EL_KEY="your_key"
LW_VOICE_ID="your_voice_id"  # from the voice page URL

curl --request POST \\
  --url "https://api.elevenlabs.io/v1/text-to-speech/${LW_VOICE_ID}" \\
  --header "xi-api-key: ${LW_EL_KEY}" \\
  --header "Content-Type: application/json" \\
  --data '{"text":"hey baby","model_id":"eleven_multilingual_v2"}' \\
  --output /tmp/test.mp3

# Play it
afplay /tmp/test.mp3
```

(Or copy to Mac and play.)

## Verification

API call returns audio. Plays cleanly.""",
    },
    {
        "title": "117 — Full pipeline smoke test: Twitter → Telegram → payment",
        "body": """## What to do

Do an end-to-end smoke test simulating a real customer journey.

### Step 1 — Twitter side
From your operator account (or a friend's), DM the persona's Twitter account.
Send: `hi cutie`

### Step 2 — Telegram bridge (you do this manually for now; the bot will automate later)
From the persona's Twitter account, reply: `hey 💋 come find me on telegram, that's where i play → [bot deep-link]`

The deep-link format is: `https://t.me/<your_bot_username>?start=test_user_001`

### Step 3 — Telegram conversation
The "customer" (you) clicks the link → opens Telegram → starts the bot.
- The bot doesn't reply yet (no code yet)
- But the chat is established

### Step 4 — Manually issue a Stars invoice
From your Hostwinds server, send a Stars invoice to the customer chat (use the curl from Page 08 Card 78).

### Step 5 — Customer pays
You (as customer) click "Pay 1 Star" → enter PIN → confirm

### Step 6 — Confirm receipt
In Telegram bot owner view, you should see Stars balance increment by 1.

## Verification

End-to-end customer journey works manually. The bot code will automate this; the plumbing is proven.""",
    },
    {
        "title": "118 — Final pipeline smoke test: content generation",
        "body": """## What to do

Now that the infra is up, do one final smoke test of the CONTENT path.

### Step 1 — Generate one image (via RunPod)
SSH into Hostwinds. Start a ComfyUI pod on RunPod with Flux + AIDMA NSFW Unlock LoRA.

(Detailed ComfyUI workflow setup will happen in build phase 2 — for now just verify a pod with Flux can start and generate one test image.)

### Step 2 — Upload to B2
```
b2 file upload lw-content-prod /tmp/test.png test/smoke.png
```

### Step 3 — Serve via Bunny
Open `https://lw-content.b-cdn.net/test/smoke.png` — image renders.

### Step 4 — Send via Telegram
```
curl "https://api.telegram.org/bot${LW_BOT_TOKEN}/sendPhoto" \\
  -d "chat_id=${LW_CHAT_ID}" \\
  -d "photo=https://lw-content.b-cdn.net/test/smoke.png"
```

Image arrives in Telegram chat.

## Verification

Full content path works end-to-end: generate → store → CDN → deliver.""",
    },
    {
        "title": "119 — Backup audit + 1Password export rehearsal",
        "body": """## What to do

Before declaring setup complete, verify the handoff mechanism works.

### Export 1Password vault test
- 1Password → LatticeWorks vault → ... menu → Export → 1Password Unencrypted Format (1pux) or CSV
- Save to your Mac temporarily as `latticeworks-vault-test-export.1pux`
- Open it (with 1Password's import tool) into a TEST vault to verify export integrity
- Delete the test export and test vault immediately

### Verify backup of seed phrase locations
- Confirm your hardware-wallet seed phrase (Page 07 Card 63) is in BOTH physical locations
- Confirm 1Password split-saved seeds (words 1-6, 7-12) are still intact

### Document the handoff process
In 1Password under `LW-Handoff playbook`:
- "To hand off to client: export this vault as 1pux → send via Signal or secure file transfer → recipient imports."
- "Then change all credentials" (passwords, API keys) AFTER handoff, so old exports become useless.

## Verification

You can export the vault successfully. Backup integrity confirmed.""",
    },
    {
        "title": "120 — Setup complete. You're ready to build.",
        "body": """## Final checklist

- [ ] All previous 119 microsteps completed
- [ ] Every vendor account active and credentials in 1Password
- [ ] Domain + email working
- [ ] Server provisioned + hardened
- [ ] All APIs (Claude, OpenRouter, ElevenLabs, etc.) tested with smoke tests
- [ ] NowPayments + crypto wallet tested with $1 transaction
- [ ] Telegram bot created + responding to API calls
- [ ] Twitter persona warmed (14 days SFW) + ACC enrolled and approved
- [ ] Voice clone trained + voice quality verified
- [ ] End-to-end pipeline smoke tested: Twitter → Telegram → payment
- [ ] End-to-end content pipeline smoke tested: gen → B2 → Bunny → Telegram
- [ ] 1Password export rehearsed (handoff mechanism verified)

## What's next (outside this setup playbook)

This page completes the **setup phase** — every account and account-to-account pipe exists, smoke-tested.

The **build phase** is separate:
- Wire the orchestration code (Claude API as brain)
- Build the conversational layer (OpenRouter for explicit chat)
- Build the content generation pipeline (ComfyUI workflows on RunPod)
- Build the Twitter posting + reply-guy bot
- Build the Telegram chat handler with memory + customer profiling
- Build the shoutout management module
- Wire detection-evasion post-processing
- Wire payment-handling + custom-request flow

That's ~9-13 weeks of engineering work, separate from this playbook.

## All boxes checked?

Drag this card to Done. The LatticeWorks setup is complete.

Welcome to the build phase. 🎯""",
    },
]


# =============================================================
# Execute build for all pages
# =============================================================
pages = [
    (2, "Register your domain", "**Goal:** Own the domain that everything hangs off — email, server, persona link-in-bio. ~30 minutes. Requires Page 01 complete (Privacy.com card + throwaway Gmail).", page02_cards, 11),
    (3, "Set up email at Migadu + DNS", "**Goal:** Get `me@latticeworks.<TLD>` live so we stop using throwaway Gmail. ~45 minutes + DNS wait. Requires Page 02 complete (domain registered).", page03_cards, 21),
    (4, "Provision Hostwinds dedicated box", "**Goal:** Stand up the production server where orchestration / Postgres / bots will run. ~2 hours + provisioning wait. Requires Page 03 complete (you'll use `hostwinds@latticeworks.<TLD>`).", page04_cards, 31),
    (5, "RunPod + storage + CDN", "**Goal:** Set up GPU compute (RunPod), object storage (Backblaze B2), and CDN (BunnyCDN). ~90 minutes. Requires Page 04 complete (server exists for SSH testing).", page05_cards, 41),
    (6, "AI APIs (Claude + OpenRouter + Postmark)", "**Goal:** Get all the AI-side API keys configured and smoke-tested. ~1 hour. Requires Page 03 complete (email anchor).", page06_cards, 51),
    (7, "NowPayments + crypto wallet", "**Goal:** Set up the payment processor (NowPayments merchant account) + crypto wallet that receives payouts. Includes 1-3 day KYC wait. Requires Page 03 complete.", page07_cards, 61),
    (8, "Telegram setup", "**Goal:** Create the persona's Telegram account + bot, and prove the bot can send messages + Stars invoices via API. ~1 hour. Requires Page 01 complete (LW-Phone).", page08_cards, 71),
    (9, "Twitter account creation", "**Goal:** Create a fresh Twitter account for the persona, ready to begin warmup. **No NSFW yet.** ~30 minutes. Requires Page 03 (email) + Page 01 (phone).", page09_cards, 81),
    (10, "Twitter warmup (7-14 days)", "**Goal:** Age the new Twitter account with 14 days of SFW activity before ACC enrollment. This page spans ~2 weeks — daily small actions, not one sitting.", page10_cards, 91),
    (11, "Twitter ACC enrollment", "**Goal:** Apply to and get approved for Twitter's Adult Content Creator program. Includes 1-7 day review. Requires Page 10 complete (14-day warmup).", page11_cards, 101),
    (12, "Voice + final smoke test", "**Goal:** Train the persona's voice clone in ElevenLabs and verify all end-to-end pipelines. ~2 hours + voice training time. Requires all prior pages complete.", page12_cards, 111),
]

results = {}
for num, title, intro, cards, start_step in pages:
    result = build_page(num, title, intro, cards, start_step)
    results[f"page_{num:02d}"] = {
        "title": f"Page {num:02d} — {title}",
        "doc_id": result["doc_id"],
        "collection_id": result["collection_id"],
    }

# Save IDs
IDS["pages"].update(results)
IDS_FILE.write_text(json.dumps(IDS, indent=2))

print()
print("=" * 60)
print("ALL 11 PAGES BUILT")
print("=" * 60)
for k, v in results.items():
    print(f"  {v['title']} (doc {v['doc_id'][:8]}...)")
print()
print("Total: 110 cards across 11 pages.")
print("Each page: 10 microsteps with rich card bodies.")
print("Step numbering: continuous 11-120.")
