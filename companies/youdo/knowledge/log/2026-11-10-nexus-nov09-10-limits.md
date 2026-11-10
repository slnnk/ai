---
system: nexus
status: verified
checked: 2026-11-10
tags: [usage, limits, read-only]
---
# DevOps-904: Nexus limits on November 9 and 10

## Task

Read-only check of Nexus limits for DevOps-904 on November 9 and 10, Moscow time.

## Context

[Nexus map](../systems/nexus.md); existing DevOps-904 remediation and seven-day verification remain open in `~/ai/TODO.md`. Previously verified limits: 100,000 repository requests per rolling 24 hours and 40,000 components.

## Actions

Reused the November 4 aggregation method, adapted to two days. Read retained request logs over SSH, including November 8 for complete preceding windows; authenticated GET of metrics, usage-history and monthly-metrics. No external writes, CI runs or configuration changes. Local scripts and evidence: `/home/slnnk/ai-data/nexus-usage/nov10_remote.py`, `nov10-logs.json`, `nov10_api.py`, `nov10-api.json`.

## Findings

Snapshot: 2026-11-10 15:26:23 Moscow. Counted all methods/statuses under `/repository/`; sorted timestamps, exact trailing 86,400-second windows, including midnight boundaries. Four log files scanned; zero parse failures.

| Moscow date | Calendar requests | Maximum rolling 24h | Peak time Moscow | Limit usage |
| --- | ---: | ---: | --- | ---: |
| 2026-11-09, complete | 57,098 | 57,098 | 23:58:12 | 57.098% |
| 2026-11-10, through 15:26:23 | 44,463 | 80,039 | 13:49:20 | 80.039% |

No rolling request-limit exceedance in either observed interval. Current rolling count: 75,861 (75.861%), leaving 24,139 requests. Today's peak leaves 19,961 requests; it slightly exceeds the provisional 80,000 headroom goal, which is not the product limit.

Largest calendar request categories: November 9 NuGet 24,363, Docker 16,740, npm 9,885; November 10 NuGet 23,083, Docker 14,168, npm 5,880. Categories combine group/hosted endpoints with matching format; raw and Maven are separate. These are protocol counts, not job attribution or causal proof of savings.

API reports component_total_count 13,647; component_history day/month high-water value 13,859 (34.6475% of 40,000). Retained hourly history is not timestamp-labelled, so no precise November 9 component peak is inferred. Both throttled_requests and grace_throttled_requests gauges are zero at the snapshot; this is not proof of no historical throttling. API sampled rolling request value 79,076 differs from exact log-snapshot 75,861; API content_request_count day is 57,097 versus log calendar 57,098. API aggregates are sampled/asynchronous; exact log calculation is used for the table, with the one-request calendar discrepancy preserved. No stronger reconciliation was performed.

## Changes

Local evidence, this note and a dated section in the existing Nexus map only.

## Status and risks

Check complete; SSH and API commands both exited zero; no background operations remain. Today is incomplete. Two observed days do not satisfy the existing seven-complete-day verification requirement or establish sustained busy-day compliance. DevOps-904 stays open; existing central TODO already tracks remaining remediation/measurement, so no duplicate task added. Tracker was not modified.

## Portable lesson

none

## Follow-up: rolling-window sources and GitLab jobs

User requested why the rolling count is high and which GitLab job produces it. Analyzed the exact previously reported window, November9 15:26:23.453404 through November10 15:26:23.453404 Moscow, rather than moving the comparison endpoint. All75,861requests reconcile; zero parse failures. GitLab runner inventory returned10runners/824overlapping jobs without errors; read306Business/monolith traces without errors or truncation. All commands exited0; no background work remains. Read-only use of `gitlab-workflow`; no CI or external state modified.

Evidence directory: `/home/slnnk/ai-data/nexus-usage/nov10-attribution/`; `nexus.json`, `runner-jobs.json`, `trace-sources.json`, `summary.json`, `local-revision-checks.json` and collection scripts. Existing company scripts directory had no Nexus usage collector; adapted prior diagnostic collectors. Local Business checkout `05580fcf342639830a957c182a461776ee0ddfdd` and monolith checkout `abc9c7ae1a5cc65509065be344abf20cb74a6810` inspected without fetch or edits. Business sample job101ea5da is not available locally, so local CI is contextual rather than proof of that exact job revision; traces provide actual execution evidence.

| Repository category | Requests | Share |
| --- | ---: | ---: |
| NuGet, including private | 36,293 | 47.84% |
| Docker, group and hosted | 25,582 | 33.72% |
| npm, public and private | 9,682 | 12.76% |
| Maven | 2,384 | 3.14% |
| raw | 1,920 | 2.53% |

These categories are disjoint. Workload checks are a subset of NuGet, not an additional category:28,680requests (37.81%of all requests), including27,287from `NuGet Client V3/6.11.2`. Repeated workload registration lookups include iOS, Android, MAUI, MacCatalyst and other SDK manifests; these are background SDK update checks, not ordinary application package downloads. Previous remediation identified the same mechanism. Counts include404and authentication responses, which still consume requests.

Business has30overlapping runs each of seven build job names,29each for mock-api/employee-web, and28dotnet-unit-tests (268build jobs across nine names, plus tests). This includes jobs starting before the window or finishing after it; do not claim all completed within the window. Its image paths account for16,476Docker requests (21.72%of the global total,64.40%of Docker traffic). Image paths identify ownership, not the particular pushing/pulling/cleanup process. Business build/test activity overlaps26,117of27,287SDK6.11workload requests;1,170occur outside those jobs. This is temporal association, not exact assignment. Traces show SDK8test jobs, successful cache extraction for28/28unit-test jobs, and cached backend Docker layers/mounts. Package-cache success does not suppress background SDK workload update requests. Several simultaneous identical clients behind the shared proxy prevent assigning all28,680workload requests to one job or exclusively to Business. The workload source and Business image traffic explain the high aggregate, but do not establish one dominant individual GitLab job.

Monolith legacy npm/NuGet clients can be isolated by non-overlapping job windows and distinct agents. Four successful `build` jobs account for12,467requests (16.43%of all requests); one fifth build failed before producing these requests:

| Job | Ref | npm | NuGet | Total |
| --- | --- | ---: | ---: | ---: |
| [3284382](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3284382) | refs/merge-requests/10112/head | 2,833 | 1,705 | 4,538 |
| [3286714](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3286714) | refs/merge-requests/10139/head | 924 | 1,745 | 2,669 |
| [3285345](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3285345) | refs/merge-requests/10138/head | 924 | 1,705 | 2,629 |
| [3287082](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3287082) | refs/merge-requests/10139/head | 924 | 1,707 | 2,631 |

Job3284382is the largest individually isolated job in this checked subset, not a proven global maximum across824jobs. Its exact source SHA051441ece54dbb16ef3faa7c7b2776aea68f9612is present locally: all three npm cache markers absent; trace restores NuGet cache only. Patched3285345SHA d8ff5d5c631f26b8a473b1d3138162fae3e1e0edhas all three markers and restores both caches. Difference in npm traffic2,833vs924is1,909requests, consistent with the previous warm-cache result. Previously diverged MR10112still lacks the merged optimization; no patch propagation performed.

Remaining workload-advertising remediation, missing-monolith-patch propagation and sustained verification are already tracked under DevOps-904 in central TODO; no duplicate backlog added and no implementation authorized by this diagnosis. Other unrelated project jobs were not investigated beyond listing temporal candidates.
