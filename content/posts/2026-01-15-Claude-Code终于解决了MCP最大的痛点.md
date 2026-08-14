---
title: "Claude Code 终于解决了 MCP 最大的痛点"
date: 2026-01-15T10:00:00+08:00
draft: false
tags: [AI, Claude Code, MCP, AI Agent]
description: "Claude Code 新增 MCP Tool Search，用懒加载解决 MCP 工具定义预先占满上下文窗口的老问题。本文解析工具搜索的触发阈值与工作流程，对比 Skills 与 MCP 的分工差异，并给出 MCP 服务器开发者打磨 server instructions 的建议。"
---

用 Claude Code 配了多个 MCP 服务器的朋友，应该都遇到过这个问题：还没开始干活，上下文窗口就被吃掉一大半了。

比如，之前我分享过，只配 GitHub、Playwright、Context7 这几个常用的 MCP 服务器，用 /context 查看，就会发现对话还没开始，Context 就被用掉 1/3 了：

![image-20260115182002599](/images/2026-01-15-Claude-CodeMCP-image-20260115182002599.png)

Claude Code 的官方 Github 有一个 Lazy Loading for MCP Servers and Tools 的 Issue（Issue ID #7336），作者的 MCP 工具占用更夸张，默认的上下文占用达到了 54% ，留给真正干活的只有 92k token 了。

今天， Anthropic 终于出手修复这个问题了，在最新的 Claude Code 中推出了 MCP Tool Search 功能，实现了 MCP 工具的懒加载。

## MCP 的问题

上下文占用可以说是 AI Agent 想要用好 MCP 工具的最大障碍：MCP 工具越多、AI Agent 能做的事情越多，按说功能也就越强大。

问题在于 MCP 有个设计特点，所有工具的定义都要预先加载到上下文窗口里。工具名称、参数说明、功能描述，一股脑塞进去。这样 AI Agent 才知道有哪些工具可用、每个工具怎么调用。

一个 MCP 服务器可能有几个到几十个工具，每个工具的描述占用几百到上千 tokens。MCP 服务器一多，开销就很可观了。

这算是协议层面的设计债务。MCP 最初设计时，可能没预料到用户会这么能装。工具少的时候，预加载没什么问题。当工具数量达到几十甚至上百个，上下文占用、工具调用不准确、参数格式错误等诸多问题就暴露了。

社区里有人调侃，MCP 让 AI 变得更强大了，也让它的“脑容量”变小了。这话说得很形象。

## Tool Search 来了

Anthropic 的解决方案叫 Tool Search，不再一开始就加载所有工具定义，而是按需发现工具，这样 Agent 只会看到当前任务实际需要的工具。

![Tool Search Tool diagram](/images/2026-01-15-Claude-CodeMCP-image-20260115185407735.png)

有了工具搜索后，Claude Code 现在会检测 MCP 工具描述是否超过上下文的 10% 。超过了，就自动切换到搜索模式。工具定义不再预加载，需要的时候通过搜索来找。

工作流程大概是这样的：启动时只加载一个轻量的工具索引，你提任务时 Claude Code 根据任务内容搜索相关工具，被搜到的工具才会加载到上下文里。搜索支持关键词匹配和相似度匹配，Claude Code 可以多次搜索、调整关键词，甚至并行搜索多个关键词来找最合适的工具。

如果你的 MCP 工具描述没超过 10% 阈值，一切照常，不会有任何变化。这个设计挺聪明的，只在真正需要的时候才介入，不影响轻量级用户的体验。

Anthropic 的工程师 Thariq 在 X 上解释了技术细节。因为 Claude Code 完全在客户端运行，他们实现了一个自定义的搜索工具。接收关键词，在工具库里做相似度搜索，返回最相关的工具列表。搜索本身也是一个普通的工具调用，所以 Claude 有足够的灵活性来找到合适的工具。

## 和 Skills 有什么不同

聊到懒加载，可能有人会问：这不是 Skills 早就实现的功能吗？

确实，Anthropic 去年 10 月推出的 Skills 系统天生就是懒加载的。每个 Skill 只需要少数 tokens 来描述自己是干什么的，完整的指令和脚本只在需要的时候才加载。

两者的核心区别在于解决的问题不同。

**Skills 是教 Claude Code 怎么做事**。Skills 是一个 Markdown 文件 + 可选的脚本，可以告诉 Claude Code 遇到某类任务时应该怎么处理。比如 slack-gif-creator 这个 Skill，教 Claude 怎么用 Python 生成符合 Slack 尺寸限制的 GIF。Skills 不会给 Claude 增加新工具，它只是让 Claude 更聪明地使用已有的工具，比如 bash、文件读写这些（你在 Skills 里面写的各种脚本实际上都是 Bash 工具调用）。

**MCP 是给 Claude Code 新能力**。通过 MCP 服务器，Claude 可以直接调用外部 API、访问数据库、操作第三方服务。这些是 Claude Code 本身做不到的事情。

换句话说，Skills 像是给 Claude Code 一本操作手册，MCP 像是给 Claude Code 配了一套新装备。

有意思的是，Skills 内部其实可以调用 MCP 工具，也可以通过脚本程序来实现自己的逻辑（比如可以包含任何能被终端调用的命令）。这让 Skills 的灵活性大大增加。很多开发者发现，与其忍受 MCP 的上下文开销，不如把同样的功能用 Skill 包一层，效果一样，上下文占用却小得多。

正因为如此，Skills 一经发布就火了。Cursor、Github Copilot、Codex CLI 这些 AI 编程工具纷纷跟进，推出了类似的机制。社区里甚至出现了一波 MCP 转 Skill 的风潮，把原本用 MCP 实现的功能用 Skills 重写。

不过 Tool Search 出来之后，MCP 的上下文效率大幅提升，和 Skills 的差距缩小了很多。两者现在更像是互补关系：需要调用外部能力用 MCP，需要教 Claude 怎么做复杂任务用 Skills。

## 对你意味着什么

如果你只是 Claude Code 的普通用户，不用做任何事情。Tool Search 会自动生效，你只会感觉到上下文变大了，能跑更复杂的任务了。

如果你是 MCP 服务器的开发者，有一点值得注意。**server instructions 字段变得更重要了**。

在 Tool Search 模式下，Claude Code 需要知道什么时候应该搜索你的工具。server instructions 就是告诉 Claude Code 我这个服务器能干什么的地方。写得好，Claude Code 就更容易在合适的时机找到你的工具；写得不好，你的工具可能就被埋没了。

这有点像 SEO。以前工具都摆在明面上，现在需要让工具能被搜到。开发 MCP 服务器的朋友，该好好打磨一下 server instructions 了。

除此之外，程序化 MCP 工具调用也是很多人期待的一个功能。简单说就是通过编程动态调用 MCP 工具，并让 MCP 工具能够通过代码相互组合。Thariq 说他们探索过这个方向，觉得先把 Tool Search 做出来解决上下文问题更紧迫。程序化调用可能是下一步。

---

**相关资源**

- Tool Search 官方文档 <https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool>

- GitHub Issue Lazy Loading for MCP Servers #7336 <https://github.com/anthropics/claude-code/issues/7336>

- Thariq 的公告推文 <https://x.com/thariq212/status/2011523109871108570>

- Introducing advanced tool use on the Claude Developer Platform: <https://www.anthropic.com/engineering/advanced-tool-use>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
