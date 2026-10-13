---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [ssh, elasticsearch, vk-cloud, backup]
---
# DevOps-894 backup root key installed on VK share

## Summary

User explicitly requested adding the backup server's root public key to the VK share. Installed RSA2048 public key from172.24.0.19 `/root/.ssh/id_rsa.pub` into10.18.26.4 `/root/.ssh/authorized_keys`, preserving existing keys. Verified backup→share root authentication using only backup-local `/root/.ssh/id_rsa`, with SSH agent disabled; remote `id -un` returnedroot and exit0. No data transfer, service change or repository edit performed.

## Task and authorization

[DevOps-894](https://youtrack.youdo.com/issue/DevOps-894). User command: add the identified root key to share. This authorizes that key addition and verification only; it does not authorize source stops, rsync, snapshot creation or DAG/config changes. [Source and destination evidence](2026-10-13-nomad-test-devops-894-es-source-check.md).

## Context

Source: `msk3-backup.youdo.corp`172.24.0.19. Destination: `vk-ms1-share-test01.mcs.local`10.18.26.4. Existing destination access via SSHyoudo with NOPASSWDsudo. Public key fingerprint: `SHA256:uQcAU22bn6Tsg++xnOcelNp9nmHOYWXwU0rKDQeG3rk`. Private key stays on backup; contents not displayed/copied. Key access is via root SSH to backup; destination write via youdo→sudo.

## Actions and key commands

Ran ai-sync (no output). Read only the source public key and held it in tool memory. One approved remote mutation ran `sudo -n python3` throughyoudo onshare: append the public key only if its type/blob was absent, retain existing file content, enforce `/root/.ssh`0700 andauthorized_keys0600. Result: addedtrue, exactly1matchingkey, file owneruid0.

Verification ran SSH on backup asroot with `IdentityAgent=none`, `IdentitiesOnly=yes`, explicit `-i /root/.ssh/id_rsa`, `BatchMode=yes` and `ForwardAgent=no`. Host verification pinned the known ECDSA public host key using an anonymous memory file held by the parent process. Destination command `id -un` returnedroot; SSHrc0 and no stderr. This proves the installed backup-local key works independently of forwarded user keys.

## Findings and changed files

Remote file changed: share `/root/.ssh/authorized_keys`; root SSH directory/file permissions verified as appropriate. No existing public keys removed; key not duplicated. Source and destination containers/data/disks remained untouched. KB logs/map/address comments updated; no repo or Git publication action.

## Risks and limits

This key grants root access onshare to the backup key holder, explicitly requested by user. Source known_hosts was not modified; the successful test supplied the pinned destination host key transiently. Ordinary unattended SSH/rsync may still need the destination key established in the backup server's persistent known_hosts; that is a separate unperformed remote change. No transfer or DAG success claim.

## Portable lesson

none
