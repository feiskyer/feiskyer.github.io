# Kubernetes核心概念

## Pod

![pod](media/pod.png)

Pod是一组紧密关联的容器集合，它们共享Volume和network namespace，是Kubernetes调度的基本单位。Pod的设计理念是支持多个容器在一个Pod中共享网络和文件系统，可以通过进程间通信和文件共享这种简单高效的方式组合完成服务。

## Node

![node](media/node.png)

Node是Pod真正运行的主机，可以物理机，也可以是虚拟机。为了管理Pod，每个Node节点上至少要运行container runtime（比如docker或者rkt）、`kubelet`和`kube-proxy`服务。

## Service

![](media/14731220608865.png)

Service是应用服务的抽象，通过labels为应用提供负载均衡和服务发现。Service对外暴露一个统一的访问接口，外部服务不需要了解后端容器的运行。


