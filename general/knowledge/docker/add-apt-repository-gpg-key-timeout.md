---
system: docker
status: outdated
checked: 2026-11-04
tags: [apt, ppa, gpg, add-apt-repository, keyserver, signed-by, ubuntu, libreoffice]
decision_state: restricted
decision_scope: Saved LibreOffice PPA key fix
decision_summary: Saved PPA fix is not ready for reuse; a replacement key route and successful build must be verified.
decision_date: 2026-11-04
decision_source: #staleness-review-2026-11-04
---
# `add-apt-repository ppa:...` fails with "retrieving gpg key timed out" in a Docker build

## Staleness review (2026-11-04)

The Dockerfile fix below is not ready for reuse: a read-only HTTP check on 2026-11-04 returned HTTP 404 for its `https://api.launchpad.net/1.0/~libreoffice/+archive/ubuntu/ppa/signing_key.asc` URL. No replacement URL or Docker build was validated in this review. The timeout's network mechanism remains a hypothesis; the note does not establish firewall, proxy, IPv6 or dirmngr as the cause. Retain the `signed-by` design principle, but require a supported key-retrieval source, fingerprint verification and a successful build before restoring this recipe to verified status.

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

## Suspected cause (unconfirmed)

The observed timeout is consistent with a failed signing-key retrieval path.
Firewall, proxy, IPv6 and GnuPG/dirmngr behavior are possible mechanisms, but
none was isolated in the original incident. Do not infer a fixed transport, port
or proxy behavior without checking the software version and actual request path.

## Historical workaround (broken URL; do not use)

The following unvalidated proposal tried to replace implicit key retrieval with
an explicit keyring and `signed-by`. Its key URL returned HTTP 404 on 2026-11-04;
do not copy this Dockerfile as a working fix:

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
