---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [elasticsearch, rsync, vk-cloud, backup]
---
# DevOps-894 thin Elasticsearch data transferred to VK share

## Summary

User explicitly approved the reviewed thin transfer operation. Copied120572815bytes (~121MB),3872regularfiles from backup172.24.0.19 `/backup/sql/elastic_smalldb/data/` to VKshare10.18.26.4 `/data/elastic/thin/` with source `elasticsearch_smalldb_1` stopped. Rsync checksum/metadata comparison while source remained stopped found no differences. Source container restarted and runningtrue confirmed; commandrc0. This proves matching cold-copy bytes, not successful ES startup. Target has no Docker. Thick dry-run passed separately; its apply remains unapproved.

## Task and context

[DevOps-894](https://youtrack.youdo.com/issue/DevOps-894), [plan](2026-10-13-nomad-test-devops-894-elasticsearch-vk-plan.md), [source/preflight evidence](2026-10-13-nomad-test-devops-894-es-source-check.md). User answeredyes to thin stop→copy→checksum→restart proposal; it does not authorize thick transfer or target package/service changes.

## Actions and key commands

Executed `ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=10 -o StrictHostKeyChecking=yes root@172.24.0.19 python3 - thin --apply < ~/ai-data/nomad-es-vk-transfer/transfer.py`. Helper used key-only root→root SSH with transient pinned target host key. Destination was empty; source data mount checked. Dockerstop followed by `rsync -aH --numeric-ids --delete --exclude=java_pid1.hprof`, checksum/metadata dry-run, then Dockerstart in `finally`.

Transfer stats:3971totalentries,3970createdentries,3872regularfiles,0deletedfiles,120572815literalbytes. Verification emitted no differences; `checksum_verified=true`. Final `running_after=true`; complete operationexit0. No target ES container launched.

Read-only destination follow-up: `/data/elastic/thin/nodes` exists; directory uid1000,gid0,0775. Root data directory mirrors source uid0,gid0,0777. Source ownership/modes were preserved byrsync; no separate chmod applied. `vm.max_map_count=1048576`. Docker executable absent. Therefore local target ES startup validation cannot be performed without an additional installation or a different approved validation host; data can later be tested through Nomad on a prepared Cinder clone.

## Thick preflight

Same helper run with `thick` and noapply exited0. Empty destination and exact source mount checks passed. Estimated22667132593bytes (~21.1GiB),5342regularfiles,5441totalentries,0deletions. Heap dump excluded. Reviewed proposed next invocation uses `python3 - thick --apply`; it stops `elasticsearch1`, copies `/backup/sql/elastic/data/` toshare `/data/elastic/thick/`, checksum-compares while stopped, then restarts source. Real apply and source stop are not performed or authorized yet. The source ES pause would cover both copying and checksum verification; duration depends on network and disk throughput.

## Changes and risks

Remote destinationthin now contains the copied dataset, ownership and permissions matching source. Source ES was temporarily stopped and restarted under user approval. Backup source files were not modified by the transfer. No Docker install, target ES startup, thick transfer, Cinder snapshot, DAG/repository edit or publication performed. Persistent backupknown_hosts remains unchanged. Cold-copy checksum equality is not an Elasticsearch backup/restore or index validation claim; inspect a restored ES instance before publishing a base snapshot.

## Portable lesson

none
