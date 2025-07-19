---
title: "掌握 Claude Code / 命令：让 AI 成为你的开发利器"
date: 2025-07-01T19:17:01+08:00
tags: [AI, Vibe Coding, Claude Code]
draft: false
---

在软件开发的日常工作中，重复性任务和复杂流程总是消耗着开发者大量的时间和精力。Claude Code 的 / 命令（Slash Command）为这个问题提供了一个优雅的解决方案——通过简洁的命令接口，将常用的开发流程和工作流自动化，让开发者能够专注于真正重要的创造性工作。本文将带你探索斜杠命令的使用方法，以及如何借助它来提高你的生产力。

## 基础概念

斜杠命令是 Claude Code 的核心交互方式，它提供了一种结构化的方法来控制 AI 助手的行为。通过简洁的 `/command` 语法，你可以快速访问预定义的功能，或行自定义的复杂工作流。

这种设计哲学借鉴了现代开发工具的最佳实践：

- **简洁性**：单一命令完成复杂任务。
- **一致性**：统一的命令格式和参数传递方式。
- **可扩展性**：支持自定义命令和团队协作。
- **上下文感知**：命令能够理解当前项目状态和开发环境。

## 内置斜杠命令

Claude Code 提供了丰富的内置命令，覆盖了开发工作流的各个环节。让我们按功能分类来详细了解：

### 账户与环境管理

这类命令帮助你管理 Claude Code 的基本配置和工作环境：

| 命令 | 功能描述 | 使用场景 |
|------|----------|----------|
| `/login` | 切换或登录 Anthropic 账户 | 多账户管理，团队协作 |
| `/logout` | 退出当前账户 | 安全清理，账户切换 |
| `/config` | 查看和修改配置设置 | 环境配置，偏好设置 |
| `/permissions` | 管理工具权限 | 安全配置，权限控制 |
| `/status` | 查看系统和账户状态 | 健康检查，故障诊断 |
| `/model` | 选择或更改 AI 模型 | 性能调优，成本控制 |
| `/mcp` | 管理 MCP 服务器连接 | 第三方集成，企业工具链 |

### 项目与内存管理

这些命令专注于项目层面的配置和上下文管理：

| 命令 | 功能描述 | 使用场景 |
|------|----------|----------|
| `/init` | 初始化项目并创建 `CLAUDE.md` | 新项目开始，团队标准化 |
| `/memory` | 编辑项目记忆文件 | 项目文档更新，上下文优化 |
| `/add-dir` | 添加额外工作目录 | 多模块项目，跨目录操作 |
| `/clear` | 清除对话历史 | 重新开始，节省 token |
| `/compact [instructions]` | 压缩对话历史 | 长对话优化，上下文管理 |

### 开发与调试工具

核心的开发辅助命令，提升日常编码效率：

| 命令 | 功能描述 | 使用场景 |
|------|----------|----------|
| `/review` | 请求代码审查 | 代码质量保证，同行评审 |
| `/bug` | 报告问题给 Anthropic | 问题反馈，产品改进 |
| `/doctor` | 检查安装健康状态 | 环境诊断，故障排查 |
| `/pr_comments` | 查看拉取请求评论 | 代码评审流程，团队协作 |
| `/vim` | 进入 vim 编辑模式 | 高效文本编辑，键盘操作 |

### 监控与分析

帮助你了解使用情况和优化工作流：

| 命令 | 功能描述 | 使用场景 |
|------|----------|----------|
| `/cost` | 显示 token 使用统计 | 成本监控，使用优化 |
| `/help` | 获取帮助信息 | 学习使用，功能发现 |

## 自定义斜杠命令

自定义斜杠命令是 Claude Code 最强大的特性之一，它让你能够将任何复杂的开发流程封装成简单的命令。这种能力不仅提升了个人效率，更重要的是能够在团队中标准化和共享最佳实践。

### 命令作用域

自定义命令采用了分层架构，支持两种作用域：

```md
项目命令 (.claude/commands/)     个人命令 (~/.claude/commands/)
        ↓                              ↓
   /project:command                /user:command
        ↓                              ↓
   团队共享，版本控制              个人定制，跨项目复用
```

