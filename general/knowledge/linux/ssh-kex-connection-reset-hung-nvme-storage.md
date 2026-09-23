---
system: linux
status: verified
checked: 2026-08-03
tags: [ssh, kex_exchange_identification, nvme, pcie-aer, smart, journald]
---
# ssh "kex_exchange_identification: read: Connection reset by peer" caused by a hung disk

## Symptom

`ssh user@host` fails with
`kex_exchange_identification: read: Connection reset by peer`. TCP port 22
answers, credentials are never asked. Other services on the host (for example
VNC) also stop authenticating at the same time. After a hard reboot everything
works again and the passwords turn out to be correct.

## Cause

The reset happens before authentication, so it is not a credential problem.
The usual suspects are `MaxStartups`, fail2ban or a firewall, but when several
unrelated daemons degrade together the cause is often a stalled storage
subsystem: the listening socket still accepts the TCP connection, while `sshd`
cannot read files or fork the session process, and the kernel resets the
connection.

Evidence pattern for a failing NVMe/PCIe link:

- `kern.log`/`journalctl -k` before the hang: repeated `PCIe Bus Error`,
  `RxErr`, `BadDLLP` (AER correctable, physical layer) on the NVMe device, then
  `nvme ... I/O Cmd ... timeout, aborting ... WRITE`.
- All logs stop abruptly mid-line with no shutdown markers.
- On the next boot `systemd-journald` renames the previous `system.journal` to
  `system.journal~` as corrupted/unfinished.
- `smartctl -a /dev/nvme0` shows `Percentage Used` above 100% and a high
  `Unsafe Shutdowns` count while the overall result is still `PASSED`.

## Fix

Diagnose from the console or after a reboot:

```bash
journalctl -k -b -1 | grep -E 'nvme|PCIe Bus Error|RxErr|BadDLLP|timeout'
ls /var/log/journal/*/ | grep '~$'
smartctl -a /dev/nvme0 | grep -E 'Percentage Used|Unsafe Shutdowns|Error Information'
sshd -T | grep -i maxstartups
```

Treat `Percentage Used >= 100%` as a worn-out drive regardless of `PASSED`:
back up immediately, replace the drive, reseat the M.2 module and check
firmware/BIOS if `RxErr`/`BadDLLP` recur (they can also be a slot/link issue),
and alert on the kernel messages above until the replacement. Reduce chatty
services that write hundreds of thousands of log lines to the same disk.

## Limits

- The pattern proves an I/O hang, not the exact failing component (SSD vs
  PCIe slot/link); confirm after replacement.
- Kernel 6.8 and OpenSSH on Ubuntu; message wording may differ on other
  kernels. The default `MaxStartups 10:30:100` produces the same client error
  when it triggers, so rule it out with the sshd log first.
