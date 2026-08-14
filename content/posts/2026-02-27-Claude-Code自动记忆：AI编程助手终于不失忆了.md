---
title: "Claude Code 自动记忆：AI 编程助手终于不失忆了"
date: 2026-02-27T10:00:00+08:00
draft: false
tags: [Claude Code, AI 编程, 自动记忆, Auto Memory, 开发工具, 效率工具]
description: "Claude Code 正式推出 auto-memory 自动记忆功能，可跨 session 记住项目上下文、调试习惯和偏好。本文拆解其工作机制、系统提示词、/memory 命令与 CLAUDE.md 的互补关系及使用注意事项。"
---

用 Claude Code 做过稍微复杂点的项目的人，应该都有一个共同的经验：新开 Session 后，第一件事不是写代码，而是提供 Context：这个项目是什么，用的什么架构，测试环境有哪些坑，之前约定的命名规范是什么等等。

这些背景情况交代完，快的也要五分钟，慢的可能要十几分钟。然后 Claude Code 说“好的，我理解了”，才终于能开始干活。

这个问题确实让人有点烦。开源社区也有很多人试图通过外挂记忆的方式来解决这个问题，但实际体验都不太好。比如 claude-mem 试图通过捕捉工具使用情况自动生成语义摘要，并把相关信息带到未来会话中。看起来很美好，但实际用起来问题一大堆，安装/依赖复杂不说，内存占用高，查询巨慢，稳定性还极差。

这样的痛点 Claude Code 作者自然也早就看到了。刚刚，Anthropic 工程师 Thariq 发了条公告：Claude Code 正式推出了 auto-memory 功能。简单说，Claude Code 现在能跨 session 记住东西了。你的项目上下文、调试习惯、偏好的解决方案，下次开新会话时自动调取，不需要你手动写任何东西。

## Auto Memory 是怎么工作的

机制不复杂。

Claude Code 在你编程过程中，会自动把它认为值得记住的东西写进一个本地文件：

```
~/.claude/projects/<project-hash>/memory/MEMORY.md
```

记什么、怎么记？我扒了一下它的系统提示词，完整内容如下：

```markdown
# auto memory

You have a persistent auto memory directory at
`~/.claude/projects/<project-hash>/memory/`.
Its contents persist across conversations.
As you work, consult your memory files to build on previous experience.

## How to save memories:
- Organize memory semantically by topic, not chronologically
- Use the Write and Edit tools to update your memory files
- MEMORY.md is always loaded into your conversation context
  — lines after 200 will be truncated, so keep it concise
- Create separate topic files (e.g., debugging.md, patterns.md)
  for detailed notes and link to them from MEMORY.md
- Update or remove memories that turn out to be wrong or outdated
- Do not write duplicate memories. First check if there is an
  existing memory you can update before writing a new one.

## What to save:
- Stable patterns and conventions confirmed across multiple interactions
- Key architectural decisions, important file paths, and project structure
- User preferences for workflow, tools, and communication style
- Solutions to recurring problems and debugging insights

## What NOT to save:
- Session-specific context (current task details, in-progress work)
- Information that might be incomplete
  — verify against project docs before writing
- Anything that duplicates or contradicts existing CLAUDE.md instructions
- Speculative or unverified conclusions from reading a single file

## Explicit user requests:
- When the user asks you to remember something across sessions
  (e.g., “always use bun”, “never auto-commit”), save it
  — no need to wait for multiple interactions
- When the user asks to forget or stop remembering something,
  find and remove the relevant entries from your memory files
```

这里有几个值得注意的设计：

memory 不只是一个文件。MEMORY.md 是主文件，前 200 行自动加载到 prompt 里。但 Claude code 还可以创建 `debugging.md`、`patterns.md` 这样的主题文件，从 MEMORY.md 链接过去，需要的时候再读取。这有点像一本带着索引页的笔记本，翻到某个主题再看详细内容。

“What NOT to save”这段我觉得挺克制的。大多数人做记忆功能，恨不得什么都往里塞。Anthropic 反过来，先画了条线说哪些东西别碰：临时状态不记、没验证的不记、CLAUDE.md 里已有的不重复记、只看了一个文件就猜的结论不记。

还有”Explicit user requests”那段也挺实用：你可以直接告诉 Claude  以后都用 bun 装依赖或者永远不要自动 commit，它会立刻写进 memory，不需要等多次交互才总结。反过来你说别再记这个了，它也会去找到对应条目删掉。

另外，内存文件存在本地，按项目哈希值隔离。不会上传到云端，不同项目之间也完全独立。

## /memory 命令

内存功能的控制中心是 `/memory` 命令。

打开它，你能看到 Claude Code 自己记录的所有内容，可以编辑某一条，可以删掉觉得没用的，也可以整个关掉这个功能。

