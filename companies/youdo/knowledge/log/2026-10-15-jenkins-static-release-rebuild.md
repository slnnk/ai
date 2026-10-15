---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, gitlab, static, vk-test]
---
# MR108 merge, test5 retry and static Release-2.917 rebuild

## Task and authorization

User explicitly instructed merging MR108, launching deployment, updating the static CI variable, and rebuilding the latest release pipeline if static source needs no edits. These external actions authorized in this task. Static production publish/tag/freeze/switch/deploy actions not part of this build scope.

## Actions

- Merged reviewed sourcef42412797e09ee1ea96d1e5ed680fca1d6fcc8dc [MR108](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/108), mergef916ad194649e10b1931d48ff82d8e0a89e19026. Guarded exact source branch/SHA and preserved MR squash/source-removal settings.
- Started user-authorized test5 [dynamic_deploy5823](https://build.youdo.sg/job/dynamic_deploy/5823/), queue19136, requested2026-10-14T21:58:52UTC. Same parameters: monolith139914/staticmetadata139593/master/gitlab; all Restore except B2B, suggestions true, WEB_STATIC/MICROSERVICES false. Parameters match fresh API; receipt ~/ai-data/jenkins-recovery/test5-deploy-retry-buildapi-20261015.json.
- Created project278 CI env variable VK_TEST_NOMAD_TOKEN, maskedtrue/protectedfalse/environment scope*, from existing current/.env key of same name. Value verified in memory by GET, never printed/copied into notes/scripts/logs. Metadata receipt static-vk-variable-receipt.json. Existing inherited old variables untouched.
- Latest release MR3638 titleRelease-2.917/targetproduction/merged; [pipeline139593](https://gitlab.youdo.sg/youdo/youdo.static/-/pipelines/139593), SHA1058542dc2254e0ed717b42b9d50bc6eddc49f5f. Official CI/Dockerfile/Next config at this SHA inspected read-only; no stale test addresses in build path and no static source adaptation required.
- Original prepare-npm artifact expired, other required build artifacts missing. Required rebuild chain prepare-npm then build_ssr then build docker preserves pipeline ID and compound image tag. Original publish/release/production-switch jobs already success, other test-deploy jobs manual/success. Guard prohibits unexpected non-build jobs actively runnable before retry.
- Retried prepare-npm original3183027 to [job3226691](https://gitlab.youdo.sg/youdo/youdo.static/-/jobs/3226691). Success155.3s, artifact333561033bytes. Retried build_ssr to job3226692, success249.6s, artifact582327668bytes. Retried build docker to [job3226693](https://gitlab.youdo.sg/youdo/youdo.static/-/jobs/3226693), success100.8s.

## Helpers and changed files

Local metadata-only helpers merge-approved-mr.py and static-release-build.py in ~/ai-data/jenkins-recovery; nonsecret receipts include static-vk-merge-receipt.json and static-release-build-receipt.json. No youdo.static repository source edit or commit. Automation source already published under prior approval. No extra test pipeline requested/created.

## Findings and limits

Build source unchanged; all three authorized build jobs succeeded. Registry metadata verifies registry.youdo.sg/youdo/youdo.static:master-2.917.139593, digest sha256:a9784d3fb4edff6c6000429af323ef09e7487c1ccb19fd86a901c12a6ea7d663, created2026-10-14T22:14:30.026UTC, size574506704bytes. Updated token is available to later static deploy jobs; no static deploy launched. test5 monolith upload against new BuildAPI passed in5823; Nomad service startup blocked by incompatible MessageBus assembly identities. See [runtime diagnosis](2026-10-15-jenkins-monolith-messagebus-assembly-mismatch.md). Job failures require read-only log diagnosis before scoped corrections.

## Authorized test5 static rollout

User subsequently explicitly requested static deploy on test5 from GitLab CI. Retried prior successful3213500 deploy_yandex_test5/17 in same release139593 to [job3226694](https://gitlab.youdo.sg/youdo/youdo.static/-/jobs/3226694). Build dependencies verified success; no other deployment active. Job clones automation master with merged VK adaptations and reads canonical token; original S3 delivery commands retained. Receipt static-test5-deploy-receipt.json, helper static-test5-deploy.py. Final GitLab statusSUCCESS, duration157.528501s, no failure_reason. Jenkins5823 final FAILURE duration940155ms; BuildAPI upload passed, service startup blocked by assembly mismatch.
