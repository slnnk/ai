---
system: agents
status: verified
checked: 2026-11-18
tags: [scripts, reuse]
---
# Agents: reusable helpers from ai-data

## Task

The user asked to execute P1.6 after reviewing its scope and expected benefits. Audit the helpers surfaced by the [initial inventory](2026-11-14-agents-ai-data-inventory.md), and move proven recurring tools into the existing script directories with working local entry points.

## Context

The earlier hash scan surfaced publication and router artifact copies. The follow-up used a bounded filename inventory and inspected the relevant callers, output formats and approval paths. It compared repeated Nexus collectors from October 22, October 29–31 and November 10, and Cudy uses for Telegram, LinkedIn and MediaManager. Data and receipts remain in `~/ai-data/`.

## Actions

Selected two candidates with demonstrated reuse before editing. The runner collector's three copies varied mainly by time window, with the latest copies also retaining commit metadata and a larger pagination limit. The Cudy importer had already been called from multiple independent tasks. Their existing Nexus and home network maps now point to the supported entry points.

## Findings

| Candidate | Decision and evidence |
| --- | --- |
| Nexus `collect_runners.py` | Keep one [company collector](../../scripts/gitlab_runner_jobs.py). Accept explicit timezone-aware window and output path. Preserve overlap semantics, runner status filtering, job fields and top-level JSON keys used by local correlators. Leave the recorded input and output artifacts in their original evidence directories. |
| Cudy `add_domains.py` | Keep one [personal domain helper](../../../../personal/scripts/cudy_add_domains.py). The old local path delegates to the tracked script. Keep source lists, generated shell files and verification receipts adjacent to each run. |
| DevOps-898 `publish.py` and `merge.py` | Keep the four publication copies and three merge copies with the reviewed manifests and results. Publication already calls `gitlab_task_mr.py`. The merge copies belong to specific review sequences. |
| Jenkins `monolith-nomad-rebuild.py` and `deploy-test5.py` | Leave the linked recovery pair in place. The former embeds a pipeline ID, commit and allowed jobs, and uses the sibling helper and receipt. Existing command approvals refer to the original paths. |
| GitLab review `collect.py` | Preserve the recorded one-week audit collector and its approval path. Found one documented review run. |
| Cudy TrustTunnel shell copies | The identical files are an upstream sample and an integration artifact. Keep them with the router evidence. |
| Nexus `trace_sources.py` | Leave the research scripts with their reports. Their project/job selection, marker sets and output limits differ by investigation. The promoted runner collector supplies the common input format. |

## Changes

The GitLab runner collector uses standard-library HTTPS and the company `.env`. It accepts `--start`, `--end` and `--output`. For new work, select an existing output directory under `~/ai-data/` and use `runner-jobs.json` as the report name. Runner-level errors are saved in the report and give a nonzero exit status. A failed top-level collection preserves any previous report. The Cudy helper validates by default. Its apply mode still requires separate approval for the reviewed list. Input validity checks also run under `python3 -O`.

## Status and risks

Offline checks on Python 3.8 verified the GitLab CLI with synthetic GET responses, UTC `Z` timestamps, overlap boundaries, offline runner filtering, historical report and job field compatibility, runner-level failure and preservation of an existing report on top-level failure. The collector retains the original contact-age filter and pagination bounds, so skipped runners and errors limit coverage. A live GitLab collection was outside this verification.

Verified matching output and receipts from both Cudy paths with stub SSH, dry validation without receipts, malformed input rejection and byte-for-byte preservation of the original router apply body. No actual SSH or router write was performed. The existing explicit approval requirement for router changes still applies. P2.2 retains the separate artifact cleanup proposal. On another workstation, use the tracked Cudy path. The legacy launcher is local to this machine.

## Portable lesson

Promote helpers where multiple real callers need the same operation, keeping per-run inputs and reports out of shared code. The demonstrated cases fit the existing scope and script-placement rules.

## Full-directory audit after user correction

The user clarified that P1.6 requires a recursive audit of all `~/ai-data/`. The first completion above used selected groups and was reopened. The second pass traversed all 69 top-level areas, including hidden paths and nested dependency and build directories. It walked 55,023 directories, examined the first 512 bytes of 201,358 regular files for interpreter declarations, and read and hashed 96,756 script or script-source candidates without depth or size limits. There were zero read or traversal errors. Symlinks were inventoried without duplicate traversal: 334 resolve within the tree, nine point outside, and 27 were broken or unresolvable.

