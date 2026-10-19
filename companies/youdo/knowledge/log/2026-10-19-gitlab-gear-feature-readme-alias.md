---
system: gitlab
status: verified
checked: 2026-10-19
tags: [docker, registry, gear]
---
# Gear master image aliased as feature-readme

## Summary

User requested adding `feature-readme` to the Gear master image to unblock [job3235910](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3235910). Registry alias creation succeeded, without rebuilding or downloading image layers.

## Evidence and actions

- Job trace failed pulling `registry.youdo.sg/sysadmins/devops-tools/gear:feature-readme`: manifest unknown.
- Initial copy from literal `master` failed: no such registry tag.
- Project408 CI tags branch images as `$CI_COMMIT_REF_SLUG-$CI_PIPELINE_IID`. Registry repository294 listed `5`, `latest`, `master-5`.
- Successful master pipeline56738 has IID5 and commit `5ae35b232bc4d2f291c7511c126880e4e43b1931`; source tag `master-5`.
- Explicit user instruction authorized adding the registry alias. Executed `docker buildx imagetools create --prefer-index=false --tag registry.youdo.sg/sysadmins/devops-tools/gear:feature-readme registry.youdo.sg/sysadmins/devops-tools/gear:master-5`, exit0.
- Published manifest digest `sha256:262285d5fa853e8310e65b60105f7de0e6e7d381a24757d1e2926ac1cee6ebdb`.

## Changes and limits

Only the requested registry tag and local KB records changed. No Git branch, source change, rebuild, runtime test or CI retry. Missing-image failure addressed; subsequent job execution remains unobserved.
