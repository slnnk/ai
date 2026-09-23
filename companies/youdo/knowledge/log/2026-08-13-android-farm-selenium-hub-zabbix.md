---
system: android-farm
status: verified
checked: 2026-08-13
tags: [android, selenium-grid, zabbix, zabbix-agent2, nat, ansible, monitoring]
---
# Zabbix on the Android Selenium hub M-K0056 — 2026-08-13

## Task

Make the Zabbix agent on the Android farm Selenium Grid hub `M-K0056` reachable from the production Zabbix server.

## Context

- Host: `M-K0056`, `192.168.30.30`, Kazan office.
- Purpose: Selenium Grid hub of the Android farm, Grid endpoint `192.168.30.30:4444`.
- Zabbix host: `M-K0056-selenium-hub`, hostid `10590`, groups `Selenium` and `All`.

## Findings: diagnosis

- The Zabbix interface `192.168.30.30:10050` was `available=2` with the error `Connection reset by peer`; item values were absent.
- On the host `zabbix-agent2` was active and listening on TCP `10050`.
- The journal confirmed the cause: passive connections arrived through NAT from `192.168.30.1`, but `Server=` allowed only the Zabbix server addresses `172.28.0.120` and `172.24.0.107`.

## Changes and verification

- Created `inventories/office/group_vars/selenium_hub.yml`; for the `selenium_hub` group `192.168.30.1` was added to the passive allowlist. `ServerActive` was not changed.
- Applied narrowly:

  ```bash
  ANSIBLE_LOCAL_TEMP=/tmp/ansible-local-py39 ansible-playbook _monitoring.yml -i inventories/office/hosts -l M-K0056 --tags zabbix-agent2
  ```

- Playbook result: `ok=12`, `changed=5`, `failed=0`.
- Prod Zabbix after retry: interface `available=1`, error cleared, system values started arriving.

## Open items: remaining risks

- Only the `YouDo OS Linux template` is linked to M-K0056; the state of the Selenium Grid/hub on port `4444` is not monitored separately.
- The agent reports an active-checks timeout to `172.24.0.107:10051`. Current passive monitoring works; the need for active checks and the route to both Zabbix servers should be verified separately.

## Portable lesson

- `~/ai/general/knowledge/zabbix/passive-agent-behind-nat-server-allowlist.md`
