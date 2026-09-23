---
system: gitlab-ci
status: verified
checked: 2026-08-20
tags: [gitlab-ci-templates, nomad, canary, rollback, deploy-prod, job-revert, job-promote]
---
# Nomad canary rollback in GitLab CI templates

- Last checked: 2026-08-20
- Repository: `/home/slnnk/git/gitlab-ci-templates`
- Safe origin: `git@gitlab.youdo.sg:sysadmins/devops-tools/gitlab-ci-templates.git`
- Relevant template: `v3/.deploy-prod.yml`, hidden job `.deploy-prod-rollback`
- Consumers include `v3/.deploy-prod-only-web.yml`, `v3/.deploy-prod-only-web-auto.yml`, `v3/.deploy-prod-web-migrations*.yml`, and `v3/.deploy-prod-full*.yml`.

## Problem and confirmed cause

`.deploy-prod-rollback` runs `nomad job revert` synchronously. Reverting to an older Nomad job version creates a new job version and deployment using the old version's update strategy. For jobs with `update.canary > 0` and `auto_promote = false`, the new rollback deployment waits for manual canary promotion. The CLI monitors the result because `-detach` is absent, so the GitLab rollback job remains running until an operator promotes it in Nomad.

## Recommended change

Implement rollback as a two-phase operation in the same CI job:

1. Run `nomad job revert -detach` to submit the rollback without blocking the CLI monitor.
2. Because production rollback is assumed to be the only active deployment, wait for the canary startup delay.
3. Run `nomad job promote <job>` to promote the only active deployment.
4. Wrap promotion in a finite timeout so the CI job cannot hang forever.

This deliberately relies on the operational invariant that no other deployment of the same Nomad job is active during rollback. If that invariant changes, restore exact evaluation/deployment tracking or add pipeline serialization before using `job promote`.

The rollback is an emergency recovery path, so automatic promotion is intentional. Do not set `auto_promote = true` globally in the Nomad jobspec: that would also remove the manual approval gate from normal production canary deploys.

## Implemented on 2026-08-20

Updated `.deploy-prod-rollback` in `v3/.deploy-prod.yml`:

- `nomad job revert` now uses `-detach`;
- no-op reverts are detected from the absence of an evaluation;
- the job waits `DEPLOY_PROD_ROLLBACK_CANARY_DELAY` (default 60 seconds);
- `nomad job promote` promotes the only active rollback deployment;
- promotion is bounded by `DEPLOY_PROD_ROLLBACK_TIMEOUT` (default 600 seconds);
- rollback is no longer `allow_failure`.

Syntax was checked with Bash and Ruby/Psych. The available local Nomad v1.3.5 CLI and CI image Nomad v1.5.3 both support the used flags. A live test confirmed that promoting before canary health returns HTTP 500, so the startup delay remains necessary.

## Live verification on Yandex test Nomad, 2026-08-20

- Endpoint variable: `NOMAD_YANDEX_TEST_ADDR`; token variable: `NOMAD_YANDEX_TEST_TOKEN` (values remain only in `~/ai/current/.env`).
- CI image tested: `registry.youdo.sg/sysadmins/nomad:latest`.
- Nomad CLI in the image: v1.5.3.
- Test datacenter: `yandex-test`; the queried nodes were ready.
- Temporary job: `codex-canary-rollback-check-20260820`, namespace `default`.
- Test task used the same internal Nomad image with a long-running shell sleep loop; update strategy was one canary, `auto_promote = false`, and task-state health checks.

Sequence completed successfully:

1. Created job version 0 with metadata `test_version=v1`; initial deployment became successful.
2. Submitted version 1 (`v2`), observed one placed and healthy canary waiting for manual promotion, promoted it, and verified the version was stable.
3. Submitted and promoted version 2 (`v3`), producing three known job versions.
4. Ran the rollback script extracted directly from `v3/.deploy-prod.yml` with target `NOMAD_PREVIOUS_VERSION=1`.
5. Revert evaluation `25206917-4799-cd79-6169-124bc8eb136e` created deployment `d836d6c9-6220-9bf5-9b47-fbf967141e07` and new job version 3 with metadata `test_version=v2`.
6. The script detected one healthy rollback canary, promoted the exact deployment, and observed final status `successful`; the active allocation was job version 3.
7. Stopped and purged only the temporary test job; a subsequent status check confirmed it no longer existed.

The live test found that Nomad v1.5.3 exposes `DeploymentState.PlacedCanaries` as a list of allocation IDs, not an integer. The CI Go template was corrected to use `len $state.PlacedCanaries`. This correction was included in the successful rollback run. No production job was changed.

A second live test used `codex-canary-rollback-simple-20260820`: the first immediate-promotion attempt correctly reproduced Nomad's HTTP 500 for an unhealthy canary; after waiting for canary health, rollback v3 → v2 succeeded with deployment `57ac0c01-7862-49fd-809c-213f4a63a5c3`. The temporary job was then stopped and purged. The final fixed-delay variant was syntax-checked after this live test; its fixed delay is intentionally based on the agreed single-active-deployment operational assumption.

## Risks and validation

- The fixed canary delay must remain longer than the normal allocation startup time; increase it if test jobs regularly need more than 60 seconds.
- The simplified flow is unsafe if another deployment can be active concurrently, because `nomad job promote` targets the job's latest deployment.
- Current `.deploy-prod-rollback` fails the CI job when promotion times out or returns an error.

## References

- HashiCorp Nomad CLI: `job revert`, `job deployments`, `deployment promote`, `deployment status`.
- Nomad `update` block: `canary` blocks rollout until promotion when `auto_promote = false`.

## Portable lesson

`~/ai/general/knowledge/nomad/job-revert-canary-manual-promotion.md`
