---
system: knowledge-base
status: verified
checked: 2026-11-18
tags: [setup, agents, sync]
---
# Set up the knowledge base on another PC

## Summary

Restore the private repository at `~/ai` on a Linux workstation with Bash, Git,
OpenSSH, Python 3.11+ and GNU coreutils. Keep `current` pointing to the intended
company layer. Agent instruction and custom skill directories are links into the
repository; client authentication, secrets, generated data and external tools need
separate setup. Use the updater to install the current stable agnix before instruction
lint. Inspect the read-only preview before the first real sync, which commits pending
KB changes and pushes to every configured origin push URL.

## Symptom

A fresh PC has no knowledge repository, agent links, local secrets or helper tools.
Cloning alone does not reproduce the working environment.

## Cause

Git carries the durable notes, scripts, instructions, skills and `current` symlink.
It excludes `.env`, generated data, client sessions, sync state and external binaries.
See [canonical rules](../README.md), especially Layers, Daily sync, Agent instruction
lint and Connecting an agent. Those rules take precedence if this procedure ages.

## Fix

### 1. Prepare the workstation and access

Use Linux with a POSIX filesystem supporting symbolic links, Bash, Git, OpenSSH,
GNU coreutils, `rg`, and Python 3.11+. The core KB scripts and agnix updater use the
Python standard library. Check the `python3` on `PATH` in the shell and agent
environment that will run the scripts.

```bash
command -v python3
python3 --version
python3 -c 'import tomllib'
```

If an older interpreter comes first, make a supported version available as `python3`
on `PATH` before continuing. A shell alias or a separate `python3.12` executable
does not change what `ai-sync.sh` invokes. Configure Git author name and email and
set up local credentials for the private KB repository and both push destinations.

Agent applications must already be installed and authenticated separately. Their
runtime folders may contain machine paths, account state and plugin caches; restore
only reviewed configuration, not entire client directories. Company operational
tools, VPN, cloud CLIs and access are separate from installing the KB.

### 2. Clone and inspect the layout

Obtain the credential-free private clone URL from the existing machine's approved
Git configuration or repository hosting UI. Replace the placeholder before running:

```bash
git clone '<PRIVATE_KB_CLONE_URL>' "$HOME/ai"
git -C "$HOME/ai" status --short --branch
git -C "$HOME/ai" branch --show-current
git -C "$HOME/ai" config user.name
git -C "$HOME/ai" config user.email
readlink "$HOME/ai/current"
test -r "$HOME/ai/current/CONTEXT.md"
```

Stop if `~/ai` already exists; inspect it instead of overwriting it. Preserve local
changes. The sync script expects local `main` and remote `origin/main`; resolve any
branch/layout mismatch deliberately before running it. Inspect origin fetch and push
URLs locally without pasting embedded credentials into logs.

To reproduce the two-destination setup, obtain both approved, credential-free push
URLs from the existing machine. On a fresh clone, set the primary push URL explicitly
before adding the secondary so both are retained. Fill in both placeholders before running these commands.

```bash
git -C "$HOME/ai" remote set-url --push origin '<PRIMARY_PUSH_URL>'
git -C "$HOME/ai" remote set-url --add --push origin '<SECONDARY_PUSH_URL>'
git -C "$HOME/ai" remote get-url origin
git -C "$HOME/ai" remote get-url --push --all origin
```

Expect one fetch URL and two push URLs. For an existing clone, inspect its full
push URL list before editing it. A separate named remote does not add an `origin`
push destination. Use the following command to check read access to `main` on the fetch URL and both push URLs.

```bash
GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=8' \
  git ls-remote --exit-code '<URL_TO_CHECK>' refs/heads/main
```

Repeat for each distinct URL. For SSH, this uses the same noninteractive mode as
normal sync. Configure trusted host keys and make the correct identity available
to the agent environment. Check the account's write permissions at both Git hosts.
`ls-remote` tests read access, and the sync preview runs entirely locally.

Expected layout: `general/`, `personal/`, `companies/<company>/`, `current`, `AGENTS.md`
and `TODO.md`. `current` must resolve to the intended `companies/<company>` directory.
Prefer a relative symlink target such as `companies/<company>` for portability. If the
tracked link is broken or selects another employer, review and change it explicitly;
do not silently switch company context. Operational notes may contain old absolute
checkout paths: consult the layer's `knowledge/repos.md` before using them.

### 3. Connect instruction and skill entry points

