---
system: nexus
status: verified
checked: 2026-11-25
tags: [usage, limits, read-only]
---
# DevOps-904: Nexus requests from November 16 to 25

## Task

Analyze Nexus requests from November 16 for [DevOps-904](https://youtrack.youdo.com/issue/DevOps-904).

## Context and method

Moscow time. The report includes nine complete days and the November 25 snapshot through 02:00:30. Counted all methods and statuses under `/repository/*` in 12 retained log files, with November 15 included for leading rolling windows. Computed trailing 86,400-second maxima over all request and midnight boundaries. Zero parser failures. Reconciled daily totals with protocol and status counts, and peak total with its protocol breakdown. Used authenticated read-only Nexus API requests and GitLab job metadata and traces. SSH host verification used the already trusted IP entry for 10.18.24.233 because the DNS alias still has an older local entry. No external writes or CI runs.

## Calendar totals and rolling maxima

| Date (November) | Calendar requests | Peak rolling 24h | Peak ends (MSK) |
| --- | ---: | ---: | --- |
| 16 | 48,267 | 48,267 | 23:55:37 |
| 17 | 45,456 | 55,697 | 12:25:40 |
| 18 | 48,998 | 51,511 | 21:44:04 |
| 19 | 49,494 | 56,816 | 15:35:05 |
| 20 | 41,280 | 65,109 | 12:41:56 |
| 21 | 3,230 | 42,390 | 10:06:52 |
| 22 | 1,313 | 3,230 | 00:00:00 |
| 23 | 49,100 | 49,101 | 23:26:41 |
| 24 | 52,623 | 57,158 | 20:28:32 |
| 25 (through 02:00:30) | 41 | 52,623 | 00:01:19 |

November 16–22 totals 238,038 requests versus 374,822 for October 28–November 3 in the [prior weekly check](2026-11-04-nexus-weekly-limits.md). The rolling maximum fell from 105,806 to 65,109 (38.5%), with 34,891 requests of headroom against 100,000. The provisional 80,000 target held throughout this observed period. Traffic and source mix differ between the windows, so the full change cannot be attributed to cache patches. November 18 had a [client-side VPN outage](2026-11-18-corporate-network-vk-ipsec-transient-outage.md); incoming logs measure requests that reached Nexus.

At the snapshot the exact trailing count was 49,433. Nexus API sampled 50,792 for the trailing window and returned seven history values all labelled November 24, so the API was not used to derive daily peaks. The API reported 14,802 current components and a November monthly high water of 15,078 against 40,000. Throttling and blocked-request gauges were zero at the API snapshot. No HTTP 402, 429 or 5xx appears in retained request logs for the interval.

## Sources and peak attribution

Of 339,802 total logged repository requests, NuGet accounted for 174,026 (51.2%), Docker 111,739 (32.9%), npm 36,791 (10.8%), Maven 11,012, raw 4,328 and PyPI 1,906. Background .NET workload manifest checks accounted for 102,065 requests (30.0% of all traffic and 58.6% of NuGet); 69,901 were from NuGet Client V3/6.11.2 and 20,972 from 6.3.4. Docker recorded 49,905 successful blob HEADs and 24,519 successful blob GETs. Nine Business image paths summed to 46,354 requests across this period and 8,737 in the peak. Image paths identify the image scope; caller identity remains limited by the shared gateway.

At the peak, the disjoint breakdown was NuGet 37,766 (including 17,511 workload checks), Docker 16,767, npm 8,514, Maven 1,758, PyPI 178 and raw 126. On 10 GitLab runners, 725 jobs overlapped the peak window, with no runner errors or skips. All 28 sampled job traces loaded without errors or truncation.

- Nine monolith jobs restored npm and NuGet GitLab caches on runners 105 and 106. Their windows contain all 8,316 legacy npm requests (all tarballs) and 15,411 legacy NuGet requests in the peak (36.4% combined). Seven jobs had 924 npm requests each in non-overlapping request windows. Two concurrent jobs had 1,848 combined. Examples are [3309169](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3309169) with 924 npm and 1,662 NuGet, and the overlapping [3312168](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3312168) and [3312173](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3312173).
- 12,220 of 13,104 peak workload requests from 6.11.2 overlapped 175 Business build/test job windows; for 6.3.4, only 592 of 3,728 overlapped. Timing is evidence of possible linkage, with multiple identical clients behind the shared gateway.
- Seven of seven sampled Android feature/BrowserStack jobs extracted the shared Gradle cache on runner 116. Nine of nine Business gates extracted their separate npm caches on runner 108. Two of two frontend-tools preparers restored npm caches on runners 105 and 106 in different protected/non-protected cache partitions. Exact package-level Nexus savings for these three groups were not measured in this sample. The most common Maven agent was Gradle 8.7 with 7,607 requests for the period; exact job attribution remains unverified.

## Status and risks

The observed rolling-limit measurement in DevOps-904 step 6 is complete for November 16–24, including busy CI days. Cold/warm and cross-runner attribution limits and the tracked remediation stay open. No CI, infrastructure or tracker changes. SSH, the Nexus API request, GitLab job inventory and trace collection completed. No background operations remain.

Local evidence under `~/ai-data/nexus-usage/nov16-25/` uses 584 KiB. Retained aggregate counts, bounded trace evidence and compact job metadata support later audit of the observed peak and cache behavior. No full request logs or full job traces were retained.

## Portable lesson

None.

## Task metrics: devops-904-requests-nov16-25

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "devops-904-requests-nov16-25",
  "created": "2026-11-25T02:03:32.275913+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "operational-analysis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Retained request logs, API snapshot and peak job trace evidence summarized in this note",
  "updated": "2026-11-25T02:03:32.275978+03:00"
}
```
