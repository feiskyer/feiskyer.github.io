---
title: "终于搞明白 Claude Code 为什么会忽略我的指令了"
date: 2026-06-23T10:00:00+08:00
draft: false
tags: [Claude Code, Anthropic, AI 编程, Harness, Skills, Hooks]
description: "Claude Code 忽略指令的根因是上下文膨胀。本文编译 Anthropic 官方指南，讲清 CLAUDE.md、Rules、Skills、Subagents、Hooks、Output Styles 这 7 种引导方法的加载时机、压缩行为与上下文成本，并给出四层分级的实践顺序。"
---

> 题记：本文编译自 Anthropic 工程博客《Steering Claude Code: skills, hooks, subagents and more》，原文链接：<https://www.anthropic.com/engineering/claude-code-best-practices>。本文在翻译基础上做了整理和补充。

在使用 Claude Code 时，我的 CLAUDE.md 曾经写到几千行。项目规范、参考约定、编码风格、部署流程，还有日常开发中碰到的各种坑，全往里面塞。CLAUDE.md 的内容越来越丰富，Claude Code 也越来越好用。直到有一天我发现 Claude Code 开始选择性忽略某些指令，才反应过来，它的上下文太长了，它已经不能很好地遵循 CLAUDE.md 定义的各种规则了。

你是不是也碰到过类似的情况？明明写了“所有修改必须跑完整 e2e 测试”，结果只跑了一个单元测试就停了，需要你反复提示才执行。

我在这个问题上卡了很久，一度怀疑是 Claude 模型又降智了，后来才发现根本原因是上下文膨胀。把所有东西都塞进了 CLAUDE.md，这本身就是用错了 AI 工具。

Anthropic 最近发了一篇官方指南，系统梳理了提示 Claude Code 的 7 种方法和它们的实现原理。我之前踩过的很多坑，根因都是没搞清楚每种方法的加载时机和上下文成本。

下面是我对这篇指南的编译和解读，每一节加了自己的使用经验。

## CLAUDE.md：写得越多，质量越差

CLAUDE.md 是使用 Claude Code 所必需的第一步，所以也就成了大家最先接触、也是最容易写过头的配置方法。它在 Claude Code 会话启动时就加载，全程驻留在上下文空间中。

不过这里有个容易忽略的设计：CLAUDE.md 的写法其实分两种。

第一种，放在项目根目录的 CLAUDE.md 每次会话都加载，压缩后会被重新读取。适合放构建命令、目录结构、团队硬性约定这些 Claude 需要始终知道的信息。

第二种，子目录的 CLAUDE.md（比如 `app/api/CLAUDE.md`）只在 Claude 读到该目录下的文件时才加载。离开这个目录，这些指令就不在上下文里了。

![CLAUDE.md 层级加载示意](/images/2026-06-23-claude-code-steering-claude-md-hierarchy.jpg)

Anthropic 给的建议是：根 CLAUDE.md 控制在 200 行以内，给它一个 owner，像审查代码一样审查对它的修改。

这件事在团队协作的大仓库里尤其明显。CLAUDE.md 很容易变成一个没人维护的公共配置文件，每个组都往里加自己的规范，没人删旧的。

最终每个工程师的每次会话都要加载所有团队的规范，不管跟当前任务有没有关系。

要解决也很简单，在 monorepo 里给每个团队目录配置单独的 CLAUDE.md，让团队只加载自己的规范。还可以用 `claudeMdExcludes` 跳过不相关团队的文件。

总结起来一句话，不要把 CLAUDE.md 当成垃圾桶，而是寸土寸金的黄金地段。能不放的，就别放。

## Rules：按路径触发，不白占上下文

Rules 是 `.claude/rules/` 目录下的 Markdown 文件。

不带路径限定的 Rule 跟根 CLAUDE.md 行为一样：每次会话都会加载、会话压缩后也会重新注入。其实本质上就是换了个目录放的 CLAUDE.md 内容。

真正有意思的是带路径限定的 Rule。给 Rule 加一个 `paths` 字段，它就只在 Claude 碰到匹配路径的文件时才加载：

```yaml
---
paths:
  - "src/api/**"
  - "**/*.handler.ts"
---
所有 API handler 必须用 Zod 校验输入参数.
```

这条规则在你改文档的时候完全不占上下文，只有碰到 API 相关代码才会出现。

所以，凡是只对特定目录或文件类型生效的约束，都应该用 path-scoped Rule，而不是写在 CLAUDE.md 里。这是控制上下文膨胀最直接的手段。

什么时候用 Rule 而不是子目录 CLAUDE.md？当一个约束是跨目录的。比如“所有 `.handler.ts` 文件都要校验输入”，它可能散布在多个目录下，放某一个目录的 CLAUDE.md 里不合适。

## Skills：按需加载，用完即走

Skills 住在 `.claude/skills/` 目录里，每个 Skill 是一个文件夹，核心是一个 `SKILL.md` 文件，里面包含了名称、描述和正文。

