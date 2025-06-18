---
title: "Kubernetes 容器运行时演进"
date: 2018-10-14T22:08:45+08:00
draft: false
---

>  注：本文是我在[中国云原生大会（CEUC 2018）](http://ceuc.k8smeetup.com/part) 上同名演讲的文字整理。 

Kubernetes 已经成为容器编排调度领域的事实标准，其优良的架构不仅保证了丰富的容器编排调度功能，同时也提供了各个层次的扩展接口以满足用户的定制化需求。其中，容器运行时作为 Kubernetes 管理和运行容器的关键组件，当然也提供了简便易用的扩展接口，也就是 CRI（Container Runtime Interface）。CRI 促进了容器运行时社区的繁荣，也为强隔离、多租户等复杂的场景带来更多的选择。

本文将介绍 Kubernetes 容器运行时的演进过程、如何借助繁荣的容器运行时社区满足各种复杂的多租户场景以及未来的发展展望。主要内容包括四个部分：

- 首先是简单介绍一下 Kubernetes 的架构，特别是 Kubelet 架构，依次确定容器运行时在 Kubernetes 整个架构中的位置和作用
- 然后介绍 Kubernetes 发展过程中，容器运行时的演进过程
- 接着第三部分介绍容器运行时接口的设计以及实现新的容器运行时的方法
- 最后看一下 Kubernetes 社区在容器运行时的发展展望

## Kubernetes 简介

首先来看第一部分，介绍下Kubernetes 的基本原理，并梳理容器运行时在 Kubernetes架构中的位置。

我们知道，Kubernetes是谷歌开源的容器集群管理系统，它的发展非常迅速，已经成为最流行和最活跃的容器编排系统。它提供了完善的集群管理能力，包括多层次的安全防护和准入机制、多租户应用支撑能力、透明的服务注册和服务发现机制、内建负载均衡器、故障发现和自我修复能力、服务滚动升级和在线扩容、可扩展的资源自动调度机制、多粒度的资源配额管理能力。

从架构上来说，Kubernetes 的组件可以分为 Master 和 Node 两部分，其中 Master 是整个集群的大脑，所有的编排、调度、API 访问等都由 Master 来负责。具体的来说，Master 包括以下几个组件：

- etcd 保存了整个集群的状态。
- kube-apiserver 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制。并且无论是集群内部还是外部的组件，都必须通过API Server来访问数据。
- kube-controller-manager 负责维护集群的状态，包括很多资源的控制器，是保证 Kubernetes 声明式 API 工作的大脑，比如故障检测、自动扩展、滚动更新等。
- kube-scheduler 负责资源的调度，按照预定的调度策略将 Pod 调度到相应的 Node 上；

而 Node 则是负责运行具体的容器，并为容器提供存储、网络等必要的功能：

- kubelet 负责维持容器的生命周期，同时也负责 Volume（CSI）和网络（CNI）的管理；
- Container runtime 负责镜像管理以及 Pod 和容器的真正运行（CRI），默认的容器运行时为 Docker；
- kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡
- Network plugin 负责为容器配置网络

![image-20181014230247199](/assets/image-20181014230247199.png)

Kubernetes 除了这些核心的组件以外，还有很多丰富的功能，而这些额外的功能都是通过“Addon”的方式来部署的。比如 kube-dns 和 metrics-server 等，都是以容器的方式部署在集群里面，并提供 API 给其他组件调用。

## Kubelet 架构

Kubelet 负责维持容器的生命周期，同时也配合 kube-controller-manager 管理容器的存储卷，并配合 CNI 管理容器的网络。接下来，我们再来仔细看看 Kubelet 的架构。

![image-20181014230306984](/assets/image-20181014230306984.png)

Kubelet 也是有很多组件构成，包括

- Kubelet Server 对外提供 API，供 kube-apiserver、metrics-server 等服务调用。比如 `kubectl exec` 时需要通过 Kubelet API `/exec/{token}` 与容器进行交互。
- Container Manager 管理容器的各种资源，比如 cgroups、QoS、cpuset、device 等。
- Volume Manager 管理容器的存储卷，比如格式化资盘、挂载到 Node 本地、最后再将挂载路径传给容器。
- Eviction 负责容器的驱逐，比如在资源不足时驱逐优先级低的容器，保证高优先级容器的运行。
- cAdvisor 负责为容器提供 metrics
- Metrics 和 stats 提供容器和节点的度量数据，比如 metrics-server 通过 `/stats/summary` 提取的度量数据是 HPA 自动扩展的依据。
- 再向下呢就是 Generic Runtime Manager，这是容器运行时的管理者，负责于 CRI 交互，完成容器和镜像的管理
- 在 CRI 之下，包括两种容器运行时的实现
  - 一个是内置的 dockershim，实现了 docker 容器引擎的支持以及 CNI 网络插件（包括 kubenet）的支持
  - 另一个就是外部的容器运行时，用来支持 runc、containerd、gvisor 等外部容器运行时

Kubelet 通过 CRI 接口跟外部容器运行时交互，它包括

- CRI Server，这是 CRI gRPC server，监听在 unix socket 上面
- Streaming Server，提供 streaming API，包括 Exec、Attach、Port Forward
- 容器和镜像的管理，比如拉取镜像、创建和启动容器等
- CNI 网络插件的支持，用于给容器配置网络
- 最后是容器引擎的管理，比如支持 runc 、containerd 或者支持多个容器引擎

这样，Kubernetes 中的容器运行时按照不同的功能就可以分为三个部分：

- 第一个是 Kubelet 中容器运行时的管理，它通过 CRI 管理容器和镜像
- 第二个是容器运行时接口，是 Kubelet 与外部容器运行时的通信接口
- 第三个是具体的容器运行时实现，包括 Kubelet 内置的 dockershim 以及外部的容器运行时（如 cri-o、cri-containerd、frakti等）

这样的话，我们就可以基于这三个不同部分来看一看容器运行的演进过程。

## 容器运行时演进过程

![image-20181014230405547](/assets/image-20181014230405547.png)

容器运行时的演进可以分为三个阶段：

首先，在 Kubernetes v1.5 之前，Kubelet 内置了 Docker 和 rkt 的支持，并且通过 CNI 网络插件给它们配置容器网络。这个阶段的用户如果需要自定义运行时的功能是比较痛苦的，需要修改 Kubelet 的代码，并且很有可能这些修改无法推到上游社区。这样，还需要维护一个自己的 fork 分支，维护和升级都非常麻烦。

第二阶段，不同用户实现的容器运行时各有所长，许多用户都希望Kubernetes支持更多的运行时。于是，从v1.5 开始增加了 CRI 接口，通过容器运行时的抽象层消除了这些障碍，使得无需修改 Kubelet 就可以支持运行多种容器运行时。CRI 接口包括了一组 Protocol Buffer、gRPC API 、用于 streaming 接口的库以及用于调试和验证的一系列工具等。在此阶段，内置的 Docker 实现也逐步迁移到了 CRI 的接口之下。但此时 rkt 还未完全迁移，这是因为 rkt 迁移 CRI 的过程将在独立的 repository 完成，方便其维护和管理。

第三阶段，从 v1.11 开始，Kubelet 内置的 rkt 代码删除，CNI 的实现迁移到 dockershim 之内。这样，除了 docker 之外，其他的容器运行时都通过 CRI 接入。外部的容器运行时一般称为 CRI Shim，它除了实现 CRI 接口外，也要负责为容器配置网络。一般推荐使用 CNI，因为这样可以支持社区内的众多网络插件，不过这不是必需的，网络插件只需要满足 Kubernetes 网络的基本假设即可，即 IP-per-Pod、所有 Pod 和 Node 都可以直接通过 IP 相互访问。

## 容器运行时接口（CRI）

容器运行时接口（CRI）是一个用来扩展容器运行时的接口，它基于 gPRC，用户不需要关心内部通信逻辑，而只需要实现定义的接口就可以，包括 `RuntimeService` 和 `ImageService`。

- RuntimeService负责管理Pod和容器的生命周期
- 而ImageService负责镜像的生命周期管理

除了 gRPC API，CRI 还包括用于实现 streaming server 的库（用于 Exec、Attach、PortForward 等接口）和 CRI Tools。

![image-20181014230459955](/assets/image-20181014230459955.png)

基于 CRI 接口的容器运行时通常称为 CRI shim， 这是一个 gRPC Server，监听在本地的unix socket上；而kubelet作为gRPC的客户端来调用CRI接口。另外，外部容器运行时需要自己负责管理容器的网络，推荐使用CNI，这样跟Kubernetes的网络模型保持一致。

CRI 的推出为容器社区带来了新的繁荣，cri-o、frakti、cri-containerd 等一些列的容器运行时为不同场景而生：

- cri-containerd——基于 containerd 的容器运行时
- cri-o——基于 OCI 的容器运行时
- frakti——基于虚拟化的容器运行时

而基于这些容器运行时，还可以轻易联结新型的容器引擎，比如可以通过 clear container、gVisor 等新的容器引擎配合 cri-o 或 cri-containerd 等轻易接入 Kubernetes，将 Kubernetes 的应用场景扩展到了传统 IaaS 才能实现的强隔离和多租户场景。

当使用CRI运行时，需要配置kubelet的`--container-runtime`参数为`remote`，并设置`--container-runtime-endpoint`为监听的unix socket位置（Windows上面为 tcp 端口）。

### CRI 接口

CRI 接口包括 `RuntimeService` 和 `ImageService` 两个服务，这两个服务可以在一个 gRPC server 里面实现，当然也可以分开成两个独立服务。目前社区的很多运行时都是将其在一个 gRPC server 里面实现。

![image-20181014230528339](/assets/image-20181014230528339.png)

管理镜像的 ImageService 提供了 5 个接口，分别是查询镜像列表、拉取镜像到本地、查询镜像状态、删除本地镜像以及查询镜像占用空间等。这些都很容易映射到 docker API 或者 CLI 上面。

而 RuntimeService 则提供了更多的接口，按照功能可以划分为四组：

- PodSandbox 的管理接口：PodSandbox 是对 Kubernete Pod 的抽象，用来给容器提供一个隔离的环境（比如挂载到相同的 cgroup 下面），并提供网络等共享的命名空间。PodSandbox 通常对应到一个 Pause 容器或者一台虚拟机。
- Container 的管理接口：在指定的 PodSandbox 中创建、启动、停止和删除容器。
- Streaming API 接口：包括 Exec、Attach 和 PortForward 等三个和容器进行数据交互的接口，这三个接口返回的是运行时 Streaming Server 的 URL，而不是直接跟容器交互。
- 状态接口，包括查询 API 版本和查询运行时状态。

### Streaming API

Streaming API 用于客户端与容器进行交互，包括Exec、PortForward 和 Attach 等三个接口。Kubelet 内置的 docker 通过 nsenter、socat 等方法来支持这些特性，但它们不一定适用于其他的运行时，也不支持 Linux 之外的其他平台。因而，CRI 也显式定义了这些 API，并且要求容器运行时返回一个 streaming server 的 URL 以便 Kubelet 重定向 API Server 发送过来的流式请求。

这是因为所有容器的流式请求都会经过 Kubelet，这有可能会给节点的网络流量带来瓶颈，因而 CRI 要求容器运行时启动一个对应请求的单独的流服务器，将地址返回给Kubelet。Kubelet然后将这个信息再返回给Kubernetes API Server，它会打开直接与运行时提供的服务器相连的流连接，并通过它跟客户端连通。

![image-20181014230541934](/assets/image-20181014230541934.png)

这样一个完整的 Exec 流程就如上图所示，分为多个阶段：

- 客户端 `kubectl exec -i -t ...`
- kube-apiserver 向 Kubelet 发送流式请求 `/exec/`
- Kubelet 通过 CRI 接口向 CRI Shim 请求 Exec 的 URL
- CRI Shim 向 Kubelet 返回 Exec URL
- Kubelet 向 kube-apiserver 返回重定向的响应
- kube-apiserver 重定向流式请求到 Exec URL，接着就是 CRI Shim 内部的 Streaming Server 跟 kube-apiserver 进行数据交互，完成 Exec 的请求和响应

在 v1.10 及更早版本中，容器运行时必需返回一个 API Server 可直接访问的 URL（通常跟 Kubelet 使用相同的监听地址）；而从 v1.11 开始，Kubelet 新增了` --redirect-container-streaming`选项（默认为 false），支持不转发而是代理 Streaming 请求，这样运行时可以返回一个 localhost 的 URL（当然也不再需要配置 TLS）。

### 容器运行时实例

以下是几个常见容器运行时的例子，它们各有所长，并且也支持不同的容器引擎：

| **CRI** **容器运行时** | **维护者** | **主要特性**                 | **容器引擎**               |
| ---------------------- | ---------- | ---------------------------- | -------------------------- |
| **Dockershim**         | Kubernetes | 内置实现、特性最新           | docker                     |
| **cri-o**              | Kubernetes | OCI标准不需要Docker          | OCI（runc、kata、gVisor…） |
| **cri-containerd**     | Containerd | 基于 containerd 不需要Docker | OCI（runc、kata、gVisor…） |
| **Frakti**             | Kubernetes | 虚拟化容器                   | hyperd、docker             |
| **rktlet**             | Kubernetes | 支持rkt                      | rkt                        |
| **PouchContainer**     | Alibaba    | 富容器                       | OCI（runc、kata…）         |
| **Virtlet**            | Mirantis   | 虚拟机和QCOW2镜像            | Libvirt（KVM）             |

## 多租户

在多租户场景下，强隔离（特别是虚拟化级别的隔离）是一个最基本的需求。

以前使用 Kubernetes 时，由于只支持Docker 容器，而它只提供了内核命名空间（namespace）的隔离，虽然也支持 SELinux、AppArmor 等基本的安全控制，但还是无法满足多租户的需求。所以曾经社区有人提出节点独占的方式实现租户隔离，即每个容器或租户独占一台虚拟机，资源的浪费是很明显的。

有了 CRI 之后，就可以接入 Kata Container、Clear Container 等基于虚拟化的容器引擎。这样通过虚拟化实现了容器的强隔离，不同租户的容器也可以运行在相同的 Node 上，大大提高了资源的利用率。

当然了，多租户不仅需要容器自身的强隔离，还需要众多其他的功能一起配合，比如

* 网络隔离，比如可以使用 CNI 构建新的网络插件，把不同租户的 Pod 接入到相互隔离的虚拟网络中。
* 资源管理，比如基于 CRD 构建租户 API 和租户控制器，管理租户和租户的资源。
* 认证、授权、配额管理等等也都可以在 Kubernetes API 之上构建。

## CRI Tools

[CRI Tools](https://github.com/kubernetes-sigs/cri-tools) 是社区 Node 组针对 CRI 接口开发的辅助工具，它包括两个工具：crictl 和 critest。

crictl 是一个容器运行时命令行接口，它对系统和应用的排错来说是个很有用的工具。当使用 Docker 运行时，调试系统信息的时候我们可能使用  `docker ps` 和 `docker inspect` 等命令检查应用的进程情况。但是对于其他基于 CRI 的容器运行时来说，它们可能没有自己的命令行工具；或者即便有，它们的操作界面也不一定与 Kubernetes 中的概念一致。更不用说，很有很多的命令对 Kubernetes 没什么用，甚至会损害系统（比如 docker rename）。因而，我们推荐使用 `crictl` 作为 Docker CLI 的继任者，用于 Kubernetes 节点上 pod、容器以及镜像的除错工具。

crictl 提供了类似 Docker CLI 的使用体验， 并且支持所有 CRI 兼容的容器运行时。并且，crictl 提供了一个对 Kubernetes 来说更加友好的容器视角：它就是为 Kubernetes 而设计的，有不同的命令分别与Pod 和容器进行交互。例如 `crictl pods` 会列出 Pod 信息，而 `crictl ps` 只会列出应用容器的信息。

而 critest 则是一个容器运行时的验证测试工具，用于验证容器运行时是否符合 Kubelet CRI 的要求。除了验证测试，critest 还提供了 CRI 接口的性能测试，比如 `critest -benchmark`。

推荐将 critest 集成到容器运行时开发的 Devops 流程中，保证每个变更都不会破坏 CRI 的基本功能。另外，还可以选择将 critest 的测试结果与 Kubernetes Node E2E 的结果提交到 Sig-node 的 [TestGrid](https://contributor.kubernetes.io/contributors/devel/cri-testing-policy/)，向社区和用户展示。

## 未来展望

最后一部分是容器运行时的未来展望，这里讨论两个点，即多容器运行时 RuntimeClass 以及无服务器容器服务。

### 多容器运行时

多容器运行时用于不同的目的，比如使用虚拟化容器引擎式运行不可信应用和多租户应用，而使用 Docker 运行系统组件或者无法虚拟化的容器（比如需要 HostNetwork 的容器）。比如典型的用例为：

- Kata Containers/gVisor + runc
- Windows Process isolation + Hyper-V isolation containers

以前，多容器运行时通常以注解（Annotation）的形式支持，比如 cri-o、frakti 等都是这么支持了多容器运行时。但这一点也不优雅，并且也无法实现基于容器运行时来调度容器。因而，Kubernetes 在 v1.12 中将开始增加 RuntimeClass 这个新的 API 对象，用来支持多容器运行时。

RuntimeClass 表示一个运行时，在使用前需要开启特性开关 `RuntimeClass`，并创建 RuntimeClass CRD：

```sh
kubectl apply -f https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/runtimeclass/runtimeclass_crd.yaml
```

然后就可以定义 RuntimeClass 对象

```yaml
apiVersion: node.k8s.io/v1alpha1  # RuntimeClass is defined in the node.k8s.io API group
kind: RuntimeClass
metadata:
  name: myclass  # The name the RuntimeClass will be referenced by
  # RuntimeClass is a non-namespaced resource
spec:
  runtimeHandler: myconfiguration  # The name of the corresponding CRI configuration
```

接着，就可以在 Pod 中定义使用哪个 RuntimeClass：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  runtimeClassName: myclass
  # ...
```

在未来版本中，RuntimeClass还会支持基于 Node 上实际运行的容器运行时来调度 Pod。

### 无服务器容器服务

无服务器（Serverless）现在是一个很热门的方向，各个云平台也提供很多种类的无服务器计算服务，比如 Azure Container Instance、AWS Farget 等。它们的好处是用户不需要去管理容器底层的基础设施，而只需要管理容器即可，并且容器通常按实际的运行时间收费。这样，对用户来说，不仅省去了管理基础设施的繁琐步骤，还更节省成本。

那么 CRI 在这里有什么应用场景呢？假如你是一个云平台的管理者，想要构建一个无服务器容器服务，那么使用 CRI 配合多容器运行时就是一个很好的思路。这样的话，

* Kubernetes 可以用来给整个平台提供调度和编排
* 基于 Kubernetes API 可以搭建租户管理功能
* 基于 CRI 可以实现多租户容器运行的强隔离
* 基于 CNI 可以实现多租户的网络强隔离

那么，对云平台的用户呢？这些无服务器容器服务提供的功能通常都比较简单，并不具备编排的功能。但可以借助 Virtual Kubelet 项目，使用 Kubernetes 为这些平台的容器提供编排功能。

Virtual Kubelet 是针对 Serverless 容器平台设计的虚拟 Kubernetes 节点，它模拟了 Kubelet 的功能，并将 Serverless 容器平台抽象为一个虚拟的无限资源的 Node。这样就可以通过 Kubernetes API 来管理其上的容器。

![image-20181014230850615](/assets/image-20181014230850615.png)

目前 Virtual Kubelet 已经支持了众多的云平台，包括

- Azure Container Instance
- AWS Farget
- Service Fabric
- Hyper.sh
- IoT Edge

以上，就是“Kubernetes 容器运行时演进”的所有内容。

