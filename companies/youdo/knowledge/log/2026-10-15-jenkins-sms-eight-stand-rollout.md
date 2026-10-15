---
system: jenkins
status: verified
checked: 2026-10-15
tags: [sms, nomad, gitlab, DevOps-899]
---
# SMS parallel rollout to eight test stands

## Summary

SMS master-191 rollout accepted on all eight test/test1-test7 stands: all jobs SUCCESS101-114s, all eight Nomad allocations running/healthy/zero restarts. Local runner caches flushed as requested; Windows MSSQL negatives expired later and all12explicit DNS queries passed.

## Task and context

Project498 youdo/microservices/youdo-sms-service, master source21060f7, pipeline140987 (master-191). Existing image/pipeline reused, seven manual deploy-yandex-test jobs played and successful test5 job3228662 retried as3229460. User explicitly requested SMS deployment and runner Docker DNS cache update. No repo edits.

## Actions and evidence

Local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-sms-stands899.py launch|watch|status` launches eight jobs concurrently; receipts `/home/slnnk/ai-data/jenkins-recovery/sms-stands-20261015/`. Only GitLab/Nomad status checks requested. Existing deployment/database behavior retained.

On both runners172.28.0.171/.172, user-authorized `resolvectl flush-caches` succeeded. Direct queries to Docker upstreamDNS172.28.0.8/.9 still returned NXDOMAIN for vk-ms1-sql-test1.mcs.local. Host cache flush does not clear Windows DNS caches. No Docker restart or runner settings changed.

## Changed files and limits

Local helper/receipts and KB bookkeeping; runtime DNS cache flush only. No Windows changes, new build, application/data/HTTP or BuildAPI validation.

## Results

| Stand | Job | Status | Duration seconds |
|---|---|---|---|
| test | 3228613 | success | 113.98 |
| test1 | 3228614 | success | 111.33 |
| test2 | 3228615 | success | 100.63 |
| test3 | 3228616 | success | 111.84 |
| test4 | 3228617 | success | 106.21 |
| test5 | 3229460 | success | 105.43 |
| test6 | 3228619 | success | 103.20 |
| test7 | 3228620 | success | 112.86 |
