---
system: gitlab
status: verified
checked: 2026-10-12
tags: [base-images, recovery, training]
---
# DevOps-891: remaining legacy image recovery

## Summary

The user requested fixes for Cake, Maven, curl, SDK3.1 Mono keyserver, ASP.NET6 legacy diagnostics, Elasticsearch ARM64 and Gradle parents. Six scoped Dockerfile changes are ready on the approved local branch. All seven full local builds passed. Six AMD64 runtime smoke checks and ARM64 architecture verification passed; independent review found no material remaining issues.

## Context and diagnosis

[DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891/Recovery-Vosstanovit-bazovye-obrazy), `/home/slnnk/git/base-images`, origin/master `d673ffaa`. Cake/Maven security packages need archive sources. SDK3.1 HKP keyserver fails; official Mono HTTPS key download was verified with fingerprint `3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF`. Curl floated a Bash parent but requested unavailable historical APK revision. Official curl8.2.1 manifest is available. Elasticsearch private ARM64 parent is missing; official identical-version ARM64 tag responds. Gradle historical alias Dockerfile was absent in master and used nonexistent parent; the working sibling uses official gradle7.5.1-jdk11. Legacy ASP.NET6 master already pins tools and its local build passes; prior failure was an older tag source.

## Actions and validation

Preserved clean existing checkout. Changes: Cake/Maven security-source redirects; SDK3.1 HTTPS key import; official curl8.2.1 parent with Bash/JQ, root/Bash defaults and the original Bash entrypoint copied from a shell stage; official Elasticsearch8.5.2-arm64 parent; restored historical Gradle alias Dockerfile with working parent. Local validation uses `/home/slnnk/ai-data/gitlab-recovery/validate-legacy-images.py` (`--help`, build/smoke, selection and concurrency args), captures separate logs, no registry push. All seven full builds passed. Checks: Maven3.8.6/Java11/JQ/AWS, curl8.2.1/Bash/JQ including legacy -c invocation, SDK3.1.426/native libraries, .NET6 runtime/all five pinned diagnostic tools, Cake .NET6/Node8/Mono/cake command, Gradle7.5.1/Java11. ES image architecture is arm64/linux. ARM64 local builder has no emulation, so ES build/architecture check can run but runtime smoke cannot be claimed.

## Training record

Stage1 proposed/approved branch `DevOps-891-restore-legacy-builds` from origin/master d673ffaa, user answered "Да, создать ветку". Branch created and scoped edits authorized. No commits, pushes, MR or tag writes. Stage2 proposal pending: commit `restore legacy base image builds`; MR `DevOps-891 Restore legacy base image builds`. Tag-only CI will not publish images from branch/MR creation. Required seven tag recreations after merge are separate release actions. Source/target intended branch/master. Previous MR36 is merged and remains historical; this change needs a new MR. Reviewer identified lost curl -c entrypoint behavior; fixed by copying the original Bash entrypoint, rebuilt and verified -c invocation. No user correction. Registry image recovery is still pending release pipelines; local success is not registry publication.

## Changes and risks

This log, six scoped Dockerfiles (one restored), local diagnostic/build artifacts. Legacy ASP.NET6 needs only a separately authorized tag recreation after publication. Other software versions/architectures are retained. No AWX or Nomad edits in this scope. Ongoing open actions are tracked only in `~/ai/TODO.md`.

## Publication and user-authorized release

Stage2 user approved the two repository publication proposals with "Сделай". Staged diff contained only six approved Dockerfiles,19additions/8removals. Commit4b8c5aa8f23857197ab178b46c57baa576ea29ac pushed, [MR37](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/37) created and remote SHA/source/target/settings verified. User then merged MR37 and explicitly authorized recreating required tags. Master equals verified mergeSHA f5f31c2b63a8b0e63da8a83098db2bfd8b5d4bd3. Seven tags deleted/recreated on that SHA, preserving messages, unprotected/lightweight status checked and every new SHA verified. Tag evidence in legacy-tags-before/recreated-20261012.json; pipelines140616–140622 created, initially running/created. Curl, ASP.NET6 legacy and Gradle +latest tags also update image latest aliases. No other tags moved. Coordinator state updated to the new release attempts, retaining prior records. Results/digests pending.

## Final follow-up

Superseded intermediate recovery state: all seven legacy releases and updated Fastlane0.0.9/latest are now verified; see [final release evidence and remaining blockers](2026-10-12-gitlab-devops-891-fastlane-upgrade-legacy-archive.md).
