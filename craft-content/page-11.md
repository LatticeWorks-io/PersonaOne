<page id="c13422cb-04a2-235d-f7e5-b1c5d7a5b2fc">
  <pageTitle>Page 11 — Twitter ACC enrollment</pageTitle>
  <content>
    # Page 11 — Twitter ACC enrollment
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Apply to and get approved for Twitter's Adult Content Creator program. Includes 1-7 day review. Requires Page 10 complete (14-day warmup).
    
    <collection>
      <title>Page 11 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">110</property>
          <title>110 — Final check before Page 12 (voice + smoke test)</title>
          <content>
            ## Confirm
            
            - [ ] ACC application submitted and approved
            - [ ] Identity verified (real ID + selfie)
            - [ ] Tax docs submitted matching tax structure decision
            - [ ] Sensitivity tier set to Adult
            - [ ] AI disclosure in bio
            - [ ] Adult content sensitivity setting ON
            - [ ] Posting templates documented for future bot use
            - [ ] Monetization features (tips, etc.) enabled
            
            ## All 8 boxes checked?
            
            Drag to Done. Open **Page 12 — Voice + final smoke test**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">109</property>
          <title>109 — On approval: enable monetization features</title>
          <content>
            ## What to do
            
            When approval email arrives at `me@latticeworks.<TLD>`:
            
            In Twitter Monetization settings:
            
            - Enable Creator Subscriptions (if you want subscription tier — most LatticeWorks personas skip, doing tips + customs)
            - Enable Tips (Twitter's native tip feature)
            - Verify Adult-tier posting capabilities active
            
            Update bio once more to reflect monetization (NowPayments tip link + Telegram bot link).
            
            ## What to NOT enable
            
            - Twitter 'Verified' (blue check) — don't need for ACC, adds friction
            - Twitter Ads — irrelevant
            
            ## Verification
            
            ACC monetization enabled. Bio reflects active operation.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">108</property>
          <title>108 — Submit application + wait for review</title>
          <content>
            ## What to do
            
            In ACC dashboard, click **Submit**.
            
            Review timeline:
            
            - Typical: 24-72 hours
            - Sometimes: 5-7 days during high-volume
            - Rarely: over 2 weeks (email Twitter support)
            
            While waiting:
            
            - DO NOT post NSFW
            - DO continue SFW posting at warmup pace (3-5 posts/day) to keep account 'alive'
            - DO NOT switch to bot automation yet
            
            ## Verification
            
            Application submitted. Status `Under review`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">107</property>
          <title>107 — Set up posting templates with required hashtags</title>
          <content>
            ## What to do
            
            ACC requires AI-generated content tagged. The pattern (as of 2026):
            
            - Every NSFW post: `#AI` or `#Generated` hashtag
            - Caption mentions 'AI' once at start of more explicit content
            
            Document standard templates in 1Password under `LW-Posting templates`:
            
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
            
            Use in bot's posting logic later.
            
            ## Verification
            
            Templates documented for future bot use.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">106</property>
          <title>106 — Configure profile for adult content</title>
          <content>
            ## What to do
            
            Settings → Privacy and Safety → Your posts:
            
            - **Sensitivity Settings:** Mark media as containing sensitive content (default ON for all posts)
            
            Settings → Privacy and Safety → Discoverability:
            
            - **Discoverable by phone:** OFF (don't let LW-Phone unmask)
            - **Discoverable by email:** OFF (don't let Migadu address leak)
            
            Settings → Privacy and Safety → Audience and tagging:
            
            - **Protect your posts:** OFF (want public discoverability)
            - **Photo tagging:** Off or Only people I follow
            
            ## Verification
            
            Settings configured.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">105</property>
          <title>105 — Update bio with AI disclosure (per ACC policy)</title>
          <content>
            ## What to do
            
            ACC requires clear AI disclosure for AI personas.
            
            Update Twitter bio (Profile → Edit Profile → Bio):
            
            **Format that complies with ACC but preserves fiction:**
            
            Example alt-niche:
            
            ```
            22 · NYC · alt baddie · AI 💋 still treat me like the real thing tho · 🔗 [link-in-bio URL]
            ```
            
            **Required:**
            
            - Word 'AI' visible in bio (not in collapsed section)
            - `#AI` hashtag pattern in posts (Card 107)
            
            **Optional:** link in bio (Page 10 Card 97).
            
            ## Verification
            
            Bio updated, AI disclosure present, link active.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">104</property>
          <title>104 — Set content sensitivity tier</title>
          <content>
            ## What to do
            
            ACC tiers:
            
            - **Adult** — nudity, suggestive content, sexual themes (less restrictive)
            - **Explicit** — actual sexual acts, hardcore (most restrictive labeling)
            
            For synthetic AI persona, tip+custom model:
            
            - Most content fits **Adult**
            - Reserve Explicit for hardcore customs (Page 12)
            
            Pick Adult for now. Request Explicit later.
            
            ## Verification
            
            Sensitivity tier set to Adult.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">103</property>
          <title>103 — Submit tax documents</title>
          <content>
            ## What to do
            
            Per Page 01 Card 8 decision:
            
            ### Option A (UpfrontOps LLC):
            
            - W-9 with UpfrontOps LLC name + EIN
            - LLC formation document
            
            ### Option B (new LLC):
            
            - W-9 with new LLC name + EIN
            - LLC formation document
            - Best if you formed the LLC during Pages 02-10 in parallel
            
            ### Option C (1099 personal):
            
            - W-9 with your personal name + SSN
            - Ties adult-creator income directly to your personal name on Twitter records
            
            Upload via ACC application.
            
            ## Why now
            
            Without tax docs, Twitter can't pay you for ACC revenue. They require before approval.
            
            ## Verification
            
            Tax docs uploaded.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">102</property>
          <title>102 — Submit identity verification (YOUR ID)</title>
          <content>
            ## What to do
            
            ACC requires VERIFIED IDENTITY of the operator. Your real ID, not the persona's.
            
            Upload:
            
            - **Government-issued photo ID** (US driver's license, passport, state ID)
            - **Selfie holding the ID** (Twitter prompts with overlay guides)
            
            Make sure:
            
            - ID clear, all corners visible
            - Selfie shows your face + ID readable
            - Good lighting
            
            ## Why your real ID
            
            ACC is the platform's KYC for adult creators. They need a real human accountable. Your real identity is on the BACK END (creator records). FRONT END (persona profile) stays anonymous — followers see persona's stage name only.
            
            ## Verification
            
            ID + selfie submitted. ACC dashboard shows `Pending`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">101</property>
          <title>101 — Open the ACC application in Twitter settings</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, log into persona's Twitter.
            
            Navigate to: Settings → Monetization → look for **Adult Content Creator**.
            
            If you can't find it:
            
            - ACC is sometimes invite-only / regional rollout
            - Apply via public form: [https://help.x.com/en/forms/account-access/regain-access/adult-content-creator-application](https://help.x.com/en/forms/account-access/regain-access/adult-content-creator-application)
            
            ## Verification
            
            ACC application form open in browser.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
