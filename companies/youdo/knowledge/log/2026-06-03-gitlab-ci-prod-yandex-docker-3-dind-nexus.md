---
system: gitlab-ci
status: verified
checked: 2026-06-03
tags: [gitlab-runner, dind, nexus, insecure-registry, s3-cache, docker-cleanup, overlay2, cpu-sizing, prod_yandex]
---
# 2026-06-03: prod_yandex gitlab-runner-docker-3 dind/Nexus

## Task

Investigate why jobs on the new `prod_yandex` Docker runner `gitlab-runner-docker-3` fail to start
the `docker:dind` service and to log in to Nexus, then fix the runner configuration (Ansible
host_vars and live config), S3 cache credentials, Docker cleanup, and assess build slowness
compared with the old runner.

## Context

- Host: `gitlab-runner-docker-3`, IP `10.16.24.173`, SSH as `root` via local key.
- Inventory area: `/home/slnnk/git/automation-services/inventories/prod_yandex/host_vars/gitlab-runner-docker-3.yml`.
- Role area: `/home/slnnk/git/automation-services/roles/gitlab-runner`.
- GitLab Runner on host: `17.9.3`.

## Symptoms

- GitLab job starts `registry.youdo.sg/youdo/base-images/docker:dind`.
- Service healthcheck warns: `FATAL: No HOST or PORT found`.
- Job fails on `docker login $NEXUS_ADDR` when `NEXUS_ADDR` resolves to `msk3-nexus.youdo.corp` without port: `10.16.24.23:443 connection refused`.
- `after_script` cannot connect to Docker daemon at `tcp://docker:2375`.

## Findings

- `msk3-nexus.youdo.corp` resolves from runner to `10.16.24.23`.
- From `gitlab-runner-docker-3`: TCP `10.16.24.23:443` is refused; TCP `10.16.24.23:3000` is reachable.
- Runner config contains `HEALTHCHECK_TCP_PORT=2375`, but GitLab service wait still reports no host/port.
- Runner config mounts `/data/daemon.json:/etc/docker/daemon.json:ro` into job containers.
- `/data/daemon.json` already defines `insecure-registries` for `msk3-nexus.youdo.corp`, `:3000`, `:3003`, and `10.16.24.0/24`, plus DNS `172.28.0.8/9`.
- The same runner sections also pass `command: ["--insecure-registry=..."]`.
- Manual dind run with both `/data/daemon.json` and duplicate `--insecure-registry` flags fails with Docker daemon config conflict.
- Manual dind run with `/data/daemon.json` and without duplicate flags succeeds; `2375` becomes reachable after about 15 seconds.

## Recommended Fix

- Remove duplicate `runners.docker.command` `--insecure-registry` entries from `gitlab-runner-docker-3` runner sections and rely on `/data/daemon.json` as the single source of dind registry/DNS config.
- Apply the same cleanup to other docker runner host_vars that mount `/data/daemon.json` and also pass the same insecure-registry flags.
- Fix CI variables or project config so Nexus Docker login uses the reachable registry endpoint, likely `msk3-nexus.youdo.corp:3000` or the proper HTTPS endpoint if one exists; bare `msk3-nexus.youdo.corp` attempts `443`, which is closed from this subnet.
- Re-run `gitlab-runners.yml` for the affected host, restart runner if needed, then run a job that uses dind and validates `docker info` plus `docker login` to the intended Nexus endpoint.

## Actions and changes

### 2026-06-03 Follow-up

- Applied the duplicate `runners.docker.command` cleanup in `inventories/prod_yandex/host_vars` for active runner definitions:
  `gitlab-runner1.yml` through `gitlab-runner6.yml`, `gitlab-runner-android.yml`,
  `gitlab-runner-ds.yml`, and `gitlab-runner-docker-1.yml` through `gitlab-runner-docker-3.yml`.
- Active `--insecure-registry` command entries are removed; only commented examples remain in `gitlab-runner1..6`.
- YAML parsing was checked locally for all `inventories/prod_yandex/host_vars/gitlab-runner*.yml`.

### 2026-06-03 HTTP Nexus Follow-up

- Verified from `gitlab-runner-docker-3` that internal Nexus responds on HTTP:
  `http://msk3-nexus.youdo.corp/v2/`, `http://msk3-nexus.youdo.corp:3000/v2/`,
  and `http://msk3-nexus.youdo.corp:3003/v2/` return `401`.
