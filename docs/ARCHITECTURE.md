# Starlight Genius Forge — Architecture

**Class-level sovereign architecture** for the talent discovery, competition, builder, and HNW matching platform. Composes existing ecosystem components without fragmentation.

## High-Level Layers

1. **Intelligence Substrate (Starlight SIS)**
   - Persistent memory, governance, agent orchestration, evals (Starlight-Intelligence-System, starlight-memory, starlight-evals, starlight-swarm, starlight-command).
   - All core logic runs as named agent swarms/guilds with handover protocols (agentic-ops).
   - Sovereign/local-first options + premium hosted layers.

2. **Creator OS Layer (GenCreator / ACOS)**
   - GenCreator-OS (Next.js canvas, Remotion studio, teleprompter, Exchange marketplace).
   - agentic-creator-os + creator-intelligence-system (SIP-conformant substrate).
   - Role-based provisioning for talent (Builder, Creator, Solution Engineer) and HNW (Investor, Syndicator, Mentor).

3. **Creative Execution (Arcanea)**
   - arcanea + arcanea-ai-app + arcanea-code (Guardian-routed CLI).
   - Lore, worldbuilding, multimedia, design challenges as first-class competition tracks.

4. **Talent & HNW Matching (Dream100 + Investor Skills)**
   - Extended Dream100 patterns for global genius lists (JP/PH/ID priority).
   - awesome-investor-agent-skills for curated deal flow, syndication, matching.
   - Agent-assisted outreach, CRM in GitHub issues/JSON, VA layer.

5. **Frontend / Portal**
   - Next.js app (extend patterns from gencreator.ai, arcanea-ai-app, frankx.ai-vercel-website).
   - Submission portal, competition dashboard, investor deal room, talent profiles.
   - Supabase auth + real-time.

6. **Data & Memory**
   - Supabase: talent profiles, submissions, competition history, matches, funding events.
   - Starlight memory contracts: long-term context, eval history, relationship graphs (talent ↔ HNW ↔ projects).
   - Privacy-first: public signals only for discovery; consent for stored profiles.

## Agent Swarms / Guilds (Core Workflows)

See docs/AGENTS.md for detailed roles and prompts.

- **Discovery Guardians**: Ethical public-signal scouting + submission analysis. Score on genius signals (technical depth, creativity, resilience despite constraints), location priority (JP/PH/ID), fit with ecosystem.
- **Competition Judges**: Rubric-based LLM + community eval. Multi-stage pipelines. Bias mitigation via 6-Pillar Ethics.
- **Builder Delegates**: Project scoping, delegation to arcanea-code / Claude Code / Codex, integration with GenCreator Studio/Remotion, skill recommendations from marketplace.
- **Investor Matchmakers**: Profile matching using investor-agent-skills, deal flow curation, syndication workflows, success tracking.
- **Community Sentinels**: Onboarding, moderation, event orchestration, guild health (Telegram/Discord/custom).
- **Governance Overseers**: 6-Pillar enforcement, ethics audits, compliance, eval of platform fairness.

## Data Models (High-Level)

- **TalentProfile**: id, name, location (JP/PH/ID signals), skills[], github/x/linkedin/portfolio, past_impact, constraints_notes (public), genius_score, status, matches[].
- **Competition**: id, theme, stages[], rubric, start/end, participants[], winners[], funding_pool.
- **Submission**: id, talent_id, competition_id, project_description, artifacts[], eval_scores[], status.
- **Match**: id, talent_id, hnw_id, project_id, type (mentorship/funding/partnership), status, value.
- **HNWProfile**: id, type (investor/entrepreneur/etc.), interests[], deal_flow_preferences, past_deals[], agent_config.

Integrations documented in docs/INTEGRATIONS.md.

## Monetization & Tiers (Starlight Patterns)

- **Free / Open Core** (talent): Discovery, basic competitions, builder tools, community access.
- **Premium SaaS** (HNW / serious talent): Advanced matching, private guilds, sponsored comp access, usage-based agent compute (Polar.sh).
- **Marketplace Cuts**: Success fees on funded projects, skill/swarms sales via Exchange.
- **Sponsored Competitions**: Corporate / HNW sponsorships.

Usage-based + tiered, sovereign by default.

## GTM & Launch

See docs/GTM-PLAN.md.

Pilot: 3 competitions focused on target regions, value-first content on frankx.ai/arcanea.ai, HNW onboarding via existing investor skills.

## Sovereign Principles

- Local-first options for memory/data.
- Open protocols where possible (forkable swarms, skills).
- 6-Pillar CoE on every artifact.
- No user-run commands — full autonomous execution patterns.

This architecture ensures Starlight Genius Forge is a **compounding moat** within the existing ~40-repo empire rather than a new silo.
