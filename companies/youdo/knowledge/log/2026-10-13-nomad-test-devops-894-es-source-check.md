---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [elasticsearch, nomad, vk-cloud, backup]
---
# DevOps-894 Elasticsearch prepared data source verified

## Summary

The user supplied an Airflow Connections screenshot: `backup_server_prod` and `backup_selectel` both point to172.24.0.19. Read-only SSH confirms hostname `msk3-backup.youdo.corp`. Both prepared Elasticsearch data directories exist and are mounted into running Elasticsearch6.8.23 containers. The user explicitly stated dataset dates do not matter; source presence is sufficient for this planning stage. No data transfer, stop, restart, snapshot or repository change performed.

## Task

Confirm the producer-side data exists for [DevOps-894](https://youtrack.youdo.com/issue/DevOps-894), avoiding reliance on unavailable Yandex destination10.16.28.4. [Migration plan](2026-10-13-nomad-test-devops-894-elasticsearch-vk-plan.md).

## Context

Screenshot establishes the copy-task connection endpoint, not the environment-selected reindexer source. The backup host is outside the failed Yandex destination. Root SSH with existing credentials works; no secrets printed or saved.

## Actions and key commands

Ran ai-sync (no output). Initial SSH was blocked by sandbox; escalated read-only retry returned hostname. Authorized read-only remote Python collected directory metadata, `findmnt`, bounded `du` and sanitized `docker inspect` fields. Only selected image/state/mount metadata was printed; environment variables and document contents were excluded.

## Findings

| Variant | Source | Container | Image | Data bytes (`nodes`) |
| --- | --- | --- | --- | --- |
| thick | `/backup/sql/elastic/data/` | `elasticsearch1` | `elasticsearch:6.8.23` | 22687526912 (~21.1GiB) |
| thin | `/backup/sql/elastic_smalldb/data/` | `elasticsearch_smalldb_1` | `elasticsearch:6.8.23` | 136355840 (~130MiB) |

Both containers are running, each with its matching data directory bound read/write at `/usr/share/elasticsearch/data`. Both also have backup-directory mounts at `/usr/share/elasticsearch/backup`. Source filesystem is `/backup`, `/dev/md3`, ext4. No container changes made.

Thick directory total allocated size is24737652736bytes; it includes `java_pid1.hprof` (2050117632bytes apparent size). Do not include this diagnostic heap dump in seed-data transfer; do not delete it under this task without an explicit request. Actual thin directory total is136359936bytes.

HTTP GET attempts from the host to127.0.0.1:9202 and9201 returned `URLError`; no indices, health or snapshot repositories were obtained. No endpoint root cause or Elasticsearch health conclusion is established. The user then directed that source presence, rather than date, is the immediate goal; additional freshness/health probing stopped. Running containers and existing `nodes` prove presence, not index validity or consistency.

## Changes and next-step boundary

### VK destination identified and inspected

User identified `10.18.26.4`; `automation-services/inventories/vkcloud/hosts:63` maps it to `share-test01`. Root SSH key authentication failed. User then explicitly requested trying `youdo`; read-only SSH succeeded and hostname is `vk-ms1-share-test01.mcs.local`. `sudo -n -l` returns0 and reports NOPASSWD access. A new public SSH host key was accepted into local known_hosts; no remote account/key change performed.

VM has approximately4GBRAM. `lsblk` reports root disk `vda`250G, `vdb`5G with no filesystem/mount reported, and `vdc`40G ext4 mounted at `/public`. Both `/data/elastic/thin` and `/data/elastic/thick` are absent. The40Gvolume's contents and purpose have NOT been inspected; do not unmount, reformat or repurpose it assuming it is an ES seed. A missing filesystem signature on5Gdisk is not proof that its contents are expendable. Volume UUID/project/AZ mapping remains unverified. Destination host is accessible, but seed-volume preparation is not complete. Next read-only step is to establish existing/public usage and Cinder identities before proposing exact disk/mount changes.

Historical Yandex role was `share-test01`; recovery Terraform module names it `yc-a-share-test01` (fixed suffixa), while fresh DBA_Clean targets10.16.28.4. No live/state artifact establishes the name/IP mapping; it remains inferred. VK name/IP above is directly verified by SSH plus user/inventory evidence.

Only KB bookkeeping changed. Source presence prerequisite is satisfied for the plan. Next implementation/run step is to choose the VK preparation host and seed volumes, then transfer through a supported ES snapshot/restore route or a reviewed cold-transfer procedure with writer quiescence and post-transfer validation. Existing source directories are live; copying them while ES writes does not guarantee a usable seed. All remote mutations still need explicit approval. Snapshot publication and stand deployment remain unverified and unexecuted.

### User-approved system-disk staging directories

Subsequent read-only check confirmed `/data` itself was absent. The user explicitly authorized creating the preparation directories on the system disk. Executed one remote mutation asyoudo: `sudo -n install -d -o youdo -g 1001 -m 0755 /data/elastic/thin /data/elastic/thick`. Fresh verification confirms both directories uid/gid1001, mode0755, writable byyoudo, backed by root `/dev/vda1` ext4; free space239.48GiB. Only directories/ownership created; no data copied, disk formatted/unmounted, container stopped, snapshot or repository file changed.

The user selected system-disk staging, superseding the proposed requirement to attach two seed disks before initial data delivery. The new directories are staging locations; they are not dedicated Cinder data volumes. Producing standalone data-volume snapshots from their contents remains a later reviewed step; do not snapshot the OS disk as an ES-only base without a separate design decision. Existing5G/40Gdisks remain untouched. No authorization for source stops or data transfer inferred from directory creation.

### Root-only source-to-destination SSH check

User explicitly requested checking the transfer SSH route only asroot. From root on `msk3-backup.youdo.corp`172.24.0.19, tested `root@10.18.26.4` with `BatchMode=yes`, timeout and intended remote command `id -un`. Initial attempts failed to read a transient known_hosts input; corrected the diagnostic to pin the previously observed ECDSA public host key via an anonymous memory file held by the parent process and force the matching host-key algorithm. Final result reaches SSH authentication and returns255: `Permission denied (publickey,password)`. This confirms reachable SSH but no root key login with the backup host's available credentials. No password attempted, no userdo fallback from source, no remote files/keys changed and no copy/container action performed. Workstation→youdo access remains verified separately; it does not prove backup→root access.

Later user-requested key inventory: root on172.24.0.19 has public `/root/.ssh/id_rsa.pub`, RSA2048, fingerprint `SHA256:uQcAU22bn6Tsg++xnOcelNp9nmHOYWXwU0rKDQeG3rk`, comment `root@msk3-backup`; matching-named private file `/root/.ssh/id_rsa` exists. Private key contents were not read/copied. SSH agent also reports user keys; do not confuse them with the backup-local root key or rely on forwarded user credentials for the DAG. No key generation or installation authorized/performed.

### Thin transfer preparation after root-key installation

User requested continuing after [approved key installation](2026-10-13-nomad-test-devops-894-backup-share-root-key.md). Read-only root→root destination check confirms `/data/elastic/thin/` is empty and239.48GiBfree; source `elasticsearch_smalldb_1` running. `rsync -aH --numeric-ids --dry-run --delete --exclude=java_pid1.hprof` succeeded:3971entries,3872regularfiles,120572815bytes (~121MB),0deletions. Source is live during dry-run, so these are transfer estimates, not consistency evidence.

Prepared reviewable operation `~/ai-data/nomad-es-vk-transfer/transfer.py`, outside repository, with CLIthin/thick and defaultdry-run. It verifies empty destination, correct running source data mount, key-only root SSH, source-size/free-space margin. `--apply` performs stop→copy→checksum/metadata dry-run verification→source restart in `finally`, with bounded timeouts. Nothing executes apply without explicit argument. Source root key remains on backup and destination host key is pinned transiently; no known_hosts persistence needed for this operation.

Actual helper dry-run on backup exited0. Local syntax/help checks passed; three mocked failure/success checks passed: dry-run performs no stop/copy/start; successful apply checksums and restarts; failed copy restarts source. These checks do not prove a real transfer or target ES startup. Only thin apply is proposed next, as one reviewed transfer operation; user approval still needed under remote-mutation rules. The reviewed invocation is `ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=10 -o StrictHostKeyChecking=yes root@172.24.0.19 python3 - thin --apply < ~/ai-data/nomad-es-vk-transfer/transfer.py`. No source stop, write transfer or target service run performed yet. Thick is separate future action.

## Risks and limits

No document data accessed/copied, no transfer authorization inferred from the screenshot or date waiver. Capacity planning must include working space and growth; allocated directory bytes are not the final requested disk size. Freshness checking intentionally omitted per user. No permission to omit consistency or restored-data checks inferred.

## Portable lesson

none
