---
title: "一个 Claude Skill，解决 AI 编程最头疼的问题"
date: 2025-12-01
tags: [AI, Claude Code, Claude Skill, AI Agent]
draft: false
---

上周我想让 Claude Code 帮我验证一个项目中所有数据查询的问题。虽然它们都散乱在项目的不同位置，但任务本身其实不算复杂，大概涉及 100 多个查询。主要复杂的问题在于失败后的处理：找到正确的数据结构、查询一些数据确认有效字段、汇总查询确认可能取值、最后再去重新构造查询。

任务给了 Claude Code 之后，结果干到一半，它突然就“忘了”之前做的事情，漏掉很多我给它涉及的流程，还有很多查询压根没验证就说任务完成了，

其实这也是困扰很多人的通用问题，即 Claude Code 在长时任务中会碰到记忆丢失、上下文窗口受限以及会话切换丢失任务进度等问题。

## 为什么 AI 会“失忆”

要理解这个问题，得先搞清楚 AI 的“记忆”是怎么工作的。

大模型有一个叫“上下文窗口”的东西，你可以把它理解成 AI 的“工作记忆”。所有的对话历史、代码内容、工具调用结果，都要塞进这个窗口里。窗口满了，老的内容就得丢弃或者主动压缩。

Claude Code 有一个叫 Compaction 的机制，会在窗口快满的时候自动压缩历史内容。听起来挺智能的对吧？问题是，压缩必然会丢失信息。当你的任务需要跨越多个上下文窗口时，每次压缩都像是给 AI 做了一次“部分失忆手术”。

所以，在实际应用中，并不推荐频繁使用 Claude Code 的自动压缩机制。更推荐的方式是把进度写到文件中，再新开会话从这个进度文件继续执行。

## Anthropic 的官方解法

前几天，Anthropic 也发布了一篇研究，专门讨论这个问题。标题叫《Effective harnesses for long-running agents》，翻译过来就是“如何让 Agent 在长时任务中保持高效”。

他们发现，即使是最强的 Opus 模型，在处理长时任务时也会翻车。比如让它“构建一个 claude.ai 的克隆”，跑着跑着就出问题了。典型的问题包括：

**贪多嚼不烂。** Agent 试图一口气完成整个任务，结果在实现到一半时上下文窗口就满了。下一个会话接手时，看到的是一个半成品——功能没完成，文档也没写，只能靠猜来理解之前发生了什么。

**过早宣布胜利。** 当项目已经有了一些进展后，后续的 Agent 实例扫一眼代码，觉得“看起来差不多了”，就直接宣布任务完成。实际上很多功能根本没实现。

![](/images/e033a73e-8666-469b-8b1c-8499041f1426.png)

Anthropic 的解决方案是一个**双 Agent 架构**，如上图所示：

- **Initializer Agent** 在第一个会话中运行，负责分析任务、创建详细的功能清单、搭建项目骨架。
- **Executor Agent** 在后续的每个会话中运行，负责读取上一个会话的进度、选择下一个任务、完成后更新进度。

这个设计的关键在于**用文件来做“记忆载体”**。

Feature List 是一个 JSON 文件，列出所有需要实现的功能，每个功能有“通过/未通过”的状态。Agent 只能改状态，不能删除或修改功能描述。Progress Notes 记录每个会话做了什么、遇到了什么问题、下一步应该做什么。再加上 Git History，每完成一个功能就提交一次。

这样一来，每个“失忆”的新 Agent 都能通过读取这些文件，快速恢复上下文，接着上一个 Agent 的进度继续工作。说白了，就是让 AI 学会“写工作日志”和“交接班”。

Anthropic 还把这套实现开源了，放在 <https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding>，感兴趣的话，你可以去看看它的源码。

## 我把它做成了一个 Skill

看我这篇研究，我就在想能不能把这套方案封装成开箱即用的工具。

Claude Skill 是 Claude Code 的一种扩展机制。通过它，你可以定义一套专门的工作流程，让 Claude Code 按照特定的模式来执行任务。基于 Anthropic 的研究，我开发了一个叫 autonomous-skill 的 Skill，把 Claude Code 作为主代理，在 Skill 内部启动 Headless 模式的 Claude Code 作为执行代理，再通过本地文件同步进度，也就实现了一个长任务的自动执行系统。

![](/images/abbc837f-db06-4097-a071-b5237b5f1aae.png)

