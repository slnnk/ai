---
system: workstation
status: verified
checked: 2026-09-13
tags: [yc, yandex-cloud, cli, oauth, dpop, iam, service-account, key-rotation]
---
# Recovering the local Yandex Cloud CLI

## Task

Restore a working `yc` CLI on the work laptop: the default profile fails the IAM token
exchange although the binary and network are fine.

## Context

- Check date: 2026-09-13 (Europe/Moscow)
- Host/user: local work machine, user `slnnk`
- CLI: `/home/slnnk/yandex-cloud/bin/yc`, version `1.32.0`, Linux amd64
- Configuration: `~/.config/yandex-cloud/config.yaml`, permissions `0600`

## Findings: symptom and cause

The binary is installed, is in `PATH` and runs. DNS and HTTPS access to
`iam.api.cloud.yandex.net` work.

The active profile `default` fails the IAM token exchange:

```text
OAuth token for user ..., issued after '2026-06-01', is not supported for IAM token exchange
```

The problem is isolated to the outdated OAuth authentication method of the profile, not
to the CLI installation or the network.

The profile `terraform-k8s-test` with a service account key works at the time of the
check: the read-only request `yc --profile terraform-k8s-test resource-manager
cloud list --limit 1` successfully returned the cloud `youdo-ya-cloud`.

## Actions: recovery

For the user profile, go through the interactive authorization again with DPoP:

```bash
cp -a ~/.config/yandex-cloud/config.yaml ~/.config/yandex-cloud/config.yaml.bak-2026-09-13
yc init --dpop
yc resource-manager cloud list --limit 1
```

Until then, operations permitted to the service account can be run without changing
the active profile:

```bash
yc --profile terraform-k8s-test <command>
```

Do not activate the service profile globally without need: its permissions and
intended purpose may differ from the user profile.

## Open items: security and TODO

- During the diagnosis on 2026-09-13 the private part of the existing service account
  key was printed into the session diagnostic output because of incorrect masking of
  nested YAML. The secret was not carried into this note.
- Rotate the authorized key with ID `aje1kjc599tg2oj7ok2d`, update it at all
  consumers and delete the old key after verifying the new one.
- Do not use the output of the whole `yc config list` or the raw `config.yaml` for
  diagnostics: a profile may contain the entire private key.

## Verification commands

```bash
yc version
yc config profile list
yc resource-manager cloud list --limit 1
yc --profile terraform-k8s-test resource-manager cloud list --limit 1
```

## Portable lesson

[yc CLI: "OAuth token ... issued after 2026-06-01 is not supported for IAM token exchange"](../../../../general/knowledge/yandex-cloud/yc-cli-oauth-token-not-supported-use-dpop.md)
