---
system: nomad
status: verified
checked: 2026-08-20
tags: [nomad, canary, rollback, job-revert, job-promote, ci, auto_promote]
---
# `nomad job revert` hangs in CI when the job uses canaries with `auto_promote = false`

## Symptom

A CI rollback job runs `nomad job revert <job> <previous-version>` and never finishes; the
pipeline job sits at "running" until an operator promotes the deployment in the Nomad UI or
the CI timeout kills it. The reverted version is placed as a canary and stays there.

## Cause

`nomad job revert` does not restore the old allocations in place. It submits a **new job
version** whose jobspec (including the `update` block) is copied from the target version. If
that block has `canary > 0` and `auto_promote = false`, the resulting deployment waits for a
manual `promote`, exactly like a normal deploy. Without `-detach`, the CLI monitors the
deployment and therefore blocks for as long as the canary waits.

Two related traps:

- Promoting immediately after the revert fails: Nomad returns HTTP 500 until the canary
  allocation is healthy.
- In Nomad 1.5.x the Go template field `DeploymentState.PlacedCanaries` is a **list of
  allocation IDs**, not a count. Use `len $state.PlacedCanaries` in `-t` templates.

## Fix

Make the rollback a two-phase operation in the same CI job and keep `auto_promote = false` in
the jobspec (turning it on globally would also remove the approval gate from normal deploys):

```bash
set -eu
: "${ROLLBACK_CANARY_DELAY:=60}"    # seconds; must exceed normal task startup time
: "${ROLLBACK_TIMEOUT:=600}"        # seconds; bound the whole promotion loop

# 1. submit the revert without blocking on the deployment monitor
out=$(nomad job revert -detach "$JOB" "$PREVIOUS_VERSION")
echo "$out"
# a revert to the already-running version yields no evaluation -> nothing to promote
echo "$out" | grep -q 'Evaluation ID' || { echo "no-op revert"; exit 0; }

# 2. wait for the canary to become healthy
sleep "$ROLLBACK_CANARY_DELAY"

# 3. promote the (only) active deployment, bounded
deadline=$(( $(date +%s) + ROLLBACK_TIMEOUT ))
until nomad job promote "$JOB"; do
  [ "$(date +%s)" -lt "$deadline" ] || { echo "promotion timed out"; exit 1; }
  sleep 10
done
```

Do not mark the rollback job `allow_failure`: a rollback that did not complete must be
visible.

## Limits

- `nomad job promote <job>` targets the job's **latest** deployment. The shortcut is only safe
  if no other deployment of the same job can be active during a rollback (serialize deploy
  and rollback pipelines, or track the exact deployment ID from the revert evaluation).
- The fixed delay is a heuristic; raise it if tasks regularly need more than 60 s to pass
  health checks, or replace it with a poll of `nomad deployment status`.
- Verified live with Nomad CLI 1.5.3 (CI image) and 1.3.5 (local); both support `-detach`
  and `job promote`.
