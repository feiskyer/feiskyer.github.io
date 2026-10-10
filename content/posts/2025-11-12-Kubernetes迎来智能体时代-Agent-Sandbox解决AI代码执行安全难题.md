---
title: "Kubernetes 迎来智能体时代：Agent Sandbox 解决 AI 代码执行安全难题"
date: 2025-11-12T22:00:00+08:00
draft: false
tags: [AI, Vibe Coding, Agent, Kubernetes]
description: "KubeCon NA 2025 上 Google 发布开源项目 Agent Sandbox，专为 AI Agent 代码执行设计，解决传统容器隔离不足、提示词注入风险以及数千沙箱快速创建销毁等难题，本文剖析其由来与 Kubernetes 的智能体演进。"
---

AI Agent 正在改变整个软件行业的游戏规则。

AI Agent 可以自主规划并执行复杂的多步骤任务，任何已有的软件都有机会借助 AI Agent 的赋能实现真正的智能化。

但是，在功能强大的同时，AI Agent 也有很多的不确定行为，包括生成的代码、执行的命令、浏览器的操作等等都无法事先预测，更不用说还需要防范提示词注入攻击。如果缺少强有力的安全和运维保障，这些不确定性很高的 Agent 可能会带来巨大风险。

此外，AI Agent 还有一些传统应用没有的基础设施需求，最突出的就是需要编排数千个沙箱作为临时环境，快速创建和删除，同时还要确保网络访问是受控的。

说到运行 AI Agent，Kubernetes 凭借其成熟、安全和可扩展性，确实是最合适的选择。但即使是 Kubernetes，也需要进一步演进，才能更好地满足 AI Agent 的执行。

Agent Sandbox 项目就是 Kubernetes 朝这个方向迈出的重要一步。在刚刚召开的 2025 年 KubeCon NA 大会上，Google 正式发布了 **Agent Sandbox**——一个专门为 AI Agent 代码执行设计的开源项目。本文就带你一起来看看这个项目的由来。

## 传统容器隔离为什么不够用？

Kubernetes 已经采用容器进行应用的隔离，但在 AI Agent 场景里面，仅靠容器的隔离是不够的。

容器会共享宿主机内核，一旦某个容器中的恶意代码找到内核漏洞，就可以突破容器边界，访问宿主机或其他容器的数据，也就是有容器逃逸风险。

对于传统应用来说，这个风险是可控的。代码是开发者编写的，经过了层层测试和审核，可以假定它是可信的。但 AI Agent 场景完全不同。

AI Agent 生成的代码是实时的、动态的，没有经过任何审核流程。它可能写出完全正常的数据分析脚本，也可能不小心生成访问敏感文件的命令。开发者无法提前知道它会做什么。而且一个 AI 应用可能同时服务数千个用户，每个用户的请求都需要一个独立的沙箱环境。这意味着需要在几秒钟内创建和销毁数千个沙箱，而且每个沙箱都必须确保严格隔离。

还有个问题是网络隔离的粒度。AI Agent 可能需要访问外部 API 来完成任务，但又不希望它随意访问内网资源或者向外传输敏感数据。传统容器的网络隔离粒度不够细，很难做到精确控制。

Google 在发布 Agent Sandbox 时明确表示：**为 AI Agent 提供内核级隔离是非协商的需求**（non-negotiable）。这不是过度设计，而是 AI 时代基础设施的刚需。

## Agent Sandbox 怎么解决这些问题？

Agent Sandbox 是 Kubernetes 推出的一个新的 CRD 资源，专门用来管理 AI Agent 的代码执行环境。它跟 Pod、Deployment、StatefulSet 一样，是 Kubernetes 生态里的一个新“公民”，但专为 AI Agent 场景优化。

这个项目是 Google 联合 Kubernetes 社区开发的，由 Kubernetes SIG Apps 维护。

你可能会问，Kubernetes 已经有 StatefulSet 了，为什么还要造一个新轮子？

StatefulSet 确实可以管理有状态的工作负载，但它的设计目标是“有序、稳定的副本集”。比如运行 3 个 MySQL 实例，每个实例有编号（mysql-0、mysql-1、mysql-2），重启后编号不变。

但 AI Agent 的需求不一样。每个用户需要一个独立的沙箱环境，不需要副本。沙箱的生命周期可能只有几分钟，需要极快的启动速度。还有“休眠”功能，当用户暂时不用时，把沙箱挂起节省资源，需要时快速恢复。

用 StatefulSet 来管理这种场景，不是做不到，但肯定不是最优解。

