---
title: "Kubernetes 1.32 新特性解析"
date: 2025-01-04T15:41:42+08:00
tags: [Kubernetes]
draft: false
---

Kubernetes v1.32 是一次充满意义的版本更新，它不仅标志着 Kubernetes 十周年的里程碑，更展现了社区在推动云原生计算领域技术发展的坚持与创新。本文将带你一起看一看 1.32 版本带来了哪些新的功能特性以及升级过程中需要注意的事项。

## 核心功能特性（GA）

v1.32 版本共包含 44 项增强功能。其中，13 项已升级至稳定版，分别是：

- [结构化授权配置](https://github.com/kubernetes/enhancements/issues/3221)
- [绑定服务帐户令牌改进](https://github.com/kubernetes/enhancements/issues/4193)
- [CRD 字段选择器](https://github.com/kubernetes/enhancements/issues/4358)
- [重试生成名称](https://github.com/kubernetes/enhancements/issues/4420)
- [Kubernetes 感知负载均衡器的行为 (LoadBalancerIPMode)](https://github.com/kubernetes/enhancements/issues/1860)
- [Pod 添加 `status.hostIPs`](https://github.com/kubernetes/enhancements/issues/2681)
- [自定义 kubectl debug 配置文件](https://github.com/kubernetes/enhancements/issues/4292)
- [内存管理](https://github.com/kubernetes/enhancements/issues/1769)
- [支持调整内存支持的卷大小](https://github.com/kubernetes/enhancements/issues/1967)
- [拓扑管理器改进多 NUMA 对齐](https://github.com/kubernetes/enhancements/issues/3545)
- [Job 注释支持创建时间戳](https://github.com/kubernetes/enhancements/issues/4026)
- [为 StatefulSets 和 Indexed Jobs 添加 Pod 索引标签](https://github.com/kubernetes/enhancements/issues/4017)
- [自动删除由 StatefulSet 创建的 PVC](https://github.com/kubernetes/enhancements/issues/1847)

接下来，让我们逐一看看这些重要的 GA 特性。

### 结构化授权配置

Kubernetes 允许为 API Server 配置包含多个 Webhook 的授权链。该链中的授权项可以具有定义明确的参数，以特定顺序验证请求，为您提供细粒度控制，例如在失败时显式拒绝。

通过配置文件的方法，您甚至可以指定 CEL 规则，在将请求分派到 Webhook 之前进行预过滤，从而帮助防止不必要的调用。当修改配置文件时，API 服务器还会自动重新加载授权链。

您可以使用 `--authorization-config` 命令行参数指定授权配置的路径。当 API Server 检测到配置文件的更改时，Kubernetes 会重新加载该文件，如果未检测到更改事件，则每隔 60 秒重新加载一次。

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AuthorizationConfiguration
authorizers:
  - type: Webhook
    name: webhook
    webhook:
      authorizedTTL: 30s
      unauthorizedTTL: 30s
      timeout: 3s
      subjectAccessReviewVersion: v1
      matchConditionSubjectAccessReviewVersion: v1
      failurePolicy: Deny
      connectionInfo:
        type: KubeConfigFile
        kubeConfigFile: /kube-system-authz-webhook.yaml
      matchConditions:
      - expression: has(request.resourceAttributes)
      - expression: "!('system:serviceaccounts:kube-system'in request.groups)"
  - type: Node
    name: node
  - type: RBAC
    name: rbac
  - type: Webhook
    name: in-cluster-authorizer
    webhook:
      authorizedTTL: 5m
      unauthorizedTTL: 30s
      timeout: 3s
      subjectAccessReviewVersion: v1
      failurePolicy: NoOpinion
      connectionInfo:
        type: InClusterConfig
```

这个配置示例展示了如何结合使用外部 Webhook 和内置的 RBAC 授权器, 并通过 CEL 表达式对请求进行预过滤。

### 优化动态资源分配 (DRA)

动态资源分配 (Dynamic Resource Allocation, DRA) 在 v1.32 中优化了专用硬件（如 GPU、FPGA 和网络适配器）的支持。最值得关注的是，结构化参数支持（Structured Parameter Support）现已升级至 Beta，允许 kube-scheduler 和 Cluster Autoscaler 直接模拟资源分配，无需依赖第三方驱动器，从而显著提高了资源调度的效率。

### Node 和 Sidecar 改进

**1. systemd Watchdog 集成**

在这一版本中，systemd 被用于监控 kubelet 的运行状态，在其健康检查失败时自动重启，并限制重启频率。这一改进将进一步提升 kubelet 的稳定性。

**2. ImagePullBackOff 错误消息优化**

当镜像拉取失败时，Pod 状态中的错误消息现在会显示具体原因。例如，若签名验证失败，消息将明确指出问题所在，帮助用户快速定位并解决问题。

**3. Sidecar 容器功能即将稳定**

Sidecar 容器的稳定性改进目标计划在 v1.33 中达成，这将进一步提升其在复杂工作负载中的表现。

### CRD 字段选择器

CRD 字段选择器允许客户端根据一个或多个资源字段的值选择自定义资源。所有 CRD 都支持 `metadata.name` 和 `metadata.namespace` 字段选择器。

在 CustomResourceDefinition 中声明的字段，当包含在 CustomResourceDefinition 的 `spec.versions[*].selectableFields` 字段中时，也可以与字段选择器一起使用。

### 支持调整内存支持的卷大小

该功能允许用户根据 Pod 的资源限制动态调整内存卷的大小（默认是节点内存的 50%），提升了资源利用率。

比如，emptyDir 默认使用节点存储，设置 `emptyDir.medium` 为 "Memory" 后使用内存存储，现在也可以通过 sizeLimit 配置内存大小：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 500Mi
      medium: Memory
```

### 自动删除由 StatefulSet 创建的 PVC

StatefulSet 所创建的 PVC 在不需要时将被自动删除，同时确保在有 StatefulSet 更新和节点维护期间的数据持久性。

你可以通过 `.spec.persistentVolumeClaimRetentionPolicy` 字段控制在 StatefulSet 生命周期中是否以及如何删除 PVC。启用后，您可以为每个 StatefulSet 配置两种策略：

- `whenDeleted`：配置 StatefulSet 删除时适用的卷保留行为。
- `whenScaled`：配置 StatefulSet 副本数量减少时适用的卷保留行为。

```yaml
apiVersion: apps/v1
kind: StatefulSet
...
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Delete
...
```

此功能简化了 StatefulSets 的存储管理，并降低了孤儿 PVC 的风险。

### 内存管理器正式 GA

在 Kubernetes 1.32 中，NUMA 感知内存管理器正式升级为通用可用性（GA），标志着在实现容器化应用高效且可预测的内存分配之路上的一个重要里程碑。自从 Kubernetes v1.22 升级到 Beta 阶段以来，内存管理器已被证明是可靠、稳定的，并且是 CPU 管理器的良好补充功能。

作为 kubelet 工作负载接纳过程的一部分，内存管理器提供拓扑提示以优化内存分配和对齐。这使用户能够为 Guaranteed QoS 类别中的 Pod 分配专属内存。内存管理器使用提示生成协议为 Pod 提供最合适的 NUMA 亲和性。内存管理器将这些亲和性提示传递给中央管理器（拓扑管理器）。根据提示和拓扑管理器策略，Pod 会被拒绝或接纳到节点中。此外，内存管理器确保分配给 Pod 的内存来自尽可能少数的 NUMA 节点。

除了 Linux 内存管理器正式 GA 外，Windows 节点也已经支持了 Alpha 版的内存管理器。

### Kubernetes 感知负载均衡器的行为 (LoadBalancerIPMode)

在 Service 的 loadBalancer 状态中新增了一个可配置的 ipMode 字段，允许云服务提供商将 kube-proxy 的行为与其负载均衡器实现对齐。目前，kube-proxy 默认将外部 IP 绑定到节点，这可能导致健康检查失败或绕过负载均衡器功能（如 TLS 终止和 PROXY 协议）。新的 ipMode 设置使提供商可以选择 Proxy 模式，从而绕过直接 IP 绑定并解决这些问题，同时保留现有的 VIP 模式作为默认设置。

`.status.loadBalancer.ingress.ipMode` 有两个可能的值：“VIP” 和 “Proxy”。默认值是 “VIP”，这意味着流量被传送到节点，目标设置为负载均衡器的 IP 和端口。将其设置为 “Proxy” 时有两种情况，取决于云提供商的负载均衡器如何传递流量：

- 如果流量被传送到节点然后进行 DNAT 到 pod，则目标会设置为节点的 IP 和节点端口；
- 如果流量直接传送到 pod，则目标会设置为 pod 的 IP 和端口。

## Beta 特性

除了 GA 特性, 1.32 版本还引入了多项 Beta 特性。这些特性虽然还不够稳定, 但已经可以在非关键环境中使用, 并且预示着 Kubernetes 未来的发展方向。

- [允许 informers 获取数据流而不是分块（API Streaming）](https://github.com/kubernetes/enhancements/issues/3157)
- [使用字段和标签选择器进行授权](https://github.com/kubernetes/enhancements/issues/4601)
- [仅允许匿名认证访问配置的端点](https://github.com/kubernetes/enhancements/issues/4633)
- [支持从卷扩展失败中恢复](https://github.com/kubernetes/enhancements/issues/1790)
- [卷组快照](https://github.com/kubernetes/enhancements/issues/3476)
- [通过挂载具有正确 SELinux 标签的卷来加速容器启动，而不是递归地更改卷上的每个文件](https://github.com/kubernetes/enhancements/issues/1710)
- [QueueingHint 调度器优化](https://github.com/kubernetes/enhancements/issues/4247)
- [添加对 kubelet 配置目录的支持](https://github.com/kubernetes/enhancements/issues/3983)
- [允许在环境变量中使用几乎所有可打印的 ASCII 字符](https://github.com/kubernetes/enhancements/issues/4369)
- [DRA: 结构化参数](https://github.com/kubernetes/enhancements/issues/4381)
- [Job API ManagedBy](https://github.com/kubernetes/enhancements/issues/4368)
- [结构化身份验证配置](https://github.com/kubernetes/enhancements/issues/3331)

### API Streaming

在 API Streaming 之前，List API 请求有很多的性能问题：

- kube-apiserver 在处理 list 请求时，会在内存中组装整个响应，然后再传输给客户端（服务器在发送第一个字节给客户端之前，必须从数据库中获取数据、反序列化数据，并将其转换为客户端请求的格式）。
- 当响应体非常大时（例如数百兆字节），或者在网络中断后多个 list 请求同时涌入时，这种方法会导致内存过载。
- API 优先级和公平性 在 CPU 过载保护方面表现良好，但在内存保护方面效果较小。
- 内存消耗的性质不同于 CPU，内存是不可压缩的，可能会随着处理对象数量的增加而无限增长。

Kubernetes v1.32 将 API Streaming（watch list）特性升级到 Beta 阶段。Watch 请求通过 watch cache 提供服务，watch cache 是一个内存缓存，旨在提高读取操作的可扩展性。通过逐个流式传输每个项目而不是返回整个集合，新方法保持了恒定的内存开销。测试发现，在启用 watch list 功能的情况下，kube-apiserver 的内存消耗稳定在约 2 GB；而在未启用该功能的情况下，内存使用量增加到约 20GB，增加了 10 倍。

要使用 API Streaming，需要升级 Kubernetes 到 1.32，确保集群使用 etcd 版本 3.4.31+ 或 3.5.13+，并修改客户端软件以使用 watch list。对于用 Golang 编写的客户端代码，需要为 client-go 启用 WatchListClient。

### QueueingHint 调度器优化

在 Kubernetes v1.32 之前，调度器在处理未调度的 Pod 时存在以下几个问题：

1. **事件重排过于宽泛**：调度器依赖于事件来决定何时重试调度未成功的 Pod。然而，这种方法可能会导致不必要的调度重试，因为事件的触发条件过于宽泛。例如，一个新创建的 Pod 可能会触发调度重试，但如果这个 Pod 没有匹配未调度 Pod 的亲和性要求，那么重试是没有意义的。

2. **`preCheck` 的局限性**：`preCheck` 功能用于在调度前进一步过滤事件，以提高效率。然而，这个功能依赖于内置插件的逻辑，无法扩展到自定义插件。这意味着对于使用自定义插件的用户，`preCheck` 无法提供有效的事件过滤。

3. **调度重试效率低下**：由于调度器需要逐个处理 Pod，如果没有有效的机制来判断哪些 Pod 可以重新尝试调度，调度器可能会浪费多个调度周期在那些无法调度的 Pod 上。

这些问题导致了调度器在处理大规模集群时的效率问题，特别是在需要频繁重试调度的情况。

为了解决这些问题，v1.32 重启默认开启了 QueueingHint 机制（代码自 v1.28 引入）。QueueingHint 通过订阅特定的集群事件并判断这些事件是否可能使 Pod 可调度，从而优化了 Kubernetes 调度器的 Pod 重试机制，提高了调度效率。

### 卷组快照

一些存储系统提供创建多个卷的一致性快照的能力，组快照代表从多个卷中创建同一时间点的副本。卷组快照功能允许从多个卷在同一时间点创建快照，以实现写入顺序一致性，这对于包含多个卷的应用程序非常有用。

注意，卷组快照仅支持 CSI Volume。

### 从卷扩展失败中恢复

新功能允许用户在卷扩展失败后重新尝试，这一改进降低了数据丢失或资源浪费的可能性。

### Job 支持 managed-by

通过新增的 `managedBy` 字段，用户可以更灵活地将 Job 的管理交由外部控制器（如 Kueue），从而实现跨多个集群的无缝作业管理。通过明确指定负责的控制器，该增强功能简化了工作流程，避免了冲突更新，并确保更可靠的状态同步。

## Alpha 特性

Alpha特性代表了Kubernetes的实验性功能,虽然不建议在生产环境中使用,但它们展示了平台未来的发展方向。1.32版本引入了多项令人兴奋的Alpha特性:

- [基于 CEL 的准入策略](https://github.com/kubernetes/enhancements/issues/3962)
- [放宽 DNS 搜索字符串验证](https://github.com/kubernetes/enhancements/issues/4427)
- [调度器中的异步抢占](https://github.com/kubernetes/enhancements/issues/4832)
- [分离容器的 stdout 和 stderr 日志流](https://github.com/kubernetes/enhancements/issues/3288)
- [Pod 级资源请求](https://github.com/kubernetes/enhancements/issues/2837)
- [为设备插件和 DRA 在 Pod 状态中添加资源健康状态](https://github.com/kubernetes/enhancements/issues/4680)
- [在 CPU 管理器中分离 L3 缓存拓扑感知](https://github.com/kubernetes/enhancements/issues/4800)
- [DRA：资源声明状态可能包含标准化的网络接口数据](https://github.com/kubernetes/enhancements/issues/4817)
- [Kubernetes 组件的状态信息 (Statusz)](https://github.com/kubernetes/enhancements/issues/4827)
- [Kubernetes 组件的标志信息 (Flagz)](https://github.com/kubernetes/enhancements/issues/4828)
- [细粒度的 Kubelet API 授权](https://github.com/kubernetes/enhancements/issues/2862)
- [允许 PreStop 钩子的 Sleep 动作为零值](https://github.com/kubernetes/enhancements/issues/4818)
- [服务账户令牌外部签名的 API](https://github.com/kubernetes/enhancements/issues/740)
- [Windows CPU 和内存亲和性](https://github.com/kubernetes/enhancements/issues/4885)
- [处理无法解密的资源](https://github.com/kubernetes/enhancements/issues/3926)
- [CBOR 序列化器](https://github.com/kubernetes/enhancements/issues/4222)
- [CPU 管理器新增严格 CPU 预留](https://github.com/kubernetes/enhancements/issues/4540)
- [Windows 节点优雅关闭](https://github.com/kubernetes/enhancements/issues/4802)

### 调度器异步抢占

Kubernetes 调度器已通过异步抢占功能得到增强，该功能通过异步处理抢占操作来提高调度吞吐量。抢占确保高优先级 Pod 通过驱逐低优先级 Pod 来获得所需资源，但此过程之前涉及重操作，如删除 Pod 的 API 调用，从而减慢了调度器。通过此增强，此类任务现在并行处理，允许调度器继续调度其他 Pod 而不会延迟，提高了调度效率，从而加快整体调度吞吐量。

此功能对于 Pod churn 率高的集群或频繁调度失败的集群特别有用，确保更高效和更具弹性的调度过程。

### 准入策略支持 CEL 表达式

该功能利用 CEL 的对象实例化和 JSON 补丁策略，结合服务器端应用的合并算法。它简化了策略定义，减少了突变冲突，并提高了准入控制性能，同时为 Kubernetes 中更强大、可扩展的策略框架奠定了基础。

Kubernetes API 服务器现在支持基于通用表达式语言（CEL）的修改型准入策略，提供了一种轻量级、高效的修改型准入网关的替代方案。使用此增强功能，管理员可以使用 CEL 来声明设置标签、默认字段或注入 sidecars 等突变，只需简单的声明式表达式即可。这种方法降低了操作复杂性，消除了对 webhooks 的需求，并直接与 kube-apiserver 集成，提供更快、更可靠的进程内变更处理。

### Pod 级资源

此增强功能通过在 Pod 级别设置资源请求和限制，简化了 Kubernetes 的资源管理，创建了一个所有 Pod 中的容器都可以动态使用的共享池。这对于具有波动或突发资源需求的容器工作负载尤其有价值，因为它最小化了过度配置并提高了整体资源效率。

通过在 Pod 级别利用 Linux cgroup 设置，Kubernetes 确保在启用紧密耦合的容器更有效地协作的同时，强制执行这些资源限制，而不会遇到人为的限制。并且，此功能与现有容器级别的资源设置保持向后兼容，使用户能够逐步采用，而不会干扰当前的工作流程或现有配置。这标志着多容器 Pods 的重大改进，因为它降低了跨容器管理资源分配的操作复杂性。它还为紧密集成的应用程序提供性能提升，例如侧边架构，其中容器共享工作负载或依赖于彼此的可用性以实现最佳性能。

### CPU 管理器新增严格 CPU 预留

CPU 管理器的静态策略用于减少延迟或提高性能。reservedSystemCPUs 定义了一个明确的 CPU 集，用于操作系统系统守护进程和 Kubernetes 系统守护进程。此选项专为电信 / NFV 类型用例设计，在这些用例中，不受控的中断 / 计时器可能会影响工作负载性能。您可以使用此选项为系统 / Kubernetes 守护进程以及中断 / 计时器定义明确的 CPU 集，这样系统上的其余 CPU 就可以专门用于工作负载，并且受到不受控中断 / 计时器的影响较小。

启用了 `strict-cpu-reservation` 策略之后，静态策略将不允许任何工作负载使用 `reservedSystemCPUs` 中指定的 CPU 核心。你可以通过在 CPUManager 策略选项中添加 `strict-cpu-reservation=true`，然后删除 `/var/lib/kubelet/cpu_manager_state` 文件并重启 kubelet 来启用 `strict-cpu-reservation` 选项。

```yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
featureGates:
  ...
  CPUManagerPolicyOptions: true
  CPUManagerPolicyAlphaOptions: true
cpuManagerPolicy: static
cpuManagerPolicyOptions:
  strict-cpu-reservation: "true"
reservedSystemCPUs: "0,32,1,33,16,48"
...
```

### Windows 节点改进

**优雅关闭功能**:

Windows 节点现已支持优雅关闭，确保 Pod 在节点关闭时能够正常终止，避免工作负载中断。

以前，当节点关闭时，Pod 通常会被突然终止，绕过了关键的生命周期事件（如 pre-stop 钩子）。这可能会导致依赖于优雅终止来清理资源或保存状态的工作负载出现问题。有了优雅关闭之后，Windows 节点上的 kubelet 将能够感知底层节点关闭事件，并为 Pod 启动适当的关闭序列，从而确保它们按照其预期方式被终止，提高了可靠性和工作负载的一致性。

**资源亲和性支持**:

改进后的 CPU 和内存管理功能提升了 Windows 节点的性能和资源分配效率。


### 允许 PreStop 钩子的 sleep 动作为零

此增强功能引入了在 Kubernetes 中为 PreStop 生命周期钩子设置零秒睡眠时间的能力，为资源验证和定制提供了更灵活且无操作的选项。

之前，尝试为睡眠动作定义零值会导致验证错误，限制了其使用。本次更新后，用户可以将零秒持续时间配置为有效的睡眠设置，使在需要时能够实现立即执行和终止行为。

增强功能向后兼容，作为由 `PodLifecycleSleepActionAllowZero` 功能门控器控制的可选功能引入。此更改特别有利于需要 PreStop 钩子进行验证或无需实际睡眠时间的 admission webhook 处理的场景。通过与 `time.After` Go 函数的功能相匹配，此更新简化了配置并扩展了 Kubernetes 工作负载的可用性。

### DRA：资源请求状态标准网络接口数据

DRA 添加了一个新字段，允许驱动程序报告资源请求中每个分配对象的具体设备状态数据。同时，它还建立了一种标准化的方式来表示网络设备信息。

### 核心组件新增 /statusz 和 /flagz

核心组件新增 /statusz 和 /flagz，可用于了解组件运行版本（如 Golang 版本）、运行时间和执行时使用的命令行标志等详细信息，增强了集群的可调试性，使得诊断运行时和配置问题更加容易。

## 升级注意事项

在升级就版本集群到 v1.32之前，需要注意：

1. 删除了 1.26 引入的旧版 DRA（Classic DRA），使用了旧版 DRA 的用户需要先升级到新版本再进行升级。

2. FlowSchema 和 PriorityLevelConfiguration 的 `flowcontrol.apiserver.k8s.io/v1beta3` API 版本已移除，需切换到 v1.29 引入的 `flowcontrol.apiserver.k8s.io/v1` （所有现有持久化对象都可通过新 API 访问）。另外，注意优先级配置 `spec.limited.nominalConcurrencyShares` 字段仅在未指定时默认为 30，显式值 0 不会被更改为 30。
