---
layout: post
title: Docker CE/EE 原生支持Kubernetes
date: 2017-10-17 17:18:31
tags: [docker, liveblog]
---

在今年的 DockerCon EU (2017) 上，Solomon、Brendan、Hockin等联合[宣布](https://blog.docker.com/2017/10/kubernetes-docker-platform-and-moby-project/)Docker将原生支持Kubernetes，也就是说Kubernetes将和Swarm一样作为Docker平台的编排管理系统。这[包括Docker EE、Docker CE以及Docker for Mac/Windows等全平台](https://www.docker.com/kubernetes)的支持。

![](/images/15082343121829.png)


## Docker for Mac/Windows

Docker for Mac/Windows将原生支持把基于docker-compose/swarm的应用部署到本地的Kubernetes集群中，docker swarm和Kubernetes共享相同的镜像、存储卷以及容器（也就是两种调度系统同时管理同一套容器）。这有助于简化容器应用的开发、构建、运行以及测试。

为了实现这个目标，Docker基于Kubernetes Custom Resources和API server aggregation将Docker Compose apps 部署为原生的Kubernetes Pods/Services。

[这里](https://www.youtube.com/watch?time_continue=262&v=jWupQjdjLN0)是一个Docker for Mac的示例视频，非常有趣。

## Docker EE

![](/images/15082337741260.jpg)

在创建Stack的时候可以选择Swarm或者Kubernetes：

![](/images/15082337923290.jpg)

并且还可以在Shared Resources除查看共享的资源：

![](/images/15082338098210.jpg)

当然，部署也很简单，内置在Docker EE中，swarm和Kubernetes共享相同的Node：

![](/images/15082339050370.jpg)

[这里](https://www.youtube.com/watch?v=h2B6mhDCw2o)这里也有一个Docker EE + Kubernetes的示例视频。

## Docker CE/Moby

[Moby与Kubernetes的集成通过一系列的开源项目](http://mobyproject.org/kubernetes/)来实现：

- [containerd](https://github.com/containerd/containerd) 和 [cri-containerd](https://github.com/kubernetes-incubator/cri-containerd)，可以参考[Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)查看使用方法
- LinuxKit：支持[构建Kubernetes镜像](https://github.com/linuxkit/linuxkit/tree/master/projects/kubernetes)
- InfraKit：支持[Kubernetes Flavor](https://github.com/docker/infrakit/tree/master/pkg/plugin/flavor/kubernetes)
- libnetwork：增加CNI的支持 <https://github.com/docker/libnetwork/pull/1978>
- [Notary](https://github.com/docker/notary)将会贡献给CNCF
- [libentitlement](https://github.com/docker/libentitlement)将提供高级安全接口


不过遗憾的是，Kubernetes的支持需要等到下个release。想要提前预览的同学可以点击<https://beta.docker.com/>注册预览版。

注：本文同步发布到知乎专栏[《Kubernetes指南》](https://zhuanlan.zhihu.com/kubernetes)。

