---
system: docker
status: verified
checked: 2026-06-26
tags: [ca-certificates, harica, root-ca, openssl, debian, ubuntu, update-ca-certificates, dotnet]
---
# Check whether a root CA is in a container image's trust store (and which base images ship it)

## Symptom

Services start failing TLS handshakes against an endpoint whose certificate chains to a
newer root (example: `HARICA TLS RSA Root CA 2021`, issued 2021, needed for some
national/regional certificates). Some images work, others do not, and a copied `.crt` file in
the repository is the only thing keeping older images alive.

## Cause

The trust store comes from the distribution's `ca-certificates` package, whose version is
frozen with the base image's release. Roots added to Mozilla's bundle after that release are
missing until the package is upgraded from the release's security suite or the image moves to
a newer release. For the HARICA 2021 roots the observed matrix was:

| Base image | Distribution | `ca-certificates` | HARICA 2021 |
|---|---|---|---|
| `dotnet/aspnet:5.0` | Debian 10 buster | `20200601~deb10u2` | no (no upgrade available, buster is EOL) |
| `dotnet/aspnet:5.0-bullseye-slim` | Debian 11 | `20210119` | no; **yes** after `apt-get install ca-certificates` -> `20230311+deb12u1~deb11u1` |
| `dotnet/aspnet:5.0-focal` | Ubuntu 20.04 | `20210119~20.04.2` | no |
| `dotnet/aspnet:6.0` | Debian 11 | `20210119` | no (upgradeable while bullseye-security exists) |
| `dotnet/aspnet:8.0`, `9.0` | Debian 12 bookworm | `20230311+deb12u1` | yes (RSA and ECC) |
| `debian:trixie` (13) | — | `20250419` | yes |

## Fix

Verification one-liner, works on any Debian/Ubuntu-based image:

```bash
docker run --rm <image> sh -lc '
  cat /etc/os-release | head -2; dpkg-query -W ca-certificates;
  for f in /etc/ssl/certs/*.pem /usr/local/share/ca-certificates/*.crt; do
    openssl x509 -in "$f" -noout -subject 2>/dev/null;
  done | grep -i "HARICA TLS RSA Root CA 2021"'
```

Expect a subject like `C = GR, O = Hellenic Academic and Research Institutions CA, CN = HARICA TLS RSA Root CA 2021`
(spacing varies by OpenSSL version). Fingerprint of that root:
`D9:5D:0E:8E:DA:79:52:5B:F9:BE:B1:1B:14:D2:10:0D:32:94:98:5F:0C:62:D9:FA:BD:9C:D9:99:EC:CB:7B:1D`,
valid 2021-02-19 to 2045-02-13.

Getting the root into the image, in order of preference:

1. Use a base image whose release already ships it (bookworm or newer).
2. Upgrade `ca-certificates` from the release's security suite during the build
   (`apt-get update && apt-get install -y --no-install-recommends ca-certificates`); works for
   bullseye, requires the security suite to be still online or mirrored.
3. Last resort for EOL releases: `COPY root.crt /usr/local/share/ca-certificates/` and
   `RUN update-ca-certificates`. Keep the file in the repository and document why.

When you remove a `COPY`'d certificate because the base now ships it, rebuild every
dependent image locally (`--pull=false`, tagging intermediate bases with the registry name
so child Dockerfiles pick up the fresh local build) and run the check above on each.

## Limits

- Checked 2026-06 on the images listed; `ca-certificates` versions move, re-run the check.
- Minimal `debian` images do not have `ca-certificates` installed at all.
- .NET uses the OpenSSL store on Linux; Java images have their own `cacerts` keystore and need
  `keytool`, not this check.
