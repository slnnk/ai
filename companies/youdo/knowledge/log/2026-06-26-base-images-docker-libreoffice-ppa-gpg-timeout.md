---
system: base-images
status: hypothesis
checked: 2026-06-26
tags: [base-images, docker, libreoffice, ppa, gpg, add-apt-repository, keyserver]
---
# base-images: LibreOffice PPA GPG timeout

Date: 2026-06-26

## Context

Repository `/home/slnnk/git/base-images`, Docker image `microsoft/aspnet/6.0-focal-libreoffice`, build command `docker build -t test -f microsoft/aspnet/6.0-focal-libreoffice/Dockerfile .`.

## Task

Build fails in the single `RUN` layer during `add-apt-repository ppa:libreoffice/ppa` with:

`Error: retrieving gpg key timed out.`

The PPA page is reachable enough for `add-apt-repository` to print the LibreOffice PPA description, but key retrieval from the Ubuntu keyserver path times out.

## Findings

- The Dockerfile installs `software-properties-common`, then calls `add-apt-repository ppa:libreoffice/ppa`, then installs `libreoffice`.
- Similar PPA usage exists in:
  - `libreoffice/6.0-focal/Dockerfile`
  - `microsoft/dotnet-sdk/6.0-focal-libreoffice/Dockerfile`
  - `microsoft/aspnet/8.0-libreoffice/Dockerfile`
- The failure is not from apt package resolution yet; it happens before the second `apt-get update`.

Likely cause (hypothesis): network/firewall/proxy path from Docker build environment to the keyserver used by `add-apt-repository` is blocked or too slow. Common workaround is to avoid the implicit key retrieval path and add the repository/key explicitly, usually via keyserver on port 80 or via Launchpad key URL, then use `signed-by`.

## Open items

Next steps:

- Replace `add-apt-repository` with explicit key + deb source setup for reproducible Docker builds.
- Prefer `signed-by=/usr/share/keyrings/libreoffice-ppa.gpg` instead of global `apt-key`.
- Consider pinning LibreOffice version or using Ubuntu archive package if bleeding-edge PPA is not required.

## Portable lesson

[`~/ai/general/knowledge/docker/add-apt-repository-gpg-key-timeout.md`](../../../../general/knowledge/docker/add-apt-repository-gpg-key-timeout.md)
