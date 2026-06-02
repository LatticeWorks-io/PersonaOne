<page id="da4d46c7-ee25-e5d0-0226-3cbcee320eb5">
  <pageTitle>Page 03 — Set up email at Migadu + DNS</pageTitle>
  <content>
    # Page 03 — Set up email at Migadu + DNS
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Get `me@latticeworks.<TLD>` live so we stop using throwaway Gmail. ~45 minutes + DNS wait. Requires Page 02 complete (domain registered).
    
    <collection>
      <title>Page 03 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">30</property>
          <title>30 — Test the full mail flow + final check</title>
          <content>
            ## Test 1: send to me@
            
            From the throwaway Gmail, send an email to `me@latticeworks.<TLD>`. Subject: "Test 1 - direct"
            
            In Migadu webmail ([https://webmail.migadu.com](https://webmail.migadu.com)), log in as `me@latticeworks.<TLD>` → check inbox. Email should arrive within 1 minute.
            
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
            
            Drag to Done. You now have a working professional email anchor. Open **Page 04 — Provision your server**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">29</property>
          <title>29 — Enable catch-all addressing</title>
          <content>
            ## What to do
            
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
            
            Catch-all is enabled. (Verify in Card 30.)
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">28</property>
          <title>28 — Create me@latticeworks.io mailbox</title>
          <content>
            ## What to do
            
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
            
            Mailbox exists in Migadu. Login + password in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">27</property>
          <title>27 — Verify domain in Migadu</title>
          <content>
            ## What to do
            
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
            
            All 6 DNS checks in Migadu show ✅ green.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">26</property>
          <title>26 — Wait for DNS propagation (~5-30 min)</title>
          <content>
            ## What to do
            
            DNS changes don't take effect instantly. Two ways to check:
            
            **Option A: Terminal (faster, more authoritative)**
            
            On your Mac terminal:
            
            ```
            dig MX latticeworks.io +short
            dig TXT latticeworks.io +short
            ```
            
            You should see migadu's MX records and the SPF record. If you see nothing or the wrong records, wait 5 min and retry.
            
            **Option B: Browser check (slower, more user-friendly)**
            
            Go to [https://www.whatsmydns.net](https://www.whatsmydns.net) → search your domain → MX records. You'll see propagation status across the world.
            
            Wait until at least 80% of locations show the correct Migadu MX records before continuing.
            
            ## Why this matters
            
            If you try to verify Migadu before DNS propagates, verification fails. Patience pays off.
            
            ## Verification
            
            `dig MX <yourdomain>` shows Migadu's MX records, OR whatsmydns.net shows MX propagation across most regions.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">25</property>
          <title>25 — Add MX + TXT records to Porkbun DNS</title>
          <content>
            ## What to do
            
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
            
            Porkbun DNS records show all 7 records (2 MX + 5 TXT) for your domain.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">24</property>
          <title>24 — Pull the DNS records Migadu generated</title>
          <content>
            ## What to do
            
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
            
            All MX + SPF + DKIM + DMARC records copied to a 1Password secure note.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">23</property>
          <title>23 — Add your domain to Migadu</title>
          <content>
            ## What to do
            
            In Migadu dashboard:
            
            - Navigate to **Domains** in the sidebar
            - Click **Add domain**
            - Enter your domain: `latticeworks.<TLD>` (the one you registered in Page 02)
            - Click Add
            
            Migadu will now show your domain in the list with status `Pending DNS verification`.
            
            ## Verification
            
            Domain appears under Domains in Migadu, with status pending DNS config.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">22</property>
          <title>22 — Create Privacy.com card for Migadu and pay annual</title>
          <content>
            ## What to do
            
            In Privacy.com (LatticeWorks Chrome profile), create new card:
            
            - **Type:** Merchant Locked
            - **Name:** `LW-Migadu`
            - **Spend limit:** $50 (covers $19/yr + headroom for renewals)
            - **Merchant lock:** `migadu.com`
            
            Save card to 1Password under `LW-Migadu virtual card`.
            
            Back in Migadu, complete the payment with this card. Choose **annual** billing ($19/yr) — there's no monthly option on Mini and annual is the recommended pricing.
            
            ## Verification
            
            Migadu shows subscription `Active`. Receipt arrived in throwaway Gmail.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">21</property>
          <title>21 — Sign up Migadu (use throwaway Gmail)</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://www.migadu.com/signup](https://www.migadu.com/signup).
            
            - **Plan:** select **Mini** ($19/year). It includes: unlimited mailboxes, unlimited aliases, unlimited domains, 30 daily / 200 incoming emails — plenty for a single-persona ops setup.
            - **Email for account login:** your throwaway Gmail from Page 01 Card 4 (`latticeworks.dev@gmail.com`)
            - **Password:** strong, unique, generated via 1Password
            - Save login in 1Password under `LW-Migadu account`
            
            ## Why Migadu (not Proton, not Tuta, not Workspace)
            
            Migadu doesn't filter by content. Their TOS is "don't spam." Adult-industry-friendly in practice (won't suspend you for hosting email for an adult persona). Cheap. Founder-run Swiss company.
            
            ProtonMail and Tutanota have suspended accounts associated with adult industries. Google Workspace is strictly prohibited (their TOS catches this fast). Don't use them.
            
            ## Verification
            
            Migadu dashboard loads. You're logged in. Account in 1Password.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
