---
system: base-images
status: verified
checked: 2026-10-15
tags: [dotnet, docker, gitlab, DevOps-899]
---
# Digest-pinned .NET 2.1 SDK and ASP.NET runtime mirrors

## Summary

Two original .NET2.1 base-image mirrors prepared, locally built/runtime checked, published as reviewed Dockerfiles and merged. Approved release tags launched publication pipelines140998/140999; both registry mirrors now published and verified against local image config digests. Cerberus consumer CI changes explicitly deferred.

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
