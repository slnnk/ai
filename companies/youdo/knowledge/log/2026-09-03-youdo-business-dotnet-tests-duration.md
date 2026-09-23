---
system: youdo-business
status: verified
checked: 2026-09-03
tags: [gitlab-ci, dotnet-unit-tests, runner-contention, integration-tests, performance]
---
# youdo.business dotnet test duration increase

Last verified: 2026-09-03

## Task

Explain why the `dotnet-unit-tests` job of `youdo.business` became about twice as slow (a 12-minute outlier) compared with a job two weeks earlier.

## Context

Compared GitLab jobs in project `youdo/microservices/youdo.business` (project id 423):

- old: `3078209`, SHA `ac9a6051d32824f88990c1b92c8f44de541df5b2`, 2026-08-20;
- slow new: `3111191`, SHA `d33d57f855c5aedaa561079f6fb12a84a1e7f93c`, 2026-09-03;
- control new: `3110672`, SHA `51f9119911fa17d8642c6859abdf06ebb280f282`, 2026-09-03.

All ran on GitLab runner id 108, `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`, Docker executor, runner version 17.9.3, and the same locally cached .NET SDK image digest.

## Findings

### Timing comparison

| Metric | Job 3078209 | Job 3111191 | Delta |
|---|---:|---:|---:|
| Total job duration | 407 s | 729 s | +322 s |
| Git checkout | 6 s | 13 s | +7 s |
| NuGet restore (`Time Elapsed`) | 72 s | 91 s | +19 s |
| Whole `step_script` | 391 s | 704 s | +313 s |
| Unit tests | 379 / 5 s | 379 / 17 s | +12 s |
| Integration tests | 473 / 179 s | 644 / 346 s | +171 cases / +167 s |

Both jobs missed the `nuget-1-non_protected` cache, so the cache miss is not a new regression.

Between the tested SHAs, the integration suite gained 178 cases and lost 7 (net +171). The test tree changed by about 6,380 inserted lines, including marketplace, beneficiary/document, onboarding, balance-check, and event-processing coverage. Fixtures also gained shared-template database cloning and four `IsolatedAppFixture` users. This is a real secondary increase in test workload and resource demand.

### Primary cause of the 12-minute outlier

Runner contention is the dominant cause, not simply the additional test cases.

During job `3111191` (16:15:36–16:27:46), runner 108 continuously ran two or three other heavyweight `youdo.business` `dotnet-unit-tests` jobs in parallel. Including `3111191`, there were three to four concurrent .NET jobs for essentially the entire run: `3110813`, `3110939`, `3111065`, then `3111317` and `3111443`. The executor name was `...concurrent-3`.

Control job `3110672` ran immediately beforehand on the same runner while effectively alone. It had 636 integration tests (only eight fewer than `3111191`) yet completed in 281 s total; its integration phase took 128 s and unit tests took 5 s. Thus the modern, larger suite can still finish faster than the old comparison job.

JUnit comparison between control `3110672` and slow `3111191` found 635 identical integration test cases. Their cumulative testcase time increased from 1,962.9 s to 6,439.1 s (3.28x). Only eight slow-job-only cases contributed 92.1 s of cumulative testcase time. The broad slowdown across unchanged tests, restore, build, and checkout is characteristic of shared CPU/I/O/PostgreSQL contention.

## Open items

Operational conclusion:

- A rerun during a quiet runner period should be near 4.5–6 minutes rather than 12 minutes.
- For stable latency, reduce concurrency for this heavyweight job on runner 108 or move it to a dedicated runner/tag with explicit CPU/RAM capacity.
- If runner concurrency must remain high, cap xUnit parallelism and benchmark; this may reduce cross-job CPU/DB thrashing but can increase isolated wall time.
- Add timing sections around restore/build/unit/integration commands and retain JUnit artifacts to make future regressions immediately attributable.

## Portable lesson

[`~/ai/general/knowledge/gitlab-ci/slow-job-runner-contention-diagnosis.md`](../../../../general/knowledge/gitlab-ci/slow-job-runner-contention-diagnosis.md)
