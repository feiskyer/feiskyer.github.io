---
title: "十个顶级 Claude Code Skills，装上就不想卸"
date: 2026-03-12T10:00:00+08:00
draft: false
tags: [Claude Code, Skills, AI 编程]
description: "精选十个真正改变工作方式的 Claude Code Skills 和 Plugin，包括 Superpowers、Planning with Files、UI UX Pro Max、Code Review、Ralph Loop、MCP Builder 等，每个都附安装命令和实际使用体验。"
---

用 Claude Code 大半年了，Skills 和 Plugin 装了几十个，删了一半，留下来的都是真正改变了我工作方式的。这篇就挑十个我用得最多、也觉得最值得推荐的，每个都附安装命令，拿去直接用。

先简单说下 Skill 和 Plugin 的区别。Skill 是一个包含 SKILL.md 的文件夹，教 Claude 怎么做某类任务；Plugin 更完整，可以打包命令、SubAgent、Hook 和 MCP 服务器。不过对使用者来说差不多，下面就不区分了。

## Superpowers

如果只能装一个，我选这个。

Superpowers 打包了 20 多个可组合的 Skill，覆盖软件开发的完整流程。brainstorming、TDD、代码审查、Git 提交，每个环节都有对应的 Skill 来约束 Claude 的行为。

我用得最多的是 brainstorming。装了之后，Claude 不会拿到需求就直接开写，而是先问你一轮问题，探索不同方案，把设计决策摊开讨论，最后生成一份设计文档存到本地。看似慢了，实际上能省掉后面大量返工。你会发现很多问题在讨论阶段就暴露了，而不是写了三百行代码之后才发现方向不对。

另一个常用的是 TDD 工作流。它会强制 Claude 先写测试再写实现，跑不过就继续改，直到全绿。Claude 的默认行为是直接写代码然后告诉你“应该没问题”，有了这个约束差别非常大。

当然，20 多个 Skill 全开可能有点重。我一般只启用 brainstorming 和 TDD 两个，其他的按需打开。

```bash
claude plugin install superpowers
```

> GitHub: <https://github.com/obra/superpowers>

## Planning with Files

Claude Code 自带的 Plan Mode 有个让人头疼的问题：规划存在对话上下文里，上下文一压缩就丢了。长任务做到一半，Claude 忘了自己在干嘛。又从头开始。

Planning with Files 把规划、进度和知识都写进 Markdown 文件。Claude 开始干活前先创建计划文件，每完成一步就更新进度，遇到有用的信息就记到知识文件里。文件在磁盘上就不会丢，即使上下文被压缩了也能恢复状态。

这个思路其实来自 Manus。Manus 在复杂任务上表现好，核心原因之一就是中间状态都持久化了。Planning with Files 算是社区版的实现。

```bash
claude plugin marketplace add OthmanAdi/planning-with-files
claude plugin install planning-with-files
```

> GitHub: <https://github.com/OthmanAdi/planning-with-files>

## UI UX Pro Max

让 Claude 写前端页面，出来的东西大都长一个样。紫色渐变背景，圆角卡片，居中布局，也就是典型的 “AI 审美”。

Anthropic 官方有个 frontend-design Skill 能改善一些，但 UI UX Pro Max 做得更彻底。它内置了 67 种 UI 风格和 161 套行业配色方案，根据你的项目类型自动推荐设计系统，从配色到排版到交互模式，一步到位。我试着让它做一个 SaaS 后台的 dashboard，选了 Bento Grid 风格，出来的效果比 Claude 默认的好太多，至少看起来不像 AI 做的了。

技术栈方面，React、Vue、Svelte、SwiftUI、Flutter 这些都支持，不只是 Web。

