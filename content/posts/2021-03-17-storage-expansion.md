---
title: "如何无宕机扩容 Kubernetes 存储"
date: 2021-03-17
tags: [Kubernetes]
draft: false
---

Kubernetes 从 1.11 开始支持 Persistent Volumes Claim（PVC）的动态扩容，诸如 AWS EBS、GlusterFS、rbd 等都可以修改 PVC 增大持久化存储的大小。但是，具体扩容时是否对应用有影响还要看具体的存储插件实现，有些存储插件的实现无需重启 Pod，而有些存储插件则需要把 PV 从 Node 上卸载之后才支持扩容。今天，我们就来看看各种不同的存储插件如何实现无宕机扩容。

### 网络文件系统

第一种存储插件是网络文件系统，如 GlusterFS、Azure File 等。这类存储插件在扩容时无需 Node 本地文件系统的扩展，因而只需要修改 PVC 的大小即可扩容。

![pvc-storageclass](pvc-storageclass.png)

## 块存储设备

第二种存储插件是块存储设备，比如 AWS EBS、Ceph RBD 等。由于文件系统的存在，块设备扩容之后，还需要对文件系统进行扩展。在 Kubernetes 早期版本，文件系统的扩展需要重启 Pod，并且需要 PVC 是以 ReadWrite 的方式挂载，这在实际应用中非常不方便。

从 Kubernetes 1.15 开始新增的 ExpandInUsePersistentVolumes 特性增加了在线修改 PVC 文件系统大小的功能，无需重启 Pod 就可以对正在挂载中的块设备进行扩容。所以，开启 ExpandInUsePersistentVolumes 特性之后，只需要修改 PVC 的大小即可扩容。

## 需卸载才可以扩容的块设备存储

最后一种是需要先从 Node 卸载才可以进行扩容的块设备存储，比如 Azure Disk 等。对这类存储，直接修改 PVC 的大小或者重启 Pod 都无法对 PVC 进行扩容。为了把块设备从 Node 卸载，Pod 需要先删除一段时间，等 PVC 完成扩容之后再创建回来。对这类存储能否实现无宕机扩容呢？

如果从单个 Pod 的角度看，删除 Pod 必然会产生宕机。但一般每个应用都会包含多个 Pod，其中某个 Pod 的删除并不会影响整个应用的可用性，故而可以从应用的角度实现无宕机扩容。

比如，对于常见的 StatefulSet 来说，一般运行 3 个副本，可以按照下面的步骤进行扩容：

1） 保存 StatefulSet 的配置留待后续重建使用 `kubectl get statefulset rabbitmq -o yaml > rabbitmq.yaml`。
2） 删除 StatefulSet 但保留所有的 Pod `kubectl delete statefulset rabbitmq --cascade=false`。
3） 删除第一个 Pod 并对其引用的 PVC 进行扩容：
```sh
kubectl delete pod rabbitmq-0
kubectl edit pvc pvc-rabbitmq-0 # 增大Capacity
```
4） 恢复 StatefulSet `kubectl apply -f rabbitmq.yaml`，这时刚才删除的 Pod 会重新创建回来。
5） 对剩余两个副本重复上述步骤，对其 PVC 进行扩容后再重建回来。

这样，虽然在扩容过程中总有一个 Pod 被删除了，但其余两个副本还是正常运行状态，整个应用还是可以正常运行的。

总之，要实现无宕机的存储扩容，可以从存储层和应用层分别考虑，存储层可以解决的问题就在存储层解决，存储层无法解决的问题可以在应用层绕开。


---

欢迎长按下面的二维码关注**漫谈云原生**公众号，输入**任意关键字**查询更多云原生知识库。

![](https://feisky.xyz/assets/mp.png)
