---
system: gitlab
status: verified
checked: 2026-10-12
tags: [base-images, debian, nomad, registry]
---
# Base image diagnosis: Bullseye archive and Nomad download stall

## Summary

Three image failures use Debian Bullseye security packages removed from regular security pool URLs but available in the archive. Nomad job 3218387 stalls after APT, at a silent wget download from the Yandex HashiCorp mirror; independent mirror probes time out, while official HashiCorp ZIP downloads respond.

## Task and context

The user requested investigation of the Debian version and [Nomad job 3218387](https://gitlab.youdo.sg/sysadmins/nomad/-/jobs/3218387). Related [five selected image builds](2026-10-12-gitlab-base-images-selected-retries.md).

## Actions and findings

Read exact tagged Dockerfiles, CI traces and public Debian metadata. Debian confirms Bullseye LTS ended 2026-08-31: https://www.debian.org/News/2026/20260831 . All three failed jobs fetch Bullseye packages. Successful dotnet-aspnet/6.0 uses sdk/aspnet `6.0-bookworm-slim`; failing aspnet/6.0 uses unqualified `6.0` images. Those Dockerfiles otherwise match apart from BOM. .NET 5 explicitly uses `5.0-bullseye-slim`; Cake parent `cakebuild/cake:sdk-6.0` also fetches Bullseye packages.

A failed `ucf_3.0043+deb11u2_all.deb` URL returns 404 on both `deb.debian.org/debian-security` and `security.debian.org/debian-security`; the identical archive path returns 200. Archive requests for failed curl, dirmngr and libexpat1 packages return 206 with valid Debian archive magic. `archive.debian.org/debian-security/dists/bullseye-security/InRelease` returns 200, dated 2026-09-12 with no Valid-Until. Ordinary mirror InRelease remains accessible, so this is not simply an unavailable Release file. `archive.debian.org/debian/dists/bullseye-updates/Release` also returns 200 today; the older generic claim that updates never exist in archive does not apply universally. No package install or rebuilt image has yet validated a complete archive fix.

Nomad project ID171, original pipeline108219/master, commit `1affea3a2740cd3d2f12412b06216c718ce3a73a`, runner docker-1. Dockerfile uses Ubuntu22.04, Nomad1.5.3 and Levant0.3.3. APT/certificate hooks finish at build elapsed16.05s; next command is `wget ${NOMAD_RELEASE} -O /nomad.zip -o /dev/null`. No explicit timeout/retry limit; wget hides diagnostics. Job remained running at duration217s with the same tail. Independent ranged GETs for both Yandex mirror archives time out after18s; official `releases.hashicorp.com` archives return206 with ZIP magic. This supports a mirror download stall; no runner process inspection was performed.

## Candidate changes and limits

For aspnet/6.0, use the demonstrated Bookworm FROM variants. For .NET5/Cake legacy images, switch the affected Debian security sources to the verified archive before APT update and validate a complete build; later Cake Mono/keyserver steps may independently fail. For Nomad, replace both Yandex mirror URLs with verified official HashiCorp URLs and make download progress/errors visible with bounded retries/timeouts. These are proposals only: no branch changes, repository edits, job cancellation/retry, or external mutations. Live actions remain in `~/ai/TODO.md`.

## Changed files and evidence

This log, GitLab map, shared backlog and generic Debian recipe. Read-only probes/scripts, sanitized traces and result JSON live under `/home/slnnk/ai-data/gitlab-recovery/`: `bullseye-diagnosis-20261012.json`, `nomad-and-archive-probes-20261012.json`, `trace-3218387.txt`. Credentials stayed in process memory.
