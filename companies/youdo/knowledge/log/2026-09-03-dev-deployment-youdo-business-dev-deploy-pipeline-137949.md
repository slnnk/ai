---
system: dev-deployment
status: verified
checked: 2026-09-03
tags: [youdo-business, pipeline-137949, build-148, employee-web, staging, mr-3567, dev-devops-689]
---
# youdo.business dev deployment verification: pipeline 137949

Date: 2026-09-03  
Project: `youdo/microservices/youdo.business` (GitLab project 423)  
Repository: `/home/slnnk/git/youdo.business`  
Environment: ephemeral Kubernetes namespace for `DevOps-689`, GitLab environment `dev/devops-689-k8s`

## Findings

MR 3567 pipeline [137949](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/pipelines/137949) completed successfully at commit `1d3ebc0c8aecd6bc6d7ad6d0764ae1608baee5cf` (`fix tests timezone`). The pipeline contained 12 successful jobs and 117 manual deploy-test/autotest jobs.

The `1 deploy dev` job [3111628](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3111628) triggered Jenkins build [148](https://build.youdo.sg/job/test/148/). Jenkins returned `SUCCESS`, and the GitLab job refreshed environment `dev/devops-689-k8s` and uploaded `environment-description.md` plus `deploy-dev.env`.

The operator reported the fresh deployment as good. An independent public check after the job returned:

- `https://employee-devops-689.dev.youdo.sg/` — HTTP 200;
- `https://employee-devops-689.dev.youdo.sg/health` — HTTP 200.

This closes the earlier employee-web HTTP 500 runtime gap. The fix was introduced by commit `a067c985165ce3d1268ce85c7e663a0a76c4509b`, which changed the shared `devops/dev.yml` environment identity from `Development` to `Staging`; the active Nomad test configuration already used `Staging`.

## Open items

- Merge MR 3567 so `devops/dev.yml` and the shared dev-deploy include are available from `master`.
- Treat post-deploy autotests as a separate workstream: all deploy-test/autotest jobs in this pipeline remained manual, so pipeline success does not validate the proposed automatic post-deploy test contract.
- Continue platform hardening from `~/ai/current/knowledge/systems/dev-deployment/overview.md`: namespace-level Jenkins locking, automatic HTTP smoke, chart validation, cleanup/TTL ownership, and operationalization of the pilot Jenkins job.

No secret values were recorded.

## Portable lesson

none
