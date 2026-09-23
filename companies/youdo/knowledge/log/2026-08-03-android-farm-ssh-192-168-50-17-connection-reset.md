---
system: android-farm
status: verified
checked: 2026-08-03
tags: [ssh, kex, nvme, pcie-aer, smart, journald, M-K0052, emulator, vnc]
---
# SSH: `192.168.50.17` resets the connection at the KEX stage

## Task

- Date: 2026-08-03
- Host: `192.168.50.17`
- Connection user: `root`
- Command: `ssh root@192.168.50.17`
- Error: `kex_exchange_identification: read: Connection reset by peer`

## Findings

### Interpretation

The TCP connection was established, but the remote side or an intermediate network device sent a TCP RST before the SSH key exchange completed. The error occurs before the password or SSH key is checked, so by itself it does not indicate wrong credentials.

### Main hypotheses

1. `sshd` is not running, is overloaded or limits new connections (`MaxStartups`).
2. The client address is blocked by firewall/fail2ban/sshguard or by access rules.
3. The connection is reset by a firewall, NAT, VPN or another intermediate device.
4. Something other than SSH is running on port 22, or SSH listens on another port/interface.
5. Restrictions in `/etc/hosts.allow`, `/etc/hosts.deny` or socket activation.

## Actions

### Checks

From the client:

```bash
ssh -vvv root@192.168.50.17
nc -vz 192.168.50.17 22
```

From the server console:

```bash
systemctl status sshd || systemctl status ssh
ss -lntp | grep ':22'
journalctl -u sshd -n 100 --no-pager || journalctl -u ssh -n 100 --no-pager
nft list ruleset
fail2ban-client status sshd
```

## Investigation after the reboot

- Checked on 2026-08-03 after a manual reboot at `13:53 MSK`.
- Hostname: `M-K0052`, Ubuntu, kernel `6.8.0-136-generic`.
- Access: direct SSH `root@192.168.50.17`; the client had the address `172.30.62.124` during the check.
- OpenSSH and TightVNC run on the host (`vncserver@1.service`, display `:1`, TCP `5901`, password file `/root/.vnc/passwd`).

### Established cause

The most likely root cause of the simultaneous degradation of SSH and VNC is a hang of the storage subsystem due to problems with the system NVMe `ADATA SX6000PNP` (`/dev/nvme0`, PCI `0000:02:00.0`), not wrong SSH/VNC credentials.

Evidence:

1. The old `kern.log` recorded 196 `PCIe Bus Error`/`RxErr`, including 50 `BadDLLP`, related to the NVMe. The errors were AER `Correctable`, `Physical Layer`.
2. On 2026-07-24 at `08:34:21 MSK` the kernel registered an NVMe write operation timeout: `I/O Cmd ... timeout, aborting ... WRITE`, then an AER PCIe and the completion of the abort. In total there are four lines with an NVMe I/O timeout in the journal.
3. All journals of the previous run stopped abruptly on 2026-07-24 at `10:06:14 MSK` in the middle of a line. There are no regular system shutdown/reboot markers.
4. At boot on 2026-08-03 `systemd-journald` found the `system.journal` file corrupted or unfinished after an unclean shutdown and renamed it to `.journal~`; the file cannot be read by a normal `journalctl`.
5. NVMe SMART: `Percentage Used: 222%`, `Unsafe Shutdowns: 94`, `Error Information Log Entries: 6`, while the formal overall status is still `PASSED`. A wear counter above 100% requires treating the drive as having exhausted its rated endurance/unreliable, even with `PASSED`.
6. After the reboot the old VNC password file was not changed (`mtime 2026-07-23 20:21:17`), but the VNC log recorded `Full-control authentication passed` from `172.30.62.124`. So the previous VNC failure does not prove a wrong password and is consistent with a general I/O/process hang.
7. After the reboot SSH and VNC are active, there are no failed units, and no new AER/NVMe timeouts in the current boot at the time of the check. The filesystem is 58% full, memory and swap are not exhausted; no signs of OOM.

Additional load on the logs: the `emulator_1` service wrote about 642 thousand lines (polling `/wd/hub/status` every 5 seconds), because of which `/var/log/syslog.1` grew to 121 MiB. This does not look like the root cause of the hang, but it increases writes to an already problematic SSD and complicates diagnostics.

### Why SSH was reset before KEX

The TCP/system SSH socket could still accept the connection, but `sshd` and the dependent read/process-spawn operations could not serve it normally with a hung disk subsystem. This explains the reset before authentication. The `MaxStartups` limit is the default (`10:30:100`); there is no evidence in the available journals that it was triggered.

## Open items

Risks and next steps:

1. Urgently ensure an up-to-date backup of the machine's data and configuration.
2. Plan an NVMe replacement; do not rely on SMART `PASSED`, since `Percentage Used=222%` and there have already been real I/O timeouts/PCIe errors.
3. During physical maintenance check the M.2 seating/contacts, cooling and BIOS/firmware. Recurring `RxErr`/`BadDLLP` may be related both to the SSD itself and to the PCIe link/slot.
4. Until replacement, monitor `journalctl -k` for `nvme`, `PCIe Bus Error`, `RxErr`, `BadDLLP`, `timeout`; set up alerts.
5. Reduce the logging verbosity of `emulator_1` or exclude the successful health check `/wd/hub/status` from debug logs; configure sensible rotation.
6. After replacement/maintenance run a filesystem check in an agreed downtime window and make sure the persistent journal is readable again without corruption.

## Status

The cause is established with high probability: degradation/failure of the NVMe or its PCIe link led to a system hang; the reboot temporarily restored operation. The configuration on the server was not changed during the investigation.

## Portable lesson

`~/ai/general/knowledge/linux/ssh-kex-connection-reset-hung-nvme-storage.md`