```bash
claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
claude plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

> GitHub: <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>

聊完前端设计，下一个自然要聊的就是代码质量了。

## Code Review

这是官方 Plugin 里我觉得设计最精巧的一个。

它不是让一个 Claude 从头到尾看代码，而是启动多个 Agent 并行审查同一个 PR。有的看逻辑正确性，有的看安全漏洞，有的看代码风格。每个 Agent 给出的问题都带置信度分数，最后按分数过滤，只保留高置信度的反馈。

为什么要搞这么复杂？因为 AI 代码审查最大的问题是假阳性太多。以前让 Claude 审代码，它总能挑出一堆潜在问题，看着很认真，但大部分都是过度谨慎的废话。有了置信度过滤之后，留下来的基本都值得看一看。

不过使用时要注意，大 PR 跑起来 token 消耗挺猛的，好几个 Agent 同时跑，一次 review 吃掉的 token 可能比写代码本身还多。小 PR 用着挺舒服，大 PR 建议先拆再审。

```bash
claude plugin install code-review
```

> GitHub: <https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review>

## Code Simplifier

写代码的时候容易堆逻辑，写完跑通了就不想再碰了。Code Simplifier 帮你做那个“写完再看一遍”的事情。

它聚焦最近修改过的代码，检查重复逻辑、多余的中间变量、可以合并的条件分支。不改功能，只做简化。上次我写了一段数据处理的逻辑，里面有三段几乎一样的错误处理，跑完 Code Simplifier 它给合并成了一个通用函数，代码量少了三分之一。

```bash
claude plugin install code-simplifier
```

> GitHub: <https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-simplifier>

## Webapp Testing

前端写完了，测试怎么办？手动点来点去太慢，写 Playwright 脚本又太繁琐。这个 Skill 把过程自动化了：你告诉 Claude 要测什么场景，它自己用 Playwright 写脚本、启动浏览器、跑测试、截屏，有问题还会自己调试。跟前面的 UI UX Pro Max 搭配起来特别顺手。

```bash
claude plugin marketplace add anthropics/skills
claude plugin install example-skills@anthropic-agent-skills
```

> GitHub: <https://github.com/anthropics/skills/tree/main/skills/webapp-testing>

## Ralph Loop

名字来自辛普森动画里的 Ralph Wiggum，Anthropic 工程师 Daisy Hollman 做的。通过 Stop Hook 拦截 Claude 的退出，把同一个任务重新喂给它。

Claude Code 有个习惯：做到一半觉得差不多了就停下来说“我已经完成了基础框架，你可以在此基础上继续”。Ralph Loop 不让它停。Claude 试图退出，Hook 拦截，检查完成条件，没满足就塞回去。循环往复，直到真正做完。

简单粗暴，但真的管用。

用这个有个关键技巧：完成条件要写得越具体越好。做完这个功能不行，Claude 会自己说服自己已经完成了。要写“所有 CRUD 端点可用，测试覆盖率超过 80% ，README 包含 API 文档，完成后输出 COMPLETE”。条件越模糊，它越会找理由提前收工。

```bash
claude plugin install ralph-loop

# 使用示例
/ralph-loop:ralph-loop "实现用户认证模块。完成标准：JWT 登录注册、测试通过、README 更新。完成后输出 COMPLETE" --max-iterations 20 --completion-promise "COMPLETE"
```

> 更好详细例子可以参考: <https://awesomeclaude.ai/ralph-wiggum>

## MCP Builder

MCP 这个协议最近讨论度挺高，但真要从零写一个 MCP Server，门槛还是不低。MCP Builder 把构建过程拆成了四个阶段，引导 Claude 一步步完成：理解 API、设计工具接口、实现、测试。

用它的体验比直接让 Claude “帮我写一个 MCP Server”好很多。直接写的话 Claude 经常漏掉 rate limiting 和 token 过期处理等等之类边界情况，用了 MCP Builder 之后这些它都会主动考虑。

```bash
claude plugin marketplace add anthropics/skills
claude plugin install example-skills@anthropic-agent-skills
```

> GitHub: <https://github.com/anthropics/skills/tree/main/skills/mcp-builder>

## PPTX

做 PPT 大概是程序员最不想做的事。

这个 Skill 让 Claude 直接生成 `.pptx` 文件，支持母版、图表、动画。说实话，生成的 PPT 不可能直接拿去做重要汇报，内容、排版和配色都还需要适当调整。但用它生成初稿已经完全够用了，可以大大节省 PPT 得创作时间。

它解决的是“从零开始太痛苦”的问题。起点有了，后面就快了。

```bash
claude plugin marketplace add anthropics/skills
claude plugin install document-skills@anthropic-agent-skills
```

> GitHub: <https://github.com/anthropics/skills/tree/main/skills/pptx>

## Skill Creator

最后一个放 meta 的。Skill Creator 是 Anthropic 官方出的，用来帮你创建新的 Skill 的技能。

之前我写过一篇文章聊它的更新（《写 Claude Skill 最大的盲区，Anthropic 终于帮你补上了》），核心变化是加了 eval 测试框架。现在你可以给 Skill 写测试用例，验证它到底有没有在起作用，还能做 A/B 对比，有 Skill 和没 Skill 的效果差多少，看数据说话而不是凭感觉。

上面九个用完了觉得不够？那就自己造。

```bash
claude plugin install skill-creator
```

> GitHub: <https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator>

---

选 Skill 跟选工具一样，不在多，在合适。装太多互相打架，反而会影响整体的性能，并且上下文也吃不消，所以精选几个足够用即可。

另外，对不同功能的 Skills，特别是仅跟项目相关的 Skills，推荐放到项目中，提交到 Git，即方便了管理和团队共享，还节省了其他项目的上下文空间。

---

相关资源：

- Anthropic 官方 Skills 仓库：<https://github.com/anthropics/skills>
- Anthropic 官方 Plugins 仓库：<https://github.com/anthropics/claude-plugins-official>
- Awesome Claude Skills 社区列表：<https://github.com/travisvn/awesome-claude-skills>
- Claude Code Skills 文档：<https://code.claude.com/docs/en/skills>
- Skills 市场：<https://skillsmp.com/>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
