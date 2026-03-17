# Skill: design-conversation

**Invocable:** No (called by `council:setup`)
**Args:** `[domain]` (e.g. `"DeFi protocols"`)
**Tools:** Read

## Purpose

Pure conversational dialogue to extract the user's vision for an evaluation council. Thinking partner, not interviewer. Returns a structured summary consumed by the parent skill's roster design phase.

## Stop Conditions

Conversation ends when all 9 can be answered:

| # | Question |
|---|----------|
| 1 | What domain are we evaluating? |
| 2 | What decision does this council inform? |
| 3 | What data sources can be fetched and measured? |
| 4 | What evaluation lenses define "good" in this domain? |
| 5 | Are dimensions falsifiable? (could two independent evaluators agree on each score?) |
| 6 | What are the Goodhart risks? (which metrics can be gamed, and how to counter that?) |
| 7 | What are the domain-specific red flags? |
| 8 | What is out of scope? |
| 9 | What is the ONE non-negotiable criterion? |

## Exit Summary

```
**Domain:** ...
**Purpose:** ...
**Data priorities:** ...
**Evaluation priorities:** ...
**Evidence standards:** ...
**Goodhart risks:** ...
**Skeptic focus:** ...
**Out of scope:** ...
**Core essence:** ...
```

## Approach

- Follow user's energy, not a checklist
- Challenge vagueness: "impact" → impact on whom, measured how, over what timeframe?
- Single-word answers get pushed back
- No premature agent design
- No structured questions — pure conversation
- Push relentlessly for objectivity — every dimension must be falsifiable and evidence-based, not vibes
- Probe for Goodhart's Law vulnerabilities: for every proposed metric, ask "How would a project game this?"
- Push for depth over breadth — fewer dimensions scored rigorously beats many scored superficially
