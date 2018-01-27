---
title: Troubleshooting Kubernetes Network
date: 2018-01-27 20:11:07
layout: "post"
---

Network issues comes up frequently for new installations of Kubernetes or increasing Kubernetes load. This chapter introduces various network problems and troubleshooting method when using kubernetes.

Kubernetes "IP-per-pod" model solves 4 distinct networking problems:

* Highly-coupled container-to-container communications: this is solved by pods and localhost communications.
* Pod-to-Pod communications: this is solved by CNI network plugin
* Pod-to-Service communications: this is solved by services
* External-to-Service communications: this is solved by services

And these are exactly the direction of what we should do when encountering network issues. Reasons include:

* CNI network plugin configure error
  * CIDR conflicts with existing ones
  * using protocols not supported by underlying network (e.g. multicast may be disabled for clusters on public cloud)
  * IP forward is not enabled
    * `sysctl net.ipv4.ip_forward`
    * `sysctl net.bridge.bridge-nf-call-iptables`
* Missing route tables
  * default kubenet plugin requires a network route for each podCIDR to node IP
  * kube-controller-manager should configure the route table for all nodes, but if something is wrong (e.g. not authorized, exceed quota, etc), route may be missing
* Forbidden by security groups or firewall rules
  * iptables not managed by kubernetes may forbid kubernetes network connections
  * security groups on public cloud may forbid kubernetes network connections
  * ACL on switches or routers may also forbid kubernetes network connections

### DNS not work

If your docker version is above 1.13+, then docker would change default iptables FORWARD policy to DROP (at each restart). This change may cause kube-dns not reaching upstream DNS servers. A solution is run `iptables -P FORWARD ACCEPT` on each nodes, e.g.

```sh
echo "ExecStartPost=/sbin/iptables -P FORWARD ACCEPT" >> /etc/systemd/system/docker.service.d/exec_start.conf
systemctl daemon-reload
systemctl restart docker
```

Or if you are using flannel or weave network plugin, upgrades to latest version could also solve the problem.

There is also possible that kube-dns is not running normally.

```sh
kubectl -n kube-system get pod -l k8s-app=kube-dns
```

If you are in such case, refer to [Troubleshooting kube-dns/dashboard CrashLoopBackOff](cluster.html#kube-dnsdashboard-crashloopbackoff) for troubleshooting kube-dns problem.

### Service clusterIP is not accessible

The first step is checking whether endpoints have been created automatically for the service

```sh
kubectl get endpoints <service-name>
```

If you got an empty result, there is possible your service's label selector is wrong. Confirm it as follows:

```sh
# Query Service LabelSelector
kubectl get svc <service-name> -o jsonpath='{.spec.selector}'
# Get Pods matching the LabelSelector and check whether they are running
kubectl get pods -l key1=value1,key2=value2
```

If all of above steps are still ok, confirm further by

* checking whether Pod containerPort is same with Service containerPort
* checking whether `podIP:containerPort` is working

Further, there are also other reasons could also cause service problems. Reasons include:

* container is not listening to specified containerPort (check pod description again)
* CNI plugin error or network route error
* kube-proxy is not running or iptables rules are not configured correctly

Normally, following iptables should be created for a service named `hostnames`:

```sh
$ iptables-save | grep hostnames
-A KUBE-SEP-57KPRZ3JQVENLNBR -s 10.244.3.6/32 -m comment --comment "default/hostnames:" -j MARK --set-xmark 0x00004000/0x00004000
-A KUBE-SEP-57KPRZ3JQVENLNBR -p tcp -m comment --comment "default/hostnames:" -m tcp -j DNAT --to-destination 10.244.3.6:9376
-A KUBE-SEP-WNBA2IHDGP2BOBGZ -s 10.244.1.7/32 -m comment --comment "default/hostnames:" -j MARK --set-xmark 0x00004000/0x00004000
-A KUBE-SEP-WNBA2IHDGP2BOBGZ -p tcp -m comment --comment "default/hostnames:" -m tcp -j DNAT --to-destination 10.244.1.7:9376
-A KUBE-SEP-X3P2623AGDH6CDF3 -s 10.244.2.3/32 -m comment --comment "default/hostnames:" -j MARK --set-xmark 0x00004000/0x00004000
-A KUBE-SEP-X3P2623AGDH6CDF3 -p tcp -m comment --comment "default/hostnames:" -m tcp -j DNAT --to-destination 10.244.2.3:9376
-A KUBE-SERVICES -d 10.0.1.175/32 -p tcp -m comment --comment "default/hostnames: cluster IP" -m tcp --dport 80 -j KUBE-SVC-NWV5X2332I4OT4T3
-A KUBE-SVC-NWV5X2332I4OT4T3 -m comment --comment "default/hostnames:" -m statistic --mode random --probability 0.33332999982 -j KUBE-SEP-WNBA2IHDGP2BOBGZ
-A KUBE-SVC-NWV5X2332I4OT4T3 -m comment --comment "default/hostnames:" -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-X3P2623AGDH6CDF3
-A KUBE-SVC-NWV5X2332I4OT4T3 -m comment --comment "default/hostnames:" -j KUBE-SEP-57KPRZ3JQVENLNBR
```

There should be 1 rule in KUBE-SERVICES, 1 or 2 rules per endpoint in KUBE-SVC-(hash) (depending on SessionAffinity), one KUBE-SEP-(hash) chain per endpoint, and a few rules in each KUBE-SEP-(hash) chain. The exact rules will vary based on your exact config (including node-ports and load-balancers).

### Pod cannot reach itself via Service IP

This can happen when the network is not properly configured for “hairpin” traffic, usually when kube-proxy is running in iptables mode and Pods are connected with bridge network.

Kubelet exposes a `--hairpin-mode` option, which should be configured as `promiscuous-bridge` or `hairpin-veth` instead of `none` (default is `promiscuous-bridge`).

Confirm `hairpin-veth` is working by:

```sh
$ for intf in /sys/devices/virtual/net/cbr0/brif/*; do cat $intf/hairpin_mode; done
1
1
1
1
```

Confirm `promiscuous-bridge` is working by:

```sh
$ ifconfig cbr0 |grep PROMISC
UP BROADCAST RUNNING PROMISC MULTICAST  MTU:1460  Metric:1
```

### References

* [Troubleshoot Applications](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/)
* [Debug Services](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-service/)
* [Kubernetes Cluster Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
