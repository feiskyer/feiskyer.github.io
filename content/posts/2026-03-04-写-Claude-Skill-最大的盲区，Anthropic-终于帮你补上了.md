---
title: "写 Claude Skill 最大的盲区，Anthropic 终于帮你补上了"
date: 2026-03-04T10:00:00+08:00
draft: false
tags: [Claude Code, Skill, Agent, 测试]
description: "Anthropic 更新 skill-creator，把软件工程的测试、基准评估和迭代改进搬进 Skill 开发。本文讲解如何用 eval 取代凭感觉判断，验证 Skill 是否真正起作用、判断触发时机并做多 Agent 并行 A/B 对比。"
---

> 题记：本文编译自 Anthropic 官方博客《Improving skill-creator: Test, measure, and refine Agent Skills》，原文链接：<https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills>。本文在翻译基础上做了整理和补充。

写了几十个 Claude Skill 之后，我最大的困惑不是怎么写，而是它到底有没有用。每次写完一个 Skill，扔到 `.claude/skills/` 目录里，然后就开始凭感觉判断效果了。有时候觉得有用，过两天再看结果好像又变差了，不确定是 Skill 在起作用，还是模型本来的随机行为导致的。更麻烦的是，Claude 每次更新之后，原来好用的 Skill 会不会悄悄失效，完全不知道。

这个困惑应该不只我一个人有。写 Skill 的人大多不是工程师，清楚自己的工作流程，但缺少工具来验证 Skill 到底有没有在起作用。昨天 Anthropic 更新了 skill-creator（《[Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)》），核心思路是把软件工程那套东西搬过来，测试、基准评估、迭代改进，但不需要写代码。

Claude Code 用户可以直接执行下面的命令安装：

```bash
claude plugin install skill-creator
```

Claude.ai 和 Cowork 里直接跟 Claude 说用 skill-creator 创建想要的 SKILL 就行。

## 先搞清楚你在写哪种 Skill

在聊测试之前，有一个框架我觉得挺有价值的，可以帮你在下笔之前想清楚一件事。

Anthropic 把 Skill 分成了两种，回头一想，确实是这么回事。

第一种是能力补充型，给模型添加它本来做不好的能力。Claude 官方提供的文档生成类 Skill 是个典型的例子，里面编码了一套技巧和模式，生成结果比直接提示词好得多。模型没有这个 Skill，就达不到这个效果。

第二种是流程编排型，模型原本就能处理每个环节，但 Skill 把这些环节按照团队规范串联起来，给的是“用什么顺序做什么事”这样的约束。NDA 审查、每周报告生成这类 Skill 属于这种。

这个区分对设计 Skill 很有参考价值：能力补充型有个隐患，随着模型变强，它可能会慢慢变得多余，甚至是限制 Claude 的能力。这有点像你精心写了一本新员工培训手册，结果新来的人比老员工还熟练，手册自然就没人翻了。如果有测试，你能及时发现“这个 Skill 已经完成历史使命了”，而不是一直带着一个没用的包袱。

流程编排型更耐用，但价值完全依赖于流程的严格执行，测试的重点是验证它有没有按预定顺序走完每一步。

写之前先想清楚自己在写哪种，测试策略和预期生命周期都不一样。

## 用 eval 取代感觉

skill-creator 现在可以帮你写 eval。形式也很简单，你给出测试提示词，描述期望的行为，然后让 skill-creator 判断你的 Skill 是否经得住检验。做过软件测试的人会觉得这个模式很熟悉，区别是不用写代码，用自然语言描述预期结果就够了。

比如 PDF Skill，以前处理不可填写的表单时经常出错，原因是 Claude 需要在没有字段定义的情况下精确定位文字放置位置。写了 eval 之后，才定位到这个具体失败点，最后通过把定位锚定到提取出来的文字坐标解决了问题。如果没有 eval，这个 bug 可能就一直隐藏着，每次遇到不可填写的表单就悄悄出问题。

![PDF Skill 处理不可填写表单的改进前后对比，改进前文字错位，改进后各字段填写到位](/images/2026-03-04-Claude-Skill-Anthropic-69a237b02128b691d9e8b2af_skillsc.png)

