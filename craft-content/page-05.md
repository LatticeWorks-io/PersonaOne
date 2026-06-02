<page id="02297da2-f2e8-9404-2c28-63098264278c">
  <pageTitle>Page 05 — RunPod + storage + CDN</pageTitle>
  <content>
    # Page 05 — RunPod + storage + CDN
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Set up GPU compute (RunPod), object storage (Backblaze B2), and CDN (BunnyCDN). ~90 minutes. Requires Page 04 complete (server exists for SSH testing).
    
    <collection>
      <title>Page 05 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">50</property>
          <title>50 — Final check before Page 06</title>
          <content>
            ## Confirm
            
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
            
            Drag to Done. Open **Page 06 — AI APIs (Claude, OpenRouter, Postmark)**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">49</property>
          <title>49 — Smoke test: upload to B2, fetch via Bunny</title>
          <content>
            ## What to do
            
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
            - B2 bucket may need `Public` if you're not using signed URLs (you'll handle signing in app code later — for smoke test you can temporarily flip to Public)
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">48</property>
          <title>48 — Create a Pull Zone in Bunny connected to B2</title>
          <content>
            ## What to do
            
            In BunnyCDN dashboard → Pull Zones → Add Pull Zone:
            
            - **Name:** `lw-content`
            - **Origin URL:** the B2 bucket endpoint, e.g., `https://lw-content-prod.s3.us-west-001.backblazeb2.com`
            - **Pricing Tier:** Standard (lowest cost)
            - **Geographic Regions:** Tick North America + Europe (your audience). Skip Asia/Africa/SA for now (3-12x more expensive).
            - Click Add
            
            This creates a Pull Zone with a URL like `lw-content.b-cdn.net`. Files in your B2 bucket are now reachable via that CDN URL.
            
            ## Verification
            
            Pull Zone shows in BunnyCDN dashboard with status `Active`.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">47</property>
          <title>47 — Sign up BunnyCDN</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://bunny.net](https://bunny.net).
            
            - Sign Up with `bunny@latticeworks.<TLD>`
            - Strong password from 1Password, save to `LW-BunnyCDN account`
            - Email verification arrives, click verify
            - Fund account with $10-20 (Privacy.com card `LW-BunnyCDN`)
            
            ## Verification
            
            BunnyCDN dashboard accessible, balance ~$10-20.
            
            
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">46</property>
          <title>46 — Generate B2 application keys</title>
          <content>
            ## What to do
            
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
            
            Keys saved in 1Password. You cannot recover the applicationKey if you lose it.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">45</property>
          <title>45 — Create your first B2 bucket</title>
          <content>
            ## What to do
            
            In B2 dashboard → Buckets → Create a Bucket:
            
            - **Bucket Unique Name:** `lw-content-prod` (or `lw-<persona>-content`)
            - **Files in Bucket are:** Private (NOT Public — you'll serve via CDN with signed URLs)
            - **Default Encryption:** Disable (we'll handle encryption at the app layer if needed)
            - **Object Lock:** Disable
            - Click Create
            
            ## Verification
            
            Bucket exists in B2 dashboard.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">44</property>
          <title>44 — Sign up Backblaze B2 (object storage)</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://www.backblaze.com/cloud-storage](https://www.backblaze.com/cloud-storage).
            
            - Click "Sign Up" → choose B2 Cloud Storage
            - Email: `b2@latticeworks.<TLD>`
            - Password from 1Password, save to `LW-Backblaze account`
            - Verification email arrives, click verify
            
            ## Verification
            
            B2 dashboard accessible.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">43</property>
          <title>43 — Test-deploy a simple pod (smoke test)</title>
          <content>
            ## What to do
            
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
            
            Or **Terminate** if you don't need to keep the configuration.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">42</property>
          <title>42 — Fund RunPod with starter credit</title>
          <content>
            ## What to do
            
            In RunPod dashboard → Billing → Add Credit.
            
            - Create new Privacy.com card: `LW-RunPod`, lock to `runpod.io`, limit $100/mo
            - Save to 1Password as `LW-RunPod virtual card`
            - Add $30-50 starter credit (you'll use it slowly during build/test phases)
            
            ## Why pay-as-you-go (not commit pricing)
            
            RunPod offers Savings Plans (committed monthly spend for discount). Don't commit yet — you don't know your usage pattern. Start with PAYG; commit later if usage justifies it.
            
            ## Verification
            
            RunPod shows balance ~$30-50.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">41</property>
          <title>41 — Sign up RunPod (GPU compute)</title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://runpod.io](https://runpod.io).
            
            - Sign up with `runpod@latticeworks.<TLD>`
            - Strong password from 1Password, save to `LW-RunPod account`
            - Email verification arrives via Migadu catch-all → click verify link
            
            ## Verification
            
            RunPod dashboard accessible. Login in 1Password.
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
