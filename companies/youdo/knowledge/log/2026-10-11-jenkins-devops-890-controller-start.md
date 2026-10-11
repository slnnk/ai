---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, ansible, controller, approval]
---
# DevOps-890: controller provisioning and startup

## Task

Provision and start the recovered controller for DevOps-890. User explicitly approved the previously proposed controller-only command with "Выполни". Publication remains deferred until recovery acceptance.

## Context

Controller root@10.16.28.8 has the validated October7 backup restored at `/data/jenkins/data/jenkins`:11 job configs,116 plugin archives,version marker2.555.1. Archive is retained separately. Independent startup review found an empty queue, no running/resumable builds and no XML timer/SCM polling triggers; built-in controller retains10 executors in NORMAL mode. See [restore evidence](2026-10-11-jenkins-devops-890-backup-transfer.md).

## Actions

Approved command from existing checkout `/home/slnnk/git/automation-services`, branch `DevOps-890-update-jenkins-images`:

```bash
ansible-playbook -i inventories/yandex/jenkins-recovery.ini jenkins.yml --limit yc-a-jenkins-test --skip-tags zabbix-agent2,alloy
```

Existing company `.env` `VAULT_YANDEX_TEST_TOKEN` is injected only as process `VAULT_TOKEN`, with `VAULT_AUTH_METHOD=token`; no credential values printed or copied to inventory. Plain output without verbosity/diff protects rendered registry auth. Sandbox attempt failed before remote changes (unreachable); identical outside-sandbox retry reached controller. Vault token/secret fetch and empty-value assertions passed. Docker dependency installation is currently in progress.

## Findings

Approved apply completed exit0: `ok=30 changed=15 unreachable=0 failed=0 skipped=4`. Docker/Compose installation, registry auth, compose rendering and controller startup succeeded. First image download/unpacking took several minutes; containerd growth confirmed progress. Monitoring deployment and agent tasks were skipped as scoped.

Independent read-only verification passed after apply:

- Container `jenkins` is running image `registry.youdo.sg/sysadmins/devops-tools/jenkins:2-555-1-2`; inspected digest matches previously verified `sha256:6f80988c634047436ac35994bb37e54e6c3b61650a9f7a87be7fa5aaf688dbe4`.
- Direct controller HTTP/API reports Jenkins2.555.1. Existing company `.env` JENKINS_USER/JENKINS_TOKEN authenticate successfully; values used only in process memory.
- API exposes all11 restored jobs and all116 plugins active, with no inactive plugins. Queue has zero items. Built-in node is online with10 executors; restored AutoTest node has5 executors and is offline pending agent recovery. Existing red job colors represent restored historical results, not newly run acceptance tests.
- Bounded startup-log review confirms completed initialization, loaded jobs and Jenkins fully up; zero plugin failures, exception classes or SEVERE entries. One warning and no bootstrap-secret prompt. Raw logs were not printed.
- `/opt/jenkins` links to `/data/jenkins`; `/data` has135GiB free and root filesystem13GiB free. Archive retained; routing still targets the old controller.

Verification helper `/home/slnnk/ai-data/jenkins-recovery/verify-jenkins-controller.py` supports `--help` and configurable `--url`, issues only GETs and prints selected metadata/counts. Initial helper invocation exposed local Python3.8 incompatibility with str.removeprefix; corrected before successful verification. No repository or remote change was needed for this local correction.

## Changes

No task repository edits in this stage. Existing task pins/inventory and unrelated user changes are preserved. Authorized remote effects: install Docker/Compose, write registry authentication and compose files, create required directories/symlink and start selected controller image `2-555-1-2`. Agent and routing changes are outside this command.

## Risks

Restored controller has10 executors and can run newly submitted jobs after startup. Queue/timer review is limited to restored configuration; plugin runtime checks follow startup. Live recovery backlog remains only in ~/ai/TODO.md.

## Portable lesson

none
