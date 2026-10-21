---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [agents, instructions, context-budget]
---
# Knowledge base: shorten shared agent instructions

## Summary

User requested implementation of the AGENTS.md shortening proposal from the central TODO.
Shared instructions decreased from 12189 to 5593 bytes (54.1 percent), below the 5632-byte
warning threshold. Detailed procedures moved into the existing rule README, with explicit
read triggers. Secret handling, task scope, Git permissions, both supervised approvals and
per-command external-change consent remain directly visible. No permission policy changed.

## Context

[Original audit and proposal](2026-10-20-knowledge-base-lint-warning-review.md).
Canonical instructions: `~/ai/AGENTS.md`; procedures: `~/ai/general/knowledge/README.md`.
Existing unrelated working-tree changes were preserved. No dedicated personal knowledge-base
system map exists; the existing README is the maintained procedural reference.

## Actions and findings

- Ran daily sync, scoped agent-learning lookup and source-note/context review.
- Moved layout into Layers, bookkeeping into Frontmatter, repository details into repos.md,
  economical tool use and external examples into Scripts, and backlog details into TODO output.
- Retained explicit read triggers for every task, repository work, KB/TODO writes, listing
  and final reconciliation. Restored ordinary-task tool-use and durable-memory obligations
  after a separate read-only coverage review identified trigger gaps.
- Used explicit repository-registry paths to avoid a new missing-file lint finding.
- Compared original policy coverage against both final documents. Shared entrypoint links,
  AGENTS.override.md and agent settings were not changed.

Key checks: `agent_lint.py --force`, `kb_lint.py`, `build_index.py`, relative-link and
README-section checks, and `git diff --check` for the changed tracked documentation.

## Changed files

`AGENTS.md`, `general/knowledge/README.md`, this log, the original audit's dated outcome,
central TODO completion status and generated personal knowledge index. One final result
was appended to `.sync-notes`; no manual Git mutation or external change was performed.

## Status and risks

Completed on 2026-10-20. Final forced agent lint:9files/0errors/1warning/2informational
findings. Remaining warning CDX-CFG-025 concerns unchanged Codex settings; informational
AGM-004 and CDX-AG-008 concern the global document shape and intentional override.
KB lint:0errors/5existing language warnings; the size warning is gone. Language false
positives remain a separate open proposal, not part of this implementation.
Static checks and same-session coverage review do not prove fresh-client activation of
conditional README reads; no broader behavioral experiment or policy weakening was done.

## Portable lesson

None; the existing README retains the reusable procedures.
