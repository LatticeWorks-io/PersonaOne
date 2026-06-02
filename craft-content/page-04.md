<page id="b8b8785d-443b-e58b-a547-2090a64a33ca">
  <pageTitle>Page 04 — Provision Hostwinds dedicated box</pageTitle>
  <content>
    # Page 04 — Provision Hostwinds dedicated box
    
    <callout>**Before working this page:** click the collection block below → `...` menu → **View** → **Kanban**. Three columns appear: Todo / In Progress / Done. Drag cards across as you work them.</callout>
    
    **Goal:** Stand up the production server where orchestration / Postgres / bots will run. ~2 hours + provisioning wait. Requires Page 03 complete (you'll use `hostwinds@latticeworks.<TLD>`).
    
    <collection>
      <title>Page 04 Microsteps</title>
      <properties>status, step</properties>
      <content>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">40</property>
          <title>40 — Final check before Page 05</title>
          <content>
            ## Confirm
            
            - [ ] Hostwinds dedicated server provisioned and running
            - [ ] Server IP saved in 1Password under `LW-Hostwinds server`
            - [ ] SSH key (Ed25519) generated, public key on server, private key in 1Password
            - [ ] `ssh lw-host` works via key auth (no password prompt)
            - [ ] Password authentication is disabled (only key auth works)
            - [ ] Firewall (ufw) is active, allowing 22/80/443
            - [ ] fail2ban is running
            
            ## Why this matters for Page 05
            
            Page 05 sets up RunPod (GPU compute) + storage (Backblaze B2) + CDN (BunnyCDN). Some of these signups will use your server's IP for whitelisting. Easier to have it provisioned and hardened first.
            
            ## All 7 boxes checked?
            
            Drag to Done. Open **Page 05 — RunPod + storage + CDN**.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">39</property>
          <title>39 — Install firewall + basic hardening</title>
          <content>
            ## What to do
            
            On the Hostwinds server:
            
            ```
            # Update first
            sudo apt update && sudo apt upgrade -y
            
            # Install ufw firewall
            sudo apt install -y ufw fail2ban
            
            # Default deny incoming, allow outgoing
            sudo ufw default deny incoming
            sudo ufw default allow outgoing
            
            # Allow SSH (port 22 or whatever you set)
            sudo ufw allow 22/tcp
            
            # Allow HTTP/HTTPS (for webhook receivers etc.)
            sudo ufw allow 80/tcp
            sudo ufw allow 443/tcp
            
            # Enable firewall
            sudo ufw enable
            
            # Verify
            sudo ufw status
            ```
            
            Enable fail2ban (auto-bans IPs that try to brute-force SSH):
            
            ```
            sudo systemctl enable fail2ban
            sudo systemctl start fail2ban
            ```
            
            ## Verification
            
            `sudo ufw status` shows active with rules for 22, 80, 443. `sudo systemctl status fail2ban` shows running.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">38</property>
          <title>38 — Harden SSH config and disable password auth</title>
          <content>
            ## What to do
            
            On the Hostwinds server (via `ssh lw-host`):
            
            ```
            # Edit SSH config
            sudo nano /etc/ssh/sshd_config
            ```
            
            Set/change:
            
            - `PermitRootLogin prohibit-password` (allows root via key, blocks password)
            - `PasswordAuthentication no`
            - `PubkeyAuthentication yes`
            - `Port 22` (or change to nonstandard like 2222 if you want — note in 1Password)
            
            Save (Ctrl+O, Enter, Ctrl+X).
            
            Reload SSH:
            
            ```
            sudo systemctl restart ssh
            ```
            
            **Before disconnecting**, open a SECOND terminal and verify `ssh lw-host` still works. If it doesn't, the first session is still alive and you can revert.
            
            ## Verification
            
            Second SSH session connects via key. Password auth is rejected (`ssh root@<ip>` with no key fails).
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">37</property>
          <title>37 — First SSH connection and add public key</title>
          <content>
            ## What to do
            
            Update `~/.ssh/config` with the server IP from Card 36:
            
            ```
            Host lw-host
              HostName <SERVER-IP-FROM-CARD-36>
              User root
              IdentityFile ~/.ssh/latticeworks_ed25519
              IdentitiesOnly yes
            ```
            
            In your Mac terminal:
            
            ```
            # First-time login uses password (not SSH key yet)
            ssh root@<SERVER-IP>
            # Enter initial root password from Hostwinds email
            ```
            
            You're in. Now add your SSH public key:
            
            ```
            mkdir -p ~/.ssh
            chmod 700 ~/.ssh
            cat >> ~/.ssh/authorized_keys << 'EOF'
            <paste contents of ~/.ssh/latticeworks_ed25519.pub here>
            EOF
            chmod 600 ~/.ssh/authorized_keys
            ```
            
            Exit SSH session. Try logging in again:
            
            ```
            ssh lw-host
            ```
            
            Should login without password (using your SSH key).
            
            ## Verification
            
            `ssh lw-host` works without a password. You're in via key auth.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">36</property>
          <title>36 — Wait for provisioning + get server IP</title>
          <content>
            ## What to do
            
            Hostwinds dedicated provisioning takes 5-30 minutes (sometimes up to 2 hrs depending on load).
            
            You'll get an email at `me@latticeworks.<TLD>` when provisioning is complete, with:
            
            - Server IP address
            - Root password (initial)
            - Optional: SSH access details
            
            When the email arrives:
            
            - Save the IP address in 1Password under `LW-Hostwinds server` (Server tab)
            - Save the initial root password in 1Password (you'll change it in Card 38)
            
            ## Verification
            
            You have the server IP and initial root password in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">35</property>
          <title>35 — Generate a new SSH keypair for LatticeWorks</title>
          <content>
            ## What to do
            
            On your Mac terminal (NOT your existing SSH key — generate a NEW one for LatticeWorks isolation):
            
            ```
            ssh-keygen -t ed25519 -C "latticeworks-admin" -f ~/.ssh/latticeworks_ed25519
            ```
            
            When prompted for passphrase: **set a strong one** (save in 1Password under `LW-SSH key passphrase`). Don't leave it empty.
            
            This creates:
            
            - `~/.ssh/latticeworks_ed25519` (private key)
            - `~/.ssh/latticeworks_ed25519.pub` (public key)
            
            ## Save to 1Password
            
            1Password supports SSH keys natively. In LatticeWorks vault:
            
            - New Item → SSH Key
            - Drag in `~/.ssh/latticeworks_ed25519` (private key)
            - Name: `LW-SSH admin key`
            - Save
            
            ## Configure SSH agent
            
            Add to `~/.ssh/config`:
            
            ```
            Host lw-host
              HostName <will-fill-in-Card-37>
              User root
              IdentityFile ~/.ssh/latticeworks_ed25519
              IdentitiesOnly yes
            ```
            
            ## Verification
            
            `ls ~/.ssh/latticeworks_ed25519*` shows both files. 1Password has the SSH key item.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">34</property>
          <title>34 — Create Privacy.com card for Hostwinds and pay</title>
          <content>
            ## What to do
            
            In Privacy.com (LatticeWorks Chrome profile):
            
            - **Type:** Merchant Locked
            - **Name:** `LW-Hostwinds`
            - **Spend limit:** $200 (covers monthly + headroom for surprise add-ons)
            - **Merchant lock:** `hostwinds.com`
            
            Save in 1Password under `LW-Hostwinds virtual card`.
            
            Back in Hostwinds checkout, pay with this card. Choose monthly billing (annual is cheaper but locks you in before you know if it's the right pick).
            
            ## Verification
            
            Order placed. Confirmation email in Migadu inbox.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">33</property>
          <title>33 — Pick dedicated server config</title>
          <content>
            ## What to do
            
            In Hostwinds dashboard → Servers → **Dedicated Server** → Configure.
            
            **Entry-level dedicated config for LatticeWorks:**
            
            - **CPU:** Xeon E3-1230v6 or equivalent (4 cores, 8 threads) — sufficient for orchestrator + Postgres + bot
            - **RAM:** 16 GB minimum, 32 GB ideal
            - **Storage:** 240 GB SSD primary + optional 1 TB HDD secondary (for content backups)
            - **Bandwidth:** 10 TB/mo unmetered (Hostwinds default)
            - **OS:** Ubuntu 24.04 LTS (long-term support, cleanest for Docker)
            - **Datacenter:** Seattle (closer to Pacific if you're US West Coast) or Dallas (central US)
            
            Expected price: ~$120-150/mo.
            
            ## Why dedicated > VPS for this
            
            You'll run: Postgres, pgvector, Redis, Telegram bot, Twitter bot, scheduled job workers, web-scraping workers, plus ComfyUI orchestration. Together they oversubscribe a VPS's noisy-neighbor I/O. Dedicated = predictable performance.
            
            ## Verification
            
            Server config in cart, total ~$120-150/mo. Don't checkout yet — Card 34 covers payment.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">32</property>
          <title>32 — Sign up Hostwinds with hostwinds@latticeworks.<TLD></title>
          <content>
            ## What to do
            
            In LatticeWorks Chrome profile, go to [https://www.hostwinds.com](https://www.hostwinds.com).
            
            - Click Sign Up / Get Started
            - **Email:** `hostwinds@latticeworks.<TLD>` (this works because of catch-all from Page 03 Card 29)
            - **Password:** strong unique from 1Password
            - Save login in 1Password under `LW-Hostwinds account`
            - Verify the confirmation email arrives in your Migadu inbox (it'll route via catch-all to `me@`)
            
            ## Verification
            
            Hostwinds dashboard accessible, login in 1Password.
          </content>
        </collectionItem>
        <collectionItem>
          <property name="status">Todo</property>
          <property name="step">31</property>
          <title>31 — Decide: Hostwinds or OVH (final pick)</title>
          <content>
            ## What to do
            
            Re-confirm the host pick based on your priorities:
            
            |  | Hostwinds | OVH (US/Canada) |
            | --- | --- | --- |
            | Entry dedicated price | $122/mo | $66.50/mo |
            | Adult-industry posture | Markets to adult (explicit-friendly heritage) | Allows via AUP (not adult-marketed) |
            | Hardware per dollar | Decent | Better |
            | Support response | Old-school, slower | Faster, more technical |
            
            **Recommendation: Hostwinds** if you want zero abuse-team risk and don't mind paying ~$60/mo more. **OVH (BHS Canada)** if you want better hardware-per-dollar and accept the slight abuse-team posture difference.
            
            Write your final pick in 1Password under `LW-Host decision`.
            
            ## Verification
            
            Decision documented. Move to Card 32 (rest of cards assume Hostwinds; if OVH, the steps are nearly identical but the UI looks different).
          </content>
        </collectionItem>
      </content>
    </collection>
  </content>
</page>
