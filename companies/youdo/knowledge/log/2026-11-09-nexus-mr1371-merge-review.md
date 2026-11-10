---
system: nexus
status: verified
checked: 2026-11-09
tags: [nexus, nomad, gitlab-ci]
---
# MR1371 merge readiness review

## Task
Explain automation-services MR1371 and assess whether it can be merged. Investigation only; no merge, repository edits, CI run or deployment authorized.

## Findings
Live GitLab GET confirms open non-draft MR, source DevOps-890-nexus-docker-auth at f4018c2bf2e1d08cb2bf4c739bf64b3b667c4853, target master at 6d467c2e196f347bfe500bb96f0af0ce4e03f111. GitLab reports mergeable without conflicts, resolved blocking discussions and no approvals. Scope is four files: common Nomad Nexus auth defaults/assert/template and Docker28.5.2 DinD pin in three Molecule jobs. CI has no deployment jobs.

Latest pipeline140673 is skipped; previous pipeline140665 failed before tests. User declined the manual final-revision test in the [original work log](2026-10-12-nexus-automation-services-nomad-docker-auth.md). No full Molecule pass claimed.

NEXUS_DOCKER_PASSWORD must be supplied by the Ansible controller for role executions that write Docker auth. Injection into every consumer has not been verified. Missing value triggers the new assertion before Docker config writes.

Current master already added no_log:true and diff:false to the template task. Local read-only merge-tree simulation yields duplicate no_log:true keys because MR adds the same key before the existing when. Live master task bytes were confirmed identical to the local simulation target through GitLab GET. Values agree, but deduplication before merge is recommended; retain diff:false. Other three affected master files are unchanged since the MR base.

## Validation
Exact source inspected locally. Source diff whitespace check passes. Jinja fixture renders valid JSON both with and without Nexus auth and preserves GitLab registry credentials. No full Ansible/Molecule execution this session. All read-only network processes completed.

## Status and risks
Review complete. Recommend removing the duplicate key and ensuring controller secret injection before merging/applying. Existing central [MR1371 review/merge backlog item](../../../../TODO.md) remains open; no status change, merge or external mutation performed. No separate implementation proposal was executed.

## Portable lesson
none
