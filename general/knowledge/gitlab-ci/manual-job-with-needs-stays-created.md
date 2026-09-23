---
system: gitlab-ci
status: verified
checked: 2026-09-04
tags: [gitlab-ci, needs, dependencies, manual-job, play, api, created, artifacts]
---
# A manual job that `needs` a running job cannot be played by that job through the API

## Symptom

Job A (for example a deploy) is supposed to auto-start manual job B (smoke tests) at its end
via `POST /projects/:id/jobs/:job_id/play`, after looking up B with
`GET /projects/:id/pipelines/:pipeline_id/jobs?scope=manual`. The lookup returns nothing
("no smoke job included; nothing to start") even though B exists in the pipeline. After A
finishes, B appears as a manual job and can be started by hand.

## Cause

With `needs: [A]`, GitLab keeps B in state `created` until **all** of its needs have
finished; only then does it transition to `manual`. While A is still running (and A is the
one doing the lookup), B is not `manual` yet, so `scope=manual` does not return it and
`play` would be rejected. The dependency graph (`needs`) also controls *when* the job becomes
actionable, not only artifact flow.

## Fix

Express the artifact relationship with `dependencies` and rely on stage ordering for
execution order; the job is then `manual` from pipeline creation and discoverable while the
upstream job runs:

```yaml
smoke tests:
  stage: autotests-dev          # a stage after the deploy stage
  when: manual
  allow_failure: true
  dependencies: ["1 deploy dev"]   # fetch its artifacts; do NOT use needs here
  script: ...
```

In the upstream job, look up the exact job by name across **all pages** and play it only when
exactly one match exists:

```bash
page=1; ids=""
while :; do
  resp=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
    "$CI_API_V4_URL/projects/$CI_PROJECT_ID/pipelines/$CI_PIPELINE_ID/jobs?scope[]=manual&per_page=100&page=$page")
  ids="$ids $(echo "$resp" | jq -r '.[] | select(.name=="smoke tests") | .id')"
  [ "$(echo "$resp" | jq 'length')" -lt 100 ] && break
  page=$((page+1))
done
set -- $ids
[ $# -eq 0 ] && { echo "no smoke tests job included; nothing to start"; exit 0; }
[ $# -gt 1 ] && { echo "ambiguous: $ids"; exit 1; }
curl -sf -X POST --header "PRIVATE-TOKEN: $TOKEN" "$CI_API_V4_URL/projects/$CI_PROJECT_ID/jobs/$1/play"
```

Because B is in a later stage, GitLab still waits for A to finish before actually running B,
and A's artifacts (dotenv, reports) are available.

## Limits

- `dependencies` requires the upstream job to be in an earlier stage; with `needs` you could
  have skipped stage ordering, so the pipeline may become one stage longer.
- If A fails, B stays manual and can still be played by hand; add an ownership/metadata
  check in B if it must not run against a stale deployment.
- Renaming the job requires updating the lookup string in the upstream template; keep the
  name in one variable.
