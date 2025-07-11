---
title: "Claude Code 最佳实践和使用技巧"
date: 2025-07-08T20:18:53+08:00
draft: false
tags: [AI, Vibe Coding]
---

Claude Code 是 Anthropic 推出的智能编程助手，它直接集成到你的终端环境中，能够理解你的代码库，并通过自然语言命令帮助你更快地编程。

本文将从实践者的角度，系统分享 Claude Code 的最佳实践和使用技巧，帮助你快速掌握这个革命性的开发工具。

## 1. 初始化配置

使用 `npm install -g @anthropic-ai/claude-code` 安装 Claude Code 并登录之后，首先为项目生成 `CLAUDE.md` 并安装配套工具。

### 1.1 创建 CLAUDE.md 文件

`CLAUDE.md` 是 Claude Code 的核心配置文件，它会被自动读取并加入到上下文中。这个文件应该包含：

- 项目基础信息和架构说明；
- 常用命令和构建脚本；
- 代码规范和约定；
- 测试指南；
- 开发环境配置；
- 其他必要的上下文信息（可通过 `@path/to/import` 来引用项目文件）。

推荐通过 init 命令创建 CLAUDE.md 文件：

```bash
# 使用 /init 命令自动生成
claude
> /init

# 或者手动创建并填充内容
touch CLAUDE.md
```

CLAUDE.md 文件可以放置在多个位置：

- 项目根目录：`./CLAUDE.md`（推荐，可提交到 git）；
- 项目本地：`./CLAUDE.local.md`（不提交到 git）；
- 全局配置：`~/.claude/CLAUDE.md`；
- 父目录和子目录中也会被自动读取。

### 1.2 配置工具权限

Claude Code 默认采用保守的权限策略。你可以通过以下四种方式显式授权：

1. 启动时的交互式授权提示
2. 运行 `/permissions` 命令
3. 手动编辑 `.claude/settings.json`
4. 启动参数 `--allowedTools`

```bash
# 使用 /permissions 命令管理权限
> /permissions

# 或者通过命令行参数
claude --allowedTools Edit,Bash(git commit:*)
```

推荐允许的工具：

- `Edit`: 文件编辑
- `Bash(git commit:*)`: Git 提交操作
- `WebFetch(*)`：访问 URL 网址

### 1.3 安装配套工具

推荐安装 GitHub CLI，自动化 Github 工作流：

```bash
brew install gh

# 配置 GitHub 认证
gh auth login
```

## 2. 工作流程

### 2.1 探索 - 计划 - 编程 - 提交流程

这是最通用的工作流程，适用于大多数开发任务：

```bash
# 1. 探索阶段 - 了解现有代码
"请阅读相关文件了解当前架构，但暂时不要编写代码"

# 2. 计划阶段 - 使用扩展思考（按两次 Shift+TAB 进入 PLAN 模式）
"请 ultrathink 并制定详细的实现计划，并指示 sub-agents 并行验证关键细节"

# 3. 编码阶段
"请按照计划实现功能"

# 4. 提交阶段
"请提交更改并创建 PR"
```

### 2.2 测试驱动开发流程

对于可以通过测试验证的功能：

```bash
# 1. 编写测试
"请基于期望的输入输出编写测试，确保测试会失败"

# 2. 运行测试确认失败
"运行测试确认失败，不要编写实现代码"

# 3. 提交测试
"请提交测试代码"

# 4. 实现功能
"请编写代码使测试通过，不要修改测试"

# 5. 提交实现
"请提交实现代码"
```

### 2.3 UI 开发迭代流程

对于前端开发：

```bash
# 1. 提供设计图
# 拖拽图片到 Claude Code 界面

# 2. 实现 UI
"请按照设计图实现界面"

# 3. 截图对比
"请截图当前实现，与设计图对比并改进"

# 4. 迭代优化
"请继续优化，直到效果满意"
```

## 3. 进阶功能和技巧

### 3.1 使用 MCP 扩展工具

Claude Code 支持 MCP（Model Context Protocol）来扩展功能：

```json
// .mcp.json 示例
{
  "mcpServers": {
    "playwright": {
      "args": [
        "@playwright/mcp@latest",
        "--headless"
      ],
      "command": "npx"
    },
    "context7": {
      "args": [
        "-y",
        "@upstash/context7-mcp@latest"
      ],
      "command": "npx"
    }
  }
}
```

### 3.2 自定义斜杠命令

在 `.claude/commands/` 目录创建自定义命令，比如创建一个 `issue.md` 存放用于修复 Github Issue 的命令：

