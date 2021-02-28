---
title: "聊一聊 GKE Autopilot"
date: 2021-03-01
tags: [Kubernetes]
draft: false
---

Google Cloud 前两天推出了 GKE Autopilot，其官方博客 [Introducing GKE Autopilot: a revolution in managed Kubernetes](https://cloud.google.com/blog/products/containers-kubernetes/introducing-gke-autopilot) 称之为革命性的托管 Kubernetes 服务。但其“革命性”的亮点都有哪些呢？

## GKE Autopilot 亮点

推出 Autopilot 之后，GKE 支持两种操作模式，包括标准模式和 Autopilot 模式。这两者的主要区别在于 Autopilot 自动管理节点，而标准模式还需要用户去管理节点。

GKE Autopilot 模式图示如下：

![](2021-02-28-11-33-00.png)

GKE 标准模式图示如下：

![](2021-02-28-11-33-19.png)

Autopilot 会预先配置和管理整个集群的底层基础架构，包括

- 根据工作负载要求自动创建和扩展节点
- 省去节点管理的开销
- 按实际使用的资源付费，如 vCPU、内存和磁盘使用量等
- 内置 GKE 最佳实践，提高安全性
- 提高了工作负载可用性

## GKE Autopilot 限制

为了支持 Autopilot，并确保集群功能不受被用户操作破坏，Autopilot 也引入了很多限制，比如不支持 Google Group RBAC、Cloud Build、Cloud Run、Istio 等等。在具体的 Kubernetes 应用上，也引入了诸多的限制：

* 节点锁定，节点对应的虚拟机对用户隐藏，并禁止对节点的特权操作，比如不允许使用 HostPort、HostNetwork 等，也不允许 HostPath 存储卷的写操作；
* 不允许使用特权容器，容器内不允许 CAP_NET_RAW（ping会失败）。
* kube-system 命名空间锁定，mutating admission webhook 锁定，很多依赖于 Webhook 的容器无法正常部署。
* 为了确保根据资源请求进行自动扩展，所有容器强制增加资源请求配置。

GKE 集群创建后，可以在其详细信息页面看到其他禁止的特性：

![](2021-02-28-11-33-44.png)
![](2021-02-28-11-33-58.png)
![](2021-02-28-11-34-07.png)

更多的限制可以参考 [GKE Autopilot 文档](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)。

## 小结

从 GKE Autopilot 的特性上可以看出，Autopilot 在托管 Kubernetes 控制平面的基础上，把节点的管理也全部托管起来，实际上也就相当于是一个提供 Kubernetes API 的 PAAS 服务，或者也可以称之为 Serverless Kubernetes。

因为需要托管并锁定节点，为了避免用户操作引发的问题，GKE Autopilot 也引入了很多 Kubernetes API 上的限制，并舍弃了原本丰富的功能特性。对用户来说，很多已有的应用（比如 Helm Charts）可能都需要做一定的修改才可以在 GKE Autopilot 上面应用。

实际上，国内的几大公有云也早已推出了类似的服务，但在实现方式上也有一些不同。比如阿里云的 ASK 是基于 Virtual Node 实现的，相对于 GKE  Autopilot 来说有更多的限制（如不支持 Daemonset、大多数的 Volume 插件都不支持等）。

总之，同时托管节点和控制平面的好处是显而易见的，节省了用户的 SRE 和运维成本，但代价也是牺牲了灵活性。既然主流的公有云平台都提供了类似的服务，提供更多的 Kubernetes 原生功能特性以及提供更丰富的灵活性就会具有更大的竞争优势，未来我们应该会看到更多类似的演进。

---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](https://feisky.xyz/assets/mp.png)
