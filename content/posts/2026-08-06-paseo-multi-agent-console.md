---
title: "Claude Code 用了一年多，我终于受不了它的终端了"
date: 2026-08-06T20:00:00+08:00
draft: false
tags: [AI 编程, Claude Code, Codex, Paseo, 多 Agent, 工具推荐]
description: "用了一年多 Claude Code 后，作者被 TUI 的刷屏和消息审查体验逼到极限，转而使用多 Agent 控制台 Paseo。它不重造 Harness，原生兼容 Claude Code、Codex 等主流 Agent，支持跨设备远程操控和多 Agent 跨 Provider 协作。"
---

Claude Code、Codex CLI 这些 AI 编程工具满打满算也就发布了不到一年半。但就这一年多时间，我们写代码的方式彻底变了。手搓代码快成“非遗”了，一行一行手敲反而成了需要特别标注的“传统编程”。变化快到有点不太真实。

不过工具用得越多，问题也暴露得越明显。其中最让我难受的不是模型能力，而是 TUI 本身。

比如早期的 Claude Code 在长会话时很容易出现终端疯狂刷屏、整个屏幕闪烁、所有历史消息全部重绘这样的问题。会话越长闪得越严重。这个问题被用户吐槽了好几个月，Anthropic 后来做了全屏渲染模式来缓解，但回滚查看历史消息也比之前慢多了。

闪烁还只是表面现象。真正让我烦的是：跑复杂任务的时候，想回头看看之前某一步 Agent 到底做了什么决策，在终端里翻消息简直是噩梦。对简单任务无所谓，但复杂任务往往需要反复审查 Agent 的中间决策，判断它有没有走偏，这就麻烦了。

你在用的时候是不是也有这个感觉？反正我经常碰到。我最近几个月一直在用一个叫 Paseo 的多 Agent 控制台，完美解决了这个问题。用下来感觉不错，分享给你。

## 克制是 Paseo 最大的优点

多 Agent 编排早就不是新鲜事了，开源闭源都冒出来很多项目，比如 Multica、Orca、Mission Control、Paperclip 等等，GitHub 上随便一搜几十上百个。但大部分都有个共同的毛病，都想做自己的 Agent Harness。

自己造 Harness 意味着什么？你的 CLAUDE.md 不生效了，Skills 读不了了，积累的配置和记忆也全部作废了。得在一个全新环境里从零开始教 Agent 干活。我之前试过几个类似的工具，对我用的 memory 格式支持都不好，老是要返工，甚至之前一两个小时的工作它能给我来来回回搞上一天，无奈最后还是回到了 Claude Code。

Paseo 则很克制，原生支持 Claude Code、Codex、OpenCode、Pi，再加上各种 ACP，主流的 Agent 它都可以接入。 Paseo 没有试图替代任何一个。你在 Paseo 里跑 Claude Code，底层就是 Claude Code 本身。CLAUDE.md、Skills、Hooks、MCP servers、memory 全都在，一个不少。说白了就是给 Agent 套了一层更直观易用的壳，灵魂还都原始保留着。

这种克制在当前这个赛道里反而成了最大的优点。切过来零成本，不喜欢随时切回去。

![Paseo 桌面端界面：多个 Agent 在同一个工作区并行，左侧是会话列表，右侧是当前 Agent 的输出](/images/2026-08-06-paseo-multi-agent-console-2026-08-06-paseo-desktop.png)

## TUI 的问题它都解决了

Paseo 完美解决了 TUI 的两大问题：

第一个是消息过滤。Paseo 可以把 Agent 的输出分成不同视图：只看消息、只看关键输出、只看工具调用、或者全部展开。TUI 把所有东西混在一条流里往下刷，要么全看要么全不看。能分层看这件事听起来简单，用过之后就回不去了。

第二个是多 Agent 并行和跨 Provider 编排。你可以同时开几个 Agent，一个用 Claude Code 的 Opus 做架构设计，另一个用 Codex 跑实现。关键是 Paseo 的子 Agent 能跨 Provider 调度：Claude Code 可以把任务派给 Codex，Codex 也可以把任务派给 Grok，这在各家原生的多 Agent 方案里是做不到的。