eval 最直接的价值是捕捉质量回归。模型升级或周边基础设施变动之后，原本好用的 Skill 可能行为发生变化。在变化影响到实际工作流之前，eval 能提前给你预警。

不过还有一个更微妙的用途，即判断 Skill 是否还有存在的必要。对于能力补充型 Skill 来说，如果基础模型不加载 Skill 就能通过 eval，说明这些技巧已经被模型内化了，Skill 不是坏了，只是完成使命了。这个信号你只能靠测试发现，靠感觉永远看不出来。

更新里还加了 benchmark 模式，可以跑标准化评估，跟踪 eval 通过率、耗时和 token 用量。数据保存在本地，可以集成到 dashboard 或 CI 系统里。

![benchmark 模式输出的评估报告，对比加载 Skill 与不加载 Skill 的通过率、耗时和 token 用量](/images/2026-03-04-Claude-Skill-Anthropic-69a237f15fbc61e1ccd00a0a_skillsc.png)

## 多 Agent 并行

之前 eval 是顺序执行的，速度慢不说，测试之间上下文还会互相污染。前一个测试的内容可能影响到后一个的判断。现在 skill-creator 支持多 Agent 并行跑 eval，每个 Agent 在独立的上下文里运行，有各自的 token 和耗时统计，互不干扰。

另外还加了 comparator agent，用来做 A/B 对比：两个版本的 Skill 对比，或者 Skill vs 不加 Skill。有点像双盲实验，负责评判的 Agent 不知道自己看的是哪个版本的输出，尽量排除评估偏差。这个设计基本解决了“我觉得改好了，但其实不知道”的问题。

![A/B 测试流程图，加载 Skill 与不加载 Skill 的两个执行 Agent 输出交给 comparator 双盲评判并给出结论](/images/2026-03-04-Claude-Skill-Anthropic-69a74e0afa8435f070120ed9_skillsc.png)

## 触发时机最容易被忽略

输出质量测完了，是不是就够了？不一定。Skill 首先得在对的时候触发才有意义。这是我自己写 Skill 时踩得最多的地方：描述写得太宽，每次稍微相关的请求都会触发；描述写得太窄，只有完全匹配的词才会触发，平时根本用不上。两种情况都让人头疼。

skill-creator 现在能分析当前的 Skill 描述，对照一组测试提示词，推荐修改来减少误触发和漏触发。Anthropic 测试了 6 个公共文档创建类 Skill，有 5 个的触发精度通过这个方法得到了改善。

![Skill 描述优化效果柱状图，pdf、docx、pptx、xlsx 等 Skill 优化描述后的触发准确率对比](/images/2026-03-04-Claude-Skill-Anthropic-69a74e1f72940942cb534904_skillsc.png)

说实话，这个功能我觉得是这次更新里最实用的，因为触发问题是最隐蔽的。你写的逻辑完全正确，但描述没有匹配到用户的表达方式，Skill 就等于白写了。

## 设计 eval 其实是在把期望说清楚

看完这次更新，我对 Skill 写作有了一个新认识：设计 eval 的过程，本质上是在逼你把“期望什么行为”说清楚。很多时候 Skill 效果差，不是因为提示词写得不好，而是作者自己也没想清楚什么叫成功。当你被迫用语言描述“在这个输入下，Claude 应该做到什么”，很多模糊的预期就会浮出水面。

Anthropic 还提到了一个有意思的预判：随着模型越来越强，Skill 和 spec 之间的边界可能会模糊。现在的 SKILL.md 本质上是实现计划，在告诉 Claude 怎么做事。以后也许只需要描述你想要什么，模型自己搞清楚怎么做。eval 框架恰好在往这个方向走，eval 描述的是 what，也就是期望的结果。某种程度上，这个描述本身可能就是未来形态的 Skill。

如果你也在写 Skill，下次不妨少靠感觉，给它加个 eval 验一验。不需要多复杂，一条提示词、一段预期描述就够了。跑一遍，可能会发现一些你没意识到的问题。

---

**相关资源**

- skill-creator 插件：<https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator>
- Anthropic 官方 Skills 仓库：<https://github.com/anthropics/skills>
- 原文链接：<https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills>
