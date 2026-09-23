---
system: workstation
status: verified
checked: 2026-09-08
tags: [apt, debian, ubuntu, gpg, dotnet, bullseye, vscode, google-chrome, gitlab]
---
# Local APT repositories

## 2026-09-08: Debian 11 Bullseye Security expired in the .NET 6 image

Context: Docker host `gitlab-runner-docker-2`, image
`mcr.microsoft.com/dotnet/aspnet:6.0` (digest
`sha256:e70c493f8af7f95bf459cb2b15c7e7a6173228929c2b7a9a6836b19377890e78`).
Inside the container `apt update` reported that
`bullseye-security/InRelease` had expired about 13.5 hours ago.

A check on 2026-09-08 showed that the public
`http://deb.debian.org/debian-security/dists/bullseye-security/InRelease`
contains:

```text
Date: Mon, 31 Aug 2026 21:13:04 UTC
Valid-Until: Mon, 07 Sep 2026 21:13:04 UTC
```

UTC at the time of the check: `2026-09-08 10:45`. The error matches the
expiry of `Valid-Until` exactly, so it is not a sign of a wrong clock on the host.
The official Debian 11 LTS period: `2024-08-15` to `2026-08-31`; the repository
stopped refreshing its metadata after LTS ended. In addition, .NET 6 reached
Microsoft end of support on 2024-11-12.

Verified: the main `bullseye` suite is still available on `deb.debian.org`, but the security
suite has already expired; `archive.debian.org/debian-security/dists/
bullseye-security/InRelease` returned HTTP 404 on the date of the check.

Recommended solution: rebuild the application on a supported .NET version and
use a supported base image (for a new long-lived migration, .NET 10 LTS). If
the migration is temporarily impossible, only the expired `bullseye-security`
line can be disabled, accepting the absence of security updates.
`Acquire::Check-Valid-Until=false` is acceptable only as a short emergency workaround:
it hides the freshness check and does not bring back security updates.

A check of the MCR tag list on 2026-09-08 confirmed a fresher interim base
image on Debian 12: `mcr.microsoft.com/dotnet/aspnet:6.0-bookworm-slim` and
the pinned last runtime
`mcr.microsoft.com/dotnet/aspnet:6.0.36-bookworm-slim`. This removes the
dependency on Bullseye, whose LTS has ended, without an immediate application retarget,
but does not bring back support for .NET 6 itself.

Diagnostic commands:

```bash
date -u
curl -fsSL http://deb.debian.org/debian-security/dists/bullseye-security/InRelease \
  | sed -n '1,12p'
grep -R --line-number bullseye-security /etc/apt/sources.list /etc/apt/sources.list.d
```

Status: cause confirmed; host/container configuration was not changed.

Portable lesson: `~/ai/general/knowledge/linux/apt-release-file-expired-after-debian-lts-end.md`.

## 2026-08-20: Google Chrome key and disabling GitLab

Context: local Ubuntu focal. `apt update` could not verify Google Chrome
because of the missing key `FD533C07C264648F`; the key of the GitLab CE and
EE repositories `3F01618A51312F3F` had expired.

Sources checked:

- `/etc/apt/sources.list.d/google-chrome.list`: Google Chrome;
- `/etc/apt/sources.list.d/gitlab_gitlab-ce.list`: GitLab CE;
- `/etc/apt/sources.list.d/gitlab_gitlab-ee.list`: GitLab EE.

The script
`~/ai/current/scripts/fix-apt-google-disable-gitlab.sh` was prepared. It downloads the official
Google key, checks for the presence of the full fingerprint
`0E225917414670F4442C250DFD533C07C264648F`, installs the keyring to
`/usr/share/keyrings/google-chrome.gpg`, switches the Chrome source to HTTPS with an
explicit `signed-by`, renames both GitLab source files to `.disabled` and
runs `apt-get update`.

State: **the fix was applied and confirmed by the user on 2026-08-20**.
The command used to apply it:

```bash
sudo bash ~/ai/current/scripts/fix-apt-google-disable-gitlab.sh
```

GitLab rollback: return the `.list` suffix to both `.list.disabled` files, then
run `sudo apt-get update`.

## 2026-08-20: Visual Studio Code

Verified locally: VS Code is installed as the Debian package `code` version
`1.92.2-1723660989` (`/usr/bin/code`), but the source
`https://packages.microsoft.com/repos/code` is absent from APT. Therefore the package
is not updated through a normal `apt upgrade`.

Recommended way to restore updates: install the official Microsoft key
into a separate keyring, create `vscode.sources` with an explicit `Signed-By`, run
`apt update` and `apt install code`. After that the package is updated normally
through APT.

After the repository was connected, the package also created
`/etc/apt/sources.list.d/vscode.list`, so APT reported a duplicate with
`vscode.sources`. Verified: both files point to the same repository; the update
candidate is `1.134.0-1787078834`, the installed version is still `1.92.2`.
Solution: comment out the `deb` line in the automatically created
`vscode.list`, keep `vscode.sources` with its separate `Signed-By`, then
repeat `apt update` and `apt install code`.

Result: **the update was confirmed by the user on 2026-08-20**. VS Code
`1.134.0` for `x64` (commit `110a328ea54b42367b803ec53ee0bf52ef26b419`) is installed.
