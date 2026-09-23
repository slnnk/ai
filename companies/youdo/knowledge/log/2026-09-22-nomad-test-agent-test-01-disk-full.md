---
system: nomad-test
status: verified
checked: 2026-09-22
tags: [incident, disk-full, dnsmasq, syslog, logrotate, docker, mssql, nomad-agent-test-01]
---
# nomad-agent-test-01: root disk full

Check date: 2026-09-22 16:38-16:44 MSK.

## Task

Find what filled the root filesystem of Nomad client `nomad-agent-test-01` to 100% and what
can be cleaned safely.

## Context

- Host: `nomad-agent-test-01`, SSH `root@10.16.26.62`.
- Role: Nomad client of the test cluster; Docker allocations run on the host.
- The check was read-only. No files, Docker objects or journals were deleted; configuration and services were not changed.

## Findings

### State

- Root ext4 `/dev/vda2`: 92 GiB, 89 GiB used, 0 available, `100%`.
- Inodes are not the cause: about 1.09 million of 6.09 million used (`18%`).
- ext4 reserved blocks: 988158 blocks of 4096 bytes, about 3.77 GiB. This is the filesystem reserve, not the first candidate for change.
- Docker: 301 containers (250 running), 185 images, 9 volumes.
  - Images: 56.5 GB, Docker estimates reclaimable at 5.402 GB.
  - Containers: 11.81 GB, reclaimable only 3.782 MB.
  - Volumes: 233.1 KB, reclaimable 0.
- `/var/log`: 5.3 GB.
  - `/var/log/syslog.1`: 3.7 GiB (about 3.94 GB), rotation date 2026-09-20 00:00.
  - `/var/log/syslog`: 636 MiB at the time of the check.
  - systemd journal: 1.6 GB.
  - Docker JSON logs: the largest about 75 MB, the rest of the top values about 8-10 MB; this is not the main source.
- APT cache, `/var/crash`, `/var/tmp` and `/tmp` are practically empty.
- No regular files larger than 100 MB were found in `/var/lib/nomad`. The large number of allocation secret tmpfs and Docker overlay mounts makes the overall `df`/`du /` noisy.
- `lsof +L1` showed numerous deleted `memfd:doublemapper` entries of dotnet with a logical size of 2 TiB on tmpfs; these are sparse/memfd and do not explain the filling of ext4.

### Cause of the log growth

- `log-queries` is enabled at `/etc/dnsmasq.conf:671`.
- In a sample of the last 50 thousand lines of the current syslog, 49,966 lines were produced by `dnsmasq`; in `syslog.1` — 49,703 of 50 thousand.
- The current syslog contains a stream of `query[...]` and `forwarded ... to 127.0.0.1#8600` for Consul DNS.
- `logrotate.timer` is active; the run of `logrotate.service` on 2026-09-22 00:00 completed successfully. rsyslog is configured to keep four rotations. A week's worth of DNS query logging leaves a large uncompressed `syslog.1`.
- The last line of the current syslog was truncated; this is consistent with a write error on a full disk, but was not separately confirmed through rsyslog errors.

### What can be cleaned

Order from the most targeted to the most operationally impactful:

1. Delete or truncate the closed `/var/log/syslog.1`: frees about 3.7 GiB immediately, but destroys the syslog history of the previous period. If needed, save it off the node before acting.
2. Shrink the journal, for example to 300-500 MB: potentially frees about 1.1-1.3 GB, losing old journal history.
3. Delete Docker images not used by containers: Docker's estimate is about 5.4 GB. Risk — subsequent image pulls and dependency on registry/network; active containers should not be deleted, but a review of the candidate list is preferable first.
4. Once free space is available, force-rotate/compress the current syslog if additional savings are needed.

### Largest containers

Additional check on 2026-09-22:

- Largest writable layer: container `mssql-11849fc9-bafd-e004-951a-dac8550bf609`, ID `597a0dff80b5`, Nomad allocation `11849fc9-bafd-e004-951a-dac8550bf609`, job `mssql-test13`, task `mssql`.
- The container is active (`Up 8 days`), writable layer `2,762,435,338` bytes, about 2.76 GB. The virtual/rootfs size of about 6.03 GB includes the image and is not entirely unique consumption of this container.
- Inside, `/var/opt/mssql` occupies about 2.6 GiB, practically all of it in `/var/opt/mssql/data`; the MSSQL log directory is about 47 MiB, the Docker JSON log about 1.1 MB.
- `/var/opt/mssql` is not moved out to a Docker volume/bind mount. The available Nomad bind mounts relate only to `/alloc`, `/local` and `/secrets`. Deleting the container/alloc will delete the data of this database, so it cannot be treated as safe garbage.
- Next container: `mssql-0dbae57d-eec2-6952-ae54-497e1ba36521`, writable layer about 1.32 GB. Then come application containers from about 516 MB and smaller.

## Open items: preventing recurrence

- Remove `log-queries` from dnsmasq or direct the DNS query logs to a separate file with size-based rotation and short retention. The change requires agreement and a reload/restart of dnsmasq.
- Add a size-based threshold for syslog instead of relying only on weekly rotation.
- Check alerting on filesystem usage before it reaches 100%.
- Do not use a change of the ext4 reserved percentage as the main solution: it only gives back a few GiB of reserve and does not stop the growth of DNS logs.

## Actions: checks used

- `df -h /`, `df -i /`
- `docker system df`, counting containers/images/volumes
- `journalctl --disk-usage`
- `find` for large files in `/var`, `/var/log`, Docker container logs and `/var/lib/nomad`
- `head`/`tail` samples and aggregation of the program field in syslog
- `systemctl status logrotate.service`, check of `logrotate.timer`
- `tune2fs -l /dev/vda2`

## Portable lesson

[dnsmasq `log-queries` fills syslog and the root disk](../../../../general/knowledge/linux/dnsmasq-log-queries-fills-syslog.md)
