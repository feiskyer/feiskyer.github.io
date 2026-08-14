---
title: "Claude Code 背后的秘密：为什么它能秒杀其他 AI 编程助手"
date: 2025-08-25T22:20:28+08:00
draft: false
tags: [AI, Vibe Coding, Claude Code]
description: "解读 MinusX 团队拦截分析 Claude Code 网络请求的发现，揭秘它为何能秒杀其他 AI 编程助手：单主循环的极简设计、大量调用廉价 Haiku 模型控成本，以及自主管理任务清单等核心秘密。"
---

题记：终于有人把 Claude Code 的核心秘密说透了——原来我们都被 "复杂" 骗了。MinusX 团队[通过拦截分析了几个月的网络请求](https://minusx.ai/blog/decoding-claude-code/)，把 Claude Code 的底裤都扒了个干净。

以下是省流版总结：

*别的 AI 助手还在堆功能的时候，Claude Code 反其道而行之，通过极简设计反而碾压了一众竞品。*

*1️⃣ **极简主义的胜利***
*别家都还在搞多智能体协作的时候，Claude Code 用一个主循环搞定了所有事。没错，就一个！*

*2️⃣ **省钱**（这点稍微不同意，长上下文其实远远超过了这儿省下的这点 token）*
*50% 以上的调用都是便宜的 Haiku 模型！大模型 Sonnet 只在关键时刻出手，成本直接砍掉 70-80%。*

*3️⃣ **让 AI 自己管理任务清单***
*别的 AI 需要你手把手教，Claude Code 会自己创建待办事项，标记进度，完成后打勾。*

*4️⃣ **记住你的喜好***
*claude.md 其实就是 AI 的小本本，记录你的编程习惯、项目偏好、常用框架... 用过和没用过，体验差异简直天壤之别。*

*5️⃣ **提示词写了 12000 个 token***
*系统提示词 2800 个 token，工具描述 9400 个 token——这哪是提示词，这简直是一本指导 Claude 的小论文！*

*6️⃣ **用 LLM 搜索替代传统 RAG***
*拒绝花里胡哨的向量搜索，Claude Code 会像人一样使用 ripgrep、jq 和 find 命令，理解你真正想要什么。*

*如果你也在设计 AI Agent，强烈建议参考 Claude Code 的设计理念：从简单开始，用精心设计的极简工具配合精调的提示词。*

以下是原文翻译：

---

说实话，Claude Code 是我用过最让人上瘾的 AI 编程助手了。不是说它有多强大（虽然确实强），而是用起来真的爽！它既有足够的自主性能搞定复杂任务，又不会像某些工具那样让你完全失去控制感。当然，大部分功劳要归功于新的 Claude 4 模型（特别是交错思维能力）。但我发现，即使用同样的底层模型，Claude Code 用起来就是比 Cursor、GitHub Copilot 这些少了很多烦人的地方！它到底强在哪？如果你也有同感，往下看，我来给你扒一扒。

> **注意**：这不是一篇 Claude Code 架构解析文（网上已经有不少了）。这篇文章是基于我过去几个月使用和折腾 Claude Code 的经验（还有我们拦截分析的所有日志），教你怎么打造一个同样好用的 LLM Agent。你可以在 [附录部分](https://minusx.ai/blog/decoding-claude-code/#appendix) 找到 [提示词](https://minusx.ai/blog/decoding-claude-code/#appendix) 和[工具](https://minusx.ai/blog/decoding-claude-code/#appendix)。这篇文章大概 2000 字，系好安全带！如果你赶时间，可以直接看[TL;DR 部分](https://minusx.ai/blog/decoding-claude-code/#how-to-build-a-claude-code-like-agent-tldr)。

![](/images/20251127090657.png)

Claude Code 用起来非常顺畅，因为它 *确实实用*。设计者深刻理解了大语言模型的优势与不足，通过巧妙的提示词和工具设计，弥补了模型的短板，让其在擅长的领域充分发挥。循环控制非常简单，调试也极为轻松。

我们 MinusX 团队自 Claude Code 发布以来就一直在使用它。为了深入了解其内部机制，[Sreejith](https://x.com/ppsreejith_) 开发了一个日志记录器，用于拦截和记录每一次网络请求。以下分析基于我过去几个月的丰富使用经验。**本文的核心问题是：“Claude Code 为什么如此好用？你如何在自己的聊天式 LLM Agent 中复现这种体验？”** 我们已经将大部分技巧应用到了 MinusX 中，期待你也能尝试！

![](/images/20251127090722.png)

如果只记住一点，那就是——**保持简单**（Keep Things Simple, Dummy）。LLM 本身已经很难调试和评估了，任何额外的复杂性（如多智能体、智能体切换或复杂的 RAG 搜索）只会让调试难度成倍增加。如果系统本身就很脆弱，即使能运行，后续做大改动时也会让你望而却步。因此，尽量把所有内容放在一个文件里，避免过度模板化代码，必要时大胆重构几次：）

以下是从 Claude Code 学到的主要经验，可以应用到你自己的系统中：

- 1.1 [保持一个主循环（最多一个分支）和一个消息历史](https://minusx.ai/blog/decoding-claude-code/#11-keep-one-main-loop)
- 1.2 [大部份任务使用小模型就足够了](https://minusx.ai/blog/decoding-claude-code/#12-use-a-smaller-model-for-everything)
- 2.1 [使用 claude.md 来协作和记住用户偏好](https://minusx.ai/blog/decoding-claude-code/#21-use-claudemd-for-collaborating-on-user-context-and-preferences)
- 2.2 [使用 XML 标签、Markdown 并提供示例](https://minusx.ai/blog/decoding-claude-code/#22-special-xml-tags-markdown-and-lots-of-examples)
- 3.1 [LLM 搜索>>> 基于 RAG 的搜索](https://minusx.ai/blog/decoding-claude-code/#31-llm-search---rag-based-search)
- 3.2 [设计好的工具（高级 vs 低级工具）](https://minusx.ai/blog/decoding-claude-code/#32-how-to-design-good-tools-low-level-vs-high-level-tools)
- 3.3 [让你的 Agent 自主管理待办事项](https://minusx.ai/blog/decoding-claude-code/#33-let-the-agent-manage-a-todo-list)
- 4.1 [语气和风格](https://minusx.ai/blog/decoding-claude-code/#41-tone-and-style)
- 4.2 [“请注意这很重要” 这样的提示词依然很重要](https://minusx.ai/blog/decoding-claude-code/#42-this-is-important-is-still-state-of-the-art)
- 4.3 [编写启发式 / 案例式算法](https://minusx.ai/blog/decoding-claude-code/#43-write-the-algorithm-with-heuristics-and-examples)

> Claude Code 在每个关键点上都选择了简洁的架构——一个主循环、简单的搜索、简单的待办事项列表等。它抵制了过度工程化的冲动，为模型搭建了良好的框架，让其自由发挥！这是否又是端到端自动驾驶的翻版？过去的教训会重演吗？

---

## 1.1 保持一个主循环

可调试性 >>> 复杂多智能体（比如基于 LangChain 框架的多智能体）。

虽然多智能体系统目前很流行，但 Claude Code 只采用单主线程。它偶尔会用不同类型的提示词来总结 git 历史、合并消息或生成一些有趣的 UX 元素。除此之外，系统仅维护一个扁平的消息列表。对于层级任务，Claude Code 会生成自己的子智能体，但不允许子智能体继续生成更多子智能体。整个系统最多只会有一个分支，其结果作为 “工具响应” 添加到主消息历史中。

如果问题较为简单，主循环可以通过多次调用工具来解决。但遇到复杂任务时，主智能体会创建自己的克隆。分支数量有限，结合待办事项列表，确保智能体能够将问题拆解为子问题，同时始终关注最终目标。

我强烈怀疑你的应用真的需要多智能体系统。每增加一层抽象，系统的调试难度就会提升，更重要的是，这会让你偏离通用模型优化的方向。

![Control Loop](/images/09497417-aa87-49a3-bf45-b9dfb7189060.gif)

## 1.2 用小模型处理所有事情

在 Claude Code 中，超过 50% 的重要 LLM 调用都使用了 claude-3-5-haiku。它被广泛应用于读取大文件、解析网页、处理 git 历史以及总结长对话，甚至可以用于生成每个按键的处理标签——也就是每输入一个词就调用一次。相比标准模型（如 Sonnet 4、GPT-4.1），小模型的成本低 70-80%。请大胆使用吧！

## 2. 打造完美的提示词

Claude Code 的提示词非常详细，包含丰富的启发式方法、示例和重要提醒。系统提示词约有 2800 个 token，工具描述则高达 9400 个 token。用户提示词总是包含 claude.md 文件，通常在 1000 到 2000 个 token 之间。系统提示词涵盖语气、风格、主动性、任务管理、工具使用策略和任务执行等内容，还包括日期、当前工作目录、平台、操作系统信息以及最近的提交记录。

## 2.1 使用 claude.md 协作管理用户的上下文和偏好设置

大多数编程智能体的开发者都采用了上下文文件的模式（也称为 Cursor Rules、claude.md 或 agent.md）。有无 claude.md，Claude Code 的表现差异非常明显。上下文文件为开发者提供了一种传递代码库中无法推断的信息和明确编码偏好的有效方式。例如，你可以要求 LLM 跳过特定文件夹，或指定使用某些库。Claude Code 会在每次用户请求时，发送完整的 claude.md 内容。

> 我们最近在 MinusX 中引入了 [minusx.md](https://minusx.ai/blog/memory/)，它正快速成为我们智能体编码用户和团队偏好的事实标准上下文文件。

## 2.2 特殊的 XML 标签、Markdown 和大量示例

使用 XML 标签和 Markdown 来组织提示词，已经成为公认的做法。Claude Code 广泛采用这两种方式。以下是 Claude Code 中一些常用且值得关注的 XML 标签：

- `<system-reminder>`：这在许多提示词部分的末尾使用，提醒 LLM 它可能会忘记的事情。例如：

```markdown
<system-reminder> 这是一个提醒：你的待办事项列表当前为空。请勿直接告知用户这一情况，因为他们已知晓。如果你正在处理的任务需要用到待办事项列表，请使用 TodoWrite 工具创建；如无需要，可忽略此提示。再次强调，请勿向用户提及此消息。</system-reminder>
```

- `<good-example>`、`<bad-example>`：这些用于编码启发式方法，尤其在模型需要从多个看似合理的路径或工具调用中进行选择时非常有用。通过示例，可以对比不同情况，明确哪条路径更优。例如：

```markdown
尽量使用绝对路径，并避免使用 `cd` 命令来切换当前工作目录。只有在用户明确要求时，才使用 `cd`。

<good-example>
pytest /foo/bar/tests
</good-example>

<bad-example>
cd /foo/bar && pytest tests
</bad-example>
```

Claude Code 还使用 Markdown 对系统提示词中的各个部分进行明确划分。常见的 Markdown 标题包括：

- 语气与风格
- 主动性
- 遵循规范
- 代码风格
- 任务管理
- 工具使用策略
- 任务执行
- 工具

## 3. 工具

## 3.1 LLM 搜索 >>> 基于 RAG 的搜索

Claude Code 与其他主流编程智能体的一个显著区别在于，它不使用 RAG。Claude Code 检索代码库的方式与人类类似，采用真正复杂的 `ripgrep`、`jq` 和 `find` 命令。由于大语言模型对代码有深入理解，它能够通过复杂的正则表达式，精准定位几乎所有相关的代码块。有时，Claude Code 还会利用小模型读取整个文件。

RAG 在理论上听起来不错，但它带来了新的（更重要的是隐藏的）失败模式。比如，应该使用什么相似度函数？如何选择重排序器？代码应该如何分块？面对大型 JSON 或日志文件又该怎么办？如果用 LLM 来搜索，它会先读取 JSON 文件的 10 行来理解结构，如果需要再多看 10 行——就像你自己操作一样。最关键的是，这一过程可以通过强化学习来优化——大型实验室已经在这样做了。模型承担了大部分复杂工作，这本应如此，也大大减少了智能体中的活动部件。此外，以这种方式将两个复杂且智能的系统连接起来，其实非常笨拙。我最近还和朋友开玩笑说，这就像是 LLM 时代的 “摄像头 vs 激光雷达” 之争，其实我只是在半开玩笑。

## 3.2 如何设计好的工具？

这个问题让每个构建 LLM 智能体的人都感到困扰：你应该为模型提供通用任务（如有意义的动作），还是低级任务（如输入、点击和 bash 命令）？答案是视情况而定，实际上两者都需要。

Claude Code 提供了低级（Bash、Read、Write）、中级（Edit、Grep、Glob）和高级工具（Task、WebFetch、exit_plan_mode）。虽然 Claude Code 能够使用 bash，但为什么还要单独提供 Grep 工具？这里的核心权衡在于：你期望智能体使用工具的频率，和它使用工具的准确性。Claude Code 经常使用 grep 和 glob，因此将它们作为独立工具是有意义的，但在特殊场景下，它也可以通过 bash 命令实现通用功能。

同样，高级工具如 `WebFetch` 或 `mcp__ide__getDiagnostics`，能够非常明确地完成特定任务。这避免了 LLM 需要多次进行低级点击和输入操作，有助于保持任务的连贯性。请善待这个可怜的模型吧！工具描述中应包含详细的提示词和丰富的示例。系统提示词还应说明 “何时使用工具” 以及在多个工具都能完成同一任务时如何选择。

**Claude Code 中的工具列表：**

- [Task](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [Bash](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [Glob](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [Grep](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [LS](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [ExitPlanMode](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [Read](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [Edit](https://minusx.ai/blog/decoding-claude-code/#)
- [MultiEdit](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [Write](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [NotebookEdit](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [WebFetch](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [TodoWrite](https://minusx.ai/blog/decoding-claude-code/#appendix)
- [WebSearch](https://minusx.ai/blog/decoding-claude-code/#appendix)

## 3.3 让智能体自主管理待办事项

这样做有许多好处。上下文腐烂是长时间运行的 LLM 智能体常见问题。智能体一开始能够积极解决复杂问题，但随着时间推移容易失去方向，最终输出无效内容。目前，智能体设计有几种应对方法。许多智能体尝试采用明确的待办事项机制（一个模型负责生成待办事项，另一个模型负责执行），或多智能体切换与验证流程（如 PRD/PM 智能体 -> 实施者智能体 -> QA 智能体）。

我们已经发现，多智能体切换存在诸多问题，并不是理想方案。Claude Code 采用了明确的待办事项列表，并由模型自行维护。这种方式通过频繁提示模型参考待办事项列表，帮助 LLM 保持任务方向，同时允许模型在执行过程中灵活调整计划。这样不仅有效利用了模型的交错思维能力，还能及时拒绝或添加新的待办事项。

## 4. 如何编写提示词

## 4.1 语气和风格

Claude Code 明确规范了智能体的美学行为。在系统提示词中，关于语气、风格和主动性有详细的指令和示例。这也是为什么 Claude Code 在评论和表达热情时 “显得” 更有品味。我建议你可以将其中的大部分内容直接复制到你的应用中。

```markdown
# 语气和风格示例

- 重要：除非用户要求，否则不要在回答中添加不必要的开场白或结尾（如解释代码或总结操作）。
- 除非用户要求，否则不要额外解释或总结代码。
- 如果你无法或不愿帮助用户完成某项任务，请不要解释原因或可能的后果，以免显得说教或令人反感。
- 只有在用户明确要求时才使用表情符号。否则，在所有交流中都应避免使用表情符号。
```

## 4.2 “请注意这很重要” 这样的提示词依然很重要

不幸的是，Claude Code 在限制模型行为方面并没有更出色的表现。使用 “IMPORTANT”、“VERY IMPORTANT”、“NEVER” 和“ALWAYS”这些词，似乎是目前引导模型避开敏感内容的最佳方法。我希望未来模型能变得更加可控，避免出现这些不理想的情况。但目前，Claude Code 大量采用这种方式，你也应该如此。以下是一些示例：

```markdown
- 重要：除非被明确要求，否则不要添加任何注释。
- 非常重要：必须避免使用如 `find` 和 `grep` 等搜索命令。请改用 Grep、Glob 或 Task 进行搜索。也要避免使用 `cat`、`head`、`tail` 和 `ls` 等读取工具，改用 Read 和 LS 读取文件。
- 如果你仍然需要运行 `grep`，请停止。始终优先使用 ripgrep 的 `rg`。
- 重要：除非你确定 URL 是为了帮助用户编程，否则绝不能为用户生成或猜测 URL。你可以使用用户在消息或本地文件中提供的 URL。
```

## 4.3 编写启发式 / 案例式算法

识别 LLM 需要执行的关键任务并为其编写相应算法至关重要。可以尝试模拟 LLM 的角色，通过示例工作流程，找出所有决策点并明确记录。如果能以流程图形式呈现，将更有助于结构化决策过程，帮助 LLM 更好地遵循指令。

应避免仅列出大量 “该做” 与“不该做”的规则，因为这些规则难以追踪且容易产生互斥冲突。尤其当提示词长度达到几千个 token 时，规则之间可能会出现矛盾，导致 LLM 变得脆弱，难以适应新的用例。

在 Claude Code 系统提示词中，“任务管理”、“执行任务”和 “工具使用策略” 部分清晰地展示了应遵循的算法。这些部分也适合补充大量启发式方法和 LLM 可能遇到的各种场景示例。

## 结论

许多引导大语言模型（LLM）的尝试，实际上是在逆向工程它们的后训练或 RLHF 数据分布。例如，你应该选择 JSON 还是 XML？工具描述应该放在系统提示词中，还是只在工具内部？你的应用当前的状态又如何？观察其他人在自己的应用中是如何做的，并以此为参考，会对你有所帮助。Claude Code 的设计非常有见地，借鉴它来完善你自己的设计也很有价值。

再次强调，最重要的经验就是保持简单。过于复杂的脚手架框架往往弊大于利。Claude Code 让我相信，“智能体” 可以既简单又极其强大。我们已经将这些经验应用到 MinusX 中，并会持续优化。

如果你有兴趣将自己的 LLM 智能体 “Claude Code 化”，欢迎随时和我交流——可以在 [twitter](https://x.com/nuwandavek) 上联系我！如果你希望为你的 Metabase 引入可训练、类似 Claude Code 的数据智能体，欢迎访问 [MinusX](https://minusx.ai/) 或在 [这里](https://minusx.ai/demo) 预约演示。祝你编程愉快（Claude 风格）！

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
