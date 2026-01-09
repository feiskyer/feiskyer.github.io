---
title: "开源 AKS MCP：解锁智能 Kubernetes 运维"
date: 2025-08-14T22:20:28+08:00
draft: false
tags: [AI, MCP, Agent, Kubernetes]
---

> 题记：本文根据 AKS 官方博客《Announcing the AKS-MCP Server: Unlock Intelligent Kubernetes Operations》整理，并结合中文表达习惯进行了适当调整。原文作者 Pavneet Ahluwalia。

我们很高兴地宣布推出 AKS MCP。这是一款开源的模型上下文协议（MCP）服务，可通过 Agentic AI 工作流程为您的 Azure Kubernetes Service (AKS) 集群赋予原生 AI 能力，并为开发人员、SRE 及平台工程师提供更便捷的访问方式。

标准化的 MCP 协议 + AKS API 深度集成 = AI Agent 直接操作 K8s 集群。无需截图、无需手写 kubectl 命令，AI 助手现在能够：

- 自动诊断集群健康状态
- 实时分析网络配置问题
- 智能扩缩容和故障排查

这不是又一个 ChatOps 工具，而是让 AI Agent 具备云原生运维的 “第一性” 能力。

![](/images/20251127084858.png)

## 为什么需要 AKS MCP？

AI Agent 企业落地面临的最大难题并非推理或语言能力，也不是提示词的编写（尽管这些仍然重要），而是其所处环境中碎片化且脆弱的上下文。目前，各类组织正面临以下三大挑战。

### 信息孤岛：AI 看不到真实环境

Claude Code 再聪明，kubectl 输出也只能看到表面。真实的集群问题往往藏在：

- Azure Portal 的 5 个不同仪表板里；
- Istio、ArgoCD 等工具的独立状态中；
- 分散在各个系统的审计日志中。

你不想每次都截图粘贴一堆面板给 AI 分析。

### 集成地狱：连接器越写越多

每加一个新工具 = 一套新的自定义集成。K8s 尤其如此，开源开放的生态使其具备极其庞大的扩展和插件系统，每种插件、每种扩展、甚至是同一个插件在不同环境下的实现方式都不同。AI Agent 无法意识到这些区别，所以都需要工具连接给 AI Agent 赋能。

难道每个 AI Agent 都要重复造轮子？

### 权限混乱：安全与便利性的死结

GitHub Copilot 能告诉你 Azure API 怎么调用，但它不知道：

- 你的订阅 ID 是什么；
- 资源组叫什么名字  ；
- RBAC 策略允许哪些操作；

每次都要手动提供一堆上下文，AI 才能真正干活。

![](/images/20251127085008.png)

![](/images/20251127085032.png)

## 技术设计：MCP 解决方案