这个设计我觉得也挺实用的。Claude Code 的判断不一定都准确，它可能觉得某个临时的 debug 方案很重要。但那只是你一次性的权宜之计，没必要永久保留。透明可控，比黑盒记忆要放心得多。

当然，如果你实在不想开启自动记忆，也可以一行命令搞定：

```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

## 跟 CLAUDE.md 什么关系

用 Claude Code 一段时间的人，大概都写过 CLAUDE.md。你把项目规范、禁止行为、常用命令写在里面，所有会话都生效。

Auto Memory 和 CLAUDE.md 是两件不同的事，完全互补，互不覆盖。

CLAUDE.md 是你主动写给 Claude Code 的规则，记录那些你希望它每次都记住的、不变的约定。Auto Memory 不一样，它是 Claude Code 自己在工作过程中积累的观察，比如项目模式、你的习惯、踩过的坑等等。

两个配合起来的效果最好。可以这样理解：CLAUDE.md 是你写的入职手册，Auto Memory 是它自己记的工作笔记。新员工到岗，先读手册，再翻笔记，然后才真正上手。

## 几个需要提前知道的问题

说实话，功能本身的设计我觉得没什么可挑的，零配置、透明可控、跟 CLAUDE.md 互补。不过用的时候有几个地方需要注意。

200 行的限制，大项目用久了会碰到天花板。目前的实现是简单的前缀加载，也就是取文件开头 200 行塞进 prompt。不像向量数据库那样能按相关性检索，它就是按顺序读。所以如果 memory 文件积累得多了，靠后的内容实际上不会被加载。

需要养成用 `/memory` 定期整理的习惯，留重要的，删过时的。就像清理浏览器书签，不主动管理就会越来越乱。

另一个问题是过期的记忆。不是所有记下来的东西都应该永久保留。比如你两个月前用了某个临时方案处理一个 bug，现在早就改了。但 Claude 还惦记着旧方案，下次遇到类似问题，再优先往那个方向想就不对了。陈旧的记忆有时候比没有记忆更麻烦。

官方还没给出自动过期或 decay 机制，所以现在还得完全靠手动管理。

不过换个角度想，Anthropic 的选择挺有意思。不用向量数据库，不做复杂的检索增强，就是本地的 Markdown 文件。这跟 Claude Code 一贯的设计哲学一脉相承，能用简单方案解决的，就别上复杂架构。先跑起来，不够再迭代。

## 说说我自己的感受

功能发布之前，我处理这个问题的方式是：在 CLAUDE.md 里手动把关键的项目背景写进去，然后还要在每次新 session 的第一条消息里补充这次的具体任务背景。

两件事加起来，我其实是在替 Claude Code 充当记忆介质。

比如，有次跑一个长任务，Claude Code 花了大半个小时梳理项目的测试文件。找出了几个有问题的查询接口，还整理出一套处理边界情况的思路。然后上下文窗口到了临界点，触发了自动压缩。下一个 session 接手时，那一套思路就不见了，从头开始分析，之前做的工作重复做了一大半。那半个小时基本白费了。

Auto Memory 解决的就是这类问题。Claude Code 在工作过程中发现的有价值的东西，不应该在 session 结束时消失。

多 Agent 协作的场景里，这个功能的价值可能会更明显一些。一个 Agent 发现了某种边界情况的处理方式，把它写进 memory。下一个 Agent 一开始就能读到，不需要上一个专门提醒。

## 写在最后

看到 Claude Code 的 Auto Memory，我第一时间想到的是 OpenClaw 的内存设计。

OpenClaw 能两周冲到 10 万星，原因很多，但持久记忆绝对是核心卖点之一。它不只是一个聊聊天就忘的机器人，而是能记住你说过的每一件事，下次提起来直接就知道上下文。这个体验差异太大了，用过的人都回不去。OpenClaw 甚至在 Markdown 记忆之上还加了向量搜索，做成了混合检索，相当于给 Agent 内置了一套 RAG 系统。

Claude Code 的 Auto Memory 走的是更简单的路线：纯本地 Markdown 文件，前 200 行前缀加载，没有向量检索。从功能完备度来说，跟 OpenClaw 的记忆系统还有很大差距。但 Anthropic 的做法一贯如此。先用最简单的方案把核心体验跑通，不够再迭代。

我比较期待的是下一步。200 行的前缀加载很快会碰到天花板，到时候大概率会引入某种形式的语义检索。如果再加上自动过期和记忆质量评估，Claude Code 的记忆系统就真的能跟 OpenClaw 掰手腕了。

---

相关链接：

- Auto Memory 官方文档：<https://code.claude.com/docs/en/memory>
- Thariq 的公告：<https://x.com/trq212>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
