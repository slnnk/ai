---
system: yandex-cloud
status: verified
checked: 2026-09-13
tags: [yc, yandex-cloud, cli, oauth, dpop, iam, service-account, secrets]
---
# yc CLI: "OAuth token ... issued after '2026-06-01' is not supported for IAM token exchange"

## Symptom

Every `yc` command with the user profile fails although the binary runs, `PATH` is fine and
`iam.api.cloud.yandex.net` is reachable:

```text
OAuth token for user ..., issued after '2026-06-01', is not supported for IAM token exchange
```

A profile that authenticates with a service-account key (`service-account-key` in
`~/.config/yandex-cloud/config.yaml`) keeps working.

## Cause

The profile was created with the legacy OAuth-token flow (`yc init` pasting an OAuth token).
Yandex Cloud stopped accepting OAuth tokens issued after 2026-06-01 for the IAM token
exchange; user profiles must use the DPoP-bound interactive authorization instead. The
failure is in the profile's credential type, not in the installation or the network.

## Fix

Re-authorize the user profile with DPoP, keeping a backup of the config:

```bash
cp -a ~/.config/yandex-cloud/config.yaml ~/.config/yandex-cloud/config.yaml.bak-$(date +%F)
yc init --dpop
yc resource-manager cloud list --limit 1      # read-only smoke test
```

Until then, run what the service account is allowed to do without switching the active
profile:

```bash
yc --profile <service-account-profile> <command>
```

Do not `yc config profile activate` the service-account profile globally: its permissions
and purpose differ from the user's.

Handle the config as a secret while diagnosing: `yc config list` and the raw `config.yaml`
print the service account's private key in nested YAML, which naive masking misses. Inspect
only specific fields (`yc config profile list`, `yc config get <key>`), and if a key was ever
echoed into a session log, rotate it (`yc iam key create --service-account-name ...`,
update consumers, `yc iam key delete <old-id>`).

## Limits

- Observed with `yc` 1.32.0 on Linux amd64. `--dpop` requires an interactive browser
  login; for headless hosts use a service-account key or a federated account instead.
- Tokens issued before the cut-off may keep working until they expire, so the symptom can
  appear at different times on different machines.
