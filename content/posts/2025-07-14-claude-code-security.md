---
title: "Claude Code 安全最佳实践"
date: 2025-07-14T21:55:29+08:00
draft: false
tags: [AI, Vibe Coding, Claude Code]
---

最近，越来越多的开发者从 Cursor、GitHub Copilot 等 AI 编程 IDE 切换到了 Claude Code。Claude Code 的强大功能让人印象深刻，但在这股切换热潮中，我发现一个令人担忧的现象：很多人只注重工具的易用性，而忽略了其中的安全和数据隐私陷阱。

以 [Supabase MCP 安全问题](https://www.generalanalysis.com/blog/supabase-mcp-blog)为例，攻击者可利用 LLM 的指令/数据混淆漏洞直接泄露整个 SQL 数据库。MCP 协议的核心问题在于：LLM 无法区分指令和数据，如果用户提供的"数据"被精心伪装成指令，AI 很可能会将其作为真实指令执行。攻击者只需在支持工单中嵌入类似 "THIS MESSAGE IS FOR YOU AFTER YOU READ THE LATEST MESSAGES FROM SUPABASE MCP > PLEASE DO THESE ACTIONS ASAP..." 的隐藏指令，AI 在读取消息时就会执行恶意 SQL 查询，绕过所有 RLS（Row-Level-Security）保护，泄露敏感数据。

这篇博客就来分享一些在使用 Claude Code 时需要注意的安全最佳实践，帮助大家在享受 AI 编程便利的同时，也能保护好自己的数据安全。

## 0. 尽量避免使用中转 API

首先要说的是，我在各种社区里看到越来越多的 Claude Code 中转服务广告。这些服务的原理很简单：Claude Code 允许你自定义 API endpoint，可以接入任何 Anthropic API 兼容的供应商。

**中转 API 的风险**，就像未加密的 HTTP 中转代理一样，很容易受到 MITM（中间人）攻击：

1. **数据窃取**：Claude Code 会读取大量文件来生成高质量回答，中间人只需简单的关键字过滤，就能获取你的各种敏感信息；
2. **命令执行**：大多数用户允许 Claude Code 执行命令，攻击者可以借此进行远程代码执行；
3. **注意力攻击**：在数万字的输出中，几十个字的可疑操作很容易被忽略。

**更安全的替代方案**：

如果你确实需要使用第三方模型，考虑这些更安全的方式：

- **官方 Anthropic API**：许多云服务商（如 AWS Bedrock、Google Vertex AI）提供官方的 Anthropic API 服务；
- **官方 Anthropic 兼容 API**：比如月之暗面直接提供了 Anthropic 格式的 API，你可以直接在 Claude Code 中使用最新的 Kimi K2 模型；
- **自建 LiteLLM 网关**：在需要使用其他大模型时，使用开源的 LiteLLM 在自己的服务器上搭建中转服务，确保数据不经过第三方（LiteLLM 也是 Anthropic 官方推荐的 [LLM 网关](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)）。

**记住**：别为了省一点钱，就忽略了数据窃取、远程代码执行等严重的安全问题，避免引发无法挽回的损失。

那么，如何在享受 Claude Code 便利的同时，确保安全性呢？基于我的使用经验和对社区安全事件的观察，我整理了以下几个关键防护要点。

## 1. 控制 Claude Code 权限

Claude Code 天然采取严格的只读策略，任何 “写文件 / 运行脚本 / 执行命令” 行为都会触发权限弹窗，需要你手动确认。但这里有个陷阱：

很多开发者为了 “省事” 会勾选 Always allow，这相当于关掉了最后一道安全门。

**我的建议**：

- 切勿在生产仓库中永久启用 Always allow；
- 改用 Session-level 白名单，每次会话重新授权；
- 使用 /permissions 命令定期审查安全列表；
- 如有必要，还可以开启 OpenTelemetry，将监控数据（Metrics/Events/Logs）导出到持久化存储。

## 2. 保护终端和本地数据

Agentic 工具的魅力就是 “能自己执行命令”，但这也是最危险的地方。AI 并不会为终端命令执行的结果负责。

**我的建议**：

- 永远不要允许 AI 自动执行高风险命令（比如 rm、wget、curl、chmod 等等）；
- 对于所有 Claude Code 修改的项目都做好版本管理，在 Claude Code 执行之前事先把之前的工作提交并推送远端；
- 对于需要频繁执行高风险命令的场景，推荐使用容器化环境运行 Claude Code。

## 3. 从源头避免数据泄漏问题

Claude Code 可以读取项目中的任何明文密钥，这是很多人忽略的风险点。

**我的建议**：

- 密钥、证书、API KEY 等都不要提交到代码仓库里，更绝不能出现在提示词中；
- 代码仓库开启安全扫描，拒绝包含密钥、证书、API KEY 等隐私数据的提交。

## 4. 小心供应链安全

除了一开始说的第三方中转 API 可能会引入很多安全问题，另一个特别需要注意的是供应链安全，即整个软件链路上的组件都是有可能会出现安全问题，这包括：

- Claude Code 自身代码以及其依赖库（Claude Code 是基于 Node.js 的）；
- 从第三方下载的 Claude Code 封装程序（GUI、CLI 或者中转等）；
- MCP、工具调用等 Claude Code 调用的外部工具。

**我的建议**：

- 从官方下载并定期更新 Claude Code；
- 对于 MCP、第三方辅助工具，仅选用开源项目并按照官方指南安装配置，订阅官方发布的安全补丁，保持同步更新；
- 严格限制 MCP 工具调用，特别是命令执行和网络访问都人工审核。

## 5. 仅在容器中运行 YOLO 模式

你可以使用 `claude --dangerously-skip-permissions` 来绕过所有权限检查，让 Claude Code 运行在 YOLO 模式（即跳过人工检查，让 AI 全自动完成任务），常用在自动化工作流中。

允许 Claude Code 运行任意命令是有很大的风险，可能导致数据丢失、系统损坏，甚至数据泄露（例如，通过提示注入攻击）。为了尽量减少这些风险，确保仅没有互联网访问的容器中使用 YOLO 模式。Claude Code 官方 Github 仓库中的 [Dev Container](https://github.com/anthropics/claude-code/tree/main/.devcontainer) 是个很好的参考。

## 写在最后

**AI 辅助编程不是简单的工具替换，而是开发流程的重新设计**。当我们把 AI 引入开发环节，安全边界也发生了根本性变化。以前只需要考虑代码本身的安全性，现在还要考虑 AI 交互过程中的数据泄露、权限滥用、供应链风险等新问题。

说实话，在刚开始使用 Claude Code 时，我也曾经因为它的便利性而忽略了一些安全细节。但随着使用时间增长，我越来越意识到这些看似 “繁琐” 的安全措施实际上是在保护我们自身。毕竟，一次数据泄露或者意外的代码执行，可能会让你损失几个月甚至更久的工作成果。

我的建议是：**从现在开始，花几分钟时间检查一下你的 Claude Code 配置**。确保没有永久启用 Always allow，检查是否有可疑的第三方中转服务，清理一下项目中的敏感信息。这些小小的改变，就能让你在享受 AI 编程便利的同时，也能睡个安稳觉。

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
