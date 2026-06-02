<page id="d7aa9d6a-7fb2-aad1-6ffb-36fc80eb1aef">
  <pageTitle>Page 02 — Register your domain</pageTitle>
  <content>
    # Page 02 — Register your domain
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Own the domain that everything hangs off — email, server, persona link-in-bio. ~30 minutes. Requires Page 01 complete (Privacy.com card + throwaway Gmail).
    
    <collection>
      <title>Page 02 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">20</property>
          <title>20 — Final check before Page 03</title>
          <content>
            ## Confirm all of these are true
            
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
            
            Drag this card to Done. Open **Page 03 — Set up email at Migadu**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">19</property>
          <title>19 — Confirm domain is Active in Porkbun dashboard</title>
          <content>
            ## What to do
            
            In Porkbun → Account → My Domains.
            
            Your new domain should show:
            
            - Status: **Active**
            - Expiry: ~1 year from now
            - Auto-renew: ON
            - Privacy WHOIS: enabled
            
            If status is "Pending" — wait 5-15 minutes and refresh.
            
            If after 30 minutes status is still pending or you see an error — contact Porkbun support (their support is unusually responsive for the price).
            
            ## Verification
            
            Domain shows `Active`. You own it.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">18</property>
          <title>18 — Enable 2FA on Porkbun</title>
          <content>
            ## What to do
            
            In Porkbun account settings, find **Security** or **Two-Factor Authentication**.
            
            - Enable TOTP-based 2FA
            - Use 1Password to store the TOTP seed (under `LW-Porkbun account` → add OTP field)
            - Save the backup codes Porkbun provides in 1Password under `LW-Porkbun account` → secure note section
            
            ## Why this matters
            
            A compromised Porkbun account means an attacker can redirect your DNS to anywhere, including hijacking your persona's traffic. 2FA is non-optional for the domain registrar.
            
            ## Verification
            
            Logging out and back in prompts for the 2FA code. 1Password auto-fills the TOTP.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">17</property>
          <title>17 — Verify the registration confirmation email</title>
          <content>
            ## What to do
            
            Open your throwaway Gmail (in the LatticeWorks Chrome profile — DO NOT log into it from your personal profile).
            
            You should receive within 5 minutes:
            
            1. Order confirmation from Porkbun
            1. A verification email from Porkbun (REQUIRED — click the link to verify your email)
            
            Click the verification link in email #2. This activates your registration.
            
            ## Why this matters
            
            ICANN requires email verification for new registrations. If you skip this for 15 days, the registrar can suspend your domain. Don't forget.
            
            ## Verification
            
            You clicked the verification link. The success page on Porkbun confirms `email verified`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">16</property>
          <title>16 — Sign up Porkbun account + checkout</title>
          <content>
            ## What to do
            
            Click **Checkout**. Porkbun will prompt for account creation.
            
            - **Email:** your throwaway Gmail from Page 01 Card 4 (`latticeworks.dev@gmail.com` or whatever variant you used)
            - **Password:** generate a strong unique one with 1Password's password generator → save in 1Password under `LW-Porkbun account`
            - **Coupon code:** check r/PorkbunReg or porkbun.com/coupon for current promo (often $1-5 off first year)
            
            At payment:
            
            - **Card:** the `LW-Porkbun` virtual card from Card 14
            - Verify total matches expected (domain price + ICANN $0.18 fee)
            - Submit
            
            ## Verification
            
            Order confirmation page shows. Save the order # in 1Password as a comment under `LW-Porkbun account`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">15</property>
          <title>15 — Add domain to cart with Privacy WHOIS + auto-renew</title>
          <content>
            ## What to do
            
            Back on Porkbun's domain search result, click **Add to Cart** on your chosen TLD.
            
            In the cart:
            
            - **Privacy WHOIS:** Confirm ON (it's free with every Porkbun domain). This hides your name/address from public WHOIS lookups.
            - **Auto-renew:** Set to **ON**. You do NOT want this domain expiring while the persona is running.
            - **Years:** 1 year is fine. You can extend later.
            
            Do NOT click checkout yet — Card 16 covers sign-up + payment.
            
            ## Why this matters
            
            If Privacy WHOIS is off, anyone running `whois yourdomain.io` sees your name + address. Auto-renew off = the persona's domain quietly expires one day and the whole operation dies. Both default-on / default-correct settings, but worth confirming.
            
            ## Verification
            
            Cart shows: 1 domain, Privacy WHOIS enabled, auto-renew ON, 1 year term.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">14</property>
          <title>14 — Create a Privacy.com card locked to Porkbun</title>
          <content>
            ## What to do
            
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
            
            Card exists in Privacy.com dashboard with status `Active` and merchant `porkbun.com`. Card details in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">13</property>
          <title>13 — Confirm the TLD decision and document it</title>
          <content>
            ## What to do
            
            Open 1Password → LatticeWorks vault → + New Item → Secure Note → title `LW-Domain decision`.
            
            Write: `Chosen domain: latticeworks.<TLD>. Reason: <one line>.`
            
            Example: `Chosen domain: latticeworks.io. Reason: most professional / least likely to confuse vendors.`
            
            ## Why this matters
            
            Once you register, you can't easily change your mind (you'd be eating the registration fee). Documenting the decision now means future-you doesn't have to remember why you picked it.
            
            ## Verification
            
            Note saved in 1Password. You're committed to a specific TLD.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">12</property>
          <title>12 — Search for `latticeworks` availability</title>
          <content>
            ## What to do
            
            In Porkbun's search bar at the top of the homepage, type `latticeworks` and press search.
            
            You'll see all TLD options with their prices.
            
            ## Your TLD priority (pick the first available)
            
            1. **`.io`** — $32.37/yr first year, $51.80/yr renewal. Tech-y, professional, what most SaaS uses.
            1. **`.com`** — $9.73/yr. Cheapest if available, but `latticeworks.com` may be taken.
            1. **`.dev`** — typically $15-20/yr. Tech-focused, signals "this is a software thing."
            1. **`.systems`** — $30-40/yr. Generic SaaS feel.
            1. **`.app`** — $15-20/yr. Requires HTTPS (built into the TLD).
            1. **`.co`** — $25-35/yr. Short, professional.
            
            Avoid: `.net` (looks dated), country TLDs (`.io` is offshore but treated as global), `.online`/`.xyz` (cheap but lower trust signal).
            
            ## Verification
            
            You have a target TLD picked. Don't add to cart yet — that's Card 13 after you have a Privacy.com card ready in Card 14.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">11</property>
          <title>11 — Open Porkbun in your LatticeWorks Chrome profile</title>
          <content>
            ## What to do
            
            In the LatticeWorks Chrome profile, navigate to [https://porkbun.com](https://porkbun.com).
            
            ## Why this matters
            
            Porkbun in the wrong browser profile = a domain registration tied to your personal Google session, with autofill / saved cards potentially exposing your real identity. Use the LatticeWorks profile or stop here.
            
            ## Verification
            
            The browser tab shows porkbun.com, and the profile color indicator (top right Chrome corner) is the LatticeWorks color. You are NOT signed into any Google account at the Chrome level.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
