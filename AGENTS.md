# Global instructions for AI agents

`~/ai` holds durable DevOps knowledge; memory is a cache. Project instructions win locally.
Read triggered sections of `~/ai/general/knowledge/README.md` (README); follow their rules.

## Before a task

- Run `~/ai/general/scripts/ai-sync.sh`; relay output/reminders. Read README "Daily sync"
  for monthly review proposals; offer once per month and wait for agreement.
  Normal runs also check the latest stable agnix daily and update the local install.
- Read `~/ai/current/CONTEXT.md` and the affected system in `~/ai/TODO.md`.
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
- Access values only in the layer's `.env` as `KEY=value`; elsewhere only secret locations,
  variable names and access routes. Minimize personal data;
  generated data goes in `~/ai-data/`.

## Local code and Git

- Keep changes within the request, including removals; propose unrelated improvements
  in TODO without implementing/deleting them.
- Before repo searches read `~/ai/current/knowledge/repos.md` (company) or
  `~/ai/personal/knowledge/repos.md` (personal), plus README "repos.md" and
  "Repository workflow details".
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

Before EACH command changing state outside local files, describe changes/location and
wait for explicit yes; publication is the sole batch exception. Read-only/local edits need
no permission subject to repo gates. Before external operations read README "External
changes"; TODO grants no permission.

## Progress and execution status

- During long work update progress at least every 30 seconds. Before final, verify task
  background commands/agents; state completion and any remaining operations, with check/stop
  instructions. Disclose unknown status. Read README "Progress and execution status".

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