Agent Sandbox 提供了几个关键能力。每个 Sandbox 有稳定的主机名和网络标识，重启后保持不变。可以配置持久卷，数据在沙箱重启后依然保留。支持定时删除、暂停、恢复等操作。通过 SandboxTemplate 定义可复用的配置，避免重复劳动。

除了核心的 Sandbox CRD，Agent Sandbox 还提供了三个扩展组件：

- SandboxTemplate 用来定义可复用的沙箱模板，比如Python 3.11 环境、Node.js 20 环境。
- SandboxClaim 让用户只需要声明“我需要一个 Python 环境”，系统就自动从模板创建。
- SandboxWarmPool 是预热沙箱池，提前创建好一批沙箱，需要时直接分配，大幅降低启动延迟。

这些组件的设计理念跟 Kubernetes 的 PVC（持久卷声明）和 StorageClass 很像。用户不需要关心底层细节，只需要声明需求，系统自动满足。

## 强隔离 + 高性能：技术实现揭秘

Agent Sandbox 的核心挑战是：如何在保证强隔离的同时，还能做到快速启动？

### 隔离层：gVisor 和 Kata Containers

Agent Sandbox 底层支持两种隔离技术：**gVisor** 和 **Kata Containers**。

gVisor 是 Google 开源的一个“用户态内核”。传统容器直接调用宿主机内核，而 gVisor 在中间加了一层。容器的系统调用先经过 gVisor 处理，gVisor 再决定是否转发给真正的内核。即使恶意代码找到了内核漏洞，它攻击的也是 gVisor 这层防护，而不是真正的内核。

Kata Containers 则采用了另一种思路：为每个容器创建一个轻量级虚拟机。虚拟机有自己独立的内核，跟宿主机完全隔离。这种隔离级别更高，但启动速度相对慢一些。

Agent Sandbox 同时支持这两种技术，用户可以根据自己的安全需求选择。在 GKE（Google Kubernetes Engine）上，Google 还提供了托管的 GKE Sandbox，底层用的就是 gVisor。不需要自己维护 gVisor，直接用就行。

### 性能优化：从分钟到亚秒

光有强隔离还不够，AI Agent 场景对性能的要求也很高。用户发了个请求，等了 2 分钟才看到沙箱启动完成，体验肯定很差。

Agent Sandbox 用了两个关键技术来解决启动速度问题。

**预热池（Warm Pool）**

预热池的思路很简单。提前创建好一批沙箱，放在“池子”里待命。当用户发起请求时，直接从池子里拿一个现成的沙箱，用完再放回池子。

通过预热池，Agent Sandbox 可以把启动延迟降到亚秒级，相比冷启动提升了 90%。

**快照恢复（Pod Snapshots）**

这是 GKE 独家提供的功能。

可以把一个运行中的 Pod 完整地拍个快照，保存它的内存状态、文件系统、进程信息等等。之后需要恢复时，直接从快照启动，几秒钟就能回到之前的运行状态。

这个功能特别有用。把 Python 环境、依赖库都装好，拍个快照，之后每次启动直接用快照，省掉了漫长的 `pip install` 过程。用户暂时不用沙箱时，拍快照然后销毁 Pod，节省计算资源。用户回来时，从快照恢复，几乎感觉不到中断。

Pod Snapshots 不仅支持 CPU 工作负载，还支持 GPU 工作负载。对于需要 GPU 的 AI 推理任务，可以把模型加载到 GPU 后拍快照，下次启动直接跳过模型加载阶段。

根据 Google 的测试数据，传统容器冷启动需要 10-30 秒，资源占用中等。Agent Sandbox 配合 Warm Pool 启动时间小于 1 秒，但池子会预占用一些资源。Agent Sandbox 配合 Pod Snapshots 启动时间 2-5 秒，空闲时不占资源。

Warm Pool 和 Pod Snapshots 适用于不同场景。高并发场景用 Warm Pool，牺牲一些资源换取极致速度。成本敏感场景用 Pod Snapshots，启动慢几秒，但空闲时不占资源。

## 为 AI 工程师设计的体验

Agent Sandbox 有个很重要的设计理念：**AI 工程师不应该被迫成为 Kubernetes 专家**。

写过 Kubernetes 的 YAML 配置的人都知道那有多繁琐。一个简单的应用，可能要写几十行 YAML，配置 Pod、Service、Ingress、ConfigMap…… 对于专注于 AI 模型和应用逻辑的工程师来说，这些基础设施细节是个巨大的负担。

Agent Sandbox 提供了一个 Python SDK，用几行 Python 代码就能完成沙箱的整个生命周期管理。

### 代码示例

