---
system: gitlab
status: verified
checked: 2026-10-12
tags: [gitlab, registry, recovery, base-images]
---
# Base images: five selected recovery builds

## Summary

Five requested builds completed: two succeeded and their registry digests match the build traces; three failed with Debian Bullseye security package HTTP 404s. No builds remain active. Current per-tag inventory: 45 successful, 10 failed, 3 seeded, 1 blocked and 1 excluded.

## Task and authorization

The user requested "Выполни 1 и 2 пункты": build the previously blocked ASP.NET 8 LibreOffice child and retry four Debian timeout failures. This explicitly authorized five existing-tag pipeline creations and resulting image publications; no repository changes or unrelated retries.

## Actions

Reconciled the successful user ASP.NET 8 retry into the local coordinator state, preserving its prior state in `rebuild-state-before-retry-20261012.json`. Reset only the five selected entries, retaining prior attempts. Ran `python3 /home/slnnk/ai-data/gitlab-recovery/retry-selected-20261012.py` with concurrency 4; tag SHA checks precede each launch. Read-only final API and registry checks confirmed all statuses and compared each successful digest with its trace.

## Findings

| Tag | Pipeline | Status |
| --- | --- | --- |
| `microsoft/dotnet-aspnet/6.0` | [140608](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140608) | success |
| `microsoft/aspnet/6.0` | [140609](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140609) | failed |
| `microsoft/aspnet/8.0-libreoffice` | [140610](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140610) | success |
| `microsoft/dotnet-aspnet/5.0` | [140611](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140611) | failed |
| `microsoft/dotnet-sdk/6.0-nodejs-cake` | [140612](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140612) | failed |

Successful publication digests:

- `microsoft/dotnet-aspnet/6.0`: `sha256:7683f60c5751c64a6253a9a9a9d42d2558d3bd799034c2411f3a218aab54c34e`; registry matches trace.
- `microsoft/aspnet/8.0-libreoffice`: `sha256:3d339b31972e9f392cd80ddfa8decc4580b62a187d4e37601127e12a708c6c9f`; registry matches trace.

The three failed jobs reached Debian HTTP endpoints but received 404 for Bullseye security packages: fonts dependencies in ASP.NET 6, curl/CA/DNS dependencies in dotnet-aspnet 5, and gnupg dependencies in SDK Cake. The first and third used endpoint `10.255.0.50`; dotnet-aspnet 5 failed at `security.debian.org` (`151.101.2.132`). The prior timeout is not the failure observed in these retries. Stale indexes or repository/proxy inconsistency remain hypotheses; the exact source has not been isolated. Further retries without diagnosis are not justified by these results.

## Changed files and limits

Local recovery state, backup, selected-run wrapper and `selected-retry-results-20261012.json`; this log, existing GitLab system map and shared TODO. No repository edits, commits, deployments or unrelated builds. Historical CSV/global verification still describe the earlier batch; fresh evidence for these five builds is in the selected results JSON. Remaining recovery actions are tracked in `~/ai/TODO.md`.
