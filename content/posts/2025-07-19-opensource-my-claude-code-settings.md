---
title: "开源我的 Claude Code 配置：Vibe Coding 的终极工作流"
date: 2025-07-19T10:22:28+08:00
draft: false
tags: [AI, Vibe Coding, Claude Code]
---

经过数月的实践和调优，我将自己的 Claude Code 配置开源。这套配置不仅包含了常用的 Claude Code 配置和自定义命令，还参考 Kiro，引入了 **Vibe Coding** 流程，支持规范驱动的开发流程。

所有配置和自定义命令开源在 Github 上，项目地址为：<https://github.com/feiskyer/claude-code-settings>。

想要了解学习 Claude Code 使用和实践技巧的话，请参考我之前的文章。

## 项目简介

Claude Code Settings包含一套精心整理的Claude Code配置和自定义命令集合，用于提升开发工作流程，包括用于功能开发（Kiro工作流）、代码分析、GitHub集成和知识管理的专用命令。

## 核心特性

### 规范驱动开发流程

借鉴 [Kiro](https://kiro.dev/)，从需求分析到代码实现的完整开发流程：

1. **`/kiro:spec [feature]`** - 创建需求文档和验收标准
2. **`/kiro:design [feature]`** - 制定架构设计和组件规划
3. **`/kiro:task [feature]`** - 生成具体的实施任务清单
4. **`/kiro:execute [task]`** - 执行具体的开发任务
5. **`/kiro:vibe [question]`** - 快速开发问答支持

这个流程的妙处在于，每一步都有明确的输出，前一步的结果会成为下一步的输入，形成了一个完整的闭环。

### 增强分析能力

除了开发流程，项目还包含一系列增强思考的命令：

- **`/think-harder [problem]`** - 深度分析问题
- **`/think-ultra [complex problem]`** - 超级综合分析
- **`/reflection`** - 分析和改进当前的指令
- **`/reflection-harder`** - 全面的会话分析和学习
- **`/eureka [breakthrough]`** - 项目成果复盘

### GitHub 深度集成

对于开源开发者来说，GitHub 集成是必不可少的：

- **`/gh:review-pr [PR_NUMBER]`** - 全面的 PR 审查和评论
- **`/gh:fix-issue [issue-number]`** - 完整的问题解决工作流

### Claude Code 管理

- **`/cc:create-command [name] [description]`** - 创建新的 Claude Code 命令

## 如何使用

### 快速安装

```bash
# 备份原有配置
mv ~/.claude ~/.claude.bak

# 克隆配置仓库
git clone https://github.com/feiskyer/claude-code-settings.git ~/.claude

# 安装 GitHub Copilot API 代理
npm install -g copilot-api

# 授权你的 GitHub Copilot 账户
copilot-api auth

# 建议在后台运行（使用 tmux）
tmux new-session -d -s copilot 'copilot-api start'
```

### 特别说明

这套配置使用 **GitHub Copilot** 作为 Claude Code 的模型提供者，通过 [copilot-api](https://github.com/ericc-ch/copilot-api) 代理实现。这样做成本低、速度快且无需注册和订阅 Claude 账户。如果你使用其他配置，可以适当调整甚至删除 settings.json 文件。

## 使用示例

### 功能开发

假设我们要开发一个用户认证功能，可以这么使用：

```bash
# 第一步：定义需求
/kiro:spec 用户认证系统

# 第二步：设计架构
/kiro:design 用户认证系统

# 第三步：拆解任务
/kiro:task 用户认证系统

# 第四步：逐个执行
/kiro:execute 用户认证系统 实现用户注册接口
```

每一步都会产生详细的文档和代码，而且前后一致，逻辑清晰。实际上，如果你一直保持在 `/kiro:spec` 开始的会话中没有退出，后面几个命令都不需要你主动执行，Claude 会自动提示你要不要进入下一步的流程。

### 代码审核

Github 项目的 PR 审核，可以这么使用：

```bash
/gh:review-pr 123
```

Claude Code 会自动拉取 PR 内容，进行全面分析，给出具体的改进建议，并在发布 PR 审核意见前征求你的意见（同意或者要求修改）。

## 写在最后

这套配置还在持续演进中，未来还会增加更多 Vibe Coding 实践技巧。如果你有什么好的建议，也欢迎随时提 PR 改进或者提 Issue 讨论。

**项目地址**：<https://github.com/feiskyer/claude-code-settings>

---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)