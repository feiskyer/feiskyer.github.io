---
layout: post
title: "Hypernetes wechat share"
description: ""
category: Kubernetes
tags: []
---

今天给大家介绍下最近在Hypernetes上做的工作。

Hypernetes是一个真正多租户的Kubernetes Distro。

Hypernetes在Kubernetes基础上增加了多租户认证授权、容器SDN网络、基于Hyper的容器执行引擎以及基于Cinder的持久化存储等。

基本上`Hypernetes = Bare-metal + Hyper + Kubernetes + Cinder(Ceph) + Neutron + Keystone`

在介绍Hypernetes细节之前先首先提一下相关背景，也就是Kubernetes的多租户支持情况。

群里之前已经很多人介绍过Kubernetes了，就不再重复介绍。

这儿主要说一下它在多租户方面的问题。

Kubernetes在多租户方面的支持还是比较少的，没有“租户”这一概念，也只有namespace提供了一个逻辑的资源池（可以给这个namespace设定一些资源的配额），并且它在认证授权、网络、Container Runtime等方面离真正的多租户还都比较远。

1. 认证方面，虽然支持client certificates，tokens，http basic auth等，但没有用户管理的功能。如果想要新建用户，需要手动修改配置文件并重启服务。最新版本增加了Keystone的认证，可以借助Keystone来管理用户。
    
2. 授权方面，目前只有AlwaysDeny ，AlwaysAllow以及ABAC模式。ABAC模式根据一个策略文件来配置不同用户的权限，比如限定用户只能访问特定的namespace等，但对于新创建的namespace等资源需要重复修改策略文件。

3. Kubernetes要求cluster内部所有的容器之间是全通的，而多租户情况下需要不同租户之前网络是隔离的。

4. Docker的安全性问题，跟虚拟化还是有不少距离。

正是由于上面这些原因，很多公司都在虚拟机里面来跑Kubernetes，比如Google Container Engine、OpenStack Magnum等。

在虚拟机内部跑容器虽然提升了安全性，但也引入了一些问题，比如容器的网络不能通过IaaS层来统一管理，容器无法直接使用IaaS层的持久化存储，无法集中调度所有容器的资源等。所以我们就做了Hypernetes.

先来看一下Hypernetes的架构图

<img width="660" alt="2015-11-10 9 23 14" src="https://cloud.githubusercontent.com/assets/676637/11051781/fac21258-878c-11e5-8545-a2b374ee5d70.png">

Hypernetes在Kubernetes基础上增加了一些组件

①增加了Tenant的概念，不同Tenant之间的网络和资源(ns, pod, svc, rc等)是隔离的。这些租户通过keystone管理，并提供认证和授权；
②通过Neutron给不同租户提供二层隔离的网络，并支持Neutron的各种插件（目前主要是ovs）；
③通过Hyper提供基于虚拟化的容器执行引擎，保证容器的隔离；
④还有通过Cinder给容器引入各种持久化存储（目前主要是ceph）

关于OpenStack的各个组件以及Hyper这儿就不再介绍了，群里很多大牛已经介绍过。

具体到Hypernetes内部，详细的架构是这样的

![](https://github.com/hyperhq/hypernetes/raw/master/architecture.png?raw=true)

为了支持多租户，Hypernetes基于Kubernetes增加了很多组件，这些组件都是以Plugin的形式提供的。

这样非常方便扩展，也很容易将Hypernetes与现有的IaaS在同一个基础架构上运行起来

比如，如果你不喜欢Neutron，可以把它替换成odl等。

Hypernetes是完全开源的，代码见https://github.com/hyperhq/hypernetes

当然，我们也会把Hypernetes做的工作contribute到Kubernetes社区，Brendan Burns大神表示很支持。

嗯，今天的分享就这么多。谢谢大家。

### QA

1. 请教一下，网络呢？kuber自带那套vip全没用？

    Kubernetes自带的功能我们都完整保留了：
    1⃣️ kube-proxy做的这部分功能，Hypernetes通过在每个Pod里面的Haproxy实现
    2⃣️service对外暴露的公网负载均衡，Hypernetes通过Neutron的Lbaas实现

2. Hyper是什么

    Hyper是一个基于Hypervisor的容器执行引擎。Hyper跟Docker相比，基于Hypervisor提供了更好的隔离性，同时还保持了Docker创建容器速度快、镜像管理方面等优点。官方网站为https://hyper.sh。
