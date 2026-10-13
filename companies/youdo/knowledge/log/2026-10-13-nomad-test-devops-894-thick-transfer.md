---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [elasticsearch, rsync, vk-cloud, backup]
---
# DevOps-894 thick Elasticsearch data transfer to VK share

## Summary

User explicitly approved the reviewed thick stop→copy→checksum→restart operation. Completed:22667132593bytes (~21.1GiB),5342regularfiles from backup172.24.0.19 `/backup/sql/elastic/data/` toVKshare10.18.26.4 `/data/elastic/thick/`, excluding `java_pid1.hprof`. Checksum/metadata comparison found no differences; `checksum_verified=true`. Source `elasticsearch1` restarted and `running_after=true` confirmed; operationexit0. Boththin/thick datasets now reside on the VK share system disk. ES startup on the copies is not yet verified.

## Task and context

[DevOps-894](https://youtrack.youdo.com/issue/DevOps-894). [Thin transfer](2026-10-13-nomad-test-devops-894-thin-transfer.md) already complete. User answeredyes to the separately proposed thick operation. No target ES startup, installation, snapshot creation or repository change authorized by this approval.

## Actions and key commands

Executed `ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=10 -o StrictHostKeyChecking=yes root@172.24.0.19 python3 - thick --apply < ~/ai-data/nomad-es-vk-transfer/transfer.py`. Helper verifies source mount and empty destination, then stops `elasticsearch1`; `rsync -aH --numeric-ids --delete --exclude=java_pid1.hprof`, checksum/metadata dry-run while stopped, and source restart in `finally`. Backup-local root key only, transient target host-key pinning.

Copy stats:5441totalentries,5440createdentries,5342regularfiles,0deletedfiles,22667132593literalbytes. Rsync reported~33.2MB/s. Temporary root-readable size monitor observed growth to22687002624allocatedbytes and was stopped after copy completion; ordinaryyoudo could not read some copied directory permissions, so progress monitoring usedsudo without changing data permissions. Source retains its files; no heap dump copied.

Checksum comparison took additional time. Read-only target process I/O showed rsync read~22.2GB with disk/page wait (`folio_wait_bit_common`), then the operation completed successfully. Final helper output: `copied=true`, `checksum_verified=true`, sourcecontainer `elasticsearch1`, `running_after=true`. No differences emitted by checksum/metadata dry-run; SSH/script exit0. Temporary monitor session exited and no verification/transfer session remains running.

## Findings and changed files

Targetthick contains copied dataset with matching cold-source checksums and metadata. Source container is running again. No cloud disks, snapshots, targetDocker or DAG/repository files changed. Only the approved transfer and local bookkeeping performed.

## Risks and limits

Cold-copy checksum equality is not proof of Elasticsearch index validity or successful boot. Target has no Docker; restored ES validation is a separate stage. Both copies are system-disk staging directories, not separate Cinder seed disks. Preparation of standalone data volumes, clone validation and snapshot publication remain separate reviewed/authorized actions. Source restart is confirmed by DockerRunning state, not an application health check.

## Portable lesson

none
