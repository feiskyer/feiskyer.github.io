---
title: "如何快速掌握 Kubernetes 网络"
date: 2021-03-12
tags: [Kubernetes]
draft: false
---

经常听到周边的人谈到 Kubernetes 网络很难掌握，今天来谈谈如何快速学习和掌握 Kubernetes 网络。

## Kubernetes 网络模型

要掌握 Kubernetes 网络，最首要的就是要熟悉其基本网络模型。实际上，Kubernetes 网络模型非常简单，只要掌握以下三点即可：

* IP-per-Pod，每个 Pod 都拥有一个独立 IP 地址，Pod 内所有容器共享一个网络命名空间。
* 集群内所有 Pod 都在一个直接连通的扁平网络中，可通过 IP 直接访问。
* Service cluster IP 仅可在集群内部访问，外部请求需要通过 NodePort、LoadBalance 或者 Ingress 来访问。

这三点基本网络模型同时也意味着：

* 所有容器之间无需 NAT 就可以直接互相访问。
* 所有 Node 和所有容器之间无需 NAT 就可以直接互相访问。
* 容器自己看到的 IP 跟其他容器看到的一样。

所以，你看 Kubernetes 网络模型非常简单。通常，我们觉得网络复杂是因为使用了自定义的网络插件，比如 Calico、Cilium 等。这些网络插件在满足 Kubernetes 网络模型的基础之上，又提供了很丰富的附加功能。这些附加功能跟 Kubernetes 原有的网络功能综合在一起，就显得很复杂了。

## 如何掌握 Kubernetes 网络

了解了 Kubernetes 网络模型之后，其实也很容易想到掌握它需要的知识点，这包括：

* Kubernetes 网络模型中提到了很多网络术语，比如网络命名空间、IP、路由、NAT、LoadBalance 等，这些网络基础知识当然是必须要掌握的。
* Kubernetes 大多运行在 Linux 服务器上，所以 Linux 网络的基本原理是必要的基础。
* Kubernetes 中的 Service、Ingress、NetworkPolicy 等是直接控制网络功能的资源，它们的原理和使用方法也需要熟悉。
* 在实际使用中，通常需要通过 CNI 插件适配实际的网络环境，所以 CNI 插件的原理以及相应的 CNI 插件也是需要掌握的内容。

在学习 CNI 网络插件的时候，可以从最基本的 bridge 插件开始，从 Pod 创建并获取 IP、同节点 Pod 间通信再到跨节点 Pod 通信等逐步深入。

![](cni-bridge.png)

关于常见网络插件的原理可以参考开源电子书《Kubernetes指南》的[网络插件模块](https://kubernetes.feisky.xyz/extension/network)。

## 如何进阶

掌握了上述网络知识之后，就足以应对常见 Kubernetes 集群中网络相关的问题了。但在复杂的场景中，可能还需要进一步的深入进阶，才可以说是完全掌控 Kubernetes 网络。

当然，具体进阶的方向根据实际需要也有不同的选择，比如

* 当需要深入排查网络相关的问题（如性能抖动、网络故障等），除了前述的 Linux 网络原理之外，你还需要深入到内核里面，去了解 Linux 内核网络协议栈的实现机制。
* 当需要打通多个集群之间的网络联通时，除了单集群内部的网络原理之外，你还需要了解多集群网络互联互通的方法，如专线联通、网关、隧道等等。
* 当需要对复杂微服务进行治理时，你想要实现诸如金丝雀部署、流量控制、网络观测、服务间请求加密等需求时，Service Mesh 是你的不二选择。
* 当网络的性能是你的瓶颈时，eBPF、DPDK、SR-IOV 等提供了绕过内核协议栈的方法以极致优化网络的性能。

![](image2_3.jpg)
(图片来自 redhat.com)

更多 Kubernetes 网络相关的细节和学习资料请参考《[Kubernetes 指南](https://kubernetes.feisky.xyz/)》。


---

欢迎长按下面的二维码关注**漫谈云原生**公众号，输入**任意关键字**查询更多云原生知识库。

![](https://feisky.xyz/assets/mp.png)
