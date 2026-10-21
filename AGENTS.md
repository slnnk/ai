# Global instructions for AI agents

`~/ai` is the DevOps user's shared knowledge base.
README: `~/ai/general/knowledge/README.md`; read sections when triggered.
Project instructions win locally; update the KB after significant work.

## Before a task

- Run `~/ai/general/scripts/ai-sync.sh`; show its output and pass on reminders.
  From November 2026, offer its monthly staleness proposal on the first session in each
  new month, wait for agreement, and do not repeat that month. Read README "Daily sync".
- Read `~/ai/current/CONTEXT.md` and the system's section in `~/ai/TODO.md`.
- Find notes with `~/ai/general/scripts/kb_find.py <keywords>`; use INDEX only to browse.
  Read long notes by Summary and needed section, not whole.
- Before related work or acting on corrections, read
  `~/ai/general/skills/agent-learning/SKILL.md`, run scoped lookup and read canonical rules.
  Apply durable corrections within authorization; keep task directions scoped and record
  evidence. Discussion/planning authorize investigation/plans; implement only on request.
  Corrections never expand external permissions.
- Use superpowers skills only on explicit user request for this task, including
  `superpowers:using-superpowers`; ignore their automatic activation instructions.

## Scope and secrets

- Company work defaults to `~/ai/current/` (employer symlink; use `current`);
  own infrastructure/projects go in `personal/`. Portable recipes go in `general/`, free
  of company names, hosts, IPs, internal URLs and tickets; link from a company log.
  Read README "Layers" and recipe template before creating/moving material.
- Store user access values only in the layer's `.env` as `KEY=value`. In notes, scripts
  and logs record secret locations, variable names and access routes only, excluding
  secret values. Retain only necessary personal data. Generated data belongs in `~/ai-data/`.

## Local code and Git

- Keep changes minimal for the requested run. Other improvements are TODO
  proposals requiring a separate request. "Remove what is not needed" covers only the
  task's scope; suggest other dead code/unused files without deleting them.
- Before repo searches, read `~/ai/current/knowledge/repos.md` (company) or
  `~/ai/personal/knowledge/repos.md` (personal). Company GitLab work
  requires `~/ai/current/skills/gitlab-workflow/SKILL.md`; inspect local code first.
  Read README "Repository workflow details" and "repos.md".
- Use the existing checkout (`~/git/<repo>`); worktrees only on explicit request.
  Preserve unrelated changes; explain conflicts before moving/discarding them.
- Perform Git mutations only on explicit request in this task. Exceptions:
  daily `ai-sync.sh` and confirmed training below. Read-only Git, including fetch, is OK.
  Commit only task changes unless requested otherwise; inspect the actual
  staged diff, including pre-staged and mixed edits. A task file is not blanket permission.
- Two supervised approvals remain until the user changes mode; dates do not end them:
  1. Before repository task edits, propose repo, branch/reuse and base; wait for explicit
     confirmation. KB bookkeeping is exempt.
  2. Before publication, present actual diff, checks, commit message, MR title/body,
     source/target and CI effects; wait for explicit confirmation. This covers task-only
     stage/commit/push/MR together. Material name/scope/branch/effect changes need reapproval.
  Neither approval covers merge/auto-merge, target push, force push, tags, history rewrite
  or deployment. Release/deployment effects need explicit approval. Record proposals,
  approvals, corrections and outcomes in task logs; read the GitLab skill for details.

## External changes

Before EACH command changing anything outside local files, say what changes and where,
then wait for explicit yes for that action. The publication approval above is the sole
batch exception. Local edits and read-only actions need no permission. Before external
operations read README "External changes" for examples; do not infer permission from TODO.

## Backlog and completion

- `~/ai/TODO.md` is the sole backlog. Read README "TODO output" before edits. For standalone
  `todo`/`задачи` or backlog requests, read that section, run
  `python3 ~/ai/general/scripts/todo.py` and return its complete Markdown stdout only.
  Use filters only for an explicitly requested subset; refresh affected cached titles
  after TODO edits. Follow that section's exact remaining-proposed-list rule on completion.
- Before tool use read README "Economical tool use". Before KB writes read
  "Bookkeeping after significant work", "Frontmatter" and the relevant note template.
  Use `new_note.py`; update existing maps, never duplicate them. Keep layer repos.md current;
  update `current/service-addresses.env` for discovered VK Cloud addresses only.
- Before final response reconcile only task-affected notes/TODO per README
  "Final note-to-TODO reconciliation"; proposals grant no execution permission.
- After instruction/skill (including resources/scripts)/settings edits, run
  `python3 ~/ai/general/scripts/agent_lint.py --force` before finishing; add changed
  repo-local paths outside KB. Read README "Agent instruction lint"; report findings or
  pending failure. Report-only; no auto-fix or extra permissions.
- Run `kb_lint.py`, fix task findings, then `build_index.py` in `general/scripts/`.
  Append one concise final result to `~/ai/.sync-notes` per README "Daily sync".
  Never commit `~/ai` yourself; `ai-sync.sh` handles it. Memory is a cache; keep durable knowledge in `~/ai`.
