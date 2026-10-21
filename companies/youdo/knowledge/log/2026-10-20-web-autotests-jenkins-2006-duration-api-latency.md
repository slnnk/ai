---
system: web-autotests
status: verified
checked: 2026-10-20
tags: [jenkins, selenium, performance, api]
---
# Jenkins 2006 duration dominated by stand API latency

## Task and context

Explain4h27m for Jenkins web two/2006 compared with roughly1.5h before migration. Read-only analysis of saved console, report,60random successful-test logs and10longest logs. Compared3same-name tests with two/1978 (Selenoid/test7) and three/1622 (Yandex Kubernetes deployment/test1). Historical systems and stands differ; this is observed latency comparison, not a controlled migration experiment.

Sources: [2006 report](https://build.youdo.sg/job/youdo_web_testing_two/2006/artifact/uitests/report/report.html), [1978 report](https://build.youdo.sg/job/youdo_web_testing_two/1978/artifact/uitests/report/report.html), [1622 report](https://build.youdo.sg/job/youdo_web_testing_three/1622/artifact/uitests/report/report.html). Generated private evidence: /home/slnnk/ai-data/jenkins-2006-autoscale/.

## Actions

Parsed report durations and statuses. Downloaded a reproducible random sample (seed2006) of60passed logs plus10longest logs; measured first browser-session log gap and summed API response times. Read3same-name historical test logs from each baseline. A delegated read-only analysis correlated the long console and sanitized endpoint timings. No services, repositories or external records changed.

## Findings

- Build wall266.99min; HTML report test phase263min. Timestamped console activity continues until14:03:26UTC, with Maven finishing14:04:01UTC. No evidence of a3h silent final WebDriver wait. Suite1594; HTML175failed/4not-implemented/52skipped/1363passed, Maven179failures.
- Parsed1590duration rows (4not-implemented excluded) sum3011.02worker-minutes, median84s;1363passed median80s and sum2281.55min.175failed median215s and sum729.47min. Sum/263min gives roughly11.45effective concurrent test methods (configured12). This ratio is a derived estimate, not thread telemetry.
- Historical two/1978 wall93.83min, report median25s and sum943min; three/1622 wall108.39min after deployment-based Selenium scaling. Historical measured values are in the existing September30/October1 investigations.
- Of60random passed logs,51had a measurable pre-remote-IP gap: median0.828s, p904.630s, max41.426s. This is a session-start proxy, not precise network timing. Browser provisioning is not the dominant observed delay.
- The60passed sample contains6247s test duration and4138.834s summed API response durations (66.3%). Parallel worker sums must not be interpreted as additive build wall time.

| Same test | Old Selenoid API sum | Yandex K8s API sum | Current API sum | Current test duration |
|---|---:|---:|---:|---:|
| TasksTestSuite.testMaxOfferLimit |126.593s /369calls|165.252s /369calls|953.350s /370calls|990s|
| ModerationTestSuite.testSearchDialogsWithUserNegative |58.009s /160calls|107.353s /160calls|1506.293s /276calls|1546s|
| PaymentForContactTestSuite.testTasWithMaximumOffers |91.123s /230calls|186.378s /277calls|2253.529s /449calls|2422s|

- The first comparison is especially useful because API call count is almost unchanged, while response-time sum increased7.53x vs Selenoid or5.77x vs Yandex K8s. The other tests also perform more requests, so their whole-test slowdown cannot be attributed solely to latency.
- Exact max-offer workload endpoint medians, with equal counts: registration34calls in each baseline/current,1978=0.5525s,1622=0.6015s,2006=9.1485s; signin38calls in each,1978=0.177s,1622=0.2025s,2006=8.368s. Relative to Yandex K8s, registration is15.2x and signin41.3x slower. These endpoints alone sum644.111s now vs26.253s in1978 (+617.858s).
- Current max-offer test:34registration calls sum319.30s/median9.149s;38signin calls sum324.81s/median8.368s. Registration and signin account for644s of953s logged API time.
- Current negative dialog-search test:104registrations sum1136.53s/median10.369s. Its API sum1506s accounts for97% of1546s test duration. Test-data preparation can occupy a worker without holding a browser slot.
- Longest test40m22s:449API calls sum2253.53s (~93% oftest duration), browser-start gap0.848s. Full console has31748logged API responses, median1.198s/p909.446s/p9510.483s;9833exceed5s. These are client-observed response times and do not separate network from backend processing.

## Changes

Added this investigation, linked it from the earlier2006evidence and existing dev-deployment map. No code or runtime changes.

## Status and risks

Observed duration is dominated by slower test/stand API interactions, notably registration and signin/data setup, while tests remain broadly parallel and browser creation is fast. Infrastructure worker scale-up was separately confirmed, but does not demonstrate API health. The underlying API latency cause (backend, database, downstream dependencies or network) has not been isolated, and full-run latency attribution is not available from a60test sample. Historical code and stands differ. No fix is claimed or deployed. Earlier user-closed diagnostic backlog entries remain closed; no new action was authorized beyond this investigation.

## Portable lesson

none

## Subsequent monolith diagnosis

[Nomad test1 inspection](2026-10-20-nomad-test-test1-monolith-rabbitmq-exchange-latency.md) identified RabbitMQ auto_delete declaration mismatch on youdo.user.signin, synchronous publication retry~8s and server-side matching API latency. This supersedes the earlier unisolated-cause status for the observed signin delay; total build attribution remains approximate.
