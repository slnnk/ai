---
system: web-autotests
status: verified
checked: 2026-10-20
tags: [selenium, kubernetes, jenkins, autoscaling]
---
# Jenkins 2007 live autoscaler and Selenium status

## Task and context

Check current autoscaler and Selenium during https://build.youdo.sg/job/youdo_web_testing_two/2007/. Snapshot2026-10-20 14:16:49UTC (17:16:49Moscow). Cluster vk-ms1-k8s-test.

## Actions

Read Jenkins build metadata, Kubernetes nodes/pods/deployment/HPA/events and cluster-autoscaler-status, plus Selenium Grid status and session queue. Credentials remain in current/.env and the existing private kubeconfig. Generated evidence is under /home/slnnk/ai-data/jenkins-2007-autoscale/. No external changes.

## Findings

- Build2007 is running, started14:04:46.567UTC, AutoTest, test1, origin/master. Suite `[Упавшие тесты]` reruns failed tests from2006.
- Cluster autoscaler probe14:16:41UTC: Running/Healthy,4Ready workers, target4/min3/max10; scaleUp NoActivity, scaleDown NoCandidates, no unregistered workers.
- Chrome pod rcdtl could not schedule14:08:29UTC because of CPU/memory requests. It triggered workers3->4 at14:08:43. New workers-2 registered14:12:53; Kubernetes Ready condition transitioned14:12:54. Four Chrome containers on that worker started14:13:56–14:13:59. Scale-up to worker Ready took4m11s.
- Selenium Chrome deployment13desired/13Ready/13available, no terminating replicas. All13Chrome pods Running/Ready; hub and external scaler also Running/Ready. Current container restart counts are0 across this namespace.
- Grid ready=true,13registered browser nodes UP,13slots,3busy; queue length0. These HTTP and Kubernetes reads are adjacent snapshots, not a transaction.
- HPA current13/desired13, min1/max20, external metric valid, scaling active, no scaling limit. ScaleDownStabilized explains retaining recent higher recommendations while current session demand is lower. Last scale time14:13:15UTC.

## Changes

Added this log and a dated observation in the existing dev-deployment system map. No repository or infrastructure edits.

## Status and risks

Autoscaler and Selenium are healthy at the checked instant. Earlier scheduling pressure resolved after worker scale-up. Grid is shared; session counts do not establish exclusive attribution to build2007. No required follow-up or new backlog item; existing user-closed web-autotest entries remain closed.

## Portable lesson

none

## Follow-up: browser slot occupancy

At14:18:48UTC (17:18:48Moscow), three adjacent Grid reads showed8busy slots of13 and queue0. The earlier3busy observation was instantaneous demand, not a3session cap. Jenkins workspace file FailedTestSuite_0002006.xml specifies `parallel="methods" thread-count="12"`; the build command selects exactly that suite via `-DsuiteXmlFile=FailedTestSuite_0002006`. Build revision6a9ddd55ca09d88ff3b292d28a6defbf609e6bb0. Read-only local checkout inspection used /home/slnnk/git/youdo.static at d6a8ea3e437c522c78de75e3de000d4df00eb899 (different revision; actual run configuration confirmed through Jenkins workspace and command). Up to12test methods can run concurrently, but method concurrency does not establish simultaneous browser demand. Exact states of other test threads at the earlier3session instant were not collected; no specific wait or bottleneck is claimed. No required follow-up or external changes.
