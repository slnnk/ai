---
system: base-images
status: verified
checked: 2026-10-20
tags: [dotnet, docker, gitlab, DevOps-899]
---
# Digest-pinned .NET 2.1 SDK and ASP.NET runtime mirrors

## Summary

Two original .NET2.1 base-image mirrors prepared, locally built/runtime checked, published as reviewed Dockerfiles and merged. Approved release tags launched publication pipelines140998/140999; both registry mirrors published and verified against local image config digests. Cerberus consumer CI was deferred on October15; user resumed it on October20. The approved two-line consumer patch is published as Cerberus MR27 under DevOps-902; MR27 merged and release1.0.10 deployed by user; release CI141231 succeeded. Production HTTP check failed; see October20 verification below.

## Task and scope approvals

User initially deferred SDK mirror, then resumed with all Cerberus external images, then narrowed to .NET only. Final scope SDK2.1 and ASP.NET2.1; Pyrra/release-cli deferred. Approved existing proposed branch DevOps-899-mirror-cerberus-dependencies from masterdfb2909 with only two Dockerfiles. User explicitly approved commit/MR publication, merge and both tags. Temporary Stop honored; resumed only base-images and Ansible, consumer CI deferred.

## Sources and targets

| Source | Linux/amd64 manifest digest | Target |
|---|---|---|
| mcr.microsoft.com/dotnet/sdk:2.1 | sha256:ae4daaaab45c6c6b0d2e36d93d8eed8ab255bdab9df02f08f3c39ba90ceb22a9 | registry.youdo.sg/youdo/base-images/microsoft/dotnet-sdk:2.1 |
| mcr.microsoft.com/dotnet/aspnet:2.1 | sha256:80ddf066edeeb7e489b23c3c90d8e5dd741037d4a4875150c1dec777fd24cc76 | registry.youdo.sg/youdo/base-images/microsoft/dotnet-aspnet:2.1 |

## Changes and checks

Only microsoft/dotnet-sdk/2.1/Dockerfile and microsoft/dotnet-aspnet/2.1/Dockerfile added, one FROM tag@digest line each. Local docker build --platform linux/amd64 passed for both. `docker run --rm --network none --entrypoint dotnet ... --info` SDK2.1.818/runtime2.1.30 passed; runtime --list-runtimes reports Microsoft.NETCore.App/Microsoft.AspNetCore.App/Microsoft.AspNetCore.All2.1.30. Actual staged diff2files/+2 reviewed, diff-check clean, no other staged paths. No added packages or runtime behavior changes.

## Publication

Commit208da11bf6fba54d695d1f865ff64b29307ae0a8, message mirror dotnet 2.1 images. [MR42](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/42), title DevOps-899 mirror dotnet 2.1 images, approved Russian paragraph plus DevOps-899 link only, current user184 assignee, squashfalse/remove-source true retained. Remote diff exact two paths verified. Merged into masterab4e5860c82285895f4432188d9d55f43e330622. Created approved tags microsoft/dotnet-sdk/2.1 and microsoft/dotnet-aspnet/2.1 at that merge SHA, started pipelines140998(build3229538) and140999(build3229539).

Local safe operational receipts: ai-data/jenkins-recovery/publication899-base-images.json, dotnet21-baseimage-tags899.json, dotnet21-baseimage-pipelines899.json. Watcher watch-dotnet21-baseimages899.py [--once]. No direct Docker registry push; publication via standard tag pipelines.

## Limits

Only Linux/amd64 mirrored; original upstream multiarchitecture list not copied. Cerberus DOTNET image refs still MCR by explicit user deferral. Other external helper images from live templates: ghcr.io/pyrra-dev/pyrra:v0.7.3 and registry.gitlab.com/gitlab-org/release-cli:v0.18.0, not changed.

## Direct publication explicitly approved

Tag pipelines stalled over14minutes at BuildKit bootstrap pulling external moby/buildkit:buildx-stable-1, before .NET Dockerfile steps. User explicitly approved direct docker push of both locally checked images, followed by canceling those two jobs if still active. Both pushes completed. Registry manifest config digests match local checked images: SDK854834983dba5b1103776b08fe8beb17a50431d5bcdad1b1e9c3cc673a1a800b (7layers), runtime34185b94ec9a7d5648b8adfe0f2be0e167d377e8f40721269c6b367c89b9bea8 (4layers). SDK registry manifestsha256:a57976f2f7f813fd979a3d485d17e31defa747ed77d3982ef80d5555dd3c8682; runtime228baf7b9e2eb7597987c6182dbf9ba5c231a17b92147c13b2fab5529c514ddf. Verification receipt dotnet21-registry-verification899.json. RuntimeCIjob independently reached success954.23s before cancel request; do not cancel completed successful job. Consumer CI image refs remain deferred.

