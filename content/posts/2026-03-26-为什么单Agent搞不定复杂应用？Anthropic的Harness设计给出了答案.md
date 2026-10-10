---
title: "为什么单 Agent 搞不定复杂应用？Anthropic 的 Harness 设计给出了答案"
date: 2026-03-26T10:00:00+08:00
draft: false
tags: [AI Agent, Anthropic, 多Agent架构, 全栈开发, Claude]
description: "让 AI 从一句话需求连续开发几小时，交付完整全栈应用有多难？Anthropic Labs 借鉴 GAN 思路，用 Planner、Generator、Evaluator 三 Agent 分工的 Harness 设计，攻克上下文焦虑和自我评估偏差两大死穴。"
---

> 题记：本文编译自 Anthropic 工程博客《[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)》，由 Anthropic Labs 团队的 Prithvi Rajasekaran 撰写。

让 AI 写一个页面、一个函数，现在大多数编程 Agent 都能做得不错。但如果你给它一句话需求，让它自己规划产品、拆分任务、写代码、测试、迭代修 Bug，连续跑好几个小时，最后交付一个完整的全栈应用呢？

这个问题 Anthropic 一直在啃。他们之前发过一篇长时间 Agent Harness 的文章（《[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)》），解决了多会话上下文传递的问题。但两个更深层的问题一直没搞定：Agent 跑着跑着就开始划水，它还对自己的产出盲目乐观。

这次 Anthropic Labs 的工程师 Prithvi 换了个思路，从 GAN（生成对抗网络）借了个核心理念：把“生成”和“评估”拆给不同的 Agent。结果挺有意思：一句话需求，6 小时后拿到一个能玩的复古游戏编辑器，还自带 AI 辅助功能。

## 单 Agent 的两个死穴

在聊多 Agent 架构之前，先说清楚为什么单 Agent 搞不定长时间开发任务。

**第一个问题是上下文焦虑。**之前在 Sonnet 4.5 上观察到一个现象：随着上下文窗口慢慢填满，模型会开始赶工，提前收尾正在做的事。然而这并不是因为它把活做完了，而是它感觉自己快没空间了。

这个问题有两种解法。一种是 Compaction，在上下文里就地压缩早期对话。另一种是 Context Reset，彻底清空上下文，起一个新 Agent 接手，通过结构化的交接文档传递状态。Anthropic 测试下来发现，Compaction 解决不了焦虑问题，因为模型还是在同一个会话里，它还是会觉得空间不够。Context Reset 更干净，代价是交接文档必须写得足够好，否则新 Agent 接不上。

**第二个问题更致命：自我评估偏差。**让 Agent 评价自己的产出，它会非常自信地给出好评，哪怕在人看来质量一般。这在前端设计这种主观任务上尤其明显，没有二进制的对错标准，模型打分一律往高了给。

Anthropic 试过让 Generator 自己做 Code Review，效果也不好。但把评估拆成独立 Agent 之后，事情变得可控了。j 就像原文说的，调教一个独立的评估 Agent 让它变得严格，比让一个生成 Agent 自我批判要容易得多。

这个观察其实不意外。人也是这样，让写代码的人自己 Review 自己的代码，效果肯定不如让另一个人来看。

## 前端设计：怎么让 AI 不再有 AI 味

在全栈开发之前，Prithvi 先拿前端设计做了实验。这个方向有个好处：设计质量虽然主观，但可以通过制定明确的评分标准来量化。

他定了四个评分维度：

- 设计质量：颜色、排版、布局有没有统一的气质，还是东拼西凑
- 原创性：有没有主动的创意决策，还是在用模板默认值。紫色渐变配白卡片这种 AI 标配直接扣分
- 工艺：字体层级、间距、对比度这些基本功
- 功能性：用户能不能看懂界面、找到操作入口

前两个维度的权重更高。因为 Claude 的基本功本来就不错，Craft 和 Functionality 通常能过关，但设计和原创性上经常输出平庸的东西。

评估 Agent 配了 Playwright MCP，它不是看截图打分，而是实际在浏览器里操作页面：点按钮、滚页面、截图分析，然后写详细的批评意见反馈给 Generator。每轮 5-15 次迭代，整个过程可能跑四个小时。

有一个案例我觉得挺值得说的。Prithvi 让模型做一个荷兰美术馆的网站，前九轮迭代都在渐进改进，产出了一个深色调的着陆页，视觉上已经挺不错了。然后第十轮，模型突然推翻了整个方案，做了一个 3D 空间体验，用 CSS 透视渲染了一个有格子地板的房间，画作挂在墙上，房间之间通过门导航，而不是传统的滚动或点击。

这种创意跳跃在单次生成里几乎不可能出现。是评估反馈的累积压力逼着 Generator 去冒险，而不是停在安全区。下面是前端设计迭代过程的演示视频：

<video controls muted src=“assets/2026-03-26-harness/frontend-design-demo.mp4”></video>

不过也有个有趣的副作用：评分标准里的措辞会直接影响生成方向。Prithvi 在标准里写了“最好的设计应该是博物馆级别的”，结果模型的审美开始往某种特定方向收敛。也就是说，标准本身不只是评分工具，也是风格引导。

