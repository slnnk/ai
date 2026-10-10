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

- Run `~/ai/general/scripts/ai-sync.sh` (daily commit and push; instant when already done).
  Do not hide its output; pass any reminder it prints on to the user.
  Starting in November 2026, offer the knowledge-base staleness review on the first
  session in each new month, even if it is after day 1. Use the monthly proposal from
  `ai-sync.sh`; wait for user agreement and do not repeat it later in the same month.
- Read `~/ai/current/CONTEXT.md` and the system's section in `~/ai/TODO.md`.
- Find notes with `~/ai/general/scripts/kb_find.py <keywords>` (hosts, jobs, services,
  tickets); open `INDEX.md` only to browse. Read a long note by its `## Summary` and the
  needed section (`sed -n A,Bp`), not whole.
- Check `knowledge/repos.md` before searching the disk for a repository.

## Which layer

- Company hosts, services, repositories, tickets, people: `current/`. This is the default.
- The user's own infrastructure and projects: `personal/`.
- A lesson reusable at any employer: `general/`, as a recipe (symptom, cause, fix, limits)
  with no company name, hostnames, IPs, internal URLs or ticket ids; publishable as is.
  From a company task: log entry in `current/` linking to a recipe rewritten for `general/`.

## After significant work

- New notes via `python3 ~/ai/general/scripts/new_note.py log|system|recipe ...`, then fill
  the sections. Log entry: task, context, actions and key commands, findings, changed files,
  risks. Update the existing system map; never create a duplicate.
- Frontmatter (`system`, `status: verified|hypothesis|outdated`, `checked`, `tags`) on every
  note. Mark hypotheses in the text; `status: outdated` instead of deleting. English;
  hostnames, jobs, variables and commands verbatim.
- Keep `knowledge/repos.md` current (path, origin URL without credentials, purpose, date).
- Run `kb_lint.py` and fix what it reports, then `build_index.py` (both in `general/scripts/`).
- `echo "- <system>: <what changed and why>" >> ~/ai/.sync-notes`. Do not commit `~/ai`
  yourself; `ai-sync.sh` does it.

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

Agent memory (`~/.claude/projects/*/memory` etc.) is a cache; anything worth keeping also
goes to `~/ai`.

## Code changes

- Keep repository adaptations minimal: change only what is needed for the requested run.
  Put optional hardening, refactors, helper tooling and other improvement proposals in
  `~/ai/TODO.md`; do not implement them without a separate request.

- "Remove what is not needed" means only what the current task touches. List other dead
  code, commented blocks and unused files as suggestions; do not delete them.

## Git

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

### Supervised Git/MR training (2026-10-08 through 2026-10-30)

- Before editing repository task files, propose the branch name, repository and base
  branch; wait for explicit confirmation. That approval permits creating/switching to
  the approved task branch and making the task's local file changes. If reusing a branch,
  propose reuse for approval. Read-only investigation and KB bookkeeping can proceed.
- After implementation and checks, present the actual diff summary, check results,
  commit message, MR title, source/target and relevant CI effects. Wait for explicit
  confirmation. That approval covers staging the task's explicit paths, committing,
  pushing the approved branch and creating/updating its MR as one publication action;
  do not ask again for each command. Corrections must be applied before execution.
  Material changes to approved names, scope, target or effects require renewed approval.
- Branch: `<TASK-ID>-<english-kebab-case>`; suffix describes the change, not the repository name; respect observed project exceptions.
  Commit: concise lowercase English action + object, no mandatory task ID or feat:/fix:.
  MR title: `<TASK-ID> <change summary>`. Preserve project settings.
  MR description: one short paragraph in Russian describing the change, then a link
  to the task, and nothing else. Do not include checks, related tasks/MRs, dependencies
  or CI details. Keep those details in the work log and publication approval summary.
  No separate Closes policy is needed.
- No merge, auto-merge, direct target-branch push, force push, tags, history rewriting
  or deployment is authorized by these approvals. CI runtime changes/releases still
  need explicit approval covering those effects. Preserve unrelated user changes.
- Record each task's proposed/final names, approvals, corrections, results and MR link
  in its work log. Apply reusable user corrections immediately to the canonical rules
  below (and this file if global); keep task-specific exceptions scoped to that task.
  Do not infer broader permissions from wording corrections.
- Canonical details and training evidence: `~/ai/current/knowledge/systems/gitlab-ci/agent-git-workflow.md`.
  Prepare the training report on 2026-10-30, or the first session after that date,
  following the due item in `~/ai/TODO.md`. Continue supervised mode until the user
  reviews the results and explicitly chooses automation or further training.

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
