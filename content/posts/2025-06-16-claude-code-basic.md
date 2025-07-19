---
title: "Claude Code 从0到1入门指南"
date: 2025-06-16T12:15:30+08:00
tags: [AI, Vibe Coding, Claude Code]
draft: false
---

Claude Code 是 Anthropic 推出的智能编程助手，它直接集成到你的终端环境中，能够理解你的代码库，并通过自然语言命令帮助你更快地编程。本指南将带你从零开始，快速掌握 Claude Code 的使用。

## 什么是 Claude Code？

Claude Code 是一个**代理式编程工具**，它具备以下核心特点：

- **直接集成终端**：无需额外服务器或复杂配置
- **理解整个代码库**：能够分析项目结构和代码逻辑
- **自然语言交互**：用普通话描述需求，Claude 帮你实现
- **安全隐私设计**：直连 Anthropic API，无中间服务器
- **实际操作能力**：真正执行文件编辑、Git 操作等任务

---

## 第一步：安装和设置

### 系统要求

确保你的系统满足以下要求：

- **操作系统**：macOS 10.15+、Ubuntu 20.04+/Debian 10+ 或 Windows（通过 WSL）
- **硬件**：最少 4GB 内存
- **软件**：Node.js 18+、Git 2.23+（可选）
- **网络**：需要互联网连接进行认证和 AI 处理

### 安装步骤

1. **安装 Node.js**
    首先确保安装了 Node.js 18+，然后运行：

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **导航到项目目录**

   ```bash
   cd your-project-directory
   ```

3. **启动 Claude Code**

   ```bash
   claude
   ```

4. **完成认证**
    Claude Code 提供多种认证选项：

   - **Anthropic Console**：通过 OAuth 流程连接（需要在 console.anthropic.com 有活跃账户）
   - **Claude Pro/Max 订阅**：使用 Claude.ai 账户登录
   - **企业平台**：配置 Amazon Bedrock 或 Google Vertex AI

---

## 第二步：第一次体验

### 初始化项目

首次使用时，建议按以下步骤操作：

```bash
# 启动 Claude Code
claude

# 让 Claude 分析项目
> summarize this project

# 生成项目指南
> /init

# 提交生成的 CLAUDE.md 文件
> commit the generated CLAUDE.md file
```

---

### 基本交互示例

试试这些简单的命令来熟悉 Claude Code：

```bash
# 了解项目
> what does this project do?

# 查看技术栈
> what technologies does this project use?

# 找到入口文件
> where is the main entry point?

# 解释文件结构
> explain the folder structure
```

---

## 第三步：核心功能掌握

### 1. 代码编辑和修改

Claude Code 最强大的功能是直接编辑代码：

```bash
# 添加简单功能
> add a hello world function to the main file

# 修复 bug
> there's a bug where users can submit empty forms - fix it

# 重构代码
> refactor the authentication module to use async/await instead of callbacks
```

---

### 2. Git 集成

Claude Code 让 Git 操作变得对话化：

```bash
# 查看变更
> what files have I changed?

# 智能提交
> commit my changes with a descriptive message

# 分支操作
> create a new branch called feature/quickstart

# 查看历史
> show me the last 5 commits

# 解决冲突
> help me resolve merge conflicts
```

---

### 3. 测试和调试

```bash
# 编写测试
> write unit tests for the calculator functions

# 运行测试
> run tests for the refactored code

# 性能优化
> analyze the performance of this code and suggest optimizations
```

### 4. 文档和代码审查

```bash
# 更新文档
> update the README with installation instructions

# 代码审查
> review my changes and suggest improvements

# 添加注释
> add JSDoc comments to the undocumented functions in auth.js
```

---

## 第四步：高级技巧

### 使用扩展思维

对于复杂的架构决策或难题，可以让 Claude 深度思考：

```bash
# 触发深度思考
> I need to implement OAuth2 authentication. Think deeply about the best approach.

# 加强思考深度
> think harder about edge cases we should handle

# 思考安全问题
> think about potential security vulnerabilities in this approach
```

---

### 自定义斜杠命令

创建项目特定的快捷命令：

```bash
# 创建命令目录
mkdir -p .claude/commands

# 创建优化命令
echo "Analyze the performance of this code and suggest three specific optimizations:" > .claude/commands/optimize.md

# 使用自定义命令
> /project:optimize
```

### 并行工作流

使用 Git worktrees 运行多个 Claude Code 实例：

```bash
# 创建新的工作树
git worktree add ../project-feature-a -b feature-a

# 在新工作树中运行 Claude
cd ../project-feature-a
claude
```

---

### 作为 Unix 工具使用

将 Claude Code 集成到脚本中：

```bash
# 管道操作
cat build-error.txt | claude -p 'explain the root cause of this error'

# 添加到构建脚本
npm run "lint:claude": "claude -p 'look at changes vs main and report issues'"

# 结构化输出
claude -p 'analyze this code' --output-format json > analysis.json
```

---

## 第五步：配置和定制

### 基本配置

运行 `/config` 命令进行交互式配置，或编辑配置文件：

```bash
// ~/.claude/settings.json (全局设置)
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)"
    ],
    "deny": [
      "Bash(curl:*)"
    ]
  }
}
```

---

## 常用命令速查

| 命令                | 功能             | 示例                                |
| ------------------- | ---------------- | ----------------------------------- |
| `claude`            | 启动交互模式     | `claude`                            |
| `claude "task"`     | 执行一次性任务   | `claude "fix the build error"`      |
| `claude -p "query"` | 运行后退出       | `claude -p "explain this function"` |
| `claude -c`         | 继续最近对话     | `claude -c`                         |
| `claude -r`         | 恢复之前对话     | `claude -r`                         |
| `/clear`            | 清除对话历史     | `> /clear`                          |
| `/help`             | 显示帮助         | `> /help`                           |
| `exit` 或 Ctrl+C    | 退出 Claude Code | `> exit`                            |

---

## 最佳实践

### 1. 具体描述需求

❌ 不好：`fix the bug`

✅ 更好：`fix the login bug where users see a blank screen after entering wrong credentials`

### 2. 分步骤处理复杂任务

```bash
> 1. create a new API endpoint for user profiles
> 2. add validation for required fields
> 3. write tests for the endpoint
```

### 3. 让 Claude 先理解代码

```bash
> analyze the database schema
> how does error handling work in this app?
```

### 4. 使用快捷方式

- 用 Tab 键自动补全命令
- 按 ↑ 键查看命令历史
- 输入 `/` 查看所有斜杠命令

---

## 故障排除

### 常见问题

1. **WSL 安装问题**

   ```bash
   npm config set os linux
   npm install -g @anthropic-ai/claude-code --force --no-os-check
   ```

2. **权限错误**
    不要使用 `sudo npm install -g`。

3. **Node.js 未找到**
    确保 WSL 使用 Linux 版本的 Node.js 而非 Windows 版本

---

## 总结

Claude Code 是一个强大的 AI 编程助手，它能够：

- 理解和分析你的整个代码库
- 执行实际的编程任务和文件操作
- 与 Git 和其他开发工具无缝集成
- 通过自然语言交互简化开发流程

通过这个入门指南，你应该已经掌握了 Claude Code 的基本使用方法。建议从简单的查询开始，逐步尝试更复杂的编程任务，随着使用经验的积累，你会发现 Claude Code 能够显著提升你的开发效率。

记住，Claude Code 就像一个有经验的编程伙伴 —— 用自然语言描述你想要实现的功能，它会帮你完成从理解需求到实现代码的整个过程。

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
