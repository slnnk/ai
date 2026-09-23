---
system: base-images
status: verified
checked: 2026-06-23
tags: [base-images, harica, ca-certificates, debian-buster, debian-bullseye, dotnet-5, snapshot.debian.org]
---
# dotnet-aspnet 5.0: HARICA TLS RSA Root CA 2021

Date: 2026-06-23
Repository: `/home/slnnk/git/base-images`
File: `microsoft/dotnet-aspnet/5.0/Dockerfile`
Base image: `mcr.microsoft.com/dotnet/aspnet:5.0`

## Task

Check whether `HARICA TLS RSA Root CA 2021` is available through Debian `ca-certificates` via `apt` for the .NET ASP.NET 5.0 base image.

## Findings

- Base image OS: Debian GNU/Linux 10 `buster`.
- Installed package: `ca-certificates 20200601~deb10u2`.
- The package contains older HARICA roots only:
  - `Hellenic_Academic_and_Research_Institutions_RootCA_2011`
  - `Hellenic_Academic_and_Research_Institutions_RootCA_2015`
  - `Hellenic_Academic_and_Research_Institutions_ECC_RootCA_2015`
- `HARICA TLS RSA Root CA 2021` is not present in `/etc/ssl/certs` or `/usr/share/ca-certificates` in the base image.
- Default buster apt sources in the image are EOL and no longer provide Release files from `deb.debian.org` / `security.debian.org`.
- Using the commented Microsoft/Debian snapshot sources from `2022-05-27` with `Acquire::Check-Valid-Until=false`, the apt candidate is still `ca-certificates 20200601~deb10u2`; upgrading through apt does not add the 2021 root.
- Current Dockerfile manual `COPY` plus `update-ca-certificates` adds one certificate successfully.

## Actions

Commands used:

```bash
docker run --rm mcr.microsoft.com/dotnet/aspnet:5.0 sh -lc 'cat /etc/os-release; dpkg-query -W ca-certificates; find /etc/ssl/certs /usr/share/ca-certificates -iname "*harica*" -o -iname "*hellenic*" 2>/dev/null; grep -Ril "HARICA TLS RSA Root CA 2021\|Hellenic Academic" /etc/ssl/certs /usr/share/ca-certificates 2>/dev/null || true'
```

```bash
docker run --rm mcr.microsoft.com/dotnet/aspnet:5.0 sh -lc 'sed -i "s|^# deb http://snapshot.debian.org/archive/debian/20220527T000000Z buster main|deb http://snapshot.debian.org/archive/debian/20220527T000000Z buster main|; s|^deb http://deb.debian.org/debian buster main|# deb http://deb.debian.org/debian buster main|; s|^# deb http://snapshot.debian.org/archive/debian-security/20220527T000000Z buster/updates main|deb http://snapshot.debian.org/archive/debian-security/20220527T000000Z buster/updates main|; s|^deb http://security.debian.org/debian-security buster/updates main|# deb http://security.debian.org/debian-security buster/updates main|; s|^# deb http://snapshot.debian.org/archive/debian/20220527T000000Z buster-updates main|deb http://snapshot.debian.org/archive/debian/20220527T000000Z buster-updates main|; s|^deb http://deb.debian.org/debian buster-updates main|# deb http://deb.debian.org/debian buster-updates main|" /etc/apt/sources.list; apt-get -o Acquire::Check-Valid-Until=false update; apt-cache policy ca-certificates; apt-get -y --only-upgrade install ca-certificates; dpkg-query -W ca-certificates'
```

```bash
docker build -f microsoft/dotnet-aspnet/5.0/Dockerfile -t base-images-dotnet-aspnet-5-harica-check .
docker run --rm base-images-dotnet-aspnet-5-harica-check sh -lc 'find /etc/ssl/certs /usr/local/share/ca-certificates -iname "*harica*" -o -iname "*hellenic*" 2>/dev/null | sort; openssl x509 -in /usr/local/share/ca-certificates/harica_tls_rsa_root_ca_2021.crt -noout -subject -issuer -fingerprint -sha256 -dates'
```

### Verified certificate

`HARICA TLS RSA Root CA 2021`

SHA256 fingerprint:
`D9:5D:0E:8E:DA:79:52:5B:F9:BE:B1:1B:14:D2:10:0D:32:94:98:5F:0C:62:D9:FA:BD:9C:D9:99:EC:CB:7B:1D`