## Final publication outcome

SDKjob3229538 canceled (duration1146.50s), as explicitly authorized. Runtimejob3229539 already succeeded954.23s, left successful. Cancellation scope guarded by current job status. Both registry tags verified after direct push; manual SDK publication supersedes canceled tag pipeline140998, runtime pipeline140999 success. Git recipes/MR42/tags retained for future standard rebuilds. No consumer Cerberus image refs changed; separate user-deferred task.

## Consumer CI resumed 2026-10-20

User requested implementation and explicitly approved the proposed repository `/home/slnnk/git/cerberus2`, new branch `DevOps-899-use-internal-dotnet21-images`, and base `origin/master` at `9f1c54f`. Original and final names match. Fresh fetch confirmed the base; checkout was clean. Created that branch without changing local master. Only `.gitlab-ci.yml` changed: SDK and ASP.NET image paths now point to the two internal mirrors above; tags remain `2.1`.

Checks: `git diff --check` passed; GitLab CI Lint with current remote includes returned valid with no errors/warnings. A dry-run on master returned an empty pipeline, consistent with MR/semantic-version-tag rules and manual production mode. Registry API GET verified both tags and their previously recorded digests. Current merged CI rules show MR builds and manual stand deployment; production, release and monitoring jobs require production rules and do not run on this branch/MR. MR builds publish API, worker and migrations images to the existing project registry. No deployment or release tag is proposed. No application build has run yet.

Prepared publication: commit `use internal dotnet 2.1 images`; MR title `DevOps-899 use internal dotnet 2.1 images`; source approved branch, target `master`, ready MR with squash off and source deletion on merge. Russian body explains the two internal image references and retains the DevOps-899 task link. Proposal, CI summary, registry verification and snapshot live under `~/ai-data/gitlab-workflow/cerberus-dotnet21/cerberus2/`. Publication approval is pending; no staging, commit, push or MR creation performed. The open central task was moved from the unrelated corporate-network/Featuretoggle headings to `YouDo` / `base-images / Cerberus2`; the historical deferral is preserved and superseded by this resumption. [Central backlog](../../../../TODO.md).


## Consumer MR publication under DevOps-902

User supplied the separate tracker task `DevOps-902` and explicitly approved renaming and the full commit/push/MR sequence, including three test-image builds. Original proposed source/title used DevOps-899; final source is `DevOps-902-use-internal-dotnet21-images`, title `DevOps-902 use internal dotnet 2.1 images`, target `master`, body links DevOps-902. The original snapshot matched before the authorized rename; updated proposal/body/snapshot were recorded as `proposal902.json`, `body902.txt`, `snapshot902.json`. The new snapshot matched immediately before staging. The full staged diff was exactly the approved two-line patch; whitespace check passed. Commit `da06848553e26d0c08e59bf1763018c2bba9ac2a` (`use internal dotnet 2.1 images`) was reviewed against the patch and pushed successfully.

[MR27](https://gitlab.youdo.sg/youdo/cerberus2/-/merge_requests/27) created and verified: source/target, branch and MR SHA, exact title/body match; assigned to current user, ready, squash false, remove-source-branch true. Initial pipeline list empty; follow-up state recorded below. Sandbox DNS failures prevented the initial push and MR lookup; network-enabled retry succeeded. Read-only inspection confirmed no existing MR before the create retry. No merge, tag or deployment performed. Previous publication-pending paragraphs above describe the earlier stage and are superseded by this outcome. The central backlog remains open for CI and merge.

Follow-up verification: pipeline141230 running; MR exact fields verified again.

Final CI verification: pipeline141230 SUCCESS. Jobs set-variables3236401, prepare-nuget3236402, build-api3236403, build-worker3236404 and build-migrations3236405 all SUCCESS. Both SDK restore and three Docker builds succeeded using the internal image configuration. Merge remains unperformed and needs explicit approval; no tag or deployment was triggered.


## User release and production check 2026-10-20

User completed merge, tag and test/production deployment. Read-only verification confirmed MR27 merged as b87d8268, tag1.0.10, pipeline141231 SUCCESS including all14test deploys and production sequence. This supersedes earlier pending-merge status. Internal-image switching is complete. Production Nomad healthy/zero restarts and all3Orleans silos started, but API HTTP probes time out even inside container localhost80. No production acceptance or causal attribution to the image switch claimed; no repair performed. [Production evidence and limits](2026-10-20-cerberus2-devops-902-production-verification.md). The HTTP failure is tracked separately in central TODO.

Production follow-up: the user API restart at01:04:45 restored GET `/v1/sources` HTTP200/~0.17s and ordinary404 routing; old859threads/new69. Root cause remains unproven, see production verification note. This supersedes the current-failure wording in prior snapshots without claiming a code fix.
