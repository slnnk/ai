---
system: nexus
status: verified
checked: 2026-10-12
tags: [recovery, youtrack, DevOps-890]
---
# Nexus recovery status comment in DevOps-890

## Task
User explicitly requested a YouTrack comment about current repositories, blob stores, users and recovery work in DevOps-890. This request authorized the comment POST.

## Context
Nexus state and completed recovery evidence from the existing system map. Fresh REST inventory confirms19repositories,10File blob stores and8active users. No credentials or personal data copied to the comment.

## Actions
Executed comment_inventory.py read-only against Nexus. Drafted devops-890-comment.md under /home/slnnk/ai-data/nexus-recovery/. Posted it using post_recovery_comment.py to /youtrack/api/issues/DevOps-890/comments. POST succeeded, comment74-124640. Subsequent GET verified exact saved text.

## Findings
Comment lists Docker/Maven/NuGet/npm/raw repository types, group memberships and blob assignments, active users/roles, completed package recovery and CI authentication work. Explicit limits: empty raw repositories, pending public npm route, integrity differences, temporary anonymous reads, incomplete historical/transitive recovery, and MR1371 Molecule Docker API mismatch.

## Changes
Added only requested YouTrack comment74-124640; no issue fields, pipeline, deployment or Nexus configuration changes. Local inventory/comment scripts and draft are in ai-data; secret values remain runtime-only.

## Risks
Status is a snapshot as of2026-10-12; this comment does not claim full historical artifact recovery or successful real mobile application downloads.

## Portable lesson
None.
