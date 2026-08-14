---
title: "Claude Code 作者说：用好 Fable 5 的关键是管理你的未知"
date: 2026-07-06T10:00:00+08:00
draft: false
tags: [Claude, Fable 5, Prompt Engineering, AI Agent, Anthropic]
description: "Claude Code 团队 Thariq 的 Fable 5 实战指南：瓶颈不再是模型能力，而是你能否讲清自己的未知。本文拆解四种未知类型，给出盲点扫描、原型头脑风暴、反向面试、实现笔记等消除未知的具体方法，并整理社区最新玩法。"
---

> 题记：本文编译自 Claude Code 团队 Thariq 的文章，原文链接：<https://x.com/trq212/status/2073100352921215386>。本文在翻译基础上做了整理和补充。

Fable 5 恢复访问之后，我拿它跑了一些之前用 Opus 做的任务。明显感觉它的一次性完成率高了很多，以前需要三四轮迭代才能收敛的事，现在经常一轮就做对了。不过反过来也有一个新问题：一旦中间跑偏了，那结果也比以前歪的更厉害了，回头看才发现是我自己没想清楚就让它动手了。

以前用 Opus 还能靠反复重试和人工 review 来兜底，现在 Fable 不太给你这个机会，具体的结果取决于你喂进去的上下文质量。

刚好看到 Claude Code 团队的 Thariq 发了一篇文章讲这个问题。他的核心观点是：Fable 5 是第一个瓶颈不在模型能力的模型，瓶颈在你能不能把自己不确定的东西讲清楚。他用了一个比喻叫“地图不是疆域”，你给 Claude Code 的 prompt、skill、上下文是地图，代码库和真实世界的约束是疆域，两者之间的差距就是未知的地方。管理好这些未知，才是用好 Fable 5 的核心。

社交媒体上这几天的实践也印证了这一点。有人用 Fable 做了 60 多个 Three.js 3D 场景 demo（Karpathy 评价 "top tier fablemaxxing"），有人复刻了 70% 的 Notion，还有人让它在终端自己渲染起了视频。这些人出活效率高，并不是因为他们 prompt 写得更长，而是他们在动手前把自己不清楚的东西消化掉了。

Thariq 这篇文章给了一套非常实用的操作框架，从实现前、实现中到实现后，每个阶段都有对应的方法来消除未知。我觉得参考价值很高，整理出来分享给大家，同时补充了 Anthropic 官方提示词指南和社区实践中的一些经验。

## 四种未知

![地图与疆域的关系](/images/2026-07-06-fable-field-guide-unknowns-map-territory-diagram.jpg)

跟人类似，Claude Code 碰到未知的时候只能靠瞎猜。做的工作越多，碰到的未知就越多，猜错的概率也越大，结果当然也会越离谱。Thariq 用了 Donald Rumsfeld 的经典分类框架，把未知拆成四种：

| 类型               | 含义                   | 例子                  |
| ---------------- | -------------------- | ------------------- |
| Known Knowns     | 你知道自己知道的，写在 prompt 里 | “把首页改成暗色模式”         |
| Known Unknowns   | 你知道自己还没想清楚           | “数据模型还没定，但我知道要先定下来” |
| Unknown Knowns   | 你不会主动写出来，但看到就知道对不对   | “这个按钮放在这里就是觉得不对”    |
| Unknown Unknowns | 你根本不知道你不知道           | “这个代码库里竟然有三套认证中间件”  |

![四种未知分类](/images/2026-07-06-fable-field-guide-unknowns-four-unknowns.jpg)

Thariq 观察到一个事情：最强的 agentic coder 并不是 prompt 写得最长，而是未知最少。他看 Boris 和 Jarred 用 Claude Code 的时候，明显能感觉到他们非常清楚自己要什么，对代码库和模型行为都有深度同步。

不过就算是高手，也会假设自己有很多未知的地方。管理和减少这些未知本身就是 agentic coding 的核心技能。

## 怎么跟 Fable 5 配合

![帮 Claude 帮你](/images/2026-07-06-fable-field-guide-unknowns-help-claude-help-you.jpg)

指导 Claude Code 是一个微妙的平衡。说得太具体，它会死板执行，该转弯的时候不知道转弯。而说得太模糊，它又会按行业最佳实践自己做选择，但未必适合你的场景。

Anthropic 官方的 Fable 5 提示词指南里提到一个关键点：Fable 5 的指令跟随好到一句简短的指令就能调整大多数行为。以前你可能要列十条不要做 X，现在一句简洁回答就够了。不过这也意味着它偶尔会做未被要求的事（比如自动起草邮件、建防御性 git 分支备份），所以需要明确告诉它边界在哪里。

另一个实用的参数是 effort。`high` 做默认就好，`xhigh` 留给最难的任务，日常用 `medium` 甚至 `low`。低 effort 的 Fable 5 往往比之前模型的 `xhigh` 还强，这个也侧面说明 Fable 5 模型的提升的确是很大的。

不过 Claude Code 能帮你更快发现未知。它搜代码库和互联网极快，对大多数话题知道得比你多，从失败中迭代的速度也比你快。Thariq 说最重要的一点是：告诉 Claude Code 你现在处于思考过程的哪个阶段。主动告诉它你对这个问题和代码库的理解，让它像伙伴一样跟你一起工作，而不是一个单纯的执行者。

## 动手之前：把不清楚的找出来

![实现前的方法概览](/images/2026-07-06-fable-field-guide-unknowns-pre-implementation.jpg)

### 盲点扫描

当你在一个不熟悉的代码库开始工作，或者用 Claude Code 帮你做设计这种你不太擅长的事情时，大概率有很多 Unknown Unknowns。

