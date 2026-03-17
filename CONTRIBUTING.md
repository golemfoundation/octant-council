# Contributing

This is a council builder, not a council. Contributions that make the builder better — sharper conversations, more robust generation, better templates — are what matter.

## What to work on

**High value:**
- Improve agent templates (`skills/generate-agent/templates/`) — better structure, stronger objectivity requirements, Goodhart-resistant scoring
- Improve design conversations (`skills/design-conversation/`, `skills/design-agent-conversation/`) — deeper probing, better domain extraction
- Add synthesis approaches beyond single-chair, debate, and ranked
- Fix bugs in the evaluate orchestrator's wave execution

**Welcome:**
- New default data sources for common domains
- Better score calibration guidance in eval templates
- Documentation improvements in `docs/`

**Also welcome:**
- Domain-specific agent definitions — if you've built a council for a domain and the agents are good, contribute them. Others can use them as starting points or cherry-pick individual agents into their own councils.
- New skills that agents can invoke — agents have access to the Skill tool, so you can give them specialized capabilities (e.g., a skill that queries a specific API, formats data a certain way, or runs a calculation). Build the skill, add it to the agent's tools, done.
- Agents that spawn their own sub-agents — council agents run as teammates, which means they can spawn parallel sub-agents themselves. A data agent could fan out 4 sub-agents to search different sources simultaneously, or an eval agent could spawn specialists to deep-dive each dimension. The wave pattern is recursive if you want it to be.

**Not needed:**
- Cosmetic refactors or comment additions to files you didn't change

## How the plugin works

```
skills/          Orchestration logic (SKILL.md files)
agents/          Agent definitions (auto-discovered by prefix: data-*, eval-*, synth-*)
docs/            Documentation
research/        Generated domain research (not checked in)
council-out/     Generated evaluation output (not checked in)
```

Skills invoke sub-skills via `<skill name="council:..." />`. The evaluate skill spawns agents as parallel tasks in three waves. Agents are markdown files — the orchestrator reads their frontmatter and injects runtime tokens (`$PROJECT`, `$DATA_DIR`, etc.).

## Making changes

1. **Skills** — edit the `SKILL.md` in the relevant `skills/` subdirectory. Skills use semantic tokens (`$TOKEN`) that expand from conversation context, not shell variables.

2. **Templates** — edit files in `skills/generate-agent/templates/`. These use `UPPER_CASE` placeholders that the generator fills in. Keep the placeholder convention consistent.

3. **Agent definitions** — the default agents in `agents/` are examples. If you improve the template structure, update the defaults to match.

4. **Testing** — run `/council:evaluate <project>` after changes to verify the full pipeline works. Check that all three waves complete and the report is coherent.

## Conventions

- Agent frontmatter fields: `name`, `description`, `tools`
- Eval agents score exactly 5 dimensions, 1-10 scale, with calibration table and Goodhart risk column
- Data agents include edge case handling for missing data
- All agent output is markdown
- Every agent process starts with `TaskUpdate` (claim) and ends with `TaskUpdate` (complete) + `SendMessage` (summary)
