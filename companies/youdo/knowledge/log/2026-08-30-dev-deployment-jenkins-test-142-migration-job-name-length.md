---
system: dev-deployment
status: verified
checked: 2026-08-30
tags: [jenkins, helm-charts, kubernetes, job-name, label-limit, migrations, oom, build-142, dev-devops-689]
---
# Jenkins `test/142`: migration Job names exceed Kubernetes label limit

Date: 2026-08-30  
System: B2B ephemeral dev deployment  
Jenkins: `https://build.youdo.sg/view/DevOps/job/test/142/`  
GitLab source: project `423` (`youdo.business`), pipeline `137652`, job `3100587`  
Environment: namespace `dev-devops-689`, Yandex dev Kubernetes cluster

## Findings

### Result

Jenkins build 142 finished `FAILURE` after about 230 seconds. The previously added GitLab project-ID contract worked at runtime:

```text
Resolved GitLab project 423: youdo.business -> youdo-business
```

Jenkins selected all 13 catalog services, created the namespace, and deployed in parallel. Ten application Helm releases are present and `deployed`; three releases failed and are absent:

- `youdo-business-billing-service-devops-689`
- `youdo-business-tochka-proxy-devops-689`
- `youdo-business-auth-service-devops-689`

### Primary failure

All three failures are Kubernetes validation errors for migration Job pod-template labels. The Job name is copied by Kubernetes into Job controller labels, whose values are limited to 63 characters:

| Service | Generated Job name | Length |
|---|---|---:|
| `youdo-business-billing-service` | `youdo-business-billing-service-devops-689-migration-pre-migrations` | 66 |
| `youdo-business-tochka-proxy` | `youdo-business-tochka-proxy-devops-689-migration-pre-migrations-mock` | 68 |
| `youdo-business-auth-service` | `youdo-business-auth-service-devops-689-migration-post-migrations` | 64 |

The API error for each is `spec.template.labels: Invalid value: ... must be no more than 63 characters`. Jenkins ends with `script returned exit code 1`.

The shared source is `/home/slnnk/git/helm-charts/microservice/templates/migration.yaml`: normal migration names are assembled at lines 15/30 and mock migration names at lines 139/154 as `<projectName>-migration-<migration.name>`. The clean chart worktree was at `master` commit `0881824` during the build.

Recommended correction: define one deterministic DNS-label-safe migration Job name helper and use it for both `metadata.name` occurrences in normal and mock migrations. For values over 63 characters, retain a readable prefix and append a short hash derived from the complete unshortened name. Plain `trunc 63` is unsafe because different pre/post/mock names can collide after truncation.

Naming clarification after the incident: remove the intermediate `-migration-` segment entirely and encode the hook kind directly as `-mpre`, `-mpost`, `-mpre-mock`, or `-mpost-mock`. This fits all current service names for deployment ID `devops-689`. The longest resulting name is 49 characters: `youdo-business-tochka-proxy-devops-689-mpost-mock`, leaving 14 characters below the Kubernetes limit. This solves the current catalog comfortably, but a chart-level 63-character guard remains advisable for longer task IDs or branch-slug fallback names.

### Live cluster state after failure

Read-only verification used `/home/slnnk/.kube/config-yandex-dev`. Namespace `dev-devops-689` remained Active. The following ten application releases were `deployed`:

- `youdo-business`
- `youdo-business-doc-generator`
- `youdo-business-landings`
- `youdo-business-mobile-id`
- `youdo-business-tkb-proxy`
- `youdo-kitcut`
- `youdo-notifications`
- `youdo-sms-service`
- `docvalidation`
- `fns`

Hook-created PostgreSQL and completed pre-migration resources from the failed atomic releases remain in the namespace, even though their Helm releases were uninstalled.

At the live check, the main `youdo-business` worker was in `CrashLoopBackOff` (exit 134). Its startup failed independently with `Hangfire.PostgreSql.PostgreSqlDistributedLockException` while obtaining `hangfire:lock:recurring-job:contracts-expire-created-by-task-end`. This did not cause Jenkins build 142 to fail—the pipeline had already accepted the Helm rollout—but means the partially deployed environment is not healthy.

## Open items

Next steps recorded at the time:

1. Add chart tests for short names and for deterministic, unique names at the 63-character boundary.
2. Implement the central migration Job name helper in `helm-charts` and publish it.
3. Rerun the deployment in a clean namespace or explicitly clean `dev-devops-689` first; do not treat the current partial environment as a valid smoke test.
4. After all 13 releases install, investigate/recheck the `youdo-business` Hangfire lock CrashLoop separately and perform application health checks.

## Changes

### Local chart correction

On 2026-08-30 the agreed short naming contract was implemented locally in clean `/home/slnnk/git/helm-charts` `master`:

- normal hooks: `{projectName}-mpre` and `{projectName}-mpost`;
- mock hooks: `{projectName}-mpre-mock` and `{projectName}-mpost-mock`;
- configured `migrations[].name` remains available in the `migration-name` label;
- `.gitlab-ci.yml` runs `tests/migration-job-names.sh`, which renders the real chart and asserts the four exact names and the 63-character limit.

TDD evidence: the new test first failed against the old chart and displayed all four `-migration-...` names, then passed after the template change. Both Helm charts linted successfully. All 13 current Jenkins catalog service values rendered with `devops-689`; migration Job names were unique and no longer than 49 characters. Changes are local and uncommitted/unpushed until the user requests publication. A new Jenkins runtime is still required.

### Manual worker memory override

The `youdo-business-devops-689-worker-74bd6cc4c9-qqrdd` pod repeatedly reached application startup and then was killed by the container memory limit: `OOMKilled`, exit code `137`, eight restarts at the last check. Deployment requests and limits were both `256Mi`; cluster nodes had ample free memory, so this was a container limit rather than node memory pressure. The previous Hangfire distributed-lock startup error was transient and was not the reason for the later repeated deaths. Worker logs also contained failed Hangfire jobs caused by malformed Google credential JSON, but those jobs were retried and did not terminate the process.

At the user's request, the live Deployment `youdo-business-devops-689-worker` in namespace `dev-devops-689` was manually changed with `kubectl set resources` to `requests.memory=512Mi` and `limits.memory=512Mi`. Rollout completed successfully. New pod `youdo-business-devops-689-worker-7fb6898479-2c8g9` was Ready with zero restarts and used approximately `160Mi` at the verification point; the old pod was Terminating. This is a live-only override: `/home/slnnk/git/youdo.business/devops/dev.yml` still declares `256Mi`, so a future Helm upgrade will revert it unless the values file is updated.

## Portable lesson

`~/ai/general/knowledge/k8s/job-name-exceeds-63-char-label-limit.md`
