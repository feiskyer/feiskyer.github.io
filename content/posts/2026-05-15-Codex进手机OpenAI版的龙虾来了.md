---
title: "Codex 进手机：OpenAI 版的龙虾来了"
date: 2026-05-15T10:00:00+08:00
draft: false
tags: [AI Agent, Codex, OpenClaw, Claude Code, 异步编程]
description: "OpenAI 发布 Codex Mobile 预览版，让 ChatGPT 手机端远程接管本地 Codex 桌面客户端。本文详解连接配置流程，并对比 Claude Code Remote Control 的架构与用量差异，聊聊移动端异步编程的真正价值。"
---

每周 400 万人在使用的 Codex 桌面客户端，从今天起，都可以在手机 ChatGPT 客户端远程接管了。

OpenAI 今天凌晨发布了 Codex Mobile 预览版，让 ChatGPT 移动客户端可以直接控制本地的 Codex 桌面客户端。架构跟 Anthropic 三个月前推的 Claude Code Remote Control 几乎一样，但解决问题的方向恰好相反。

## 怎么连，怎么用

Codex Mobile 不是把 Codex 跑到云端，也不是远程桌面投屏。你 Mac 上的 Codex 桌面客户端还在 Mac 上跑，移动端通过 OpenAI 的 secure relay 同步状态。文件、credentials、本地配置都不动，移动端看到的是任务进度、终端输出、diff、截图。

设置流程比想象的还简单。Codex 桌面客户端升级后，侧边栏多一个 “设置 Codex 移动版” 选项，点开会显示二维码。

![桌面端设置入口](/images/2026-05-15-CodexOpenAI-setup-qrcode.jpg)

但你不用扫码。打开手机上的 ChatGPT 移动客户端，它会自动识别到同账号下有 Codex 桌面客户端在等你确认，弹一个授权提示。

![手机端授权](/images/2026-05-15-CodexOpenAI-setup-authorize.jpg)

点授权此手机，桌面端立刻显示“已连接”，下面还有三个开关进一步控制权限：让电脑保持唤醒、启用 Computer Use、装 Chrome 扩展。

![桌面端已连接](/images/2026-05-15-CodexOpenAI-setup-connected.jpg)

整个过程不到一分钟。同账号下多台机器都能管，桌面端和移动端共享同一个 thread，不用来回粘贴上下文。

## 跟 Claude Code Remote Control 比

Claude Code 早在三个月前就推出了 [Remote Control](https://code.claude.com/docs/en/remote-control)，OpenAI 显然又是一个跟随者。架构几乎一样：本地跑 Claude Code，移动端做窗口，云端 relay 中转，桌面端和移动端共享同一会话。

这两个我都尝试过一些任务。从体感上看，Codex Mobile 跟 Claude Code Remote Control 差不多，主要区别不在功能，而在用量这件事上。

Claude Code 的 5 小时窗口是真的不够用，复杂任务几分钟就能把额度跑光。虽然 Anthropic 最近宣布了 5 小时配额加倍和周配额提升 50% ，但社区里普遍反馈差别不太明显。

反观 Codex 的限额政策一直比较大方，ChatGPT Pro 订阅很少会撞到上限不说，免费版甚至也能用 5.5 Extra High。对于 AI 编程重度用户来说，订阅 ChatGPT 要比 Claude 划算的多，更不用说 Claude 那畸形的封号策略了。

当然 Codex 移动端也有很多限制，比如现在只支持 macOS 上的 Codex 桌面客户端，不支持 Windows，高峰时间稳定性也有待提升。

## 写在最后

看到 Codex 移动端发布，第一时间想到的是 OpenAI 版的龙虾终于来了。OpenClaw 爆火这么长时间，各家 Agent 产品能抄的都已经抄过去了。现在 OpenClaw 热度都过去了，OpenAI 才姗姗来迟。

话说回来，不要被“在手机上写代码”这个画面骗到。Codex 的功能并不仅限于编程，它真正适合的场景，不只是让你掏出手机指挥电脑敲代码，更重要的是让你不在电脑前也能推进任务。正如 OpenAI 的 slogan 所说，“Touch grass and leave your laptop”，Codex 移动端不是替代你坐在电脑前的工作，而是让你不用一直守着电脑等 AI 跑完任务。

---

相关资源：

- OpenAI Codex Mobile 官方博客：<https://openai.com/index/work-with-codex-from-anywhere/>
- Claude Code Remote Control 文档：<https://code.claude.com/docs/en/remote-control>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
