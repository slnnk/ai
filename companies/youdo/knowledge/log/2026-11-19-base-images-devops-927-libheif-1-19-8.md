---
system: base-images
status: verified
checked: 2026-11-19
tags: [docker, libheif, libvips]
---
# DevOps-927 libheif 1.19.8 in the Content base image

## Task

Prepare and verify a source build of libheif 1.19.8 for [DevOps-927](https://youtrack.youdo.com/youtrack/issue/DevOps-927).

## Context

Content CI selects `microsoft/dotnet-core-sdk:3.1-libvips` for both build and runtime. The recipe uses Ubuntu Focal, where a fresh default APT index offers `libheif-dev` and `libheif1` only at `1.6.1-1build1`.

## Actions

Proposed `youdo/base-images`, new branch `DevOps-927-build-libheif-1-19-8`, based on `master` at `f8981379402754dd7d07e512fc667946e793e06d`. The user explicitly confirmed the branch and base through the approval prompt. The remote `master` and branch absence were checked with `git ls-remote` before branch creation.

## Findings

The libheif release requests C++20. The Dockerfile uses Focal's GCC 10 for that build. The shared CI template `partials/.build-base-image-tag.yml` selects Git tags and builds and pushes the corresponding image. The current remote release tag `microsoft/dotnet-core-sdk/3.1-libvips` points to `4923b2f`.

The first image build completed, but the runtime smoke test showed an empty HEIF module. The libvips 8.13.3 Meson build detects libheif 1.19.8 and emits a dynamic module even when the older `builtin_h265_decoder` and `builtin_h265_encoder` pkg-config variables are missing. Without them it leaves the HEIF decoder and encoder macros unset. Both actual codecs were built in through Focal's libde265 and x265. Restored the two pkg-config variables and required both operations in the image build.

## Changes

Only `microsoft/dotnet-core-sdk/3.1-libvips/Dockerfile` is in scope. It builds the checked upstream libheif archive, refreshes the linker cache, verifies the pkg-config version, and requires HEIF support when building the libvips module.

## Status and risks

Local preparation complete. The amd64 rebuild with `--pull` succeeded as `devops-927-libheif:local`. `ldd` resolved `vips-heif.so` to the local libheif library, whose `heif_get_version()` returned `1.19.8`. `vips thumbnail` converted both upstream samples to 128×85 JPEGs, and an x265 HEIC encode/decode round trip produced a 32×24 JPEG. The AVIF sample emitted `heifload: ignoring nclx profile`, and x265 emitted container NUMA policy warnings. Neither affected the tested output dimensions. AOM AV1 decoding is available, while the Focal AOM package did not provide AV1 encoding in this build. The application and production input were outside the local smoke test. The remote tag and published image have not been updated.

## Merge request publication

The user requested an MR and approved the proposed commit, source push, and Ready MR with `Подтверждаю публикацию`. Original and final commit message: `build libheif 1.19.8 from source`. Original and final MR title: `DevOps-927 Build libheif 1.19.8 from source`. Source `DevOps-927-build-libheif-1-19-8`, target `master`. GitLab project defaults used: squash off, remove source branch after merge, assigned to the authenticated user. The approved body and the matching pre-stage snapshot are retained in `~/ai-data/gitlab-workflow/DevOps-927/base-images/` (16 KiB) for publication audit.

The unmodified CI include resolves to `gitlab-ci-templates` master `17d15809d9b109a1cf4e6726c3459a7be7938d79`. Its only job runs for tags, and that job pushes the built image. Publication checks passed: `git diff --check`, repeat runtime smoke tests, matching snapshot and staged Dockerfile diff (+18/-2), and inspection of the resulting commit. Pushed `298e97b4694161061a737d94db352f8ea69decf6` and created [MR !44](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/44). Independent API verification matched the approved body, title, branches and SHA. GitLab returned an empty pipeline list with verification available. MR publication completed; release-tag changes and registry publication were outside the approval.

## Published Content API image verification

The user requested tests of `msk3-nexus.youdo.corp/youdo/microservices/youdo.content/api:2.5.14`. Pulled `linux/amd64` from Nexus and pinned all tests to digest `sha256:53711714a59a4dec4e2e342a8ed24e4953bd72d1a2e853c934be445d7336a55f`. All tests used ephemeral local containers without network access.

The image entrypoint returned `200 Healthy` at `/hc`. The live API process mapped `/usr/lib/x86_64-linux-gnu/libvips.so.42.15.3` and `/usr/local/lib/libheif.so.1.19.8`. Runtime CLI verification reported libvips 8.13.3, confirmed the dynamic module linkage and libheif API version, produced 128×85 JPEGs from HEIC and AVIF, and encoded and decoded a generated HEIC.

Tested the packaged `YouDo.Content.Image.Vips.Processor` with the API's `.deps.json` and `.runtimeconfig.json`. Both array and stream overloads returned valid JPEGs at 1280×854 from HEIC and 800×533 from AVIF. `Size.Max128` produced 128×128 JPEGs for both inputs. The standalone harness's initial compile/runtime attempts had dependency context mismatches and were corrected by referencing the packaged logging assembly and using the API dependency manifests. The final harness confirmed the loaded libheif path. AVIF decoding still emitted `heifload: ignoring nclx profile`. No HTTP upload, database, or S3 integration was exercised.

## Production acceptance

On 2026-11-19 the user reported deploying the Content service to production and verified that photo upload works. This is the accepted production outcome for DevOps-927. The upload result is user-reported. Production image digest, the input format and individual storage operations were not independently checked in this turn.

The user then closed DevOps-927. YouTrack GET independently confirmed `State: Fixed` and a resolved status. No open DevOps-927 entry remained in the central backlog.

## YouTrack comment draft

Verified that DevOps-927 is the Content libheif task and had no comments. The user initially requested a draft. Original draft:

```markdown
В базовом образе `3.1-libvips` обновили `libheif` до `1.19.8`. Библиотека собирается из исходников и используется модулем HEIF в `libvips 8.13.3`. [MR !44](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/44)

На образе `youdo.content/api:2.5.14` проверили запуск API, конвертацию HEIC и AVIF в JPEG и генерацию миниатюр. Сервис развернули в production и проверили загрузку фото. Загрузка работает.
```

The user supplied shorter first-person wording for this issue and explicitly requested posting it. Posted comment `74-125679` with the MR reference linked and verified exact text by GET. The draft and receipt are retained under `~/ai-data/gitlab-workflow/DevOps-927/youtrack/`. Final comment:

```markdown
В базовом образе 3.1-libvips обновил libheif до 1.19.8. Библиотека собирается из исходников и используется модулем HEIF в libvips 8.13.3. [MR !44](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/44)
```

## Portable lesson

none

## Task metrics: DevOps-927

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-927",
  "created": "2026-11-19T16:48:56.292909+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "implementation",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Local amd64 image and HEIC/AVIF checks passed; approved MR !44 published and exact GitLab metadata verified.",
  "updated": "2026-11-19T17:00:14.689992+03:00"
}
```
