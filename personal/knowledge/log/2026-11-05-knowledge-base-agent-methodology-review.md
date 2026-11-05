---
system: knowledge-base
status: verified
checked: 2026-11-05
tags: [agents, review, automation, permissions]
---
# Agent methodology review: policies, skills and automation

## Summary

Reviewed the local agent operating method: policies, skills, prompts, retrieval,
maintenance scripts and verification boundaries. The user clarified that knowledge
content itself is out of scope. No content-freshness or infrastructure findings are
adopted from the preliminary broad inspection. No implementation was requested.
The layered design and permission boundaries are sound; reproducible weaknesses
remain in failure handling, secret-scan coverage, instruction retrieval and policy
consistency. The existing test suites pass, but isolated failure scenarios do not.
The initial review changed no rules, skills or implementation scripts and made no
task-specific external writes. Later on 2026-11-05 the user requested point 1 only;
[F1 was fixed](2026-11-05-knowledge-base-sync-checker-failure-stop.md). Remaining
remediation stays proposed in the central backlog.

## Task

Review the overall method used by local agents in `~/ai`. The initial request was
interpreted too broadly as also covering stored knowledge. The user's same-session
clarification restricted the review to rules, skills, scripts and other instructions
that govern agent work. This is a task-scope correction, not a global prohibition on
future content audits. The parent stopped the content audit and excluded its findings.

## Context

- Canonical policy: [AGENTS](../../../AGENTS.md) and
  [procedures](../../../general/knowledge/README.md).
- Reviewed four local skills, associated procedural references, three prompts,
  instruction links, setup guidance and the principal maintenance/retrieval scripts.
- The working tree already contained unrelated modifications. An initial status/hash
  snapshot and generated test artifacts are under
  `/home/slnnk/ai-data/ai-review/2026-11-05/`.
- One unrelated company log changed concurrently between the initial and final hash
  snapshots; this review did not write it. The benchmark separately confirmed stable
  inputs throughout its own run. This is a working-tree review, not a locked revision.
- Delegation was authorized by the existing economical-tool-use rule. The parent
  explicitly retained sync, index, TODO and canonical-write ownership; reviewers
  performed read-only inspection and temporary local reproductions.

## Actions

1. Ran the required startup sync. It reported instruction lint success and no reminder.
   Read applicable policy and queried scoped learning records and canonical targets.
2. Reviewed policy coherence, automation failure paths and retrieval behavior in parallel.
3. Ran existing local test suites and lint checks, and the saved retrieval regression
   suite against its unchanged accepted baseline.
4. Independently repeated isolated synthetic reproductions of the secret-scan gap,
   checker failure and missing-root behavior. Fixtures used fake credentials and mock
   Git; they did not publish, change the real Git index or access external services.
5. Recorded method-only findings and proposed follow-ups; preserved existing permissions.

## Findings

### F1 — P1: sync proceeds after the protective checker crashes

Resolved after the review by explicit user request on 2026-11-05; see the
[implementation and checks](2026-11-05-knowledge-base-sync-checker-failure-stop.md).
The original diagnosis below is retained as evidence.

At [ai-sync.sh](../../../general/scripts/ai-sync.sh), lines 145–154, `kb_lint.py`
exit status is discarded. Only an output line beginning with `E secret` blocks the
commit. A traceback is neither reported nor treated as a failed check.

An unchanged sync script with a failing checker and mocked Git exited zero,
invoked mock commit and wrote `.last-sync`; the simulated exception was invisible.
This establishes that the publication path is not stopped by checker execution
failure. The reproduction deliberately had no real remote.

Proposal: distinguish completed lint findings from tool failure; fail the publication
path when the secret check cannot complete. Preserve the explicitly chosen report-only
handling of ordinary nonsecret findings and instruction lint.

### F2 — P1: secret scanning omits non-Markdown staged content

[kb_lint.py](../../../general/scripts/kb_lint.py), lines 122–134, restricts both
staged and complete inventories to `.md`. Sync stages all files at line 140 and
separately rejects only the exact `.env` filename at lines 141–143.

A synthetic PAT in a Python file produced zero findings; the same bytes in Markdown
were detected. This is a coverage defect, not evidence of a real leaked credential.

Proposal: separate secret scanning from Markdown validation, inspect the staged
contents of all publishable text formats, and handle unreadable/unsupported inputs
explicitly. Add paired fixtures for script/config/backup formats and staged content.

### F3 — P2: targeted correction retrieval loses to unrelated global rules

[agent_learning.py](../../../general/scripts/agent_learning.py), lines 387–400,
bypasses system and keyword filters for active global records, sorts by active state
and update time, then applies the default eight-result limit.

