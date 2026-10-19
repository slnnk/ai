# Global instructions for AI agents

The user is a DevOps engineer. `~/ai` is the shared knowledge base for every AI agent
(Codex, Claude Code, Gemini, ...). Details, templates and the script list:
`~/ai/general/knowledge/README.md`.

## Layout

    ~/ai/general/     portable knowledge, no company context: knowledge/<technology>/, skills/, scripts/, prompts/
    ~/ai/personal/    the user's own servers, VPN, side projects: knowledge/, scripts/, .env
    ~/ai/companies/<name>/  one employer: CONTEXT.md, knowledge/, skills/, scripts/, prompts/, .env
    ~/ai/current -> companies/<name>   active employer; always address it as `current`
    ~/ai-data/        generated data of skills and scripts, one subdirectory per tool (e.g. rp/); outside git, may hold private data
    knowledge/ = INDEX.md, systems/ (maps), log/ (dated entries), repos.md

## Before a task

- Run `~/ai/general/scripts/ai-sync.sh` (daily Git sync plus changed-agent-file lint).
  Do not hide its output; pass any reminder it prints on to the user.
  Starting in November 2026, offer the knowledge-base staleness review on the first
  session in each new month, even if it is after day 1. Use the monthly proposal from
  `ai-sync.sh`; wait for user agreement and do not repeat it later in the same month.
- Read `~/ai/current/CONTEXT.md` and the system's section in `~/ai/TODO.md`.
- Find notes with `~/ai/general/scripts/kb_find.py <keywords>` (hosts, jobs, services,
  tickets); open `INDEX.md` only to browse. Read a long note by its `## Summary` and the
  needed section (`sed -n A,Bp`), not whole.
- Before searching the disk for a repository, check `~/ai/current/knowledge/repos.md`
  for company work or `~/ai/personal/knowledge/repos.md` for personal work.

## Skills

- Use `superpowers` skills only when the user explicitly requests them for the current
  task. Do not automatically invoke them based on task type or their own activation
  instructions, including `superpowers:using-superpowers`.

## Learn from corrections

- Before related work and when corrected, read `~/ai/general/skills/agent-learning/SKILL.md`
  and run its scoped rule lookup. Read applicable canonical targets before acting.
- Apply explicit durable corrections immediately within existing authorization; keep
  task-specific directions scoped. Record evidence and diagnose repeats using the skill.
- Discussion and planning authorize investigation and the requested plan; implementation
  starts after a request to implement. A correction never expands external permissions.

## Which layer

- Company hosts, services, repositories, tickets, people: `current/`. This is the default.
- The user's own infrastructure and projects: `personal/`.
- A lesson reusable at any employer: `general/`, as a recipe (symptom, cause, fix, limits)
  with no company name, hostnames, IPs, internal URLs or ticket ids; publishable as is.
  From a company task: log entry in `current/` linking to a recipe rewritten for `general/`.

## After significant work

- New notes via `python3 ~/ai/general/scripts/new_note.py log|system|recipe ...` (correction
  evidence via `agent_learning.py`), then fill
  the sections. Log entry: task, context, actions and key commands, findings, changed files,
  risks. Update the existing system map; never create a duplicate.
- Frontmatter (`system`, `status: verified|hypothesis|outdated`, `checked`, `tags`) on every
  note. Mark hypotheses in the text; `status: outdated` instead of deleting. English;
  hostnames, jobs, variables and commands verbatim.
- Keep the relevant layer's `~/ai/<layer>/knowledge/repos.md` current
  (path, origin URL without credentials, purpose, date).
- For VK Cloud only, maintain `~/ai/current/service-addresses.env`: whenever a new or
  changed service address is discovered, add or update it in the relevant datacenter
  section. Keep credentials in `.env`; record the observation date and known verification
  status in comments. Updating the map does not require extra infrastructure checks.
- Before the final response, reconcile notes created or changed in this task with
  `~/ai/TODO.md`: track remaining actions with source links, align completed/cancelled/deferred
  status and supersede stale directions while preserving history. Optional improvements stay
  proposals, not execution permission. Review only this task's affected records; details in
  `general/knowledge/README.md`, "Final note-to-TODO reconciliation".
- After changing agent instructions, skills (including references/scripts), or agent settings,
  run `python3 ~/ai/general/scripts/agent_lint.py --force` before the final response.
  Add changed repository-local files/directories as arguments when outside `~/ai`.
  Review findings and report the result; if unavailable or failed, report the pending check.
  Use report-only mode; findings do not grant permission for fixes or external actions.
- Run `kb_lint.py` and fix what it reports, then `build_index.py` (both in `general/scripts/`).
- Append one concise final result per completed task to `~/ai/.sync-notes`: system, what
  changed and why, key check and material remaining risk. Keep stage details in the task log.
  Do not commit `~/ai` yourself; `ai-sync.sh` does it.

## Token economy

- Check `<layer>/scripts/` before improvising. A sequence of three or more commands run
  twice becomes a script (CLI args or env, `--help`, compact summary output).
- Reading more than three files or a long log: delegate to a subagent that returns a few
  lines of conclusions.
- Never print a whole file or raw output when a line will do: `head`, `grep -c`, `wc -l`,
  `--quiet`.
- Reusable prompts go to `<layer>/prompts/<name>.md` with a `model:` tier line.

## Secrets

- Never write passwords, tokens, private keys, cookies or one-time codes into notes,
  scripts or logs.
