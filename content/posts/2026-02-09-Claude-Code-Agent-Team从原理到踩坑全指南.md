---
title: "Claude Code 多 Agent 组队开发：从原理到踩坑全指南"
date: 2026-02-09T10:00:00+08:00
draft: false
tags: [AI, Claude Code, Agent Team, 多Agent, AI Agent, 协作开发]
description: "深入解析 Claude Code 的 Agent Team 多 Agent 组队开发功能，从系统提示词原理到快速上手、Delegate Mode、Plan Approval 等进阶技巧，并总结文件冲突、Token 消耗、会话恢复等实战踩坑经验与避坑指南。"
---

大多数人用 AI 编程助手，还是一对一模式，也就是你发指令，AI 写代码，来回对话直到任务完成。但实际上，随着 Kimi K2.5 以及 Claude Opus 4.6 的发布，AI 已经学会组队了。

比如，Anthropic 发布的 Agent Team 功能，可以让多个 Claude Code 实例可以像真正的开发团队一样并行协作。一个 Agent 当技术负责人，负责规划和分配任务；其他 Agent 当开发组员，各自拿着独立的上下文窗口埋头干活。

这几天也在密集体验了这个功能，并且深挖了它背后的系统提示词设计。今天的文章就从原理到实战到踩坑，把 Agent Team 这件事讲清楚。

## 一句话理解 Agent Team

你可以把 Agent Team 想象成一个软件开发团队的分布式架构。

* 以前是单体应用，一个 Claude Code 单线程干所有事情，上下文窗口就是它的内存，窗口满了就得压缩（当然压缩就意味着丢掉某些信息）。
* 现在是微服务，一个 Lead Agent 当负责人，多个 Teammate Agent 当专业工程师。每个 Teammate 有自己的独立上下文窗口，互不干扰，但可以通过消息系统通信，并通过共享任务列表协调进度。

Agent Team 的好处很明显，每个 Agent 的上下文窗口更聚焦单个任务，可以更专注地处理自己负责的部分；并行多个 Agent 执行也大大加快了整体任务的推进速度。

Agent Team 乍看起来跟 SubAgent 比较像，但一用起来就可以发现它们明显不一样：SubAgent 只能向主 Agent 汇报结果，相互之间不能通信；而 Teammate Agent 则可以互相直接通信，用户也可以直接跟任何一个 Teammate Agent 对话。它们的详细对比如下表格所示：

| 维度 | SubAgent | Agent Team |
|------|----------|------------|
| 上下文 | 独立窗口，结果回传给调用者 | 独立窗口，完全独立 |
| 通信 | 只能向主 Agent 报告 | Teammate 之间可以直接通信 |
| 协调 | 主 Agent 管理所有工作 | 共享任务列表，可自行领取任务 |
| 适合场景 | 聚焦型任务，只需要结果 | 需要讨论、协作和互相挑战的复杂任务 |
| Token 消耗 | 较低（结果摘要回传） | 较高（每个 Teammate 独立 Claude 实例） |

## Agent Team 的架构设计

我相信你已经看过不少关于 Agent Team 的文档了，但它们大多停留在功能介绍层面。这里我换个角度，直接看它的系统提示词，从底层分析 Anthropic 是怎么设计这套多 Agent 协作机制的。

![Agent Team 架构原理图](/images/2026-02-09-Claude-Code-Agent-Team-2026-02-09-agent-team-architectu.png)

如图所示，整个 Agent Team 由四个核心部分组成：

### Team Lead（团队负责人）

Team Lead 就是你正在交互的那个主 Claude Code 会话。它通过 `TeamCreate` 工具创建团队，通过 `Task` 工具创建 Teammate，通过 `SendMessage` 工具发消息，通过 `TaskCreate`/`TaskUpdate` 管理任务列表。

从系统提示词来看，Anthropic 对 Lead 的定位就是管理 Agent 团队（或者叫 Agent 集群）：

> Use this tool proactively whenever the user explicitly asks to use a team, swarm, or group of agents, or a task is complex enough that it would benefit from parallel work.

注意这里有个 proactively，这说明 Lead 会主动判断任务是否值得开团队，而不总是等着你明确要求。

### Teammate（团队成员）

每个 Teammate 是一个完全独立的 Claude Code 实例。它们在创建时会加载项目的 CLAUDE.md、MCP servers 和 Skills，但不会继承 Lead 的对话历史。这是个有意思的取舍，用上下文隔离换来了团队成员的执行效率。

系统提示词中有一条关键规则：

> IMPORTANT for teammates: Your plain text output is NOT visible to the team lead or other teammates. To communicate with anyone on your team, you MUST use the SendMessage tool.

这里说明，Teammate 的独白不会被任何人看到，必须通过消息工具显式通信。这就像一个开发团队里，你在自己电脑上嘟囔的话同事听不到，得发 Slack 消息才行。

### Task List（共享任务列表）

任务列表存储在 `~/.claude/tasks/{team-name}/` 目录下，所有成员都可以访问。任务有三种状态：pending、in_progress、completed。任务之间可以设置依赖关系，被依赖的任务没完成时，下游任务就不能被领取。

