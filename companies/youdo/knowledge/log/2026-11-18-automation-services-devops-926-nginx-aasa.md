---
system: automation-services
status: verified
checked: 2026-11-18
tags: [nginx, aasa]
---

# DevOps-926 AASA universal link

## Task

Append `/tasks-my-any-all/` to the AASA paths served by nginx. [DevOps-926](https://youtrack.youdo.com/youtrack/issue/DevOps-926).

## Context

`sysadmins/automation-services`, base `origin/master` at `72002f69`. The `youdo.com` vhost serves both AASA URLs from the same static file. The nginx role copies `.well-known` via `nginx_sync_static_content` in the production balancer inventory.

## Actions

- Proposed `DevOps-926-update-aasa` from `origin/master`. The user explicitly replied `Да` before branch creation and editing. The proposal was accepted as presented.
- Proposed commit `update AASA paths` and Ready MR `DevOps-926 update AASA paths`, source `DevOps-926-update-aasa`, target `master`, assigned to `a.solonenko`. The approved description was:

```markdown
Добавлен путь `/tasks-my-any-all/` в конец списка `applinks` файла AASA, который отдаёт nginx.

[DevOps-926](https://youtrack.youdo.com/youtrack/issue/DevOps-926)
```

- The user separately replied `Да` to the publication proposal after seeing the diff, checks, names, body and CI effects. The proposal was accepted as presented. The saved proposal snapshot matched immediately before staging.
- The complete staged diff and committed diff show one added final path, with the preceding comma, in `roles/nginx/files/sync/.well-known/apple-app-site-association`. Commit `3ffdc3587a1a0141308d8f2552ee302b862c40b3` was pushed to the approved branch.

## Findings

JSON parsed successfully. The requested path exists exactly once and is last. Removing it yields the original JSON. `git diff --check` and `git diff --cached --check` passed. The first branch push is excluded by CI rules, and there are no automatic MR or deployment jobs. GitLab confirmed an empty pipeline list.

## Status

[MR !1400](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1400) is Ready and assigned to `a.solonenko`. GitLab verified the branch and MR SHA, source, target, title and description. The checkout is clean. The requested MR publication is complete. No merge, deployment or live endpoint check was performed.

## Task metrics: DevOps-926

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-926",
  "created": "2026-11-18T19:41:34.061809+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "gitlab-mr",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": 0,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Verified MR !1400 and complete staged diff; both supervised approvals obtained",
  "updated": "2026-11-18T19:41:34.061857+03:00"
}
```
