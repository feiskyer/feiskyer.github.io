---
title: Troubleshooting Kubernetes
date: 2018-01-27 20:11:07
layout: "post"
---

This part introduces how to troubleshoot various problems on Kubernetes, includes

- [Troubleshooting Cluster](cluster.html)
- [Troubleshooting Pod](pod.html)
- [Troubleshooting Storage](pv.html)
- [Troubleshooting Network](network.html)
- [Troubleshooting Windows Containers](windows.html)
- [Troubleshooting Cloud Provider](cloud.html)

Remember `kubectl` is always the most important tool when starting to troubleshoot any problems.

### Listing Nodes

```sh
kubectl get nodes
kubectl describe node <node-name>
```

#### Listing Pods

```sh
kubectl get pods -o wide
kubectl -n kube-system get pods -o wide
```

#### Looking at Pod events

```sh
kubectl describe pod <pod-name>
```

#### Looking at kube-apiserver logs

```sh
PODNAME=$(kubectl -n kube-system get pod -l component=kube-apiserver -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME --tail 100
```

#### Looking at kube-controller-manager logs

```sh
PODNAME=$(kubectl -n kube-system get pod -l component=kube-controller-manager -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME --tail 100
```

#### Looking at kube-scheduler logs

```sh
PODNAME=$(kubectl -n kube-system get pod -l component=kube-scheduler -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME --tail 100
```

#### Looking at kube-dns logs

```sh
PODNAME=$(kubectl -n kube-system get pod -l k8s-app=kube-dns -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME -c kubedns
```

#### Looking at kubelet logs

SSH to the Node and then run

```sh
journalctl -l -u kubelet
```

#### Looking at  kube-proxy logs

Kube-proxy is usually run as DaemonSet

```sh
$ kubectl -n kube-system get pod -l component=kube-proxy
NAME               READY     STATUS    RESTARTS   AGE
kube-proxy-42zpn   1/1       Running   0          1d
kube-proxy-7gd4p   1/1       Running   0          3d
kube-proxy-87dbs   1/1       Running   0          4d
$ kubectl -n kube-system logs kube-proxy-42zpn
```