The real query `query --scope personal --system agents discussion-before-implementation`
returns eight other global records and omits the exact requested key. A footer offers
a larger limit, but neither exact-key precedence nor automatic recovery is provided.

Proposal: prioritize exact keys and task/repository applicability; prevent mandatory
global context from consuming the entire quota for targeted results. Add a regression
with more global records than the default limit. Keep global obligations visible.

### F4 — P2: missing input roots look like empty or successful checks

With `AI_ROOT` pointing to a nonexistent directory:

- [kb_find.py](../../../general/scripts/kb_find.py), lines 37–45: exit 1, zero notes,
  no stderr; indistinguishable from a legitimate empty query.
- [kb_lint.py](../../../general/scripts/kb_lint.py), lines 128–134: exit 0,
  zero errors and warnings.
- [build_index.py](../../../general/scripts/build_index.py), lines 189–193:
  skips all layers but returns exit 0 for `--check`.

Proposal: validate the root and explicitly requested layers before enumeration.
Distinguish a deliberately optional unconfigured layer from a broken configured link.
This implements the existing requirement that unavailable knowledge is not absence.

### F5 — P2: duplicated procedural rules already disagree

- [rp skill](../../../current/skills/rp/SKILL.md), lines 75–77, accepts owner
  tracker activity as evidence without chat context, while lines 127–128 prohibit
  tracker-only items. Clarify the latter as excluding items without period activity.
- [normalization prompt](../../../general/prompts/normalize-notes.md), line 32,
  directs agents to choose a new topic when a system-map target exists; README line 45
  requires updating the existing map. Merge evidence for the same system; reserve
  separate topics for genuinely distinct components.
- [new_note.py](../../../general/scripts/new_note.py), line 42, emits `Open items`,
  while the current log template uses `Status and risks` with central TODO links.
- Company CONTEXT line 78 still recommends INDEX first, whereas AGENTS lines 12–14
  require scoped search and reserve INDEX for browsing. README line 69 also retains
  unscoped lint-fix wording where AGENTS line 84 restricts fixes to the task.

Proposal: choose one complete canonical formulation for each rule; entry points should
contain an applicability trigger and reference rather than another competing procedure.
Keep current user-selected approvals and exceptions unchanged.

### F6 — P2: retrieval quality degrades as the corpus grows

The saved 72-condition benchmark returned exit 1. Case `c01`, operational query,
lost its target and visible answer from the top five in both scoped and unscoped
modes: the source moved from rank 5 to rank 8 after three additional matching logs.
The default 15-result search still contains it; the document itself is not missing.
The search script hash is unchanged from the baseline and the corpus changed.

[kb_find.py](../../../general/scripts/kb_find.py), lines 221–226, ranks by title/path
term coverage and absolute matching-line count. This favors keyword-rich logs and
long documents without an explicit authoritative-source preference.

Proposal: review ranking using the fixed suite and broader representative cases;
measure response size and target/answer visibility. Do not alter the baseline merely
to accept this failed run. This is a mechanism finding, not a recommendation to edit
the business facts in the case documents.

### F7 — P3: instruction dependencies are outside ordinary link validation

[android-dig runbook](../../../current/skills/android-dig/references/runbook.md),
line 65, names a nonexistent legacy map path. The established target is
`~/ai/current/knowledge/systems/android-farm/system-map.md`.
[kb_lint.py](../../../general/scripts/kb_lint.py), lines 175–176, skips link validation
for non-note instruction files, and lines 204–211 ignore ordinary link anchors.
The runbook reference is also plain inline code, rather than a Markdown link.

Proposal: use machine-checkable local links for instruction dependencies and validate
their targets/anchors in skills, README and context documents. Report coverage explicitly.

## Architecture assessment

Strengths: compact entry policy with triggered detail, specialized skills, deterministic
helpers, local-first repository work, preserved approval boundaries, isolated sync
preview, verified updater downloads and scoped decisions separate from evidence status.
The learning workflow correctly separates recorded, linked, loaded and behaviorally
demonstrated rules. These foundations should be retained.

Priorities for simplification, rather than additional broad instructions:

- Select task context by personal/company/portable scope. Company CONTEXT is currently
  mandatory even for unrelated personal work. Separate daily maintenance from task
  semantics without silently removing already authorized maintenance.
- Define coordinator versus reviewer responsibilities. Only the coordinator should
  perform shared sync/index/TODO/final bookkeeping; apply the existing learning parent
  ownership principle consistently to other shared state.
- Replace mandatory delegation at more than three files (README lines 267–268) with
  independent-work and reading-volume criteria. File count alone does not establish
  token savings; this review does not claim a measured economic benefit.
- Keep exact approval choices intact. Two Git stages, explicit external-write approval,
  daily stable updater and progress frequency are user decisions, not defects merely
  because they add work.
