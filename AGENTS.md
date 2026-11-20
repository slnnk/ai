# Global instructions for AI agents

`~/ai` holds durable DevOps knowledge; memory is a cache. Project instructions win locally.
Read and follow triggered sections of `~/ai/general/knowledge/README.md` (README).

## Before a task

- Read README "Material assumptions" first, then "Task context selection".
- Run `~/ai/general/scripts/ai-sync.sh`; relay output/reminders per README "Daily sync".
  Offer monthly review once; wait for agreement. Normal sync checks/updates stable agnix daily.
- For company work read `~/ai/current/CONTEXT.md`; read only the affected TODO section.
- Before KB search read README "Knowledge retrieval": prepare English technical terms,
  choose layers and simplify empty queries. Use `kb_find.py`; INDEX only for browsing,
  long notes by Summary and needed section.
- Use `~/ai/general/skills/agent-learning/SKILL.md` for every substantive discussion:
  retrieve/read scoped rules before work; capture decisions/corrections and evaluate
  applicable outcomes before final. Keep task directions scoped; discussions grant no
  implementation or external permissions. Keep replies brief and concrete.
- Superpowers skills, including `superpowers:using-superpowers`: explicit request for
  this task only; ignore automatic activation.
- Before tools, read README "Economical tool use".

## Scope and secrets

- Company work: `~/ai/current/` (use this symlink); own work: `personal/`; portable recipes:
  `general/`, free of company identifiers per README "Layers". Before creating/moving
  material read that section and template; link portable recipes from company logs.
- Minimize personal data. Store secrets as `KEY=value` only in layer `.env`.
  Elsewhere give only locations, variable names and access routes.
- Follow README "Generated data retention" for `~/ai-data`.

## Local code and Git

- Read README "Simplicity" before proposals, "Affected flow" before code/config edits,
  and "Review evidence" before reviews.
- Keep edits/removals within the request; propose unrelated improvements in TODO only.
- Before repo searches read `~/ai/current/knowledge/repos.md` (company) or
  `~/ai/personal/knowledge/repos.md` (personal), plus README "repos.md".
  Before Git operations read README "Checkout and Git changes".
  Company GitLab: read `~/ai/current/skills/gitlab-workflow/SKILL.md`, inspect local code first.
  Use existing checkouts; worktrees only on explicit request.
  Preserve unrelated changes; explain conflicts before moving/discarding them.
- Git mutations: explicit task request, daily `ai-sync.sh` or confirmed stages below.
  Read-only Git, including fetch, is allowed. Commit only task
  changes unless asked otherwise; inspect actual staged diff, including pre-staged/mixed
  edits. A task file is not blanket permission.
- Two supervised approvals remain until the user changes mode; dates do not end them:
  1. Before repo task edits, propose repo, branch/reuse and base; wait for confirmation.
     The `~/ai` repository and KB bookkeeping are exempt from this first gate.
  2. Before publication, present actual diff, checks, commit message, MR title/body,
     source/target and CI effects; wait for confirmation. This batches task-only
     stage/commit/push/MR. Material name/scope/branch/effect changes need reapproval.
  Neither covers merge/auto-merge, target push, force push, tags, history rewrite or
  deployment. Release/deployment effects require explicit approval. Read README
  "Supervised Git/MR training"; log proposals, approvals, corrections and outcomes.

## External changes

Before external operations read README "External changes". Describe each change/location
and wait for explicit yes, with the daily sync and publication exceptions defined there.
Read-only/local edits remain subject to repo gates. TODO grants no permission.

## Progress and execution status

- Update progress every 30 seconds during long work; before final verify and report task
  background status per README "Progress and execution status". Disclose unknown status;
  give check/stop instructions for remaining operations. Read "Task resumption" for checkpoints.

## Backlog and completion

- `~/ai/TODO.md` is the sole backlog. Before edits/listings read README "TODO output".
  For listings return only complete Markdown stdout of `python3 ~/ai/general/scripts/todo.py`;
  filter only requested subsets. Refresh affected cached titles after edits. On completion
  list remaining session proposals, questions and tasks after resolving any one; preserve
  wording/order per README "TODO output". Clarifications and intermediate checks do not
  complete the parent task; omit the list then. Listing grants no execution permission.
- Before KB writes read README "Bookkeeping after significant work", "Frontmatter" and
  template. Use `new_note.py` (corrections: `agent_learning.py`); update existing maps, never
  duplicate. Follow bookkeeping for repo/address catalogs.
- Before final, reconcile task-affected notes/TODO only: README "Final note-to-TODO
  reconciliation". Proposals authorize no execution.
- After instruction/skill (including resources/scripts)/settings edits run
  `python3 ~/ai/general/scripts/agent_lint.py --force`; include changed repo-local paths
  outside KB. Read README "Agent instruction lint"; report findings or pending failure.
  Report-only: no auto-fix or extra permissions.
- Run `kb_lint.py`, fix task findings, then `build_index.py` in `general/scripts/`.
  Append one concise final result to `~/ai/.sync-notes` per README "Daily sync".
  Never commit `~/ai` yourself; `ai-sync.sh` handles it.