系统提示词里对任务协调有明确的指导：

> Teammates should check TaskList periodically, especially after completing each task. Claim unassigned, unblocked tasks with TaskUpdate. Prefer tasks in ID order (lowest ID first).

任务领取用的是文件锁机制来防止竞争条件，确保多个 Teammate 同时抢同一个任务时不会冲突。

### Mailbox（消息系统）

通信机制支持三种消息类型：

- `message`：点对点私信，发给特定 Teammate；
- `broadcast`：广播消息，发给所有人，成本较高（Broadcasting is expensive. N teammates = N separate message deliveries）；
- `shutdown_request` / `shutdown_response`：优雅关停协议，Teammate 可以拒绝关停（比如“我还在处理任务 #3”）。

这里还有一个很重要的设计：`plan_approval_response`。Lead 可以要求 Teammate 在做之前先写计划，Lead 审批通过后才允许执行，进一步保证了 Teammate 任务执行的质量。

## 快速上手

Agent Team 目前还是实验性功能，默认关闭。想要开启，需要在 `~/.claude/settings.json` 中添加：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

或者直接设置环境变量：

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### 你的第一个 Agent Team

启用后不需要学任何新命令。直接用自然语言告诉 Claude Code 你想要一个团队：

```
创建一个 Agent Team 来审查 PR #142。
三个审查员分别从安全、性能、测试覆盖率三个角度审查，
最后综合出一份报告。
```

Claude Code 会自动创建团队、分配任务、等待结果、综合报告。整个过程你只需要发一条消息。

### 选择显示模式

Agent Team 支持两种显示模式：

- in-process 模式（默认）：所有 Teammate 运行在主终端内。用 `Shift+Up/Down` 切换 Teammate，直接跟任何一个对话。这种模式比较通用，能在任何终端中使用。
- split-pane 模式：每个 Teammate 独占一个终端面板。需要 tmux 或 iTerm2。

我个人建议先用默认的 in-process 模式入门，等熟悉了再考虑 split-pane。split-pane 看起来很酷，多个面板同时输出，但不支持 VS Code 内置终端、Windows Terminal 和 Ghostty 等等。

### 一个实际的使用场景

比如你想重构一个模块，可以这样分配：

```
创建一个 3 人团队来重构 src/auth/ 模块：
- 一个 Teammate 负责重构核心认证逻辑
- 一个 Teammate 负责更新所有相关测试
- 一个 Teammate 负责更新 API 文档
每个人只改自己负责的文件，不要动其他人的代码。
```

注意最后的“每个人只改自己负责的文件”，这句不可缺少。后面也会讲到，文件冲突是 Agent Team 最大的坑。

## 进阶技巧

### Delegate Mode：让 Lead 专注当项目经理

默认情况下，Lead 会忍不住自己动手写代码。这就像一个技术 Lead 说好了只做 code review，结果控制不住就自己上手改了。

解决方法是按 `Shift+Tab` 切换到 Delegate Mode。在这个模式下，Lead 只能使用协调类工具，不能读写文件、执行命令，强制它做一个纯粹的管理者。

### Plan Approval：先审方案再执行

对于高风险任务，可以要求 Teammate 先写方案：

```
spawn 一个架构师 Teammate 来重构数据库层。
要求它先写方案，我审批后再动手。
```

Teammate 会进入 plan mode，用只读工具探索代码库、设计方案。方案完成后发给 Lead 审批。Lead 可以批准或驳回并附上反馈。Teammate 收到反馈后修改方案，重新提交。

### 用 Hooks 做质量门禁

Claude Code 的 Hooks 机制可以用来在 Agent Team 中强制执行质量标准：

- `TeammateIdle` Hook：Teammate 准备空闲时触发。如果 exit code 为 2，会发送反馈让 Teammate 继续工作。可以用来检查测试是否通过、代码是否 lint 干净等。
- `TaskCompleted` Hook：任务被标记完成时触发。Exit code 2 阻止完成并发送反馈。可以用来做自动化的完成标准检查。

### 直接跟 Teammate 对话

每个 Teammate 都是完整的 Claude Code session。你可以随时绕过 Lead，直接跟任何 Teammate 对话：

- in-process 模式：`Shift+Up/Down` 选择 Teammate，输入消息；
- split-pane 模式：直接点击对应的面板对话。

这在 Teammate 跑偏时特别有用，直接纠正它，不需要通过 Lead 传话。

## 避坑指南

Agent Team 毕竟才刚刚发布，还有不少问题。以下是几个我碰到的踩坑经验，供你在使用时参考。

### 文件冲突是最大的坑

多个 Teammate 同时编辑相同文件，导致文件内容覆盖丢失，这是最容易碰到的问题。这个问题是因为 Agent Team 的任务列表有文件锁，但文件写入本身没有锁机制。

解决的思路是在分配任务时划清文件所有权。比如 Teammate A 只改 `src/auth/`，Teammate B 只改 `tests/auth/`，绝不交叉。用任务依赖确保共享文件只有一个写入者。这也是为什么前面那个重构例子里特别强调每个人只改自己负责的文件。

