---
system: nexus
status: verified
checked: 2026-10-13
tags: [nexus, pypi, python, gitlab, recovery]
---
# PyPI basis 10.0.2 recovery execution

## Summary

`youdo-basis==10.0.2` is published to restored `pypi-private`. Both wheel and source archive SHA256 exactly match existing consumer locks; independent Nexus component metadata verifies both without downloading packages. No source or lockfile change was needed. Extraform release-source image was locally built and approved runtime tag `0-31-17` published with independently verified manifest/config digests. No deployment or Nomad periodic job was launched.

## Task and context

After Nexus stage 1, the user said "Начинай" and then "Если есть проблема давай локально" to proceed with library recovery and local fallback. Extraform release `0.31.17` needs the exact locked distribution of `youdo-basis==10.0.2`. Source tag SHA is `0fa692f2624270e69f489a1ad2b065f5ca721dae`. Existing release CI metadata has no original distribution artifacts and its trace is zero bytes; named local cache searches found none. This does not exclude external backups.

## Approvals and actions

Read-only SSH checks on runners `172.28.0.171`/`.172` resolved `pypi.youdo.local` to `10.18.24.233` and returned indexHTTP200. No Docker DNS override was present in their configuration. These are host checks, not a claim about every running container's DNS.

Approved retry of original publish2254150 created3222818. Project207 instance/shared runners were disabled with no eligible runners. Approved project PUT enabled shared runners; independent GET returned enabled state and nine runners. The retried job remained pending. Database inspection found `Ci::PendingBuild` with instance enabled/protected true and tags `[18]`; this disproved the proposed stale queue-flag hypothesis. Runner services were active and idle, polling returned204; the actual scheduling cause remains undetermined. The user's local fallback steering covered canceling the pending retry: cancellation returned201 and GET verified canceled status.

Built an unchanged GitLab source archive for basis10.0.2 using uv0.5.29/Python3.12. Current hatchling1.32.4 produced a different wheel hash (prefix `7aa060`), so publication was held. Official PyPI release metadata before the original February10,2025 release identified hatchling1.27.0 and uv-dynamic-versioning0.5.0. Pinning those two build tools and building with `--no-build-isolation` reproduced both exact locked distributions. No dependency/source/lock changes were made.

Approved local publication used actual inherited CI `PYPI_REPOSITORY=http://msk3-nexus.youdo.corp/repository/pypi-private/`, user `pypi` and existing `PYPI_PASSWORD` accessed only in process memory. Nexus component GET returned one component with both assets and exact expected SHA256 values; packages were not downloaded for verification.

## Findings and evidence

- Wheel SHA256: `aef135fb0571bd33ce0a042f137760b6a266e02405794d8cba99f756ebe854f7`.
- Source archive SHA256: `a205adc769bf1772d6c14fd6b1280fbcc9a75849338147235f21b5dd6232cd18`.
- Generated evidence in `~/ai-data/nexus-pypi-recovery/`: `basis-10.0.2-local/published-manifest.json`, `basis-10.0.2-local/historical-tools-manifest.json`, `basis-10.0.2-nexus-verification.json`, `runner-host-pypi-verification.json` and `publication-plan.json` (32 exact-version references). Artifact names should be read from the directory if generated filenames change.

## Extraform local release image verified

The first local attempt from the release archive completed frozen uv dependency synchronization and installed restored basis, then failed because archive source lacked Git metadata. The approved temporary checkout in existing clean `/home/slnnk/git/extraform` built tag `0.31.17`, actual SHA `3c04a38b`, with unchanged Dockerfile and `uv.lock`. The original branch `Site-24662_appmetrica_installs`, SHA `b550dd2f81f95692111b706238daff38b9f3078e`, was restored and a clean working tree confirmed.

Local image `extraform-recovery:0.31.17` built successfully: ID `sha256:bc896c9fec1ad1be9fecd87fa146b0afaa0898620e92f40579ac3d525fcd5ee2`, size629104411 bytes. Runtime metadata smoke check found Python3.12.15, basis10.0.2, Luigi3.6.0 and dynamic extraform distribution version `0.0.0.post368.dev0+3c04a38`; do not equate that generated package metadata with Git release tag `0.31.17`. Source and runtime image contract use the release Git SHA. Evidence: `~/ai-data/nexus-pypi-recovery/extraform-0.31.17-local/manifest.json`, including original branch restoration and lock hash.

Nomad runtime requires `registry.youdo.sg/data/extraform:0-31-17`. After verifying that target tag was absent and obtaining approval, the exact release-source image was pushed and independently verified by `docker manifest inspect`: manifest digest `sha256:9795ee9a5049059ba46479e0a881713cbe8db90a64a6de0040b05e0cba2b9bab`; config digest matches local image ID `sha256:bc896c9fec1ad1be9fecd87fa146b0afaa0898620e92f40579ac3d525fcd5ee2`. Evidence: `extraform-0.31.17-local/registry-verification.json` and `extraform-0.31.17-local/published-manifest.json`. Dotted `0.31.17` and `latest` tags are unnecessary for the observed contract. Four release-source Nomad periodic files are appmetrica-installs/appmetrica/eventum/yametrica at3:00/3:00/4:00/12:00. This source inventory is not a live deployed Nomad job inventory. No deployment or periodic execution was authorized or performed.

## Changes and limits

Remote changes: project207 shared runners enabled, publish retry created then canceled, exact basis distributions published to Nexus, approved extraform runtime image tag `0-31-17` published to GitLab registry. Local files: generated recovery evidence/helper artifacts, this log, existing Nexus/GitLab maps, plan, repos registry, TODO, portable recipe and sync notes. No repository application source/lock edit, commit, deployment or periodic job execution was performed. Local helpers fetched release archive/source metadata and temporarily checked out the approved existing clean repository release, preserving and restoring the original branch. The other31canonical required library versions across the nine publisher projects, undetermined CI queue cause and real Nomad deployed refs beyond the four source jobs remain tracked in `~/ai/TODO.md`.

Matching both hashes proves byte identity for these assets, not every dependency or service build. Two historical top-level build pins sufficed in this case; other packages may need full transitive build-tool constraints, original interpreters/platforms, Git metadata or original artifacts. Runner scheduling cause remains undetermined.

## Portable lesson

[Recover exact locked Python distribution hashes](../../../../general/knowledge/python/reproducible-wheel-recovery.md).
