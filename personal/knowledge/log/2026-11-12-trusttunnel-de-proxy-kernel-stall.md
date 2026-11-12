---
system: trusttunnel-de
status: verified
checked: 2026-11-12
tags: [vpn, relay, incident, linux]
---
# VPN and relay health after relay kernel stalls

## Summary

- Russian relay suffered three recorded downtime periods on November12.
- Five guest CPU0 soft lockups occurred during the same incident windows.
- Full boot journal shows four CD-ROM stacks and one independent QXL stack.
- All share interrupt restoration; CD-ROM-only causality is not established.
- Guest CPU/RAM/I/O were low before the evening outage; nginx did not restart.
- Daytime recovery had steal14.17%; agent history is missing during freezes.
- QEMU/KVM execution or emulation stalls are the leading hypothesis.
- Guest-kernel versus host cause cannot be resolved without host evidence.
- Deep diagnosis section records raw artifacts, limits and upstream sources.
- Central TODO tracks provider evidence; support draft is local and unsent.
- All monitor locations recovered; no remote changes or background operations.

## Task
Check VPN and vpn-proxy availability and investigate reported outages using read-only diagnostics.

## Context
German endpoint it-garage-de-01 and Russian relay dline-spb-01. See [system map](../systems/trusttunnel-de.md).

## Actions
Read SSH uptime, boot journal, systemd activation/restart counters, warning/kernel journals, nginx errors and short vmstat samples. Read both HetrixTools monitors and downtime histories. Probe authenticated-certificate HTTPS /tt_ping directly to Germany and through Russia from the relay; no authenticated VPN data-plane test.

## Findings
At 15:58 Moscow on November 12 both monitors were UP; both HTTPS probes returned 200 with TLS verification result 0 (0.15/0.13 seconds). No failed units on either VM. VPN uptime was almost six days, relay uptime over three days. Neither VM rebooted today. TrustTunnel and nginx on Germany remained active since November 9, NRestarts=0. Relay nginx remained active since November 9, NRestarts=0.

Relay monitor recorded November 12 outages 15:37:50–15:42:38 (4m48s) and 15:43:54–15:52:38 (8m44s), Moscow time. German monitor had no November 12 downtime; its latest recorded outage was November 9 02:04:37–02:23:31, during the already documented hostname/certificate deployment period.

Relay kernel logged `soft lockup` at 15:37:41, 15:40:09 and 15:42:22 (CPU0 stuck for 26–121 seconds), followed at 15:50:38 by RCU stalls/starvation and a clocksource readout interval of approximately 483 seconds. Stacks included kworker, libata/SCSI and CD-ROM event polling. This is evidence of guest execution/kernel stalls; a kernel defect versus provider hypervisor pause/starvation cannot be established from these logs alone.

At 15:50 systemd watchdogs killed/restarted timesyncd, udevd, logind and journald; the monitoring agent timed out. Journald replaced a journal described as `corrupted or uncleanly shut down`. Nginx logged one upstream connection timeout at 15:50:46. No new kernel warnings after 15:51 at final check. No actual OOM kill was found; RCU's OOM wording was a warning about possible consequences. Current short vmstat samples showed 95–99% idle on relay and 97–100% idle on Germany after initial sampling effects. RAM available approximately 350MiB/1421MiB, root disk 18%/28% used on relay/Germany.

German warning journal today contained unsolicited SSH connection/protocol failures; no kernel warnings or TrustTunnel error/fatal/start/stop matches in the inspected journal. This does not prove absence of transient network loss below monitoring resolution.

## Changes
Local KB bookkeeping only. No service restart, configuration edit, deployment or provider operation.

## Status and risks
Requested diagnosis completed. Availability recovered; root cause of relay kernel stalls remains unproven and recurrence cannot be excluded. No repair was requested or performed. No new implementation proposal or pending session action; affected central TODO entries concern prior completed setup and remain unchanged. All SSH commands completed; no task background operations.

## Portable lesson
None. Existing permission rules were loaded and diagnostics remained read-only; no new durable user preference was introduced.

## Evening recurrence, 23:22 Moscow

A new user-reported HetrixTools alert corresponded to downtime 23:19:51–23:21:34 Moscow (103 seconds), outage ID `88a5dad6a2c9ac0230398c4423718687`. Failure logs showed ten-second connection timeouts from all four monitoring locations. At the follow-up read both monitors were UP; the relay snapshot still listed New York as failing, so complete location recovery was not yet verified.

