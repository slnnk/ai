---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, agent, ansible, websocket, approval]
---
# DevOps-890: AutoTest agent connection

## Task

User requested connection of the recovered Jenkins agent. Prepare necessary local adaptations and a concrete agent-only apply command; remote changes require a separate explicit approval under global AGENTS.md. Existing branch DevOps-890-update-jenkins-images remains approved for this recovery; publication is deferred.

## Context

Controller10.16.28.8 is running and verified. New agent root@10.16.28.26 has /data mounted ext4 with9.3GiB free, root6.9GiB free; Docker/Compose absent and no prior agent directory. Restored node AutoTest uses inbound launcher, remoteFS /home/jenkins/work,5 executors and label autotest_web. Selected latest agent image is3355.v388858a_47b_33.6 (JDK21/Maven3.9.13).

## Actions

Read-only API confirms existing AutoTest connection secret available through authenticated /computer/AutoTest/jenkins-agent.jnlp. Secret was validated only in process memory, never printed or written to a file. Controller /tcpSlaveAgentListener/ declares port50000 whereas existing controller compose publishes49187. Recovery-specific WebSocket over HTTP80 avoids this mismatch. Official entrypoint supports JENKINS_WEB_SOCKET: [upstream entrypoint](https://github.com/jenkinsci/docker-agents/blob/master/jenkins-agent).

Prepared local helper /home/slnnk/ai-data/jenkins-recovery/connect-jenkins-agent.py. Default invocation performs read-only JNLP GET and list-hosts; --apply executes the scoped Ansible command. It loads existing company .env credentials, validates64hex secret and exact AutoTest name, injects process-only VAULT_TOKEN/VAULT_AUTH_METHOD/JENKINS_AGENT_SECRET, without secrets in arguments/files/output.

## Findings

Approved agent-only apply completed exit0: `ok=31 changed=16 unreachable=0 failed=0 skipped=4`. Docker/Compose, registry authentication, working directories/symlink and protected compose were installed; the selected agent container started successfully.

Independent read-only verification passed: Jenkins API reports AutoTest `offline=false`,5 executors; controller remains online,116 plugins active, queue empty. Agent container `jenkins-agent-jenkins_agent-1` is running image3355.v388858a_47b_33.6 with digest `sha256:f40c3b92f4670dd59df5fca91c8158aeb6309982aec25788fb49fbd390f6dc2f`, matching the preverified registry image. Compose permissions root:root0600; /opt/jenkins-agent links to /data/jenkins-agent. Data disk9.3GiB free; root4.9GiB free after pull. Bounded log review confirms WebSocket connection and Connected marker, Remoting3355.v388858a_47b_33, no exception classes or severe/error entries. Raw logs/secrets were not printed.

No build/job was triggered as part of connection verification. Agent workspaces/SSH/cache remain newly created; functional acceptance, backup/routing and publication are separate stages.

User approved the exact proposed --apply command with "Выполни". Sandbox attempt could not obtain controller metadata and exited before changes. Identical outside-sandbox retry validated the secret, reached the agent and passed Vault checks; Docker dependency installation is in progress. No extra command, routing change or Git publication is authorized by this approval.

Syntax check passed and list-hosts selects exactly yc-a-jenkins-agent-test-01. Helper default completed exit0. Scoped git diff check passed; whole-checkout diff check reports preexisting unrelated gitlab-runner trailing whitespace, left untouched. No agent deployment or other remote modifications occurred.

## Changes

Local task changes only:

- roles/jenkins/tasks/install-jenkins-agent.yml: nonempty secret assertion, rendered compose0600 and no_log.
- roles/jenkins/templates/docker-compose-agent.j2: secret from jenkins_agent_secret or process JENKINS_AGENT_SECRET; optional jenkins_agent_websocket defaults false.
- inventories/yandex/jenkins-recovery.ini: WebSocket enabled only for the new recovery agent.

Proposed command, pending explicit runtime approval:

```bash
python3 /home/slnnk/ai-data/jenkins-recovery/connect-jenkins-agent.py --apply
```

It runs ansible-playbook -i inventories/yandex/jenkins-recovery.ini jenkins.yml --limit yc-a-jenkins-agent-test-01 --skip-tags zabbix-agent2,alloy from the existing checkout. Effects: install Docker/Compose, write registry authentication and protected agent compose, create working/cache/SSH directories and symlink, start selected agent image connected to AutoTest via WebSocket. Monitoring, controller and routing are outside the scoped apply.

## Risks

Image storage uses the root disk; monitor available capacity while pulling. Workspaces, SSH directory and Gradle caches start empty. Connecting the node makes5 executors available for newly submitted builds; restored queue was empty. Functional build acceptance is separate. Global remaining work lives in ~/ai/TODO.md.

## Portable lesson

none
