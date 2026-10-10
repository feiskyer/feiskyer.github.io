---
title: "Loop Engineering 很好，但先想清楚一个问题"
date: 2026-06-10T10:00:00+08:00
draft: false
tags: [AI Agent, Loop Engineering, Claude Code, Codex, 长时任务]
description: "Loop Engineering 火了，但它到底是什么？本文梳理从 ReAct、Ralph loop 到 Codex /goal 的演进，讲清它与定时任务的区别、独立验证为何是关键，以及上 loop 前你必须想清楚的那个朴素问题：能不能把「做完了」写清楚。"
---

这两天一个新的 AI 编程范式 Loop Engineering 火了。Peter Steinberger 发推说你不应该再 prompt coding agent，应该去设计 prompt agent 的 loop，两天冲到 800+ 万阅读。随后 Claude Code 负责人 Boris Cherny 也表达了类似的观点，他管理的几百个 agent 自己读 GitHub 和 Slack、自己决定干什么，过去 30 天合并了 250 多个 PR，全部由 Claude Code 完成。

![image-20260610211044921](/images/2026-06-10-loop-engineering-image-20260610211044921.png)

今天 Anthropic 刚刚发布了最新的 Claude Fable 5 和 Mythos 5 模型，甚至能够把数月的工作压缩至几天内完成。

说实话挺有感触的。上个月 Codex 推出的 /goal 功能其实就是最好用的 Loop Engineering 实现，配合广受好评的 GPT-5.5，工作完成度一下子就把之前经常使用的 Claude Code + Ralph loop 组合拉开了，我自己的大部分工作也都切换到了 Codex 上面来。

但用了几个月之后，我发现 loop 好不好用，其实取决于一个很朴素的问题。这个问题后面会展开，先说说 Loop Engineering 到底是什么。

Loop 说白了就是一个替你 prompt agent 的小系统：给 agent 发任务，读结果，判断做完没有，没做完就继续执行。以前我们用 Claude Code，要靠你自己输入 prompt、盯着输出、中断后再输入，如此循环往复，你就是那个循环。Loop Engineering 则是把你从循环里摘出来，但如何摘出来是个问题。

## 什么是 Loop Engineering

![Loop Engineering 循环流程](/images/2026-06-10-loop-engineering-loop-engineering-cycle.png)

说到 Loop Engineering，我觉得最早可以追溯到 ReAct 模式：你输入提示词后，模型推理、调工具、读结果、循环重复直到没有工具调用时结束。这个循环后面演变成了 AI Agent 最基本的执行过程，是所有 Agent 都必备的基础模块。

不过只有这个循环明显还不够，AI 经常会在执行完一些工具调用后停下来等待你的输入。所以后来就有了 Geoffrey Huntley 的 Ralph loop 模式：通过一行 bash，把同一个 prompt 文件反复发送给 agent 执行，直到模型说工作完成了才停止。

Ralph loop 推出后的确解决了很多长程任务的执行问题，但问题也不少：模型跑着跑着自己宣布胜利，任务清单还剩大半；状态文件越写越离谱，跨会话之后新 agent 看到的进度跟实际对不上；偶尔整个循环还会直接卡死。

后来，Codex 推出了第一个真正可以稳定执行长程任务的功能 /goal，通过状态持久化+权限控制+强制自审三层机制解决了这些问题。详细的实现原理和使用方法可以参考我之前写的《[Codex /goal 上线后，我把 Ralph loop 卸了](https://mp.weixin.qq.com/s/qwjxsGpMacLNy93g6dz4Aw)》，这儿就不展开了。

Claude Code 在随后的版本里也增加了相同的 Goal 功能，不过需要注意 Opus 模型相对 GPT-5.5 还是有差距，效果稍微差一些（Claude Fable 则会好一些）。

## 跟定时任务有什么区别

乍看起来，Loop Engineering 就像是把之前的定时任务改了个名字，底下都是让 AI 大模型不停地执行任务。

但这两者有很大的区别：

* 定时任务的目的是触发任务的执行，执行的时间是固定的。至于到了时间执行啥取决于你给它的指令，可以是脚本、提示词甚至是 Goal 这种复杂的任务目标；
* Loop Engineering 的目的是确保 AI 大模型能够以正确的方法完成你的任务目标，它能够自己查看状态、决定是否执行下一步，循环往复直到目标完成。

在实际使用中，你可以把它们结合在一起来使用。比如，使用定时任务来触发 Github issue 的排查，而在排查每个 issue 时使用 Loop 来确保任务执行的质量。

## 怎么用好 Loop Engineering

那怎么用好 Loop Engineering？

我的建议是，目标写清楚、步骤有边界、每步有检查、有明确的停止点，确保 Agent 能够闭环迭代就可以了。

Cherny 也给过几条建议，可以参考：权限开 auto 模式、让 Claude 自己编排子 agent、用 /goal 模式、跑在云端，以及自我验证。前四条大家都在用，但最重要的其实是最后一条：验证。产出没人查，方向迟早跑偏。

为什么验证这么重要？大模型给自己的产出打分很不可靠，但如果换一个独立上下文的子 agent 来评估，效果就稳定得多。Lance Martin 的测试里（链接见最后），Fable 5 最好的运行有 73% 的结论经过了独立验证，Opus 4.7 中位数只有 17% ，差距主要就在这儿。

这跟我翻 Codex /goal 源码看到的设计思路是一致的。模型能宣布做完，但不能说预算快没了先撤。再配上每轮注入的自审，强制逐项对照真实文件和测试结果。简单来说，你可以逼模型继续干活，但你逼不了它承认自己没干好，能戳穿它的只有独立的验证。

## 写在最后

回到开头说的那个朴素问题：你要不要给手头的事上 loop？判断标准跟我在 /goal 那篇里说的一样：你能不能把“做完了”写清楚。能写清楚，loop 确实能帮你省掉大量重复劳动。但如果连做完的标准都说不清，那还是老老实实一步步来吧。

另外还要提醒一点，Loop Engineering 绕不开一个现实问题：烧 token。跑起来烧钱比你想的快，自修正、验证子 agent、重试，每一步都在消耗 token。说白了，你是 token 富人还是 token 穷人，直接决定了你对 loop 的态度。如果你对 token 消耗比较敏感，建议优先使用订阅制的产品而不是直接调 API，能省不少钱。

如果你想了解更多的 Loop Engineering，推荐阅读：

- Addy Osmani: Loop Engineering：<https://addyosmani.com/blog/loop-engineering/>
- Lance Martin: Designing loops with Fable 5：<https://x.com/RLanceMartin/status/2064397389189071163>
- Boris Cherny 谈自我验证：<https://x.com/bcherny/status/2064426115255730578>
- Codex /goal 上线后，我把 Ralph loop 卸了：<https://mp.weixin.qq.com/s/qwjxsGpMacLNy93g6dz4Aw>
