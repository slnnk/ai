---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [mailer, smtp, vk-test, postfix]
---
# VK test mailer SMTP rejection and runtime failures

## Summary

Mailer8.1.10 is running, but SMTP delivery is rejected by postfix-test. Mailer egress is 85.192.34.208; this /32 is absent from effective Postfix mynetworks. postscreen_access_list=permit_mynetworks. Untrusted mailer sessions trigger PREGREET and BARE NEWLINE and receive5505.5.1Protocol error; sessions passing postscreen receive554Relay access denied. User approved recovery ("Примени"). Added only 85.192.34.208/32 to persistent and effective mynetworks on postfix-test; postfix check and reload succeeded at 2026-10-16 11:26:42 UTC. No repository edits authorized/applied.

## Task and context

User reported test5 LogReader MailerSendMessageException on2026-10-16. User prohibited superpowers skills. Investigated source, Nomad state/logs and SMTP server read-only. User supplied VK VM screenshot: postfix-test10.18.26.49/public138.16.203.115. DNS mail.youdo.sg resolves to that public IP.

## Actions and evidence

- Nomad GET /v1/job/mailer, allocations, allocation task events and bounded logs. Runtime image8.1.10, SMTP mail.youdo.sg:25, MailFrom=noreply@mail.youdo.sg. Source checkout differs in sender default; use runtime facts.
- All21mailer allocations running:10scheduler,10dispatcher,1API. Pechkin3allocations running.
- Server logs /data/postfix/docker-data/dms/mail-logs/mail.log correlate85.192.34.208 sessions with PREGREET19after0 (HELO before complete greeting), BARE NEWLINE after HELO, then RCPT550Protocol error. Other sessions from same address receive554Relay access denied.
- Effective docker exec mailserver postconf mynetworks postscreen_access_list postscreen_greet_action postscreen_bare_newline_action smtpd_relay_restrictions smtpd_recipient_restrictions confirms no VK egress /32, permit_mynetworks postscreen bypass and enforce actions.
- Full-greeting SMTP envelope probes from VK node10.18.26.21 used HELO/MAIL FROM/RCPT/RSET/QUIT only; no DATA or mail delivery. LF and CRLF both reached relay denial. Probe passed postscreen and temporarily populated its pass cache for this source; this does not grant relay access or fix production clients.
- SSH mail.youdo.sg had stale ECDSA key. User explicitly confirmed new VM fingerprint SHA256:aEjQhLXzvORPqv+x3opIXfwlsvAnK/ZQDPJkhXeqM3Q. Internal and public endpoints match. Pinned task-local known_hosts; original known_hosts unchanged. SSH asyoudo+sudo works.

## Other findings and limits

- All10scheduler allocations have historical OOMKilled exit137 events;1–2restarts each. Do not attribute SMTP protocol rejection to OOM.
- API17historical restarts, stderr includes53300too many clients and57P01administrator termination. Current API is running; database capacity has not been re-audited here.
- Scheduler exception logger repeatedly fails with System.Data.SqlClient assembly mismatch, expectedVersion4.6.0.0. This is separate from the SMTP rejection.
- Source src/src/YouDo.Mailer.Smtp/SmtpClient.cs uses default Linux LF, reads one greeting line in a separate buffered reader and does not fully handle multiline SMTP greetings. Fixing client protocol would still leave missing relay authorization.
- Canonical role automation-services/roles/mailserver_test/templates/postfix-main.cf.j2 contains old network list. Persistent live override /data/postfix/docker-data/dms/config/postfix-main.cf. Live container mailserver, docker-mailserver14.0.0. Deployment config must eventually retain approved recovery; repository editing requires branch-stage approval.
- No external message sent. Runtime mutation limited to the explicitly approved SMTP trust update and reload; diagnostic connections also affect the postscreen pass cache. No Git state changes. Source-address stability/other VK egress addresses not audited.

## Changed local files

- Evidence/helper files: ~/ai-data/mailer-vk-diagnosis/ (GET/log summaries, SMTP probe, pinned public SSH key).
- This log, existing nomad-test map, service-addresses.env and central TODO.

## Proposed recovery and risks

Append85.192.34.208/32 to existing persistent and effective mynetworks, validate config and reload Postfix in mailserver on10.18.26.49. This grants SMTP relay and postscreen bypass to every client using that exact NAT address. Preserve all existing trusted networks. Remote change requires explicit user approval. Delivery verification should initially stop before DATA; actual test-message sending is a separate external action. Reconcile Ansible after separately approved repository branch.

## Approved recovery result

User explicitly approved applying the proposed runtime fix. Applied through one remote command via youdo + sudo. Before editing, asserted persistent/effective network lists match, preserved all existing entries and created backup `/data/postfix/docker-data/dms/config/postfix-main.cf.before-vk-trust-20261016T112641Z`. Updated persistent override and effective container config with `postconf -e`, then `postfix check` and `postfix reload`; all exit0.