- Verified that `https://msk3-nexus.youdo.corp/v2/` fails because port `443` is closed.
- `NEXUS_ADDR` is managed on the CI side, not in Ansible runner host_vars.
- A temporary attempt to add `NEXUS_ADDR=http://msk3-nexus.youdo.corp` to runner host_vars was reverted.
- At this point the existing prod_yandex host_vars files are untracked in the local git worktree; old
  `gitlab-runner1..6.yml` are deleted in the worktree.

### 2026-06-03 Live Runner Cleanup

- On `gitlab-runner-docker-3`, removed stale `command = ["--insecure-registry=..."]` lines directly from
  `/etc/gitlab-runner/config.toml`.
- Backup created on the host:
  `/etc/gitlab-runner/config.toml.codex-backup-20260603141951`.
- `gitlab-runner verify --config /etc/gitlab-runner/config.toml` reported all three runners alive.
- Restarted `gitlab-runner`; service status became `active`.
- Re-tested dind manually with `/data/daemon.json`; `2375` became reachable after about 15 seconds.
- `docker info` inside dind shows internal Nexus in `Insecure Registries`.
- `docker login msk3-nexus.youdo.corp` with invalid credentials now reaches
  `http://msk3-nexus.youdo.corp/v2/` and returns expected authentication failure.

### 2026-06-03 S3 Cache Check

- Checked S3 cache access from `gitlab-runner-docker-3` using credentials from
  `/etc/gitlab-runner/config.toml`, without printing secrets.
- There are two unique S3 cache credential sets on the host.
- The credential used by runner sections `gitlab-runner-docker-3` and
  `gitlab-runner-docker-3 autotests03` returned `403` for bucket list and `403` for test object upload.
- The credential used by `gitlab-runner-docker-3 b2b` successfully completed test object
  `PUT`, `GET`, and `DELETE` against bucket `youdo-gitlab-runner`.
- The original cache restore `403 Forbidden` is consistent with the first credential lacking required
  access to the bucket/path, despite the credential being present in config.

### 2026-06-03 Old Runner Comparison

- Checked old working runner `root@172.28.0.171`, hostname `gitlab-runner-docker-1`.
- GitLab Runner version is also `17.9.3`.
- The old runner has one unique S3 cache credential set, matching the working credential used by
  `gitlab-runner-docker-3 b2b`.
- S3 cache test from old runner succeeded: bucket list `200`, test object `PUT` `200`,
  `GET` `200` with body match, and `DELETE` `204`.
- Old runner still has stale `command = ["--insecure-registry=..."]` entries in live config, but its
  `/data/daemon.json` does not include `10.16.24.0/24`; it includes named Nexus registries only.

### 2026-06-03 S3 Credential Fix

- Updated `inventories/prod_yandex/host_vars/gitlab-runner-docker-3.yml` so the main
  `gitlab-runner-docker-3` section and `autotests03` use the same working S3 cache credential set as `b2b`.
- Manually updated `/etc/gitlab-runner/config.toml` on `gitlab-runner-docker-3` because applying the role is slow.
- Backups created during the manual update:
  `/etc/gitlab-runner/config.toml.codex-backup-credentials-20260603143058`,
  `/etc/gitlab-runner/config.toml.codex-backup-credentials-fixed-20260603143214`,
  and `/etc/gitlab-runner/config.toml.codex-backup-s3-working-20260603143244`.
- A first manual replacement attempt produced invalid TOML; the file was restored from backup before the final successful replacement.
- Restarted `gitlab-runner`; `gitlab-runner verify` reported all three runner sections alive and service status is `active`.
- Re-tested S3 cache access from current live config: there is now one unique credential set, and bucket list,
  test object `PUT`, `GET`, and `DELETE` all succeeded.

### 2026-06-03 Runner Performance Check

- Checked `gitlab-runner-docker-3` during active builds.
- Host has 4 vCPU and 15 GiB RAM; GitLab Runner global `concurrent = 4`.
- Load average was high (`24.52`, `21.58`, `14.32`), while `vmstat` showed CPU user time around
  `82-90%` and I/O wait around `0%` during sampling.
- Top CPU consumers were `.NET`/MSBuild/Roslyn processes inside Docker builds; one StaticWebAssets process
  was using about `290%` CPU by itself.
