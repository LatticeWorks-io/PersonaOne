<page id="16758d07-a2ac-f7ab-00c6-96e37e212d5b">
  <pageTitle>Page 01 — Set up isolated workspace</pageTitle>
  <content>
    # Page 01 — Set up isolated workspace
    
    **Goal:** Create a clean dev surface for the LatticeWorks project, fully isolated from your UpfrontOps / personal stack.
    
    **Time:** ~30 minutes.
    
    **Why this page exists:** You can't sign up for vendors without virtual cards, a clean browser, a fresh email anchor, and a phone number that doesn't trace back to UpfrontOps. This page sets all of that up.
    
    **You can't open Page 02 until every card below is in Done.**
    
    ***
    
    Switch the kanban below to **Board view** (collection's `...` menu → View → Kanban). Then work the cards left-to-right.
    
    <collection>
      <title>Page 01 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">10</property>
          <title>10 — Final verification + open Page 02</title>
          <content>
            ## Confirm all of these are true
            
            - [ ] LatticeWorks Chrome profile exists on Mac, pinned, signed out of Google, sterile
            - [ ] LatticeWorks Chrome profile created on iPhone (matches desktop pattern)
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
            
            If any box above is unchecked, Page 02 will dead-end on you. Finish them all first.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">9</property>
          <title>9 — Sterilize the LatticeWorks Chrome profile</title>
          <content>
            ## What to do
            
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
            
            You opened all six chrome:// settings listed above and confirmed each was empty. The only extension is 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">4</property>
          <title>4 — Create throwaway Gmail for bootstrap signups</title>
          <content>
            ## What to do
            
            In the LatticeWorks Chrome profile (Mac), go to [https://accounts.google.com](https://accounts.google.com) → **Create account** → For my personal use.
            
            - **Username:** `latticeworks.dev@gmail.com` (or `latticeworks.setup@gmail.com` or variant if taken)
            - **Phone verification:** use your real personal phone for the SMS code (one-time use; Google won't link it to anything else automatically)
            - **Recovery email:** skip
            - **Save** the login in 1Password under `LW-Gmail (bootstrap)`
            
            ## Why this comes early (Card 4, not Card 8)
            
            This Gmail is the **bootstrap email for everything else in Pages 01-03**. Specifically:
            
            - **Card 5 (burner phone, Google Voice option)** — Google Voice requires a Gmail. (MySudo doesn't.)
            - **Card 6 (Privacy.com)** — Privacy.com signup requires an email. You don't want to use your personal/UpfrontOps email for this.
            - **Page 02 (Porkbun)** — domain registration requires email.
            - **Page 03 (Migadu)** — email host signup requires an existing email.
            
            Without this Gmail in place first, every subsequent signup in Pages 01-03 dead-ends.
            
            ## Why not just use your UpfrontOps email?
            
            You could — Privacy.com / Porkbun / Migadu don't know what you're using the accounts for. But the discipline of isolation means every LatticeWorks-related signup uses LatticeWorks-isolated identity. Using your real email leaks ownership records that connect LatticeWorks vendors to UpfrontOps.
            
            ## Why a throwaway Gmail (and not Proton/Tuta)
            
            Porkbun, Migadu, and other registrars occasionally flag freshly-created Tutanota/Proton accounts as fraud risk. Gmail at signup has the lowest friction. Use it for THIS bootstrap purpose only — it becomes dormant once `me@latticeworks.io` is live in Page 04.
            
            ## Verification
            
            You can log into the throwaway Gmail in your LatticeWorks Chrome profile. Login is in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">8</property>
          <title>8 — Decide tax structure for this engagement</title>
          <content>
            ## What to do
            
            This is a **decision**, not a signup. You don't form anything new yet — you just commit to a path so you know how to set up the next pages.
            
            You have UpfrontOps LLC already. Three options:
            
            | Option | Pros | Cons |
            | --- | --- | --- |
            | **A. Flow revenue through UpfrontOps LLC** | Simplest. Clean tax filing. Reuses existing bank account. | UpfrontOps' books show adult-industry revenue (only visible to your accountant, IRS, and you, but still). |
            | **B. Form new LLC just for LatticeWorks** | Cleanest isolation. UpfrontOps stays squeaky. Best liability separation. | ~$200-500 setup + annual fees. New EIN, new bank account, takes 1-2 weeks. |
            | **C. 1099 personal income** | Zero setup. | No LLC liability protection. Adult work tied directly to your personal name on tax filings. |
            
            **Recommendation:** A or B depending on how much adult-industry exposure you want on UpfrontOps' books. If client is paying $5-10K/mo, B starts to pay for itself in liability terms.
            
            ## Write the decision in 1Password
            
            Open 1Password → LatticeWorks vault → **+ New Item** → Secure Note → title `LW-Tax structure`.
            
            Write: `Option chosen: A/B/C`. If B, also write: `Action: form WY/DE LLC by [date]`.
            
            ## Why this matters
            
            Pages 04 (NowPayments KYC) and 11 (Twitter ACC enrollment) both ask for tax / business identity. If you're going B (new LLC), you need to form it BEFORE those pages, which means starting now in parallel.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">5</property>
          <title>5 — Get a burner phone number</title>
          <content>
            ## What to do
            
            Pick **ONE** of these (recommendation: MySudo since Twitter has been increasingly rejecting Google Voice as VoIP):
            
            ### Option A — MySudo (recommended)
            
            You've used MySudo before. Open the app → create a new **Sudo persona** named `LatticeWorks` → assign it a new phone number ($5/mo plan if you need a fresh paid number).
            
            ### Option B — Google Voice
            
            In the LatticeWorks Chrome profile (Mac), signed into the throwaway Gmail from Card 4: [https://voice.google.com](https://voice.google.com) → claim a US number with an area code that isn't yours.
            
            ### Either way
            
            Save the number in 1Password under `LW-Phone`.
            
            ## Why this comes before Privacy.com
            
            Privacy.com may ask for phone verification during signup. Having the burner number ready means you don't have to interrupt the Privacy.com flow.
            
            ## Why this matters more broadly
            
            You'll use this number for Telegram signup (Page 08), Twitter signup (Page 09), and any other vendor that requires SMS verification. Critically: **Twitter ACC enrollment** (Page 11) requires a real, working phone number. Google Voice numbers get rejected at ACC enrollment with rising frequency in 2026.
            
            ## Verification
            
            You have a phone number. It can receive SMS. It's saved in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">7</property>
          <title>7 — Create your first test virtual card</title>
          <content>
            ## What to do
            
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
            
            Card appears in your Privacy.com dashboard with status `Active`. Card details copied to 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">6</property>
          <title>6 — Sign up Privacy.com (or confirm existing access)</title>
          <content>
            ## What to do
            
            **If you already use Privacy.com** for other UpfrontOps work:
            
            - Log in (via your LatticeWorks Chrome profile)
            - Create a Group or use a card-name convention like `LW-<vendor>` to keep LatticeWorks cards separate from other clients
            - Skip to Card 7 (you already have virtual card capability)
            
            **If you don't have Privacy.com:**
            
            - Go to [https://privacy.com](https://privacy.com) (in LatticeWorks Chrome profile) → Sign up
            - **Email:** use the **throwaway Gmail** from Card 4 (`latticeworks.dev@gmail.com` or whatever variant you used)
            - **Phone verification:** use `LW-Phone` from Card 5 (MySudo or Google Voice)
            - **KYC:** SSN last 4 + your name — Privacy.com is a legitimate financial service and needs this for regulatory reasons. Doesn't leak to vendors.
            - Link your existing personal or business checking account (Privacy.com only sees balance, not transaction history)
            
            Save your Privacy.com login in 1Password under `LW-Privacy.com`.
            
            ## Why virtual cards are required
            
            Every subsequent signup (Hostwinds, RunPod, Migadu, Porkbun, etc.) gets paid with a Privacy.com-issued merchant-locked virtual card. Reasons:
            
            - Each vendor gets a unique card → if one vendor's database is breached, only that one card is exposed
            - Spend limits enforce hard caps → no surprise overcharges
            - Charge-back leverage → if a vendor goes bad, you can pause the card without canceling your real card
            
            ## Verification
            
            You can land on Privacy.com dashboard with a "Create New Card" button visible. Don't create one yet — Card 7 covers the smoke test.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Done</property>
          <property name="step">3</property>
          <title>3 — Create LatticeWorks vault in 1Password</title>
          <content>
            ## What to do
            
            Open 1Password (you already have it). In the sidebar → click **+** next to Vaults → **New Vault**.
            
            - **Name:** `LatticeWorks`
            - **Description:** `All credentials for the LatticeWorks project. Will be exported and handed off.`
            - Color: pick one you don't use elsewhere
            
            Then in the LatticeWorks Chrome profile:
            
            - Go to [https://1password.com/downloads/browser](https://1password.com/downloads/browser) → install the 1Password extension
            - Sign in with your existing 1Password account
            - In the extension settings → set **Default vault** to `LatticeWorks`
            
            ## Why this matters
            
            This vault is the deed of sale at handoff. Every credential for every LatticeWorks vendor account goes here — and **nothing else** goes here. When you hand the project off to the client, you export this one vault and they have everything.
            
            ## Verification
            
            In the LatticeWorks Chrome profile, click the 1Password extension icon → confirm the active vault is `LatticeWorks`. New items saved from this profile should land in this vault by default.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Done</property>
          <property name="step">2</property>
          <title>2 — Create LatticeWorks Chrome profile on iPhone</title>
          <content>
            
            
            ## What to do
            
            On your iPhone, open Chrome (if you don't have it: App Store → Chrome → install).
            
            - Tap your profile circle (top right of Chrome) → **Add another account** OR scroll to the profile picker
            - Create a NEW profile named `LatticeWorks` matching your desktop profile name
            - Pick a distinct color/icon (matching your desktop choice ideally)
            - **SKIP** "Sign in" — leave this profile signed out of any Google account
            
            To switch profiles fast:
            
            - Add a Chrome icon shortcut to your iPhone home screen for the LatticeWorks profile (long-press Chrome → Add to Home Screen if available, or just remember which profile you're in via the colored profile icon)
            
            ## Why Chrome profile (not Brave, not Safari)
            
            - **Consistency with desktop:** same browser brand, same mental model, profile switching works the same way
            - **Profile isolation on iOS Chrome got good in 2024-2025:** separate cookies, sessions, autofill, sync — meaningfully isolated from your personal Chrome profile
            - **No need for a separate browser app:** less mental overhead, fewer apps to maintain
            
            ## Important — keep these separate
            
            - The LatticeWorks Chrome profile on iPhone must NOT sync to your personal Google account
            - Don't reuse passwords from your personal profile (1Password handles this for you anyway)
            - If you have iCloud Keychain enabled, it does NOT cross-contaminate Chrome — Chrome's password manager is separate from Keychain
            
            ## Verification
            
            - Open Chrome on iPhone, switch to LatticeWorks profile
            - Confirm: no bookmarks, no autofill addresses, no signed-in Google account, no saved passwords from your personal profile
            - Profile shows the LatticeWorks color/icon you chose
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Done</property>
          <property name="step">1</property>
          <title>1 — Create LatticeWorks Chrome profile (Mac)</title>
          <content>
            ## What to do
            
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
            
            If anything got auto-imported from your other profiles, delete it now. Treat this profile as a quarantine.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