## 三个 Agent，一个完整应用

前端设计验证了 Generator-Evaluator 模式的可行性之后，Prithvi 把它扩展到了全栈开发。架构变成了三个 Agent。

#### Planner：从一句话到完整产品规格

之前的 Harness 需要用户写好详细的产品 Spec。现在 Planner 接手了这个活：给它一句话需求，它输出完整的产品规格文档，包括功能列表、设计语言、Sprint 划分，甚至主动在产品里嵌入 AI 功能。

Prithvi 特意让 Planner 只做高层设计，不写具体实现细节。逻辑是这样的：如果 Planner 在规格里写死了技术方案但写错了，这个错误会一路传到下游。不如只约束“做什么”，让 Generator 自己决定“怎么做”。

#### Generator：按 Sprint 推进

Generator 接过 Spec，按 Sprint 一个一个实现功能。技术栈是 React + Vite + FastAPI + SQLite，有 Git 版本控制。每完成一个 Sprint，在提交给 Evaluator 之前先自评一轮。

这里有个设计细节：每个 Sprint 开始前，Generator 和 Evaluator 先谈判一份 Sprint Contract，约定这个 Sprint 具体要交付什么、怎么验收。这一步弥补了高层 Spec 和具体实现之间的鸿沟。

Agent 之间怎么通信？通过文件。一个 Agent 写文件，另一个读文件并回复，没有用复杂的消息队列或 API 调用。简单，但够用。

#### Evaluator：用 Playwright 当真正的用户

Evaluator 不是看代码打分，而是用 Playwright 像真实用户一样操作应用，真正去点按钮、填表单、测 API、查数据库状态。然后根据 Sprint Contract 里的验收标准逐条打分，不达标就打回去。

这个 Evaluator 调教起来不容易。Prithvi 说 Claude 开箱即用作为 QA Agent 其实很差劲：早期运行中，我看着它发现了真实的问题，然后说服自己这些问题不是大问题，最后批准了。它还倾向于只测表面功能，不深入边界情况。

调教的方法是反复看 Evaluator 的日志，找到它的判断和人的判断不一致的地方，然后针对性地改 Prompt。来回迭代了好几轮才让它的评分标准达到一个合理的水平。

## 9 块钱 vs 200 块钱：差距有多大

Prithvi 用同一个需求测了单 Agent 和三 Agent Harness。需求很简单：做一个 2D 复古游戏编辑器，要有关卡编辑、精灵编辑、实体行为和可玩测试模式。

| 方案 | 耗时 | 成本 |
|------|------|------|
| 单 Agent | 20 分钟 | $9 |
| 三 Agent Harness | 6 小时 | $200 |

贵了 20 倍，但产出质量完全不是一个级别的。

单 Agent 的版本乍看还行，但点进去就出问题了。布局浪费空间，面板用了固定高度，大片空白。工作流没有引导，用户得自己猜到”先做精灵和实体，再布关卡”的操作顺序。最要命的是游戏本身跑不了，实体出现在画面上但不响应任何输入，代码里实体定义和游戏运行时的连接是断的，表面看不出来。

![单 Agent 版本的主界面](/images/2026-03-26-AgentAnthropicHarness-solo-opening.png)

![单 Agent 版本的精灵编辑器](/images/2026-03-26-AgentAnthropicHarness-solo-sprite-editor.png)

![单 Agent 版本的游戏模式，实体不响应输入](/images/2026-03-26-AgentAnthropicHarness-solo-gameplay.png)

三 Agent 版本从同一句话需求出发，Planner 把它扩展成了 10 个 Sprint、16 个功能的完整 Spec。除了基础编辑器和测试模式，还规划了精灵动画系统、行为模板、音效和音乐、AI 辅助精灵生成和关卡设计，甚至游戏导出和分享链接。Planner 还读了 Anthropic 的 frontend-design Skill，为整个应用制定了统一的视觉设计语言。

实际体验下来，画布用满了视窗，面板大小合理，界面有统一的视觉风格。精灵编辑器工具更丰富，颜色选择器更好用，缩放控制也更顺手。因为 Planner 主动嵌入了 AI 功能，应用内置了 Claude 集成，可以用自然语言生成精灵、设计关卡。

![三 Agent 版本的主界面](/images/2026-03-26-AgentAnthropicHarness-harness-opening.png)

![三 Agent 版本的精灵编辑器](/images/2026-03-26-AgentAnthropicHarness-harness-sprite-editor.png)

![用内置 AI 生成关卡](/images/2026-03-26-AgentAnthropicHarness-harness-ai-design-1.png)

![AI 辅助关卡设计的结果](/images/2026-03-26-AgentAnthropicHarness-harness-ai-design-2.png)

最关键的区别是在游戏模式能玩了。角色能移动、能跳跃，虽然物理引擎有些粗糙（角色跳到平台上会出现重叠），但核心功能是通的。

![三 Agent 版本的游戏模式，核心功能可以运行](/images/2026-03-26-AgentAnthropicHarness-harness-gameplay.png)

