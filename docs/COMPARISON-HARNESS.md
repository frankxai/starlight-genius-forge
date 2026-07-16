# Multi-CLI Comparison Harness — Idea Forge (product pointer)

Compete Grok CLI · Claude Code · Codex · AGY · OpenCode on idea evolution tasks.  
Text-first. Disk TIGHT: no new worktrees. Native image = Grok/xAI only.

> **Canonical full harness (646 lines, Windows git-bash recipes, best-of-N, JSON scorecards):**  
> `C:\Users\frank\starlight\ops\model-arena\COMPARISON-HARNESS.md`  
> Written by multi-CLI leaf 2026-07-16 (deleg_40648ba1 task 2). This file is the **product-facing summary**; run live competitions from the ops SSOT.

---

## Routing table

| Work | CLI | Flags (git-bash) |
|------|-----|------------------|
| Creative / cinematic / image prompts | Grok | `grok --single "..." --always-approve --model grok-4.5` |
| Architecture / judgment / PR | Claude Code | `claude -p "..." --max-turns 12 --allowedTools "Read,Write,Bash"` |
| Implement loops | Codex | `codex exec --sandbox workspace-write - < prompt.txt` |
| Bulk grunt / Gemini | AGY | `agy -p "..."` |
| Free flexible | OpenCode | `opencode run "..."` |
| Queen / CoE / receipts | Hermes | this session |

## Scoring rubric (0–10 each)

1. Correctness  
2. Reasoning depth  
3. Taste / brand fit  
4. Actionability (ship-ready artifacts)  
5. Cost / latency awareness  

**Winner** = highest average; ties → prefer more executable artifacts.

## First experiment brief

**Title:** Improve football anime content engine + Idea Forge football module  

**Inputs:** `docs/CONTENT-ENGINE.md`, `docs/FOOTBALL-DOMAIN.md`, `docs/IDEA-FORGE.md`  

**Deliverables per CLI:**
- Diff-ready markdown improvements (no media files)
- 3 improved prompts or posting tactics  
- 1 quantified business micro-plan  

**Commands (from repo root):**

```bash
cd /c/Users/frank/starlight/repos/starlight-genius-forge

# Grok
grok --single "Improve docs/CONTENT-ENGINE.md: stronger virality + ethics + metrics. Output full revised markdown." --always-approve --model grok-4.5

# Claude
claude -p "Read docs/IDEA-FORGE.md and docs/FOOTBALL-DOMAIN.md. Propose architecture improvements as a patch-ready markdown section." --max-turns 10 --allowedTools "Read,Write,Bash"

# Codex
codex exec --sandbox workspace-write "Read docs/*.md. Add docs/COMPARISON-RESULTS.md with a sample scorecard for Grok vs Claude on football content engine."
```

## Judge template

```
Experiment: [name]
Date:
Artifacts:
| CLI | Correctness | Depth | Taste | Actionability | Cost | Avg | Notes |
|-----|-------------|-------|-------|---------------|------|-----|-------|
| Grok | | | | | | | |
| Claude | | | | | | | |
| Codex | | | | | | | |
Winner:
Merged into:
```

## Policy

- Draft PRs only until green  
- No FAL image gen  
- No home recursive search  
- Queen receipt after each multi-hour wave  

---

*Starlight Idea Forge · coding-agents MCR*
