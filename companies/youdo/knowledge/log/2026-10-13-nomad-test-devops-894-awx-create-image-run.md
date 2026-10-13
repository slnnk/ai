---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, elasticsearch, vk-cloud, ansible, awx, DevOps-894]
---
# DevOps-894 AWX create_image stage execution

## Summary

Executed the user-requested first AWX playbook stage locally: recreate_es_base_image.yml --tags create_image with VK inventory. Two new thin/thick snapshots are available. Both seed mounts restored and temporary validation resources removed. Actual successful run exit0, failed0. During completion the user requested removing clone/ES validation from future publication runs; local code now publishes available snapshots directly without Nomad or source ES API calls. No rerun creating redundant snapshots was performed.

## Task

DevOps-894: execute the base snapshot preparation stage intended for AWX, then simplify it according to user steering.

## Context

User explicitly instructed running stage1. The concrete create_image operation, including temporary unmount, candidate creation and then-current clone validation/cleanup, was described before execution. This authorizes this run, not subsequent delete_image cleanup or stand deployment. AWX itself remains unavailable; the same entrypoint/tag was executed from the existing local checkout. Credentials read from existing current/.env names into process environment, never written into command arguments or notes. SSH as youdo with sudo on share10.18.26.4.

## Actions

Ran `python3 ~/ai-data/devops-894-playbooks/run_create_image.py`, wrapping `ansible-playbook -i inventories/vk_es/hosts playbooks/deploy/docker/recreate_es_base_image.yml --tags create_image -l vk_es`. First attempt exited2 before mutation: YAML flow list split UUID,FSTYPE into two findmnt argv values. Quoted the single argument in es_vk_publish_variant.yml and retried the same approved stage. Actual findmnt, snapshot creation, remount and then-current restoration validation passed. Censored Ansible task output stored at ~/ai-data/devops-894-playbooks/create_image.log, mode0600. Wrapper uses only required environment names and hides skipped-host chatter.

Successful recap: ok90, changed6, unreachable0, failed0, skipped0, rescued0, ignored0; wrapper exit0. Separate snapshot GET collected nonsecret resource IDs, status and publication metadata. delete_image was not run; previous artifacts retained. No staging, commit, push or AWX infrastructure changes.

## Findings

| Variant | Name | UUID | Size | Status | Source volume |
| --- | --- | --- | --- | --- | --- |
| thin | vk-ms1-share-base-thin-20261013205203 | 0d38e5f9-3c42-4923-9e29-4c50bb1de70c | 5 GiB | available | ad66e572-b39a-4ed7-86a6-eb5a094763cb |
| thick | vk-ms1-share-base-thick-20261013205344 | ef5fb5f1-c828-4605-9f1c-81022edd988b | 40 GiB | available | 6b8a8094-227f-4eb2-968c-5469e98fd92c |

The completed run used the original validation path and set es_validated=true. Source seed filesystems were remounted through fstab. Both temporary ES validation jobs stopped/purged and their cloud volumes deleted. User asked whether this validation existed in Yandex; answer: no, historical playbook only deleted/created images. User then explicitly requested removing the added validation to prepare snapshots faster. The in-flight run had already completed by that steering message's processing; no further validation or repeated preparation was launched.

## Changes

Future create_image now only unmounts prepared seeds, creates Cinder snapshots, waits available, remounts in always and marks es_published=true. Removed all clone/ES startup/index comparison tasks and the unused es_vk_validate_publication.yml/es_validation.j2. Removed source API, seed server identity and filesystem UUID validation variables that are no longer used. Updated snapshot selection and retention to the publication marker; configured fallback UUIDs now point to the two just-created available snapshots. These fallback IDs work without changing the old cloud metadata marker. README explains the faster workflow. No metadata changes were made to existing snapshots after the completed run.

Syntax check and template parsing pass. Two local API-fixture scenarios cover direct publication with no /v1/Nomad calls and retention. git diff --check passes. No live rerun was needed because the requested snapshots already exist. Separate stand deployment uses blocking Nomad job run success only, as previously requested.

## Limits

Snapshots reflect the current prepared seed data; no new DBA_Clean run was triggered. AWX workflow/schedule and the DAG destination still need separate migration. Local branch remains unpublished. Backlog is maintained in ~/ai/TODO.md.

## Portable lesson

none
