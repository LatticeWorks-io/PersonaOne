<page id="b3d122eb-9864-4855-5d0d-cf0331c76926">
  <pageTitle>Page 07 — NowPayments + crypto wallet</pageTitle>
  <content>
    # Page 07 — NowPayments + crypto wallet
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Set up the payment processor (NowPayments merchant account) + crypto wallet that receives payouts. Includes 1-3 day KYC wait. Requires Page 03 complete.
    
    <collection>
      <title>Page 07 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">70</property>
          <title>70 — Final check before Page 08</title>
          <content>
            ## Confirm
            
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
            
            Drag to Done. Open **Page 08 — Telegram setup**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">69</property>
          <title>69 — Test crypto payment flow end-to-end</title>
          <content>
            ## What to do
            
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
            
            You paid $1 + ~$0.10 in network fees + ~$0.005 NowPayments fee. Cheap smoke test.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">68</property>
          <title>68 — Wait for KYC approval (1-3 business days)</title>
          <content>
            ## What to do
            
            KYC review typically takes 1-3 business days.
            
            While waiting:
            
            - Don't reapply or contact support unless 5+ business days pass
            - Don't try to do test transactions yet
            - Move on to Page 08 (Telegram setup) — that's independent
            
            When approval email arrives at `me@latticeworks.<TLD>`:
            
            - Save the approval timestamp in 1Password under `LW-NowPayments account` notes
            - Status in dashboard updates to `Approved`
            
            ## Verification
            
            Email confirming approval. Dashboard status `Approved`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">67</property>
          <title>67 — Submit KYC documents</title>
          <content>
            ## What to do
            
            NowPayments requires KYC for merchant accounts (this is the gate to processing real money).
            
            Documents you'll need:
            
            - **Government-issued photo ID** (driver's license or passport)
            - **Selfie** with the ID held visible (NowPayments will prompt for this in their KYC flow)
            - **Proof of business:** depends on your tax structure from Page 01 Card 8
              - If existing LLC: LLC formation document + EIN
              - If new LLC: same once formed
              - If 1099: your SSN + a recent utility bill
            
            In LatticeWorks Chrome profile, complete NowPayments KYC flow. Upload via their portal.
            
            ## Why KYC is required
            
            NowPayments is a regulated MSB (Money Services Business). They must KYC merchants under AML laws. There's no way around this. Your real identity is on the merchant account — but the customer-facing brand can still be the persona.
            
            ## Verification
            
            KYC submitted. Status in dashboard shows `Pending review`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">66</property>
          <title>66 — Add your crypto wallet as payout destination</title>
          <content>
            ## What to do
            
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
            
            At least one wallet (USDT-TRC20 recommended) verified in NowPayments.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">65</property>
          <title>65 — Sign up NowPayments</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://nowpayments.io](https://nowpayments.io).
            
            - Sign Up with `pay@latticeworks.<TLD>`
            - **Important:** during signup, choose **Merchant** account type (not Individual)
            - Strong password from 1Password, save to `LW-NowPayments account`
            
            ## Verification
            
            NowPayments dashboard accessible. Account type shows Merchant.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">64</property>
          <title>64 — Get your wallet address for NowPayments</title>
          <content>
            ## What to do
            
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
            
            Wallet addresses saved in 1Password. You can paste them into NowPayments in Card 66.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">63</property>
          <title>63 — Secure the recovery phrase</title>
          <content>
            ## What to do
            
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
            
            You can demonstrate (to yourself) that you have the seed in two physical locations + split across 2 1Password notes.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">62</property>
          <title>62 — Install + set up your hot wallet (Phantom)</title>
          <content>
            ## What to do
            
            Two installs to make it cross-device:
            
            ### Mac (LatticeWorks Chrome profile)
            
            - chrome.google.com/webstore → search Phantom → install extension
            - Open extension → Create New Wallet (NOT Import)
            - Set a strong password (save in 1Password under `LW-Phantom wallet password`)
            - Phantom shows your **12-word recovery phrase** — write it down on PAPER (not in 1Password — see Card 63)
            - Verify the phrase by typing back into Phantom
            
            ### iPhone (Chrome — LatticeWorks profile)
            
            - App Store → install Phantom app
            - Sign in using the recovery phrase from above (same wallet across devices)
            
            ## Verification
            
            Phantom shows your wallet with $0 balance on both devices. Both show the same wallet address.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">61</property>
          <title>61 — Decide crypto wallet strategy</title>
          <content>
            ## What to do
            
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
            
            Strategy documented in 1Password.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
