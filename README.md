# LatticeWorks

Isolated 12-component creator platform. Code, configs, and architectural decisions live here; the operational playbook (120 setup steps, kanban) lives in Craft.

## Architecture

- **3→1 persona pivot.** Claude handles orchestration, CRM, and Twitter. Llama and Flux run explicitly on RunPod.
- **12-component isolated platform.** Each component is self-contained; the Craft playbook documents setup per page.
- **Conversion path.** Twitter DM → Telegram. Monetization via Telegram Stars + crypto tipping, quote-based pricing.
- **Shoutout management module.** Aged-account vendor DB, conversion tracking, SFS, recommender; compliance + alerts.
- **Pricing tiers.** $245–$852/mo.
- **Market window.** 12–18 months (validated 2026-06-01).

## Layout

```
/opt/latticeworks.io/
├── craft-pages.json    # Craft folder + per-page doc/collection IDs
├── README.md
└── .gitignore
```

`craft-pages.json` is symlinked from `~/.config/craft/latticeworks-ids.json` so existing Craft helpers keep working.

## Craft playbook

Folder: `50527e79-f818-7a20-700f-d6d0596216ac`
Start here doc: `6a3f32df-1168-296f-4d1d-c97188cd2cd2`

12 pages, 10 steps each. Pages 01, 09, 10, 11, 12 have kanban collections. Page 01 is the workspace setup page.

## Status

Brownfield design phase. Playbook authored 2026-06-02. No code shipped yet.

## Git

Local repo, no remote. Not part of the upfrontops org.