Read `~/ai/AGENTS.md` and its triggered README sections first. For each installed
client, inspect any existing destination before creating links. These examples are
for absent destinations; do not use `ln -f` to replace existing files:

```bash
mkdir -p "$HOME/.codex/skills" "$HOME/.claude/skills" "$HOME/.gemini"
ln -s "$HOME/ai/AGENTS.md" "$HOME/.codex/AGENTS.md"
ln -s "$HOME/ai/AGENTS.md" "$HOME/.claude/CLAUDE.md"
ln -s "$HOME/ai/AGENTS.md" "$HOME/.gemini/GEMINI.md"
```

Link each applicable directory in `~/ai/general/skills/` and `~/ai/current/skills/`
individually into the installed client's skill directory. Example for the shared
learning skill:

```bash
ln -s "$HOME/ai/general/skills/agent-learning" "$HOME/.codex/skills/agent-learning"
ln -s "$HOME/ai/general/skills/agent-learning" "$HOME/.claude/skills/agent-learning"
```

Repeat for the other applicable custom skills after checking names for collisions.
Do not link an entire skills root over the client's directory. Plugin/system skills
are installed through their own distribution and are not copied from runtime caches.
After changing `current`, review company skill links and remove stale employer links
only after inspecting them. Gemini reads the explicitly referenced shared skill files;
do not assume that Codex/Claude discovery behavior applies to it.

For jcode, use its global prompt overlay and link the same custom skills individually
into `~/.jcode/skills/`. Jcode can import copies on first run. Compare each existing
copy with its canonical source and preserve it before replacing it with a link.

```bash
mkdir -p "$HOME/.jcode/skills"
ln -s "$HOME/ai/AGENTS.md" "$HOME/.jcode/prompt-overlay.md"
ln -s "$HOME/ai/general/skills/agent-learning" "$HOME/.jcode/skills/agent-learning"
```

For the optional [tracked jcode configuration](../../../personal/jcode/config.toml),
review the provider settings and link it to `~/.jcode/config.toml` if the destination
is absent. Keep provider credentials in jcode's local authentication store.
Start a new session after changing the overlay or skill links.
[Jcode prompt layers](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/SYSTEM_PROMPT_CONFIG.md)

After wiring a full Codex or jcode setup, check its global instructions and shared
skills before opening a session. The check expects each skill in `general/skills`
and the active `current/skills` to point at its source. It reports copies, broken
links and wrong targets, including links to a previous company layer.

```bash
python3 ~/ai/general/scripts/agent_lint.py --check-links codex
python3 ~/ai/general/scripts/agent_lint.py --check-links jcode
```

For optional code navigation, install agentgrep v0.2.0 from its pinned upstream
revision with a Rust toolchain that supports edition 2024. Ensure the install
directory is on PATH and run `agentgrep --version`.

```bash
cargo install --git https://github.com/1jehuang/agentgrep \
  --rev a2c52bbfea9fbcf1d7e89d74ef607c6d1fb4ba14
agentgrep outline --max-items 5 "$HOME/ai/general/scripts/kb_lint.py"
```

#### On-demand Graphify

Install the Graphify CLI in a Python 3.12 virtual environment. Install the
symlink when the destination is absent. Agents can invoke the CLI through their
existing shell access.

```bash
graphify_venv="$HOME/.local/share/graphify/0.9.119"
python3.12 -m venv "$graphify_venv"
"$graphify_venv/bin/python" -m pip install 'graphifyy==0.9.119'
ln -s "$graphify_venv/bin/graphify" "$HOME/.local/bin/graphify"
"$HOME/.local/bin/graphify" --version
```

Use one private output directory per checkout, mirroring its path relative to
`~/git`. From the checkout root, substitute its relative path for `repo-name`.
Run `update` on the first use or after relevant source changes. Reuse the graph
for additional queries against the same source. Confirm the returned edges in
the source before relying on them.

```bash
install -d -m 700 "$HOME/ai-data/graphify"
install -d -m 700 "$HOME/ai-data/graphify/repo-name"
(
  export GRAPHIFY_OUT="$HOME/ai-data/graphify/repo-name"
  export GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_VIZ_NODE_LIMIT=0
  "$HOME/.local/bin/graphify" update . &&
    "$HOME/.local/bin/graphify" path 'Start.Method()' 'End.Method()' \
      --graph "$GRAPHIFY_OUT/graph.json"
)
```

