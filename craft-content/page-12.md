<page id="35df201d-e5d5-0e74-2fce-eddff803fbc5">
  <pageTitle>Page 12 — Voice + final smoke test</pageTitle>
  <content>
    # Page 12 — Voice + final smoke test
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Train the persona's voice clone in ElevenLabs and verify all end-to-end pipelines. ~2 hours + voice training time. Requires all prior pages complete.
    
    <collection>
      <title>Page 12 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">120</property>
          <title>120 — Setup complete. You're ready to build.</title>
          <content>
            ## Final checklist
            
            - [ ] All previous 119 microsteps complete
            - [ ] Every vendor account active, credentials in 1Password
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
            
            **Build phase** is separate:
            
            - Wire orchestration code (Claude API as brain)
            - Build conversational layer (OpenRouter for explicit chat)
            - Build content generation pipeline (ComfyUI on RunPod)
            - Build Twitter posting + reply-guy bot
            - Build Telegram chat handler with memory + customer profiling
            - Build shoutout management module
            - Wire detection-evasion post-processing
            - Wire payment-handling + custom-request flow
            
            ~9-13 weeks of engineering, separate from this playbook.
            
            ## All boxes checked?
            
            Drag this card to Done. LatticeWorks setup complete.
            
            Welcome to the build phase. 🎯
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">119</property>
          <title>119 — Backup audit + 1Password export rehearsal</title>
          <content>
            ## What to do
            
            Verify handoff mechanism works.
            
            ### Export 1Password vault test
            
            - 1Password → LatticeWorks vault → `...` → Export → 1Password Unencrypted Format (1pux) or CSV
            - Save to Mac temporarily as `latticeworks-vault-test-export.1pux`
            - Open (with 1Password import tool) into TEST vault to verify export integrity
            - Delete test export and test vault immediately
            
            ### Verify backups of seed phrase locations
            
            - Confirm hardware-wallet seed phrase (Page 07 Card 63) in BOTH physical locations
            - Confirm 1Password split-saved seeds (words 1-6, 7-12) intact
            
            ### Document handoff process
            
            In 1Password under `LW-Handoff playbook`:
            
            - 'To hand off to client: export this vault as 1pux → send via Signal or secure file transfer → recipient imports.'
            - 'Then change all credentials' (passwords, API keys) AFTER handoff, so old exports become useless.
            
            ## Verification
            
            Vault export works. Backup integrity confirmed.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">118</property>
          <title>118 — Final pipeline smoke test: content generation</title>
          <content>
            ## What to do
            
            Final smoke test of CONTENT path.
            
            ### Step 1 — Generate one image (RunPod)
            
            SSH into Hostwinds. Start ComfyUI pod on RunPod with Flux + AIDMA NSFW Unlock LoRA.
            
            (Detailed ComfyUI setup in build phase 2 — for smoke test just verify a pod with Flux starts and generates one test image.)
            
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
            
            Full content path works end-to-end: generate → store → CDN → deliver.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">117</property>
          <title>117 — Full pipeline smoke test: Twitter → Telegram → payment</title>
          <content>
            ## What to do
            
            End-to-end smoke test simulating a real customer journey.
            
            ### Step 1 — Twitter side
            
            From operator account (or friend's), DM persona's Twitter: `hi cutie`
            
            ### Step 2 — Telegram bridge (manual for now; bot will automate)
            
            From persona's Twitter, reply: `hey 💋 come find me on telegram, that's where i play → [bot deep-link]`
            
            Deep-link format: `https://t.me/[your_bot_username]?start=test_user_001`
            
            ### Step 3 — Telegram conversation
            
            'Customer' (you) clicks link → opens Telegram → starts the bot.
            
            - Bot doesn't reply yet (no code yet)
            - Chat established
            
            ### Step 4 — Manually issue Stars invoice
            
            From Hostwinds server, send Stars invoice to customer chat (curl from Page 08 Card 78).
            
            ### Step 5 — Customer pays
            
            You click 'Pay 1 Star' → enter PIN → confirm
            
            ### Step 6 — Confirm receipt
            
            In bot owner view, Stars balance increments by 1.
            
            ## Verification
            
            End-to-end customer journey works manually. Plumbing proven.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">116</property>
          <title>116 — Get ElevenLabs API key</title>
          <content>
            ## What to do
            
            ElevenLabs → Profile → API Key.
            
            Copy the key (long string starting `sk_...`).
            
            Save in 1Password as `LW-ElevenLabs API key`.
            
            Test from Hostwinds server:
            
            ```
            LW_EL_KEY="your_key"
            LW_VOICE_ID="your_voice_id"
            
            curl --request POST \\
              --url "https://api.elevenlabs.io/v1/text-to-speech/${LW_VOICE_ID}" \\
              --header "xi-api-key: ${LW_EL_KEY}" \\
              --header "Content-Type: application/json" \\
              --data '{"text":"hey baby","model_id":"eleven_multilingual_v2"}' \\
              --output /tmp/test.mp3
            
            # Play it
            afplay /tmp/test.mp3
            ```
            
            ## Verification
            
            API call returns audio. Plays cleanly.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">115</property>
          <title>115 — Test voice quality</title>
          <content>
            ## What to do
            
            ElevenLabs → Voices → click persona's voice → Generate.
            
            Test phrases (3-5):
            
            - 'Hi babe, just thinking about you 💋'
            - 'want to see what i'm doing right now?'
            - 'tip me $30 and i'll send you something special'
            
            Listen on headphones. Check:
            
            - Matches persona's 'feel' (age, accent, vibe)?
            - Robotic / glitchy moments?
            - Pacing natural?
            
            If off:
            
            - Re-upload with cleaner reference
            - Adjust stability + similarity settings
            
            ## Verification
            
            Voice sounds natural, matches persona vibe.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">114</property>
          <title>114 — Train the persona's voice clone in ElevenLabs</title>
          <content>
            ## What to do
            
            In ElevenLabs → Voices → Add Voice → **Professional Voice Clone**.
            
            - **Name:** persona's stage name (e.g., `Lily`)
            - **Description:** 'AI persona voice for LatticeWorks'
            - Upload reference audio from Card 113
            - Click Create
            
            Training: 2-5 minutes.
            
            ## Verification
            
            Voice clone in your Voices list. Generate a test phrase to confirm.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">113</property>
          <title>113 — Source reference audio for voice clone</title>
          <content>
            ## What to do
            
            Professional Voice Cloning needs 30+ sec (ideally 1-2 min) of clean reference audio.
            
            **Sources for persona's voice:**
            
            ### Option A — Generate via TTS (zero-shot)
            
            - Use OpenAI's TTS API or similar to generate ~60 sec clean speech in a voice you like
            - Save as `.mp3` / `.wav`
            - Reference for ElevenLabs
            
            ### Option B — Record a voice actor
            
            - Hire on Fiverr (~$30-80) for 1-2 min read-out clean audio
            - Get rights to use as AI voice reference (specify in contract)
            
            ### Option C — Sample from public domain / royalty-free
            
            - CC0 / royalty-free podcast audio
            - More complex for 'consistent persona voice'
            
            **Recommendation: Option B.** Voice actors give unique, ownable voice with proper rights. ~$50 well spent.
            
            ## Verification
            
            30+ sec audio file ready to upload to ElevenLabs.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">112</property>
          <title>112 — Pay with Privacy.com card</title>
          <content>
            ## What to do
            
            Create Privacy.com card: `LW-ElevenLabs`, lock to `elevenlabs.io`, $50/mo limit.
            
            Save to `LW-ElevenLabs virtual card` in 1Password.
            
            Pay $22/mo with this card.
            
            ## Verification
            
            Subscription active.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">111</property>
          <title>111 — Sign up ElevenLabs Creator tier</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://elevenlabs.io](https://elevenlabs.io).
            
            - Sign Up with `eleven@latticeworks.<TLD>`
            - Choose **Creator plan** ($22/mo) — unlocks Professional Voice Cloning
            - Save login to `LW-ElevenLabs account` in 1Password
            
            ## Why Creator (not Starter)
            
            - Starter ($5/mo): only Instant Voice Clone (lower quality, won't match persona consistency)
            - Creator ($22/mo): Professional Voice Clone (trained on 30+ sec, much higher fidelity)
            
            For a 'feels real' persona experience, Creator is the floor.
            
            ## Verification
            
            Account active on Creator tier.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
