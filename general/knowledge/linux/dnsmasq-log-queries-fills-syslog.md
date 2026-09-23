---
system: linux
status: verified
checked: 2026-09-22
tags: [dnsmasq, syslog, rsyslog, logrotate, disk-full, journald]
---
# dnsmasq `log-queries` fills syslog and the root filesystem

## Symptom

Root filesystem at `100%` on a container host; inodes fine. `docker system df` shows little
reclaimable space, `/var/lib/<orchestrator>` has no large files, but `/var/log` holds
several GB: an uncompressed `syslog.1` of 3-4 GiB, a current `syslog` growing by hundreds
of MB per day, and a journal of 1-2 GB. Sampling the log shows almost every line comes from
one program:

```bash
tail -n 50000 /var/log/syslog | awk '{print $5}' | cut -d'[' -f1 | sort | uniq -c | sort -rn | head
# 49966 dnsmasq
```

with lines like `query[A] foo.service.consul from 172.17.0.5` and
`forwarded foo.service.consul to 127.0.0.1#8600`. The last line of the current file may
be truncated (write failed on a full disk).

## Cause

`log-queries` is enabled in `/etc/dnsmasq.conf`. On a host where every container resolves
service names through the local dnsmasq (service-discovery forwarders, health checks,
retry loops), this is tens of thousands of lines per minute, all going to syslog. Weekly
logrotate with several uncompressed rotations keeps a week of that volume on disk; nothing
size-based triggers earlier. journald duplicates part of the stream.

## Fix

Immediate space recovery (in order of least operational impact):

1. Truncate or remove the already-rotated file: `: > /var/log/syslog.1` (copy it off the
   host first if the history matters). Frees the biggest chunk instantly.
2. `journalctl --vacuum-size=300M` to shrink the journal.
3. Only then consider `docker image prune` for unused images; check the candidate list, and
   never treat containers with data inside their writable layer (databases without a
   volume) as garbage.
4. With space back, `logrotate -f /etc/logrotate.d/rsyslog` to compress the current file.

Prevent recurrence:

- Remove `log-queries` from `/etc/dnsmasq.conf` (or keep it only for debugging), then
  `systemctl restart dnsmasq`. If query logging is required, send it to its own file
  (`log-facility=/var/log/dnsmasq.log`) with a size-based logrotate rule:

  ```text
  /var/log/dnsmasq.log {
      size 200M
      rotate 3
      compress
      delaycompress
      missingok
      notifempty
      postrotate
          systemctl kill -s HUP dnsmasq.service
      endscript
  }
  ```

- Add `maxsize` (or `size`) to the rsyslog rotate rule instead of relying on `weekly`.
- Alert on filesystem usage before 100%.
- Do not "fix" this with `tune2fs -m 0`: the ext4 reserve gives back a few GiB once and
  does nothing about the growth.

## Limits

- Debian/Ubuntu layout (`/var/log/syslog`, rsyslog + logrotate weekly, 4 rotations).
  On journald-only systems the same growth shows up in `journalctl --disk-usage`.
- `lsof +L1` on such hosts lists huge deleted `memfd:` files from .NET runtimes; these are
  sparse tmpfs mappings and are not the cause of an ext4 full disk.
- Diagnosis was read-only: `df -h`, `df -i`, `docker system df`, `journalctl --disk-usage`,
  `find /var -xdev -size +100M`, `tune2fs -l`.