- Add a bounded fresh-session behavior suite after the deterministic faults are fixed.
  Check scope/skill selection, planning without implementation, unrelated-change
  preservation, repeated permission avoidance and child-agent housekeeping boundaries.
  The current learning report has no recorded evaluations; this is not proof that no
  historical behavioral pilots exist or that the rules fail in every session.

## Context engineering discussion follow-up

On 2026-11-05 the user asked whether Anthropic's
[Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)
applies to this method. The discussion refined the existing proposals rather than
authorizing implementation. Initially only its broad overlap and a short sync result
were persisted; the following details were reconciled when the user asked whether
all proposals were recorded. These are local application recommendations, not new
active instructions or measured improvements.

| Discussion recommendation | Existing central TODO proposal |
| --- | --- |
| Load context by task scope; retain staged discovery through search and selected sections | Task applicability and coordination |
| Ensure exact and task-relevant rules survive retrieval limits; evaluate ranking as sources grow | Instruction and knowledge retrieval, F3/F6 |
| Keep one full canonical formulation with triggers and references elsewhere | Skills, prompts and templates, F5/F7 |
| Distinguish success, empty results and execution failure; return concise tool summaries with paths to details | Automation F2/F4 for input failures; applicability and coordination for output shaping; F1 already fixed |
| Preserve compact resumption state: user goal, authorized scope, decisions, completed checks and next step | Task applicability and coordination |
| Delegate independent substantial work with concise evidence; give shared housekeeping to one coordinator | Task applicability and coordination |
| Compare behavior in fresh sessions by correctness, missed constraints, unnecessary reads, elapsed time and token usage | Task applicability and coordination |

The proposed resumption state belongs in the existing task record; it is not a second
backlog. Goal, restrictions, already granted approvals and preservation of unrelated
changes remain essential when selecting or compacting context. Current approval
choices are retained. No numeric context limit, mandatory new retrieval service or
demonstrated cost reduction was established. The agent's own overly broad outputs
in this conversation illustrate execution drift despite existing economical-read rules.

All remaining actions are represented by the existing four central proposals, with
this section as supporting detail. No duplicated task or new implementation approval
is implied by recording the discussion.

The user subsequently requested continued proposal recording and primary-source
developer research. [The research and R1–R7 mappings](2026-11-05-knowledge-base-developer-best-practices-research.md)
extend these same proposals. The user then clarified that recording was requested
only within this dialogue. The mistakenly added standing README rule was removed
and its learning entry rejected; see the [scope correction](2026-11-05-knowledge-base-developer-best-practices-research.md#scope-correction).
The saved proposals are retained and the researched technical changes remain proposals.

## Verification

| Check | Result |
| --- | --- |
| General script unittest discovery | 105 tests passed |
| Company workflow unittest discovery | 20 tests passed |
| `agent_lint.py --force` | 9 entry files; zero errors, warnings or info |
| `kb_lint.py` before bookkeeping | zero errors/warnings |
| `agent_learning.py check` | 24 valid records |
| `agent_learning.py report` | 22 linked, 17 active, zero recorded evaluations |
| Saved retrieval suite, unchanged baseline | 72 conditions; exit 1, c01 regression |
| Failure/coverage fixtures | F1, F2 and F4 independently reproduced |

Final KB lint remained at zero errors/warnings and indexes were rebuilt. Whole-tree
`git diff --check` reported one pre-existing extra blank line at EOF in an unrelated
company log; its hash is unchanged from the initial snapshot. It was not repaired
under this review. Task bookkeeping paths pass their focused whitespace check.

Generated evidence: `~/ai-data/ai-review/2026-11-05/reproduce.py`,
`reproductions.json`, `missing-root.json`, and `retrieval/` (results, cases, manifest,
summary). Retrieval manifest records unchanged inputs during the run. The real-query
suite is private generated data, retained outside Git. Tests verify local scripts;
no fresh client activation, external API, cloud state or clean-machine installation
was exercised in this task.

## Changes

Only this review log, proposed central TODO follow-ups, affected display-cache titles,
generated index and one final sync note are task bookkeeping. Existing policy/skill/
script changes in the working tree predate this review and were not overwritten.
No task fixes, commits, push, MR or infrastructure changes were performed.

## Status and risks

Review complete on 2026-11-05. The user subsequently requested only F1, now
[implemented and verified](2026-11-05-knowledge-base-sync-checker-failure-stop.md).
F2–F7 and optional architecture simplification remain proposals in
[central TODO](../../../TODO.md), Knowledge base; that record does not authorize
implementation. Content-audit observations are excluded from follow-ups.
All reviewer tasks and test commands finished; no background work remains.

## Portable lesson

none
