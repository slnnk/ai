---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [landings, b2b, nginx, gitlab, deployment]
---
# DevOps-898 Landings stand port mismatch and local fix

## Task

Diagnose slow Landings stand deployment in pipeline141017 and prepare the user-approved minimal local fix. User explicitly excluded superpowers skills; acceptance remains GitLab/Nomad status only.

## Context

Project532, source39c1e5fe4977e500b414549e5d27057930b4fca4, actual master-107 (pipeline IID107). Build jobs3230068/build-web and3230069/build-api SUCCESS. User launched ordinary test10–test15 deploy jobs3230082–3230087. This follows merged MR18 for internal Node24 and dependency checksum repair. Previous pipeline141016 was cancelled.

## Actions

Read-only GitLab/Nomad audit at2026-10-15 20:55UTC: jobs3230082–3230087 running inside Ansible task Run nomad task. All6Nomad allocations running, all tasks restarts0, deployment HealthyAllocs0. No placement failure or fatal startup event. Read recent task logs; nginx started normally and API logs recorded scheduler health-check responses200. Read existing service check results for diagnosis only; no direct application HTTP probes were launched. All6API checks passing, all6web checks critical with connection refused where output present. Diagnostic metadata in ~/ai-data/DevOps-898/landings-141017-preflight.json, landings-141017-diagnose.json, landings-141017-task-logs.json and landings-141017-existing-checks.json.

## Findings

Repository devops/nginx.conf listens only on8080. The common automation-test-yandex template playbooks/deploy/docker/files/deploy_microservices/deploy_microservices.j2:174–175 hardcodes web_port container target80. This sends stand health checks and traffic to a closed socket. Deployment waits for healthy allocation until its600second progress deadline. No PostgreSQL/PgBouncer dependency is involved. Setting web_port in devops/config.yml would not help because the common template does not read such an override.

Production devops/production.hcl maps web to8080; devops/dev.yml also uses8080. Add listen80 while retaining listen8080 to support the stand mapping and preserve existing deployment configurations.

## Changes and approval

User explicitly approved branch and local fix. Parent created DevOps-898-fix-landings-stand-port in existing ~/git/youdo.business.landings from origin/master39c1e5fe4977e500b414549e5d27057930b4fca4. Actual diff: one insertion in devops/nginx.conf, listen80; all other configuration preserved. No separate worktree. Peer review verified only this file changed, no staged changes, correct approved branch and no scope issue.

Proposed commit: listen on stand port in landings nginx. Proposed MR: DevOps-898 fix landings nginx stand port. Source DevOps-898-fix-landings-stand-port, target master. User explicitly approved Stage2 publication and separately cancellation of the six pending stand deploy jobs. No merge, new master pipeline or deployment retry authorization inferred.

## Verification

Parent ran git diff --check successfully and a readonly-config nginx1.26.1 syntax check: docker run --rm --entrypoint nginx with the config mounted read-only, -t, exit0; syntaxOK and test successful. Image digest sha256:0f0c707b16468ea9b6cc13a315f29d2c84b0fc53c223ee4b3e8b882506343659. Peer review passed. Stand rollout verification requires a new approved build and deployment after publication/merge.

## Risks

Adds an additional HTTP listen socket within the image; existing8080 remains available. Production/development templates remain unchanged. MR branch pipeline can build changed image; later master pipeline includes existing production/release behavior, which needs explicit user authorization. No service is marked deployed or healthy from local syntax validation.

## Portable lesson

none

## Publication and cancellation (2026-10-16 MSK)

After explicit user approval, parent committed172a557f070a3487e84b5d8898c6da12110b5edc (listen on stand port in landings nginx), pushed the approved branch and created [MR19](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/merge_requests/19), title DevOps-898 fix landings nginx stand port, source DevOps-898-fix-landings-stand-port to master. Existing MR settings preserved. GET verification confirms opened, exact source/target/SHA. Automatic MR pipeline141018/IID108, merge_request_event, refs/merge-requests/19/head, running at verification; no manual pipeline creation.

Parent issued separately user-approved cancellation commands for jobs3230082–3230087. GET verification confirms all6terminal canceled, finished2026-10-16 00:00:49–53MSK. Cancellation does not stop Nomad allocations or repair their port mismatch; no runtime recovery claimed. Metadata artifact ~/ai-data/DevOps-898/landings-build/port-fix-publication-verification.json. Wait for MR review/merge and separate approval for build/deployment as applicable. No merge performed.

## Explicitly approved merge and MR-pipeline stop (2026-10-16 MSK)

User explicitly requested merge and stop of the MR pipeline. Parent canceled pipeline141018 and merged MR19 with project settings preserved; GET confirms MR merged, merge commit0d17499bbc2557e3c15aa5b3e4e5955d9f014fb6, no squash commit. Pipeline141018 terminal canceled, finished00:02:43.734MSK.

GitLab automatically created master push pipeline141019/IID109 on that merge SHA; no manual master pipeline creation was performed. Initial read-only status running, build-web3230136 running, build-api3230137 pending. Expected image tag master-109. Ordinary test10–test15 jobs3230150–3230155 created and not played. Their deployment still requires explicit user approval; no retry authorization inferred from merge. Evidence ~/ai-data/DevOps-898/landings-build/port-fix-merge-verification.json.

## Approved stand rollout accepted (2026-10-16 MSK)

User separately approved ordinary six-stand deployment from pipeline141019. Jobs3230150–3230155 allSUCCESS; read-only GitLab/Nomad verification00:08:46MSK confirms all6master-109running/healthy/restarts0. [Final rollout evidence](2026-10-16-nomad-test-devops-898-landings-b2b-rollout.md). Parent master pipeline still running for independent production/release work.
