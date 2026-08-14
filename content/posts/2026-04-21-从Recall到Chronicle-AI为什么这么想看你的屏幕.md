---
title: "从 Recall 到 Chronicle：AI 为什么这么想看你的屏幕?"
date: 2026-04-21T10:00:00+08:00
draft: false
tags: [Codex, Claude Code, AI 记忆, Chronicle, Auto Memory]
description: "从微软 Recall 到 OpenAI Codex 的 Chronicle，AI 为何执着于持续截取你的屏幕？本文对比 Chronicle 的读屏记忆与 Claude Code 的 Auto Memory 两条路线，剖析上下文争夺战背后的隐私风险与产品逻辑。"
---

还记得去年 Recall 的翻车吗？让 AI 每隔几秒截一次屏，记住关于你的一切，结果截屏未加密存储，最后不得不下架。

现在 OpenAI 在 Codex 中推出了一个类似的功能 Chronicle，让 AI 持续盯着你的屏幕，持续构建和更新关于你的记忆。

## Chronicle 做了什么

Chronicle 是 Codex 的一个实验性功能，目前只对 Pro 订阅用户和 Mac 用户开放。在 Codex 设置里打开 Chronicle research preview 开关，状态变成 Running，它就开始工作了。

![Chronicle 配置界面](/images/2026-04-21-RecallChronicle-AI-2026-04-21-chronicle-settings.jpg)

开启之后，它会在后台定期截取你的屏幕内容，把截图发到 OpenAI 服务器跑一遍 OCR 和视觉分析，提取出文字摘要，再存回你本地的一个 Markdown 文件里。

想象空间确实挺大的。你在浏览器里查了一篇文档，切到编辑器写了几行代码，又去 Slack 回了条消息，这些 Chronicle 都看得到。下次你跟 Codex 对话的时候，不用再花时间解释我刚才在干什么，因为它早就已经知道了。

Codex 的产品负责人 Tibo 说 Chronicle 改变了他和很多 OpenAI 员工使用 Codex 的方式。说白了，OpenAI 想让 Codex 从一个编码工具变成一个全能的 Super App，Chronicle 就是这个方向上的关键一步，让 Codex 能感知到你整个工作环境。

但这里有个问题。

## 截图去了哪

Chronicle 整体的工作流程比想象中复杂，下面这张图拆解得比较清楚：

![Chronicle 工作原理](/images/2026-04-21-RecallChronicle-AI-2026-04-21-chronicle-architectur.jpg)

简单说，数据流是这样的：

1. 后台定期截屏，临时存在 `$TMPDIR/chronicle/screen_recording/`，6 小时后自动删除
2. 截图发送到 OpenAI 服务器，进行 OCR 和视觉分析
3. 分析结果经过多阶段的提炼和整合，最终以 Markdown 格式存回本地 `~/.codex/memories_extensions/chronicle/`

OpenAI 文档明确指出，截图处理完就删掉，不会用于训练。但有几个细节值得注意。

本地存储的记忆文件是未加密的 Markdown，任何有文件系统访问权限的程序都能读。有意思的是，Recall 翻车之后重新上线时加了不少安全措施：加密数据库、Windows Hello 认证、敏感信息自动过滤（信用卡号、身份证等）。Chronicle 发布的时候，这些一个都没有。

不过这些还不是最让我在意的。更值得警惕的是 prompt injection 的攻击面被大幅扩大了：你打开一个恶意网页，网页里藏了一段指令，Chronicle 截屏后发给 AI 分析，这段指令就可能被执行。以前攻击者只能通过你主动输入的内容来注入指令，现在你屏幕上出现过的一切都是潜在的攻击入口。

OpenAI 的建议是什么？开会前或查看敏感内容前，手动暂停 Chronicle。

不过这就有个明显的问题了，如果系统需要用户自己记得在关键时刻关掉它，那这个系统的设计本身就有问题。

## 另一条路：Claude Code 怎么做记忆

同样是解决 AI 不记得你在干什么这个问题，Anthropic 走了一条完全不同的路。

Claude Code 的 Auto Memory 不看你的屏幕，也不截图。它只从你和它的对话中学习。当你纠正了它的一个错误、当你表达了某个偏好、当一个 debug 过程走完了，Claude 会判断哪些信息值得记住，然后写进本地的 `MEMORY.md` 文件。

两个产品的思路差别挺大的。Chronicle 想做一个全知全能的助手，持续观察你的整个桌面活动，浏览器查的文档、编辑器里的代码、Slack 里的讨论，它全都能关联起来。这种跨应用的上下文理解是 Auto Memory 做不到的。但代价是你的截图得先过一遍 OpenAI 的服务器，隐私边界从一开始就是模糊的。

Auto Memory 正好反过来，只从对话里提炼，全程不碰你的屏幕。记忆文件就是本地的 Markdown，想删就删，想改就改。代价是 Claude Code 只能记住对话里的东西，对话之外的活动它一无所知。用个不太严谨的类比，Chronicle 像是装了个监控摄像头，Auto Memory 像是发了一本笔记本让它自己记。

## 为什么 AI 都想看你的屏幕

Recall、Chronicle，加上之前的 Rewind AI（被 Meta 收购后直接关了 Mac 应用），三家公司在不同时间点做了同一个决策：让 AI 看用户的屏幕。

这不是巧合。

做过 AI 编程的你应该有体会：每次开一个新会话，都得重新交代一遍“我在做什么项目、用什么技术栈、之前跑到哪一步了”。我自己用 Claude Code 的时候，复杂项目开头经常要花点时间交代背景信息，有时候还忘了说某个关键细节，结果 Claude Code 给出的方案就跑偏了。这个冷启动的成本，用得越深越明显。

上下文是 AI 最稀缺的资源，模型再聪明，不知道你在干什么就是不知道。而屏幕恰好是信息密度最高的上下文来源，一张截图包含的信息量，远比你打字描述的多得多，编辑器里的代码、浏览器里的文档、终端里的报错，全在一个画面里。我觉得这就是为什么尽管 Recall 被骂得那么惨，OpenAI 还是选择做同样的事。

但这里有个解不开的矛盾：用户想要 AI 懂我，同时又不想 AI 监视我。目前谁也没想出两全的办法。也许等端侧模型足够强，截屏和分析都能在本地完成的时候，这个矛盾才有可能真正化解。

GitHub 上有个叫 Screenpipe 的开源项目，做的事情跟 Chronicle 类似，但完全在本地处理。截屏、OCR、记忆生成，全部跑在你自己的机器上，不上传任何数据。18000 多个 star，说明这个需求是真实的，但用户对怎么实现有自己的判断。

## 写在最后

回到开头的问题：Recall 搞砸了，为什么 OpenAI 还要做 Chronicle？因为上下文争夺战才刚开始。

不只是 OpenAI 和 Anthropic，Google 在最新发布的 Gemini Mac App 里也加了读屏功能。每家都在赌同一件事：AI 的终局不是一个更聪明的聊天框，而是一个真正理解你工作的搭档。问题在于，这个搭档需要时刻盯你的屏幕才能做到吗？

---

**相关资源：**

- Codex Chronicle 官方文档：<https://developers.openai.com/codex/memories/chronicle>
- Claude Code Memory 文档：<https://code.claude.com/docs/en/memory>
- Greg Brockman 发布推文：<https://x.com/gdb/status/2046293955009274019>
- Screenpipe（开源本地方案）：<https://github.com/mediar-ai/screenpipe>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