Validity: 2021-02-19 to 2045-02-13.

### Conclusion

For this Debian buster-based .NET ASP.NET 5.0 image, `HARICA TLS RSA Root CA 2021` is not available through the image's apt `ca-certificates` package. Keeping the explicit certificate file in `microsoft/dotnet-aspnet/5.0/` and running `update-ca-certificates` is necessary unless the base image is moved to a newer Debian/ca-certificates set.

### Follow-up: base image upgrade check

Checked alternative Microsoft ASP.NET runtime images:

- `mcr.microsoft.com/dotnet/aspnet:5.0-bullseye-slim`
  - Debian 11 `bullseye`
  - `ca-certificates 20210119`
  - Does not include `HARICA TLS RSA Root CA 2021`.
- `mcr.microsoft.com/dotnet/aspnet:5.0-focal`
  - Ubuntu 20.04.4 LTS
  - `ca-certificates 20210119~20.04.2`
  - Does not include `HARICA TLS RSA Root CA 2021`.
- `mcr.microsoft.com/dotnet/aspnet:6.0`
  - Debian 11 `bullseye`
  - `ca-certificates 20210119`
  - Does not include `HARICA TLS RSA Root CA 2021`.
- `mcr.microsoft.com/dotnet/aspnet:8.0`
  - Debian 12 `bookworm`
  - `ca-certificates 20230311+deb12u1`
  - Includes `HARICA_TLS_RSA_Root_CA_2021` and `HARICA_TLS_ECC_Root_CA_2021`.
- `mcr.microsoft.com/dotnet/aspnet:9.0`
  - Debian 12 `bookworm`
  - `ca-certificates 20230311+deb12u1`
  - Includes `HARICA_TLS_RSA_Root_CA_2021` and `HARICA_TLS_ECC_Root_CA_2021`.

Conclusion: simply switching .NET 5 from buster to bullseye/focal, or moving only to .NET 6, does not solve this CA issue. Moving to a bookworm-based ASP.NET runtime such as .NET 8/9 solves the CA-store issue, but requires application runtime compatibility/migration away from .NET 5.

### Correction: 5.0-bullseye-slim with apt update

A later check showed that `mcr.microsoft.com/dotnet/aspnet:5.0-bullseye-slim` can solve the HARICA 2021 issue if `ca-certificates` is upgraded from current Debian bullseye security repositories during image build.

Command checked:

```bash
docker run --rm mcr.microsoft.com/dotnet/aspnet:5.0-bullseye-slim sh -lc 'apt-get update; apt-get install -y --no-install-recommends ca-certificates; dpkg-query -W ca-certificates; find /etc/ssl/certs /usr/share/ca-certificates -iname "*harica*" -o -iname "*hellenic*" 2>/dev/null | sort'
```

Result:

- Before update: `ca-certificates 20210119`.
- After `apt-get update`: candidate `20230311+deb12u1~deb11u1` from `bullseye-security`.
- After install: `ca-certificates 20230311+deb12u1~deb11u1`.
- Trust store includes:
  - `/etc/ssl/certs/HARICA_TLS_RSA_Root_CA_2021.pem`
  - `/etc/ssl/certs/HARICA_TLS_ECC_Root_CA_2021.pem`

Updated conclusion: switching from `aspnet:5.0` buster to `aspnet:5.0-bullseye-slim` plus upgrading `ca-certificates` via apt can remove the need to store HARICA certificate files in the repository, while keeping .NET runtime major version 5.0. This still depends on Debian bullseye security repositories being available at build time or mirrored internally.

### Current Debian ca-certificates baseline

Checked after `docker pull debian:latest` on 2026-06-23:

- `debian:latest` is Debian 13.5 `trixie`; `ca-certificates` candidate is `20250419` from `trixie/main`.
- `debian:sid` is Debian `forky/sid`; `ca-certificates` candidate is `20260601` from `sid/main`.

Note: official minimal `debian` images do not have `ca-certificates` installed by default; these are apt candidate versions after `apt-get update`.

## Open items

- The follow-up verification of all changed images after the certificate file was removed is in [`2026-06-26-base-images-harica-root-ca-check.md`](2026-06-26-base-images-harica-root-ca-check.md).

## Portable lesson

[`~/ai/general/knowledge/docker/verify-root-ca-present-in-image.md`](../../../../general/knowledge/docker/verify-root-ca-present-in-image.md)
