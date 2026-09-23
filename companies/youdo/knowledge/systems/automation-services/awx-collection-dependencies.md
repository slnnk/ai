---
system: automation-services
status: verified
checked: 2026-09-01
tags: [awx, ansible-collections, execution-environment, galaxy]
---
# automation-services: AWX collection dependencies

Last verified: 2026-09-01

## Context

- Repository: `/home/slnnk/git/automation-services` (`git@gitlab.youdo.sg:sysadmins/automation-services.git`).
- GitLab MR: `sysadmins/automation-services!1319`, branch commit `c69876db` (`AP-1756-drop-requirements`), merged into `master`.
- The MR deletes only `collections/requirements.yml`.

## Verified behavior

- Before the MR, AWX detected `collections/requirements.yml` during every project synchronization and downloaded `community.general >=10,<11`, `community.docker >=4,<5`, and `community.windows >=2,<3` from Ansible Galaxy.
- According to the commit rationale, those downloads used external Internet access dozens of times daily; 4 of 254 synchronizations failed and consequently failed the following job.
- The collections are now baked into `registry.youdo.sg/youdo/base-images/awx-ee:24.6.1` under `/usr/share/ansible/collections`. The versions recorded as checked in the production AWX pod as UID 1000 are `community.general 10.7.9`, `community.docker 4.8.8`, and `community.windows 2.4.0`.
- Therefore AWX users, including newly onboarded employees who launch existing templates, should not need a separate collection-installation step. Project synchronization is less dependent on Galaxy availability.

## Onboarding/local-development caveat

- A plain local clone does not provide the AWX execution image and, after this MR, no longer contains a manifest for the three collection dependencies.
- Local playbook runs may fail with missing modules unless the employee uses the same AWX execution image or independently installs compatible collection versions.
- The repository README documents external *roles* via a generic `requirements.yml`, but does not document the AWX execution image or local installation of these *collections*. The remaining `playbooks_old/requirements.yml` is not a replacement.
- Recommended follow-up: add a short contributor/onboarding section that names `awx-ee:24.6.1` as the canonical runtime and either documents container-based local execution or gives a pinned local collection-install command. Avoid restoring `collections/requirements.yml` at the AWX auto-discovery path unless repeated downloads are intentionally re-enabled.

## Useful checks

```bash
git show c69876db
git merge-base --is-ancestor c69876db origin/master
git grep -n 'community\.general\|community\.docker\|community\.windows' origin/master
```

## Related

- Local Ansible access to Vault: `local-vault-ansible-access.md` (same directory).
