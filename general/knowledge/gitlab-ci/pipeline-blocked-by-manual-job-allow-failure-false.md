---
system: gitlab-ci
status: verified
checked: 2026-08-21
tags: [manual, allow_failure, blocked, rollback, when-manual, pipeline-status]
---
# Pipeline stays "Blocked"/manual after a successful deploy

## Symptom

A production pipeline finished all deploy steps successfully, yet its status is `manual`
(shown as **Blocked** in the UI) and downstream jobs such as `release` or `notify` stay
`created` and never run. Nothing failed; no runner is involved.

## Cause

A manual job with `allow_failure: false` is a **blocking manual job**: the pipeline cannot
proceed past its stage until an operator plays it. `when: manual` jobs default to
`allow_failure: true` (non-blocking), but a rule or template may set `allow_failure: false`
explicitly. A typical case is a manual rollback job at the end of a deploy stage: the template
authors made it blocking on purpose so the pipeline waits for a human decision after the
deployment.

Identify the job through the API rather than by scrolling the UI:

```bash
curl -s --header "PRIVATE-TOKEN: $TOKEN" \
  "$CI_API_V4_URL/projects/<id>/pipelines/<pipeline_id>/jobs?per_page=100" \
  | jq -r '.[] | select(.status=="manual" and .allow_failure==false) | "\(.id) \(.name) \(.stage)"'
```

Then trace the job's definition through `extends`/`include` to the rule that sets
`when: manual` and the `allow_failure` value.

## Fix

Nothing to repair. Decide operationally:

- If the manual job is a rollback or another destructive action, **do not play it just to
  clear the status**. Leave it or cancel the finished pipeline according to the release
  procedure.
- If the pipeline must complete automatically, change the job or template deliberately:
  either `allow_failure: true` on the manual job (it becomes non-blocking and downstream
  stages continue), or move the downstream jobs before it / give them `needs:` that do not
  depend on the blocking stage. Review the safety impact before changing a rollback gate.

## Limits

- Cancelling the pipeline does not undo anything the deploy did; it only removes the
  pending manual jobs.
- Manual jobs with `allow_failure: true` never block; if the pipeline is blocked, at least one
  manual job has `allow_failure: false`.
