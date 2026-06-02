<page id="2261b5e7-dc0b-7e31-487f-e37c1f2fab40">
  <pageTitle>Page 09 — Twitter account creation</pageTitle>
  <content>
    # Page 09 — Twitter account creation
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Create a fresh Twitter account for the persona, ready to begin warmup. **No NSFW yet.** ~30 minutes. Requires Page 03 (email) + Page 01 (phone).
    
    <collection>
      <title>Page 09 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">90</property>
          <title>90 — Final check before Page 10 (Twitter warmup)</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">89</property>
          <title>89 — DO NOT post anything yet</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">88</property>
          <title>88 — Configure email + notifications</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">87</property>
          <title>87 — Enable 2FA on Twitter</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">86</property>
          <title>86 — Add placeholder profile pic and banner</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">85</property>
          <title>85 — Set placeholder bio (NO NSFW yet, NO AI disclosure yet)</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">84</property>
          <title>84 — Set the @handle and finalize username</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">83</property>
          <title>83 — Phone verify with LW-Phone</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">82</property>
          <title>82 — Sign up new Twitter account</title>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">81</property>
          <title>81 — Pick the persona's Twitter handle + display name</title>
        </collectionItem>
      </content>
    </collection>
    <collection>
      <title>Page 09 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">90</property>
          <title>90 — Final check before Page 10 (Twitter warmup)</title>
          <content>
            ## Confirm
            
            - [ ] Twitter handle + display name picked + documented in 1Password
            - [ ] Account created with `twitter@latticeworks.<TLD>` email
            - [ ] Phone verified via LW-Phone
            - [ ] Placeholder bio (SFW, no NSFW signals, no AI disclosure yet)
            - [ ] Placeholder profile pic and banner (generic)
            - [ ] 2FA enabled with authenticator app, backup codes in 1Password
            - [ ] Email notifications ON to `me@latticeworks.<TLD>`
            - [ ] DMs open to message requests
            - [ ] Zero tweets posted. Following 5-10 niche accounts MAX.
            
            ## All 9 boxes checked?
            
            Drag to Done. Open **Page 10 — Twitter warmup (7-14 days)**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">89</property>
          <title>89 — DO NOT post anything yet</title>
          <content>
            ## What to do
            
            Resist the urge.
            
            For the next 7-14 days (Page 10's warmup), the account looks slightly suspicious to Twitter:
            
            - New account
            - New IP (Hostwinds server, if you ever log in from there)
            - New phone
            
            Post NSFW in the first 24-48 hours → Twitter's automated systems shadowban or suspend. Patience pays exponentially.
            
            ## What you CAN do today
            
            - Follow 5-10 accounts in your niche (max 5-10 in first 24 hours)
            - 'Like' a few of their tweets
            - That's it. No tweets, no replies, no DMs sent.
            
            ## Verification
            
            Account exists. Zero original tweets. Following ~5-10 niche accounts.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">88</property>
          <title>88 — Configure email + notifications</title>
          <content>
            ## What to do
            
            Settings → Notifications:
            
            - Email notifications: ON (security alerts reach `me@latticeworks.<TLD>` via Migadu)
            - Push notifications: OFF (no phone buzzes for every like during automation)
            
            Settings → Privacy and Safety:
            
            - Protected mode: OFF (persona must be discoverable)
            - DM settings: Allow message requests from everyone (the inbox the bot will work)
            
            ## Verification
            
            Settings configured for autonomous operation.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">87</property>
          <title>87 — Enable 2FA on Twitter</title>
          <content>
            ## What to do
            
            Settings → Security and account access → Security → Two-factor authentication.
            
            - Choose **Authentication app** (NOT SMS — SMS 2FA is vulnerable to SIM swaps)
            - Use 1Password's TOTP feature: in `LW-Twitter account` item, add the OTP field by scanning Twitter's QR code
            
            Save backup codes Twitter provides in 1Password under `LW-Twitter account` → Secure Note.
            
            ## Verification
            
            Logging out and back in requires 1Password TOTP. Backup codes saved.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">86</property>
          <title>86 — Add placeholder profile pic and banner</title>
          <content>
            ## What to do
            
            - **Profile pic:** use a generic abstract image (sunset, texture, non-face avatar). NOT a final persona image — those come post-ACC.
            - **Banner:** similar — a generic vibey image.
            
            Placeholders via:
            
            - Unsplash / Pexels stock photos
            - DALL-E for SFW landscapes via your Anthropic API
            - canva.com gradient
            
            ## Why placeholders?
            
            Twitter algorithms flag profile changes during warmup as suspicious. Start with clearly-placeholder branding and update to real persona content AFTER ACC approval.
            
            ## Verification
            
            Profile pic and banner set. Both SFW placeholders.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">85</property>
          <title>85 — Set placeholder bio (NO NSFW yet, NO AI disclosure yet)</title>
          <content>
            ## What to do
            
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
            
            Bio set, vanilla, no NSFW signals.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">84</property>
          <title>84 — Set the @handle and finalize username</title>
          <content>
            ## What to do
            
            In Twitter → Profile → Edit Profile:
            
            - Set @handle from Card 81
            - Twitter sometimes auto-generates an ugly one — change it to your picked handle now
            
            ## Verification
            
            Profile URL is `x.com/<your-picked-handle>`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">83</property>
          <title>83 — Phone verify with LW-Phone</title>
          <content>
            ## What to do
            
            Twitter will prompt for phone verification (sometimes immediately, sometimes after first post or first reply).
            
            - Use `LW-Phone` from Page 01 Card 5 (MySudo recommended — Twitter is increasingly rejecting Google Voice)
            - Enter the SMS code from MySudo
            
            If Twitter rejects the number as VoIP:
            
            - Try a real burner SIM (e.g., $20 prepaid SIM from Mint Mobile, Visible, or similar)
            - Use the SIM in an old phone or via an eSIM in your existing iPhone (configure eSIM with a separate plan)
            
            ## Verification
            
            Phone verified on Twitter.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">82</property>
          <title>82 — Sign up new Twitter account</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://x.com](https://x.com) → **Sign Up**.
            
            - **Name:** persona's display name from Card 81
            - **Email:** `twitter@latticeworks.<TLD>` (works via Migadu catch-all)
            - **Date of birth:** persona's stated age — must be 18+. Pick a believable date (e.g., 22-30 range).
            - Click Next
            
            Twitter sends verification email — check Migadu inbox, click verify link.
            
            ## Verification
            
            Account created, email verified.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">81</property>
          <title>81 — Pick the persona's Twitter handle + display name</title>
          <content>
            ## What to do
            
            Decide on the persona's identity on Twitter. Document in 1Password under `LW-Persona Twitter identity`:
            
            - **Handle** (`@username`): short, memorable, matches Telegram bot username pattern. E.g., `@lily_xo` or `@itslilybabe`.
            - **Display name:** persona's stage name (e.g., `Lily 💋`)
            - **Niche:** which audience (alt / gym / Latina / etc.) — should match your earlier persona-niche pick
            
            ### Handle availability check
            
            In LatticeWorks Chrome profile (LOGGED OUT of any Twitter), go to [https://x.com/[candidate_handle]](https://x.com/[candidate_handle]).
            
            - 404 page = available
            - Profile shown = taken; try variants
            
            Avoid:
            
            - Numbers in handle (`lily123`) — looks scammy/AI
            - Underscores at start/end (`_lily_`) — looks fake
            - Trying to match an existing real OnlyFans creator's vibe too closely (risk of trademark/impersonation claims)
            
            ## Verification
            
            Handle picked, available, documented.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
