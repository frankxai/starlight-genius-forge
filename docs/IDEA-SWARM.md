# Starlight Idea Swarm

**Product face (2026-08-10):** Starlight Idea Swarm  
**Legacy / internal track name:** Idea Forge · Genius Forge (talent track only)  
**Repo:** `frankxai/starlight-genius-forge`  
**Orchestrator:** Starlight Queen (`/si` · `starlight-queen`)  
**Memory substrate:** `second-brain-os` + SIS private memory  
**Version:** 2.0.0 · 2026-08-10

---

## 1. Naming decision

| Name | Role | Status |
|------|------|--------|
| **Starlight Idea Swarm** | Public product + operator face | **Canonical** |
| Idea Forge | Lifecycle process docs / skill alias | Compatibility |
| Genius Forge | Talent discovery + competitions + HNW track | Nested specialty track |
| Starlight Idea OS | Optional future product shell name | Reserved |

**Why not only "Forge":** Forge reads industrial/talent-only. Swarm matches SIS, Queen multi-agent truth, and the debate topology. Keep Genius Forge for the talent market track so HNW/GTM docs stay valid.

---

## 2. Purpose

Turn raw sparks — Hermes chat, ChatGPT/Claude exports, X signals, self-submit — into **Git-backed, roadmap-aligned, multi-agent-tested, monetizable assets** without fragmenting Starlight / GenCreator / Arcanea / FrankX.

Highest bar:
- Sovereign second brain (local vault + MCP privacy contract)
- Queen-led multi-agent debate (planner · executor · critic)
- GitHub issues/Projects + portfolio roadmaps as living alignment plane
- Premium UI/UX aesthetics (Premium Web OS + design intelligence)
- Proactive loops (cron + swarm-bus + skill hooks) — not one-off chats

---

## 3. External SOTA absorbed (patterns only — no blind installs)

### 3.1 jxnl/kura (chat data intelligence)

Open-source chat analysis inspired by Anthropic CLIO:
- Label conversations with LLMs
- Recursive embedding clusters
- Surface patterns, pain points, opportunities across **thousands** of chats

**Absorb into Idea Swarm:**
- Batch ChatGPT/Claude export → cluster map → idea candidates
- Cluster themes become portfolio goals or roadmap themes
- Never ship secrets; private tier stays in second-brain `private/`

### 3.2 Kura AI YC S24 (browser agent debate)

Multi-agent **planner + executor + critic** debating each action (vision + DOM), SOTA-class self-heal/backtrack on WebVoyager-class tasks.

**Absorb into Idea Swarm (idea domain, not browser automation as default product):**
- Every high-value idea step runs **Planner → Executor → Critic debate**
- Critic can force backtrack before GitHub issue or roadmap write
- Optional later: browser lane only when web research/validation requires CUA (Hermes computer-use / Skyvern-class) under separate admission

### 3.3 Second brain SOTA (estate + market)

- Own stack: `second-brain-os` already implements Claude + ChatGPT export → dual-write (`private/` + `brain/_inbox/`)
- Market patterns (Taskade, Archon+second-brain, Mem0, GraphRAG): notes → knowledge → **action**
- Idea Swarm is the **action + swarm** layer on top of the vault

### 3.4 Explicit non-absorb (now)

| Candidate | Why hold |
|-----------|----------|
| trykura.com production browser SaaS | Paid external; browser SOTA not core idea SSOT |
| Random agent frameworks (AutoGen/CrewAI full replace) | Estate already has Queen + coding-agents + Hermes |
| New top-level home clones | Bootstrap ban |
| Media fanout under BOUNDED/TIGHT | Text-first |

Promotion rule: license/security intake → sandbox → baseline → cost ceiling → rollback → Queen verdict before install.

---

## 4. Lifecycle (unchanged stages, Swarm topology)

| Stage | Goal | Swarm roles | Exit |
|-------|------|-------------|------|
| 1 Capture | Ingest sparks + exports | Cartographer + Ingest | Idea card + provenance |
| 2 Cluster | Kura-style theme map | Clusterer | Cluster map + ranked themes |
| 3 Refine | Clarify ICP/problem | Planner + multi-CLI briefs | One-page brief |
| 4 Quantify | Scorecard | Quantifier + Critic | Ship bar ≥7 |
| 5 Debate | Planner/Executor/Critic | Debate triad | Approved action plan |
| 6 Align | GitHub + roadmaps | Aligner + portfolio scan | Issue(s) + links |
| 7 Validate | Pilot / evidence | Validator | Evidence pack |
| 8 Execute | Build | coding-agents MCR | Working artifact |
| 9 Document | Vault + repo + queen | Documenter | Searchable SSOT |
| 10 Monetize | Path or free | CRO path | Explicit route |

