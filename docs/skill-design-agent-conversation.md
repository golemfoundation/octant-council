# Skill: design-agent-conversation

**Invocable:** No (called by `council:add-agent`)
**Args:** `<wave-type> [name-hint]` (e.g. `"eval governance"`)
**Tools:** Read

## Purpose

Focused dialogue to design a single agent. Scoped to one agent within an already-decided council — never revisits council-level questions.

## Input

- **$ARGUMENTS** — Wave type and optional name/context parsed as: first word = wave type (`data`/`eval`/`synth`), second word (if present) = name hint (e.g. `governance`, `audits`).

| Arg | Required | Values |
|-----|----------|--------|
| `wave-type` | Yes | `data`, `eval`, `synth` |
| `name-hint` | No | Starting name context (e.g. `governance`, `audits`) |

## Constraints

- Stay scoped to this single agent — never revisit council-level design
- Challenge vague dimensions and generic data sources
- Demand **falsifiable evidence standards** — "what data proves a 3 vs a 7?"
- Probe **Goodhart vulnerabilities** for every metric — "how would a project game this score?"
- Push for depth — fewer rigorous dimensions beats many shallow ones
- Ensure evaluators can independently verify data, not just read data agent output
- Do not design the agent yourself — extract it from the user

## Wave-Specific Probes

| Wave | Probes for |
|------|-----------|
| `data` | Specific APIs/URLs, data format, key metrics, missing-data fallback |
| `eval` | 5 scoring dimensions, what distinguishes 6 vs 8, priority when dimensions conflict, supporting evidence in data files, Goodhart vulnerabilities, independent verification vs relying on data agent output |
| `synth` | Audience, output structure, handling evaluator disagreement |

**Objectivity traps to catch (eval agents):** self-reported metrics, vanity metrics, proxy collapse, missing base rates.

## Stop Conditions

| Field | Required |
|-------|----------|
| Agent name (`wave-name`) | Yes |
| One-line description | Yes |
| Detailed purpose (2-3 sentences) | Yes |
| Sources (data) / 5 dimensions with scoring criteria (eval) / output structure (synth) | Yes |
| Research brief (what domain knowledge to gather) | Yes |

## Exit Summary

```
**Name:** [wave]-[name]
**Description:** ...
**Purpose:** ...
**[Sources / Dimensions / Method]:** ...
**Research needed:** ...
```

## Difference from design-conversation

`design-conversation` = council-level (domain, purpose, scope, roster).
`design-agent-conversation` = single agent within an established council.
