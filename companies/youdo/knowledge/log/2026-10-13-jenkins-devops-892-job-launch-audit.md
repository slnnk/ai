---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, recovery, gitlab, acceptance]
---
# DevOps-892: job launch and GitLab checkout acceptance audit

## Task

User clarified recovery acceptance: jobs must start and access GitLab; missing downstream infrastructure and resulting infrastructure failures are acceptable for this stage.

## Context

Controller10.18.26.8 remains quietingDown=true with empty queue; controller has10executors and AutoTest5online. User kept general quiet-mode release as a separate subsequent stage. No jobs were launched by this audit.

## Actions

Read-only DNS/HTTPS checks on both hosts resolve gitlab.youdo.sg to138.16.203.174 and return/users/sign_in HTTP200 with normal TLS validation. Read existing job config.xml through authenticated Jenkins GET using JENKINS_USER/JENKINS_TOKEN from current/.env; raw XML and credentials were not persisted. Created local read-only summary helper under ~/ai-data/jenkins-recovery/audit-job-configs.py.

## Findings

Existing test-git is a checkout-only Freestyle job: SCM https://gitlab.youdo.sg/sysadmins/automation-test-yandex.git, branch */master, stored credential reference present, no parameters/builders/publishers. canRoam=true and no assignedNode mean scheduling can select controller or AutoTest; builtOn must be checked, and a single build cannot establish checkout on both nodes.

Existing youdo_web_testing_one is assigned to AutoTest, SCM https://gitlab.youdo.sg/youdo/youdo.static.git, ref ${branch}, branch default origin/master. Parameters include stand, suite, failedSuite, PREVIOUS_BUILD_ID default0 and failedSuiteAuto. Suite default[first choice] is [Smokus]; stand choices include test/test1–17, prod, autotest01–03 and public-test. Builders warm stand URLs, choose suite configuration and run Maven clean/test/-U; publishers include artifacts/reports and a post-build script. Therefore it is not a checkout-only smoke job; production selection is outside this audit scope, and stopping after checkout has a race with subsequent effects. test ansible and dynamic deploy jobs execute infrastructure changes after checkout and are unsuitable for this limited check.

Host HTTPS200 proves connectivity but not Jenkins credentialed checkout. Proposed next concrete action is a controlled test-git build, recording checkout result and actual execution node. Any temporary cancellation/restoration of quiet mode requires separate explicit approval under the user external-mutation rule; permanent quiet-mode release remains separate.

## Changes

Updated Jenkins acceptance criterion in ~/ai/TODO.md, this log, index and sync-note. No job configuration, queue, quiet mode, credential or remote state was changed.

## Risks and limits

Legacy job builders contain inline curl -u credentials. Initial summary redaction failed to catch those lines and tool output exposed values; they are not repeated or stored here. Locations: Jenkins job test buildsinfo/config.xml and youdo_web_testing_one/config.xml builder shell commands; review/rotation is separate work in ~/ai/TODO.md. The local audit helper now omits curl credential lines and avoids raw pipeline XML. Web-test post-build script effects are not fully audited; do not infer that launching it is side-effect-free.

## Portable lesson

none