此外，你还可以通过目录结构创建命名空间，实现命令的逻辑分组：

```bash
.claude/commands/
├── frontend/
│   ├── component.md        # /project:frontend:component
│   ├── style-guide.md      # /project:frontend:style-guide
│   └── testing.md          # /project:frontend:testing
├── backend/
│   ├── api-design.md       # /project:backend:api-design
│   ├── database.md         # /project:backend:database
│   └── security.md         # /project:backend:security
└── devops/
    ├── deploy.md           # /project:devops:deploy
    ├── monitoring.md       # /project:devops:monitoring
    └── backup.md           # /project:devops:backup
```

这种组织方式让大型项目的命令管理变得井然有序，团队成员可以快速找到所需的命令。

### 参数传递

使用 `$ARGUMENTS` 占位符传入参数，支持复杂的参数传递模式：

```markdown
---
description: 智能代码重构工具
allowed-tools: Read, Edit, Bash(git*)
---

# 重构任务：$ARGUMENTS

## 重构策略

根据传入的参数类型执行不同的重构策略：

** 如果是文件路径 **：分析文件结构，提供重构建议
** 如果是函数名 **：查找函数定义，优化实现逻辑
** 如果是模块名 **：审查模块接口，改进 API 设计

## 执行前检查

当前工作区状态：!`git status --porcelain`
代码覆盖率：!`npm run test:coverage 2>/dev/null | grep -E '[0-9]+%' || echo "无测试覆盖率数据"`

## 安全保障

- 自动创建备份分支
- 执行测试验证重构结果
- 提供回滚方案
```

### 上下文感知机制

通过预执行命令和文件引用，命令能够智能地理解当前开发环境：

```markdown
---
description: 智能问题诊断工具
allowed-tools: Bash(*), Read, Grep
---

# 问题诊断：$ARGUMENTS

## 环境信息收集

** 系统环境 **：
- Node.js 版本：!`node --version`
- NPM 版本：!`npm --version`
- Git 状态：!`git status --short`

** 项目状态 **：
- 包信息：@package.json
- 配置文件：@.env.example
- 最近错误日志：!`tail -20 logs/error.log 2>/dev/null || echo "无错误日志"`

** 代码分析 **：
- 依赖检查：!`npm ls --depth=0 2>&1 | grep -E "WARN|ERR" || echo "依赖状态正常"`
- 类型检查：!`npx tsc --noEmit 2>&1 | head -10 || echo "无 TypeScript 错误"`

基于以上信息，请分析问题 "$ARGUMENTS" 的可能原因并提供解决方案。
```

### 实践参考

为了帮助你快速上手自定义斜杠命令，以下提供了几个常用的命令模板，你可以直接使用或根据自己的需求进行调整。

#### 全栈开发命令

```bash
mkdir -p .claude/commands/fullstack
cat > .claude/commands/fullstack/feature.md <<EOF
---
description: 全栈功能开发流程
allowed-tools: Read, Edit, MultiEdit, Bash(*)
---

# 全栈功能开发：$ARGUMENTS

## 开发阶段

### 1. 需求分析
- 功能规格：从产品文档或用户故事中提取需求
- 技术方案：设计 API 接口和数据模型
- 测试策略：定义测试用例和验收标准

### 2. 后端开发
- 数据模型：@src/models/
- API 路由：@src/routes/
- 中间件：@src/middleware/
- 测试用例：@src/tests/

### 3. 前端开发
- 组件设计：@src/components/
- 状态管理：@src/store/
- 页面逻辑：@src/pages/
- 样式实现：@src/styles/

### 4. 集成测试
- API 测试：!`npm run test:api`
- 前端测试：!`npm run test:frontend`
- 端到端测试：!`npm run test:e2e`

## 代码质量保证

** 静态分析 **：
- ESLint 检查：!`npx eslint src/ --format compact`
- 类型检查：!`npx tsc --noEmit`
- 测试覆盖率：!`npm run test:coverage | grep -E "Lines|Functions|Branches"`

请按照以上流程实现功能："$ARGUMENTS"，确保代码质量和测试覆盖率。
EOF
```