- Access variables provided by the user go only to `<layer>/.env` as `KEY=value`.
- For secrets found in infrastructure record only the location, variable name and access
  route (bastion, VPN, vault path, role). Never the value.
- Do not copy personal data without need.

## Backlog

`~/ai/TODO.md` is the single live list of open work for all layers, grouped by system. Add
open items there as `- [ ] action (date) — [src](note)` and close finished ones; notes keep
no TODO lists of their own.

For standalone `todo` or `задачи` requests (case-insensitive, optional punctuation), or
requests to show the backlog, run `python3 ~/ai/general/scripts/todo.py`. Return its
complete Markdown stdout as the final answer: Russian descriptions, ordinary bullet lists,
no dates, source links or checkboxes; no code fence, extra commentary or silent truncation.
Use short task titles (6–12 words, at most 120 characters), with no blank lines between
items in a group. Keep details in source TODO; preserve IDs and deferral/proposal labels.
Default: all open items in file order. Reuse the derived Russian display cache; on exit 2
run with `--missing`, translate only missing descriptions and rerun (README: "TODO output").
After editing TODO entries, refresh affected cached descriptions in the same task.
For an explicitly requested subset use `--layer`, `--system` or `--query`; never infer a
company-only filter from the default layer. On failure report the error, not an empty list.
See `general/knowledge/README.md`, "TODO output", for the contract. Listing tasks is
read-only and does not authorize executing them.

After completing a task from a list you initially proposed to the user, show the remaining
unfinished items in the final response, preserving the original wording, order, numbering,
grouping and formatting; remove only completed items. If none remain, say so.

Agent memory (`~/.claude/projects/*/memory` etc.) is a cache; anything worth keeping also
goes to `~/ai`.

## Code changes

- Keep repository adaptations minimal: change only what is needed for the requested run.
  Put optional hardening, refactors, helper tooling and other improvement proposals in
  `~/ai/TODO.md`; do not implement them without a separate request.

- "Remove what is not needed" means only what the current task touches. List other dead
  code, commented blocks and unused files as suggestions; do not delete them.

## Git

- For company GitLab work, use `~/ai/current/skills/gitlab-workflow/SKILL.md`.
  Inspect code in an existing local checkout first; consult `current/knowledge/repos.md`
  before searching. Clone a missing project into `~/git/<repo>` without overwriting
  existing paths. Use GitLab for remote revisions, MR discussion, CI and settings.
- Work in the existing repository checkout (`~/git/<repo>` by default), not a separate
  git worktree. Create a separate worktree only when the user explicitly requests it.
  Preserve unrelated local changes; if they block switching branches, explain the
  conflict before taking any action that moves or discards them.
- Commits must contain only changes made by the agent for the current task, unless
  the user explicitly asks to include other changes. Check the actual staged diff,
  including pre-staged changes and mixed user/agent edits within the same file;
  selecting a task file does not authorize committing every change in that file.
- Never run state-changing git commands (`git add`, `git commit`, `git push`, `git tag`,
  `git merge`, `git rebase`, `git reset`, `git stash`, ...) in any repository unless the
  user explicitly asks for it in the current task. Read-only commands (`status`, `diff`,
  `log`, `show`, `fetch`) are fine.
- Exceptions: the daily `~/ai/general/scripts/ai-sync.sh` run, which commits and pushes
  `~/ai`, and the explicitly confirmed training stages below.

### Supervised Git/MR training (started 2026-10-08)

- Keep two approvals until the user explicitly chooses a different mode. The early
  report was delivered on 2026-10-19; the date alone never changes permissions.
- Before repository task edits, propose repository, branch/reuse and base branch;
  wait for explicit confirmation. KB bookkeeping is exempt.
- Before publication, present the actual diff, checks, commit message, MR title/body,
  source/target and CI effects; wait for explicit confirmation. One confirmation covers
  task-only staging, commit, push and MR creation/update. Do not ask per command again.
  Material changes to names, scope, source/target or effects require renewed approval.
- Neither gate authorizes merge, auto-merge, target-branch push, force push, tags,
  history rewriting or deployment. Triggered release/deployment effects need explicit
  approval covering them. Preserve unrelated user changes, including pre-staged edits.
- Detailed workflow and naming conventions are canonical in the
  skill `~/ai/current/skills/gitlab-workflow/SKILL.md`; training history and the early report
  are linked from system map `~/ai/current/knowledge/systems/gitlab-ci/agent-git-workflow.md`.
  Record original/final proposals, both approvals, corrections and outcomes in task logs.

## Changes outside local files

- Ask the user for permission before every command that changes state anywhere other than
  local files. Examples: `terraform apply`/`destroy`, `ansible-playbook` without `--check`,
  `kubectl apply`/`delete`/`scale`, `nomad job run`/`stop`, `helm install`/`upgrade`,
  `docker` commands on shared hosts, editing files or restarting services on remote servers
  over ssh, and API calls that create, update or delete (POST/PUT/PATCH/DELETE to GitLab,
  YouTrack, Zabbix, cloud providers, ...).
- Say what the command changes and where, then wait for an explicit yes. A yes covers only
  that action; ask again for the next one. Exception: the second training-stage approval
  above covers commit + branch push + MR creation/update for the reviewed task together;
  it does not authorize other external changes.
- No permission is needed for editing local files (including files in a repository
  checkout), or for read-only commands: `terraform plan`, `--check`/`--diff`, `kubectl get`,
  GET requests, reading logs.

## Precedence

Project-level instructions win on conflicts inside that project. Keeping `~/ai` current
after significant work is expected regardless.
