---
title: "Codex /goal 上线后，我把 Ralph loop 卸了"
date: 2026-05-08T10:00:00+08:00
draft: false
tags: [AI, Codex, GPT-5.5, AI Agent, 长时任务, Ralph Loop]
description: "Codex 新增的 /goal 命令搭配 GPT-5.5，让长时任务第一次变得丝滑可托付。本文解析 /goal 状态持久化、权限控制、自审注入的三层设计，对比 Ralph loop 的痛点，并分享适合跑 Goal 的任务类型与工作流。"
---

强烈推荐一下 Codex 的 `/goal` 命令。搭配 GPT-5.5，我第一次感受到长时任务可以完成得这么丝滑。

之前用 Claude Code + Ralph loop 跑长任务，总是各种各样的问题：跑着跑着模型自己宣布胜利了，明明任务清单还有大半没做；状态文件越写越离谱，跨会话后新 Agent 看到的进度跟实际对不上；偶尔卡住，整套循环死在那里。社区里很多人也有同感，有人说自己用 Ralph loop 最长跑 3 小时就失控，中间得不停盯着；使用成本也是巨高，每轮循环都要重新读一遍代码库，token 消耗比正常操作高出很多。

上周升级 Codex 用上了新增的 Goal 命令，Greg Brockman 发推说“codex now has a built in Ralph loop++”。试了几天，太丝滑了，把 Ralph loop 卸了。今天就来给大家分享下它的用法。

## /goal 怎么用

首先编辑 `~/.codex/config.toml` 开启这个功能特性：

```toml
[features]
goals = true
```

然后给它一个目标就可以等着它帮你干完了，比如：

```
/goal 把仓库里所有 axios 调用迁移到 fetch,要求:
1. 所有现存测试通过
2. 类型签名不变
3. 错误处理行为等价(4xx/5xx 都要 throw)
4. 完成后跑一遍 npm run build 和 npm test 确认
```

跟普通对话的区别就一条：每轮结束后 Codex 不停，自己接着干下一轮，直到目标达成。TUI 上有个进度面板，显示当前状态（pursuing / complete / paused）和 token 用量。你可以全程不看它的进度。

运行过程中可以用 `/goal` 查看状态，用 `/goal pause` 暂停，`/goal resume` 恢复，`/goal clear` 清除。

## /goal 的三层设计

最开始我以为 /goal 就是把 Ralph loop 照搬到了 Codex 里面来。翻了 GitHub 源码才发现，这个设计比 Ralph loop 更进一步，如下图所示：

![/goal 运行原理](/images/2026-05-08-codex-goal-goal-architecture-compressed.jpg)

最底层是状态持久化。Codex 把 Goal 状态写进 state-db（源码在 `codex-rs/core/src/goals.rs`），可能的值是 `pursuing` / `paused` / `complete` / `unmet` / `budget_limited`。你中途退出再打开，Goal 还在，还可以接着跑。Ralph loop 脚本挂了虽然磁盘文件还在，但得手动重启、重新接上上下文。

中间层是权限控制。Codex 给模型三个工具：`get_goal`、`create_goal`、`update_goal`，但 `update_goal` 的状态参数只接受一个值：`complete`。模型能宣布“我搞定了”，但不能说“预算快没了我撤了”。断了它的退路，要么真做完，要么继续干。

最上层是自审注入。每轮执行时，运行时注入 `continuation.md` 里一段 prompt，强制模型把目标拆成检查清单，逐项对照真实文件和测试结果。最关键的一句：

> Do not call update_goal unless the goal is complete. Do not mark a goal complete merely because the budget is nearly exhausted or because you are stopping work.

直接避免了我之前 Ralph loop 里最常碰到的问题：模型为了脱身硬说基本完成了。

把三层放在一起看，Ralph loop 只是让模型反复跑，/goal 让模型反复跑的同时不停反问自己“我真的做完了吗”。

## GPT-5.5 + 100% confident loop