Read-only SSH at 23:22 confirmed a new kernel `soft lockup` at 23:20:23: CPU0 stuck for 77 seconds in `kworker/0:2`, workqueue `events_freezable_pwr_efficient`, `disk_events_workfn`. Stack included libata/SCSI and `sr_check_events` / CD-ROM polling, matching the daytime symptom. Kernel is `6.12.85+deb13-amd64` on KVM. The monitoring agent timed out at the same timestamp. This establishes recurrence of guest execution/kernel stalls, but does not distinguish a guest kernel defect from hypervisor/provider starvation.

Host uptime was 3 days 21 hours; nginx remained active since November 9 with `NRestarts=0`. Relay HTTPS returned HTTP200 with TLS verification0 in 0.132 seconds; direct German HTTPS returned HTTP200/TLS0 in 0.120 seconds from the relay. No authenticated VPN session was tested. No remote mutations were performed. All diagnostic commands finished; no background operations remain. No additional repair proposal was introduced; central TODO setup entries remain completed and unchanged. Existing read-only permission expectations were followed; no new durable instruction arose.

## Deep diagnosis requested after the evening alert

Read-only full-boot kernel, platform, PCI, sysfs, pressure, vmstat, process and timer collection is saved under `/home/slnnk/ai-data/vpn-proxy-diagnostics/relay-20261112.json`; 466 retained minute samples are in `hetrix-history.json`. The local collectors change no remote configuration. Several SSH connections timed out, including the later 20-second timing sampler; no continuous timing result was obtained. A German SSH jump attempt was denied by its forwarding policy, without any configuration change.

The full journal contains five soft lockups (77/26/51/121/77 seconds). Four have the CD-ROM path; one has `drm_fb_helper_damage_work` / `qxl_ring_push`. All include interrupt restoration at `_raw_spin_unlock_irqrestore`; this is not evidence of a spinlock acquisition deadlock. Timer/softirq code also appears. The common device-emulation boundary makes QEMU/KVM execution stalls a leading hypothesis, not a proven root cause. The initial CD-ROM-only hypothesis is insufficient because of the independent QXL trace.

Guest has one vCPU, clocksource `kvm-clock`, QXL, and unused `sr0` (`QEMU DVD-ROM`) on AHCI `0000:00:0b.0/ata17`. Root disk is virtio `vda`, not that AHCI controller. CD event polling inherits2000ms via per-device-1; IRQ35 advanced twice during the short collection, without an observed interrupt storm. Zero I/O errors, ATA resets/failed commands, OOM kills or NETDEV watchdog events in this boot's kernel journal. Root usage18%, available RAM341MiB; memory pressure averages0. No sysstat/atop history exists.

At23:17, CPU3.31%, steal0.38%, iowait0.15%, RAM56.89%, load0.45; at23:20 load7.09 while CPU3.45%, steal0.18% and iowait2.91%. Samples missing23:18–19. Daytime gap spans15:36–49; the15:50 sample has steal14.17% and load14.02, so it cannot reconstruct the freeze itself. A live one-second vmstat interval showed25%steal, but a short isolated sample does not establish minutes of host starvation. Guest clocks agreed to approximately208microseconds over the logged482.838-second interval: this is a missed-check interval, not proof of clock skew. No observed scheduled maintenance timer coincides with both outages.

Leading hypothesis: host/QEMU execution or emulation stalls; guest kernel/virtual-device defects remain possible. Exact host scheduling, BQL, storage, memory, pause/backup/migration data and QEMU version are unavailable. No provider credentials/access route were found among relevant local environment variable names. A support request draft is local at `/home/slnnk/ai-data/vpn-proxy-diagnostics/provider-request.txt`, not sent. User was asked for panel/hypervisor access. Remaining root-cause work is tracked in central TODO; earlier completion statements apply only to the initial availability checks. Disabling CD-ROM polling is at most a future controlled test, not an established repair; no remote mutation or reboot was performed. Final monitor read is UP in all four locations; all task subprocesses finished, no background operations remain.

