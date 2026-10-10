---
title: "Codex CLI 也能用 Skills 了：把 Claude Code 的“技能包”迁了过来"
date: 2025-12-08
draft: false
tags: [Agent, AI, Vibe Coding, 大模型, Codex]
description: "Codex CLI v0.65.0 开始支持 Skills，本文说明它为什么能缓解 MCP 带来的上下文膨胀，介绍 Codex 中 Skills 的用法、我迁移的技能包以及目前还存在的小问题。"
---

Codex CLI v0.65.0 带来了一个我期待已久的功能——Skills 支持。

这个功能最早是 Anthropic 在 Claude Code 上推出的，我已经用了一段时间，早就想着什么时候 Codex 也能有。上周末刷 Codex GitHub 看到合并的 PR，就花了点时间把之前写的 Claude Code Skills 迁移过来，顺手开源在了 GitHub <https://github.com/feiskyer/codex-settings> 上。

## 为什么需要 Skills

AI 编程助手很强，但真实工作需要的不只是通用能力，还需要你给它配置各种工具。MCP 就是配置外置工具的事实标准，用过 Claude Code、Codex 或者其他 AI Agent 的应该都配过不少 MCP Server。

MCP 普及之后，问题也渐渐暴露出来了。

最明显的是上下文占用。每个 MCP 工具的定义都要占用大量上下文空间，工具多了，光是工具描述就能吃掉好几千到几万 token。我之前配了 playwright、github 这些 MCP Server，启动时上下文窗口已经被 MCP 用掉了一半，留给实际对话的空间就太少了。

另一个问题是 Agent 性能下降。工具越多，模型做决策的时候越容易“选择困难”。该用 A 工具的时候用了 B，或者在几个相似工具之间反复尝试。这种情况在工具数量超过二三十个的时候特别明显。

Skills 解决的就是这两个问题。

它采用“渐进式披露”的设计——AI 启动时只读取 Skill 的名字和描述，一般几十个字就足够了。只有真正用到的时候，才会去读完整的说明文档。如果文档里还引用了其他文件，也是按需加载。就像一本手册，先看目录，再翻章节，最后查附录。

这意味着你可以装几十个 Skills，但不会把上下文窗口撑爆。而且因为每次只加载相关的 Skill，模型不用在一堆工具里做选择，决策路径更清晰，出错率也低了。

Skills 里还能放可执行代码。有些操作用代码跑比让 AI 生成 token 高效多了，排序、数据处理这些，代码执行既快又稳定。

## Codex 的 Skills 怎么用

12 月 1 日，Codex CLI 通过 [PR #7412](https://github.com/openai/codex/pull/7412) 正式支持了 Skills。官方文档标注这还是实验性功能，后续可能还会有重大修改，不过已经基本可用了。

文件结构很简单，在 `~/.codex/skills/` 目录下建文件夹，里面放一个 `SKILL.md` 文件就行。

```
~/.codex/skills/
├── claude-skill/
│   └── SKILL.md
├── nanobanana-skill/
│   ├── SKILL.md
│   └── nanobanana.py
│   └── requirements.txt
```

`SKILL.md` 文件格式是 YAML 开头加 Markdown 正文：

```yaml
---
name: pdf-processing
description: 处理和填写 PDF 表单。用于 PDF 相关任务。
---
# PDF 处理说明

用 pdfplumber 提取文本...
```

description 要写清楚“做什么”和“什么时候用”，Codex 靠这个判断要不要加载。写得太模糊的话，该触发的时候触发不了。

Codex CLI 中的 Skill 调用方式有两种：

1）类似于 Claude Code，在你的提示词里面直接说“使用某某 skill 干嘛”；

2）显式调用，使用 `$skill-name [prompt]`，比如 `$nanobanana-skill 帮我绘制微信公众号封面图`。

## 我迁移了哪些 Skills

我把之前在 Claude Code 上常用的 Skills 都迁移过来了，开源在 [feiskyer/codex-settings](https://github.com/feiskyer/codex-settings)。目前有六个。

**claude-skill** 在 Codex 里调用 Claude Code。有些任务 Claude 做得更好，比如代码审查、写文档、做设计等，我就会用这个 Skill 把任务甩给 Claude。

**nanobanana-skill** 用来生成图片，调用的是 Google Gemini API。写公众号文章需要配图的时候特别好用，一句话就能生成。支持各种尺寸和分辨率，从 1K 到 4K 都有。

**youtube-transcribe-skill** 提取 YouTube 字幕。看国外的技术分享视频想做点笔记时，手动找字幕下载太麻烦了。这个 Skill 会先尝试 yt-dlp，失败了自动切换到浏览器自动化方式。

**autonomous-skill** 用于长时间任务。有些任务一个会话完不成，需要断点续传。这个 Skill 会生成任务清单，一个个执行，中间断了也能接着来。不过目前还不能完全自动运行，执行时可能会因为权限请求暂停，需要人盯着点。

**kiro-skill** 是个完整的规范驱动开发工作流。从需求文档、架构设计到任务清单、逐步实现，一条龙服务。适合做新功能的时候用，能帮你把需求想清楚再动手。

**spec-kit-skill** 集成了 GitHub 官方的 Spec Kit 工具，规范驱动开发那一套。从项目原则、功能需求到技术方案、任务清单，七个阶段走下来，适合团队协作的场景。

后面这三个 Skill 还不是特别稳定，还在测试阶段。如果你也有类似的需求，欢迎提 Issue 或者直接发 PR 改进。

## 快速上手

安装很简单，三行命令。

```bash
# 备份原有配置
mv ~/.codex ~/.codex.bak

# 克隆配置仓库
git clone https://github.com/feiskyer/codex-settings.git ~/.codex

# 安装 Codex CLI
npm install -g @openai/codex
```

根据你的需要配置 Codex CLI，可以使用 ChatGPT 订阅、OpenAI API Key 或者其他第三方国内外兼容 OpenAI API 的各种大模型。

如果你没有这个仓库，而是手动配置的话，不要忘记在你的 `~/.codex/config.toml `文件中添加：

```yaml
[features]
skills = true
```

配置好后，启动 codex 后输入 `/skills` 能看到已加载的 Skills 列表。试试 `$nanobanana-skill 生成一张简约风格的山水画`，看看效果。

## 还有些小问题

Codex CLI 跟 Claude Code 的 Skills 设计理念基本一致，毕竟文件格式都一样。但细节上还有改进空间。

Claude Code 支持 `allowed-tools` 字段，可以限制 Skill 只能用哪些工具，比如做只读操作。Codex 暂时没这个功能。另外 Codex CLI 的权限系统一直都比较粗糙，时不时需要人来授权操作，想让 Skill 完全自主跑起来还有点难。

还有项目级别的 Skill 配置、Marketplace、Plugin 这些 Claude Code 已经有的功能，Codex 也都还没支持。

不过 Codex 是开源项目，社区很活跃，这些功能应该不会等太久。

说实话，AI 编程工具发展到现在，越来越像个可编程的平台了。Prompt、Skill、MCP Server、Hook，各种扩展机制层出不穷。工具本身的能力边界越来越模糊，关键看你怎么配置和定制。

这对我们技术人来说是好事。不用等官方加功能，自己动手就能扩展。

---

**相关资源**

· Codex Skills 配置仓库 https://github.com/feiskyer/codex-settings

· Codex Skills 官方文档 https://github.com/openai/codex/blob/main/docs/skills.md

· Claude Code Skills 文档 https://code.claude.com/docs/en/skills

· Claude Code 配置仓库 https://github.com/feiskyer/claude-code-settings
