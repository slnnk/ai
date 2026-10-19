---
system: jenkins
status: verified
checked: 2026-10-16
tags: [jenkins, selenium, kubernetes, dns]
---

# Jenkins Selenium Grid session startup EOF

## Summary

Jenkins AutoTest can reach a Selenium Grid endpoint at selenium.dev.youdo.corp. Build 3362 and VK Kubernetes logs correlate the EOF with scale-from-zero: KEDA/HPA expanded Chrome pods, but image pull DNS timed out and additional pods could not schedule on two workers for CPU/memory. Hub had no free slots during the failure and registered nodes at the same second. The VK node group is configured auto_scale min1/max10, but no worker was added during the burst.

## Context and actions

User supplied Selenium 3.141.59 RemoteWebDriver failure at 2026-10-16 13:06:23 (log timezone unspecified): `unexpected end of stream` connecting to `selenium.dev.youdo.corp:80`, resolved address10.18.26.60. User clarified Selenium is expected in VK Cloud Kubernetes, deployed from infra-tf/dev. Read-only checks ran from AutoTest10.18.26.26 and local repo contexts. No infrastructure, repository or Jenkins changes made.

## Findings

- From AutoTest, DNS resolves selenium.dev.youdo.corp to10.18.26.60. HTTP `/status` returns Selenium Grid4.48; `/readyz` returns `Router is true`; `/wd/hub/status` returned200. This confirms the hostname reaches a Grid service, not that the underlying cluster matches the intended VK target.
- At 2026-10-16 13:09 UTC (16:09 MSK), Grid `/status` reported ready=false and `Selenium Grid not ready`; two Chrome nodes were UP with one slot each and both sessions occupied. `/se/grid/newsessionqueue/queue` later returned an empty queue, and a subsequent `/wd/hub/status` reported `Selenium Grid ready.` This is consistent with transient capacity or scale-up timing but does not prove the state at13:06 caused the EOF.
- `infra-tf/dev/selenium.tf` declares namespace `selenium` and Helm release `selenium`; values configure hostname `selenium.dev.youdo.corp` and Selenium4.48. The BuildAPI operational kubeconfig already on disk at `/home/slnnk/ai-data/buildapi-vk/kubeconfig-ci.yaml` is mode0600, context `default/vk-ms1-k8s-test`; it was read-back matched to GitLab project77 file variable `KUBECONFIG_DEV`, scope `kube-test`. It authenticates with the local exec plugin `/home/slnnk/ai-data/buildapi-vk/bin/client-keystone-auth`; add that directory to PATH when invoking kubectl. It successfully queried the VK cluster. The ordinary `~/.kube/config` current context is unrelated Yandex `kube-test`; the available `admin@mks-infra` context is Selectel. The existing dirty `infra-tf/dev/main.tf` backend path change to `terraform/yandex-dev-k8s-a` was preserved.

## Next evidence needed

The remaining task is to determine why the configured VK worker auto_scale group did not add workers for pending Chrome pods and why worker DNS to registry.youdo.sg timed out. A controlled new-session probe would change remote state by creating a browser session and was not run.


## Build 3362 correlation and autoscaling

Read-only Jenkins artifact analysis: `youdo_web_testing_one/3362` started 2026-10-16 16:04 MSK and failed after10.4min; 43 test artifacts, 38 with a session start, median47.1s, p90 87.8s, max248.3s. The job log failure timestamp13:06:23 is UTC (16:06:23 MSK), matching VK cluster logs.

- KEDA activated `selenium-node-chrome` from0 at13:05:30Z; HPA increased it to2 at13:05:33Z. Pods were scheduled on the existing two workers.
- At13:05:40Z the registry image pull failed because DNS lookup `registry.youdo.sg` via10.18.20.3 timed out. Retry succeeded at13:06:19Z; Chrome node containers started at13:06:19-20Z and Hub registered nodes at13:06:22.133Z and13:06:23.314Z.
- During13:06:20-29Z Hub received12 Chrome session requests;10 initially had no free slot; two sessions were created as nodes registered. The error at13:06:23.026Z landed between the two node registrations.
- More Chrome pods failed scheduling with `0/2 nodes are available: Insufficient memory` and `Insufficient cpu`. No worker node was added during the burst; the same two workers remained. VK Terraform project625 master config (`test-k8s/k8s-cluster.tf`) sets node group `scale_type=auto_scale`, min1, max10. Workload KEDA/HPA autoscaling did react; managed worker autoscaling did not provide capacity in time. The exact control-plane reason for no worker increase remains unknown.
- Current Selenium config scale-to-zero (`minReplicaCount:0`) makes a burst pay image pull/cold-start delay. Registry DNS timeout and worker capacity both contributed. No config changes or new browser sessions were made.

## Follow-up: autoscaler and DNS event detail

On 2026-10-16, read-only live checks confirmed the cluster autoscaler did react to unschedulable Chrome pods: group size was requested from2 to3 at13:06:00Z, then3 to4 at13:06:18Z (maximum10). No new worker registered; at13:21:32Z the cluster emitted `ScaleUpTimedOut` after15m10s. Current status configmap shows `autoscalerStatus: Running`, group target2, two Ready nodes, min1/max10, and no unregistered nodes. This distinguishes a scale-up request from successful capacity provisioning; Kubernetes-side evidence does not identify why VK Cloud failed to register the requested nodes. No autoscaler pod is exposed in `kube-system`, so provider node-group activity/events are needed for the lower-level cause.

