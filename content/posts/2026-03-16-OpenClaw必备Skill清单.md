---
title: "OpenClaw 必备 Skill 清单：装完这些再开始干活"
date: 2026-03-16T10:00:00+08:00
draft: false
tags: [OpenClaw, Skills, AI 工具]
description: "OpenClaw 必备 Skill 清单，涵盖 self-improving-agent、find-skills、skill-vetter 三个基础项，Tavily Search 等联网三件套，社交媒体 CLI 工具，以及用 Mcporter 桥接 MCP，每个都附安装命令。"
---

上次分享了《[十个顶级 Claude Code Skills，装上就不想卸](https://mp.weixin.qq.com/s/b-0ppca5YhiGgxR_mWJNVA)》，不少读者问我 OpenClaw 这边有没有类似的推荐。今天就来一篇。

跟 Claude Code 比，全新安装的 OpenClaw 其实挺无聊的。它能聊天、能写代码、能操作文件系统，但碰到需要上网搜东西、刷个社交媒体、或者画张图的场景，就卡住了，看起来跟 ChatGPT 之类的聊天工具并没有多大区别。但这其实是还没用好 OpenClaw 最基本的扩展机制，也就是 Skill。ClawHub 上的 Skill 数量已经破了 25000，光是排名第一的 self-improving-agent 就有 20 多万的安装量。不过 Skill 装多了也有问题，互相打架不说，上下文也吃不消。所以关键还是选对几个真正有用的。

这篇就整理一份我自己在用的 OpenClaw Skill 清单，每个都有附安装命令，方便你一键安装。

## 先装这三个

这三个 Skill 我觉得属于必备级别，建议第一时间搞定。

### Self-Improving Agent

ClawHub 排名第一不是没道理的。

这个 Skill 让 OpenClaw 具备了自我学习的能力。每次你纠正它的错误、每次命令执行失败、每次它发现了更好的做法，都会被记录下来，变成它下次做事的经验。用得越久，它就越懂你的习惯和偏好。

我用了一段时间之后，最明显的变化是它不再重复犯同一个错了。比如我习惯用 pnpm 而不是 npm，纠正过一次之后就再也没出过。听起来是个小事，但每天省几次纠正的功夫，累积下来效率提升挺明显的。

```bash
npx clawdhub install self-improving-agent
```

### Find Skills

OpenClaw 不像 Claude Code 那样内置了大量工具，很多能力需要通过 Skill 来补齐。问题是 ClawHub 上 25000 多个 Skill，你怎么知道哪个能解决你当前的问题？

Find Skills 做的就是这件事。当你问 OpenClaw“怎么做 X”的时候，它会先去 ClawHub 搜一圈，看看有没有现成的 Skill 能用，找到了就直接推荐给你，省得自己一个个去翻。

有点像给 OpenClaw 装了个应用商店的搜索入口。

```bash
npx clawdhub install find-skills
```

### Skill Vetter

前面说了 ClawHub 上有 25000 多个 Skill，质量参差不齐。有的 Skill 写得不错，有的可能藏着恶意代码，毕竟 Skill 本质上就是一段会被 Agent 执行的指令。

Skill Vetter 的作用是在安装前自动扫描 Skill 的内容，检查有没有潜在的安全隐患。比如 Skill 里是否有可疑的网络请求、是否试图读取敏感文件、是否包含 prompt injection 的模式。

如果你对安全要求更高，可以搭配慢雾（SlowMist）出的 OpenClaw 安全实践指南一起用。那份指南走的是零信任路线，默认假设 prompt injection、供应链投毒都可能发生，从日常操作到每晚巡检都有覆盖。对于在高权限环境下跑 OpenClaw 的用户来说，值得过一遍。

```bash
npx clawhub install skill-vetter
```

> 附安全实践指南链接：<https://github.com/slowmist/openclaw-security-practice-guide>

## 让 OpenClaw 能上网

裸机的 OpenClaw 没有联网能力，不能搜索、不能访问网页。这三个 Skill 分别解决搜索、浏览器操作和长文提炼三个场景。

### Tavily Search

给 OpenClaw 加上网络搜索能力。Tavily 有月免费额度，对个人用户来说日常搜索基本够用，不需要一上来就掏钱。

搜索质量比让 OpenClaw 去 curl 一个搜索引擎然后解析 HTML 好太多了。返回的结果是结构化的，直接就能用。

```bash
npx clawhub install tavily-search
```

### Agent Browser

有些事光靠搜索引擎搞不定。比如你要操作一个需要登录的后台、要在某个网站上填表单、或者要从一个动态加载的页面抓数据，这些都需要真正的浏览器。

Agent Browser 让 OpenClaw 能控制浏览器，点击、输入、截屏、导航，该有的都有。

这里有个关键技巧：用 `--auto-connect` 参数连接到你已经登录过的 Chrome 浏览器。这样 OpenClaw 就能直接用你的登录态，不用每次都重新登录各种服务。省事太多了。

```bash
npx clawhub install agent-browser
```

### Summarize

经常需要让 OpenClaw 帮你读一篇长文章或者处理一段音视频，Summarize 就是干这个的。给它一个网址、一个文件路径、或者一段媒体，它帮你快速生成摘要。

用之前需要先装个全局依赖：

```bash
npm i -g @steipete/summarize
npx clawhub install summarize
```

搜索、浏览器、摘要，三个加一起，OpenClaw 在信息获取层面就基本没有短板了。不过这还只是读的能力。如果你还想让它去社交媒体上逛，那就需要下面这组 Skill。

## 社交媒体三件套

这三个 Skill 来自同一个开发者 jackwener，做的事情就是让 OpenClaw 等各种 Agent 能搜索、访问和交互主流社交平台的内容。

小红书：

```bash
npx skills add jackwener/xiaohongshu-cli
```

Twitter/X：

```bash
npx skills add jackwener/twitter-cli
```

Reddit：

```bash
npx skills add jackwener/rdt-cli
```

我自己用得最多的是 xiaohongshu-cli 和 twitter-cli。比如想要了解某个工具的用户评价，让 OpenClaw 去小红书和 Twitter 上搜一圈，回来给我整理个摘要，比自己去翻快多了。

jackwener 还开源了 Bilibili、Telegram、Discord、微博、BOSS 直聘等平台的 CLI 工具和对应 Skill，需要的可以去他的 GitHub 上看看。

## 锦上添花

下面这几个不是每个人都需要，但如果你的使用场景刚好对上了，装了之后体验会好一截。

### Proactive Agent

普通 OpenClaw 是你给任务它才干活。Proactive Agent 让它变得主动一些，能自我迭代、主动发现问题、主动优化方案。

```bash
npx clawhub install proactive-agent
```

### GitHub

有开源项目要维护，或者想给别人的项目提 PR，这个 Skill 让 OpenClaw 能直接操作 GitHub 的 Issues、PR、Code Review 等工作流。

```bash
npx clawhub install GitHub
```

### Nano Banana Pro

用 Gemini 3 Pro 的图像生成能力，让 OpenClaw 能画图。支持文生图和图生图，1K/2K/4K 分辨率都行，编辑已有图片也可以。做封面图、画流程图、生成配图的时候挺方便的。

```bash
npx clawhub install nano-banana-pro
```

### Mcporter

OpenClaw 本身不支持 MCP 工具。如果你之前在 Claude Code 上用惯了各种 MCP Server，换到 OpenClaw 会觉得少了点什么。

Mcporter 做的是格式转换：把 MCP 工具转成 CLI 格式，再作为 Skill 给 OpenClaw 使用。算是一个桥接方案，让你之前的 MCP 生态投资不至于浪费。

```bash
npx clawhub install mcporter
```

---

以上就是我目前在用的 OpenClaw Skill 组合：先把自学习和安全两个基础打好，再把联网和社交媒体的信息通道打通，最后根据自己的工作场景挑几个辅助工具。而至于编程呢，还是把专业的事情交给专业的工具，继续交给 Claude Code 来负责。你可以用 OpenClaw 的 ACP Agent 来调度 Claude Code，顺手也解决了手机访问的问题（接入 Slack/Discord/飞书等可以随时手机下发任务）。

如果这些还不够用，下面这几个地方可以继续探索：

---

相关资源：

- ClawHub 官网：<https://clawhub.ai/>
- Awesome OpenClaw Skills：<https://github.com/VoltAgent/awesome-openclaw-skills>
- OpenClaw Skills 仓库：<https://github.com/openclaw/skills>
- SkillsMap：<https://skillsmp.com/>
- Skills.SH：<https://skills.sh/>
- Awesome OpenClaw Usecases：<https://github.com/hesamsheikh/awesome-openclaw-usecases>