Keep the graph and extraction cache locally while they serve follow-up
traces. Remove a checkout's output directory when its graph is no longer
used. The [Graphify CLI reference](https://github.com/Graphify-Labs/graphify#full-command-reference)
describes available commands.

#### Codex configuration

If using the tracked [global Codex configuration](../../../personal/codex/config.toml),
review the absolute paths in `[projects]` and the MCP helper paths for this
workstation. After inspecting any existing `~/.codex/config.toml`, create the link
if the destination is absent and the paths match the machine.

```bash
ln -s "$HOME/ai/personal/codex/config.toml" "$HOME/.codex/config.toml"
readlink -f "$HOME/.codex/config.toml"
```

If machine-specific paths need to differ, use a reviewed local copy of the config.
Changes to a linked config also change the tracked file that sync can publish.

The tracked Codex and jcode configurations call `general/scripts/kb_post_edit.py`
after supported Markdown edits. Codex registers it as `PostToolUse` for
`apply_patch`. Review and trust that exact hook through `/hooks` in a new Codex
CLI session. Jcode uses `post_tool_feedback` with its named edit tools after a
fresh launch. Clean edits are silent. Findings contain lint codes and file
paths. The hook checks explicit edit paths, while the end-of-task KB lint covers
shell writes and all other notes.
[Codex hook review](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks) ·
[Jcode feedback hook](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/HOOKS.md#feedback-hook-post_tool_feedback)

### 4. Restore secrets and local generated data

Check ignore coverage before restoring secrets. Resolve the tracked `current` link
first because Git rejects paths that pass through a symlink. Each check should print
its path and exit with code 0.

```bash
kb_company_layer=$(readlink -f "$HOME/ai/current") &&
  git -C "$HOME/ai" check-ignore -- "$kb_company_layer/.env" &&
  git -C "$HOME/ai" check-ignore -- personal/.env
```

Transfer required secrets through an approved private route into the intended
`~/ai/current/.env` or `~/ai/personal/.env`, using `KEY=value`. Restrict these files to
the account, for example with `chmod 600`. Restore only the variables needed by the
selected workflows. Never put values in Markdown, Git URLs, commands or sync summaries.

The tracked runner job collector and issue comment inspector use the company layer `.env`
and the existing Python installation.
The tracked home-router domain helper validates local files with Python 3.11+.
Its separately approved apply mode uses the existing SSH access and a trusted
host key. Generate new reports and keep input lists and receipts in `~/ai-data/`.

```bash
mkdir -p "$HOME/ai-data/todo"
```

`~/ai-data/` is outside Git. Let this machine regenerate lint and metrics state,
locks and sync markers, including `.last-sync`. Before the final checklist, restore
`~/ai-data/todo/display-ru.json` from the old machine if available. Check for missing
or stale entries with the command below.

```bash
python3 "$HOME/ai/general/scripts/todo.py" --missing
```

If the script lists entries or headings, translate only those and merge them into
the cache as described in [TODO output](../README.md#todo-output). With a complete
cache `todo.py` renders the backlog and exits 0. An absent or stale cache yields exit
2 on a normal run. `~/ai/TODO.md` is the source backlog.

### 5. Restore MCP integrations

The [global Codex config](../../../personal/codex/config.toml) supplies two HTTP
servers. Restore the servers you use by keeping their existing entries under
`[mcp_servers]`.

| Server | Setup on the new PC | Read-only check in a fresh Codex session |
| --- | --- | --- |
| `openaiDeveloperDocs` | Keep the URL `https://developers.openai.com/mcp`. The tracked entry uses HTTPS without a local helper or token setting. | Use the server to fetch a Codex documentation page and check that it returns the page content. |
| `hetrixtools` | Keep the URL `https://mcp.hetrixtools.net` and the configured `User-Agent`. Point `http_headers_helper` to `python3` and the absolute path of [`hetrixtools_mcp_headers.py`](../../../personal/scripts/hetrixtools_mcp_headers.py) on this PC. Restore `HETRIXTOOLS_API_KEY` to `~/ai/personal/.env`. Keep the existing approval mode. | Call `get_api_scope` to verify authentication. Keep the helper's stdout out of terminals, chat and logs because it contains the credential. |

The [Ansible MCP config](../../../personal/codex/ansible/config.toml) applies only
to the trusted Ansible checkout. Use its `AGENTS.md` to recreate the Python 3.12
`.ansible-venv`, install `ansible-core` and restore the project's collections.
Install the pinned npm dependencies outside Git under `~/ai-data/ansible-mcp`.
The [Ansible MCP setup](../../../personal/codex/ansible/README.md) gives the install
command and explains the launcher and four-tool allowlist. Review the absolute
launcher and checkout paths, then connect the project config as
`<checkout>/.codex/config.toml` according to that repository's workflow.
From a fresh session opened in the checkout, call `ade_environment_info` to check
the workspace and venv or `ansible_content_best_practices` to fetch reference guidance.

Use `codex mcp list` outside the checkout to inspect global entries and run it again
inside the trusted checkout to check that `ansible` is present there.
After the sync preview and first-run checks below, use `/mcp` in a fresh Codex
session and run the corresponding read-only calls to test each connection.
For MCP servers supplied by client plugins, restore the plugin and its account
connection in that client, then verify the tools in a fresh session.
See [Codex MCP configuration and inspection](https://developers.openai.com/codex/mcp).

### 6. Install the current stable instruction linter

Run the daily updater to download the latest official stable agnix release, verify
its API SHA-256 and binary version, and activate the local installation:

```bash
python3 "$HOME/ai/general/scripts/agnix_update.py"
"$HOME/.local/share/agnix/current/agnix" --version
python3 "$HOME/ai/general/scripts/agent_lint.py" --force
```

Normal `ai-sync.sh` also runs this updater before lint, once per local calendar day.
Network access to the GitHub API and release downloads is required. A failed attempt
keeps the previous selection and remains pending for retry. The helper prefers
`~/.local/share/agnix/current/agnix`, then the legacy 0.59.0 installation, then `PATH`.
Per-version binaries stay in `~/.local/share/agnix/`; machine-local update state stays
in `~/ai-data/agnix/`. Do not copy successful daily state from another PC.
Use `agnix_update.py --force` to explicitly recheck the release on the same day.
Supported targets and failure behavior are documented in README "Agent instruction lint".
Keep lint report-only and review findings before changing instructions.

### 7. Verify locally, then enable normal synchronization

```bash
python3 "$HOME/ai/general/scripts/kb_find.py" knowledge-base
python3 "$HOME/ai/general/scripts/todo.py"
python3 "$HOME/ai/general/scripts/kb_lint.py"
python3 "$HOME/ai/general/scripts/build_index.py"
"$HOME/ai/general/scripts/ai-sync.sh" --dry-run
git -C "$HOME/ai" status --short
```

Review errors, warnings, generated index changes and the complete sync preview.
The preview leaves the working files, staging, Git objects and sync state intact.
It skips the agnix update, instruction lint, metrics preparation, weekly usage report
and monthly staleness update.

Weekly token accounting uses local client history and therefore differs across PCs.
For KB access extraction, additionally provide Node.js and the `acorn` module in its
module search path; verify `node -e "require('acorn')"`. Install these optional
dependencies outside the synchronized repository. A missing parser reduces Codex
KB extraction coverage.

Once the preview and destinations are satisfactory, use normal sync with the
applicable publication permissions. Do this before prompting agents whose task-start
instructions run normal sync automatically.

```bash
"$HOME/ai/general/scripts/ai-sync.sh"
"$HOME/ai/general/scripts/ai-sync.sh" --status
```

Normal sync checks agnix and prepares daily metrics before the same-day Git skip.
If it reports `daily analysis pending`, follow the [daily metrics workflow](../../skills/agent-learning/SKILL.md#daily-metrics).
When Git sync runs, it stages all KB changes, commits, rebases against `origin/main`
and pushes to both configured destinations. A failed push leaves the sync pending
for retry. Agents call this script at task start.

Open a fresh session in each installed client. Ask it to identify the canonical
instruction file, resolve `current/CONTEXT.md`, find a harmless note via `kb_find.py`
and report available custom skills without exposing secrets. Repeat inside and
outside `~/ai` to check runtime instruction loading. For Codex, run the selected
integration checks in [Restore MCP integrations](#5-restore-mcp-integrations).
Retain the checked-in
`AGENTS.override.md` duplicate-loading exception and inspect existing client
overrides before modifying them.

## Limits

The local checks were exercised in an isolated copy. A full installation on a fresh
PC, remote access and client authentication still require verification. Linux is
the documented baseline. Windows and macOS need separate validation for GNU date,
symlinks, Python `fcntl`, client paths and binary architecture.
Do not copy `.git/config`, SSH keys, machine caches or client auth state blindly.
