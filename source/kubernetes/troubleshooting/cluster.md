---
title: Troubleshooting Kubernetes Cluster
date: 2018-01-27 20:11:07
layout: "post"
---

This chapter is about cluster troubleshooting, including kubernetes core components and addons. For network related issues, please refer to [troubleshooting network](network.html).

### Overview of failure modes

Starting from Node and addons status is what we usually do. After confirmed the ill-behavior component, then we could identify how to fix it. There are a lot of reasons which could result in cluster unhealthy,

- VM or physical machine shutdown
- Network partition within cluster, or between clusters
- Crashes in Kubernetes components
- Data loss or unavailability of persistent storage (e.g. GCE PD or AWS EBS volume)
- Operator error, e.g. misconfigured Kubernetes software or application software

Specifically,

- **kube-apiserver VM shutdown or kube-apiserver crashing** could result in
  - unable to stop, update, or start new pods, services, replication controller
  - existing pods and services should continue to work normally, unless they depend on the Kubernetes API
- **etcd cluster down or abnormal** could result in
  - kube-apiserver fails to come up
  - cluster changes to read only
  - kubelet couldn't update its status but will continue to run original Pods
- **kube-controller-manager/kube-scheduler VM shutdown or crash** could result in
  - Replication controller and other controller stops to work, and deployments/services won't work any more
  - Node controller stops to work and no new node could be registered in the cluster
  - Scheduler is down so that new pods couldn't be scheduled
  - This is why HA is important
- **kube-dns crash or not come up** could result in
  - in-cluster dns resolve failure
  - other components depending on dns (e.g. dashboard) would also fail
- **Individual node (VM or physical machine) shuts down** could result in
  - pods on that Node stop running
- **Network partition** could result in
  - partition A thinks the nodes in partition B are down; partition B thinks the apiserver is down. (Assuming the master VM ends up in partition A.)
  - pods not tolerating partition stop to work
- **Kubelet crash** could result in
  - crashing kubelet cannot start new pods on the node
  - kubelet might delete the pods or not
  - node marked unhealthy
  - replication controllers start new pods elsewhere
- **Cluster operator** error could result in
  - loss of pods, services, etc
  - lost of apiserver backing store
  - users unable to read API

### Mitigations

- Use IaaS provider’s automatic VM restarting feature for IaaS VMs
- Use IaaS providers reliable storage (e.g. GCE PD or AWS EBS volume) for VMs with apiserver+etcd
- Configure multiple nodes cluster for etcd and backup data periodically
- Configure high-availability for controller components, e.g.
  - load balancer on front of kube-apiserver
  - multiple replicas of kube-controller-manager, kube-scheduler and kube-dns
- Use replication controller and services in front of pods
- Multiple independent clusters and avoid making risky changes to all clusters at once

### Listing nodes

Normally, all nodes should be in Ready state

```sh
kubectl get nodes
kubectl describe node <node-name>
```

If some nodes are NotReady, `kubectl describe node <node-name>`  could get the node's events, which usually helps to identify the problem.

### Looking at logs

Usually, components of kubernetes are managed by systemd or kubelet itself (static pods).

- For static pods, please see next part of how to view their logs
- For systemd-managed components, SSH to the nodes and use journalctl to get logs, e.g.

```sh
journalctl -l -u kube-apiserver
journalctl -l -u kube-controller-manager
journalctl -l -u kube-scheduler
journalctl -l -u kubelet
journalctl -l -u kube-proxy
```

or view their log files

- /var/log/kube-apiserver.log
- /var/log/kube-scheduler.log
- /var/log/kube-controller-manager.log


- /var/log/kubelet.log
- /var/log/kube-proxy.log

#### Looking at kube-apiserver logs

Suppose kube-apiserver is running as static pods

```sh
PODNAME=$(kubectl -n kube-system get pod -l component=kube-apiserver -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME --tail 100
```

#### Looking at kube-controller-manager logs

Suppose kube-controller-manager is running as static pods

```sh
PODNAME=$(kubectl -n kube-system get pod -l component=kube-controller-manager -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME --tail 100
```

#### Looking at kube-scheduler logs

