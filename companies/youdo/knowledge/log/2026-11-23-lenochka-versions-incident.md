---
system: lenochka
status: verified
checked: 2026-11-23
tags: [incident, jenkins, buildapi, gitlab]
decision_state: cancelled
decision_scope: Optional Lenochka release-search and error-handling hardening
decision_summary: The user declined the proposed hardening after service recovery.
decision_date: 2026-11-23
decision_source: #decision-record
---
# Lenochka version parsing stalls Jenkins and BuildAPI

## Task

Investigate the concurrent BuildsInfo 502, slow and empty Jenkins dynamic deployment parameters, and the Static release view in Lenochka.

## Context

Jenkins runs in VK, BuildAPI in VK Kubernetes, and Lenochka as a Selectel Nomad job. The user supplied screenshots of the external BuildsInfo 502 and the Static release `Draft: Release-2.922` with zero ready MRs.

## Actions

Read nginx error logs, BuildAPI logs and Kubernetes workload status, Jenkins controller health and job parameter configuration, and Selectel Nomad logs. Reproduced authenticated Lenochka reads and checked the related GitLab release searches, pipeline lists and labels. Inspected local Lenochka revision `5348cd5` and BuildAPI revision `bb23b95`.

## Findings

- GitLab release search uses `search=Release-` across titles and descriptions. Monolith [!10149](https://gitlab.youdo.sg/youdo/youdo/-/merge_requests/10149) matches only via `Release-сборка` in its description. It targets `master` and its title contains no version. The exact live query returned it at the top of the candidate list. Restricting the query to titles excluded it and returned versioned release candidates.
- Lenochka job version 105 repeatedly logs `TypeError: Cannot read property '0' of null` in `MergeRequestVersion`, followed by `API resolved without sending a response for /api/versions/18`. The parser indexes the unchecked regex result. The route catches the exception and sets a status without completing the response. An authenticated GET timed out after 16 seconds.
- Jenkins `MONOLITH_PIPELINE_ID` and `STATIC_PIPELINE_ID` call Lenochka versions for projects 18 and 278 before querying GitLab. Neither script sets connection or read timeouts. Direct GitLab API reads returned current pipelines for both projects. BuildAPI logs confirm the home route fails on `resp.json()` from Lenochka project 18. Public nginx logs show repeated premature upstream closes, and the user saw 502. BuildAPI pods were Ready with zero restarts and `/metrics` returned 200.
- Static `/api/versions/278`, `/api/projects/278` and the release candidate list returned 200. The candidate list for [!3663](https://gitlab.youdo.sg/youdo/youdo.static/-/merge_requests/3663) contained zero ready and one accepted MR. The release MR is `master` to `production` with no head pipeline. [!3661](https://gitlab.youdo.sg/youdo/youdo.static/-/merge_requests/3661) has `qa::tested` and a successful head pipeline, while the candidate lookup requires `devops::ready for release` on open MRs targeting `master`. The directly queried GitLab candidate set was empty. The reported Static 500 was not reproduced on these reads, and its exact route or action is unknown.

## Changes

Local knowledge bookkeeping. Incident diagnostics used reads. No incident-related remote writes, builds, deployments or restarts.

## Status and risks

Diagnosis complete for the shared Monolith dependency. Proposed immediate recovery is a targeted wording change in the description of monolith !10149, subject to approval. Verify its exclusion from release search, a successful JSON response from Lenochka, the authenticated BuildsInfo page, and Jenkins parameter loading. The durable parser correction and the unidentified Static 500 remain tracked in the [central backlog](../../../../TODO.md).

## Recovery follow-up

The user edited the description of monolith !10149 and confirmed that all reported functions work again. The same GitLab search now excludes !10149. Authenticated Lenochka project 18 returned HTTP 200 with versions 2.1014 and 2.1013 on retry, after one ten-second timeout. Project 278 returned HTTP 200 with versions 2.922 and 2.921. Authenticated public BuildsInfo home returned HTTP 200 HTML in 4.41 seconds. Jenkins parameter and Static UI recovery are based on the user's confirmation. The previous Static 500 route remains unidentified. The incident is closed. At incident closure the parser hardening proposal was recorded in the central backlog. See the later decision below.

## Decision record

On 2026-11-23, the user declined the proposed Lenochka release-search and error-handling hardening. The proposal was closed as cancelled in the central backlog.

## Portable lesson

none

## Task metrics: 2026-11-23-lenochka-versions-incident

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "2026-11-23-lenochka-versions-incident",
  "created": "2026-11-23T17:43:10.548635+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "incident",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "User edited !10149 and confirmed end-to-end recovery. GitLab search excluded !10149 and authenticated Lenochka and BuildsInfo GET returned 200.",
  "updated": "2026-11-23T18:48:23.736940+03:00"
}
```
