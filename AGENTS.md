# Global instructions for AI agents

The user is a DevOps engineer. `~/ai` is the shared knowledge base for every AI agent
(Codex, Claude Code, Gemini, ...). Agent-specific directories (`~/.codex`, `~/.claude`)
hold only symlinks into `~/ai` plus the agent's own runtime state.

## Layout

    ~/ai/AGENTS.md                      this file
    ~/ai/general/                       portable knowledge, no company context
      knowledge/<technology>/           docker/, nomad/, gitlab-ci/, k8s/, ansible/, dotnet/, ...
      knowledge/README.md               layer rules in detail, note and system-map templates
      skills/  scripts/  prompts/
    ~/ai/personal/                      the user's own servers, VPN, side projects
      knowledge/{INDEX.md,systems/,log/,repos.md}  scripts/  .env
    ~/ai/companies/<name>/              everything tied to one employer
      CONTEXT.md                        role, priorities, stack and conventions at this company
      knowledge/{INDEX.md,systems/,log/,repos.md}  skills/  scripts/  prompts/  .env
    ~/ai/current -> companies/<name>    active employer; always address it as `current`

## Before a task

- Run `~/ai/general/scripts/ai-sync.sh`. It commits and pushes the knowledge base once a day
  (state in `~/ai/.last-sync`) and exits instantly when already done today.
- Read `~/ai/current/CONTEXT.md`.
- Open `knowledge/INDEX.md` of the relevant layer, then the system map in `knowledge/systems/`.
- `grep -ril <keyword> ~/ai/general/knowledge ~/ai/personal/knowledge ~/ai/current/knowledge`
  for hosts, jobs, services, tickets.
- Check `knowledge/repos.md` before searching the disk for a repository.

## Which layer

- Company hosts, services, repositories, tickets, people: `current/`. This is the default.
- The user's own infrastructure and projects: `personal/`.
- A lesson reusable at any employer: `general/`, written as a recipe (symptom, cause, fix,
  limits) with no company name, hostnames, IPs, internal URLs or ticket ids. Must be
  publishable as is.
- A company task that yields a portable lesson: log entry in `current/`, recipe in `general/`,
  link from the log entry to the recipe. Never copy a company note into `general/` with
  identifiers stripped; rewrite it.

## After significant work

- Create new notes with `python3 ~/ai/general/scripts/new_note.py log|system|recipe ...`;
  it sets the path, name and frontmatter. Then fill the sections.
- Log entry: `knowledge/log/YYYY-MM-DD-<system>-<slug>.md`. Cover: task, context (project,
  environment, hosts, ticket), actions and key commands, findings and conclusions, changed
  files, remaining risks and TODO.
- System map: update the existing file in `knowledge/systems/`; never create a duplicate.
- Run `python3 ~/ai/general/scripts/kb_lint.py` and fix what it reports; `ai-sync.sh` also
  prints findings at the start of the next day.
- Repositories: keep `knowledge/repos.md` current: local path, origin URL without
  credentials, purpose, related system, date checked.
- Regenerate indexes: `python3 ~/ai/general/scripts/build_index.py`.
- Append one line to `~/ai/.sync-notes` describing the work for the daily commit message:
  `echo "- <system>: <what changed and why>" >> ~/ai/.sync-notes`.
- Do not commit or push `~/ai` yourself; the daily `ai-sync.sh` run does it.
- Every note starts with frontmatter:

      ---
      system: <system or technology>
      status: verified | hypothesis | outdated
      checked: YYYY-MM-DD
      tags: [optional, keywords]
      ---
      # Title

- Mark hypotheses and unverified claims explicitly in the text. Update `checked` after
  re-verification. Set `status: outdated` instead of deleting.
- Write notes in English. Keep hostnames, job names, variables and commands verbatim.

## Scripts and prompts

- Reusable scripts go to `<layer>/scripts/`: parameters via CLI args or env vars, `--help` or
  a header comment. Do not save one-off drafts; put the important command into the log entry.
- Reusable prompts go to `<layer>/prompts/<name>.md`.

## Secrets

- Never write passwords, tokens, private keys, cookies or one-time codes into notes,
  scripts or logs.
- Access variables provided by the user go only to `<layer>/.env` as `KEY=value`.
- For secrets found in infrastructure record only the location, variable name and access
  route (bastion, VPN, vault path, role). Never the value.
- Do not copy personal data without need.

## Backlog

`~/ai/TODO.md` is the user's backlog for the knowledge base itself. Read it when asked to
review it; add entries only when the user asks.

## Agent memory

The agent's own memory (for example `~/.claude/projects/*/memory`) is a cache. Anything
worth keeping is also written to `~/ai`.

## Connecting an agent

- Instructions: symlink to `~/ai/AGENTS.md` from `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`,
  `~/.gemini/GEMINI.md`.
- Skills: one symlink per directory from `~/ai/general/skills/` and `~/ai/current/skills/`
  into the agent's skills folder (`~/.codex/skills/`, `~/.claude/skills/`).
- Switching employer: create `companies/<new>/`, repoint `current`, redo skill symlinks.

## Git

- Never run state-changing git commands (`git add`, `git commit`, `git push`, `git tag`,
  `git merge`, `git rebase`, `git reset`, `git stash`, ...) in any repository unless the
  user explicitly asks for it in the current task. Read-only commands (`status`, `diff`,
  `log`, `show`, `fetch`) are fine.
- Exception: the daily `~/ai/general/scripts/ai-sync.sh` run, which commits and pushes `~/ai`.

## Changes outside local files

- Ask the user for permission before every command that changes state anywhere other than
  local files. Examples: `terraform apply`/`destroy`, `ansible-playbook` without `--check`,
  `kubectl apply`/`delete`/`scale`, `nomad job run`/`stop`, `helm install`/`upgrade`,
  `docker` commands on shared hosts, editing files or restarting services on remote servers
  over ssh, and API calls that create, update or delete (POST/PUT/PATCH/DELETE to GitLab,
  YouTrack, Zabbix, cloud providers, ...).
- Say what the command changes and where, then wait for an explicit yes. A yes covers only
  that action; ask again for the next one.
- No permission is needed for editing local files (including files in a repository
  checkout), or for read-only commands: `terraform plan`, `--check`/`--diff`, `kubectl get`,
  GET requests, reading logs.

## Precedence

Project-level instructions win on conflicts inside that project. Keeping `~/ai` current
after significant work is expected regardless.
