## Summary

Promotes **Starlight Idea Swarm** as the canonical product face for idea capture → cluster → debate → GitHub/roadmap alignment, while keeping Genius Forge as the talent track and Idea Forge as a compatibility alias.

### Why

- Centralize hundreds/thousands of ChatGPT chats via second-brain ingest + Kura-style clustering patterns
- Highest-intelligence multi-agent refinement using Planner / Executor / Critic (Kura AI debate architecture pattern)
- Compose estate stack (Queen, coding-agents, portfolio swarm, Premium Web OS) instead of new fragmented OS
- Premium static cockpit shell for SOTA aesthetics baseline

### Artifacts

- `docs/IDEA-SWARM.md` — SSOT
- `docs/DEBATE-LOOP.md`, `docs/CHAT-CLUSTER-AND-INGEST.md`, `docs/ABSORB-CANDIDATES.md`
- `skills/idea-swarm/SKILL.md`
- `scripts/idea_swarm_intake.py` (executed locally; sample idea card included)
- `ui/idea-swarm-cockpit.html`

### Explicit non-goals in this PR

- No install of trykura.com SaaS or random agent frameworks
- No production deploy
- No dirty second-brain-os branch edits

### Test plan

- [x] `python scripts/idea_swarm_intake.py --text ...` creates card + outbox issue body
- [x] `python -m py_compile scripts/idea_swarm_intake.py`
- [ ] Visual open `ui/idea-swarm-cockpit.html` in browser
- [ ] Optional: real ChatGPT export through second-brain `sbo-ingest`

Receipt: `starlight/queen/reports/idea-swarm-massive-action-2026-08-10.md`