Both LF and CRLF probes from VK node10.18.26.21 now receive2502.1.5Ok on RCPT, followed by RSET/QUIT without DATA. Read-only log audit since server time11:26:42 reports9ALLOWLISTED sessions,0protocol errors,0relay denials,7ordinary mailer DATA sessions. All7hit existing test header-discard rules; this proves SMTP acceptance, not delivery to external inboxes. No test-filter changes made.

Canonical Ansible template still lacks the new /32. A subsequent role application could overwrite this recovery; repository branch/edit approval remains required. OOM, historical PostgreSQL failures and logger assembly mismatch were not changed.

## Ansible follow-up and training record

User requested preserving the SMTP change in Ansible and asked whether mailer variables need changes. Proposed repository automation-services, base origin/master (observed454ef804), branch DevOps-898-trust-vk-smtp-egress. Stage1branch approval pending; repository files unchanged. Planned scope: append85.192.34.208/32 to existing mynetworks in roles/mailserver_test/templates/postfix-main.cf.j2. Existing unrelated local changes remain present. Stage2publication approval not requested yet.

Mailer Host=mail.youdo.sg and Port=25 remain correct: DNS resolves to the new VK SMTP VM. No mailer variable change is needed for this recovery. Runtime MailFrom=noreply@mail.youdo.sg differs from checked-out HCL noreply@mail.youdo.com, but both sender forms were accepted by SMTP; sender normalization is outside the minimal relay fix.

## Ansible implementation and publication proposal

Stage1approved by user "Да". Fetched origin; master advanced from454ef804 toac136015 (public-test merge). Created approved branch DevOps-898-trust-vk-smtp-egress from current origin/master ac136015 in existing checkout. Unrelated local changes preserved; index empty. Exact task diff: one line in roles/mailserver_test/templates/postfix-main.cf.j2, appending85.192.34.208/32 to mynetworks. Original no-final-newline preserved.

Validation passed: byte comparison against HEAD confirms only exact suffix addition; strict Jinja render matches intended bytes; all CIDRs parse strictly and new /32 is unique; task-scoped git diff --check clean. Whole-worktree diff check sees pre-existing trailing whitespace in unrelated runner cron template, untouched. No new test file added for this static change. Existing runtime equivalent was postfix-check/reload/SMTP verified earlier.

Proposed commit `allow vk egress in test smtp networks`. MR title `DevOps-898 allow vk egress in test smtp networks`. Source DevOps-898-trust-vk-smtp-egress -> master, repository sysadmins/automation-services. MR body:

```text
Добавлен исходящий IP VK 85.192.34.208/32 в доверенные сети тестового SMTP-сервера, чтобы mailer мог отправлять письма после переноса в VK.

https://youtrack.youdo.com/youtrack/issue/DevOps-898
```

 Stage2publication approval pending. CI contains only Molecule nginx/Consul/Nomad; changed path does not select automatic test jobs, Nomad fallback is manual. No automatic deployment. Ordinary mailserver_test role application not requested; template currently not published.

## Publication result

Stage2explicitly approved by user "Да" for reviewed commit/push/MR publication. Staged only roles/mailserver_test/templates/postfix-main.cf.j2; inspected actual staged diff and asserted exact approved suffix addition. Committed `ff104e33c385f9ac177b4f8afc5596de9d6457d7` (`allow vk egress in test smtp networks`), pushed branch DevOps-898-trust-vk-smtp-egress and created [MR1379](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1379) (`DevOps-898 allow vk egress in test smtp networks`) into master. GET verification confirmed remote SHA, source/target, assignee a.solonenko, squash=false, remove-source-on-merge=true. Pipeline141074 status skipped. No merge or Ansible run performed. Original unrelated worktree status preserved exactly; index empty. Repository changes are published and await merge; SMTP runtime fix remains active and verified.

## Merge result

User explicitly requested merging MR1379 (2026-10-16). Before merge, GET confirmed opened/mergeable/no conflicts, expected source/target and ff104e33 SHA; exact single-file/single-line trust addition rechecked. Merged via SHA-guarded GitLab API preserving squash=false and source-removal-on-merge=true. GET verified state merged, merge commit `200eada5b92c127486c366f486eb5e0f356f88e2`, master HEAD equals that commit, parent list includes ff104e33. Merged at2026-10-16T14:33:06+03:00. Canonical Ansible now preserves the already-applied runtime SMTP trust. No Ansible run or additional runtime change performed. Repository checkout remains on task branch with unrelated local changes preserved.


## Read-only recheck at 13:44 UTC

User reported mailer delivery failures again. Fresh Nomad GET shows all 21 mailer allocations running (10 scheduler, 10 dispatcher, 1 API); restart counters remain the previously observed values. A bounded 400 KB stdout scan for each scheduler found no matches for the three previously tracked exception signatures; this is a limited tail check, not proof of no application failures.

