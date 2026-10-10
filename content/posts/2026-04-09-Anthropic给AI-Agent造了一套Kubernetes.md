---
title: "Managed Agents 架构拆解：Anthropic 给 Agent 造了一套 K8s"
date: 2026-04-09T10:00:00+08:00
draft: false
tags: [AI Agent, Anthropic, Managed Agents, 架构设计, Kubernetes]
description: "深度解读 Anthropic Managed Agents 架构：把 session、harness、sandbox 三个组件虚拟化成接口，像 Kubernetes 抽象 Pod、Volume、Service 一样实现脑手分离、状态持久化与安全隔离。"
---

> 题记：本文编译自 Anthropic 工程博客《[Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)》，由 Lance Martin、Gabe Cemaj 和 Michael Cohen 撰写。

Kubernetes 早就是 AI 基础设施的事实标准了。不管是大模型训练还是推理服务，最后都跑在 K8s 上。AI Agent 也不例外，Harness、sandbox、工具调用这些组件，基本都可以容器化部署。

但跑过长时间 Agent 任务的人应该都碰过这种事：Agent 跑着跑着容器挂了，session 没了，只能从头来。session 卡死了想调试，Harness、sandbox、session 全在一个容器里，根本分不清问题出在哪。好不容易跑起来了，上下文窗口又满了，压缩还是丢弃，怎么选都可能踩坑。

做过 K8s 的人看这些问题应该很眼熟。十年前容器编排领域碰到的也是同一类：组件耦合、状态丢失、扩展困难。K8s 的解法是把硬件虚拟化成抽象层，Pod、Service、PersistentVolume 这些概念比底层硬件活得久得多。你换磁盘、换机器，上层应用完全不用管。

Anthropic 昨天开放公测的 Managed Agents，本质上在做同样的事，只不过虚拟化的对象从硬件换成了 Agent 的组件。