- Active dind containers were each using about one full CPU and writing multiple GiB during builds.
- `/data` was 76% full (`132G` used of `183G`), not yet full; inode usage was 35%.
- Docker storage had large cache volumes: `/data/docker/volumes` about `28G`.
- `/data/containerd` has many files (`~1.33M`) and overlay snapshots (`1435`); `docker system df -v` and
  broad `du` scans were slow/hung, indicating expensive Docker/containerd metadata traversal.
- `/etc/cron.d/dockerclean` is invalid because it has no newline before EOF; syslog shows:
  `(*system*dockerclean) ERROR (Missing newline before EOF, this crontab file will be ignored)`.
- Because the cron file is ignored, scheduled Docker `container/image/volume prune` is not running.
- Current conclusion: immediate build slowness is primarily CPU overcommit from running up to 4 parallel
  .NET/Docker builds on 4 vCPU; Docker/containerd file buildup and disabled cleanup are secondary issues.

### 2026-06-03 Old Runner Performance Comparison

- Checked old runner `root@172.28.0.173`, hostname `gitlab-runner-docker-3`.
- Old runner also has 4 vCPU and 15 GiB RAM, GitLab Runner `17.9.3`, and `concurrent = 4`.
- At check time the old runner was idle: load average `0.00`, no active Docker containers.
- Old runner Docker storage is clean: `/data/docker` about `20M`, Docker images `0`, containers `0`,
  volumes `0`, `/data` 27% used.
- Old runner uses Docker `overlay2`; new runner reports Docker driver `overlayfs`.
- Old runner Docker stack: Docker `28.3.0`, containerd `1.7.27`, classic `overlay2`.
- New runner Docker stack: Docker `29.5.2`, containerd `2.2.4`, containerd snapshotter `overlayfs`.
- During test builds on the old runner, load also jumped high and `vmstat` showed I/O wait up to about `38%`
  during pull/unpack, but the old runner started from a clean Docker storage state.
- Old runner `/etc/cron.d/dockerclean` is valid and syslog shows hourly Docker prune commands running.
- New runner has invalid `dockerclean` cron due to missing final newline; cleanup is ignored.
- Comparison reinforces that the new runner's slowness is a combination of active CPU-heavy load plus
  accumulated Docker/containerd metadata because cleanup is not running, not simply a permanent disk I/O limit.

### 2026-06-03 Docker Cleanup Fix

- Fixed `roles/gitlab-runner/templates/cron-docker-clean.j2` by adding the required final newline.
- Manually fixed `/etc/cron.d/dockerclean` on live `gitlab-runner-docker-3` (`10.16.24.173`) and restarted `cron`.
- Verified live cron file is now valid and `cron` is `active`.
- Ran the same cleanup commands that are configured in cron:
  - `/usr/bin/docker container prune --force`: reclaimed `0B`.
  - `/usr/bin/docker image prune -a --force`: reclaimed `3.97GB`.
  - `/usr/bin/docker volume prune -a --force`: reclaimed `22.09GB`.
- `/data` improved from `111G` used / `62G` free (`65%`) to `70G` used / `104G` free (`41%`).
- After cleanup there are no Docker containers, images, or local volumes on the host.
- Remaining Docker storage issue: `docker system df` still reports `924` build cache entries using `71.44GB`,
  all reclaimable. The current cron does not prune build cache.

### 2026-06-03 Runtime Overlay2 Test

- User requested a manual runtime-only test on `gitlab-runner-docker-3` (`10.16.24.173`), without changing Ansible.
- Before change, Docker reported `Storage=overlayfs` with `driver-type=io.containerd.snapshotter.v1`.
- Backed up live daemon configs:
  - `/etc/docker/daemon.json.codex-backup-overlay2-20260603170500`
  - `/data/daemon.json.codex-backup-overlay2-20260603170500`
- Stopped `gitlab-runner` and `docker`.
- Added to live Docker daemon config:
  - `"storage-driver": "overlay2"`
  - `"features": {"containerd-snapshotter": false}`
- Moved previous Docker/containerd state aside for rollback instead of deleting it:
  - `/data/docker.codex-before-overlay2-20260603170500`
  - `/data/containerd.codex-before-overlay2-20260603170500`
- Started Docker and GitLab Runner again.
- Verified Docker now reports `Storage=overlay2`, `Backing Filesystem=extfs`, `Native Overlay Diff=true`,
  root `/data/docker`.
