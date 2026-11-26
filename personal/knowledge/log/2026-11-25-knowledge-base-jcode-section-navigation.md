---
system: knowledge-base
status: verified
checked: 2026-11-25
tags: [agents, search, jcode]
---

# Structured KB navigation adapted from Jcode

## Task

The user closed the CLI comparison and asked to implement useful tools and approaches from Jcode for the current rules and knowledge base. The earlier benchmark remains historical evidence. Its suggested benchmark-report extension is withdrawn for this task.

## Approach

Adapted the known-file outline used by Jcode's agentgrep for the Markdown files our workflow already searches. Previously a search result gave a bounded excerpt and the start of its source section. Agents then determined the end of the section manually. The new `kb_find.py --outline NOTE` lists headings, line numbers and anchors. `--section NOTE ANCHOR` prints the heading, body and descendants up to the next heading of the same or higher level. Both reuse the existing heading and anchor parser. Updated the shared retrieval guidance. [Jcode's structural search](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/HARNESS.md#token-optimization)

The standalone code search utility targets repository navigation. The implementation uses the existing Python helper and applies to the Markdown rules and notes in this task.

## Verification

A live check on Python 3.8 exposed two newer Python methods. Replaced them with compatible operations. The complete Material assumptions section occupies 14 lines out of 835 in the shared README at verification time. The outline reports its heading and anchor without rendering note text.

All 37 synthetic KB tests passed. The fixed real-query suite reproduced a historical-baseline miss for the unscoped operational Claude skills access query on both the committed and edited scripts. All 72 conditions produced identical ranked paths, selected sections, snippets and decision checks when compared on the same current corpus. The feature therefore introduces no measured search regression. Agent lint and KB lint reported zero findings.

## Additional upstream mechanisms

Adapted the staged diagnostic pattern from Jcode's Provider Doctor to inspect a configured KB client. `agent_lint.py --check-links codex|jcode` verifies the global instruction link and per-skill source under the current KB layers. It reports a missing link, a first-run copied file or directory, a dangling alias and a link to an old company. The check writes no report or cache and makes no client or provider request. Updated the setup guide with the command. Static link coverage does not establish instruction compliance in a live session. [Provider Doctor](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/PROVIDER_DOCTOR.md)

Local alternative mechanisms assessed include structural source code search via agentgrep, post-tool feedback and scoped session search. Existing rules already provide compact resumption checkpoints and explicit evidence of outcomes. Jcode's remote memory relevance layer is unsuitable for the local KB lookup because it forwards candidate memories to a provider. [Lifecycle hooks](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/HOOKS.md) · [Memory architecture](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/MEMORY_ARCHITECTURE.md)

## Status

The navigation, local wiring check and shared guidance are implemented and verified. This task has no outstanding actions or background operations.

## Task metrics: jcode-kb-section-navigation-2026-11-25

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "jcode-kb-section-navigation-2026-11-25",
  "created": "2026-11-25T01:09:06.101498+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Verified section navigation, parity across 72 retrieval conditions, two live KB link setups and 26 agent lint tests.",
  "updated": "2026-11-25T01:13:28.870503+03:00"
}
```
