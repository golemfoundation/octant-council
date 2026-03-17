# Skill: generate-agent

**Invocable:** No (called by `council:setup` and `council:add-agent`)
**Context:** Fork
**Model:** Sonnet
**Args:** `$ARGUMENTS` — agent name (e.g. `eval-governance`, `data-audits`, `synth-debate`)
**Tools:** Read, Write, Glob

## Purpose

Create an agent definition file from plan + research + structural template.

## Inputs

| File | Purpose |
|------|---------|
| the calling skill's prompt | Agent config: description, dimensions, sources |
| `research/$ARGUMENTS.md` | Domain expertise from research step |
| Template (see below) | Structural skeleton with UPPER_CASE placeholders |

## Steps

### Step 1: Read inputs

Read `research/$ARGUMENTS.md` for domain expertise. The calling skill passes agent config (purpose, dimensions, sources) via the prompt.

### Step 2: Read a template

Determine agent type from the `$ARGUMENTS` prefix and read the matching template:

| Prefix | Template |
|--------|----------|
| `data-*` | `skills/generate-agent/templates/data.md` |
| `eval-*` | `skills/generate-agent/templates/eval.md` |
| `synth-*` | `skills/generate-agent/templates/synth.md` |

Templates use UPPER_CASE placeholders (NAME, DESCRIPTION, DIMENSION_1, etc.) filled from plan and research. An existing agent of the same type may also be read as a fully realized example, but the template is always the structural skeleton.

Falls back to inline minimal template instructions if templates are somehow missing.

### Step 3: Generate the agent file

Write `agents/$ARGUMENTS.md` following the template's exact structure.

| Wave | Title | Input tokens | Process steps | Key sections |
|------|-------|-------------|--------------|-------------|
| `data-*` | `# Data Gatherer: [Name]` | `$PROJECT`, `$OUTPUT_DIR` | TaskUpdate → search/fetch → normalize → write → TaskUpdate → SendMessage | Sources, Output Format, Edge Cases |
| `eval-*` | `# Evaluator: [Name]` | `$PROJECT`, `$DATA_DIR`, `$OUTPUT_DIR` | TaskUpdate → read data → score 5 dimensions → composite → write → TaskUpdate → SendMessage | Scoring Table, Calibration (9-10/7-8/5-6/3-4/1-2) |
| `synth-*` | `# Synthesizer: [Name]` | `$PROJECT`, `$EVAL_DIR`, `$OUTPUT_PATH` | TaskUpdate → read evals → extract scores → agreement/disagreement → synthesize → write → TaskUpdate → SendMessage | Decision Criteria, Output Format |

### Step 4: Verify

Read back the written file and confirm:
1. Frontmatter has `name`, `description`, `tools`
2. All template sections present
3. Dimensions/sources are domain-specific (not placeholders)
4. Score calibration is domain-appropriate
5. Correct `$TOKEN` placeholders for wave type (`$OUTPUT_DIR`, `$DATA_DIR`, `$EVAL_DIR`, `$OUTPUT_PATH`)
