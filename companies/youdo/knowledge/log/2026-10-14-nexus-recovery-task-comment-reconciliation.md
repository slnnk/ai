---
system: nexus
status: verified
checked: 2026-10-14
tags: [nexus, youtrack, recovery, gitlab, nomad]
---
# Recovery task ownership and verified YouTrack comments

## Summary

The user explicitly assigned Python library/PyPI recovery to DevOps-890, Nomad cron image recovery to DevOps-895 and data/dockers base images to DevOps-891. Three user-requested YouTrack comment writes completed and independent GETs verified exact final text. Existing unrelated recovery content was preserved. Historical approved branch names, commits and MR titles containing DevOps-891 remain unchanged; this classification correction does not authorize Git renaming or history rewriting.

## Task and authorization

The user's explicit request covered updating the existing DevOps-890/891 comments in their established format and adding a DevOps-895 comment. It authorized those three comment writes; no additional approval was requested. The canonical classification for subsequent bookkeeping is Python libraries → DevOps-890, periodic workload images → DevOps-895, base images including data/dockers → DevOps-891.

## Published comments and verification

| Task | Action | Comment | Verified UTC |
| --- | --- | --- | --- |
| [DevOps-890](https://youtrack.youdo.com/issue/DevOps-890) | Update existing | 74-124640 | 2026-10-13T22:00:27.785566Z |
| [DevOps-895](https://youtrack.youdo.com/issue/DevOps-895) | Create | 74-124666 | 2026-10-13T22:00:28.143105Z |
| [DevOps-891](https://youtrack.youdo.com/issue/DevOps-891) | Update existing | 74-124638 | 2026-10-13T22:00:29.576127Z |

DevOps-890 comment8219characters preserves other Nexus ecosystem/LDAP sections and adds PyPI repositories/stores/identity, the nine publisher repositories,32required versions and five merged consumer MRs with successful master CI. Fresh Nexus GET verifies22repositories/12stores. It links the base-image and cron-image tasks separately. Credentials were not written.

DevOps-891 comment10789characters corrects the stale data/dockers running state to successful build3222108 and exact python-uv:3.12-base/3.12-builder publication evidence. Cron recovery plan point8 now cross-references DevOps-895 instead of carrying the workload scope in the base task. Other base-image content is preserved; no claim is made that the separate plain Python image job was rebuilt.

DevOps-895 comment4823characters records eight exact runtime references for23periodic parents, original-Dockerfile builds and fixed-release hash repairs, plus actual-run audit limits. Four non-cleaner parents have post-restoration task starts, actual image IDs on the worker remain unverified, and eighteen others lack retained detailed runtime records rather than proven never running. Cleaner is explicitly ignored by the user for known bad Nexus credentials; its cached image differs from registry. The user-executed ab production deployment job success is distinguished from allocation/application health verification.

## Evidence and changed files

Generated evidence: ~/ai-data/nexus-pypi-recovery/task-comments/publication-results.json, published issue snapshots and proposed.txt comment bodies. Every publication result has written=true and verified=true. This log, existing Nexus/GitLab maps, current context task convention, live TODO links, indexes and sync notes record the corrected ownership. No repository, historical Git name, CI setting, infrastructure service, Nomad job or credential changed in this comment-publication stage.

## Limits

All32PyPI versions and8runtime references were artifact-verified; all5consumer MRs/master CIs completed. Actual periodic image/runtime verification remains incomplete as detailed in [runtime audit](2026-10-14-nexus-nomad-cron-runtime-audit.md). Task comments describe those limits rather than claim every periodic task ran the rebuilt image.

## User-reported DevOps-895 closure

On October14 the user reported closing DevOps-895 and accepted the cron image restoration scope as complete. This is a user-reported task closure, not an agent tracker mutation. Eight runtime image references are restored/available; actual image identity and retained run-history limits remain documented in the audit. Closure does not infer all23periodic jobs executed rebuilt images. Those audit limitations do not reopen or block the accepted restoration task; further runtime investigation requires a separate user request. Wider Nexus/PyPI DevOps-890 and base-image DevOps-891 work is unaffected.
