---
system: agents
status: verified
checked: 2026-11-18
tags: [ai-data, retention, cleanup]
---
# ai-data retention audit and local cleanup

## Task

P2.2. The user authorized a full local inventory of `~/ai-data` and discretionary
archival or deletion. During the cleanup the user clarified that repeated builds
must resolve from current registries so missing packages are visible. Package
caches and old installed build dependencies should be discarded. The global
[local rebuild rule](../../../../general/knowledge/README.md#dependency-sources-for-repeated-builds)
records that decision without changing CI configuration.

## Result

Completed 2026-11-18. The inventory covered 82 original root entries. Allocated
space fell from 8,536,637,440 to approximately 1,834,840,064 bytes, freeing
6.24 GiB. Two verified archives and six standalone Maven recovery files remain
in the private retention directory. The registry was not queried or used for
a fresh build during this cleanup. All local operations finished.

## Inventory and disposition

The private inventory is at `~/ai-data/.retention-20261118/inventory-before.json`.
It includes hidden entries, allocated bytes, entry counts and reference matches
from the KB and inspected scripts/configuration. The original root contained 69
directories and 13 loose files. Lower-volume entries were reviewed by category.

| Area | Disposition |
| --- | --- |
| Nexus NuGet | Remove 16 historical dependency caches and their temporary archive. The 218 cached package IDs corresponded to third-party dependencies; separate internal build artifacts and receipts remain in place. |
| Nexus Gradle | Remove the dependency cache and its temporary archive after separating six internal Maven files (about 39 MiB), absent from the separate local Maven repository. The six files are preserved as recovery evidence. |
| Nexus npm | Remove four content stores, all six identified build-only installed dependency trees, and two associated scratch symlinks. Retain source, lockfiles, packed artifacts, npm logs and publication evidence. |
| ai-qa | Archive Git 2.47.3 and PostgreSQL 16.13 build trees. Keep installed Git and PostgreSQL, the venv, the stopped test database and acceptance evidence at their original paths. |
| Jenkins web-autotests job 2006 | Archive the full original console capture. Keep other job evidence in place. |
| Nexus PyPI | Preserve publication evidence and the exact rowers-ranker model snapshot. |
| Ansible MCP and Nomad access | Keep the MCP runtime at its launcher path and the local Terraform executable alongside recovery state. |
| Other root entries | Keep generated skill state, benchmark baselines, recovery and publication records, diagnostics, configurations and helpers. The DevOps-908 directory named `gradle-cache` contains proposal and publication evidence. |

## Verification

The first root inventory command hit a Python version mismatch in its targeted
reference check. The check was rerun with Python 3.12 before any destructive
operation. Candidate paths were checked for visible process use and incoming
symlinks. One early npm archive attempt was stopped by two incoming links from
historical scratch builds. Those exact links were subsequently removed with the
old dependency trees following the user's cache decision.

The two retained tar.xz archives were extracted privately before removal of
originals. Restored entry sets, contents and accessible metadata were compared
with the originals, including checksums, ACLs, extended attributes and links.
Final checksum verification covered both archives and 20 retained files.
The retained Git, PostgreSQL and Node runtimes reported their expected versions;
`pg_controldata` confirmed that the separate test database was shut down.
The two published UI packages matched the SHA-256 values in the recovery log.

Exact removed and archived paths are in the private JSON manifests. The private
archives are stored on the same filesystem. No automatic cleanup, remote build,
pipeline changes or external writes were performed.

## End-of-task retention

Use private temporary work for disposable build intermediates and discard
package-manager caches when the build ends. Retain active tools, unique assets,
published binaries, receipts, rollback evidence and immutable baselines when
there is a concrete reuse or recovery need. Preserve the needed output
independently of the source and object tree. Archive a completed build tree only
when it has recovery or evidence value.

The user subsequently asked to make this a general closeout rule for logs,
archives and artifacts. See [Generated data retention](../../../../general/knowledge/README.md#generated-data-retention).

## Restore

Archives and per-group JSON manifests are under
`~/ai-data/.retention-20261118`. Each manifest has the exact original paths,
allocated sizes, entry count and SHA-256.

To inspect or recover a member, use a new private destination. For example,
recover the console, then copy it to its original path if required.

```bash
archive_dir="$HOME/ai-data/.retention-20261118"
(cd "$archive_dir" && sha256sum -c SHA256SUMS)
restore_dir=$(mktemp -d)
tar --acls --xattrs --xattrs-include='*' -xJpf "$archive_dir/jenkins-console.tar.xz" \
  -C "$restore_dir" -- jenkins-2006-autoscale/console.txt
```

For a build, use the appropriate archive and list the required member roots
from its manifest. Check for recreated files before copying recovered data
back to the original location.

## Sources

- [Initial ai-data inventory and retention proposal](2026-11-14-agents-ai-data-inventory.md)
- [Historical npm UI builds and package checksums](2026-10-15-nexus-ui-0260-0254-ci-recovery-inspection.md)
- [Jenkins job 2006 console context](2026-10-20-web-autotests-jenkins-2006-k8s-autoscaling.md)

## Task metrics: P2.2-ai-data-retention

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "P2.2-ai-data-retention",
  "created": "2026-11-18T23:40:22.975053+03:00",
  "first_result": "fail",
  "final_result": "pass",
  "state": "closed",
  "kind": "knowledge-base",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Initial targeted inventory needed a Python version retry; full local inventory and cleanup completed with verified archives and retained artifacts. User clarified registry-only dependency resolution before final cleanup.",
  "updated": "2026-11-18T23:52:12.986752+03:00"
}
```

