---
description: Install the council plugin — shell alias + teams feature + permissions
allowed-tools:
  - Bash
  - AskUserQuestion
model: inherit
context: inherit
user-invocable: true
---

# Council Setup

Sets up the council plugin for a user. Detects or clones the repo, explains everything that will happen, asks for confirmation, then configures the shell.

<progress>
- [ ] Step 1: Detect environment + check for repo
- [ ] Step 2: Explain everything, ask for confirmation
- [ ] Step 3: Clone repo (if needed)
- [ ] Step 4: Ask for alias name
- [ ] Step 5: Validate alias is available
- [ ] Step 6: Write alias + env var to shell config
- [ ] Step 7: Report success + dev tips
</progress>

## Step 1: Detect Environment + Check for Repo

Detect shell and config file:

```bash
echo "SHELL=$SHELL"
```

Map shell to config:
- `zsh` → `~/.zshrc`
- `bash` → `~/.bashrc` (or `~/.bash_profile` on macOS if `.bashrc` doesn't exist)
- `fish` → `~/.config/fish/config.fish`
- Other → `~/.${shell}rc`

Check if we're inside the council repo (or can find it nearby):

```bash
# Check current directory
if [ -f ".claude-plugin/plugin.json" ]; then
  PLUGIN_DIR="$(pwd)"
  echo "REPO_FOUND=true"
  echo "PLUGIN_DIR=$PLUGIN_DIR"
else
  # Check common locations
  for dir in \
    "$HOME/git/octant-council-builder" \
    "$HOME/octant-council-builder" \
    "$HOME/projects/octant-council-builder" \
    "$HOME/code/octant-council-builder" \
    "$HOME/src/octant-council-builder" \
    "$HOME/dev/octant-council-builder" \
    "../octant-council-builder"; do
    if [ -f "$dir/.claude-plugin/plugin.json" ]; then
      PLUGIN_DIR="$(cd "$dir" && pwd)"
      echo "REPO_FOUND=true"
      echo "PLUGIN_DIR=$PLUGIN_DIR"
      break
    fi
  done
  if [ -z "$PLUGIN_DIR" ]; then
    echo "REPO_FOUND=false"
  fi
fi
```

Store `$REPO_FOUND` and `$PLUGIN_DIR`.

## Step 2: Explain Everything, Ask for Confirmation

Before doing anything, tell the user exactly what will happen and why. The preview content depends on whether the repo was found.

```
AskUserQuestion:
  question: "Here's what setup will do. Ready to proceed?"
  header: "Council Setup"
  options:
    - label: "Let's go"
      description: "Proceed with setup"
      preview: |
        HOW PLUGINS WORK
        Claude Code can load plugins from any directory via --plugin-dir.
        It reads .claude-plugin/plugin.json from that directory and registers
        all skills/*/SKILL.md files as slash commands under the plugin's name.

        This repo is a plugin called "council" — loading it gives you
        /council:evaluate, /council:design, /council:add-agent, and more.

        [IF REPO NOT FOUND:]
        STEP 1: CLONE THE REPO
        The council repo wasn't found on your machine. We'll clone it from:
        https://github.com/golemfoundation/octant-council-builder.git
        You can pick where to put it (default: ~/git/octant-council-builder).

        STEP 2: CREATE A SHELL ALIAS
        Creates an alias so you can launch Claude Code with the council
        plugin loaded. Example: alias council='claude --plugin-dir /path/to/repo'

        The alias keeps things isolated — plain "claude" stays clean.
        The council only loads when you use the alias.

        STEP 3: ENABLE AGENT TEAMS
        The council's evaluate skill uses Claude Code's teams feature to run
        parallel agent waves. This requires an env var:
        export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

        Both shell config changes are tagged with "# public-goods-council"
        so they can be cleanly removed or updated by re-running setup.

        WHY THIS IS USEFUL FOR DEVELOPMENT
        The alias points at your local clone. Edit agent .md files or skill
        files and changes take effect immediately — no reinstall, no rebuild.
        Run /reload-plugins inside a session to pick up skill changes without
        restarting.
    - label: "Cancel"
      description: "Exit without changes"
```

If "Cancel" → report "Setup cancelled. No changes made." and stop.

## Step 3: Clone Repo (if needed)

Only runs if `$REPO_FOUND` is false.

```
AskUserQuestion:
  question: "Where should I clone the council repo?"
  header: "Clone Location"
  type: text
  placeholder: "~/git/octant-council-builder"
```

Use the user's answer, or the default if left blank. Then clone:

```bash
git clone https://github.com/golemfoundation/octant-council-builder.git "$CLONE_DIR"
```

Set `$PLUGIN_DIR` to the absolute path of the clone.

If clone fails, report the error and stop.

## Step 4: Ask for Alias Name

```
AskUserQuestion:
  question: "Pick a name for your council. You'll type this to launch Claude with the council loaded."
  header: "Alias Name"
  type: text
  placeholder: "e.g. betty, hal, sage, oracle, ada"
```

Store as `$ALIAS_NAME`.

### Validate

- Non-empty
- Alphanumeric + hyphens + underscores: `[a-zA-Z0-9_-]+`
- No spaces

If invalid, explain and re-ask.

## Step 5: Validate Alias is Available

```bash
command -v $ALIAS_NAME 2>/dev/null; alias $ALIAS_NAME 2>/dev/null; echo "exit:$?"
```

If collision found:

```
AskUserQuestion:
  question: "'$ALIAS_NAME' already exists as [command/alias]. Use it anyway?"
  header: "Name Conflict"
  options:
    - label: "Use it anyway"
      description: "Overwrite the existing alias"
    - label: "Pick a different name"
      description: "Go back and choose another name"
```

If "Pick a different name" → loop back to Step 4.

## Step 6: Write to Shell Config

Build the lines to add. Two lines, both tagged:

For zsh/bash:
```
alias $ALIAS_NAME='claude --plugin-dir $PLUGIN_DIR'  # public-goods-council
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1  # public-goods-council
```

For fish:
```
alias $ALIAS_NAME "claude --plugin-dir $PLUGIN_DIR"  # public-goods-council
set -gx CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1  # public-goods-council
```

Before writing, remove any existing tagged lines:

```bash
grep -v '# public-goods-council' "$SHELL_CONFIG" > "$SHELL_CONFIG.tmp" && mv "$SHELL_CONFIG.tmp" "$SHELL_CONFIG"
```

Then append:

```bash
echo "" >> "$SHELL_CONFIG"
echo "$ALIAS_LINE  # public-goods-council" >> "$SHELL_CONFIG"
echo "$TEAMS_LINE  # public-goods-council" >> "$SHELL_CONFIG"
```

## Step 7: Report Success + Dev Tips

```
Setup complete. Added to [config file]:

  [alias line]
  [teams env var line]

Copy-paste this to get started right now:

  source [config file] && cd $PLUGIN_DIR && $ALIAS_NAME

Or step by step:

  1. source [config file]        # load the alias + env var
  2. cd $PLUGIN_DIR              # enter the council repo
  3. $ALIAS_NAME                 # launch Claude with the council loaded

Inside a session, try:
  /council:evaluate Protocol Guild
  /council:design DeFi protocols
  /council:add-agent eval security


HOW THE ALIAS WORKS

The alias runs: claude --plugin-dir $PLUGIN_DIR

--plugin-dir tells Claude Code to load .claude-plugin/plugin.json from
that directory, registering all skills/*/SKILL.md as slash commands
under the "council" prefix. Plain "claude" stays clean.


DEVELOPING YOUR COUNCIL

The alias points at your local clone, so everything is live-editable:

  Agents (agents/*.md)
    Edit scoring dimensions, data sources, calibration tables.
    Changes are read fresh each /council:evaluate — no restart needed.

  Skills (skills/*/SKILL.md)
    Edit skill definitions to change orchestration behavior.
    Run /reload-plugins inside a session to pick up changes.

  No build step. No compilation. It's all markdown.

Once you've designed your own council, anyone else can install it too —
just push your fork and share the repo URL. They clone it, run
/council:setup, and they have your council as a plugin.
```
