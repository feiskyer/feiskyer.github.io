---
title: "OpenAI 和 Anthropic 居然合作了？聊聊 Agentic AI 基金会背后的野心"
date: 2025-12-11
draft: false
tags: [Agent, AI, Vibe Coding, 大模型, MCP]
description: "OpenAI、Anthropic 联合 Block 成立 Agentic AI 基金会并把核心开源项目捐给 Linux Foundation，本文类比当年 CNCF 统一容器编排的历史，解读这场合作背后争夺 AI Agent 标准话语权的野心。"
---

![](/images/0cf18915-355f-4005-89eb-b25fd9d19aae.png)

这两天，OpenAI 和 Anthropic 居然坐到了一起，联合 Block 成立了 Agentic AI 基金会（AAIF），把各自的核心开源项目捐给了 Linux Foundation。

看到这个消息，我第一反应是——这背后的野心不小。想想当年的 CNCF 就明白了。

## Agentic AI 基金会想干什么

熟悉云原生的朋友应该记得，Kubernetes 刚出来那会儿，容器编排领域也是一片混战。Docker Swarm、Mesos、Kubernetes 三足鼎立，谁也不服谁，而 Kubernetes 还是其中上手最难的。后来 Google 把 Kubernetes 捐给了 Linux Foundation 下面的 CNCF，才逐渐统一了市场。

AAIF 的野心很可能就是成为 AI Agent 领域的 CNCF。

看看白金会员名单就知道了——除了三个联合创始人，AWS、Google、Microsoft、Bloomberg、Cloudflare 全都在列。黄金会员里还有 IBM、Oracle、Salesforce、Docker、JetBrains 这些大厂。大家都想参与，但又都不想让某一家独大。

这个逻辑其实不难理解。AI Agent 正在从实验走向生产，谁来定标准，谁就有话语权。与其让市场碎片化、各搞各的，不如联手把标准定下来。开源是手段，标准才是目的。

## 三个创始项目

AAIF 成立时，三家公司各自捐了一个项目。

### MCP：连接 AI 和工具的“USB 接口”

MCP 是 Anthropic 一年前开源的项目，全称 Model Context Protocol。简单说，它定义了一套标准协议，让 AI 模型能连接外部工具和数据源。你可以把它理解成 AI 世界的 USB 接口——有了统一标准，各种设备才能即插即用。

一年时间，MCP 的增长速度确实吓人。现在已经有超过 10000 个公开的 MCP 服务器，ChatGPT、Cursor、Microsoft Copilot、Gemini、VS Code 这些主流产品全都支持了。Python 和 TypeScript SDK 每月下载量超过 9700 万次。

![](/images/d7e29732-a06a-4c20-986d-7ed0c0ee06d2.png)

我自己在使用各种 AI 编程和 Agent 产品时也都连接了很多 MCP 服务器，体验确实比以前写一堆适配代码方便地多了。以前要让 Claude 连数据库，得自己写工具函数、处理各种边界情况。现在找个现成的 MCP 服务器，配置一下就能用。

不过 MCP 虽然已经是一个公认的行业标准，它的上下文占用、工具混乱以及大量工具导致的 Agent 性能下降等各种问题最近也都爆了出来。Anthropic 主推的 Skills 有取而代之的趋势。Anthropic 只把快要过气的 MCP 捐给了 Linux Foundation，至于是慷慨捐赠还是顺势甩包袱，就见仁见智了。

### goose：本地优先的 Agent 框架

goose 是 Block 在 2025 年初发布的开源 AI Agent 框架。特点是“本地优先”，可以在你自己的机器上运行，基于 MCP 做标准化集成。

一家金融科技公司为什么要做 AI Agent 框架？Block 开源负责人的说法是他们选择站在开放这边。但更实际的原因可能是，Block 内部已经有大量工程师在用 goose 做开发、数据分析和文档工作。开源出来能让社区帮着一起改进，最终受益的还是自己。

### AGENTS.md：AI 编程标准文件

AGENTS.md 是 OpenAI 在 2025 年 8 月发布的，目的是统一 AI 编程的指导标准。说它是“标准”可能都抬举了，本质上就是一个 Markdown 文件。

它解决的问题很简单：AI 编程助手在不同项目里工作时，怎么知道这个项目的规范？代码风格、构建步骤、测试要求这些，以前每次都要手动告诉它，现在只要在项目根目录放一个 AGENTS.md 文件，AI 自己会去读。

这个方案被采用得很快，超过 60000 个开源项目已经在用。Cursor、Devin、GitHub Copilot、Gemini CLI、VS Code 这些主流工具都支持了。

## 背后的商业逻辑

说白了，这事儿的核心就是——标准化能让市场做大，大家都能多赚钱。

对云厂商来说，Agent 跑在哪里？跑在云上。工具调用消耗什么？消耗算力和存储。如果 Agent 市场碎片化，开发者都在观望，市场起不来，云服务也卖不出去。统一标准后，开发者敢大规模投入，AWS、Google、Microsoft 才能规模化卖服务。

对 AI 公司来说，各有各的小算盘。Anthropic 把 MCP 捐出去，表面上是慷慨，实际上可能是趁 Skills 还没完全取代它之前，把包袱甩给基金会，换来“开放标准制定者”的影响力。OpenAI 的 AGENTS.md 更妙，一个 Markdown 文件几乎零维护成本，却能影响所有 Agent 的开发方式。Block 的 goose 则是内部工具外部化，开源后社区帮着改进，最终受益的还是自己。

如果不统一标准，每家都搞自己的协议，碎片化成本最终所有人都要承担。大家联手做标准，市场做大了，都能分一杯羹。

## 对我们意味着什么

Agentic AI 基金会的野心，是成为 AI Agent 时代的基础设施标准制定者。这个野心足够大，大到让竞争对手愿意暂时放下争斗，一起把蛋糕做大。一个开放、中立、持续演进的标准，对所有参与者都更有利。

短期来看，对开发者好处很明显。统一接口，统一框架，少写适配代码，Agent 开发的工作量可以减轻很多。并且有了 AGENTS.md 让不同的 AI 编程助手在同一个项目里有一致的行为规范，Agent 行为更可预测。goose 这样的框架提供了现成的 Agent 运行环境，部署起来也更简单。

长期来看，AAIF 能不能复现 CNCF 的辉煌还是个问号。最终能不能成功，还要看接下来几年的发展。但至少从现在来看，这是一个好的开始。

如果你也在做 AI Agent 相关的开发，建议现在就开始关注这几个项目。
