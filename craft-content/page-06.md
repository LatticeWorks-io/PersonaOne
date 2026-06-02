<page id="e87ecf08-1b77-5d85-9d96-e4cf5d19874b">
  <pageTitle>Page 06 — AI APIs (Claude + OpenRouter + Postmark)</pageTitle>
  <content>
    # Page 06 — AI APIs (Claude + OpenRouter + Postmark)
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Get all the AI-side API keys configured and smoke-tested. ~1 hour. Requires Page 03 complete (email anchor).
    
    <collection>
      <title>Page 06 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">60</property>
          <title>60 — Final check before Page 07</title>
          <content>
            ## Confirm
            
            - [ ] Anthropic Console account + $20-50 credit + API key in 1Password
            - [ ] Claude API smoke test succeeded
            - [ ] OpenRouter account + $50 credit + API key in 1Password
            - [ ] Uncensored model smoke test succeeded (model name documented in `LW-Uncensored model choice`)
            - [ ] Postmark account on free tier + verified sender domain + API token in 1Password
            - [ ] Postmark email smoke test succeeded
            
            ## All 6 boxes checked?
            
            Drag to Done. Open **Page 07 — NowPayments + crypto wallet**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">59</property>
          <title>59 — Get the Postmark Server API token</title>
          <content>
            ## What to do
            
            In Postmark → your `LW-Transactional` server → API Tokens.
            
            Copy the **Server API Token** (long string).
            
            Save in 1Password as `LW-Postmark API token`.
            
            Test with a curl from your Hostwinds server:
            
            ```
            curl "https://api.postmarkapp.com/email" \
              -X POST \
              -H "Accept: application/json" \
              -H "Content-Type: application/json" \
              -H "X-Postmark-Server-Token: $LW_POSTMARK_TOKEN" \
              -d '{
                "From":"me@latticeworks.<TLD>",
                "To":"<your throwaway Gmail>",
                "Subject":"Postmark test",
                "TextBody":"This is a smoke test from LatticeWorks."
              }'
            ```
            
            Should return success and the email arrives at the throwaway Gmail within 30 sec.
            
            ## Verification
            
            Smoke test email arrived.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">58</property>
          <title>58 — Create a Postmark Server + verify sender domain</title>
          <content>
            ## What to do
            
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
            
            Postmark shows domain verified (green checkmarks on DKIM + Return-Path).
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">57</property>
          <title>57 — Sign up Postmark (transactional email)</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://postmarkapp.com](https://postmarkapp.com).
            
            - Sign Up with `postmark@latticeworks.<TLD>`
            - Stay on **Free plan** for now (100 emails/mo, plenty for setup phase)
            - Save login to `LW-Postmark account` in 1Password
            
            ## Why Postmark vs others
            
            Postmark explicitly allows adult senders (other transactional providers like SendGrid have been known to suspend). Their deliverability is among the highest in the industry.
            
            ## Verification
            
            Postmark dashboard accessible.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">56</property>
          <title>56 — Test the uncensored model end-to-end</title>
          <content>
            ## What to do
            
            You don't need to actually generate explicit content yet (that's Phase 6+ when the bot is wired). Just verify the uncensored model responds and isn't refusal-trained.
            
            Send a benign but model-personality-revealing prompt via OpenRouter API:
            
            ```
            curl https://openrouter.ai/api/v1/chat/completions \
              -H "Authorization: Bearer $LW_OR_KEY" \
              -H "Content-Type: application/json" \
              -d '{"model":"sao10k/l3-lunaris-8b","messages":[{"role":"system","content":"You are a flirty character named Test."},{"role":"user","content":"hey there"}]}'
            ```
            
            You should get a response that's flirty, personality-driven, not "I cannot engage in romantic roleplay" refusal.
            
            If it refuses → try `cognitivecomputations/dolphin-2.6-mistral-7b` or another uncensored model on OpenRouter.
            
            ## Verification
            
            Model returns in-character response. Save the model identifier you settled on in 1Password under `LW-Uncensored model choice`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">55</property>
          <title>55 — Fund OpenRouter + generate API key</title>
          <content>
            ## What to do
            
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
            curl https://openrouter.ai/api/v1/chat/completions \
              -H "Authorization: Bearer $LW_OR_KEY" \
              -H "Content-Type: application/json" \
              -d '{"model":"sao10k/l3-lunaris-8b","messages":[{"role":"user","content":"hi"}]}'
            ```
            
            Should return a response.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">54</property>
          <title>54 — Sign up OpenRouter (for uncensored LLM)</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://openrouter.ai](https://openrouter.ai).
            
            - Sign Up with `openrouter@latticeworks.<TLD>`
            - Password from 1Password, save to `LW-OpenRouter account`
            
            ## Why OpenRouter (not self-hosted vLLM)
            
            For our scale, OpenRouter is ~8x cheaper than self-hosting an uncensored Llama on RunPod 24/7. We confirmed this in cost analysis. Use OpenRouter unless / until usage justifies self-hosting.
            
            ## Verification
            
            OpenRouter dashboard accessible.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">53</property>
          <title>53 — Create the Claude API key</title>
          <content>
            ## What to do
            
            In Console → API Keys → Create Key.
            
            - **Name:** `LW-orchestrator`
            - **Permissions:** Full access (default)
            - Click Create
            
            **Copy the key IMMEDIATELY** — `sk-ant-api03-...` format. This is the only time you'll see it.
            
            Save in 1Password as `LW-Claude API key` (Secure Note or API Credential type).
            
            ## Verification
            
            API key in 1Password. Test it:
            
            ```
            curl https://api.anthropic.com/v1/messages \
              -H "x-api-key: $LW_CLAUDE_KEY" \
              -H "anthropic-version: 2023-06-01" \
              -H "content-type: application/json" \
              -d '{"model":"claude-sonnet-4-6","max_tokens":50,"messages":[{"role":"user","content":"Say hi"}]}'
            ```
            
            Should return a response with "hi" in the content.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">52</property>
          <title>52 — Fund Anthropic with starter credit</title>
          <content>
            ## What to do
            
            In Console → Billing → Plans & Billing.
            
            - Create Privacy.com card: `LW-Anthropic`, lock to `anthropic.com`, limit $200/mo
            - Save to `LW-Anthropic virtual card` in 1Password
            - Pre-pay $20-50 in credits
            
            ## Why pre-pay vs pay-as-you-go
            
            Pre-paid credits give you a hard ceiling — runaway API loops can't exceed credit balance. Auto-recharge is convenient but risky for new projects. Set auto-recharge ON later once you know your burn rate.
            
            ## Verification
            
            Account shows $20-50 in available credit.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">51</property>
          <title>51 — Sign up Anthropic Console (Claude API)</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://console.anthropic.com](https://console.anthropic.com).
            
            - Sign Up with `claude@latticeworks.<TLD>`
            - Password from 1Password, save to `LW-Anthropic account`
            - Email verification via Migadu catch-all
            - Phone verification: use `LW-Phone` (Card 6 from Page 01)
            
            ## Verification
            
            Console accessible.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