#### 安全审查命令

```bash
mkdir -p ~/.claude/commands/security
cat > ~/.claude/commands/security/audit.md <<EOF
---
description: 全面安全审查工具
allowed-tools: Bash(*), Read, Grep
---

# 安全审查：$ARGUMENTS

## 安全检查维度

### 1. 代码安全
** 敏感信息泄露 **：
- 硬编码密钥：!`rg -i "password|secret|key|token" --type js --type ts | head -20`
- 调试信息：!`rg "console\.(log|debug|info)" --type js --type ts | wc -l`

** 输入验证 **：
- SQL 注入风险：!`rg "SELECT.*\$\{|INSERT.*\$\{" --type js --type sql | head -10`
- XSS 风险：!`rg "innerHTML|dangerouslySetInnerHTML" --type js --type tsx | head -10`

### 2. 依赖安全
** 漏洞扫描 **：
- NPM 审计：!`npm audit --audit-level=high`
- 过期依赖：!`npm outdated`

### 3. 配置安全
** 环境配置 **：
- 环境变量：@.env.example
- 配置文件：@config/
- 权限设置：!`find . -name "*.json" -o -name "*.yaml" | xargs grep -l "auth\|permission"`

### 4. 网络安全
**HTTPS 配置 **：!`grep -r "http://" src/ config/ | head -10`
**CORS 设置 **：!`grep -r "cors\|Access-Control" src/ | head -5`

## 安全建议

根据以上检查结果，提供具体的安全改进建议和修复方案。
EOF
```

#### 代码评审命令

```bash
cat > .claude/commands/review/comprehensive.md <<EOF
---
description: 全面代码评审流程
allowed-tools: Bash(git*), Read, Grep, Edit
---

# 代码评审：$ARGUMENTS

## 评审检查清单

### 1. 功能正确性
- [ ] 实现是否符合需求规格
- [ ] 边界条件处理是否完善
- [ ] 错误处理是否健壮
- [ ] 业务逻辑是否正确

### 2. 代码质量
** 可读性 **：
- 命名是否清晰表达意图
- 代码结构是否逻辑清晰
- 注释是否恰当和准确

** 可维护性 **：
- 函数职责是否单一
- 模块耦合度是否合理
- 代码复用是否恰当

### 3. 性能考虑
** 算法效率 **：
- 时间复杂度是否合理
- 空间复杂度是否优化
- 数据结构选择是否恰当

** 资源使用 **：
- 内存使用是否合理
- 网络请求是否优化
- 数据库查询是否高效

### 4. 安全性检查
** 输入验证 **：
- 用户输入是否验证
- SQL 注入风险评估
- XSS 攻击防护

** 权限控制 **：
- 访问权限是否正确
- 敏感操作是否保护
- 数据权限是否隔离

## 变更分析

**Git 变更信息 **：
- 修改文件：!`git diff --name-only HEAD~1 HEAD`
- 代码行数：!`git diff --stat HEAD~1 HEAD`
- 提交信息：!`git log -1 --pretty=format:"%s%n%b"`

** 影响范围分析 **：
- 修改的模块和函数
- 相关测试用例
- 依赖关系影响

## 评审建议

根据以上检查，提供具体的改进建议：
1. ** 必须修改 **：影响功能和安全的问题
2. ** 建议改进 **：代码质量和性能优化
3. ** 可选优化 **：最佳实践和代码风格

## 测试验证

** 自动化测试 **：
- 单元测试：!`npm test -- --testPathPattern=$ARGUMENTS`
- 集成测试：!`npm run test:integration`
- 代码覆盖率：!`npm run test:coverage`

** 手动测试要点 **：
- 功能验证步骤
- 边界条件测试
- 异常场景验证

请对 "$ARGUMENTS" 进行全面的代码评审。
EOF
```

#### 上下文压缩命令

在大型项目和团队环境中，Claude Code 的使用效率直接影响开发体验。通过合理的优化策略和最佳实践，可以显著提升 AI 辅助开发的效果。

