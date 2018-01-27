---
title: Troubleshooting Kubernetes Pod
date: 2018-01-27 20:11:07
layout: "post"
---

This chapter is about pods troubleshooting, which are applications deployed into Kubernetes.

### Get pod status

The first step is getting pod's current state

```sh
kubectl describe pod <pod-name>
```

If the pod state is not Running, then check the following guides.

### Pod stuck in Pending

Pending state indicates the Pod has been scheduled yet. By running

```sh
kubectl describe pod <pod-name>
```

Check events and they will show you why the pod is not scheduled. Generally this is because there are insufficient resources of one type or another that prevent scheduling. Possible reasons include:

* Cluster doesn't have enough resources, e.g. CPU, memory or GPU. You need to adjust pod's resource request or add new nodes to cluster
* Pod is using hostPort, but the port is already been taken by other services. Try using a Service if you're in such scenario

### Pod stuck in Waiting or ContainerCreating

In such case, Pod has been scheduled to a worker node, but it can't run on that machine. Again, get information from `kubectl describe pod <pod-name>` and check what's wrong. Reasons include:

* Failed to pull image, e.g.
  * image name is wrong
  * registry is not accessible
  * image hasn't been pushed to registry
  * docker secret is wrong or not configured for secret image
  * timeout because of big size (adjusting kubelet  `--image-pull-progress-deadline` and `--runtime-request-timeout` could help for this case)
* Network setup error for pod's sandbox, e.g.
  * can't setup network for pod's netns because of CNI configure error
  * can't allocate IP address because exhausted podCIDR
* Failed to start container, e.g.
  * cmd or args configure error
  * image itself contains wrong binary

### Pod stuck in BackOff

In such case, Pod has been started and then exited abnormally. Take a look at the container logs:

```sh
kubectl logs <pod-name>
```

If your container has previously crashed, you can access the previous container’s crash log with:

```sh
kubectl logs --previous <pod-name>
```

From container logs, we may find the reason of crashing, e.g.

* Container process exited
* Health check failed

Alternately, you can run commands inside that container with `exec`:

```sh
kubectl exec cassandra -- cat /var/log/cassandra/system.log
```

If none of these approaches work, SSH to Pod's host and check kubelet or docker's logs. The host running the Pod could be found by running:

```sh
kubectl get pod <pod-name> -o wide
```

### Pod is stuck in Error

In such case, Pod has been scheduled but failed to start. Again, get information from `kubectl describe pod <pod-name>` and check what's wrong. Reasons include:

* referring non-exist ConfigMap, Secret or PV
* exceeding resource limits (e.g. LimitRange)
* violating PodSecurityPolicy
* not authorized to cluster resources (e.g. with RBAC enabled, rolebinding should be created for service account)

### Pod is running but not doing what it should do

If the pod has been running but not behaving as you expected, there may be errors in your pod description. Often a section of the pod description is nested incorrectly, or a key name is typed incorrectly, and so the key is ignored.

Try to recreate the pod with `--validate` option:

```sh
kubectl delete pod mypod
kubectl create --validate -f mypod.yaml
```

or check whether created pod is expected by getting its description back:

```sh
kubectl get pod mypod -o yaml
```

### Static Pod not recreated after manifest changed

Kubelet monitors changes under `/etc/kubernetes/manifests`  (configured by kubelet's `--pod-manifest-path` option) directory by inotify. There is possible kubelet missed some events, which results in static Pod not recreated automatically. Restart kubelet should solve the problem.

### References

- [Troubleshoot Applications](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/)