这时候直接问 Claude Code：“帮我做一次盲点扫描，找出我在这个问题上的 Unknown Unknowns”。

示例提示词：

> 我要在这个代码库里加一个新的 auth provider，但我对 auth 模块一无所知。帮我做一次盲点扫描，找出我的相关 Unknown Unknowns，帮我更好地给你写 prompt。

### 头脑风暴 + 原型

当你有很多 Unknown Knowns 的时候（就是那种“我说不出来但看到就知道对不对”的标准），最好让 Claude Code 做几个方向给你挑。

比如你想加一个按钮到界面上，但不确定放哪里好看，也说不清什么算好看。这时候让 Claude Code 做四个完全不同的设计方向，用 HTML 原型展示出来，你看到了自然就能做选择。

> 我想做一个数据 dashboard，但我没有视觉品味，也不知道有什么可能性。做一个 HTML 页面展示 4 个完全不同的设计方向，让我能看看效果，然后跟你反馈。

其实 Thariq 几乎每次 coding session 都会以探索或头脑风暴阶段开始。Claude Code 经常能找到他自己会错过的高价值路径。

### 面试

做完头脑风暴后大概率还有很多未知点。这时候让 Claude Code 来采访你：

> 对任何模糊的地方一个一个问我，优先问那些答案会改变架构的问题。

这个方法特别有用。Claude Code 会逼你想清楚那些你以为已经想清楚、但其实并没有的东西。

## 动手的时候：记下每次偏离

不管规划做得多充分，动手之后总会遇到意料之外的情况。Thariq 的做法是让 Claude 维护一个临时的 `implementation-notes.md` 文件：

> 维护一个 implementation-notes.md。如果碰到 edge case 需要偏离计划，选保守方案，记录到 Deviations 下面，然后继续。

这样下一次做类似任务的时候就有据可查。这里补充一个 Anthropic 官方指南里提到的坑：长时间运行的任务中，Fable 5 可能编造进度报告。官方建议是让它对照实际工具结果审计每一条进度声明，只报告你能指向证据的工作。不要让它复述自己的推理过程（会触发安全分类器导致 refusal），需要看推理过程就读 thinking block。

## 做完之后：让别人看懂你做了什么

![实现后的交付](/images/2026-07-06-fable-field-guide-unknowns-post-implementation.jpg)

做完之后，Thariq 会让 Claude Code 把原型、规格文档和实现笔记打包成一个可以扔到 Slack 里让人快速理解的文档。

还有一个我觉得挺妙的做法：让 Claude Code 给你出一份关于这次改动的测试题。

> 我想确保我理解了这次改动的所有内容。给我一份 HTML 报告，包含改动的上下文、直觉、做了什么，底部附一个 quiz，我必须答对才 merge。

## Fable 5 的实战验证：视频剪辑

Thariq 在文章最后举了一个自己的例子：Fable 5 的发布视频是他完全用 Claude Code 剪辑的。

他的流程完美体现了管理未知的方法：

1. 他知道 Claude Code 能用代码剪视频和做转录，但不确定精度够不够。于是先问 Claude Code 解释 Whisper 的工作原理，确认是否能精确切掉”嗯啊”和停顿
2. 他想做一个和语音同步的字幕 UI，但不确定能不能做到。让 Claude Code 做一个 Remotion 原型验证可行性
3. 视频色彩偏灰，他知道需要调色但不知道什么是好的调色。让 Claude Code 教他调色的基础知识，帮他发现自己的未知

每一步都是先暴露未知，再决定怎么做。

## 社区在怎么用 Fable 5

Thariq 这篇文章是方法论层面的。社区这几天的实践则展示了 Fable 5 的具体能力边界。

我觉得最有意思的一个玩法是知识蒸馏。有人让 Fable 5 扮演即将退休的首席工程师，审计整个代码库，写出 10-16 个 Skill 文件（调试手册、变更规则、曾经踩过的坑等等）。之后 Opus 和 Sonnet 按这套 playbook 跑更便宜的 session，效果接近 Fable 标准。代价是一次跑下来能吃掉 30% 的周额度。这个玩法和 Anthropic 官方建议的构建记忆系统不谋而合：给 Fable 一个地方记录教训，哪怕只是一个 Markdown 文件，它在有历史参考的时候表现显著更好。

另一个社区逐渐形成共识的模式是 Fable 做大脑、Codex 做四肢。Fable 5 最强的不是写代码，而是理解复杂需求、拆解任务、制定策略。具体执行交给 GPT-5.5 或者 Opus，相当于 Tech Lead 配高执行力工程师。

Peter Gostev 在 3D 场景生成方向做了一个 45 分钟的视频，60 多个 Three.js 环境 demo。Karpathy 看完评价”top tier fablemaxxing”，Fable 在 3D 这块确实跨了一个台阶。

还有一个方向是网站复刻。给 Fable 5 一个链接，它能读底层代码（不只是截图），理解视觉和技术细节，然后复刻出带动效和 3D 交互的落地页。

## 写在最后

说实话，Fable 5 让我对“怎么写 prompt”这件事的理解变了。以前的难点是怎么让模型理解我的意思，现在的难点是我自己到底想要什么。这完全是两码事。

推荐你在下次动手前试试 Thariq 的方法：先花两分钟问问自己“我这里有什么不确定的”，然后让 Claude Code 帮你先把它们挖出来之后再去干活。

---

相关资源：

- Thariq 原文：<https://x.com/trq212/status/2073100352921215386>
- Anthropic 官方 Fable 5 提示词指南：<https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5>
- Fable 5 知识蒸馏到 Skill 的完整 prompt（@PrajwalTomar_）：<https://x.com/PrajwalTomar_/status/2073768365873885396>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
