---
name: idea-swarm
description: "Use when capturing, clustering, refining, debating, aligning, or monetizing ideas via Starlight Idea Swarm (Queen-led). ChatGPT/Claude scale ingest, Kura-style clusters, planner-executor-critic debate, GitHub roadmap alignment. Trigger: Idea Swarm, idea intake, chat export ideas, multi-agent idea debate."
version: 1.0.0
author: Frank Riemer + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [idea-swarm, idea-forge, genius-forge, swarm, queen, second-brain, chatgpt, kura, multi-cli, starlight]
    related_skills:
      - agent-workspace-bootstrap
      - starlight-idea-forge
      - starlight-queen
      - coding-agents
      - todo-discipline
      - swarm-comms-protocol
      - multi-repo-portfolio-swarm
      - github-issues
      - starlight-second-brain-os
      - premium-web-os
---

# Starlight Idea Swarm (operator skill)

Canonical doctrine: `docs/IDEA-SWARM.md` in `frankxai/starlight-genius-forge`.

**Alias:** Idea Forge skill remains valid; this skill is the Swarm-facing operator entry.

## When to use

- User dumps ideas / pastes ChatGPT threads / wants export → durable system
- "Idea Swarm", multi-agent refine, roadmap alignment, proactive idea hygiene
- Naming preference: Swarm over Forge for general ideas
- Queen massive-action idea campaigns

## Hard rules

1. `agent-workspace-bootstrap` + 4-fact git before writes
2. Chat export ingest via **second-brain-os** `sbo-ingest` first when full dumps
3. Debate triad (Planner/Executor/Critic) before GitHub or roadmap mutations
4. Native Grok/xAI images only if media needed; default text under BOUNDED/TIGHT
5. Compose estate repos — no new top-level OS
6. Todo merge=true + read before handover

## Procedure

1. **Classify** brand/domain + idea class  
2. **Capture** — `python scripts/idea_swarm_intake.py` or vault write + IdeaCard under `docs/ideas/`  
3. **Cluster** (batch) — kura-style labels over inbox themes (`docs/CHAT-CLUSTER-AND-INGEST.md`)  
4. **Refine** — multi-CLI compete via `coding-agents`  
5. **Quantify** — scorecard from IDEA-SWARM / IDEA-FORGE  
6. **Debate** — follow `docs/DEBATE-LOOP.md`; Critic PASS required  
7. **Align** — `github-issues` + portfolio scan; labels `idea-swarm`  
8. **Execute / Document / Monetize** — correct product repo only  
9. **Receipt** — `starlight/queen/reports/idea-swarm-YYYY-MM-DD.md`  

## Queen topology (default)

```text
Queen (Hermes)
  ├─ Planner leaf
  ├─ Executor leaves (≤2 concurrent when admitted)
  ├─ Critic leaf (independent)
  └─ Aligner leaf (gh + roadmaps)
```

Enqueue C940 only for backend/GitOps weight. Never forge peer heartbeats.

## UI

Premium cockpit shell: `ui/idea-swarm-cockpit.html` — open in browser for visual baseline; product Next surface can absorb later under Premium Web OS.

## Compat

Load `starlight-idea-forge` for football/domain modules and Genius talent track details.
