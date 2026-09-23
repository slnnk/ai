---
system: mail
status: verified
checked: 2026-08-12
tags: [postfix, smtp, queue, zabbix, sc-mta-01, fallback-relay]
---
# sc-mta-01.youdo.corp: Postfix

## Purpose and access

- Host: `sc-mta-01.youdo.corp`.
- Access for diagnostics: `ssh root@sc-mta-01.youdo.corp`.
- Service: `postfix.service`.
- Main log: `/var/log/mail.log`; the logs are very intensive (on 12 August 2026 the current file was about 720 MB). `journalctl -u postfix` showed no entries.
- Reduced monitoring log: `/var/log/mail.zabbix.log`.
- Queue check: `postqueue -p` or the JSON representation `postqueue -j`.
- Internal mail source seen in the logs: `sc-lb-postfix-service.youdo.corp` (`172.28.0.73`).
- Fallback SMTP relay: `172.28.0.139:25` (value of `smtp_fallback_relay`).
- Transport map: `/etc/postfix/transport`; Gmail is routed to the dedicated transport `gmail:`, Apple domains to `apple-out:`.

## Incident 2026-08-12: queue above 10 000

Notification: `PROBLEM: TRIGGER sc-mta-01.youdo.corp - Postfix queue is over 10000`.

### State at the time of the check

- At 13:42 MSK Postfix was `active`, host uptime 33 days, load average about `0.72 / 1.49 / 1.23`.
- First sample: 13 345 messages, about 960 MB.
- All messages were in the active queue, sender `noreply@mail.youdo.com`.
- Main recipient domains: Gmail 9 777, Mail.ru 1 740, Yandex 897; the rest considerably smaller.
- The queue consisted almost entirely of fresh messages accepted approximately between 13:26 and 13:44 MSK.
- Peak incoming flow: 3 332 messages/min at 13:39 and 3 205 messages/min at 13:40.
- The removal rate of successfully delivered messages during the degradation was on the order of 550-700/min.

### Cause and confirmations

The queue arose from a combination of a sharp mass incoming flow and slow direct outbound delivery. Starting at about 13:26, `/var/log/mail.log` filled with mass `Connection timed out` errors to the MX servers of Gmail, Mail.ru, Yandex, iCloud and Yahoo. After the timeouts Postfix switched to the internal fallback relay `172.28.0.139`, which accepted the mail with `status=sent`.

In the analyzed log fragment the most timeouts were to:

- `mxs.mail.ru`: 4 822;
- Gmail MX: about 4 900 in total across the main and two alt MX;
- `mx.yandex.ru`: 1 954;
- iCloud MX: about 866.

About 730-746 `smtp` processes were running on the server simultaneously, and 248-259 TCP connections were in `SYN-SENT`. `default_process_limit=500`, the regular `smtp_destination_concurrency_limit=300`; the Gmail transport is configured with concurrency 20 and a rate delay of 1 second. The likely operational cause of the delay is too high a parallelism of direct external SMTP connections during the burst, leading to timeouts and the subsequent slow fallback. To pinpoint the loss point, the external egress/NAT/firewall and provider limits need to be checked separately.

Exhaustion of the local conntrack is ruled out: there were 4 726 entries against a maximum of 1 048 576. The kernel log for the last 30 minutes had no OOM, `table full`, conntrack or drop messages. Postfix itself did not crash.

### Dynamics and outcome of the check

Without intervention the queue was decreasing:

- 13:42:53: 13 345 messages / 960 282 KB;
- about 13:43: 12 787 messages / 920 147 KB;
- 13:44:56: 12 445 messages / 895 430 KB;
- 13:45:42: 12 820 messages / 922 149 KB.

At 13:43 only 10 new messages were accepted against 576 successfully completed, at 13:44 272 against 576 completed, so the queue initially decreased. However, at 13:45 the flow resumed: in less than a minute 1 503 messages were accepted against 552 completed, and the queue grew again. Consequently, there was no sustained recovery at the end of the diagnostics and the trigger justifiably remains active. The configuration was not changed, the queue was not flushed and no mail was deleted.

### Safe commands used

```bash
systemctl is-active postfix
postqueue -p
postqueue -j
postconf -h default_process_limit smtp_destination_concurrency_limit smtp_destination_rate_delay relayhost smtp_fallback_relay transport_maps
postconf -M
tail -n 250000 /var/log/mail.log
ss -s
ss -Htan state syn-sent
sysctl net.netfilter.nf_conntrack_count net.netfilter.nf_conntrack_max
dmesg --since "30 minutes ago"
```

### TODO / further actions

- Watch the queue until it drops below 10 000 and the trigger recovers; the speed depends on the continuing waves of the incoming mass mailing.
- If the incident recurs, correlate the bursts with the initiator of the mass mailing behind `sc-lb-postfix-service`.
- Check limits/losses on the external SMTP egress or NAT at the moment of high parallelism.
- Consider a controlled reduction of the concurrency of the regular `smtp` transport or dedicated transports/rate limits for the large providers; change only after assessing the required throughput.
