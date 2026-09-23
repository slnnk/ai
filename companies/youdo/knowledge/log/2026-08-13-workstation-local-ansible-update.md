---
system: workstation
status: verified
checked: 2026-08-13
tags: [ansible, python3.9, pip, zabbix-agent2, get_url, adb, M-K0058, M-K0057, nat]
---
# Local Ansible update (2026-08-13)

## Task

Update the local Ansible installation so that the `zabbix-agent2` role runs on `M-K0058`.

## Context

- Workstation: `slnnk@youdo`; initially Ansible ran through Python `3.8.10`.
- Repository: `/home/slnnk/git/automation-services`.
- Initial problem: the `zabbix-agent2` role failed on `M-K0058` when executing `get_url` with the error `CustomHTTPSConnection object has no attribute cert_file`.
- Target host: `M-K0058`, `192.168.30.147`, Kazan office subnet.

## Actions

### What was updated

- The installation actually in use is in `~/.local`, not apt.
- Intermediate update on Python 3.8: `ansible 6.1.0 / core 2.13.2` -> `ansible 6.7.0 / core 2.13.13`. The original `get_url` error persisted.
- The working update was done on the already installed `/usr/bin/python3.9` (`3.9.5`): `ansible 8.7.0`, `ansible-core 2.15.13`.
- The system `/usr/bin/python3` was not switched, so as not to break Ubuntu components. The script `~/.local/bin/ansible-playbook` now has the shebang `#!/usr/bin/python3.9`.
- Final installation command:

  ```bash
  /usr/bin/python3.9 -m pip install --user --upgrade 'ansible==8.7.0' 'ansible-core==2.15.13'
  ```

- The apt packages `ansible 5.10.0` and `ansible-core 2.12.10` also remain on the system, but the command from `PATH` uses `/home/slnnk/.local/bin/ansible-playbook`.

### Checks

- `ansible-playbook --version` confirms `core 2.15.13`, Python `3.9.5` and loading from `~/.local/lib/python3.9/site-packages`.
- Syntax check succeeds:

  ```bash
  ANSIBLE_LOCAL_TEMP=/tmp/ansible-local-py39 ansible-playbook _monitoring.yml -i inventories/office/hosts --syntax-check
  ```

- Full rollout `_monitoring.yml -l M-K0058` succeeded: `ok=45`, `changed=28`, `failed=0`. The task `download zabbix repo`, which previously failed with `cert_file`, downloaded the package successfully.
- Zabbix Agent 2 `6.4.21`, Alloy and Falco are installed and running on `M-K0058`. The agent is active and listens on `*:10050`.
- `zabbix_agent2 -t adb_dev.discovery` returns three devices: `15888255AE004773`, `RZ8R71ZRK8H`, `x4pf5l5haegykni7`.

## Findings and changes

### Additional infrastructure cause and fix

- After installation the agent rejected passive checks: Zabbix reaches the Kazan subnet through NAT, so the source on the host is seen as `192.168.30.1`, while `Server=` allowed only `172.28.0.120,172.24.0.107`.
- For the `adb_devices` group the NAT address was added only to the passive allowlist; `ServerActive` was not changed.
- Changed file: `inventories/office/group_vars/adb_devices.yml`.
- The change was applied narrowly:

  ```bash
  ANSIBLE_LOCAL_TEMP=/tmp/ansible-local-py39 ansible-playbook _monitoring.yml -i inventories/office/hosts -l M-K0058 --tags zabbix-agent2
  ```

- Prod Zabbix confirmed the recovery: the interface of host `M-K0058` became `available=1`, the error field was cleared, the first `system.uname` value was received at `2026-08-13 20:42:51 MSK`.
- The user confirmed the rollout on `M-K0057`; an API check of prod Zabbix confirmed `available=1`, no interface error and 61 items with data.
- ADB monitoring on `M-K0057` also receives values: `5b2d4fe2=device`, `RZCY20AXJHN=device`, `GHKBB23B15002735=unauthorized`.
- `GHKBB23B15002735` is an external device outside the Android farm and must not be counted as capacity.
- The exclusion was added to `roles/zabbix-agent2/files/adb_devices/adb_devices.sh` and deployed to `M-K0057` with the command `_monitoring.yml -l M-K0057 --tags zabbix-agent2` (`failed=0`). The script ignores the serial when building the LLD JSON, but does not modify the source `/tmp/adb_devices.log`.
- Verified on the host: with `GHKBB23B15002735 unauthorized` present in the ADB file, `adb_dev.discovery` returns only `5b2d4fe2` and `RZCY20AXJHN`. The previously created Zabbix item will be removed according to the discovery rule lifetime and may remain in the UI for some time.

## Portable lesson

- `~/ai/general/knowledge/ansible/get-url-customhttpsconnection-no-attribute-cert-file.md`
- `~/ai/general/knowledge/zabbix/passive-agent-behind-nat-server-allowlist.md` (NAT source address in the passive `Server=` allowlist; written by another batch)
