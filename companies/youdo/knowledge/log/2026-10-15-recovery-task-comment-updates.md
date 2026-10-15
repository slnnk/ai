---
system: recovery
status: verified
checked: 2026-10-15
tags: [youtrack, recovery, jenkins, nexus, gitlab-ci]
---
# Six recovery task comments reconciled with October15 acceptance

## Summary

User requested a plan for updating recovery task comments, then explicitly instructed executing it. Updated existing YouTrack comments for DevOps-890,891,892,894; created first comments for DevOps-897,899. Six exact GET verifications passed. No issue state changes, repository edits, releases or infrastructure mutations performed.

## Context and decisions

Read current issues887-899 and comments before drafting; refreshed the six target baselines immediately before publication. Existing UI recovery in890 and BuildAPI0.5.13 in898 were already documented and not duplicated. Tasks893,895,896,898 left unchanged; optional888 comment not included. Correct task ownership preserved: Python/PyPI890, base/data-dockers891, cron895, per-stand delivery899.

## Published changes

| Issue | Comment | Outcome |
| --- | --- | --- |
| [DevOps-890](https://youtrack.youdo.com/youtrack/issue/DevOps-890) | 74-124640 | Added MassTransit1.8.1 assembly repair and five historical ServiceCore packages; Trackingpixel acceptance; existing history preserved. |
| [DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891) | 74-124638 | Added ES mirrors, kubectl1.35.6, devdockerMR55/localPostgreSQL10 publication; dated former quiet-mode state, marked56+3 as initial inventory. |
| [DevOps-892](https://youtrack.youdo.com/youtrack/issue/DevOps-892) | 74-124647 | Working5826/test5 and5827/test4 accepted; quiet hook removed, BuildAPI publication corrected; existing valid history retained. |
| [DevOps-894](https://youtrack.youdo.com/youtrack/issue/DevOps-894) | 74-124669 | Replaced obsolete first-working-run-pending claim with5826/5827 acceptance; retained DBA_Clean/AWX/canonicalDNS limits. |
| [DevOps-897](https://youtrack.youdo.com/youtrack/issue/DevOps-897) | 74-124677 | First summary: largeSQLstages1-5/ACTIVE400GiB,6-7notrun,11thinSQLjobs, DNS/MR106/MR1374, one-off90.1GiBbackup. |
| [DevOps-899](https://youtrack.youdo.com/youtrack/issue/DevOps-899) | 74-124678 | First summary:8+7services/test5, separateModerationS3,8services/test4,104catalogjoblinks across13otherstands; fixes and UI/exclusion limits. |

## Actions and verification

Artifacts~/ai-data/recovery-task-comment-plan/: issues-current.json fresh baseline, drafts/DevOps-ID.md, six root-level diffs, manifest.json, per-issue intent/publication receipts and publication-results.json. comments.py --apply checks all six exact text/updated baselines before the first POST, refuses prior intent/receipt replay, then verifies exact published text via GET. Four existing comments retained their IDs; two new IDs captured. Author/login and credential-literal checks passed, source mapping reviewed. Draft897 corrected to require agreement before stages6-7;892 distinguishes Ansible staticMR108 from inline JenkinsBuildAPI correction.

## Limits and changed files

Original remaining-work boundaries preserved: no whole-six-image devdocker rebuild success asserted; MSSQL6-7 not executed; prepared104links do not mean104deployments; Landings/SocketUI limits retained. Issue states unchanged by this operation. Local files changed only in ai-data artifacts and KB log/index/sync-notes. No secrets recorded.
