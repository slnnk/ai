---
system: agent-learning
status: verified
checked: 2026-10-19
tags: [agents, corrections, learning]
---
# Shared correction learning workflow across agents

## Task

Systematize reusable user corrections so coding agents retrieve and apply them in
future sessions. The user first requested research and a tailored plan, then explicitly
authorized full implementation without a pilot. Superpowers skills were excluded.

## Context

The current conversation is the authority for scope and authorization. All three
instruction entrypoints (`~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md` and
`~/.gemini/GEMINI.md`) are symlinks to `~/ai/AGENTS.md`. Existing dated corrections
already live in `current/CONTEXT.md` and the canonical Git/MR workflow, so the design
extends capture, retrieval and verification rather than creating competing policies.

The [earlier behavior review](2026-10-12-knowledge-base-agent-behaviour-two-week-review.md)
found that stronger wording alone did not prevent stale follow-ups. Existing shared
instructions require portable general content, English notes and one central TODO.

## Actions

Read the shared instructions, relevant README sections, existing correction conventions,
script help and parser/linter behavior. Inspected agent instruction symlinks and skill
directory paths without reading secrets. Recorded the existing dirty checkout before
editing; unrelated changes were preserved.

Research reference established in the conversation: [Task Observer](https://github.com/rebelytics/one-skill-to-rule-them-all)
and its [user guide](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/USER-GUIDE.md).
The coordinating agent also researched these primary implementations:

- [self-improvement skill](https://github.com/pskoett/pskoett-ai-skills/blob/main/skills/self-improvement/SKILL.md).
- [claude-reflect](https://github.com/BayramAnnakov/claude-reflect).
- [Dreamer dream skill](https://github.com/whistler/dreamer/blob/main/skills/dream/SKILL.md).
- [reflect skill](https://github.com/hansvangent/reflect-skill-claude/blob/main/SKILL.md).
- [continuous-learning-v2](https://github.com/affaan-m/ECC/blob/main/skills/continuous-learning-v2/SKILL.md).
- [Emulo mining prompt](https://github.com/ohad6k/emulo/blob/main/MINING_PROMPT.md).

Selected a local combination of capture, deduplication, retrieval, recurrence diagnosis
and behavior verification. No complete third-party plugin is being installed. The
initial correction is the user's explicit distinction between discussing a proposal
and authorizing execution. Five existing explicit policies were linked as initial
evidence: discussion versus execution, preserving unrelated checkout changes, established
service deployment, base-image releases from master, and updating existing recovery
summaries. These are policy imports with provenance, not five newly observed failures;
no inferred historical rule was silently promoted.

Created these documentation notes with `general/scripts/new_note.py` and updated the
README script/discovery guidance. Implemented the shared skill, helper, tests and review
prompt. Added the common instruction entrypoint and linked the skill into Codex and
Claude. The sandbox initially blocked the Codex link; the approved escalated command
created that single local link. Gemini receives the procedure through its existing
shared instruction link; native Gemini skill discovery was not assumed.

## Findings

`kb_find.py` and the indexer find Markdown recursively under layer `knowledge/`
directories. A root-level `.learnings` directory would not participate in normal KB
search. Frontmatter status remains `verified|hypothesis|outdated`; workflow lifecycle
must use a separate field. Existing Codex and Claude skill directories support symlinks;
Gemini can read the portable skill through shared instructions without assuming native
skill discovery.

Proposed and final local names are `agent-learning` for the portable skill,
`agent_learning.py` for its CLI, and `agents/correction-learning.md` for the recipe.
This work uses the shared KB workflow, not a task branch or company MR. No Git
publication, deployment or infrastructure change is authorized by correction learning.

## Changes

- `general/knowledge/agents/correction-learning.md`: portable capture/retrieval/check procedure.
- `general/knowledge/README.md`: CLI catalog entry and agent integration guidance.
- This log: authorization, integration evidence, implementation boundaries and limitations.
- `AGENTS.md`: mandatory correction workflow, scoped retrieval and discussion boundary.
- `general/skills/agent-learning/SKILL.md`, `references/operations.md`, `agents/openai.yaml`:
  portable behavior, CLI operations and discovery metadata.
- `general/scripts/agent_learning.py`: record/query/link/resolve/verify/report/check;
  scoped evidence, deduplication, revision history, locking and atomic writes.
- `general/scripts/tests/test_agent_learning.py`: isolated regression cases.
- `general/prompts/review-agent-learning.md`: bounded review entrypoint.
- Five dated evidence records in personal/current knowledge logs, linked to existing policies.
- Local Codex and Claude skill symlinks; shared instructions already cover all three agents.

No manual Git mutation, commit, push, MR, scheduler, plugin installation or external
state write was performed. Existing unrelated local changes were preserved. Daily
sync remains responsible for publishing KB changes.

## Verification

Local checks cover concurrent writers, duplicate occurrence IDs across agents,
Russian lookup, global/company/repository/task isolation, revision-specific evaluation,
adoption and rejection, dry-run/read-only invariance, corrupt data and missing-target
repair. Skill metadata validation passed. Independent review found and drove fixes
for omitted repository rules, stale expectations, inactive records, and target repair.
Three independent scenario interpretations respected task-only scope, explicit durable
preferences and repeated violation of a loaded rule; these were not recorded as actual
fresh-client successes.

Final checks on 2026-10-19:

- `python3 -B -m unittest discover -s general/scripts/tests -p test_agent_learning.py -v`:
  all 15 tests passed, including 18 concurrent writer invocations with deduplicated events.
- Skill creator `quick_validate.py`: valid skill.
- `agent_learning.py check`: five valid records; scoped query returned the matching
  company deployment rule and both active global rules.
- `agent_learning.py report`: five recorded/linked/active rules, zero applicable real
  evaluations; success remains unknown.
- Codex/Claude skill symlinks and all three shared instruction links were checked.
- `kb_lint.py`: zero errors and six existing warning categories: oversized global
  instructions and five older notes with Cyrillic outside code. The global file grew
  from 9641 to 10244 bytes; unrelated rules were not reorganized.
- Task-scoped `git diff --check`: passed. Whole-checkout check reports a preexisting
  blank line at EOF in `current/knowledge/systems/tracing.md`; that unrelated file was
  left untouched. Generated bytecode from this task was removed.

The five real records are linked and active; real applicable-task outcomes are initially
unknown. Query/record/lint success does not demonstrate future compliance. No pilot,
mass history scan or recurring review job was created. Actionable follow-ups belong
only in `~/ai/TODO.md`.

## Portable lesson

[Correction learning across coding agents](../../../general/knowledge/agents/correction-learning.md)
