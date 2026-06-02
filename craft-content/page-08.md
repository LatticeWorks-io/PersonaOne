<page id="397ada36-43cf-9a26-b423-08e3b91ca3d7">
  <pageTitle>Page 08 — Telegram setup</pageTitle>
  <content>
    # Page 08 — Telegram setup
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Create the persona's Telegram account + bot, and prove the bot can send messages + Stars invoices via API. ~1 hour. Requires Page 01 complete (LW-Phone).
    
    <collection>
      <title>Page 08 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">80</property>
          <title>80 — Final check before Page 09</title>
          <content>
            ## Confirm
            
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
            
            Drag to Done. Open **Page 09 — Twitter account creation**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">79</property>
          <title>79 — Enable Telegram inline + groups settings</title>
          <content>
            ## What to do
            
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
            
            BotFather confirms each setting.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">78</property>
          <title>78 — Test Telegram Stars (in-bot payments)</title>
          <content>
            ## What to do
            
            Stars are how customers will tip + buy customs. Test that the API can request payment.
            
            From the Hostwinds server, send an invoice:
            
            ```
            LW_BOT_TOKEN="your_bot_token"
            LW_CHAT_ID="your_chat_id"
            
            curl -X POST "https://api.telegram.org/bot${LW_BOT_TOKEN}/sendInvoice" \
              -H "Content-Type: application/json" \
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
            
            Invoice card appears in your Telegram chat with the bot. You can see the "Pay 1 Star" button. (Actual payment is optional for smoke test.)
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">77</property>
          <title>77 — Smoke test: send a message FROM the bot via API</title>
          <content>
            ## What to do
            
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
            curl "https://api.telegram.org/bot${LW_BOT_TOKEN}/sendMessage" \
              -d "chat_id=${LW_CHAT_ID}" \
              -d "text=smoke test from server $(date)"
            ```
            
            ## Verification
            
            Telegram on your devices receives the message from your bot. Confirms the bot can send programmatically.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">76</property>
          <title>76 — Send /start to your bot from your operator account</title>
          <content>
            ## What to do
            
            In Telegram, find your new bot (search the username from Card 74).
            
            Click Start (or send `/start`).
            
            The bot won't reply yet — there's no code running. But Telegram now has a record of you as a user of your own bot. Useful for testing.
            
            ## Verification
            
            You see your `/start` message in the bot chat. The bot doesn't reply (expected).
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">75</property>
          <title>75 — Configure bot description and about</title>
          <content>
            ## What to do
            
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
            
            Bot's profile in Telegram shows description, about, and pic.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">74</property>
          <title>74 — Create the persona's Telegram bot via @BotFather</title>
          <content>
            ## What to do
            
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
            
            Bot appears in your Telegram (search for the bot username, click to chat with it). Token saved in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">73</property>
          <title>73 — Enable Telegram cloud password (2FA)</title>
          <content>
            ## What to do
            
            In Telegram Desktop:
            
            - Settings → Privacy and Security → Two-Step Verification (Cloud Password)
            - Set Password: strong unique from 1Password
            - Set Hint: something only you'd know (don't write the password itself as hint)
            - Set Recovery Email: `me@latticeworks.<TLD>`
            
            Save in 1Password as `LW-Telegram cloud password`.
            
            ## Why this matters
            
            Without cloud password, anyone who gets your SMS (SIM swap attack, MySudo compromise, GV hijack) can take over the Telegram account, hijack the bot, and start tipping themselves money.
            
            ## Verification
            
            Logging out and back in requires both SMS code AND cloud password. 1Password autofills the cloud password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">72</property>
          <title>72 — Sign up Telegram with LW-Phone</title>
          <content>
            ## What to do
            
            ### On Mac Telegram Desktop:
            
            - Click "Start Messaging"
            - Country code: USA (+1)
            - Phone number: enter `LW-Phone` (from Page 01 Card 5 — MySudo or Google Voice)
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
            
            Telegram active on Mac + iPhone, signed in as persona. No profile pic / bio yet.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">71</property>
          <title>71 — Install Telegram on Mac + iPhone</title>
          <content>
            ## What to do
            
            ### Mac
            
            - Telegram Desktop: [https://desktop.telegram.org](https://desktop.telegram.org) → install for macOS
            - Open Telegram Desktop
            
            ### iPhone
            
            - App Store → Telegram Messenger → install
            
            **Do not log in yet** — we need to do this carefully with the right phone number in Card 72.
            
            ## Why both surfaces
            
            Telegram bots are operated through ONE Telegram account (the owner). You'll access the bot from both Mac (for admin / debugging) and iPhone (for mobile alerts). Same account, two devices.
            
            ## Verification
            
            Telegram installed on both devices, both showing login screen.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