它还有几个内置 Skills 挺实用。`/paseo-handoff` 在不同 Agent 之间交接任务，比如先用 Claude 做规划然后 handoff 给 Codex 去实现。`/paseo-loop` 循环跑一个 Agent 直到满足验收条件，还可以配一个 verifier。`/paseo-committee` 拉两个不同的 Agent 组成委员会做根因分析。另外还有 heartbeat 功能，可以让 Agent 定时检查 CI 状态，失败了自动修，通过了自动停。

## 手机不是用来写代码的

Paseo 支持 iOS、Android、桌面端和网页端，覆盖面在同类工具里算最全的。

不过手机端的价值不是让你在手机上写代码，而是监控和介入。Agent 跑长任务的时候不用一直盯着电脑，出门掏出手机看一眼进度，Agent 遇到需要确认的问题直接在手机上回复就行。它还有语音模式，可以直接用语音给 Agent 布置任务或者讨论问题，走路的时候不用掏手机打字。

![Paseo 移动端：在手机上查看 Agent 运行状态、回复确认、管理会话](/images/2026-08-06-paseo-multi-agent-console-2026-08-06-paseo-mobile.png)

其实 Paseo 这个名字就说明了设计意图。Paseo 是西班牙语里“散步”的意思。作者 Mo Boudra 之前遛弯的时候总是得 SSH 到 tmux 里查看 Agent 状态，太折腾了，于是做了这个工具。一个人从头写到尾，GitHub 上 12,000 多个 Star 全是他一个独立开发者撑起来的。

安全方面，设备之间通过端到端加密的 relay 配对。Agent 始终在你自己的机器上跑，没有遥测，没有追踪，也不需要登录。

## 部署在服务器上，随时随地连

Paseo 最实用的部署方式是跑在开发机或远程服务器上，然后从任何设备连过来操作。

桌面端最简单，从 paseo.sh/download 下载，打开之后 daemon 自动启动。手机配对在设置里扫个码就行。

远程服务器用 Docker：

```bash
docker run -d --name paseo \
  -p 6767:6767 \
  -e PASEO_PASSWORD=your-password \
  -v "$PWD/paseo-home:/home/paseo" \
  -v "$PWD:/workspace" \
  ghcr.io/getpaseo/paseo:latest
```

启动后访问 `http://your-server:6767` 就是完整的 Web 界面。手机 App 连这个地址，就可以在任何地方操作服务器上的 Agent 了。服务器不在公网的话，可以用 Tailscale 或者 Paseo 自带的 relay 做穿透，relay 走端到端加密，不需要开端口。

前提是服务器上要装好对应的 Agent CLI。Paseo 是编排层，不包含 Agent 本身，Docker 镜像里自己加装就行。

## 写在最后

Paseo 还在 beta 阶段，有些粗糙的地方。移动端侧边栏滑动手势偶尔失灵，终端在手机上的输入体验还在打磨。WebSocket 连接在 Cloudflare relay 上大概 100 秒不活跃会断开，长时间挂着需要注意。

另外 Paseo 上手门槛不低，你得先有自己的 Agent CLI 环境，它也不帮你管理 Agent 环境。不过换个角度想，这恰恰是它克制的体现。不做自己不该做的事。

在一个所有人都想做 Agent Harness 的市场里，Paseo 选择不造引擎。它不跟 Claude Code 和 Codex 竞争，它让你同时用好它们。这种思路在我看来是对的。

当然，如果你不需要远程访问和多 Agent 跨 Provider 编排，只是单纯想在本机上有个比 TUI 更舒服的界面，Claude Desktop 和 Codex App 也都是不错的选择。它们各自对自家 Agent 的集成更深，开箱即用，不需要额外部署 daemon。Paseo 的优势在跨 Agent 和跨设备这两个场景上，如果你同时用多个 Agent 或者经常需要远程操作，它才是更合适的选择。

项目地址：<https://github.com/getpaseo/paseo>
