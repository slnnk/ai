---
system: jenkins
status: verified
checked: 2026-10-11
tags: [jenkins, git, credentials, recovery]
---
# DevOps-890: restored Git parameter credential failure

## Task

Investigate the user's branch parameter failure in `youdo_web_testing_one` after recovery. Task: DevOps-890.

## Context

All three `youdo_web_testing_*` jobs use HTTPS SCM `https://gitlab.youdo.sg/youdo/youdo.static.git` and the same stored username/password credential. Screenshot and logs report `fatal: unable to get password from user`, exit 128.

## Actions

- User separately authorized two Script Console POST probes; helper `/home/slnnk/ai-data/jenkins-recovery/probe-git-credential.py --apply` loads tooling authentication from company `.env` in memory and emits only booleans/counts.
- First probe proved credential selection and a nonempty decrypted password, but failed because the diagnostic used nonexistent `TaskListener.fromPrintStream`. Corrected locally to `new StreamTaskListener(logStream)` after checking Jenkins source.
- Second approved probe reproduced the password prompt failure through Jenkins git-client with the actual job credential; no authentication rejection or TLS error was reported.
- Read-only SSH checks inspected Git version, locale and configuration on controller and agent. No builds or configuration changes executed.

## Findings

- Controller container working directory and Git repository top level are `/`; `/.git/config` contains `credential.interactive=never`. Git version is 2.47.3.
- Git 2.47.3 `credential_getpass` returns before calling askpass when that setting is `never`. Jenkins git-client 6.6.0 passes username/password through a temporary `GIT_ASKPASS` script. This configuration blocks that path.
- Agent working directory is `/`, Git is 2.43.0, and no corresponding credential setting or root Git repository was found.
- Credential presence/decryption is verified, but GitLab acceptance of the credential remains untested until the blocking Git setting is bypassed or removed.
- Primary source: https://github.com/git/git/blob/v2.47.3/credential.c and https://github.com/jenkinsci/git-client-plugin/blob/git-client-6.6.0/src/main/java/org/jenkinsci/plugins/gitclient/CliGitAPIImpl.java.

## Changes

User authorized the exact runtime fix with "Выполни". Executed on controller `10.16.28.8`: `docker exec jenkins git -C / config --local --unset-all credential.interactive`; exit 0. A separate read-only command verified the key is absent (Git config exit 1, explicit `credential.interactive_absent`). No credential replacement, job mutation or build was performed. The user subsequently refreshed the parameter form and supplied a screenshot showing multiple remote branches including `origin/master`, with the authentication error absent. This verifies functional Git branch lookup for `youdo_web_testing_one` after the runtime fix. No actual build has been verified. The `failedSuite` selector still reports missing workspace files, consistent with the fresh agent and backup workspace exclusions. Container-layer fix will not survive recreation; image correction requires separately approved repository work.

## Portable lesson

none