光有 /goal 还不够，模型还需要足够强大。

GPT-5.5 是少数会主动质疑自己的模型。/goal 的自审提示对一个不爱质疑自己的模型就是耳旁风，对 5.5 是放大器。并且 GPT-5.5 也没有之前 GPT 模型那种总是很懒的感觉了，你想不到的它也可以帮你想到了。

对比一下 Opus 4.7。你说“再检查一遍”，它说“你说得对”，然后说一堆早想好的话。你说“这有 bug”，它说“绝对的，我重写”，然后小幅改一下交回来。讨好型选手，跑长任务越跑越偏。而 GPT-5.5 不一样，让它再查一遍，它真会去 grep、跑测试、对照 spec，然后告诉你哪里还有边界情况。

社区里有个配套 prompt 传得很广：

> Are you 100% confident in this strategy? If not, find all possible loopholes, suggest proper fixes and run this loop until you are factually 100% confident in the new strategy.

关键是让 5.5 自己开循环：找漏洞、提修复、再问自己一次。这招在 Opus 上完全不好使，它把自查当客套环节，5.5 当成一份正经工作。

我推荐的工作流是：先写 SPEC.md（或者任何保存到文件的目标任务），用这个 prompt 自审一遍，SPEC.md 没问题了再 `/goal` 启动执行，完成后做 QA。

按这个流程，Codex 连续干十几个小时完全不是问题（如果你的 token 足够，更长应该也完全没问题）。

## 什么任务适合

判断标准就一个：你能不能把“做完了”写清楚。能写清楚，/goal 就可以跑的很多；写不清楚，跑出来也可能是垃圾。官方文档的说法是，好的 Goal 应该定义清楚四件事：要达成什么、不能动什么、怎么验证进度、什么时候停。

我自己跑下来，Goal 比较适合这几类场景：

**代码迁移和大型重构**。有明确的目标状态，有验收手段（ build 通过 + 测试通过 + e2e 通过）。比如：

```md
/goal Migrate this project from [legacy stack] to [target stack]. Make sure all screens stay exactly the same visually, using playwright interactive to verify the output.
```

**原型和游戏开发**。写一份 PLAN.md 描述你要什么，然后让 Codex 实现它。Codex 会按里程碑推进，每个节点跑测试确认。

```md
/goal Implement PLAN.md, creating tests for each milestone and verifying the output with playwright interactive
```

**Prompt 优化**。如果你有 eval 套件，可以让 Codex 自己迭代，做实验、看结果、调参数，循环到收敛。比如：

```md
/goal Optimize the prompts in [prompt file] until the eval suite reaches [target score]. After each change, run [eval command], inspect the failing cases, and keep the prompt edits minimal and targeted.
```

**夜间 QA 和批量处理**。回归测试、数据校验、批量文件处理这类机械但耗时的活，丢给 /goal 过夜跑。

## 写在最后

回到开头说的那个问题：长时任务为什么一直不稳？

我之前开发 autonomous-skill 的时候，思路跟 Ralph loop 其实一样，都是在模型外面套一个逼它继续干活的循环。跑了大半年，我逐渐意识到问题不在循环本身，而在模型。模型没有自查能力的话，再套多少层也只是把错误重复 N 次。你可以逼它继续干，但你逼不了它承认自己没干好。

/goal 解决的恰恰是这一层。运行时不让模型耍赖，GPT-5.5 又真的会自查，两条腿一起走，长时任务才第一次变成可以托付的事情。

当然 /goal 也不是万能的。目标写不清楚的任务它照样跑偏，需要频繁跟人确认方向的任务它也不适合。不过对于那些验收标准明确、可以自动化验证的工作，它确实把盯着 Agent 干活这件事变成了睡一觉起来看结果。这个体验的差距，用过就知道了。

---

相关链接：

- Codex /goal 官方文档：<https://developers.openai.com/codex/use-cases/follow-goals>
- Codex GitHub 源码：<https://github.com/openai/codex>