在这个 Skill 中，所有任务数据存储在项目根目录的 `.autonomous/<task-name>/` 目录下。

```
project-root/
└── .autonomous/
    └── build-rest-api/
        ├── task_list.md    # 任务清单
        └── progress.md     # 进度日志
```

当你启动一个新任务时，Initializer Agent 会分析你的任务描述，把它拆解成若干个可执行的小任务，按优先级和依赖关系排序，记录到 task_list.md 里。

任务清单长这样。

```markdown
# Task List: Build REST API

## Meta

- Created: 2025-12-01 10:00
- Total Tasks: 25
- Completed: 0/25 (0%)

## Tasks

### Phase 1: Foundation

- [ ] Task 1: 初始化项目结构
- [ ] Task 2: 配置数据库连接
- [ ] Task 3: 创建基础模型

### Phase 2: Core Implementation

- [ ] Task 4: 实现用户认证
- [ ] Task 5: 创建 CRUD 接口
      ...
```

有一条铁律。**任务描述一旦创建，就不能修改或删除。** 只能把 `[ ]` 改成 `[x]`。这是为了防止后续 Agent 作弊——通过删除困难任务来虚假地提高完成率。这个设计我觉得挺妙的。

后续的每个会话都由 Executor Agent 接管。它先读取任务目录，了解当前进度，检查之前的工作是否正常，有没有遗留 bug。找到第一个未完成的任务，执行，测试验证，标记完成，写进度日志，git commit。如果上下文还有空间，继续下一个任务。

每个会话结束后，Autonomous Skill 会检查是否还有未完成的任务。如果有，等待 3 秒后自动启动下一个会话。

这样你可以让 Claude Code 自动跑一整夜，早上醒来检查成果就行了。

## 怎么用

安装很简单，在 Claude Code 里执行两条命令：

```bash
# 添加插件市场源
/plugin marketplace add feiskyer/claude-code-settings

# 安装 autonomous-skill
/plugin install autonomous-skill
```

启动任务的时候，在 Claude Code 中输入类似这样的话。

```
<先开启plan模式，讨论确认你要达成的目标和要实现目标的任务列表>

请使用 autonomous skill 帮我实现刚刚讨论的设计
```

Claude Code 会识别到 autonomous-skill 并自动切换到长时任务模式。

任务运行过程中，你可以到 `.autonomous/` 目录随时查看进度，比如：

```bash
# 查看所有任务
ls .autonomous/

# 查看具体任务进度
cat .autonomous/build-rest-api/task_list.md

# 查看进度日志
cat .autonomous/build-rest-api/progress.md
```

## 几个使用建议

**先设计再执行，任务一定要具体。** 不要把类似“帮我写个 XXX 后端”这样的任务直接交给 Autonomous Skill 执行，而是先开启 plan 模式，讨论好你想要达成的目标、实现的效果以及详细的步骤，然后再去执行。记住，AI 不是你肚子里的蛔虫，给的信息越具体，拆解的任务越合理，最终执行的效果才能越好。

**合理预期任务规模。** 简单任务大概十几二十个子任务，几个会话就能完成。中等任务二三十到五十个子任务，可能需要跑几个小时。

**定期检查进度。** 虽然 autonomous-skill 能自动运行，但建议每隔一段时间看一眼。任务分解是否合理？有没有卡在某个任务上？代码质量是否符合预期？毕竟是 AI 在干活，完全放手不管还是有风险的。

**善用 Git。** autonomous-skill 会自动 git commit，但建议你在任务开始前确保当前分支干净，最好创建一个专门的分支。万一跑出来的东西不满意，还能轻松回滚。

## 写在最后

长时任务一直是 AI 编程助手的痛点。Anthropic 的这篇研究提供了一个挺优雅的解决方案。与其让 AI 强行“记住”所有东西，不如教它学会“写笔记”和“交接班”。

autonomous-skill 把这个方案打包成了开箱即用的工具。它不是银弹，但对于那些需要长时间持续执行的编程任务，它确实让 Claude Code 变得更加可靠。

我自己用了一段时间，体验还不错。项目本身也已经开源在 https://github.com/feiskyer/claude-code-settings。

如果你也受够了 AI 的“失忆症”和不停的手动 Approve，不妨试试这个 Skill。

---

相关链接：

- Effective harnesses for long-running agents https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

- Claude Code Settings Github: https://github.com/feiskyer/claude-code-settings

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
