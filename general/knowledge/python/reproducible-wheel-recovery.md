---
system: python
status: verified
checked: 2026-10-13
tags: [python, pypi, recovery, reproducibility]
---
# Recover exact locked Python distribution hashes

## Summary

A rebuild from the original source can match locked wheel and source-archive SHA256 values when its historical build tools are restored. Check both hashes before publication; equal version numbers alone do not prove identical artifacts.

## Symptom

A private package registry is rebuilt without original distribution files. Consumers use frozen locks containing absolute artifact URLs and SHA256 values. Building the original release with current tools produces a different wheel hash.

## Cause

PEP517 build isolation usually resolves available backend versions today. A backend or versioning-plugin update may change distribution metadata or packaging even when application source is unchanged.

## Fix

1. Seek original artifacts in backups, CI artifacts and caches first. Record expected wheel/source hashes from consumers and identify the original release source and timestamp.
2. Build untouched release source using its required Python/platform. Compare both generated hashes; do not publish mismatching bytes as a recovered locked asset.
3. Inspect official PyPI release metadata for build backends and versioning plugins available before the original release cutoff. Install historical candidates into the build environment and disable build isolation explicitly (`--no-build-isolation`) so those candidates are actually used.
4. Rebuild and compare SHA256 values against consumer locks. In a verified case, pinning two top-level tools reproduced both exact artifacts without source changes.
5. Publish only after authorization. Verify target registry metadata reports expected names, versions and hashes, without downloading packages when metadata suffices. Then retry a representative frozen consumer build under its normal network and credential conditions.

## Limits

Release cutoff identifies candidates, not proof of original versions. Two top-level pins may be insufficient; transitive build dependencies, timestamps, locale, Git metadata, interpreter and platform can affect output. A source archive may lack Git metadata required by versioning. Never bypass hash checking to conceal mismatches. If exact reproduction fails, recover original bytes or explicitly review source/lock changes. Keep credentials in runtime secret access paths and generated distribution evidence outside documentation repositories.
