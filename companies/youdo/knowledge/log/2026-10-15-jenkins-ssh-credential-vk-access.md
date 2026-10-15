---
system: jenkins
status: verified
checked: 2026-10-15
tags: [ssh, credentials, jenkins, vk-test]
---
# Jenkins ssh credential root access for test5 PostgreSQL and balancer

## Task and authorization

User explicitly requested adding the public key from Jenkins Credentials ID ssh to root authorized_keys on test5 PostgreSQL10.18.26.39 and balancer10.18.20.97, and changing PostgreSQL dynamic_deploy stage to use that credential. Existing stage settings were described before apply: credentialsId=ssh and hostKeyChecking=false, matching current Nginx stage. No deployment retry authorized/performed.

## Actions and key commands

- Extracted only the public key through read-only Jenkins Script Console code. Private key passed to ssh-keygen through stdin inside the controller process; never printed or persisted. Credential username root, public fingerprint SHA256:ggvn7B3Cz6PWEGlTC0u4JR4Fo8K4KQGt7wghSn6NH/s. Public artifact ~/ai-data/jenkins-recovery/jenkins-credential-ssh.pub; metadata only in jenkins-credential-ssh-public.json.
- Administrative SSH youdo + sudo succeeded on both targets. Balancer known host already trusted; PostgreSQL host key was enrolled locally through accept-new on first connection. No independent prior fingerprint attestation existed for PostgreSQL.
- Idempotent append to each /root/.ssh/authorized_keys, preserving all existing bytes/keys. Root owner, authorized_keys0600 and .ssh0700 verified. Installation receipts ssh-install-10.18.26.39.json and ssh-install-10.18.20.97.json under ~/ai-data/jenkins-recovery/.
- Updated only Restore PG DB ansiblePlaybook arguments in dynamic_deploy. Added credentialsId ssh and hostKeyChecking false; XML settings outside script and all script content outside this stage preserved and GET-verified. Old script SHA256aeb21ece7c726f2a1e7a61228e7c6b35da3326c32589a8869f36f4bba1d86541, new SHA2565dd2515bb205fe742db1206fe9e6ff9cb4cff28785717bbca2ab713478e3614d. Exact new script approval verified; pending count3 to2, unrelated entries preserved.

## Findings and validation

SSH server effective settings on both hosts allow root key authentication, PermitRootLogin without-password, PubkeyAuthentication yes, expected authorized_keys paths, no extra user/group restriction. No sshd configuration/restart performed.

Initial verification falsely reported authentication rejection because OpenSSH could not load stdin/self-fd identities. Corrected the verifier to hold the key in Linux memfd and address /proc/<parent-pid>/fd/<fd>; no disk file. A subsequent read-only id -u command from the Jenkins controller using the exact ssh credential succeeded as root on both10.18.26.39 and10.18.20.97 (status0/rootLogin true). Verification deliberately uses host-key options matching the Pipeline; it does not attest server identity independently. See [portable memory identity recipe](../../../../general/knowledge/ssh/openssh-memory-identity.md).

## Changed files

Remote root authorized_keys on two targets; Jenkins dynamic_deploy PostgreSQL stage and exact matching ScriptApproval entry. Local helper ~/ai-data/jenkins-recovery/jenkins-ssh-access.py and Groovy public-extraction/verification helpers; nonsecret receipts and knowledge notes. No repository task files, Git state or credentials definitions modified. No private material copied into notes, scripts or logs.

## Risks and limits

Both requested SSH root accesses now verified. Rabbit API401 from build5819 remains outside this task; no credential/service edit performed there. No PostgreSQL reset, cache clear or deployment run during these access changes. Full job acceptance remains unverified after correction.

## Related evidence

[Failed deployment and parameters](2026-10-14-jenkins-test5-release-deploy.md), [Jenkins map](../systems/jenkins.md).