Skills 最关键的一个设计时只有名称和描述在会话启动时加载，正文只有在被调用时才进入上下文。

![Skills 触发机制](/images/2026-06-23-claude-code-steering-skills-trigger.jpg)

它的调用方式有两种：通过斜杠命令（比如 `/code-review`），或者 Claude 根据任务自动匹配。

在使用 Skills 的时候，也需要注意会话压缩的行为：压缩时，已调用的 Skills 会被重新注入，但所有 Skills 共享一个总 token 预算。一次会话里调用太多 Skills，最早调用的会被丢掉。

Anthropic 给的原则是：流程性的东西放 Skill，不要放 CLAUDE.md。部署流程、发布检查清单、代码审查规范，这些都应该是 Skill。CLAUDE.md 只放 Claude 需要始终知道的事实。

我自己的经历可也是如此。之前 CLAUDE.md 里写了一大段“发布+验证流程”，后来拆成 Skill，不发布的时候这些指令就不占空间了。省下来的上下文让 Claude 能记住更多真正相关的事情。

## Subagents：不是多一个帮手，是多一块白板

Subagents 是 `.claude/agents/` 目录下的 Markdown 文件，用 YAML frontmatter 定义名称、描述和工具权限，正文是这个子 Agent 的系统提示词。

名称、描述和工具列表在会话启动时加载。但正文永远不会进入主会话的上下文，它在子 Agent 自己的独立上下文窗口里运行，只有最终的摘要消息回到主会话。

![Claude Code 上下文窗口结构](/images/2026-06-23-claude-code-steering-context-window.jpg)

这个设计对上下文管理的意义挺大的。Subagent 可以嵌套最多 5 层，动态工作流可以编排几十甚至上百个后台 Agent。中间结果全在脚本变量里，不污染主上下文。

那 Skill 和 Subagent 怎么选？Anthropic 给的判断标准是这样的：

- 用 Skill：当你希望流程在主线程里执行，你能看到每一步、随时干预。
- 用 Subagent：当侧任务的中间结果你不需要再看（深度搜索、日志分析、依赖审计），只需要一个最终摘要。

说白了，Subagent 的核心价值不是“多一个 Agent”，而是上下文隔离。让主会话保持干净，不被旁支任务的中间过程淹没。

我自己用 Subagent 最多的场景有两个：一个是让它先 explore 整个代码库，写一份结构报告回来，主 Agent 拿着报告再动手改代码；另一个是设计和实现分离，设计时需要进行大量的调研工作，但实现的时候只需要设计文档就足够了。

## Hooks：让 Claude Code 100% 执行

Hooks 是在 Claude Code 生命周期事件上触发的用户定义命令。注册在 `settings.json` 里，在文件编辑、工具调用、会话启动等事件上自动触发。

![Hooks 生命周期事件图](/images/2026-06-23-claude-code-steering-hooks-lifecycle.jpg)

Hook 有五种类型：command、HTTP、mcp_tool、prompt 和 agent。前三种确定性执行（跑脚本、发请求、调工具），后两种用模型判断来决定输出。

Hooks 的上下文成本极低，配置在主上下文窗口外面，harness 直接执行。只有少数 Hook 的输出会回到主上下文（比如阻断型 Hook 的错误信息，让 Claude Code 知道为什么被拒绝）。

Hooks 在整套 Claude Code 体系里最容易被忽略但最重要的一点是：

“每次 X 都必须做 Y” 如果放在 CLAUDE.md 里，本质上是在靠模型的遵从性来保证执行。模型大多数时候会遵守，但在长会话、上下文压力大、或者遇到 prompt injection 的时候，它可以不遵守。

想要确定性执行，必须用 Hook。比如“每次编辑后跑 prettier”，这不该是一条指令让 Claude Code 选择执行，而应该是一个 `PostToolUse` Hook 在每次文件写入后自动触发。

同理，“绝对不能做 X” 这种约束也不该靠 CLAUDE.md。用 `PreToolUse` Hook 检查调用，exit code 2 直接阻断。对企业来说，更严格的配置可以用 Managed Settings，管理员部署、用户不可覆盖。

所以，你要注意，凡是在 CLAUDE.md 里写了“必须”或“绝对不能”的规则，都别忘了问自己一句：这条规则失败了会怎样？如果后果严重，就赶紧改成 Hook。

## Output Styles 和 append-system-prompt：慎用，杀伤力大

最后两种方法放在一起说，它们都作用在系统提示词层面，威力大但副作用也大。

Output Styles 是 `.claude/output-styles/` 目录下的文件，注入系统提示词，永不压缩。注意一个关键细节：自定义 Output Style 默认会替换 Claude Code 的默认系统提示词，除非在 frontmatter 里设置 `keep-coding-instructions: true`。