```md
Please analyze and fix the Github issue: $ARGUMENTS.

Follow these steps:

# PLAN

1. Use 'gh issue view' to get the issue details
2. Understand the problem described in the issue
3. Ask clarifying questions if necessary
4. Understand the prior art for this issue
    - Search the scratchpads for previous thoughts related to the issue
    - Search PRs to see if you can find history on this issue
    - Search the codebase for relevant files
5. Think harder about how to break the issue down into a series of small, manageable tasks.
6. Document your plan in a new scratchpad
    - include the issue name in the filename
    - include a link to the issue in the scratchpad.

# CREATE
- Create a new branch for the issue
- Solve the issue in small, manageable steps, according to your plan.
- Commit your changes after each step.

# TEST
- Use puppeteer via MCP to test the changes if you have made changes to the UI
- Write unit tests to describe the expected behavior of your code
- Run the full test suite to ensure you haven't broken anything
- If the tests are failing, fix them
- Ensure that all tests are passing before moving on to the next step

# SUBMIT
- Push and open a PR on Github.

Remember to use the GitHub CLI ('gh') for all Github-related tasks.
```

使用方法如下：

```bash
> /issue 1234
```

### 3.3 上下文管理

Claude Code 的上下文窗口有限，且上下文过长会导致幻觉严重，需要合理管理上下文信息：

- 使用 @ 引用文件；
- 在任务切换时使用 `/clear` 清空上次任务信息；
- 长时间会话定期压缩上下文；
- 必要时从历史会话恢复（即找回之前的上下文信息）；
- 将重要信息通过 `# <context>` 记录到 CLAUDE.md 中。

命令格式：

```bash
# 使用文件引用
请参考 @src/components/UserProfile.tsx 的结构

# 压缩上下文
> /compact

# 清理上下文
> /clear

# 增加记忆
# <context>

# 恢复历史会话
/resume
```

也可以在启动 claude 命令时从历史会话恢复：

```bash
# 续聊上次会话
claude --continue
claude --continue --print   # 适合脚本调用

# 从历史会话中选择再继续
claude --resume
```

## 4. 项目组织和管理

### 4.1 使用 `ROADMAP.md` 管理项目

创建项目路线图：

```md
# 项目开发路线图

## 开发流程

1. ** 任务规划 **
   - 分析现有代码基础
   - 更新 ROADMAP.md 添加新任务
   - 优先级任务插入到最后完成任务之后

2. ** 任务创建 **
   - 在 `/tasks` 目录创建详细任务文件
   - 命名格式：`XXX-description.md`
   - 包含规格说明、相关文件、验收标准

3. ** 任务实现 **
   - 按照任务文件中的步骤实现
   - 每完成一步更新任务文件进度
   - 每步完成后暂停等待进一步指令

## 任务列表

### 已完成 ✅
- **任务 001: 数据库架构** ✅
  - 参考: `/tasks/001-database.md`
  - 实现了核心表结构和关系

### 进行中 🔄
- ** 任务 002: 用户界面 ** 🔄
  - 参考: `/tasks/002-ui.md`
  - 正在实现登录和注册页面

### 计划中 📋
- ** 任务 003: API 接口 **
  - 设计 RESTful API
  - 实现用户认证
```

### 4.2 任务模板

```md
# 任务 XXX: 功能描述

## 进度摘要

**状态**: 未开始

- [ ] 步骤 1: 创建组件
- [ ] 步骤 2: 实现逻辑
- [ ] 步骤 3: 编写测试
- [ ] 步骤 4: 集成验证

## 概述

详细描述功能需求和预期效果。

## 当前状态分析

分析现有代码基础和相关文件。

## 目标状态

描述完成后的期望状态。

## 实现步骤

### 步骤 1: 创建组件
详细描述第一步需要做什么。

** 涉及文件:**
- `src/components/NewComponent.tsx`
- `src/types/index.ts`

### 步骤 2: 实现逻辑
详细描述第二步需要做什么。

## 验收标准

### 功能要求
- [ ] 功能 A 正常工作
- [ ] 功能 B 正常工作

### 技术要求
- [ ] 通过所有测试
- [ ] 代码符合规范
- [ ] 性能满足要求

## 相关文件

### 新建文件
- `src/components/NewComponent.tsx`
- `src/utils/helper.ts`

### 修改文件
- `src/app/page.tsx`
- `src/types/index.ts`

## 注意事项

- 保持向后兼容性
- 确保响应式设计
- 考虑无障碍性
```

### 4.3 并行工作流

当需要同时开发多个功能分支时，可结合 `git worktree` 与多终端并行运行 Claude：

```bash
git worktree add -b feature-x ../feature-x
cd ../feature-x
claude --resume   # 在新终端继续上下文
```

这样可避免频繁切换分支且互不干扰，提高多任务效率。

## 5. 实用技巧和最佳实践

### 5.1 清晰明确的提示词指令

```bash
# 不好的指令
"给 foo.py 添加测试"

# 好的指令
"为 foo.py 编写新的测试用例，覆盖用户登出的边界情况，避免使用 mock"
```

### 5.2 使用思考模式

```bash
# 激活不同级别的思考
"think 并分析问题"          # 基础思考
"think hard 制定计划"       # 深度思考
"think harder 优化方案"     # 更深思考
"ultrathink 并制定详细计划"  # 最深思考
```

### 5.3 引用文件、图片或网址

Claude Code 支持各种不同类型的输入文件：

