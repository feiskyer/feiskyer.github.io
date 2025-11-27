---
title: "AKS发布首个K8S AI Agent，Kubernetes运维进入智能时代"
date: 2025-08-22T22:20:28+08:00
draft: false
tags: [AI, Vibe Coding, MCP, 大模型, Kubernetes]
---

> **题记**：本文将带你一起了解 AKS 团队最近在 AI Agent 方面的新产品，即由 Agentic AI 驱动的智能运维和诊断命令行工具——AKS CLI Agent，专门用来解决 K8s 运维中那些让人头疼的问题。

在本月初的 KubeCon India 上，AKS 团队在 Kubernetes 社区发布了最新的智能 AI 驱动产品—— AKS  CLI Agent。AKS CLI Agent 是一个全新的 Agentic AI 命令行工具，可以帮助 Azure Kubernetes Service (AKS) 用户以更便捷性和更智能的方式对集群进行故障诊断、优化和运维。

AKS  CLI Agent 基于开源的 [HolmesGPT](https://github.com/robusta-dev/holmesgpt) Agent（已提交 CNCF）和[AKS MCP（模型上下文协议）服务](https://github.com/Azure/aks-mcp)构建，将安全、可扩展和智能的 Agentic 工作流程直接带到你的终端。

在过去几个月里，我们专注于解决大多数 Kubernetes 用户最关心的问题：排查和诊断 Kubernetes 环境中的故障。目前，我们正为少数用户提供早期体验机会，以便深入合作并收集反馈。如果您有兴趣参与，请填写我们的[报名表](https://aka.ms/aks/cli-agent/signup)。

![cli-agent-vision](/images/cli-agent-vision.png)

## 我们为什么要构建 AKS  CLI Agent

AKS 团队的目标很简单：让开发者、SRE、DevOps 和平台工程师在 AKS 上能完成更多事情。AI 绝对是我们这代人见过最牛的生产力工具，关键是怎么把它用好、用安全。我们就想把这些 AI 能力直接交到用户手里，专门解决那些让人头疼的问题——集群故障排查、成本优化、还有那些配置和决策选择困难。

摆在我们面前有个选择题：是做一个啥都能干的万能工具，还是先把一个场景做到极致？我们最后决定从故障排查入手，因为这是大家最头疼也最常见的问题，AI 在这方面确实有两把刷子（说实话，我们内部最开始就叫它"AKS AI 故障排除神"）。目前主要搞定 4 类问题：网络/DNS、Pod 调度、节点健康、还有集群各种 CRUD 操作的坑。当然了，我们也在同步搭建通用的 K8s 和 AKS 基础能力，毕竟 AI 在日常运维中到处都用得上。别担心，我们肯定会覆盖大部分 AKS 的使用场景，所以您的反馈对我们来说就是金子般宝贵。

K8s 故障排查有多难？用一个词形容就是：要命。不管是刚起步的云原生公司还是大厂，大家都被同样的问题折磨着。你说这些监控数据吧，到处都是，指标、日志、链路追踪散落在各个工具里，想关联起来分析更是难上加难。更要命的是，没有 K8s 和 Azure 等云平台的深度经验，看这些数据就像看天书一样难以理解。平时查个故障，得在好几个工具之间来回切换，手忙脚乱一通操作下来，MTTR（平均故障恢复时间）高得吓人，工单也是蹭蹭往上涨。现有的工具确实能给你展示原始数据，但就是不告诉你这些数据到底啥意思、该怎么处理，这就是为什么我们觉得 AI Agent 来得正是时候。

AKS CLI Agent 就是来解决这些破事儿的，让大家少熬夜、少掉头发，哪怕是 K8s 新手也能淡定地搞定 AKS 集群的各种疑难杂症。

![target-customer-pain-points](/images/target-customer-pain-points.png)
![target-customer-benefits](/images/cli-agent-benefits.png)

## 基于开源构建：HolmesGPT + AKS-MCP

还有一个让我们纠结的问题：是自己闷头搞一套私有的，还是跟开源社区一起玩？其实这个选择题不难，毕竟“拥抱开源”一直是 AKS 的核心理念，所以我们毫不犹豫地选择了后者。

**Agent 框架 - HolmesGPT**：HolmesGPT 就是个开源的 AI 诊断神器，专门负责找问题根源、跑诊断脚本，还能把复杂的技术问题用人话给你解释清楚。选框架这事我们也是做足了功课，把市面上几个主流的开源方案都研究了个遍，甚至自己撸了几个内部原型来对比。最后选择跟 Robusta.dev 团队合作搞 HolmesGPT，主要是因为：

- 架构设计很灵活，天生就支持各种工具插件、MCP 服务器和自定义运维手册；
- 专门为 K8s 环境优化过的智能提示，该有的都有了；
- 开源社区很活跃，大家都愿意一起搞事情。

现在微软 AKS 团队已经是 HolmesGPT 的共同维护者了，Robusta 也把项目捐给了 CNCF 作为沙盒项目。欢迎大家来 [HolmesGPT](https://github.com/robusta-dev/holmesgpt) 一起玩！

**工具和能力 - AKS-MCP 服务器*：AKS-MCP 服务就像是 AI agent 和 AKS 集群之间的安全翻译官，负责把 K8s 和 Azure 的各种 API、监控数据、诊断工具包装成 AI 能理解的标准接口。现在你就可以把 AKS-MCP（或者其他 MCP 服务器）跟 HolmesGPT 组合使用（具体怎么用看[这里](https://docs.robusta.dev/master/configuration/holmesgpt/remote_mcp_servers.html)），随着我们给 [AKS-MCP 项目](https://github.com/Azure/aks-mcp)加更多功能和最佳实践，集成体验会越来越丝滑。

这些组件搭在一起就是个 **乐高积木架构**，你想用什么 AI 提供商、监控工具、集群配置都随你，数据和执行权限完全掌握在自己手里。

![cli-agent-lego-blocks](/images/cli-agent-lego-blocks.png)

## 安全设计：为什么我们从 CLI 体验开始

说实话，我们最终的目标是搞个 **完全自主的 AI 自愈系统**（给 AKS 提供真正的“SRE 即服务”），但第一步我们还是保守点比较好。

生产环境一出事儿，那代价可就大了。要是让 AI 完全自己做主，万一它理解错了监控数据或者基于不完整信息瞎操作，直接把系统搞崩了怎么办？最近业界那些翻车事故已经告诉我们了：**没人兜底的自动化就是在玩火**。

这就是为什么我们选择从 **人在回路的 CLI 体验** 开始。

AKS CLI Agent 的定位很明确：**帮你干活** 而不是抢你饭碗。AI agent 负责分析问题、跑诊断脚本、给建议，但最终拍板还得是你自己。这样的好处是：

- **透明性**：AI 跑了什么工具、分析了哪些数据，你都看得清清楚楚；
- **控制权**：没经过你同意，绝对不会对集群动手动脚；
- **可信度**：AI 的建议都是基于真实数据，有理有据不忽悠。

这样的模式让我们能摸清 AI 的脾气，收集大家的使用体验，一步步优化，为以后真正的自动化运维打下坚实基础。

安全和隐私是智能 CLI 体验的核心：

- **本地运行**：所有诊断和数据采集都在你自己机器上运行，数据压根不会跑到外面去；
- **Azure CLI 认证**：直接用你现有的 Azure 身份和权限，该访问啥就访问啥，绝不越界；
- **自带 AI**：你想用 OpenAI、Azure OpenAI、Anthropic 随便哪家都行，微软不碰你的任何数据。甚至可以用你们公司批准的私有 LLM，包括部署在自己订阅和 VPC 里的 Azure OpenAI。

![cli-agent-demo](/images/cli-agent-demo.gif)

## 🔌 可扩展和可定制

Agentic CLI 就是为了适配你的各种环境：

- **自定义工具集**：想接入 Prometheus、Datadog、Dynatrace 或者自家的监控平台？分分钟搞定。
- **Runbook 插件**：可以加载你自己的故障排查套路，也能用社区大神们贡献的各种玩法。
- **MCP 服务器支持**：接入 AKS-MCP 或其他 MCP 服务器，解锁更多高级诊断能力，包括 AppLens 检测器、Azure Monitor 还有调试 Pod 部署等等。

## 如何使用

填完 [报名申请表](https://aka.ms/aks/cli-agent/signup) 后，我们会分批通知大家，到时候会给你 CLI 安装教程、文档和下一步操作步骤指南。

拿到访问权限后，你可以用下面这个命令看看 AKS CLI Agent 都有什么功能：

```bash
az aks agent --help
// 或者 $ az aks agent "how is my cluster [Cluster-name] in resource group [Resource-group-name]".
```

以下是几个 AKS  CLI Agent 的更多示例：

### 🧠 节点 NotReady

诊断 kubelet 崩溃、CNI 故障和资源压力：

```bash
az aks agent "why is one of my nodes in NotReady state?"
```

### 🌐 DNS 故障

识别 CoreDNS 问题、NSG 错误配置和上游 DNS 问题：

```bash
az aks agent "why are my pods failing DNS lookups?"
```

### 🕵️ Pod 调度失败

检测资源约束、亲和性不匹配和区域限制：

```bash
az aks agent "why is my pod stuck in Pending state?"
```

### 🔄 升级失败

精确定位 PDB 违规、配额问题和 IP 耗尽：

```bash
az aks agent "my AKS cluster is in a failed state, what happened?"
```

### 一般 CloudOps 和优化

```bash
az aks agent "how can I optimize the cost of my cluster?"
```

每个场景都由 AI 驱动的推理、工具执行和可操作建议支持，帮助弥合原始遥测数据与实际洞察之间的差距。

## 🌐 愿景：全渠道 AKS 智能体

AKS 的 CLI Agent 只是一个起点。我们希望能够在客户常用的平台上为其提供服务，因为我们了解到每位用户都有不同的工具偏好——有些人喜欢命令行界面，有些人使用 AKS 的 VS Code 扩展，还有一些人选择 Azure Copilot。因此，我们的长期愿景是与用户的所有工具平台进行集成，让他们无论身处何地，都能获得一致且全面的体验。接下来，我们将重点关注以下几个领域：

- **Azure 门户**：通过 Copilot 和诊断与解决集成智能能力，如诊断和操作等。
- **Visual Studio Code**：通过 AKS VS Code 扩展和 MCP 集成实现一键故障排除。

这种全渠道策略确保每位 AKS 用户——无论是开发者、运维人员还是 SRE——都能在其工作环境中便捷访问智能故障排除功能。

## 📣 加入预览

我们正在积极收集反馈，并在 AKS CLI Agent 正式发布前，通过有限预览不断进行优化。欢迎通过 GitHub 问题或我们的[反馈表单](https://aka.ms/aks/cli-agent/feedback)分享你对 CLI Agent 或 AKS-MCP 的使用体验。更多信息请访问：aka.ms/cli-agent/signup。

## 💬 结语

AKS CLI Agent 在提升 Kubernetes 操作的易用性、智能化和安全性方面迈出了重要一步。通过结合开源创新与 Azure 原生集成，我们帮助每一位 AKS 用户更高效地排查故障、减少停机时间，让大家能够专注于最重要的事情——构建出色的应用程序。

敬请关注我们的后续更新。我们将不断扩展功能，集成托管体验，并将 AI 驱动的故障排除能力带到 AKS 生态系统的每一个角落！

> 产品体验报名链接：https://aka.ms/aks/cli-agent/signup
>
> 官方博客链接： https://blog.aks.azure.com/2025/08/15/cli-agent-for-aks
>
> 原作者：Pavneet Ahluwalia, Julia Yin, Aritra Ghosh（均为 AKS 产品 PM）

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
