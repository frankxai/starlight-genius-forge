# Comparison Results — Grok vs Claude on Football Anime Content Engine

Experiment: Improve `docs/CONTENT-ENGINE.md` (football anime image + posting engine)
Date: 2026-07-16
Basis: conceptual pass, not a live dual-CLI run (see Notes)

## Scorecard

| CLI | Correctness | Depth | Taste | Actionability | Cost | Avg | Notes |
|-----|-------------|-------|-------|----------------|------|-----|-------|
| Grok | 7 | 6 | 8 | 8 | 9 | 7.6 | Fast, on-brand prompt variety (hair/flag/action deltas per country); weak on structure — tends to hand back prose, not diff-ready markdown; no native cost/ethics framing unless asked. |
| Claude | 9 | 8 | 7 | 8 | 6 | 7.6 | Strong at turning the doc into patch-ready structure (tables, rubric, metrics), catches gaps (no 9:16 spec, no A/B hook variants, ethics line underspecified); slower and pricier per turn; anime "taste" calls are more generic than Grok's native visual instinct. |

**Winner:** Tie on average — route by task. Grok for prompt/variant generation (its native strength), Claude for architecture, doc structure, and the ethics/metrics scaffolding. Matches the harness's own routing table.

## What each would likely add

**Grok pass** (creative headwind):
1. 9:16 vertical variant of all 10 prompts (currently 16:9 only) — TikTok/Reels native.
2. A hook-line variant field per country ("GOAL!!" vs quiet-tears-of-joy vs pre-match hype) to A/B caption tone.
3. Faster iteration loop: batch-generate 3 stills per team before committing to final prompt text.

**Claude pass** (structural headwind):
1. Add a `## 0. Metrics baseline` section before content — no engine should ship without a measurement plan, and §4 currently reads as an afterthought.
2. Tighten the ethics line: "AI-label if required by platform" should be a hard default, not conditional — flag as a real-athlete-likeness risk (young women as fan avatars is fine; drifting toward real player likeness is not).
3. Split §3 (business models) out of the content engine doc entirely — it's a different altitude (biz plan vs prompt library) and dilutes a doc that should be copy-paste-ready for Grok.

## Business micro-plan (quantified, Claude-style)

- Cost basis: 10 stills/day × $0/still (native Grok, no FAL) + ~15 min human curation = near-zero marginal cost.
- Target: 3% follower growth/week during World Cup window if posted within the 15–30 min match-moment rule.
- Break-even signal: 50k cumulative views → justifies one paid boost test ($20) on best-performing team asset.

## Notes

- No live Grok/Codex CLI invocation was run for this pass — Grok CLI is not available in this session's toolset. This scorecard reasons about known Grok vs Claude strengths (visual/creative generation vs structural/architectural judgment) applied to the actual doc content, per the harness's judge template.
- To make this a real (non-conceptual) comparison, run the two commands in `docs/COMPARISON-HARNESS.md` directly in a git-bash terminal and re-score against actual outputs.

---

*Starlight Idea Forge · coding-agents MCR*
