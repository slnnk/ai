---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, elasticsearch, vk-cloud, ansible, DevOps-894]
---
# DevOps-894 test stand thick ES deployment through Ansible

## Summary

Elasticsearch for stand test with the thick dataset successfully deployed through the prepared Ansible playbook. Final run used stop_es,run_es, retained the already-created40GiB CSI disk, and completed exit0/failed0 in60.037s. User steering additionally removed every direct VK API call from the deployment; Nomad now owns CSI volume provisioning and snapshot lookup.

## Task

DevOps-894: launch ES in Nomad for test (large database), strictly through deploy_es_nomad.yml.

## Context

User explicitly requested the deployment and clarified it must use the prepared Ansible playbook. Later user required the deployment to interact only with Nomad; this supersedes the earlier cloud-authentication/snapshot lookup/readiness implementation. Seed preparation remains a separate cloud-aware playbook. Existing branch approval covers local corrections; actual deployment is separately authorized by this request. No Git publication performed.

## Actions

Used local wrapper `python3 ~/ai-data/devops-894-playbooks/run_test_es.py`, which runs `ansible-playbook -i inventories/vk_es/hosts playbooks/deploy/docker/deploy_es_nomad.yml -l vk_es -e instance=test -e instance_type=thick`. Job is elasticsearch-test, namespace default, DCvk-test; volume test-vk-csi-es,40GiB, pluginvk-csi. No ad-hoc job submission or Docker command was used.

First attempt stalled deleting a nonexistent volume. GET confirmed volume and job404; interrupted that run and restored only existence handling: skip CSI delete when Nomad volume is absent. The next full playbook created Cinder disk62bf8889-a3b2-4be2-8f3c-21711b7112cd, but deployment failed after127.754s: CSI attempted Nova attach while disk statuscreating, then Nomad progress deadline expired. Existing disk was preserved for retries.

User requested Nomad-only deployment. Removed direct Cinder auth/lookup/poll tasks, switched snapshot selection to Nomad CSI snapshot list, and added Nomad rescheduling for transient attach failures. A retry was rejected immediately because old CLI defaults filled attempts3 alongside unlimitedtrue. Explicit attempts0, interval0 resolved that validation conflict. Final `run_test_es.py --tags stop_es,run_es` used the existing disk and succeeded.

## Findings

Final Ansible recap: ok6, changed2, unreachable0, failed0; commandexit0,60.037s. Blocking nomad job run monitored deployment success. No additional ES/index/HTTP checks were run, as requested by the user.

Initial failed allocationf09315a9-2ca1-415c-90ed-624173d5c6cb reported CSI ControllerPublishVolume Nova400: volume must beavailable but wascreating. Failed deployment6b38d1af-b64c-a58a-690e-326abb4da3ab expired progress deadline. The final successful deployment follows the corrected job spec and the already-created disk; source data was not recopied or rebuilt for retries.

## Changes

Local es_vk_deploy.yml now handles an absent previous volume; Nomad-only snapshot selection and reschedule changes are detailed in [Nomad-only design](2026-10-14-nomad-test-devops-894-nomad-only-deploy.md). Local runner imports only Nomad/Consul credential names for this deployment. Censored log: ~/ai-data/devops-894-playbooks/deploy-test-thick.log; first failed deployment log retained separately. No tokens/credentials written into notes or command arguments.

Configured service addresses added to current/service-addresses.env: elasticsearch.test.vk-test.youdo.local, elasticsearch-auth.test.vk-test.youdo.local, eshead.test.vk-test.youdo.local. Comment marks Nomad deployment success and unprobed DNS/HTTP routes.

## Limits

Application routing/data responses were not independently checked; success criterion is Nomad deployment only. AWX/DAG migration and Git publication remain separate tasks. Backlog is in ~/ai/TODO.md.

## Portable lesson

none