- **截图**: `cmd+ctrl+shift+4` 截图到剪贴板，然后 `ctrl+v` 粘贴；
- **拖拽**: 直接拖拽图片到界面；
- **文件引用**: 使用 @ 时按 Tab 键自动补全文件路径；
- **URL**: 直接粘贴 URL 让 Claude 获取内容。

### 5.4 集成版本控制

```bash
# 让 Claude 管理 Git 操作
"请查看当前更改并提交"
"请创建新分支实现 feature-x"
"请基于当前更改创建 PR"
"请解决合并冲突"
```

### 5.5 无人值守模式

> **⚠️ 风险提示：** 仅在一次性脚本或 CI 容器中使用 `--dangerously-skip-permissions`，避免本机数据被篡改或泄露。

```bash
# 跳过所有权限确认
claude --dangerously-skip-permissions

# 设置别名方便使用
alias cc="claude --dangerously-skip-permissions"
```

### 5.6 使用检查清单和 Scratchpad

对于复杂多步骤任务或批量任务，建议让 Claude 先生成 Markdown 检查清单，再逐项勾选完成。示例：

```bash
# 生成 ESLint 报错清单
claude -p "运行 eslint 并把所有错误输出成 Markdown checklist"
```

然后让 Claude 循环处理每一项，修复后勾选 ✅ 并继续下一个。

### 5.7 非交互模式

在自动化任务、CI/CD 等场景中，你可以使用非交互模式，在 CLI 中直接提供提示词，让 claude 自动完成你的任务。

```bash
claude -p "分析代码并生成测试报告"

# JSON 输出
claude -p "分析代码并生成测试报告" --output-format json

# 自动化代码审查
claude -p "审查当前 PR 中的代码变更"

# 提供数据
cat build-error.txt | claude -p 'concisely explain the root cause of this build error'
```

### 5.8 键盘快捷键

几个常用的快捷键：

- 单次 `Shift+Tab`: 切换自动接受模式；
- 两次 `Shift+Tab`: 切换 PLAN 模式；
- `Esc`: 中断当前操作；
- `Esc + Esc`: 返回历史编辑提示；
- `Tab`: 文件名自动补全
- `#`: 快速添加记忆到 CLAUDE.md

## 6. 使用多智能完成复杂任务

Claude Code 支持并行启动多个 Agent，让它们分别负责不同任务，可用来加速执行过程并完成复杂任务。以下是两个最常用的多 Agent 模式。

### 6.1 多任务并行执行

这是最简单的多任务并行模式，常用在无需修改代码或者任务所需修改代码无冲突的场景下，特别适合代码库探索和独立子任务处理。

Claude Code 的 Task Tool 可以创建多个 "subagent"（子代理），每个都是轻量级的 Claude Code 实例，拥有独立的上下文窗口。即，你可以在单个会话中并行运行多个任务：

```bash
# 探索代码库的并行任务
"使用 4 个并行任务探索代码库，每个代理探索不同的目录"

# 批量处理子任务
"开始一项研究，使用 6 个并行任务将所有仓库更新为使用 Bun。其中一个任务用于网络搜索，获取针对 Nexts、服务器和包的最佳实践，另外 5 个任务用于规划如何迁移我们现有的 5 个包，制定完整的迁移计划并将其写入 PLAN.md 文件。"

# 适合的应用场景
"并行运行不同的测试套件"
"同时分析多个日志文件"
"批量处理多个配置文件"
```

### 6.2 Git Worktree 并行开发

使用 `git worktree` 创建多个工作区，各自运行独立的 Claude 实例：

```bash
# 创建功能分支工作区
git worktree add -b feature-auth ../auth-workspace
git worktree add -b feature-payment ../payment-workspace
git worktree add -b feature-admin ../admin-workspace

# 在各工作区启动 Claude
cd ../auth-workspace && claude --resume
cd ../payment-workspace && claude --resume
cd ../admin-workspace && claude --resume
```

## 结语

用好 Claude Code，你需要做三件事

1. 把 “写代码” 升级为“设计问题”

   - **先问为什么**：每次提指令前，先用一句话写清 “我要解决的核心约束”。
   - **再问如何验证**：给 Claude 明确的 “判定标准”（测试、日志或业务指标）。
   - **结果**：你获得的不是片段式答案，而是一套完整方案。

2. 把 AI 当“偏执的实习生”

   - 视它为 **无限精力 + 零上下文** 的新人。
   - **喂足上下文信息**，再用分步骤指令驱动；别指望它自己补全隐含假设。
   - **审稿而非复写**：先让它产出初稿，再由你决策取舍。

3. 把“工具链”写进流程

   - 在 `CLAUDE.md` 固化 **常用命令 + 权限模板**；
   - 每次新功能都走 **探索 → 计划 → 编程 → 提交** 四步；
   - 定期回顾 `ROADMAP.md`，删掉陈旧指令，防止上下文膨胀。

掌握了这些技巧，你会发现 Claude Code 放大的不是键盘速度，而是你的“问题建模能力”。

当你把重复性的复杂度留给机器，把创造性的决策留给自己，真正的效率提升就此开始。这就是 AI 时代开发者的新工作方式。

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
