---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, diagnosis]
---
# Jenkins build5826 ignored errors and recovery quiet hook removal

## Summary

Three ignored errors prevent RabbitMQ test5 queue cleanup: queue listing returns401, list construction fails on the error response, and purge has no queues_name. The fourth ignored error is nginx cache cleanup invoking rm without operands. User explicitly requested investigation and quiet-hook removal; hook was moved outside init.groovy.d with preserved0600/root ownership and independently verified absent from startup. Jenkins quietingDown=false; no restart.

## Task and context

User: «1 - проверь, 3 - сделай», referring to ignored errors and persistent recovery quiet hook. No superpowers skills used. Sources: Jenkins5826 GET API/consoleText, local automation-test-yandex playbooks/deploy/rabbit/clear.yml and playbooks/deploy/nginx/clear-cache.yml.

## Actions and findings

- GET /job/dynamic_deploy/5826/consoleText, ANSI stripping and JSON parsing of fatal results; no raw secret-bearing response copied.
- Rabbit listing /api/queues/test5 on rabbitmq.service.vk-test.consul returns401 Unauthorized. Playbook uses admin with rabbit_admin_pass. This establishes rejection of those credentials, without establishing the correct replacement.
- set name queues fails: can only concatenate str (not list) to str. Error-response items are not a queue list; the normal success path was not independently reproduced.
- purge rabbit queues fails because queues_name is undefined. All three tasks ignore errors; Rabbit cleanup did not complete.
- Fourth error: grep -Rl test5.youdo.sg /data/nginx/cache/ | xargs rm -v returns123 with rm: missing operand. No matching file operands were passed; the playbook lacks xargs -r. This is nginx cache cleanup, not a PG snapshot failure; interleaved console TASK headings were misleading.
- Read-only preflight confirmed hook is regular0600 file and contains only Jenkins.doQuietDown plus recovery log message. API quietingDown=false.
- Approved SSH action on root@10.18.26.8 moved /data/jenkins/data/jenkins/init.groovy.d/devops-892-recovery-quiet.groovy to /data/jenkins-recovery/disabled-hooks/devops-892-recovery-quiet.groovy after exact SHA256 guard ef9aed004bc13e0b2004d140dde95111e7b186d0806c326bd252847f5900bba6 and destination-absence guard.
- Independent second SSH read confirmed startup hook absent and backup600/root. Fresh API quietingDown=false. No restart, build, credential or repository change.

## Changes and limits

Updated Jenkins map and TODO. Rabbit authentication repair and optional nginx xargs empty-input fix were not requested or implemented; tracked in TODO. No claim about Jenkins restart acceptance or other startup hooks. Recovery backup retains original hash/mode.

## Portable lesson

None.

## User-authorized local Rabbit cleanup follow-up

User requested local playbook execution and expected401 to disappear. Existing checkout preserved without repository edits. Created local-only /home/slnnk/ai-data/jenkins-recovery/rabbit-test5-local.ini with rabbit group containing localhost/ansible_connection=local. Syntax and host-scope checks passed (one localhost).

Executed from /home/slnnk/git/automation-test-yandex:

```bash
ansible-playbook -i /home/slnnk/ai-data/jenkins-recovery/rabbit-test5-local.ini playbooks/deploy/rabbit/clear.yml -e @group_vars/all.yml -e instance=test5
```

Local group_vars/all.yml dc=vk-test and existing rabbit_admin_pass were used; no credential value copied. User-authorized execution obtained queues and performed contents DELETE operations for test5. Final recap localhost ok=3 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0; subprocess rc0, HTTP401/fatal/ignoring markers all0, no stderr warnings. Ansible uri default success reporting leaves changed=0 despite purge operations. No Jenkins rerun or job credential/config change performed; local success does not establish Jenkins uses the same effective credential. Further Jenkins-source comparison remains in TODO.
