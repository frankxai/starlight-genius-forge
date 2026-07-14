# Starlight Genius Forge — Agent Swarms & Guilds

Detailed roles, prompts, and workflows for the sovereign agent layer. All agents run on **Starlight Intelligence (SIS)** + **Hermes profiles** with 6-Pillar CoE governance.

## Core Swarms

### 1. Discovery Guardians (Talent Scouting & Intake)
- **Purpose**: Ethically discover under-represented geniuses, especially JP/PH/ID.
- **Inputs**: Public GitHub/X/LinkedIn/portfolio signals, self-submissions via portal.
- **Process**:
  - Scrape/analyze public data (tools: web_search, open_page, x_search where allowed).
  - Score: Technical depth, creativity/impact, resilience (constraints overcome), location priority, ecosystem fit.
  - Output: TalentProfile JSON + why-fit analysis (Dream100 style).
- **Prompt Template** (example for Claude/Grok):
  ```
  You are a Discovery Guardian in Starlight Genius Forge.
  Analyze this public profile for genius signals despite limited opportunity.
  Focus: JP/PH/ID or similar. Score 1-10 on [dimensions]. Output structured TalentProfile.
  Profile: [data]
  ```
- **Integration**: Feeds Dream100-style lists + SIS memory. Privacy: public data only.

### 2. Competition Judges
- **Purpose**: Fair, high-signal evaluation of competition entries.
- **Stages**: Submission review → AI rubric scoring → Community vote (agent-orchestrated) → Live pitch eval.
- **Rubric** (see docs/TALENT-EVAL-RUBRIC.md): Genius (originality, depth), Execution (build quality, demo), Impact (relevance to theme, scalability), Resilience/Fit (story of constraints overcome), Ecosystem Alignment.
- **Bias Mitigation**: Multiple models + human oversight + Ethics pillar audits.
- **Output**: Scores, feedback, advancement decisions, winner recommendations.

### 3. Builder Delegates
- **Purpose**: Help talent turn ideas into shipped projects using the full stack.
- **Workflow**:
  - Scope project with Visionary Agent Canvas (GenCreator-OS).
  - Recommend MCP servers, skills, swarms from Exchange.
  - Delegate coding to arcanea-code, claude-systematic-workflows, Codex, etc.
  - Studio integration: Remotion video, Arcanea creative assets.
  - Track progress in SIS memory + Supabase.
- **Prompts**: Role-specific for "Code Architect", "Creative Director", "Launch Operator".

### 4. Investor Matchmakers (HNW Layer)
- **Purpose**: Curate deal flow for Lumina Investors Guild (built on awesome-investor-agent-skills).
- **Process**:
  - Match talent projects to HNW preferences (sector, region, stage, values).
  - Generate personalized intros, syndication memos, co-build proposals.
  - Track outcomes (funding, mentorship, partnerships).
- **Integration**: Pull from investor-agent-skills patterns, push to private HNW channels.

### 5. Community Sentinels
- **Purpose**: Onboard, moderate, nurture the dual-sided community (talent + HNW).
- **Features**: Welcome sequences, event scheduling, guild health monitoring, conflict resolution, value-first content.
- **Channels**: Telegram (primary for global), Discord, custom portal.

### 6. Governance Overseers
- **Purpose**: Enforce 6-Pillar CoE, ethics, compliance, platform fairness.
- **Audits**: Bias in evaluations, data sovereignty, opportunity equity, financial transparency.
- **Outputs**: Reports, rule updates, escalation to Lumina Board (if applicable).

## Swarm Orchestration

- **Queen / Sentinel**: Starlight Queen patterns (from starlight-queen skills) for high-level coordination.
- **Handover & Memory**: agentic-ops ASPH protocol for session/state preservation across agents/models.
- **Evals**: starlight-evals harness for continuous improvement of agent performance on talent tasks.
- **Deployment**: Hermes profiles, cron for recurring discovery/competition cycles, multi-LLM routing.

## New Skills to Author (if needed)

- genius-discovery-skill
- competition-judge-skill
- hnw-matchmaker-skill

See workflows/ for executable prompt packs.

All agents prioritize **sovereignty, compounding intelligence, and 6-Pillar alignment**.