The raw report contains 23,457 exact-hash groups. Of the 96,756 candidates, 90,367 are in dependency directories. Another 5,367 are in identifiable source or build trees and 116 in frozen generated trees. This left 906 candidates for operation-level comparison. Exact hashes, Python ASTs with parameter literals normalized, file names and token shingles found ten exact groups, 29 same-structure groups, 35 same-name groups and 242 near pairs in that set. Exact, structural and near matches form 44 candidate families. These counts overlap and reflect lookalike code, including shared boilerplate. They are not counts of live tools or proven semantic duplicates. Seven Python sources outside dependency directories could not be parsed as AST by Python 3.8; the raw hash and token passes still covered them. Arbitrary embedded code in documents or unsupported formats may escape file-type recognition.

The reproducible local inventory lives in `~/ai-data/p16-audit/`. `inventory.json` records per-file paths, hashes, area counts and match evidence. `review.json` contains the filtered candidate list and paths grouped into all 44 families. `scan.py` and `review.py` capture the two passes. Reports contain paths and fingerprints, with no raw source or secret values. Some families include different operations that share a template; decisions below consider actual inputs, effects and ownership.

| Repeated operation | Disposition |
| --- | --- |
| GitLab runner collection for Nexus | Five revisions confirmed across separate windows. Continue with the promoted `gitlab_runner_jobs.py` and retain the old dated scripts as provenance. |
| GitLab job inspection and trace reads | Six same-shape job-ID wrappers in data-services alone. For new single-job tasks, reuse the existing [job helper](../../skills/android-dig/scripts/gitlab_job.py) with `--metadata-only` or sanitized trace output. Historical jobs may need additional product-specific fields. |
| YouTrack comment inspection | Four near copies across Zabbix, GitLab and Nexus. [Promoted a read-only inspector](../../scripts/youtrack_comment_inspect.py) for exact draft matching and related text. It reuses the RP YouTrack client, reads all comment pages, and outputs only matches and issue metadata. Posting scripts remain attached to approved bodies and receipts. |
| MR update and publication | Use the existing `gitlab_task_mr.py` for fresh approved operations. Keep per-task `publish.py`, `merge.py` and update scripts with evidence. The runner-job and YouTrack inspectors have no publication role. |
| Nexus metrics, access logs and CI trace attribution | The metrics snapshots share the same requests but use the incident-specific Nexus admin access route. Preserve them until a supported authenticated route is selected for routine reuse. The parser and trace families vary in time windows, selected jobs, marker definitions and aggregation scope. Preserve dated evidence and evaluate a shared offline parsing core separately if reuse is needed. |
| Jenkins deployments, pipeline triggers, PgBouncer and recovery | Repeated templates embed different targets, approved batches, receipts and postconditions. Keep task-bound state changes and approved paths in place. New work starts from the standard service workflow or the existing documented helper. |
| Android, Selenium, VPN and data-service probes | Keep device- or incident-specific fixtures as evidence. Use existing Android GitLab/Loki helpers for overlapping read-only collection. Different probe inputs and checks remain attached to their investigation. |
| Dependencies, build sources, temporary checkouts and frozen benchmark/recovery artifacts | Keep inventory and evidence paths. Retention and space reclamation stay in P2.2. |

The additional YouTrack helper was verified offline with a stub transport: two nonempty pages followed by an empty page, exact draft equality, Unicode case-insensitive keyword matching, duplicate-page rejection and GET-only requests. `--help` ran with the system Python. No external call or write was performed in the second pass. The earlier Cudy and runner changes remain in place. The full-tree pass addresses the user's requested scope, with similarity coverage limited by the documented detection methods.

none

## Task metrics: agents-p16-helper-reuse

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "agents-p16-helper-reuse",
  "created": "2026-11-18T23:22:36.499163+03:00",
  "first_result": "fail",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": 1,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "First pass closed after a selected sample; the user required all ai-data. Recursive inventory, 44 candidate families, three promoted helpers total and offline validation are documented above.",
  "updated": "2026-11-18T23:31:28.927318+03:00"
}
```
