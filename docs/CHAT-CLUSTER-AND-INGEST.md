# Chat Cluster & Ingest (ChatGPT / Claude at scale)

Version: 1.0.0 · 2026-08-10

## Goal

Recover signal from **hundreds to thousands** of ChatGPT (and Claude) conversations into Starlight Idea Swarm + second brain — without context death and without leaking private data.

## Estate SSOT for export → vault

**Do not reinvent ingest.** Use `frankxai/second-brain-os`:

- Operator guide: `second-brain-os/docs/ingestion-guide.md`
- CLI: `sbo-ingest path/to/conversations.json`
- Dual-write:
  - `private/chat-history/{platform}/...` (full raw; MCP cannot resolve)
  - `brain/_inbox/{platform}/...` (summary + insights; agent-readable)

ChatGPT path: Settings → Data Controls → Export data → ZIP with `conversations.json`.

## Idea Swarm layer (after vault write)

```text
second-brain inbox
        ↓
Clusterer (kura-style labeling + recursive clusters)
        ↓
Theme map + ranked opportunity list
        ↓
Idea cards (this repo) for top clusters
        ↓
Debate loop + GitHub alignment
```

## Kura (jxnl/kura) pattern absorb

From open-source chat analysis (CLIO-inspired):

1. **Label** each conversation (intent, domain, urgency, brand: Starlight|Arcanea|GenCreator|FrankX|personal).
2. **Embed** summaries only (never raw private dumps into public indexes).
3. **Recursive cluster** → hierarchy of themes.
4. **Surface** pain points + product opportunities + roadmap candidates.

Implementation posture:
- Prefer calling a **local/scripted** cluster pipeline in this repo or second-brain when ready.
- Optional research dependency: study `https://github.com/jxnl/kura` API shapes before any install.
- Install only after Queen absorb gate (license, sandbox, cost, rollback).

## Hermes-native capture (no export)

When user pastes an idea or chat slice in Hermes/Telegram:

```bash
python scripts/idea_swarm_intake.py --text "..." --source hermes --tags "arcanea,product"
```

Writes:
- Idea card under `docs/ideas/`
- Optional enqueue payload for swarm-bus
- Stub GitHub issue body under `docs/ideas/_outbox/`

## Batch hygiene cron (design)

- Workdir: verified child repo (never home)
- Prompt self-contained: import pending exports if path provided; cluster inbox; open capture issues; write queen report
- Deliver: local or origin digest
- No auto-public publish

## Privacy

- Private tier never enters public GitHub issue bodies  
- Redact emails, phone, health, finance, credentials  
- Cluster reports use aggregates + sanitized examples  
