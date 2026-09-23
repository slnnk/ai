---
system: dev-deployment
status: verified
checked: 2026-09-04
tags: [jenkins, jenkins-pipelines, replicaset, pod-phase, race, groovy-tests, build-152]
---
# Dev deployment: Jenkins old-ReplicaSet pod race correction

Date: 2026-09-04  
System: B2B ephemeral dev deployment  
Repository: `/home/slnnk/git/jenkins-pipelines`  
Related incident: GitLab job `3112382`, Jenkins build `152`

## Task

The service deployment stage first completed `kubectl rollout status` successfully, then performed a single namespace pod query and failed if any non-Job pod had a phase other than `Running`. During build 152, Kubernetes was deleting an old ReplicaSet pod whose displayed status briefly became `Error`; the one-shot check treated it as an active workload failure.

## Changes

Local correction:

- Added `getBlockingDeploymentPods` to classify pod-list JSON.
- Pods with `metadata.deletionTimestamp` are ignored because they are already being removed from an old rollout.
- Pods owned by Jobs are excluded through the standard `batch.kubernetes.io/job-name` label and the legacy `job-name` label.
- Active pods whose phase is not `Running` remain blockers.
- The Jenkins deployment stage now repeats the check six times with five seconds between attempts. This absorbs short control-plane/ReplicaSet transitions but still fails after the bounded retry period and reports blocking pod names and phases.
- Added fixtures covering Running, Pending, Failed, deletion-marked old ReplicaSet, current Job, and legacy Job pods.

Changed files:

- `pipelines/deploy-dev-b2b.Jenkinsfile`
- `tests/deploy_dev_b2b_test.groovy`

## Actions

Verification executed locally:

```bash
java -cp /opt/android-studio-2024.1.1/android-studio/lib/groovy.jar groovy.ui.GroovyMain tests/deploy_dev_b2b_test.groovy
git diff --check
```

Result: Groovy tests passed and the diff has no whitespace errors.

## Open items

- Completed: committed and pushed to `jenkins-pipelines/master` as `20b9d78` (`fix race condition`).
- Run a repeat deployment that replaces a ReplicaSet and confirm that a terminating old pod cannot fail the build while a persistent current Pending/Failed pod still does. (Runtime-proven in Billing Jenkins build `158` on 2026-09-04.)

## Portable lesson

`~/ai/general/knowledge/k8s/post-rollout-pod-phase-check-false-failures.md`