Anthropic 的工程博客一直在聊怎么给 Agent 搭 Harness：从[构建有效 Agent](https://www.anthropic.com/engineering/building-effective-agents) 到[长时间任务的 Harness 设计](https://www.anthropic.com/engineering/harness-design-long-running-apps)，再到[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。这些文章贯穿着一条线索：Harness 编码的是对 Claude 当前能力边界的假设，但模型在进步，假设会过期。

举个例子。之前在 Sonnet 4.5 上，他们发现模型会随着上下文窗口接近极限而提前收工（也称为上下文焦虑）。于是 Harness 里加了上下文重置机制。结果换到 Opus 4.5 上一跑，行为消失了。重置机制变成了死代码。

Harness 免不了一直改下去。所以 Anthropic 造了 Managed Agents：用一组尽可能通用的接口来运行长时间 Agent，让这些接口比任何一套具体的 Harness 实现活得更久。

![Managed Agents 架构概览](/images/2026-04-09-AnthropicAI-AgentKubernetes-image.jpg)

它把 Agent 的核心组件虚拟化成了三个接口：session（发生了什么的完整事件日志）、harness（调用 Claude 和路由工具调用的循环）、sandbox（Claude 跑代码和编辑文件的执行环境）。每个组件可以独立替换，互不干扰。跟 K8s 对 Pod、Volume、Service 的抽象思路一致。

## 别养宠物

做过 K8s 的你对 Pets vs Cattle 这个比喻肯定不陌生。Pet 是你精心照料的单台服务器，挂了就得抢救；Cattle 是随时可以杀掉重建的无状态实例。云原生的核心理念之一就是把所有东西变成 Cattle。

Managed Agents 一开始没做到这一点。

最初的设计是把所有 Agent 组件塞进一个容器。好处是文件操作就是本地 syscall，不需要设计服务边界。但这就养了一只宠物。容器挂了，session 就没了。容器卡住了，得想办法把它救活。

救活容器意味着调试卡死的 session。唯一的观察窗口是 WebSocket 事件流，但它分不清故障发生在哪个环节。Harness 的 bug、事件流的丢包、容器下线，在外面看起来症状完全一样。要搞清楚怎么回事，工程师得开 shell 进到容器里，但容器里还有用户数据，这条路基本走不通。

还有一个更深的问题。Harness 默认 Claude 的工作内容就在同一个容器里。当客户说“我想让 Claude 连我自己的 VPC”时，要么做网络对等互联，要么让客户在自己的环境里跑 Anthropic 的 Harness。一个 Harness 里硬编码的假设，变成了基础设施层面的约束。

这跟早年单体应用跑在物理机上的困境太像了。

## 把大脑从手上拆下来

解法是把大脑（Claude 和 Harness）从手（sandbox 和工具）和记忆（session 日志）上拆开。每个组件变成一个接口，对其他组件的假设尽可能少，独立故障、独立替换。

K8s 里 Pod 是无状态的计算单元，PersistentVolume 是持久化存储，两者通过声明式绑定关联但互不依赖。Pod 挂了重建一个，数据还在。Managed Agents 的拆法思路一样。

Harness 不再住在容器里。它像调用其他工具一样调用容器：`execute(name, input) → string`。容器变成了 Cattle，挂了就挂了，Harness 把失败当作工具调用错误传回给 Claude，Claude 决定要不要重试。重试的话，`provision({resources})` 拉一个新的就行。

不用再抢救挂掉的容器了。

Harness 自己也是 Cattle。session 日志在外部，Harness 里没有任何需要在崩溃中存活的状态。挂了？`wake(sessionId)` 启动一个新的，`getSession(id)` 拿回事件日志，从最后一个事件继续。运行过程中用 `emitEvent(id, event)` 往 session 写入持久化记录。

![脑手分离架构](/images/2026-04-09-AnthropicAI-AgentKubernetes-image2222.jpg)

这里面还有一个安全维度值得单独说。

之前所有东西耦合在一个容器里的时候，Claude 生成的不可信代码和凭证跑在同一个环境中。一次成功的 prompt injection 只需要说服 Claude 读一下自己的环境变量。拿到 token 之后，攻击者可以开新 session 干什么都行。

收窄 token 权限？当然可以。但这本身又是一个假设：Claude 拿着受限 token 干不了什么。模型在变强，这个假设随时可能失效。

结构性的解法是让 token 在 sandbox 里根本不可达。Git 仓库的做法是在 sandbox 初始化时用 token 克隆仓库并写入本地 git remote，之后 `push` 和 `pull` 都走本地配置，Agent 从头到尾碰不到 token。自定义工具走 MCP，OAuth token 存在安全保险箱里，Claude 通过专用代理调用 MCP 工具，代理根据 session 拿到对应的凭证再调外部服务。整个链路里，Harness 不接触任何凭证。

Anthropic 这个思路挺值得参考的：不是所有安全问题都要靠权限收窄来解决，有时候换个架构就能把问题消除掉。

## Session 不是上下文窗口

脑手分离解决了组件耦合的问题，但 Agent 跑久了还有另一个挑战：上下文管理。

长时间任务经常超出 Claude 的上下文窗口。常见的应对方式都涉及不可逆的决策：compaction 把上下文压缩成摘要，memory 工具把信息写到文件，context trimming 选择性地删掉旧的工具结果或 thinking block。这些方法都能用，但有个共同的软肋，就是你很难预判未来哪些 token 会被用到。删错了就回不来了。

之前有[研究](https://arxiv.org/pdf/2512.24601)探索过一个思路：把上下文存成一个对象放在 REPL 里，模型通过写代码来过滤和切片，而不是被动接受压缩后的结果。

Managed Agents 的 session 做了类似的事，但把上下文存在了 sandbox 外面。session 日志是持久化的，通过 `getEvents()` 接口让大脑按位置切片查询事件流。可以从上次读到的地方继续往下读，也可以倒回某个时刻前几个事件看看当时的背景，或者在执行某个操作前重新读一遍相关上下文。

![Session 作为外部上下文对象](/images/2026-04-09-AnthropicAI-AgentKubernetes-session-context.jpg)

拿到的事件在传给 Claude 之前还可以在 Harness 里做各种变换：重组结构以提高 prompt cache 命中率，或者做其他上下文工程。这里的设计考量是把“可恢复的上下文存储”和“任意的上下文管理”分成两个关注点。前者放在 session 里保证持久和可查询，后者放在 Harness 里，怎么折腾都行。因为未来的模型需要什么样的上下文工程，现在谁也说不准，但 session 的持久性是确定需要的。

用 K8s 类比的话，session 就是 PersistentVolume：数据在那里，不管哪个 Pod 来挂载都能用。上下文工程是 Pod 里的应用逻辑，随着业务需求随时可以换。

## 多脑多手

组件拆开之后，扩展变得自然了。

先说多脑。之前大脑和手都在一个容器里，每启动一个 session 就要起一个容器。不管这次 Claude 用不用 sandbox，容器都得先跑起来：克隆仓库、启动进程、拉取待处理事件。这些全卡在 TTFT（Time to First Token）上，用户最敏感的延迟指标。

拆开之后，容器只在需要时才通过工具调用启动。不需要 sandbox 的 session 直接跳过容器初始化，推理在编排层拉到 session 事件后就开始。

p50 TTFT 下降约 60% ，p95 下降超过 90% 。

这个优化思路在 K8s 社区一点都不陌生。这些年围绕 Pod 冷启动的优化从没停过：镜像预拉取、lazy snapshot、WASM 轻量运行时。核心逻辑都是一样的，不需要的东西别提前准备。

再说多手。之前一个大脑只能操作一个容器，容器挂了就全完了。现在每只手就是一个工具调用：`execute(name, input) → string`，名字和输入进去，字符串出来。这个接口能接任何自定义工具、任何 MCP 服务器、Anthropic 自己的内置工具。Harness 不知道也不关心 sandbox 到底是一个容器、一部手机，还是一个宝可梦模拟器。

![多手架构](/images/2026-04-09-AnthropicAI-AgentKubernetes-image23433.jpg)

因为手不绑定任何特定的脑，多个 Agent 之间可以互相传递工具。产品公告里提到 Managed Agents 已经在研究预览中支持多 Agent 协调，一个 Agent 可以生成和指挥其他 Agent。多脑多手的架构落地之后，这种能力是水到渠成的。

Anthropic 内测的数据也挺有意思。在结构化文件生成这类任务上，比如根据 API schema 自动生成 SDK 代码和文档，相比标准的 prompting 循环，任务成功率最高提升了 10 个百分点，难题上增益最大。加上 Console 里内置的执行追踪和分析工具，每个工具调用、每次决策、每个失败点都能看到，对于把 Agent 推上生产环境的团队来说实用性不错。

## 写在最后

读完这篇工程博客，我脑子里一直跑着一个想法：这就是 Agent 领域的 Kubernetes。

K8s 当年解决的也是同一类问题。应用越来越复杂，单机跑不动了，需要一个编排层来管理容器的生命周期、网络和存储。K8s 没有规定你的应用该怎么写，它定义了一组接口，让任何应用都能跑在上面。十年过去了，底层的容器运行时从 Docker 换到了 containerd，节点从 CPU 服务器换到了 GPU 集群，但 Pod 的定义还是那个 Pod。

Managed Agents 在做同样的事。它不规定 Harness 怎么写，而是把 Agent 的核心组件虚拟化成接口。Claude Code 是一个很好的 Harness，任务专用的 Agent Harness 在特定领域可能表现更好，Managed Agents 都能承载。接口固定，实现自由替换。

不过有一个差异。K8s 是开源的，CNCF 社区驱动，任何云厂商都能跑。Managed Agents 是 Anthropic 的托管服务，目前只服务 Claude 生态，或许这也是为什么他们会不停封禁诸如 OpenClaw 这样的第三方平台。当然，这篇博客公开了设计理念和接口抽象的思路，即使不用 Managed Agents，这套脑手分离的架构模式也能自己实现。

AI Agent 的基础设施层还在快速成型。Anthropic 在做 Managed Agents，OpenAI 有 Codex 的云端 Agent，Google 有 Vertex AI Agent Engine，最终谁成为 Agent 编排的事实标准还不好说。但有一点是确定的：Agent 的组件解耦、状态持久化、安全隔离这些需求不会消失，只会随着 Agent 能力的增长变得更重要。

---

相关资源：

- 原文链接：<https://www.anthropic.com/engineering/managed-agents>
- 产品公告：<https://claude.com/blog/claude-managed-agents>
- Managed Agents 文档：<https://platform.claude.com/docs/en/managed-agents/overview>
- 构建有效 Agent：<https://www.anthropic.com/engineering/building-effective-agents>
- 长时间 Agent Harness 设计：<https://www.anthropic.com/engineering/harness-design-long-running-apps>
- 上下文工程：<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