换句话说，一旦用了自定义 Output Style，Claude Code 默认的那些行为指导（怎么控制变更范围、什么时候加注释、安全关注点、跑测试再报完工）全部会被覆盖。Claude Code 就从一个软件工程助手变成一个通用助手了。

所以 Anthropic 的建议是：先看看内置的 Proactive、Explanatory、Learning 三个样式够不够用，再考虑自定义。

append-system-prompt 是另一种用法，它是 CLI 启动时传入的 flag，只对当前会话生效，不会持久化。它是纯追加的，不会替换默认行为，一般适合临时加一些格式偏好或领域知识。

我觉得大多数人不需要碰 Output Styles。内置样式加上 CLAUDE.md 已经够用了，除非你真的要把 Claude Code 改造成一个完全不同的角色。

## 别踩这些坑

最后整理一下 Anthropic 给的“反模式”清单，基本都是我自己踩过或见过别人踩的：

第一个是把“每次 X 都必须做 Y” 这种强制性约束写在 CLAUDE.md 里。模型的指令遵循和代码自动执行是两回事。如果这个行为必须可靠发生，一定要用 Hook。同理，“绝对不能做 X” 也不该靠 CLAUDE.md，禁止性约束在 prompt injection 面前毫无抵抗力，要用 Hook 或 Managed Settings 做墙纸约束。

第二个是把流程放在 CLAUDE.md 里面。CLAUDE.md 应该只放 Claude Code 需要始终知道的事实以及它最常犯的一些错误的经验教训，而流程则放到 Skills 里面。

第三个是 Rule 不加 paths。一条只对 `src/api/` 生效的规则如果不加路径限定，效果等同于在 CLAUDE.md 里多了一行，每次都加载，每次都耗 token。个人偏好也是同样的道理，所有的配置方法都分为项目级和用户级，“永远用 semantic commit message” 这种个人习惯应该只放在本地，项目级只放团队共识。

---

## 速查表：7 种方法一览

| 方法 | 何时加载 | 压缩行为 | 上下文成本 | 适用场景 |
|------|---------|---------|-----------|---------|
| CLAUDE.md（根目录） | 会话启动，全程驻留 | 缓存式：读一次缓存，压缩后重读 | 高 | 构建命令、目录结构、编码规范、团队约定 |
| CLAUDE.md（子目录） | 按需加载，读到该目录下文件时触发 | 触发后才有，离开即丢 | 低 | 特定目录的局部规范 |
| Rules | 会话启动（无路径限定）或文件触发（有路径限定） | 压缩后重新注入 | 中 | 具体约束（如“所有 API handler 必须用 Zod 校验”） |
| Skills | 名称和描述在会话启动时加载，正文在调用时加载 | 已调用的 skill 按预算重新注入，超出则最旧的先丢 | 低 | 流程性工作（部署清单、发布检查、代码审查） |
| Subagents | 名称、描述和工具列表在会话启动时加载，正文在被调用时加载 | 只有最终摘要回到主会话 | 低 | 并行任务或需要隔离的侧任务（深度搜索、日志分析、依赖审计） |
| Hooks | 生命周期事件触发 | 完全绕过压缩 | 低 | 确定性自动化（跑 linter、发 Slack、拦截命令） |
| Output Styles | 会话启动，注入系统提示词 | 永不压缩 | 高 | 大幅改变 Claude 的角色定位 |

这张表最有价值的一列是“上下文成本”。搞清楚哪些指令需要全程驻留、哪些只在触发时加载，是用好这套系统的关键。

---

## 写在最后

说实话，这篇官方指南没介绍什么新功能，这 7 种方法早就存在了。但它的价值在于第一次把每种方法的加载时机、压缩行为和上下文成本都讲清楚了。

这 7 种方法按 harness 设计的思路大致可以整理成为四层：

- 全局层（CLAUDE.md、unscoped Rules、Output Styles）：高成本、高权威，克制使用
- 触发层（path-scoped Rules、子目录 CLAUDE.md、Skills）：按需加载，中低成本
- 隔离层（Subagents）：零主上下文成本，只关注结果
- 确定性层（Hooks）：绕过模型，代码级保证

搞清楚这四层，大部分“Claude 为什么忽略我的指令”的问题就有了答案。不是模型不听话，是你把指令放在了错误的层级，或者上下文爆满之后它被忽略掉了。

我推荐的实践顺序是这样的：所有项目第一步先给根 CLAUDE.md 瘦身，拆出去的流程丢进 Skills，跨目录的约束用 path-scoped Rules，必须 100% 执行的规则用 Hooks 做约束。然后在日常使用中持续观察、持续迭代修改，如果发现有的指令被忽略了，那大概率是相关的指令放错了层级。

上下文窗口就那么大，每一行指令都有成本。把对的指令放在对的层级，比写更多指令管用得多。

---

原文：Steering Claude Code: skills, hooks, subagents and more
<https://www.anthropic.com/engineering/claude-code-best-practices>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