SSH to 10.18.26.49 using the task-local pinned known_hosts succeeded. Effective mynetworks still includes 85.192.34.208/32 and postscreen_access_list is permit_mynetworks. The live mail queue is empty. Recent ordinary mailer sessions from this source show ALLOWLISTED and data=1, followed by cleanup DISCARD. Examples: queue6FB0E20C7DF at13:28:02UTC, 8FBAC20C7DF at13:28:10UTC and99C2E20C7DF at13:29:47UTC. Recipients match the existing numeric-local-part @youdo.com rule; other current discards match the alphanumeric @test.ru rule. Recipient local parts are intentionally not retained.

Live /etc/postfix/header_checks contains six DISCARD patterns, matching canonical roles/mailserver_test/templates/user-patches.sh.j2. Two relevant patterns are /^To: [0-9]+@youdo\.com/ and /^To: [a-z0-9]+@test\.ru/. Thus SMTP acceptance is restored; the observed messages are intentionally filtered by the current test-server policy. Whether the newly reported specific message belongs to this set remains unverified until an approximate timestamp and recipient are supplied. No filter change, reload, test message, repository edit or external write performed.

Commands: Nomad GET /v1/job/mailer/allocations and bounded allocation stdout tails; docker exec mailserver postconf mynetworks postscreen_access_list header_checks smtp_header_checks; tail mail.log; docker exec mailserver cat /etc/postfix/header_checks; docker exec mailserver postqueue -p. A helper inspect.py completed mailer inspection but then exited on pechkin Templates=null; no runtime implication. Public-IP SSH did not match the task-local hostname entry; internal-IP SSH used the existing verified key successfully.


## Specific Yandex recipient correlation at 13:47 UTC

User supplied a Yandex recipient and approximate sending time. Exact recipient search in current mail.log found three attempts at11:55:34,11:57:03 and13:45:48UTC (14:55,14:57,16:45MSK). Queue IDs E991D20C7DF,D757F20C7DF,4871E20C7DF all trace from client85.192.34.208 through cleanup/qmgr to mx.yandex.ru77.88.21.249:25. Sender noreply@mail.youdo.sg. Every attempt ended dsn5.7.1/status=bounced with remote response `554 5.7.1 Message rejected under suspicion of SPAM` at end of DATA. Bounce notification generated and original queue item removed. The supplied address is intentionally omitted from this note; queue IDs suffice for correlation.

This specific complaint is external recipient-provider rejection, not local header DISCARD or a regression of VK relay trust. Exact antispam trigger is not identified by the SMTP response. Read-only postconf additionally shows myhostname=mail.youdo.sg, default smtp_helo_name, empty relayhost, smtpd_milters and non_smtpd_milters. A DKIM domain directory exists, but that alone does not establish signing; no key content was read. No DNS authentication or IP reputation audit completed, and no causal claim about these settings is established. No remote changes or test messages sent.


## User-requested Gmail delivery test at 14:05 UTC

User explicitly requested one test email through postfix-test to their supplied Gmail address. Sent exactly one plain-text message using local /usr/sbin/sendmail inside mailserver via SSH, envelope/header From noreply@mail.youdo.sg, subject `postfix-test VK Cloud delivery check`. This uses local Postfix injection, not the mailer application path/content. Message ID <179215952763.42175.14240179934341052936@mail.youdo.sg>, queue4DD0C20D90E. At14:05:29UTC (17:05:29MSK) Gmail MX gmail-smtp-in.l.google.com64.233.165.27 returned2502.0.0OK; Postfix dsn2.0.0/status=sent. This proves recipient MX acceptance, not inbox placement or authentication results. Gmail original-message headers remain unavailable until supplied by the user. Metadata in ~/ai-data/mailer-vk-diagnosis/gmail-test-20261016.json. No server configuration changes.


## Authentication and DNS follow-up

User clarified Gmail placed the test in spam (earlier inbox inference is superseded). Supplied original headers confirm SPF pass for138.16.203.115 and noreply@mail.youdo.sg; no DKIM-Signature and no reported DMARC result. Read-only DNS: mail.youdo.sg TXT `v=spf1 a mx ~all`, A138.16.203.115; _dmarc.mail.youdo.sg returns NXDOMAIN, _dmarc.youdo.sg TXT returns NOERROR with empty answer through system resolver. Public1.1.1.1 reverse lookup138.16.203.115 returns NXDOMAIN (no PTR); other queries to that resolver timed out. Fresh Postfix postconf again shows smtpd_milters/non_smtpd_milters empty; /etc/opendkim.conf points at KeyTable/SigningTable and socket localhost8891. No private keys read. Deficits established: absent reverse DNS, no DKIM integration/signature, no DMARC TXT returned. They do not identify a unique cause of provider antispam decisions. No DNS or server changes performed.