Sources: [Linux ATA queue path](https://github.com/torvalds/linux/blob/v6.12/drivers/ata/libata-scsi.c), [QXL ring path](https://github.com/torvalds/linux/blob/v6.12/drivers/gpu/drm/qxl/qxl_cmd.c), [disk-event polling semantics](https://github.com/torvalds/linux/blob/v6.12/block/disk-events.c), [KVM steal-time semantics](https://docs.kernel.org/virt/kvm/x86/msr.html). [Red Hat similar CD-ROM stack](https://access.redhat.com/solutions/6704891) is corroborating symptom evidence only; its resolution is subscription-restricted and was not read.

## VM-side diagnostic test proposed

The user has no access to the physical host and asked about guest-side actions. Proposed first step, awaiting explicit approval: set `/sys/block/sr0/events_poll_msecs` to0 on `dline-spb-01` for a temporary single-variable test. Current recorded value is-1, inheriting2000ms; rollback is-1, and no persistent rule is proposed. Read back the setting and check nginx/HTTPS immediately; assess subsequent kernel/monitor evidence over24–48hours. No recurrence in a short interval cannot prove repair. Recurrence without the CD polling path weakens that trigger hypothesis; the QXL stack remains an independent reason not to claim a CD-only cause. No VM change or monitoring schedule has been applied. Host-side evidence remains unavailable to the user; support can still be requested independently.

## Temporary CD-ROM polling change approved and applied

User explicitly approved the proposed temporary change and reported another outage. HetrixTools outage `f01ce0d6bced37239ec200d74321f9da` lasted23:28:55–23:31:28 Moscow (153 seconds), before the change. Pre-change kernel tail shows another QXL stack at23:29:46 and a33-second CD-ROM soft lockup at23:30:28/30.

At23:32:14 Moscow, read old value-1, set `/sys/block/sr0/events_poll_msecs` to0 and read back0. Nginx active sinceNovember9, NRestarts0; relay HTTPS200/TLS0 in0.140seconds. Independent SSH at23:32:27 confirmed0, no kernel entries since23:32:14, nginx active, HTTPS200/TLS0 in0.135seconds. Monitor read UP in all four locations. This verifies application and immediate health only;24–48hour recurrence assessment remains pending. Setting is temporary and may reset after reboot; rollback-1. No persistent config, reboot or QXL change was authorized or performed.

User asked what can be done with QXL. Proposed guest-side option is `qxl.modeset=0` at boot, confirmed by upstream qxl driver source; this needs a separately approved boot configuration change and reboot, and may remove QXL graphical console output. It remains a hypothesis test, not a proven fix. https://github.com/torvalds/linux/blob/v6.12/drivers/gpu/drm/qxl/qxl_drv.c

## Observation selected by user

The user chose to observe after the temporary CD-ROM polling change. QXL boot changes and reboot are deferred, not authorized. No automatic monitoring job or background command was started; existing HetrixTools monitoring remains the source of alerts. Recurrence assessment stays open in central TODO; revisit kernel evidence on a new alert or after the proposed24–48hour observation period. No additional remote checks were run for this decision.

## Recurrence with CD-ROM polling disabled

User reported another problem during observation. HetrixTools outage `c2a558c2aebf9efaaf2c5960a32c4f47` lasted23:40:48–23:41:35 Moscow (47seconds); last monitor snapshot UP with NewYork still failing. Read-only SSH at23:42:01 confirmed `/sys/block/sr0/events_poll_msecs=0`, unchanged uptime (no reboot), nginx active/NRestarts0, relay HTTPS200/TLS0 in0.165seconds.

The inspected post-change kernel tail includes a41-second CPU0 lockup at23:36:34/35 and a53-second lockup at23:41:03/04, both `drm_fb_helper_damage_work` -> `qxl_ring_push` -> interrupt restoration; RCU starvation at23:39:09 also has a QXL workqueue stack. The tail begins during an earlier23:34:39 dump, so no claim of complete post-change stack coverage is made. CD-ROM polling-disable is insufficient to prevent recurrence. QXL remains an observed stall context, not a proven root cause; host emulation stalls remain possible.

The planned24–48hour wait is superseded by observed recurrence. Next proposed test is boot-time QXL disable with `qxl.modeset=0`; no QXL edit or reboot was performed. Proposed preparation is a dedicated `/etc/default/grub.d/99-qxl-diagnostic.cfg` appending `qxl.modeset=0`, followed by GRUB regeneration and inspection; this needs explicit approval before remote writes, and reboot remains a separately approved action. Reboot would reset the temporary sr0 setting unless separately addressed; do not silently reapply it or add persistence. Potential loss of graphical console output and inability to attribute a reboot-only improvement to QXL remain limits. All read-only commands finished; no task background operations remain.

## QXL boot-disable and persistent CD-ROM rule authorized

User explicitly authorized preparing QXL disable, subsequent reboot, and persistence of CD-ROM polling-disable across reboot. This supersedes the previous deferral for these exact actions. Read-only preflight confirmed old boot ID `a3d34241-203a-490b-95cd-e3b7fc09032b`, kernel/initrd present, root18%used/7.7GiBfree, no dpkg audit output, and absent task target files.

At23:47:43 Moscow installed `/etc/default/grub.d/99-qxl-diagnostic.cfg`, appending `qxl.modeset=0` to `GRUB_CMDLINE_LINUX`, and `/etc/udev/rules.d/99-cdrom-polling.rules` matching block sr0 add/change and assigning `events_poll_msecs=0`. Old `/boot/grub/grub.cfg` and bootID saved in `/var/backups/vpn-proxy-qxl-20261112/`. `sh -n`, `udevadm verify` (1success/0failure), `update-grub` and `grub-script-check` passed. All generated Linux entries contain qxl.modeset=0; existing root UUID and quiet/recovery arguments retained. Local apply and verify scripts are in `/home/slnnk/ai-data/vpn-proxy-diagnostics/`.

Sent one user-authorized `systemctl reboot`. It returned0. Read-only check at23:48:31 still observed old boot/old parameters and then connection was closed by the remote host; this does not establish successful reboot. Subsequent SSH and workstation HTTPS timed out; latest HetrixTools downtime `2382c611ce37a152af51ce80304e02d9` began23:49:57 and was ongoing at the latest read. Its prior UP/agent sample were from before shutdown. No second reboot, force restart, rollback or provider action was attempted. User was asked for panel VNC/serial-console status. Reboot completion and actual persistence remain pending verification; record the eventual outcome below.

## Console screenshots and panel status

User supplied two screenshots: a blank console view and a separate view reporting `Something went wrong, connection is closed`. Neither contains guest boot output or an OS error. User reports panel status `Активен`; this does not establish successful guest boot. At23:53 Moscow HetrixTools remained DOWN at all four locations; another read-only SSH check timed out. Requested a fresh console connection from the panel; that outcome is not yet known. A QXL-disabled framebuffer can lack graphical output, but a console-client connection-closed message alone cannot establish QXL causality or a hypervisor fault. No new restart, stop/start, reset or remote mutation was performed.

## Access recovered and boot settings verified

User reported a forced reboot via provider panel. Subsequent read-only checks first saw connection refused/timeouts, then succeeded at23:55:50 Moscow. New bootID is `7a7fc431-ac3d-4ce5-a7fd-6752f194db49`; kernel command line includes `qxl.modeset=0`; QXL PCI device has no bound driver and `/proc/fb` is empty. `/sys/block/sr0/events_poll_msecs=0` confirms persistence after boot. Nginx and SSH active; failed units0. Pinned relay HTTPS200/TLS0 in0.208seconds. Exact attribution of this boot to the earlier soft reboot versus the user's reported panel reset is not established solely from these observations; new boot and applied settings are verified.

Full new-boot snapshot is `/home/slnnk/ai-data/vpn-proxy-diagnostics/relay-after-qxl-reboot-20261112.json`. It records CPU0 soft lockups21seconds in `scsi_eh_12` / `ahci_scr_read` / SATA reset handling and87seconds in `pm_runtime_work` / `xhci_urb_dequeue` / USB runtime suspend, plus RCU starvation. Reported timestamp23:54:14; no later lockup in the collected boot journal through23:56. QXL is disabled, so it is not required for all observed stalls; these boot-time device-init/power-management stalls are not proof of identical causality to the earlier steady-state outages. Host emulation/execution versus guest-kernel cause remains unresolved. Initial vmstat line is boot-to-date, not a current-load sample; subsequent one-second samples were85–100%idle, steal0. Available RAM385MiB, root18%used.

The requested configuration and boot verification is complete; root-cause/recurrence work remains open in central TODO. Latest monitor at23:56 still DOWN overall while Frankfurt and Amsterdam recovered; NewYork/Warsaw remained down in that snapshot. No new remote mutations or reset commands were performed by the agent after the user's force-reboot report. All task commands finished; no background operations remain.

## Provider migration preferred and diagnosis stopped

Final monitor read recovered toUP at all four locations, status-change timestamp1794516995 (23:56:35 Moscow). SSH/nginx/HTTPS and boot settings were already verified. User then stated preference to change hosting provider and no desire to continue investigating this provider. Further current-provider root-cause diagnostics are stopped by user decision, not completed by a demonstrated repair. Existing QXL/polling changes remain applied; no rollback or further runtime action was requested. Central TODO closes the diagnostic follow-up without claiming the cause fixed and records provider migration planning as a proposal; destination is not selected and no purchase, provisioning, DNS change or deployment is authorized. All task commands finished; no background operations remain.
