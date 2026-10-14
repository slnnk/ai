---
system: nexus
status: verified
checked: 2026-10-14
tags: [nexus, nomad, docker, recovery, runtime]
---
# Nomad cron runtime checks after image recovery

## Summary

A read-only audit at approximately00:40MSK found post-restoration task starts for four production periodic parents: ab-pipeline, cashflow, cashflow-openai and recommended-tasks-generator. Two cashflow tasks completed with exit0; recommended has successful runs and a current running allocation; ab is running. This proves execution state, not exact Docker image identity. Cashflow force_pull=true plus Downloading image events gives strong new-image evidence, but worker SSH authentication was unavailable, so actual image IDs remain unverified. Eighteen other parents have no currently retained detailed children/allocations in the audited response; this does not prove they never ran. The remaining cleaner parent is explicitly excluded from follow-up at the user's request.

## Task and scope

After [artifact recovery](2026-10-13-nexus-pypi-library-batch-recovery.md), the user requested checking whether cron tasks ran using new images. Nomad API GETs covered production, yandex-test and vk-test: production has23periodic parents, the two test clusters have0. No job trigger, deployment, restart, image pull or remote file change was performed.

## Findings

At00:40MSK, ab-pipeline had a running task started00:27:37. Cashflow ran00:01:06–00:02:09 and cashflow-openai00:01:06–00:01:17, both completed exit0. Recommended-tasks-generator had completed00:20 and00:30 runs with exit0 (the latter finished00:37:08), plus a00:40 running allocation. Reported times are October14 Moscow time.

Cashflow parents use force_pull=true and allocation events show Downloading image. Actual image/config identity could not be verified on worker msk3-hdp-worker01/172.24.0.221: the user confirmed its SSH host-key fingerprint, the agent pinned that key only in temporary known_hosts, and root authentication was denied. No permanent known_hosts, host credentials or server access configuration was changed. Ab/recommended references alone do not prove actual image IDs; recommended remains the fixed1.16.24 runtime ref.

Eighteen non-cleaner parents have no currently retained detailed child jobs/allocations in this response. Summary counts retain historical executions, and daily/training pending or negative counts are not proof of a new run or of never running. Many schedules next execute in the morning; schedule checks must be distinguished from retained runtime evidence.

Only nexus-cleaner on172.24.0.12 had an actual Docker image-ID inspection: sha256:284a765e233c30f92b4312c35666f3e9f81271491df4be6df9b73905573887d8 differs from the current registry config sha256:3140e971f90b6ba4a643ca5bae668125b2b7527b2d49d9a38d21312a771e0dae. This demonstrates a cached different image. It restarts with exit1. The user explicitly instructed ignoring cleaner because its Nexus credentials are known bad; no credential investigation, replacement, pull or fix was performed, and no cleaner follow-up is requested.

## Evidence and access limits

Generated, filtered evidence under ~/ai-data/nexus-pypi-recovery/: nomad-cron-runtime-audit.json, nomad-cron-pull-policy-summary.json, nomad-cron-docker-runtime.json and current-config-digests.json. API inventory is checked at2026-10-13T21:40:42Z. Runtime identity verification needs actual Docker .Image matched to registry config, not only matching tags or start dates. GC may remove old allocations/containers; lack of retained detail is not an execution-history assertion.

Nomad token access remains through current/.env variable names only. No credential values, complete task environments or raw application logs were stored. Source, Nomad jobs and host configuration remain unchanged. Completed32PyPI versions,8runtime registry references and all5merged/green master CIs remain artifact/build facts rather than proof that every periodic job executed a restored image.

## Changes and risks

Local changes are this audit note, existing Nexus/GitLab maps, recovery-log reference, live TODO, indexes and sync notes. Remaining runtime identity/retained-run verification is tracked in ~/ai/TODO.md. No agent infrastructure mutation occurred.
