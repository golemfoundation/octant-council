# Skill: evaluate

**Invocable:** Yes
**Args:** `<project-name-or-url>` (prompts if omitted)
**Tools:** Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent, Task, SendMessage, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, WebFetch, WebSearch

## Purpose

Orchestrates the full council evaluation: discovers agents, creates a team, spawns three waves sequentially, gates between waves, and presents the final report.

## Semantic Tokens

| Token | Source | Value |
|-------|--------|-------|
| `$PROJECT` | User input | Project name or URL |
| `$SLUG` | Derived | URL-safe slug (lowercase, hyphens, max 40 chars) |
| `$DATA_AGENTS` | Glob | List of `agents/data-*.md` files discovered |
| `$EVAL_AGENTS` | Glob | List of `agents/eval-*.md` files discovered |
| `$SYNTH_AGENTS` | Glob | List of `agents/synth-*.md` files discovered |
| `$DATA_DIR` | Constructed | `council-out/$SLUG/data` |
| `$EVAL_DIR` | Constructed | `council-out/$SLUG/eval` |
| `$OUTPUT_DIR` | Per-agent | Agent's wave output directory |
| `$OUTPUT_PATH` | Constructed | `council-out/$SLUG/REPORT.md` |

## Process

| Step | Action | Tools |
|------|--------|-------|
| 1 | Parse input → `$PROJECT` + `$SLUG`. Glob `agents/{data,eval,synth}-*.md`. Read frontmatter. Create `council-out/$SLUG/{data,eval}`. Show roster, confirm. If "Modify roster" → invoke `add-agent` skill, then re-discover. | Glob, Read, Bash, AskUserQuestion |
| 2 | Create team `council-$SLUG`. Pre-create tasks for all agents across all waves. | TeamCreate, TaskCreate |
| 3 | **Wave 1** — Spawn ALL `data-*` agents in single message (`run_in_background=true`). Poll `TaskList` until all Wave 1 tasks complete. Send `shutdown_request` to each `w1-*` agent. | Agent, Task, TaskList, SendMessage |
| 4 | **Wave 2** — Spawn ALL `eval-*` agents in single message. Poll until complete. Do NOT shut down — evaluators stay alive for Wave 3 synthesizer follow-up questions. | Agent, Task, TaskList |
| 5 | **Wave 3** — Spawn ALL `synth-*` agents with list of live Wave 2 evaluator names. Synthesizer may message evaluators via `SendMessage`. Poll until complete. Then send `shutdown_request` to all `w2-*` and `w3-*` agents. | Agent, Task, TaskList, SendMessage |
| 6 | Read and present `REPORT.md` to user. Offer: done / evaluate another / dig deeper. | Read, AskUserQuestion |
| 7 | Delete team. | TeamDelete |

## Wave Gates

Each wave spawns all agents in a **single message** for parallelism. Orchestrator polls `TaskList` until every task in that wave shows `status="completed"`. Only then proceeds to next wave.

## Agent Discovery

```
Glob agents/data-*.md  →  Wave 1 agents
Glob agents/eval-*.md  →  Wave 2 agents
Glob agents/synth-*.md →  Wave 3 agents
```

No hardcoded roster. Add/remove files to change the council.

## Synthesizer ↔ Evaluator Messaging

Wave 2 evaluators remain alive through Wave 3. The synth agent receives the list of live `w2-*` agent names and can send them `SendMessage` follow-ups to request clarification, challenge scores, or resolve disagreements. Evaluators reply and wait for a `shutdown_request`. The orchestrator shuts down all Wave 2 and Wave 3 agents after the Wave 3 gate clears.

## Shutdown Sequence

| After | Who gets shutdown_request |
|-------|--------------------------|
| Wave 1 gate clears | All `w1-*` agents |
| Wave 3 gate clears | All `w2-*` and `w3-*` agents |
| Step 7 | `TeamDelete` only — agents already shut down |

## Output

```
council-out/$SLUG/
├── data/        ← one .md per data agent
├── eval/        ← one .md per eval agent
└── REPORT.md    ← synth output
```

## Constraints

1. Never skip wave gate — all agents in wave must complete before next wave starts
2. Evaluators read `data/` only, never `eval/` — independence is enforced
3. Never fabricate data — agents report absence, not invention
4. Never spawn agents one at a time — all in single message per wave
5. Never synthesize in orchestrator — that's the synth agent's job
6. Never shut down Wave 2 agents before Wave 3 completes — synthesizer needs them for follow-up questions
