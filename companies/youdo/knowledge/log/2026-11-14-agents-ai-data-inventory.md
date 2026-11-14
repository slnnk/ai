---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, scripts, storage, reuse]
---
# Agent scratch data: size, script copies and reuse assessment

## Task

The user raised repeated creation of scripts under ai-data despite the durable-script
rule and concern about directory size/file count. Performed a bounded read-only
inventory and reviewed existing policies and helper references. No script was run,
removed, promoted or rewritten; KB bookkeeping only. Source session:
01a1d727-6401-7be0-ab41-a4ea664e6a74, ai-data reuse question.

## Findings

Local snapshot November14: du -x reports about7.7GiB allocated across ai-data.
A no-follow directory walk counted193647file entries, including symlink file entries;
this is not193647agent-authored scripts. Counts and sizes can change during use.

| Directory | Allocated size | File entries |
| --- | --- | --- |
| nexus-recovery | 5.9GiB | 164940 |
| ai-qa | 1.2GiB | 22485 |
| nexus-pypi-recovery | 245MiB | 1510 |
| jenkins-2006-autoscale | 127MiB | Not separately reported |

The two largest directories contain187425of193647entries, about96.8%.
Within nexus-recovery, npm-local-build is1.4GiB and ui-local-0260-0254 is1.1GiB;
other large directories are package builds and caches. In ai-qa, git-2.47.3 is646MiB,
postgresql-16.13 is230MiB, git-runtime106MiB, venv79MiB and pg16-test-data59MiB.
Directory inspection confirms source/build trees and package artifacts. This does
not establish that any directory can safely be removed or recreated from an available
remote source; recovery artifacts may have unique value.

A bounded scan hashed799regular script-extension files no deeper than three relative
path components, under2MB each, excluding named dependency/cache paths. This is a
candidate set, not a count of799unique handwritten agent helpers or a full semantic
clone audit. No script read errors were reported. Exact SHA-256 groups found:

- DevOps-898/{vks-build-publication,manual-production-publication,socket-revert-publication,publication}/publish.py: four identical files.
- DevOps-898/{vks-build-publication,socket-revert-publication,publication}/merge.py: three identical files.
- cudy/trusttunnel-netifd-upstream.sh and cudy/integration/trusttunnel.sh: two identical files.

AST-only inspection shows the publication helper references sibling manifest/results
files and existing canonical gitlab_task_mr.py. These copies may be immutable evidence
or per-publication packaging, so identical bytes alone do not prove redundant live
maintenance. The monolith-nomad-rebuild.py helper exposes multiple commands and relies
on neighboring receipts and deploy-test5.py; its long-lived role is documented in the
[recovery task](2026-10-15-jenkins-monolith-rebuild-nomad-restart.md). It is a candidate
for lifecycle review, not a safe standalone move. No secret values were printed.

## Rule assessment

README Layers places portable scripts in general, personal tools in personal and
company tools in current; ai-data holds generated data. Economical tool use already
requires checking layer scripts first and scripting repeated command sequences.
The inspected README does not specify a general cleanup/retention lifecycle for
completed ai-data builds. The evidence supports separating code reuse from bulky
artifact retention; adding another broad simplicity slogan would not fix either.

## Proposed disposition

Reusable operational helpers belong in the correct scripts directory (or an existing
skill's scripts); parameterize only concrete reuse needs, retain approved behaviors
and verify callers. One-off investigation scripts and frozen review artifacts may
remain with task evidence. Do not move company details into general or blindly copy
credentials/instance-specific payloads into tracked code.

Before cleanup, classify reproducible build/cache output, unique recovery artifacts,
active runtime/test data, receipts, benchmark baselines and rollback evidence. Check
live use, dependencies, KB/source links and actual recovery availability. Present an
exact reviewed removal/archive list and obtain explicit cleanup approval; size or
age alone is not permission. Moving scripts can invalidate existing approved command
prefixes and callers and needs explicit accounting. No automatic expiry policy adopted.

## Actions and status

Saved this assessment and two separate proposals in central TODO: helper promotion/
reuse, then reviewed artifact retention/cleanup. Existing P0.1 can treat a demonstrated
recreation of an already suitable helper as an avoidable-work example; counts of new
files are not automatically failures. Existing learning/pilot priorities remain open.
The current audit is complete; cleanup and migration are not performed. All inventory
commands finished with no background operation. No external systems changed.

## Portable lesson

Use the existing Layers and Economical tool use rules. No new general rule or automatic
cleanup implementation was introduced by this discussion.

## Task metrics: 01a1d727-ai-data-inventory

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "01a1d727-ai-data-inventory",
  "created": "2026-11-14T02:58:09.800681+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "investigation",
  "model": "gpt-6-astra",
  "session_id": "01a1d727-6401-7be0-ab41-a4ea664e6a74",
  "corrections": 0,
  "unnecessary_actions": null,
  "critical_events": 0,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Read-only size/count/hash inventory and AST checks completed; no migration or deletion; root-cause universality and first-delivery acceptance remain unassessed",
  "updated": "2026-11-14T02:58:09.800736+03:00"
}
```

## Clarification: persistent data versus temporary work

The user asked whether ai-data is a replacement for /tmp and why completed builds
and dependencies remain. Clarified that ai-data is for generated evidence/state
needed across sessions; disposable, reproducible intermediates can use temporary
storage. Keeping a build needs a concrete continuation, reuse or unique-recovery
reason. A required executable does not necessarily require retaining its entire
source/object tree. Proposed end-of-task retain/temporary/delete dispositions and
bounded caches belong to existing P2.2, not a new cleanup task. The user asked to
ensure all proposals are recorded and list the Knowledge base backlog. No deletion,
movement, runtime policy or automatic expiration was authorized by this clarification.
