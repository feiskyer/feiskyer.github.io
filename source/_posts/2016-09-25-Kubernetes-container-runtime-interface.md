---
title: Kubernetes container runtime interface
date: 2016-09-25 06:59:31
tags: [kubernetes]
---

题记：最近一段时间在做Kubernetes容器引擎接口（Container Runtime Interface， CRI）的重构，并支持以插件的方式引入外部容器引擎。CRI还在紧张有序的开发中，预计在v1.5发布第一个alpha版。

## 什么是CRI

CRI是Kubelet（负责管理容器生命周期的服务）与容器引擎之间的接口。为了适应多种不同的容器引擎，Kubelet在加入rkt的时候就已经在docker API的基础上抽象了一个Runtime接口，只是由于一些特定的缺陷，在这个接口上不太容易引入其他新的容器引擎：

- Runtime接口的抽象度太高，导致一些原本该在Kubelet控制的逻辑被放到了Runtime实现里面。比如在当前的实现中，rkt和docker的`SyncPod`（负责Pod创建的接口）存在大量重复的逻辑，每次修改docker部分的时，都有可能需要同时修改rkt部分。这样，如果再加入新的容器引擎的话，同时修改多个Runtime部分的代码是没法维护的。
- Runtime接口是集成在Kubelet内部的，集成容器引擎相关的代码需要放到Kubernetes代码库里面，这同样带来了维护的问题：代码维护麻烦，任何一个容器引擎修改了代码都需要发布新的kubelet；集成测试麻烦，要为每个不同的容器引擎部署不同的集成测试环境。
- 没有提供容器创建的接口，无法直接在Kubelet里面做到对容器的精细控制。
- 耦合了镜像和容器管理，而它们的生命周期本来就是独立的。

既然Runtime接口有很多问题，并且有很多容器引擎想要集成到Kubernetes中，所以有必要重新定义CRI，并且提供一种插件机制，允许容器引擎以外部独立进程的方式接入。所以，Brendan Burns在[Hyper](http://hypercontainer.io)集成的时候就提供了一种以客户端/服务器方式接入外部容器引擎的思路。在大量的社区讨论后，Node team重新抽象了容器引擎接口（也就是CRI），并决定以gRPC的方式接入外部容器引擎。

## CRI是如何工作的

CRI比Runtime接口提供了更细粒度的抽象，解耦了镜像管理和容器管理，并为Pod和Container提供了独立的操作接口。CRI以gRPC的方式接入，Kubelet是gPRC API的客户端，而容器引擎则是gRPC API的服务端。gRPC已经自动实现了它们之间交互的细节，容器引擎只需要实现每个具体的API。

一个典型的启动Pod的流程为

![createpod](/images/createpod.png)

而停止Pod的流程为

![killpod](/images/killpod.png)


## CRI带了什么

CRI解决了上述提到的Runtime接口的问题，使得新的容器引擎可以更方便的集成到Kubernetes中来，这必将给Kubernetes社区带来新一轮的变革，并促进Kubernetes走入更多的应用场景中。比如，Redhat借助OCI容器引擎runc摆脱对docker依赖，Hyper以虚拟化的方式解决多租户场景下的容器隔离问题，甚至Mirantis直接用Kubernetes来管理原生的虚拟机。

CRI也在着力解决一些很有挑战的问题，比如

- 容器日志的管理，包括日志格式化规范、日志文件rotate、日志文件磁盘IO控制以及日志的统一收集处理等。
- 解除streaming API（exec、attach、logs等）对kubelet的网络压力。当前所有的streaming API都是从`apiserver->kubelet->runtime`，apiserver是无状态的，可以水平扩展，但kubelet和runtime则是每台机器只能有一个，streaming API有可能会给他们带来处理的瓶颈。所以在CRI中，将会考虑使用一个独立进程（需要对apiserver开放端口）来单独处理这些请求`apiserver->newStreamProcess`，释放kubelet来做更核心的事情。
- 更灵活的网络配置，将Pod网络的配置完全交给容器引擎，而Kubernetes只需要最终的网络状态。

## CRI的未来

虽然CRI还在持续开发中（目前还没有任何release），但已经有很多厂商已经开始了引入新容器引擎的进程：

- Frakti：为解决多租户场景下的容器隔离问题，Hyper以虚拟化的方式运行容器。关于frakti的更多细节见https://github.com/kubernetes/frakti。
- Ocid：为解耦对docker的依赖，Redhat提供对OCI容器引擎的支持（目前主要是runc）。关于ocid的更多细节见https://github.com/kubernetes-incubator/ocid。
- Rktlet：为了加速rkt容器引擎的开发维护，CoreOS提议将rkt集成独立出Kubelet，并重构rkt以适应CRI的变化。关于rktlet的更多细节见https://github.com/kubernetes-incubator/rktlet。
- Virtlet：为了支持原生的虚拟机管理，Mirantis提议直接用Kubernetes来管理原生的虚拟机（需要将docker镜像替换成qcow2镜像）。关于virtlet的更多细节见https://github.com/Mirantis/virtlet。
- 当然，docker相关的代码还会继续保留在kubelet内部，只不过要重构到CRI上面来。

CRI预计在Kubernetes v1.5发布第一个alpha版。届时，上面各个容器引擎的实现也将会发布第一个release。