The Selenium image pull on worker10.18.26.62 failed at13:05:40Z because the host resolver10.18.20.3 timed out resolving `registry.youdo.sg`; retry pulls succeeded by13:06:19Z (worker0) and13:06:15Z (worker1). A read-only `getent` from the existing Selenium Hub pod resolves `registry.youdo.sg` to138.16.203.174, so pod-network DNS was working at check time. This supports a transient worker-host resolver path issue, but does not verify the host resolver's current live behavior.

## Retry monitoring: build 3363

User-triggered `youdo_web_testing_one/3363` was monitored read-only together with VK Kubernetes. Build3363 ran `[Smokus]`, test5, and failed:42 tests,22 failures; its post-build publisher successfully created build3364 with `[Упавшие тесты]`, `PREVIOUS_BUILD_ID=3363`, `FailedTestSuite_0003363.xml`. Build3364 ran22 tests,19 failed and launched3365 using `FailedTestSuite_0003364.xml`; build3365 ran19 tests and all19 failed. Since the failure count matched3364, no3366 was queued, consistent with the publisher's stop condition. The logs contain repeated `UnreachableBrowserException`; no registry DNS errors occurred during this retry chain.

At peak the Chrome deployment requested12 pods, but only2 ran on the two existing workers and10 remained Pending for insufficient CPU/memory. VK Cluster Autoscaler requested node-group size2->3->4 at13:45Z, then emitted `ScaleUpTimedOut` at14:00:42Z because nodes did not register within15m. It requested4 again at14:02:49Z. At14:05Z the cloud-provider target was4 while Kubernetes still had2 Ready nodes and Selenium had2 Running Chrome pods/10 Pending. The user portal also showed the group configured for4, but this was not evidence of four Kubernetes-registered nodes. Provider-side node creation/registration remains the blocker; the image-pull DNS timeout did not recur during these builds.

## Why failed tests were not rerun

Jenkins job configuration and build 3362 console were checked read-only. The post-build publisher is configured to execute on FAILURE. It did execute after Maven reported 42 tests with 22 failures, and its script attempted to enqueue a `[Упавшие тесты]` build because the original suite was `[Smokus]`. The enqueue failed before creating a build: the script's hard-coded `jenkins-test.ru-central1.internal` host could not resolve from the Jenkins agent while `python-jenkins` requested `/crumbIssuer/api/json` (`NameResolutionError`). The post-build step then marked the build as failed. This is separate from the Selenium per-test `Retry #1` entries in the log.

The configured publisher also embeds its Jenkins API credential directly in the script. Do not copy it into notes or logs; migrate it to Jenkins Credentials and rotate it as part of correcting the publisher. Recommended fix is to use the active Jenkins URL from its runtime environment (or another verified reachable canonical URL), store auth in Jenkins Credentials, then verify an authenticated GET/crumb and a controlled enqueue. No Jenkins change or retry build was made.

Read-only config comparison of the three WEB jobs shown in Jenkins (`youdo_web_testing_one`, `youdo_web_testing_two`, `youdo_web_testing_three`) confirmed each has the same post-build setup and hard-coded internal URL. Proposed URL-only change for all three is `url = os.environ['JENKINS_URL']`, using Jenkins' standard runtime variable (configured server address is `build.youdo.sg`). No job configuration was changed pending the required approval for remote Jenkins state changes.

After the user authorized URL-only changes, Jenkins `config.xml` POST was attempted with a valid crumb. It returned HTTP500 with the Jenkins generic “Oops!” page (logging ID `bddce77c-8de3-459f-975b-8a61fccf794b`). Read-only GET confirmed all three jobs still have the old URL; no partial change occurred. `/whoAmI` authenticated as `technical` and returned only `authenticated` authority, which may indicate missing configure permissions but does not establish the cause of the HTTP500. Needs Jenkins-side log review for the logging ID or a user with job configure permissions.


## VK Cloud quotas and latest autoscaler events (2026-10-16 14:32 UTC)

Read-only VK Cloud Quota Manager API reports managed-k8s limits of140 vCPU and350 GB RAM, with52 vCPU and200 GB RAM used:88 vCPU and150 GB RAM remain. Nova project quota separately reports330 cores/1,358,400 MB RAM with261 cores/927,744 MB used. The Cloud Containers quota therefore has substantial available capacity and could fit two additional STD3-8-32 workers (16 vCPU/64 GB) within the reported remaining quota. The portal screenshot taken earlier showed104 vCPU/214 GB free; current live API values have since decreased, but remain sufficient.

Latest cluster-autoscaler-status shows Running, scale-up NoActivity, cloud-provider target2, two Ready/registered nodes, group min1/max10. Kubernetes events contain two ScaleUpTimedOut warnings (nodes failed to register within ~15 minutes) and scale-up requests to sizes3 and4 (max: 10). Filtering the available event stream for quota exceeded|max size reached returned no matches. No Cluster Autoscaler pod exists in kube-system, so its raw process logs are not exposed through this cluster; provider-side VM/node-group activity and managed-service logs are still required to establish why the requested nodes did not register. This evidence does not indicate quota exhaustion or the configured max-size boundary as the cause.