### Lead 和 Teammate 都可能失控

Lead 有个毛病，会忍不住自己动手写代码，不愿意把活分给 Teammate。解决方法是用 Delegate Mode（`Shift+Tab`）强制限制它只能做协调，或者在提示词中明确说“你不要自己写代码”。

Teammate 则容易跑偏。比如让它只审查安全问题，结果它顺手重构了代码风格；或者让它改测试，结果它跑去改了实现代码。这个问题实际上一直都是 Claude 模型的问题，缓解方法是 PLAN 先审方案再执行：

```md
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

另外，在后续执行过程中发现跑偏了也要及时纠正。这个要人眼来盯着了，所以任务颗粒度最好不要过大。

### Token 消耗不容忽视

每个 Teammate 是独立 Claude 实例，5 人团队约 5 倍 token 消耗，PLAN 模式下更可以达到 7 倍。

建议从 2-3 个 Agent 开始，别上来就开 10+ 个 Agent。可以给 Teammate 用 Sonnet 而不是 Opus（`Create a team with 4 teammates. Use Sonnet for each teammate.`），只在真正需要并行的场景才动用 Agent Team。

### Teammate 的失忆问题

Teammate 只加载 CLAUDE.md、MCP servers 和 Skills，不继承 Lead 的对话历史。它不知道你之前跟 Lead 聊了什么。所以一开始的提示词必须包含充分的上下文。

不要说“继续刚才的工作”，要说审查 src/auth/ 目录下的认证模块，重点关注 JWT token 处理和 session 管理，应用使用 httpOnly cookies 存储 token：

```md
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

更麻烦的是 `/resume` 和 `/rewind` 不能恢复正在运行的 Teammate。会话中断后，Lead 会尝试给已不存在的 Teammate 发消息，只能重新创建。这意味着长时间运行的任务有较高的中断风险，建议拆成较短的分步执行。

### 协调本身的问题

除了 Token，多 Agent 协作还有一些琐碎的协调开销。Teammate 有时候忘记把任务标记为已完成，导致下游任务一直被阻塞，这时候得手动检查或者让 Lead 去催。关停也不是即时的，Teammate 会先完成当前的工具调用才响应关停请求，如果它正在跑测试套件，可能需要等很久。另外 Teammate 的权限请求会通过 Lead 频繁打断你的操作，建议提前在权限设置中批准常用操作。

### 别指望 Agent Team 自觉保证质量

没有验证流程的话，AI Agent 一个常见的问题是声称任务已完成但实际上并没有，而是输出一个差不多的结果就交差了。

解决方法是通过 `TaskCompleted` Hook 添加自动验证，比如要求任务完成时必须测试通过。当然，最重要的是，对关键任务一定要人工审查。

## 什么时候该用，什么时候不该用

| 适合使用 Agent Team | 不适合使用 Agent Team |
|---------------------|----------------------|
| 多角度并行调研/审查 | 简单的单文件编辑 |
| 独立模块的并行开发 | 强依赖的串行任务 |
| 竞争性假设的并行验证 | 同一文件的多处修改 |
| 跨层协调（前端/后端/测试） | 日常的 bug fix |
| Code Review（安全/性能/测试多角度） | Token 预算紧张 |

一个更实用的判断标准是：如果你要做的事情可以自然地拆成 2-3 个互不依赖的子任务，而且每个子任务涉及不同的文件集合，那就适合用 Agent Team。反过来，如果任务本身就是串行的，或者多个步骤都需要改同一批文件，那单会话或 SubAgent 更合适。

如果你是第一次尝试，建议从不需要写代码的研究/审查任务开始。比如让三个 Teammate 从不同角度审查一个 PR，或者让它们分别调研一个技术方案的不同方面。这些任务没有文件冲突的风险，先感受一下多个 Agent 同时干活是什么体验。

## 写在最后

Agent Team 把团队协作这件事搬到了 AI 编程领域，消息系统、任务依赖、文件锁、优雅关停、计划审批这些机制都借鉴了真实的软件开发团队协作经验。Agent Team 一经发布，确实让不少人（包括我自己）感到惊艳，这无疑又是一个重要的 AI Agent 设计范式，估计其他 AI 大厂也要很快跟进了。

但要注意，Agent Team 还在早期阶段，文件冲突、会话恢复、Token 消耗等等问题还待解决，在使用过程中要注意绕开这些坑。你也可以使用 kieranklaassen 发布的 Swarm 编排 SKILL，让 Claude Code 帮你设计编排 Agent Team。

---

相关资源：

- Claude Code Agent Team 官方文档：<https://code.claude.com/docs/en/agent-teams>
- Anthropic Engineering Blog - Building a C compiler：<https://www.anthropic.com/engineering/building-c-compiler>
- Hacker News 讨论帖：<https://news.ycombinator.com/item?id=46743908>
- kieranklaassen 的 Swarm 编排 SKILL：<https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