问题的本质是缺乏标准化的 “上下文工程”。[模型上下文协议（MCP）](https://modelcontextprotocol.io/overview) 正好解决这个问题。

AKS MCP 的四大设计原则：

### 1. 开源社区驱动

MIT 许可证，完全开源。云原生生态系统需要透明的工具链，不需要又一个黑盒 SaaS。

### 2. AI Agent 原生支持

专为主流 AI 工具设计：Claude、Cursor、GitHub Copilot 开箱即用。你继续用熟悉的 AI 助手，AKS MCP 在后台提供 AKS 和 Kubernetes 能力。

![](/images/20251127085125.png)

### 3. 快速迭代 > 完美设计

AI Agent 技术变化太快，MCP 协议也在不断演进（例如从 SSE 演变为 HTTP 流式传输）。

这凸显了我们需要快速响应，并信任用户能够理解不断变化的生态系统。因此，我们首先在 GitHub 上发布了二进制文件和 Docker 镜像，方便用户在本地或集群环境中运行，充分发挥其优势。同时，社区也在共同努力，推动安全的远程 MCP 服务。

### 4. 默认只读，显式授权

AI 的不确定性带来了风险。AKS MCP 默认设置为只读模式，用户需主动开启写权限。

对于部署 Pod、删除资源等操作，必须由用户明确授权。

## 核心架构与能力

AKS-MCP Server 作为 AI Agent 与 AKS 集群间的标准化桥梁，具备三大核心能力：

**1. 零配置身份验证**

- 复用 `az login` 认证状态；
- 强制 Azure RBAC 权限检查；
- 三级权限控制：readonly/readwrite/admin。

**2. 深度诊断工具集**

- Kubernetes API 全覆盖；
- Azure 监控数据集成；
- [Inspektor Gadget](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/logs/capture-system-insights-from-aks?tabs=azurelinux30) 系统级诊断；
- 活动日志 + 审计日志分析。

**3. 社区驱动扩展**
完全开源，针对新工具快速适配。Istio、ArgoCD、Prometheus 等工具的支持正在路上。

![](/images/images20251127085207.png)

完整的工具和功能列表请查看 [AKS MCP 工具列表](https://github.com/Azure/aks-mcp#available-tools)。

## 安全模型：零信任架构

AKS-MCP 采用 Azure 标准身份验证 + 多级权限控制：

### 身份验证链路

AKS-MCP 服务器以安全性为核心设计，依赖 Azure SDK 的 DefaultAzureCredential 链（通过 azidentity 库）实现业界标准的 Azure 身份验证机制。该链会依次检查环境变量、托管身份、Azure CLI 登录以及基于浏览器的凭据。因此，AKS MCP 服务器无需直接管理用户凭据，用户只需提前通过 Azure CLI（az login）完成身份验证，服务器即可复用该身份上下文，为每次调用 Azure API 获取所需的安全 OAuth 令牌。

### 权限分级控制

为进一步提升操作安全性，AKS-MCP 实施了三层访问控制体系：只读、读写和管理员，并内置安全验证器，在执行命令前对权限级别进行检查。该机制为自动化和交互式场景提供了安全、无缝的访问体验，确保仅授权操作可被执行，并依托于 Azure 现有的可信身份认证模式。

## 5 分钟上手指南

### 方法一：VS Code 一键安装（推荐）

```bash
# 前提：已登录 Azure CLI
az login
```

安装步骤：

1. VS Code 安装 AKS 扩展
2. `Ctrl+Shift+P` → **AKS: Setup AKS MCP Server**
3. `Ctrl+Shift+P` → **MCP: List Servers** 确认运行状态
4. 开始和 GitHub Copilot 对话：*"检查集群健康状况"*

扩展自动完成二进制下载、MCP 配置、权限设置。

![](/images/20251127085253.png)

### 方法二：手动配置

**1. 下载二进制**

```bash
# Linux/macOS
curl -sSL https://github.com/Azure/aks-mcp/releases/latest/download/aks-mcp-linux-amd64 -o aks-mcp
chmod +x aks-mcp

# Windows PowerShell
Invoke-WebRequest -Uri "https://github.com/Azure/aks-mcp/releases/latest/download/aks-mcp-windows-amd64.exe" -OutFile "aks-mcp.exe"
```

**2. 配置 MCP 服务器**
创建 `.vscode/mcp.json`：

```json
{
  "servers": {
    "aks-mcp": {
      "type": "stdio",
      "command": "/path/to/aks-mcp",
      "args": ["--access-level", "readonly"]
    }
  }
}
```

## 实战场景：AI 运维工作流

AKS MCP 实现了智能化、代理驱动的云运维。以下是在 GitHub Copilot、Claude Code 或其他兼容 MCP 的代理中可尝试的实际操作场景：

### 诊断资源健康

提示词示例：“为什么我的某个 AKS 节点处于 NotReady 状态？”

### 分析网络安全

提示词示例：“你能帮我查看 AKS 集群的 VNet 和 NSG 配置吗？我怀疑 DNS 流量被阻止了。”

### 自动扩缩容

提示词示例：“将我的 payments-api 部署扩展到 5 个副本，并确认部署状态”。

### 完整演示：GitHub Copilot + AKS MCP

**用户提示词**: "How is the health of my cluster?"

![](/images/20251127085324.png)

![](/images/20251127085342.png)

**用户提示词**: "diagnose the outbound connectivity failure"

![](/images/20251127085404.png)

如您所见，GitHub Copilot 能够使用 AKS MCP 服务，并调用多种工具与 Azure 和 Kubernetes API 交互，从而识别问题、分析原因并提供解决方案。

## 下一步

欢迎访问 GitHub 仓库：<https://github.com/Azure/aks-mcp>。我们期待您的反馈、贡献和创新建议。

让我们携手迈向云原生 DevOps 的新阶段——在这里，Kubernetes、AI 和开放协议为每一位开发者赋能。

项目地址：[https://github.com/Azure/aks-mcp](https://github.com/Azure/aks-mcp)

官方博客原文：<http://blog.aks.azure.com/2025/08/06/aks-mcp-server>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
