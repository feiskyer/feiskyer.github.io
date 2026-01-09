layout: post
title: Kubernetes HA
date: 2017-03-15 18:12:47
tags: [kubernetes]

---

Kubernetes 从 1.5 开始，通过`kops`或者`kube-up.sh`部署的集群会自动部署一个高可用的系统，包括

- etcd 集群模式
- apiserver 负载均衡
- controller manager、scheduler 和 cluster autoscaler 自动选主（有且仅有一个运行实例）

## etcd 集群

从`https://discovery.etcd.io/new?size=3`获取 token 后，把<https://kubernetes.io/docs/admin/high-availability/etcd.yaml>放到每台机器的`/etc/kubernetes/manifests/etcd.yaml`，并替换掉`${DISCOVERY_TOKEN}`, `${NODE_NAME}`和`${NODE_IP}`，既可以由 kubelet 来启动一个 etcd 集群。

对于运行在 kubelet 外部的 etcd，可以参考[etcd clustering guide](https://github.com/coreos/etcd/blob/master/Documentation/op-guide/clustering.md)来手动配置集群模式。

## apiserver

把<https://kubernetes.io/docs/admin/high-availability/kube-apiserver.yaml>放到每台 Master 节点的`/etc/kubernetes/manifests/`，并把相关的配置放到`/srv/kubernetes/`，即可由 kubelet 自动创建并启动 apiserver:

- basic_auth.csv - basic auth user and password
- ca.crt - Certificate Authority cert
- known_tokens.csv - tokens that entities (e.g. the kubelet) can use to talk to the apiserver
- kubecfg.crt - Client certificate, public key
- kubecfg.key - Client certificate, private key
- server.cert - Server certificate, public key
- server.key - Server certificate, private key

apiserver 启动后，还需要为它们做负载均衡，可以使用云平台的弹性负载均衡服务或者使用 haproxy/lvs 等为 master 节点配置负载均衡。

## controller manager 和 scheduler

controller manager 和 scheduler 需要保证任何时刻都只有一个实例运行，需要一个选主的过程，所以在启动时要设置`--leader-elect=true`，比如

```
kube-scheduler --master=127.0.0.1:8080 --v=2 --leader-elect=true
kube-controller-manager --master=127.0.0.1:8080 --cluster-cidr=10.245.0.0/16 --allocate-node-cidrs=true --service-account-private-key-file=/srv/kubernetes/server.key --v=2 --leader-elect=true
```

把[kube-scheduler.yaml](https://kubernetes.io/docs/admin/high-availability/kube-scheduler.yaml)和[kube-controller-manager.yaml](https://kubernetes.io/docs/admin/high-availability/kube-controller-manager.yaml)(非 GCE 平台需要适当修改) 放到每台 master 节点的`/etc/kubernetes/manifests/`即可。

## 数据持久化

除了上面提到的这些配置，持久化存储也是高可用 Kubernetes 集群所必须的。

- 对于公有云上部署的集群，可以考虑使用云平台提供的持久化存储，比如 aws ebs 或者 gce persistent disk
- 对于物理机部署的集群，可以考虑使用 iSCSI、NFS、Gluster 或者 Ceph 等网络存储，也可以使用 RAID

## 参考文档

- https://kubernetes.io/docs/admin/high-availability/
- http://kubecloud.io/setup-ha-k8s-kops/
- https://github.com/coreos/etcd/blob/master/Documentation/op-guide/clustering.md
