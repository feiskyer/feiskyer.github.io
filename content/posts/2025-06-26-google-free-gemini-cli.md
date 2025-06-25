---
title: "谷歌发布开源免费命令行编程工具 Gemini CLI"
date: 2025-06-26T06:50:06+08:00
draft: false
tags: [AI, Vibe Coding]
---

类似于 Claude Code 和 OpenAI Codex CLI，谷歌也下场发布了命令行编程工具—— Gemini CLI，提供了慷慨的免费额度，其代码还是完全 [开源](https://github.com/google-gemini/gemini-cli) 的。

## 什么是 Gemini CLI？

Gemini CLI 是一个 **AI 驱动的终端工具**，它具备以下核心特点：

- **命令行集成**：直接在终端中与 AI 交互的工具。
- **大型代码库处理**：1M 令牌上下文窗口，能够查询和编辑大型代码库。
- **多模态能力**：支持从 PDF、草图等多种输入生成应用。
- **开源架构**：Apache 2.0 开源协议，代码完全透明。
- **内置搜索增强**：使用内置于 Gemini 的 Google 搜索工具提供事实依据。
- **丰富工具集成**：连接 MCP、Imagen、Veo、Lyria 等外部工具。
- **免费配额**：个人 Google 账号即可享受每分钟 60 次、每天 1000 次的免费请求。

---

## 使用方法

1. **临时运行**

   ```bash
   npx https://github.com/google-gemini/gemini-cli
   ```

2. **全局安装**

   ```bash
   npm install -g @google/gemini-cli
   gemini
   ```

3. **完成认证**

   启动 gemini 命令行后会自动引导你完成 Google 账号认证：

   - **个人 Google 账号**：默认选项，免费使用
   - **API Key 方式**：从 Google AI Studio 生成 API Key，设置环境变量 `export GEMINI_API_KEY="YOUR_API_KEY"`

---

## 架构原理

### 核心组件

Gemini CLI 主要由两个核心包组成，以及一套可供系统在处理命令行输入时使用的工具套件：

**1. CLI 包 (packages/cli)**

- **用途**：包含面向用户的 Gemini CLI 部分，负责处理初始用户输入、呈现最终输出并管理整体用户体验
- **关键功能**：
  - 输入处理
  - 历史记录管理
  - 显示渲染
  - 主题和 UI 定制
  - CLI 配置设置

**2. Core 包 (packages/core)**

- **用途**：作为 Gemini CLI 的后端，接收来自 CLI 包的请求，协调与 Gemini API 的交互，并管理可用工具的执行
- **关键功能**：
  - 与 Google Gemini API 通信的 API 客户端
  - 提示构建和管理
  - 工具注册和执行逻辑
  - 对话或会话的状态管理
  - 服务端配置

**3. 工具套件 (packages/core/src/tools/)**

- **用途**：扩展 Gemini 模型功能的独立模块，允许其与本地环境交互（如文件系统、shell 命令、网络获取）
- **交互方式**：Core 包根据 Gemini 模型的请求调用这些工具

### 交互流程

典型的 Gemini CLI 交互遵循以下流程：

1. **用户输入**：用户在终端输入提示或命令，由 CLI 包管理
2. **请求发送到 Core**：CLI 包将用户输入发送到 Core 包
3. **请求处理**：Core 包执行以下操作：
   - 为 Gemini API 构建适当的提示，可能包括对话历史和可用工具定义
   - 将提示发送到 Gemini API
4. **Gemini API 响应**：Gemini API 处理提示并返回响应，响应可能是直接答案或使用可用工具的请求
5. **工具执行（如适用）**：
   - 当 Gemini API 请求工具时，Core 包准备执行它
   - 如果请求的工具可以修改文件系统或执行 shell 命令，会首先向用户提供工具及其参数的详细信息，用户必须批准执行
   - 只读操作（如读取文件）可能不需要明确的用户确认即可继续
   - 确认后，或如果不需要确认，Core 包在相关工具内执行相关操作，结果由 Core 包发送回 Gemini API
   - Gemini API 处理工具结果并生成最终响应
6. **响应返回 CLI**：Core 包将最终响应发送回 CLI 包
7. **显示给用户**：CLI 包格式化响应并在终端中显示给用户

### 关键设计原则

- **模块化**：将 CLI（前端）与 Core（后端）分离允许独立开发和潜在的未来扩展
- **可扩展性**：工具系统设计为可扩展的，允许添加新功能
- **用户体验**：CLI 专注于提供丰富的交互式终端体验

---

## 基础用法示例

### 简单示例

启动 Gemini CLI 后，试试这些基本命令：

```bash
# 启动 Gemini CLI
gemini

# 分析代码库
> Summarize the changes in this project since last week

# 探索系统架构
> Help me understand the architecture of this system

# 迁移代码库
> Migrate this codebase from JavaScript to TypeScript

# 创建 Discord 机器人
> Create a Discord bot that responds to messages
```

### 多模态能力体验

```bash
# 分析图像
> analyze this screenshot and explain what it shows

# 基于设计图生成代码
> convert this UI mockup to React components

# 处理多种文件类型
> explain the relationship between these config files
```

---

## 核心功能

### 1. 代码库查询和分析

Gemini CLI 最强大的功能是理解和分析大型代码库：

```bash
# 项目概览
> give me a high-level overview of this project's architecture

# 依赖关系分析
> show me the dependency graph for this module

# 性能分析
> identify potential performance bottlenecks in this codebase

# 安全审计
> scan for common security vulnerabilities
```

---

### 2. 智能代码编辑

直接修改代码文件：

```bash
# 添加新功能
> add a caching layer to the database queries

# 重构代码
> refactor this class to follow SOLID principles

# 修复 bug
> fix the memory leak in the event listener cleanup

# 优化性能
> optimize this algorithm for better time complexity
```

---

### 3. 文件系统操作

内置的文件系统工具让你能够：

```bash
# 批量文件操作
> rename all .js files to .ts and update imports

# 文件搜索和过滤
> find all unused CSS classes in the stylesheets

# 目录结构优化
> reorganize the components folder following best practices
```

### 4. Shell 命令集成

无缝执行系统命令：

```bash
# 构建和测试
> run the test suite and fix any failing tests

# 部署相关
> prepare this application for production deployment

# 开发环境设置
> set up the development environment for new contributors
```

---

### 5. 网络搜索和获取

```bash
# 技术调研
> search for the latest best practices for React state management

# 实时信息获取
> fetch the current status of this API endpoint

# 文档查询
> find the official documentation for this library version
```

---

## 高级功能

### 自动化工作流

创建复杂的自动化任务：

```bash
# 端到端功能开发
> create a complete user authentication system with:
  1. backend API endpoints
  2. frontend login/signup forms
  3. JWT token handling
  4. password validation
  5. unit tests

# 项目初始化
> bootstrap a new microservice with:
  - Docker configuration
  - CI/CD pipeline
  - logging and monitoring
  - API documentation
  - health check endpoints
```

### 多模态应用生成

```bash
# 基于设计生成应用
> create a mobile app based on this design mockup

# 数据可视化
> generate interactive charts from this CSV data

# 界面原型开发
> build a prototype dashboard with these requirements
```

### 系统集成

```bash
# 数据库迁移
> create migration scripts for schema changes

# API 集成
> integrate this third-party API with error handling

# 监控和日志
> add comprehensive logging and metrics collection
```

---

## 配置和定制

### 内置工具概述

Gemini CLI 包含内置工具，供 Gemini 模型用于与本地环境交互、访问信息和执行操作。这些工具增强了 CLI 的功能，以便完成各种复杂任务。

**工具工作原理**：
在 Gemini CLI 中，工具是 Gemini 模型可以请求执行的特定函数或模块。例如，当你要求 Gemini "总结 `my_document.txt` 的内容" 时，模型会识别需要读取该文件，并请求执行 `read_file` 工具。

**核心能力**：

- **访问本地信息**：访问本地文件系统、读取文件内容、列出目录等
- **执行命令**：通过 `run_shell_command` 等工具运行 shell 命令（具备安全措施和用户确认）
- **网络交互**：从 URL 获取内容
- **执行操作**：修改文件、创建新文件或在系统上执行其他操作（通常带有安全防护）
- **增强响应准确性**：通过工具获取实时或特定本地数据，使 Gemini 的响应更准确、相关且基于实际环境

**内置工具分类**：

- **文件系统工具**：用于与文件和目录交互（读取、写入、列出、搜索等）
- **Shell 工具** (`run_shell_command`)：执行 shell 命令
- **网络获取工具** (`web_fetch`)：从 URL 检索内容
- **网络搜索工具** (`web_search`)：搜索网络
- **多文件读取工具** (`read_many_files`)：专用于从多个文件或目录读取内容的工具，常与 `@` 命令一起使用
- **内存工具** (`save_memory`)：跨会话保存和回忆信息

**扩展工具集成**：

- **MCP 服务器**：MCP 服务器充当 Gemini 模型与本地环境或其他服务（如 API）之间的桥梁
- **沙箱隔离**：沙箱将模型及其更改与环境隔离，以降低潜在风险

**安全和确认机制**：

许多工具，特别是那些可以修改文件系统或执行命令的工具（`write_file`、`edit`、`run_shell_command`），都具有安全设计：

- **需要确认**：在执行潜在敏感操作之前提示用户，显示即将采取的操作
- **沙箱隔离**：所有工具都受到沙箱执行的限制，将模型及其更改与环境隔离以降低潜在风险


---

## 实际应用场景

### 1. 探索新代码库

```bash
# 快速上手陌生项目
> I'm new to this codebase, help me understand:
  - project structure
  - main technologies used
  - how to run locally
  - where to start contributing

# 代码审查
> review recent commits and highlight important changes
```

### 2. 现有代码维护

```bash
# 技术债务处理
> identify technical debt and suggest refactoring priorities

# 依赖升级
> analyze dependencies and create upgrade plan

# 性能优化
> profile the application and optimize critical paths
```

### 3. 运维自动化

```bash
# 部署脚本生成
> create deployment scripts for multiple environments

# 监控设置
> set up comprehensive monitoring and alerting

# 故障排查
> analyze these error logs and suggest solutions
```

---

## 使用配额和定价

### 免费使用配额

**个人 Google 账号** 提供慷慨的免费配额：

- **请求频率**：每分钟 60 次请求
- **日配额**：每天 1000 次请求
- **上下文窗口**：完整的 100 万 token
- **功能限制**：无功能限制

### 高级使用选项

如需更高配额或企业级功能：

- **Google AI Studio API Key**：按使用量付费
- **Vertex AI 集成**：企业级部署
- **Gemini Code Assist 集成**：标准版和企业版许可

---

## 最佳实践

### 1. 清晰描述需求

❌ 不好：`fix this code`

✅ 更好：`fix the race condition in the async data fetching that causes UI flicker`

### 2. 结构化复杂任务

```bash
> Create a user management system with:
  1. User model with validation
  2. CRUD API endpoints
  3. Authentication middleware
  4. Admin dashboard UI
  5. Role-based permissions
  6. Comprehensive tests
```

### 3. 充分利用上下文

```bash
# 先让 Gemini 理解项目背景
> analyze the existing authentication system

# 然后基于理解进行修改
> enhance it with two-factor authentication
```

### 4. 增量开发

```bash
> start with basic user registration
> add email verification
> implement password reset
> add social login options
```

---

## 开源生态和社区

Gemini CLI 代码完全开源在 [GitHub](https://github.com/google-gemini/gemini-cli)，使用 Apache 2.0 许可证，刚刚发布就冲到了 1 万 + Star，可见其受欢迎程度。作为完全开源的项目，所有功能实现都可审查，无中间服务器，直连 Google API，安全可信。如果你在使用过程中发现任何问题，都可以随时通过 Issues 提交 bug 和功能请求，或者遵循贡献指南提交 PR 修复问题、完善文档。社区驱动的开发模式使得这个工具能够快速迭代和改进。

---

## 与其他 AI 工具对比

| 特性           | Gemini CLI | Claude Code | OpenAI Codex CLI | Cursor |
| -------------- | ---------- | ----------- | --------------- | ------ |
| **免费配额**   | ✅ 慷慨    | ❌ 需付费   | 需自带模型   | 短期试用           |
| **开源**      | ✅ 开源    | ❌ 闭源     | ✅ 开源     | ❌ 闭源             |
| **终端集成**   | ✅ 原生    | ✅ 原生     | ✅ 原生     | ❌ IDE             |
| **MCP 集成**   | ✅ 完整    | ✅ 完整     | 仅 Rust 实现   | ✅ 完整 |
| **内置搜索**   | ✅ Google  | ✅ Claude       | ❌     | ❌             |
| **实际体验** | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️ | ⭐️⭐️⭐️⭐️ |

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
