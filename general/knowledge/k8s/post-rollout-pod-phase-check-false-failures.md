---
system: k8s
status: verified
checked: 2026-09-04
tags: [kubernetes, rollout, pods, jobs, replicaset, deletionTimestamp, ci, jenkins, health-check]
---
# Post-rollout "all pods must be Running" check fails on completed Jobs and terminating pods

## Symptom

A CI deploy step passes `kubectl rollout status` for every Deployment, then lists pods with
the release label and fails because some pod is not `Running`. Two flavours:

1. `ERROR: 2 pod(s) are not in Running state.` right after the migration Jobs are listed as
   `Completed` (phase `Succeeded`).
2. Intermittently, a pod from the **previous** ReplicaSet shows `Error`/`Failed` for a few
   seconds while it is being deleted after a successful rollout; the one-shot check catches it
   and fails an otherwise healthy deployment.

## Cause

`status.phase != Running` is not a health signal on its own:

- Job pods legitimately end in `Succeeded` (or `Failed` for retried attempts) and stay
  around until TTL/cleanup.
- During a rolling update the old ReplicaSet is scaled to 0; its pods receive a
  `metadata.deletionTimestamp`, may be reported with a terminal phase for a moment, and then
  disappear. A single `kubectl get pods` between rollout completion and garbage collection
  sees them.

## Fix

Classify pods instead of counting phases, and retry for a bounded window:

```bash
# exclude Job pods by the standard and legacy labels
SELECTOR="app.kubernetes.io/instance=${RELEASE},!batch.kubernetes.io/job-name,!job-name"

blocking() {
  kubectl -n "$NS" get pods -l "$SELECTOR" -o json | jq -r '
    .items[]
    | select(.metadata.deletionTimestamp == null)      # ignore pods already being removed
    | select(.status.phase != "Running")
    | "\(.metadata.name) \(.status.phase)"'
}

for attempt in 1 2 3 4 5 6; do
  out=$(blocking)
  [ -z "$out" ] && exit 0
  sleep 5
done
echo "Blocking pods after retries:"; echo "$out"; exit 1
```

Rules encoded above: Job pods are excluded by label; pods with `deletionTimestamp` are
ignored; any remaining `Pending`/`Failed`/`Unknown` pod is still a blocker after the retry
window (6 x 5 s here) and is reported by name and phase.

## Limits

- `rollout status` already proves the new ReplicaSet is available; this extra check is only
  worth keeping for catching sidecar/companion pods that are not part of a Deployment.
- A pod stuck `Terminating` for a long time (finalizers, node gone) is hidden by the
  `deletionTimestamp` filter; add a separate age-based alert if that matters.
- Prefer readiness (`kubectl wait --for=condition=Ready pod -l ...`) over phase when you need
  an application-level signal.
