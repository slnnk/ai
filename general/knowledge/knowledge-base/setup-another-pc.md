---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [setup, agents, sync]
---
# Set up the knowledge base on another PC

## Summary

Restore the private repository at `~/ai` on a Linux workstation with Bash, Git,
OpenSSH, Python 3.11+ and GNU coreutils. Keep `current` pointing to the intended
company layer. Agent instruction and custom skill directories are links into the
repository; client authentication, secrets, generated data and external tools need
separate setup. Install the pinned agnix binary before instruction lint. Inspect the
read-only sync preview before the first real sync, which commits all KB changes and
pushes to every configured origin push URL. This guide was checked against local
scripts on 2026-11-04; a clean-machine installation was not executed.

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
GNU coreutils, `rg`, and Python 3.11+ (includes `tomllib`). The core KB scripts use
the Python standard library. Download/extraction examples also require `curl`,
`tar` and `sha256sum`. Use an account authorized to read the private KB repository
and write to its configured Git remotes. Configure Git author name/email explicitly;
do not copy another machine's private SSH key or global Git configuration wholesale.

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
URLs locally without pasting embedded credentials into logs. Recreate the approved
secondary push destination explicitly: additional origin push URLs and Git remotes
live in `.git/config` and are not restored by cloning.

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

### 4. Restore secrets and local generated data

Transfer required secrets through an approved private route into the intended
`~/ai/current/.env` or `~/ai/personal/.env`, using `KEY=value`. Restrict these files to
the account, for example with `chmod 600`. Restore only the variables needed by the
selected workflows. Never put values in Markdown, Git URLs, commands or sync summaries.
Check ignore coverage without printing contents:

```bash
git -C "$HOME/ai" check-ignore current/.env personal/.env
mkdir -p "$HOME/ai-data"
```

`~/ai-data/` is outside Git. Copy generated reports only when needed; machine-local
linter state, locks and sync markers should be regenerated. Do not copy `.last-sync`
from the old PC. Restore `~/ai-data/todo/display-ru.json` separately if available: it
contains Russian display titles keyed by source-entry hashes, not the backlog itself.
If absent or stale, `todo.py` exits 2; run `todo.py --missing`, translate only returned
entries/headings and merge them into the display cache per README TODO output. The
single source backlog remains `~/ai/TODO.md`.

### 5. Install the current stable instruction linter

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
`~/.local/share/agnix/current/agnix`, then the legacy0.59.0 installation, then PATH.
Per-version binaries stay in `~/.local/share/agnix/`; machine-local update state stays
in `~/ai-data/agnix/`. Do not copy successful daily state from another PC.
Use `agnix_update.py --force` to explicitly recheck the release on the same day.
Supported targets and failure behavior are documented in README "Agent instruction lint".
Keep lint report-only and review findings before changing instructions.

### 6. Verify locally, then enable normal synchronization

```bash
python3 "$HOME/ai/general/scripts/kb_find.py" knowledge-base
python3 "$HOME/ai/general/scripts/todo.py"
python3 "$HOME/ai/general/scripts/kb_lint.py"
python3 "$HOME/ai/general/scripts/build_index.py"
"$HOME/ai/general/scripts/ai-sync.sh" --dry-run
git -C "$HOME/ai" status --short
```

Review errors, warnings, generated index changes and the complete sync preview.
The preview makes no commits or pushes and does not generate weekly usage or monthly
review updates. Normal `ai-sync.sh` stages all KB changes, commits, rebases against
`origin/main` and pushes every configured origin push URL. Run it only after the
destinations and all pending changes are intentional; an agent must retain the
applicable publication permissions. A failed push leaves sync pending for retry.
There is no need to add cron or startup hooks: agents call the script at task start.

Weekly token accounting uses local client history and therefore differs across PCs.
For KB access extraction, additionally provide Node.js and the `acorn` module in its
module search path; verify `node -e "require('acorn')"`. Do not install dependencies
into the synchronized repository or copy old token totals as new local measurements.

Open a fresh session in each installed client. Ask it to identify the canonical
instruction file, resolve `current/CONTEXT.md`, find a harmless note via `kb_find.py`
and report available custom skills without exposing secrets. Check both outside and
inside `~/ai`: filesystem links alone do not prove runtime instruction loading.
Retain the checked-in `AGENTS.override.md` duplicate-loading exception and inspect existing
client overrides before modifying them. Do not assume authentication or skill
discovery passed merely because lint succeeded.

## Limits

This is documentation, not automated provisioning. It does not install software,
copy secrets, authenticate clients or authorize infrastructure changes. Local source
inspection verified the procedure; end-to-end installation on a fresh PC remains
untested. Linux is the documented baseline; Windows/macOS need separate validation
for GNU date, symlinks, Python `fcntl`, client paths and binary architecture.
Do not copy `.git/config`, SSH keys, machine caches or client auth state blindly.
