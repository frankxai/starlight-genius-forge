# Idea Swarm Debate Loop

Inspired by Kura AI's planner / executor / critic architecture (debate per action, self-heal/backtrack). Adapted for **ideas**, not browser CUA as the default product.

Version: 1.0.0 · 2026-08-10

## Roles

| Role | Job | Preferred routing |
|------|-----|-------------------|
| **Planner** | Goal decomposition, risks, done-when, stage choice | Claude / Hermes Queen |
| **Executor** | Produce the artifact | Codex (impl), Grok (creative), AGY (bulk) |
| **Critic** | Adversarial verification; may force backtrack | Independent CLI or model |

## Protocol

```text
1. Planner emits PlanCard:
   - stage, objective, constraints, budget, done-when, success metrics
2. Executor produces Artifact + Evidence paths
3. Critic scores:
   - truth / grounding
   - ethics (6-Pillar)
   - roadmap fit
   - feasibility / cost
   - anti-slop / brand
   - security / privacy
4. If any hard fail → BACKTRACK with blockers; Planner revises
5. If pass → ADVANCE; write receipt; optional GitHub/issue/PR action
```

## Hard fails (always backtrack)

- Invented metrics, clients, or live sports facts without re-check  
- Private vault content proposed for public issue  
- Money/spend/DNS/credential mutations without human gate  
- Roadmap edit without Critic PASS  
- Disk CRITICAL worktree/media fanout  

## Receipt schema (minimum)

```json
{
  "ideaId": "isw-YYYYMMDD-slug",
  "stage": "refine|quantify|align|execute",
  "plan": "...",
  "artifactPaths": ["docs/...", "issues/..."],
  "critic": {"verdict": "PASS|FAIL", "blockers": [], "score": 0},
  "models": {"planner": "", "executor": "", "critic": ""},
  "next": "..."
}
```

## Multi-CLI default

Use `coding-agents` MCR. High-value stages require ≥2 Executor variants before Critic when capacity admits.

## Browser lane (optional)

Only when validation needs live web interaction:
- Prefer Hermes `computer_use` / documented CUA with admission  
- Do not default product identity to trykura.com SaaS  
- Critic still gates any external side effect  
