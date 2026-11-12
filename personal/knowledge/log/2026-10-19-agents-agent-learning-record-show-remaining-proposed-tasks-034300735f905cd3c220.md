---
system: agents
status: verified
checked: 2026-11-11
tags: [agents, learning]
---
# Agent learning: show-remaining-proposed-tasks

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T18:42:39.188583+00:00",
  "decisions": [
    {
      "at": "2026-10-19T18:44:17.704042+00:00",
      "decision": "adopted",
      "expected": "After completing an item from an agent-proposed list, show remaining unfinished items using the original wording, order, numbering, grouping and formatting; remove only completed items. If none remain, say so.",
      "revision": 2,
      "source": "User clarification on 2026-10-19: display remaining tasks in the same form as initially, because the reformatted list had discrepancies.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T18:13:52.941240+00:00",
      "decision": "adopted",
      "expected": "Track proposals, questions and tasks raised by either participant across the session. After resolving one, display remaining unresolved items with original wording and order; retain deferred context, omit resolved or explicitly cancelled items, and say when none remain. Listing grants no execution permission.",
      "revision": 3,
      "source": "User instruction in current session, 2026-11-11: after resolving one session proposal, question or task, display the remaining items.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T18:16:35.910268+00:00",
      "decision": "adopted",
      "expected": "Track session proposals, questions and tasks. Show remaining unresolved items only after actually settling an underlying question or completing task/proposal work. Clarifications, explanations, status updates and approach discussions do not trigger a list; recording a correction during them does not complete the underlying work. Preserve original wording/order and deferred context; listing grants no execution permission.",
      "revision": 4,
      "source": "User correction in current session, 2026-11-11: explanation of NEXUS_DOCKER_PASSWORD check was clarification only, not resolution; show remaining items only after resolving a question or completing task/proposal work.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T18:31:16.861046+00:00",
      "decision": "adopted",
      "expected": "Show remaining session proposals, questions and tasks only after completion of an agreed parent task/proposal or settlement of the underlying question. Individual messages, requested intermediate checks, explanations, status updates and recording corrections do not qualify. Before listing, identify the agreed parent item that closed; if none closed, omit the list. Preserve original wording/order; listing grants no execution permission.",
      "revision": 5,
      "source": "User correction in current session, 2026-11-11: password verification did not resolve the ongoing task and must not trigger the remaining-items list.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T19:49:30.800640+00:00",
      "decision": "adopted",
      "expected": "After completing an agreed parent task/proposal or settling the underlying question, explicitly list remaining session action items with original wording/order. A count of files or vague remaining-work statement is not a substitute. Intermediate checks, explanations and corrections do not themselves close the parent task. Listing grants no execution permission.",
      "revision": 6,
      "source": "User correction 2026-11-11 after Jenkins push: explicitly list remaining points after completing one; a statement about nine remaining files is insufficient.",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
  "evaluations": [
    {
      "at": "2026-11-11T18:16:35.550367+00:00",
      "cause": "Treated an explanatory clarification as resolution of the underlying open item.",
      "event_id": "2026-11-11-mr1371-clarification-premature-list",
      "expected": "Track proposals, questions and tasks raised by either participant across the session. After resolving one, display remaining unresolved items with original wording and order; retain deferred context, omit resolved or explicitly cancelled items, and say when none remain. Listing grants no execution permission.",
      "outcome": "fail",
      "revision": 3,
      "rule_loaded": "yes",
      "source": "Current session: assistant appended remaining items after merely explaining the controller password check; user explicitly corrected that no item had been resolved.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T18:31:03.212038+00:00",
      "cause": "Used completion of an intermediate verification step as the trigger instead of completion of the agreed parent task.",
      "event_id": "2026-11-11-mr1371-password-check-premature-list",
      "expected": "Track session proposals, questions and tasks. Show remaining unresolved items only after actually settling an underlying question or completing task/proposal work. Clarifications, explanations, status updates and approach discussions do not trigger a list; recording a correction during them does not complete the underlying work. Preserve original wording/order and deferred context; listing grants no execution permission.",
      "outcome": "fail",
      "revision": 4,
      "rule_loaded": "yes",
      "source": "User correction in current session: password verification was an intermediate step of the unresolved Nexus secret task, so appending remaining items was premature.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T19:49:30.523616+00:00",
      "cause": "Recognized completion but substituted a vague count of files for the explicit remaining action items.",
      "event_id": "2026-11-11-sync-publication-missing-explicit-remaining-list",
      "expected": "Show remaining session proposals, questions and tasks only after completion of an agreed parent task/proposal or settlement of the underlying question. Individual messages, requested intermediate checks, explanations, status updates and recording corrections do not qualify. Before listing, identify the agreed parent item that closed; if none closed, omit the list. Preserve original wording/order; listing grants no execution permission.",
      "outcome": "fail",
      "revision": 5,
      "rule_loaded": "yes",
      "source": "After completing approved Jenkins push to MR1396, assistant replaced the remaining action list with a count of nine runner files. User explicitly corrected the missing remaining-items list.",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
  "expected": "After completing an agreed parent task/proposal or settling the underlying question, explicitly list remaining session action items with original wording/order. A count of files or vague remaining-work statement is not a substitute. Intermediate checks, explanations and corrections do not themselves close the parent task. Listing grants no execution permission.",
  "key": "show-remaining-proposed-tasks",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T18:42:39.188583+00:00",
      "cause": "",
      "event_id": "codex-20261019-remaining-proposed-tasks-1",
      "expected": "After completing a task from a list initially proposed to the user, show the remaining unfinished tasks in the final response; if none remain, say so.",
      "source": "User instruction in the local-agent TODO discussion on 2026-10-19, following implementation of nested Codex accounting.",
      "summary": "After completing the classifier task, the user requested showing remaining tasks from the originally proposed list after each completion."
    }
  ],
  "repo": "",
  "revision": 6,
  "scope": "global",
  "summary": "User broadened the remaining-items rule to all session proposals, questions and tasks, including prose and multiple turns.",
  "system": "agents",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-11-11T19:49:30.800640+00:00",
  "version": 1
}
```