```python
from agentic_sandbox import Sandbox

# 使用上下文管理器创建沙箱
with Sandbox(template_name="python3-template", namespace="ai-agents") as sandbox:
    # 在沙箱中执行代码
    result = sandbox.run("print('Hello from inside the sandbox!')")
    print(result)

# 沙箱会在 with 块结束时自动清理
```

就这么简单。不需要写一行 YAML，不需要懂什么是 CRD，不需要关心底层是 gVisor 还是 Kata Containers。

SDK 帮你做了这些事情：根据模板名称找到对应的 SandboxTemplate，创建 Sandbox 资源，等待 Pod 启动完成，建立到沙箱的连接，执行代码并返回结果，清理资源。

这种设计体现了一个重要的工程理念：关注点分离（Separation of Concerns）。

AI 工程师关注的是：我需要一个 Python 环境来运行代码。平台工程师关注的是：这个环境用什么隔离技术、怎么配置网络策略、如何监控和告警。

Agent Sandbox 通过模板机制实现了这种分离。平台工程师定义好各种 SandboxTemplate（Python 3.11、Node.js 20、带 GPU 的环境等），AI 工程师只需要指定模板名称，就能获得一个配置好的沙箱。

AI 工程师可以专注于业务逻辑，平台工程师可以持续优化底层配置，互不干扰。

## 如何上手？

想试试 Agent Sandbox 的话，上手其实很简单。

Agent Sandbox 的安装只需要一条 kubectl 命令：

```bash
# 查询最新版本号
VERSION="$(curl -s 'https://api.github.com/repos/kubernetes-sigs/agent-sandbox/releases/latest' | jq -r '.tag_name')"

# 安装核心组件
kubectl apply -f "https://github.com/kubernetes-sigs/agent-sandbox/releases/download/${VERSION}/manifest.yaml"

# 如果需要扩展功能(模板、预热池等),安装扩展组件
kubectl apply -f "https://github.com/kubernetes-sigs/agent-sandbox/releases/download/${VERSION}/extensions.yaml"
```

安装完成后，用 `kubectl get crd` 检查是否成功，应该能看到 `sandboxes.agents.x-k8s.io` 这个 CRD。

最简单的方式是用 YAML 创建一个 Sandbox：

```yaml
apiVersion: agents.x-k8s.io/v1alpha1
kind: Sandbox
metadata:
  name: my-first-sandbox
spec:
  podTemplate:
    spec:
      containers:
      - name: python-env
        image: python:3.12
```

保存为 `sandbox.yaml`，然后执行：

```bash
kubectl apply -f sandbox.yaml
```

几秒钟后，就有了一个运行 Python 3.12 的沙箱环境。可以用 `kubectl exec` 进入沙箱：

```bash
kubectl exec -it my-first-sandbox -- /bin/bash
```

如果用的是 GKE，可以利用托管的 GKE Sandbox 和 Pod Snapshots：

```bash
# 创建启用了 Sandbox 的节点池
gcloud container node-pools create agent-pool \
  --cluster=my-cluster \
  --sandbox type=gvisor
```

在 Sandbox spec 中指定使用 gVisor 运行时：

```yaml
apiVersion: agents.x-k8s.io/v1alpha1
kind: Sandbox
metadata:
  name: secure-sandbox
spec:
  podTemplate:
    spec:
      runtimeClassName: gvisor  # 使用 gVisor 运行时
      containers:
      - name: python-env
        image: python:3.12
```

需要提醒你的是，Agent Sandbox 目前处于 Alpha 阶段（v1alpha1），还在快速进化中，上述提到的 API 和对应实现都有可能还会继续变化，在使用时需要保持关注。

## 写在最后

AI Agent 正在改变我们构建软件的方式。从被动的“工具”到主动的“智能体”，从确定性的逻辑到非确定性的推理，这些变化对基础设施提出了全新的要求。

Agent Sandbox 是 Kubernetes 社区对这些挑战的回应。用强隔离保证安全，用预热池和快照恢复保证性能，用简洁的 API 降低使用门槛。这些特性的发布其实也标志着 Kubernetes 不仅可以作为容器编排平台，更是一个理想的智能体编排平台。

如果你正在构建 AI Infra，正在解决编排 AI Agent 的难题，Agent Sandbox 值得关注。

---

**参考资料**

- Agent Sandbox 官方文档：<https://agent-sandbox.sigs.k8s.io/>
- GitHub 仓库：<https://github.com/kubernetes-sigs/agent-sandbox>
- Google Cloud 博客：[Introducing Agent Sandbox： Strong guardrails for agentic AI on Kubernetes and GKE](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke)