Suppose kube-scheduler is running as static pods

```sh
PODNAME=$(kubectl -n kube-system get pod -l component=kube-scheduler -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME --tail 100
```

#### Looking at kube-dns logs

Suppose kube-dns is running as deployment pods

```sh
PODNAME=$(kubectl -n kube-system get pod -l k8s-app=kube-dns -o jsonpath='{.items[0].metadata.name}')
kubectl -n kube-system logs $PODNAME -c kubedns
```

#### Looking at Kubelet logs

Kubelet couldn't be run as static pods, so it is usually managed by systemd

```sh
journalctl -l -u kubelet
```

#### Looking at kube-proxy logs

Suppose kube-proxy is running as daemonset pods

```sh
$ kubectl -n kube-system get pod -l component=kube-proxy
NAME               READY     STATUS    RESTARTS   AGE
kube-proxy-42zpn   1/1       Running   0          1d
kube-proxy-7gd4p   1/1       Running   0          3d
kube-proxy-87dbs   1/1       Running   0          4d
$ kubectl -n kube-system logs kube-proxy-42zpn
```

## Kube-dns/Dashboard CrashLoopBackOff

Because dashboard is depending on kube-dns (it needs to resolve `kubernetes.default`), its failure is usually caused by kube-dns.

Looking at kube-dns logs, if you find following errors

```sh
Waiting for services and endpoints to be initialized from apiserver...
skydns: failure to forward request "read udp 10.240.0.18:47848->168.63.129.16:53: i/o timeout"
Timeout waiting for initialization
```

Then it indicates kube-dns pod failed to forward dns request to upstream servers. The solution to this problem is

- Check docker version whether it's >= 1.13. If so, run `iptables -P FORWARD ACCEPT` on each node
- Wait a while, kube-dns should recover automatically. If not, check on node with
  - whether network configure is right
  - whether upstream dns servers is accessible
  - whether there are iptables or firewall disabled DNS

If kubernetes API access timeout is find instead of forward errors, e.g.

```sh
E0122 06:56:04.774977       1 reflector.go:199] k8s.io/dns/vendor/k8s.io/client-go/tools/cache/reflector.go:94: Failed to list *v1.Endpoints: Get https://10.0.0.1:443/api/v1/endpoints?resourceVersion=0: dial tcp 10.0.0.1:443: i/o timeout
I0122 06:56:04.775358       1 dns.go:174] Waiting for services and endpoints to be initialized from apiserver...
E0122 06:56:04.775574       1 reflector.go:199] k8s.io/dns/vendor/k8s.io/client-go/tools/cache/reflector.go:94: Failed to list *v1.Service: Get https://10.0.0.1:443/api/v1/services?resourceVersion=0: dial tcp 10.0.0.1:443: i/o timeout
I0122 06:56:05.275295       1 dns.go:174] Waiting for services and endpoints to be initialized from apiserver...
I0122 06:56:05.775182       1 dns.go:174] Waiting for services and endpoints to be initialized from apiserver...
I0122 06:56:06.275288       1 dns.go:174] Waiting for services and endpoints to be initialized from apiserver...
```

Then it indicates there are something wrong with Pod-Node and Node-Node networking. There are also a lot of possible reasons for this, please refer to [troubleshooting network](network.html).

## Kubelet: failed to initialize top level QOS containers

This error message is reported when restarting kubelet ([#43856](https://github.com/kubernetes/kubernetes/issues/43856)). The problem has been fixed in [#44940](https://github.com/kubernetes/kubernetes/pull/44940) (v1.7.0). For old clusters, please try

- add options `--exec-opt native.cgroupdriver=systemd` to docker.service
- reboot the node

## Kube-proxy: conntrack returned error: error looking for path of conntrack

This error message is usually happening when setup a new cluster. kube-proxy may not find the conntrack binary on the node:

```sh
kube-proxy[2241]: E0502 15:55:13.889842    2241 conntrack.go:42] conntrack returned error: error looking for path of conntrack: exec: "conntrack": executable file not found in $PATH
```

Install `conntrack-tools` and restart kube-proxy could fix the problem.

## References

- [Troubleshoot Clusters](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-cluster/)
