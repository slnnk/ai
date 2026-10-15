---
system: ssh
status: verified
checked: 2026-10-15
tags: [ssh, verification, memfd]
---
# Verify an SSH identity held only in memory

## Symptom

An SSH verification command using a private identity from stdin or /proc/self/fd reports authentication rejection, despite installing its corresponding public key. A key-loader failure can precede authentication and resemble a server rejection.

## Cause

OpenSSH closes inherited nonstandard descriptors. Therefore subprocess pass_fds with a /proc/self/fd identity path is insufficient: the path can disappear inside the SSH process. Also, stdin has its own lifecycle inside the SSH client. A verifier must distinguish an unavailable identity from a rejected key.

## Fix

On Linux, hold a memfd in the parent Python process, chmod0600, write the in-memory private bytes, and pass /proc/<parent-pid>/fd/<fd> to ssh -i. Keep the parent and descriptor alive until ssh exits, then close the descriptor in finally. Set IdentitiesOnly=yes and BatchMode=yes, run a harmless command, capture stdout/stderr, and emit only exit status, authentication classification and any public fingerprint. Private contents need not be saved to disk or printed. Use an explicitly located executable if the service PATH differs from an interactive shell.

## Limits

This requires Linux memfd support and permission to read the parent descriptor through procfs. It is a verifier technique, not a change to server authentication policy. Keep normal host identity verification and use independently trusted host keys. Encrypted private keys require a separate in-memory passphrase/parser path; do not put a passphrase in command-line arguments.
