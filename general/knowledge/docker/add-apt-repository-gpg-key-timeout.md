---
system: docker
status: hypothesis
checked: 2026-06-26
tags: [apt, ppa, gpg, add-apt-repository, keyserver, signed-by, ubuntu, libreoffice]
---
# `add-apt-repository ppa:...` fails with "retrieving gpg key timed out" in a Docker build

## Symptom

An Ubuntu-based Dockerfile step

```dockerfile
RUN apt-get update && apt-get install -y software-properties-common \
 && add-apt-repository ppa:libreoffice/ppa \
 && apt-get update && apt-get install -y libreoffice
```

prints the PPA description (so Launchpad itself is reachable) and then stops with

```text
Error: retrieving gpg key timed out.
```

before the second `apt-get update` runs.

## Cause

`add-apt-repository` fetches the signing key from `keyserver.ubuntu.com` over HKPS (443)
using GnuPG's dirmngr. Build environments behind a corporate firewall/proxy, or with broken
IPv6, frequently cannot complete that path even though plain HTTPS to Launchpad works; dirmngr
has no proxy awareness unless configured and gives up after a fixed timeout. The result is a
non-reproducible build that depends on network conditions at build time.

## Fix

Stop depending on the implicit keyserver path. Fetch the key from Launchpad over HTTPS
(regular proxy rules apply) and register the repository with `signed-by`:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
 && curl -fsSL "https://api.launchpad.net/1.0/~libreoffice/+archive/ubuntu/ppa/signing_key.asc" \
      | gpg --dearmor -o /usr/share/keyrings/libreoffice-ppa.gpg \
 && echo "deb [signed-by=/usr/share/keyrings/libreoffice-ppa.gpg] https://ppa.launchpadcontent.net/libreoffice/ppa/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) main" \
      > /etc/apt/sources.list.d/libreoffice-ppa.list \
 && apt-get update && apt-get install -y --no-install-recommends libreoffice
```

If the keyserver must be used, force port 80: `gpg --keyserver hkp://keyserver.ubuntu.com:80
--recv-keys <fingerprint>`. Prefer `signed-by` over the deprecated global `apt-key`.

Also ask whether the PPA is needed at all: the distribution's own `libreoffice` package
avoids the external repository entirely if the version is acceptable, and pinning a version
keeps the image reproducible.

## Limits

- Root cause on the network side (firewall vs proxy vs IPv6) was not isolated; the explicit
  key fetch removes the dependency instead of fixing the path.
- The same pattern usually exists in several sibling Dockerfiles; fix all of them.
