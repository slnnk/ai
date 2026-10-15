---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, nomad-test, buildapi]
---

## Summary

User declared test8 obsolete and requested removal of resources deployed by Jenkins5831. Subsequently limited further cleanup to BuildAPI only.

## Actions and results

5831 had completed SUCCESS in413268ms. Four exact Nomad jobs were purged: youdo-test8, youdo-static-test8, mssql-test8, elasticsearch-test8. Final GET showed no matching jobs or active allocations. Dedicated ES CSI volume test8-vk-csi-es, external Cinder4491f1d7-6cf1-40a0-865f-dcb684d72a55,5GiB, was deleted after claims released; final GET404. Seeds and snapshots preserved.

A combined additional metadata command was interrupted before execution. GET confirmed both Consul keys static/test8/manifest.json and test_instances/test8/mssql_db still existed. Following user restriction, no further Consul/PG/S3/Redis/Rabbit cleanup was performed.

BuildAPI-only deletion executed in its API pod, Mongo filter exactly {instance:test8}, using existing MONGO_URI/MONGO_DBNAME from runtime environment without printing secrets. Removed one document each from builds, allbuilds, ms_builds. Every affected collection has zero test8 records; counts of non-test8 documents unchanged. No other collection had test8 records.

## Files and access

Helpers and evidence: ~/ai-data/jenkins-recovery/remove-test8.py, test8-buildapi-db-cleanup.py, test8-cleanup/*.json. Kubernetes access via existing BuildAPI kubeconfig and local VK auth plugin. No repository modifications.

## Limits

Shared Redis job and RabbitMQ retained. PostgreSQL, S3 data and Consul keys intentionally retained under user scope correction. Initial inspection still had the stopped static allocation pending; final verification confirmed all allocations stopped. CSI DELETE returned empty success body, causing local JSON parse failure; read-back404 established removal without reissuing DELETE.