---

## 5. Debate loop (Kura-inspired)

```text
Planner   → proposes next step + risks + done-when
Executor  → produces artifact (brief, spike, issue body, PR draft)
Critic    → adversarial check (truth, ethics, roadmap fit, cost, slop)
            if FAIL → backtrack to Planner with exact blockers
            if PASS → commit evidence + advance stage
```

Rules:
- Critic cannot be the same model instance as Executor for high-value work when multi-CLI is available.
- No GitHub issue/roadmap edit without Critic PASS receipt.
- Queen reduces final synthesis; never agent-count theater.

---

## 6. Capture surfaces

1. **Hermes / Telegram** — natural language idea → intake skill  
2. **second-brain-os** — `sbo-ingest` for ChatGPT + Claude exports (see their `docs/ingestion-guide.md`)  
3. **Cluster pass** — Idea Swarm script/skill runs kura-style labeling over vault inbox  
4. **GitHub** — issues labeled `idea-swarm` across portfolio  
5. **Queen proactive** — cron scans unfinished agent branches + chat clusters → capture issues  

---

## 7. Alignment plane (GitHub primary)

- Issues: `github-issues` skill — labels `idea-swarm`, `roadmap-align:<repo>`, project links  
- Portfolio: `multi-repo-portfolio-swarm` for cross-repo capture of unfinished agent intents  
- Roadmaps: agents read `ROADMAP.md` / GitHub Projects in connected frankxai repos  
- Work ledger: cross-repo impact in starlight-agent-config progress ledger when required  
- Notion: optional mirror via `notion-operating-system` — **not** SSOT  

---

## 8. Operator loop (Queen)

1. Storage gate (BOUNDED+ preferred)  
2. `agent-workspace-bootstrap` + 4-fact git on this repo or execute target  
3. Load `todo-discipline` + `coding-agents` + `starlight-queen` + this doctrine  
4. Capture → Cluster → Refine → Quantify → Debate → Align → …  
5. Draft PR only; queen receipt under `starlight/queen/reports/idea-swarm-*`  
6. Enqueue C940 only for backend/GitOps when useful (never forge peer)  
7. Todo merge=true + no-parameter read before handover  

---

## 9. Premium UI/UX bar

Apply Premium Web OS (`_intelligence/`) + design-agent-standards:
- Restraint, editorial type, one dominant idea per viewport  
- No AI slop gradients, no fake dashboards as hero  
- Flagship surface: Idea Swarm Cockpit (capture · clusters · debate status · GitHub links)  
- Static composition first; motion only for hierarchy  
- Brand: Starlight signal/material language — not generic SaaS purple  

See `ui/idea-swarm-cockpit.html` for the v0 cockpit shell.

---

## 10. Estate composition (do not fragment)

| Layer | Repo / surface |
|-------|----------------|
| Lifecycle + swarm doctrine | **this repo** |
| Chat export ingest | `second-brain-os` |
| Memory substrate | SIS + `starlight-private-memory` |
| Swarm bus | `agentic-ops` hermes-bus + `agentic-ops-hub` fleet |
| Multi-CLI | `coding-agents` |
| Portfolio GitOps | `multi-repo-portfolio-swarm` |
| Design | `starlight-design-intelligence` + `_intelligence` |
| Queen | `/si` + `starlight-queen` |

---

## 11. Related docs

- `docs/IDEA-FORGE.md` — v1 lifecycle (compat)  
- `docs/DEBATE-LOOP.md` — detailed triad protocol  
- `docs/CHAT-CLUSTER-AND-INGEST.md` — ChatGPT scale + kura patterns  
- `docs/ABSORB-CANDIDATES.md` — research queue / install gates  
- `skills/idea-swarm/SKILL.md` — operator skill  
- `scripts/idea_swarm_intake.py` — CLI intake skeleton  

---

*Starlight Queen · SIS · GenCreator · Arcanea · 6-Pillar CoE*
