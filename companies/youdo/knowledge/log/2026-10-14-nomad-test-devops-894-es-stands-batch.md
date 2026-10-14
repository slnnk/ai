---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [ansible, elasticsearch, DevOps-894]
---
# DevOps-894 Elasticsearch deployment for test1-7 and test10-15

## Summary
All13requested Elasticsearch stands deployed through the prepared Ansible playbook: test1–test7 and test10–test15. test1/test6 use thick40GiB; remaining11stands use thin5GiB. Each final deployment returned success through blocking Nomad job run.

## Task
User authorized deploying Elasticsearch for the13stands. Existing test deployment was not changed.

## Context
Repository automation-test-yandex, approved local DevOps-894 branch, vk-test/default, vk-csi. Existing group_vars selects thick for test1/test6 and thin by default. Cinder readiness polling enabled.

## Actions
Ran run_es_batch.py --instances test1 test2 test3 test4 test5 test6 test7 test10 test11 test12 test13 test14 test15 --workers3, using actual Ansible entrypoint for every stand. Batch315.412s,12/13initially passed. test3initial129.131s attempt exceeded Nomad healthy_deadline1m while tasks were starting and an image was downloading. Diagnostic allocation076c4edc-d49c-8958-7c27-aedf02e7df85 was running but marked unhealthy for missing min_healthy_time10s before deadline. Retried test3with run_test_es.py --instance test3 --instance-type thin --tags stop_es,run_es, preserving the created disk. Retry succeeded62.088s, exit0/failed0. Final13/13successful. No ES HTTP/index checks or Git publication.

## Findings
Initial seconds: test1 thick84.834; test2 thin63.293; test3 thin129.131failedthen62.088successfulretry; test4 thin63.902; test5 thin70.603; test6 thick69.515; test7 thin59.815; test10 thin71.276; test11 thin47.300; test12 thin64.944; test13 thin61.182; test14 thin55.508; test15 thin53.752. Claim-release and disk available waits remained enabled. Container start timing caused the test3deadline miss; downloading was observed but its precise contribution was not measured.

## Changes
13stand jobs and CSI disks deployed. Local run_test_es.py generalized with explicit instance/type and per-stand logs. Local bounded batch helper and results at ~/ai-data/devops-894-playbooks/{run_es_batch.py,batch-deploy-results.json}. Configured stand service routes recorded in current/service-addresses.env with observed deployment status, without DNS/HTTP probes. Repository code unchanged this batch.

## Open items
Git publication and DAG/AWX migration remain in ~/ai/TODO.md. User subsequently proposed moving ES images into the internal registry via base-images; investigation started without authorizing Git publication or redeployment.

## Portable lesson
none
