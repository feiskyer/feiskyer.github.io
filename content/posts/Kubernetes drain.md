layout: "post"
title: "Kubernetes drain"
date: "2016-02-17 18:57"
---

Kubernetes v1.2以前，如果想要对某个NODE（也就是Kubelet和Docker所在的机器）进行维护（比如升级Docker或者内核等）又不想影响运行中的Pod的话，需要手动做很多的步骤：

- 首先patch NODE，将其改为不可调度状态： `kubectl patch nodes $NODENAME -p '{"spec": {"unschedulable": true}}'`
- 然后逐一删掉该NODE上的Pod，由Replication Ctroller自动到其它NODE上创建新的Pod
- 维护结束后再重新patch NODE，将其改成正常状态

在即将发布的v1.2中，`kubectl`中增加了`drain`和`uncordon`命令，使得这个过程更为简单易用。

### kubectl drain

`kubectl drain`的功能是将NODE改为维护模式，使用方法为

```sh
kubectl drain NODE [Options]
```

其中，可选的Options为：

```
--force[=false]: Continue even if there are pods not managed by a ReplicationController, Job, or DaemonSet.
--grace-period=-1: Period of time in seconds given to each pod to terminate gracefully. If negative, the default value specified in the pod will be used.
```

注意：

- 它会删除该NODE上由ReplicationController, Job或者DaemonSet创建的Pod
- 不删除`mirror pods`（因为不可通过API删除`mirror pods`）
- 如果还有其它类型的Pod（比如不通过RC而直接通过kubectl create的Pod）并且没有`--force`选项，该命令会直接失败
- 如果命令中增加了`--force`选项，则会强制删除这些不是通过ReplicationController, Job或者DaemonSet创建的Pod

为什么这些不是通过ReplicationController, Job或者DaemonSet创建的Pod没有迁移到其它NODE上去呢？因为在Kubernetes中，一个Pod一旦创建好就与某个NODE绑定了，并且不会因为资源不足、NODE失效等再对其进行重新调度：

> Pods aren't intended to be treated as durable pets. They won't survive scheduling failures, node failures, or other evictions, such as due to lack of resources, or in the case of node maintenance.

所以，Kubernetes推荐通过Ctroller（ReplicationController, Job或者DaemonSet等）来管理Pod，而不是直接创建Pod。

### kubectl uncordon

`kubectl uncordon`的功能比较简单，就是将NODE重新改成可调度状态，使用方法为：

```sh
kubectl uncordon NODE
```
