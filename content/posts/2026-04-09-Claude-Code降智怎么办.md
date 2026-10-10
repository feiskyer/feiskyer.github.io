---
title: "Claude Code 降智怎么办?这几个配置救回来"
date: 2026-04-09T10:00:00+08:00
draft: false
tags: [AI, Claude Code, AI 编程]
description: "Claude Code 最近变笨了？原因是 adaptive thinking 自作主张减少思考量，加上默认 effort 从 high 降到 medium。本文给出 /effort max 和环境变量配置，把推理深度调回来。"
---

最近用 Claude Code 写代码，总觉得哪里不对。

我的 CLAUDE.md 里写得很清楚：每次开发完成后，先跑单元测试,再跑 e2e 测试。这个要求跟了我好几个月，之前一直好好的。但最近两三周，e2e 测试愣是不跑。单元测试做完，它就活干完开始总结了。

我以为是提示词不够明确，又在每个任务最后都加了一行“e2e 测试必须执行，不能跳过”这样的提示词。结果还是没用。最后变成每次单元测试跑完，手动再输一句“跑 e2e”，它才肯动。

一开始以为是自己的问题。直到前几天 Hacker News 上炸了一个帖子，才知道不止我一个人。

有人分析了 Claude Code 的 thinking 深度，发现从 2 月底开始下降了 67% 。Claude Code 的作者 Boris Cherny 在 HN 上亲自回复了。他把问题拆成了两个原因。

第一个是 adaptive thinking。Opus 4.6 上线后默认启用了自适应思考，模型自己决定每一轮想多久。听起来更高效，但它经常判断失误。觉得这个任务简单，少想一点就行，该深入的地方直接跳过。

Boris 后来进一步确认：有用户已经设了 effort=high，但 adaptive thinking 仍然在某些轮次分配了零思考 token。零思考，直接出现幻觉了。

第二个是 effort 默认值。3 月 3 号开始，Claude Code 把默认 effort 从 high 降到了 medium。Boris 说这是成本-延迟曲线上的最佳点。但对需要深度推理的任务，这就不够了。

知道原因，解决起来不复杂。

最简单的办法是输入 /effort high，想更激进可以 /effort max。

但光调 effort 不够，核心问题是 adaptive thinking 会自作主张降低思考量。关掉它需要设环境变量：CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1。

你可以在 ~/.claude/settings.json 里一次性配好这两个配置:

```json
{
  "env": {
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1"
  }
}
```

这样每次启动自动生效。

顺便提一个反直觉的坑：ULTRATHINK 触发的是 high effort，不是 max。如果你已经设了 /effort max，加 ULTRATHINK 反而会降低那一轮的 effort。

我自己设完这套配置后，e2e 被跳过的情况少了不少。从每次都跳变成偶尔还会跳。不能说完全解决，但至少不用每次手动催了。

如果你也觉得最近 Claude Code 不太对劲，先试试上面那几个配置。

相关资源

- Boris 在 HN 的回复:<https://news.ycombinator.com/item?id=47664442>
- 原始 issue 讨论:<https://news.ycombinator.com/item?id=47660925>
- Claude Code 设置文档:<https://code.claude.com/docs/en/settings>