- `gitlab-runner verify` reports all three runner sections alive; `docker` and `gitlab-runner` services are `active`.
- New active Docker storage is empty: `docker system df` shows `0B` images, containers, volumes, and build cache.
- `/data` after the switch: `77G` used, `97G` free, `45%`.

### 2026-06-03 Post-Overlay2 Slowness Check

- User reported that switching the live Docker daemon to `overlay2` did not improve build time.
- Checked `gitlab-runner-docker-3` during/after a slow project `547` build batch.
- Disk did not look like the active bottleneck at sampling time: `vmstat` showed `wa=0`, free memory was about `7G`,
  and Docker was already on `overlay2`.
- The heavy process was `.NET publish`, especially `Microsoft.NET.Sdk.StaticWebAssets.Tool.dll`, using more than two CPU cores.
- Four project `547` jobs were accepted almost simultaneously with `concurrent = 4`.
- Their durations on the new runner were about `421s`, `431s`, `435s`, and `506s`.
- Compared CPU topology with old runner `172.28.0.173`:
  - New runner: `Intel Xeon Processor (Icelake)`, `2` cores x `2` threads = `4` vCPU, BogoMIPS `4000`.
  - Old runner: `Intel Xeon Gold 6336Y`, `4` single-thread vCPU presented as `2` sockets x `2` cores, BogoMIPS `4788`.
- Old runner project `547` examples in the last hour were about `219s`, `264s`, `268s`, `341s`, and `135s`.
- Working hypothesis after overlay2 test: the main remaining difference is CPU capacity/topology, not Docker storage.
  The new host runs up to four CPU-heavy .NET jobs on two physical cores with SMT.
- For a runtime-only test, changed live `/etc/gitlab-runner/config.toml` on `10.16.24.173` from `concurrent = 4`
  to `concurrent = 2`.
- Backup created: `/etc/gitlab-runner/config.toml.codex-backup-concurrent2-20260603171524`.
- Reloaded GitLab Runner with `SIGHUP`; logs show `max_builds=2`.
- `gitlab-runner verify` reports all three runner sections alive.

### 2026-06-03 CPU Details: New vs Old Runner

- New runner `10.16.24.173`:
  - CPU model exposed to guest: `Intel Xeon Processor (Icelake)`.
  - `4` logical CPUs as `1` socket x `2` cores x `2` threads per core.
  - Reported `/proc/cpuinfo` frequency: `2000.000 MHz`.
  - BogoMIPS: `4000.00`.
  - L1d: `128 KiB (4 instances)`.
  - L1i: `128 KiB (4 instances)`.
  - L2: `8 MiB (2 instances)`, effectively `4 MiB` per physical core.
  - L3: `16 MiB (1 instance)`.
- Old runner `172.28.0.173`:
  - CPU model exposed to guest: `Intel(R) Xeon(R) Gold 6336Y CPU @ 2.40GHz`.
  - `4` logical CPUs as `2` sockets x `2` cores x `1` thread per core.
  - Reported `/proc/cpuinfo` frequency: `2394.374 MHz`.
  - BogoMIPS: `4788.74`.
  - L1d: `128 KiB (4 instances)`.
  - L1i: `128 KiB (4 instances)`.
  - L2: `16 MiB (4 instances)`, effectively `4 MiB` per vCPU/core.
  - L3: `32 MiB (2 instances)`, effectively `16 MiB` per socket.
- Practical interpretation: the old runner has four full exposed cores at about `2.4 GHz`, while the new
  runner has two cores with SMT at about `2.0 GHz`. For CPU-bound .NET builds this is a material difference.

## Open items

- Build cache (`924` entries, `71.44GB`) is not pruned by the current cron; decide whether to add `docker builder prune` to the cleanup.
- The `concurrent = 2` and `overlay2` changes on `10.16.24.173` are live runtime-only changes not reflected in Ansible; either persist them in host_vars or roll back from the backups listed above.
- Host_vars files in `inventories/prod_yandex/host_vars` are untracked in the local worktree and old `gitlab-runner1..6.yml` are deleted there; the working tree needs review before commit.

## Security Note

- Do not store runner tokens, S3 keys, registry auth values, or Nexus credentials in this note.

## Portable lesson

- [Docker dind fails to start when daemon.json and command-line flags set the same option](../../../../general/knowledge/docker/dind-daemon-json-and-cli-flag-conflict.md)
- [A /etc/cron.d file without a trailing newline is silently ignored](../../../../general/knowledge/linux/cron-d-file-ignored-missing-newline.md)
