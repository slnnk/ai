---
system: gitlab
status: verified
checked: 2026-10-12
tags: [gitlab, registry, base-images, recovery]
---
# Base images: ASP.NET 8 retry verified

## Summary

The user retried ASP.NET 8 successfully. The original batch now has 43 successful and 11 failed pipelines. The LibreOffice child is ready for a separately authorized build.

## Task and context

Restore the stopping point of [the recovery batch](2026-10-11-gitlab-base-images-rebuild.md) and inspect user-supplied [job 3218243](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3218243).

## Actions and findings

Read-only GitLab API GETs checked the job, trace and original 54 pipeline statuses. Job 3218243 is successful on tag `microsoft/aspnet/8.0`, original pipeline 140549, finished 2026-10-12 11:56:20 +03:00. Debian HTTP package downloads succeeded in this run; this alone does not establish recovery for every runner or older Debian release.

Authenticated registry manifest GET for `registry.youdo.sg/youdo/base-images/microsoft/aspnet:8.0` matches the published trace digest `sha256:898d58c70359290f09ec2e8c7bd0435694d6a30d9ffb4dd7491f651678403990`.

Original pipelines 140545 through 140598 currently total 43 success / 11 failed, none running. Remaining failed tags and previously recorded causes remain in the original batch log, excluding ASP.NET 8.

`microsoft/aspnet/8.0-libreoffice` was never launched because its parent failed; that blocker is now resolved. `nomad-n-tools/1.1+latest` still requires the external Nomad parent per the previous investigation, not rechecked today.

## Changed files and limits

Updated this log, the existing GitLab map and the shared backlog. No repository edits, pipeline creation or external mutations. Local `rebuild-state.json` remains a historical snapshot: its helper refresh only checks running/launching items and does not discover retries of failed pipelines. Reconcile the successful parent and blocked child before any future coordinator run. Actionable work remains in `~/ai/TODO.md`.
