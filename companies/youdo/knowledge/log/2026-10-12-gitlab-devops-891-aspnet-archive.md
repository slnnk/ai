---
system: gitlab
status: verified
checked: 2026-10-12
tags: [base-images, debian, training]
---
# DevOps-891: ASP.NET Debian archive fix

## Task and context

The user assigned image recovery to [DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891/Recovery-Vosstanovit-bazovye-obrazy) and requested an archive fix for Debian ASP.NET images. Scope proposed: failed `microsoft/aspnet/6.0` and `microsoft/dotnet-aspnet/5.0`; affected security package pool URLs are verified available in archive. See [diagnosis](2026-10-12-gitlab-bullseye-archive-nomad-download.md).

## Findings and proposed change

Checkout `/home/slnnk/git/base-images` clean, on `dotnet-10-ports`; origin/master recorded as `a6d14d5`. Minimal fix redirects affected Debian security sources to archive before the first APT update, retaining requested runtime versions. Both security source host variants are redirected to archive before the first APT update; original runtime versions, other sources and newline formats are preserved. Local Docker build commands use task-specific devops-891-aspnet tags and do not push. Both full local builds passed (exit0), archive packages installed successfully. Container runtime smoke checks passed: Microsoft.AspNetCore.App / Microsoft.NETCore.App 6.0.36 and 5.0.17. Diff whitespace check passed with cr-at-eol for the existing CRLF file. Independent review found no material issues. CI template is tag-only, so a normal branch/MR publication does not build/publish images. Existing image tags point at old commits; changing repository files alone does not update their published image contents.

## Training record

2026-10-12, DevOps-891, base-images. Proposed branch `DevOps-891-use-debian-archive` from `origin/master`; source/target proposed branch/master. Stage1 approved by user reply "Да" to branch/scope proposal. Created approved branch from origin/master in the clean existing checkout and edited exactly the two approved Dockerfiles. Committed and pushed only the two task files after Stage2 approval. No pipeline triggers, tags or merge performed. Stage2 publication proposal: commit `use debian archive for aspnet security packages`; MR title `DevOps-891 Use Debian archive for ASP.NET security packages`; source `DevOps-891-use-debian-archive`, target `master`. Stage2 approved by user "Публикуй" for the exact proposed names/scope. Final commit `62226b8a2da26baa8946b1d0ee5e3b6a61210275`, [MR !36](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/36). MR body: one Russian paragraph about redirecting ASP.NET5/6 Debian Security sources to archive.debian.org to restore Bullseye builds, followed only by the DevOps-891 link. Branch publication CI effects: tag-only image build is not triggered. No image tag moves or publication included. No corrections yet.

## Changed files and limits

Two approved Dockerfiles, this work log and shared backlog. Local build logs are under /home/slnnk/ai-data/gitlab-recovery/devops-891-aspnet{5,6}-build.log. Significant previous recovery evidence remains linked; open actions are in `~/ai/TODO.md`.

## Publication result

Staged diff reviewed: exactly two approved Dockerfiles, 6 additions and2 removals, no prestaged changes. Commit and remote SHA match. MR !36 source/target verified, assigned a.solonenko, squash false and source deletion on merge true. Current SHA has no pipelines, consistent with tag-only CI. Checkout is clean. First push was rejected by stale domain SSH host-key entry; successful retry used `core.sshCommand='ssh -o HostKeyAlias=138.16.203.174 -o StrictHostKeyChecking=yes'` against the previously verified trusted key. No known_hosts changes or disabled verification. No user correction or additional publication approval required. Merge and rebuilding release image tags remain separate actions.

## Authorized tag recreation after user merge

The user reported merging MR !36 and explicitly requested recreating necessary tags on master to restart pipelines. GET verified MR merged and master exactly equals merge commit `d673ffaa90197769aec5df1dbdadfefe25fa6732`. Only `microsoft/aspnet/6.0` and `microsoft/dotnet-aspnet/5.0` were deleted/recreated on that SHA; both previously pointed at `958b0802ff7f7ed84124d116e9e73a016e6da33f`, were unprotected and lightweight. GitLab API DELETE/POST performed after authorization; each recreated tag SHA verified. No other tags or branch refs changed.

New pipelines [140613](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140613) (ASP.NET6) and [140614](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140614) (.NET5) are running on the merge SHA. These tag pipelines publish their corresponding versioned images; no +latest alias is requested. Results/digests are not yet verified. Local coordinator entries updated to the new SHA and running pipeline IDs, preserving prior attempts. Tag evidence and execution script are under `/home/slnnk/ai-data/gitlab-recovery/aspnet-tags-*-20261012.json`, `aspnet-tag-pipelines-20261012.json` and `recreate-aspnet-tags-20261012.py`. Local git checkout/tags were not fetched or switched.

## Release result verified

Pipelines140613/140614 succeeded. Authenticated registry digests match each successful build trace: ASP.NET6 `sha256:c87ea4d301fecd7429b31b49cabaa6cedf1ce39dc68e18f304fbfe88846b1992`; ASP.NET5 `sha256:d14d72c3d452ba15cc2a429d99a9c7c3e494ee2b50981f18d713fce90293d13e`. Current inventory47success/8failed/3seeded/1blocked/1excluded. API confirms latest attempts of all eight remaining failed refs still fail. Nomad job3218387 still running at duration886s, external `sysadmins/nomad:latest` still404. Next proposed recovery order: archive sources for Cake, fix Nomad mirror then rebuild its dependent image, resolve remaining download/package/tool pinning and unavailable parents. No new builds or repository edits during this result check.
