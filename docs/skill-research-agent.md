# Skill: research-agent

**Invocable:** No (called by `council:design` and `council:add-agent`)
**Context:** Fork
**Args:** `<agent-name>` (e.g. `data-audits`, `eval-governance`)
**Tools:** Read, Write, Glob, WebSearch, WebFetch

## Purpose

Gather domain expertise for a single agent before its definition is generated. The calling skill passes agent config via prompt; this skill researches it and writes structured findings for `generate-agent` to consume.

## Input

`$ARGUMENTS` is the agent name (e.g., `data-audits`, `eval-governance`, `synth-debate`).

## Process

### Step 1: Read the plan

The calling skill passes the agent's config (purpose, sources/dimensions, research needed) via the prompt. No plan file to read.

Find the section for `$ARGUMENTS`. Extract:
- **Purpose** — what this agent does
- **Sources** — specific data sources or APIs (for data agents)
- **Dimensions** — scoring dimensions (for eval agents)
- **Research needed** — what domain knowledge to gather

### Step 2: Research

Based on the agent type (determined by prefix):

| Prefix | Searches for |
|--------|-------------|
| `data-*` | API docs, data schemas, access methods, rate limits, alternatives |
| `eval-*` | Evaluation methodologies, scoring rubrics, benchmarks, what distinguishes excellent from adequate |
| `synth-*` | Synthesis frameworks, panel aggregation, handling disagreement, report formats |

### Step 3: Write research file

Write findings to `research/$ARGUMENTS.md`:

```markdown
# Research: $ARGUMENTS

**Researched:** YYYY-MM-DD
**Purpose:** [from plan]

## Domain Context

[2-3 paragraphs of domain background relevant to this agent's role]

## Data Sources Found

[For data agents: specific URLs, APIs, access methods]
[For eval agents: frameworks, rubrics, benchmarks discovered]
[For synth agents: synthesis methodologies, report formats]

### Source 1: [name]
- **URL:** [url]
- **What it provides:** [description]
- **Access method:** [API/scrape/manual]
- **Reliability:** [high/medium/low]

### Source 2: [name]
...

## Methodology Notes

[For eval agents: how to score each dimension based on research]
[For data agents: how to normalize data across sources]
[For synth agents: how to handle disagreement, weighting]

## Key Findings

- [Finding 1 — something that should influence the agent definition]
- [Finding 2]
- [Finding 3]

## Gaps

[What couldn't be found — this is valuable for setting agent expectations]
```

## Output

The research file at `research/$ARGUMENTS.md`, ready for consumption by `generate-agent`.