```bash
cat > ~/.claude/commands/optimization/context.md << 'EOF'
---
description: 智能上下文管理和优化
---

# 上下文优化：$ARGUMENTS

## 上下文分析

** 对话长度 **：当前对话包含约 X 条消息
**Token 使用 **：预估 token 消耗情况
** 关键信息 **：识别核心讨论内容

## 压缩策略

### 1. 保留关键信息
- ** 项目背景 **：@CLAUDE.md
- ** 当前任务 **：$ARGUMENTS
- ** 重要决策 **：技术选型、架构设计
- ** 待解决问题 **：阻塞问题、技术难点

### 2. 移除冗余内容
- 重复的代码片段
- 已解决的问题讨论
- 过程性的调试信息
- 不相关的话题

### 3. 结构化总结
** 项目状态 **：
- 当前进度
- 完成的功能
- 待开发特性

** 技术栈 **：
- 主要框架和库
- 开发工具配置
- 部署环境

** 约定规范 **：
- 代码风格
- 命名约定
- 文件组织

## 优化建议

基于分析结果，建议在以下时机进行上下文压缩：
- 对话消息超过 50 条
- 讨论主题发生转换
- 开始新的开发阶段
- Token 使用接近限制

使用 `/compact` 命令执行压缩，保留核心上下文信息。
EOF
```

#### 会话状态管理命令

```bash
cat > .claude/commands/session/save-state.md <<EOF
---
description: 保存和恢复会话状态
allowed-tools: Write, Read, Edit
---

# 会话状态管理：$ARGUMENTS

## 状态信息收集

### 当前工作内容
** 主要任务 **：$ARGUMENTS
** 进度状态 **：[进行中 / 已完成 / 待开始]
** 完成度 **：X%

### 技术上下文
** 项目信息 **：
- 项目类型：@package.json
- 主要依赖：当前使用的框架和库
- 开发环境：Node.js, Python, etc.

** 代码状态 **：
- 工作分支：!`git branch --show-current`
- 未提交更改：!`git status --porcelain`
- 最近提交：!`git log -3 --oneline`

### 决策记录
** 技术决策 **：
- 已选择的技术方案
- 架构设计决策
- 重要配置选择

** 待解决问题 **：
- 当前阻塞问题
- 需要讨论的技术点
- 优化改进计划

## 状态保存

将状态信息保存到 .claude/session-state.md：

"""
# 会话状态 - $(date +%Y-%m-%d)

## 当前任务
$ARGUMENTS

## 项目上下文
[项目基本信息]

## 工作进度
- [x] 已完成项目 1
- [ ] 进行中项目 2
- [ ] 待开始项目 3

## 技术决策
1. 选择 React + TypeScript 作为前端技术栈
2. 使用 Express.js 构建 API 服务
3. 采用 PostgreSQL 作为主数据库

## 待解决问题
1. 用户认证方案设计
2. 数据库性能优化
3. 前端状态管理选型

## 下次会话计划
1. 完成用户认证模块
2. 实现 API 接口
3. 编写单元测试
"""

## 恢复建议

下次会话开始时：

1. 阅读 `.claude/session-state.md` 了解上下文
2. 检查 git 状态确认代码变更
3. 继续未完成的任务
4. 更新会话状态
EOF
```

## 访问控制

自定义斜杠命令的强大能力同时也带来了安全风险。合理的访问控制配置是保护系统安全的重要措施。

**权限最小化原则**：

- 仅授予必要的工具权限
- 限制文件系统访问范围
- 控制网络访问权限

**命令权限配置**：

```yaml
# 严格权限示例
allowed-tools:
  - Read(src/**, tests/**)      # 只读源码和测试
  - Bash(git status, git log)   # 限制 git 命令
  - Edit(src/components/**)     # 限制编辑范围
```

## 结语

Claude Code 的斜杠命令让开发者能够专注于创造性工作，而将重复性任务交给 AI 智能体来处理，在 Vibe Coding 的基础上不仅提升了开发效率，更为代码质量提供了可靠性保障。

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