Evaluator 在这个过程中抓到了很多具体问题。比如矩形填充工具只在拖拽起止点放置了瓦片，而不是填满区域；删除实体生成点的快捷键判断条件写错了；FastAPI 的路由顺序有问题，`reorder` 被当成了 `frame_id` 去解析。这些是单 Agent 版本里根本不会被发现的 Bug。

## Opus 4.6 来了，Harness 该减肥了

上面这套三 Agent 架构是用 Opus 4.5 跑的。等 Opus 4.6 发布之后，Prithvi 做了一件所有维护 Harness 的人都应该做的事：重新审视每个组件，看哪些还有存在的必要。

比如，之前 Harness 里的每个组件都编码了一个关于模型不能做什么的假设，而这些假设值得反复检验。

Opus 4.6 在规划能力、长上下文检索和自我纠错上都有明显提升。Prithvi 于是把 Sprint 机制整个拿掉了，不再把工作拆成小块，让 Generator 一口气连续写代码。

Planner 保留了，因为没有它 Generator 会低估项目范围，直接开始写代码，最后做出来的东西功能少很多。Evaluator 也保留了，但从每个 Sprint 结束后评分改成了全部开发完再做一轮 QA。

这个简化改变了 Evaluator 的角色定位。在 4.5 时代，开发任务本身就在模型能力的边界上，Evaluator 几乎每轮都能抓到有意义的问题。到了 4.6，模型的裸能力边界往外扩了，很多以前需要 Evaluator 把关的东西现在 Generator 自己就能做好。Evaluator 的价值集中在那些仍然超出 Generator 能力的部分。

简化后的 Harness 测了一个更大的需求：用 Web Audio API 在浏览器里做一个 DAW（数字音频工作站）。

| Agent 阶段 | 耗时 | 成本 |
|------------|------|------|
| Planner | 4.7 分钟 | $0.46 |
| Build 第一轮 | 2 小时 7 分 | $71.08 |
| QA 第一轮 | 8.8 分钟 | $3.24 |
| Build 第二轮 | 1 小时 2 分 | $36.89 |
| QA 第二轮 | 6.8 分钟 | $3.09 |
| Build 第三轮 | 10.9 分钟 | $5.88 |
| QA 第三轮 | 9.6 分钟 | $4.06 |
| **合计** | **3 小时 50 分** | **$124.70** |

Generator 连续写了两个多小时的代码，没有 Sprint 拆分也没有跑偏，这在 4.5 上是做不到的。

QA 仍然抓到了关键问题。第一轮反馈说：“应用设计很好，AI Agent 集成也不错，但好几个核心 DAW 功能只是展示用的，时间轴上的音频片段不能拖动，没有乐器 UI 面板，没有可视化的效果编辑器。这些不是边缘功能，是让 DAW 可用的核心交互。”第二轮继续追：“录音功能还是空壳，片段裁剪和分割没实现，效果可视化只有数字滑块没有图形。”

最后跑出来的 DAW 离专业软件自然还很远，但核心组件都有了：编排视图、混音器、音频传输控制。Prithvi 甚至通过内置的 AI Agent 完全用自然语言编曲，设定节拍和调性、铺旋律、加鼓点、调混音、上混响。下面是 DAW 的演示视频：

<video controls muted src=“assets/2026-03-26-harness/daw-demo.mp4”></video>

## 写在最后

这篇文章给我最大的触动不是三 Agent 架构本身，而是 Prithvi 对 Harness 简化过程的记录。他一开始试过激进地砍组件，发现不行，又改成一次只去掉一个来观察影响。这种方法论比架构本身更有迁移价值，不管你是在做 Agent 还是做传统系统，理解每个组件为什么存在、它的假设是否还成立，都是工程上很重要的习惯。

另一个让我印象深刻的点是 Evaluator 的调教过程。它不是写几行 Prompt 就能用的，而是要反复看日志、找判断偏差、改 Prompt、再看日志。这跟我在做 Agent 评估时的体验一致，评估系统本身就是一个需要持续迭代的产品。

有趣的是，这套架构和 OpenAI 最近在 Codex 上做的方向形成了对照。Codex 更偏“单 Agent + 强上下文管理”路线，Anthropic 走的是“多 Agent 分工 + 外部反馈”路线。两条路各有取舍：单 Agent 更简单、更便宜，多 Agent 在复杂任务上的上限更高但成本也高得多。$124 做一个 DAW 和 $9 做一个游戏编辑器，差距不只是价格，更是产出质量的级别差异。

模型在变强，Harness 在变简单，但“找到下一个有效的 Agent 组合”这件事不会消失。用 Prithvi 的话说：“有意思的 Harness 组合空间不会随模型进步而缩小，它只是在移动。”

---

相关资源：

- 原文链接：<https://www.anthropic.com/engineering/harness-design-long-running-apps>
- 前作《长时间 Agent Harness》：<https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- Frontend Design Skill：<https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md>
- 上下文工程：<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Building Effective Agents：<https://www.anthropic.com/research/building-effective-agents>
