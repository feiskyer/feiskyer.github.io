---
title: "Kubernetes Ingress 可视化编辑器"
date: 2021-03-19
tags: [Kubernetes]
draft: false
---

[Ingress](https://kubernetes.io/zh/docs/concepts/services-networking/ingress/) 是 Kubernetes 集群中用于管理服务外部访问的 API 对象，典型的访问方式是 HTTP 和 HTTPS。Ingress 可以提供七层负载均衡、SSL 终结、基于名称的虚拟主机等。

通过 Ingress 访问服务的一个典型示例如下图所示：

![55DD2101-C159-4C16-9E3E-C918BB19F423](55DD2101-C159-4C16-9E3E-C918BB19F423.png)

为了配置这些 Ingress 策略，Kubernetes 集群中需要部署一个 Ingress 控制器，它监听 Ingress 和 Service 的变化情况，并根据规则配置负载均衡并提供访问入口。 Ingress Controller 在部署的时候通常会以 NodePort 或 LoadBalancer 的形式将入口地址公开到 Internet，以便集群外部访问。

典型的 Ingress Controller 以及支持的特性列表如下图所示（原始电子表格见[这里](https://docs.google.com/spreadsheets/d/191WWNpjJ2za6-nbG4ZoUMXMpUK8KlCIosvQB0f-oq3k/edit#gid=907731238)）：

![ingress-controller](ingress-controller.png)

这些 Ingress Controller 的选型可以参考上述特性对比，本文不作展开。

除了 Kubernetes Ingress API 对象定义的资源，很多 Ingress 控制器都基于 Kubernetes annotation 扩展了丰富的特性，并且不同控制器中这些特性的使用方法均不相同。因而，在需要切换不同 Ingress 控制器的场景中，想要正确配置这些特性就需要去查询多个项目的文档。

而 [Ingress Builder](https://ingressbuilder.jetstack.io/) 就提供了一个 Ingress API 资源的可视化编辑器。从编辑器的右侧选择控制器（如 nginx）和 Kubernetes 版本之后，在其下方就会显示该控制器支持的各种特性。下图就是一个编辑 nginx ingress 资源的示例：

![CB4B9C6B-A7C8-417F-8BB6-66703E26791E](CB4B9C6B-A7C8-417F-8BB6-66703E26791E.png)

在右侧选择不同的特性之后，在左侧的 Ingress 资源处就会自动添加对应的 annotation，使用起来非常方便。

Ingress Builder 的访问网址为 <https://ingressbuilder.jetstack.io>，祝你玩的开心。


---

欢迎长按下面的二维码关注**漫谈云原生**公众号，输入**任意关键字**查询更多云原生知识库。

![](https://feisky.xyz/assets/mp.png)
