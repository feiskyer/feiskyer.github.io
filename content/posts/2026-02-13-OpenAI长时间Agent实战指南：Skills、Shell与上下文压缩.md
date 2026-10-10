---
title: "OpenAI 长时间 Agent 实战指南：Skills、Shell 与上下文压缩"
date: 2026-02-13T10:00:00+08:00
draft: false
tags: [OpenAI, AI Agent, Skill, Shell, 上下文压缩]
description: "编译自 OpenAI 开发者博客的长时间 Agent 实战指南，讲解 Skills、Shell Tool 与 Compaction 三大能力如何协同，解决上下文压缩、执行环境与可复用指令包问题，并给出五条实践建议和三种递进构建模式。"
---

> 题记：本文编译自 OpenAI 开发者博客《[Shell + Skills + Compaction: Tips for Long-Running Agents](https://developers.openai.com/blog/skills-shell-tips)》，由 Charlie Guo 撰写，发表于 2026 年 2 月 11 日。本文在翻译基础上做了整理和补充。

用 Agent 做过稍微复杂一点任务的朋友，应该都碰到过这几个问题：跑着跑着上下文爆了，中间结果没地方存，任务流程每次都要从头描述一遍。

这些问题说白了就是一个核心矛盾：Agent 要做的事越来越重，但它的“工作记忆”和“工具箱”还停留在对话级别。

OpenAI 最近发了一篇实践指南，专门聊怎么用三个互相配合的能力来解决这些问题：Skills、Shell Tool 和 Compaction。

我自己在 Claude Code 和 Codex 上都用过类似的机制，读完这篇觉得有几个点挺实用，整理分享一下。

## 三个核心概念

先把这三个东西分别说清楚。

### Skills：可复用的指令包

Skills 本质上是一组带版本控制的指令文件，核心是一个 `SKILL.md` 清单文件，里面写着这个技能是干什么的、什么时候该用、怎么用。你可以把它理解成给 Agent 准备的操作手册，平时不用的时候不占上下文，需要的时候按需加载。

这个概念其实来自 Anthropic。Anthropic 在 Claude Code 上早就实现了类似的机制，Codex CLI 后来也跟进了。OpenAI 这次把它的 API 也标准化了，对齐了 Agent Skills 开放标准。平台会把每个 Skill 的名字、描述和路径暴露给模型，让模型自己决定什么时候调用。

我自己用 Claude Code 的 Skills 已经有一段时间了，体验下来最大的好处就是：把那些重复性的工作流固化下来，不用每次都在 Prompt 里写一遍。

### Shell：真正的执行环境

Shell Tool 给 Agent 提供了一个真实的终端环境，可以是 OpenAI 托管的容器，也可以是本地运行时。在这个环境里，Agent 可以安装依赖、跑脚本、生成文件，而且有受控的网络访问权限。

这跟简单的代码执行还是有本质区别的。举个例子，你让 Agent 分析一个 CSV 数据集，它可以在 Shell 里先 `pip install pandas matplotlib`，然后写一段 Python 脚本做数据清洗和可视化，最后把生成的图表存到 `/mnt/data/` 目录。整个过程不需要你提前配环境，Agent 自己就能搞定。

两种模式（托管容器和本地运行）通过 Responses API 保持了统一的工具语义。开发阶段在本地快速迭代，上线后切到托管容器做隔离，API 调用方式是一样的：

```python
response = client.responses.create(
    model="gpt-5.2",
    tools=[{
        "type": "shell",
        "environment": {"type": "container_auto"}  # 本地模式改成 "local"
    }],
    input="Install pandas, fetch the CSV from S3, and generate a summary report"
)
```

这样做的好处是，本地开发和生产环境的切换只需要把 `environment` 类型从 `container_auto` 改成 `local`。

### Compaction：上下文不够用怎么办

长时间运行的 Agent 最头疼的问题就是上下文窗口不够用。跑了几十轮工具调用之后，前面的对话内容就被挤出去了，Agent 就可能开始断片。

Compaction 就是解决这个问题的。它有两种方式：一种是自动压缩，在 `context_management` 里设个阈值，上下文超了就自动触发；另一种是通过 `/responses/compact` 接口手动压缩：

```python
# 方式一：自动压缩，上下文超过阈值时服务端自动触发
response = client.responses.create(
    model="gpt-5.2",
    input=conversation,
    context_management=[{"type": "compaction", "compact_threshold": 200000}],
)

# 方式二：手动压缩，显式调用 compact 接口
compacted = client.responses.compact(
    model="gpt-5.2",
    input=long_conversation_items,
)
```

核心思路都是把之前的对话历史压缩成摘要，保留关键信息，释放上下文空间。

这个功能的关键在于心态转变，也就是不要把 Compaction 当成上下文快爆了才用的应急措施，而是从一开始就把它作为默认实践。设计任务流程的时候就考虑好：容器要复用，`previous_response_id` 要传递，压缩要常态化。

## 五条实践建议

概念说完了，来看具体怎么用好这些能力。OpenAI 在文章里给了几条实操建议，结合我自己的使用经验一起聊聊。

### Skill 的描述就是路由逻辑

很多人写 Skill 描述的时候，只写了这个 Skill 是干什么的，这远远不够。描述要能回答三个问题：什么时候该用它、什么时候不该用它、用完之后期望的输出是什么。

具体来说，要写明 Use when 和 Don't use when 两类场景。举个例子，一个数据分析 Skill 的描述可能是这样的：

```markdown
# Data Analysis Skill

Use when:
- User provides a dataset and asks for trends, patterns, or insights
- User needs charts or visualizations from raw data

Don't use when:
- User asks a simple statistical question (e.g., "what's the average of X")
- User just needs data formatting or conversion
```

不只写用于分析数据集，还要明确告诉模型什么时候不需要大费周章地调用这个 Skill。

### 反面案例比正面案例更重要

OpenAI 的测试数据显示，光有 Skill 不写反面案例，正确调用率反而会下降大约 20% 。加上什么时候不该用的说明后，路由准确性才恢复并提升。

这个发现挺有意思的。模型看到一个新工具，本能反应是有锤子就找钉子。如果你不明确告诉它边界在哪，它会倾向于过度使用。

### 模板放在 Skill 里，别放 System Prompt

这条建议很实用。很多人习惯把示例和模板直接塞进 System Prompt 里，结果不管当前任务用不用得上，每次对话都要消耗这些 token。

把模板放在 Skill 内部，效果是不用时基本免费。只有模型决定调用这个 Skill 的时候，模板内容才会被加载进上下文。这对 token 消耗的优化是巨大的，也是 Skill 最大的优点。

### 需要确定性的时候，别让模型自己选

自动路由在大多数场景下够用了。但在生产环境中对确定性要求高的流程里，最好直接告诉模型用某某 Skill，别让它自己判断。

这就把模糊的路由变成了明确的指令。特别是在多步骤工作流中，每一步用哪个 Skill、按什么顺序执行，都应该在编排层面写清楚，不留给模型自由发挥的空间。

### 网络安全不能马虎

Skill 加上网络访问权限，等于给 Agent 开了一条可以往外发数据的通道。网络安全这事不能大意。

安全策略说白了就是两层白名单：组织级白名单划定最大范围，请求级白名单只能在这个范围内再缩小。两层都要尽量收紧。

另外一个关键点是，模型绝对不能看到明文凭证。OpenAI 搞了个 `domain_secrets` 机制，在 Skill 里写占位符（比如 `Authorization: Bearer {{API_KEY}}`），实际的密钥只在请求发往白名单里的目标地址时才替换进去。思路跟环境变量注入差不多，但多了目标地址校验。

## 三种构建模式

OpenAI 还总结了三种递进的构建模式，从简单到复杂，适合不同阶段的需求。

### 基础模式：安装 → 获取 → 写入

最简单的用法：让 Agent 在 Shell 里安装依赖、拉取外部数据、把结果写到 `/mnt/data/` 目录。

`/mnt/data/` 相当于一个约定好的交付目录，Agent 生成的需要人来审查或者给下游用的文件都放这里。这样做的好处是划清了 Agent 的工作区和最终交付物的界限，后续取用和审查都方便。

### 工作流模式：Skills + Shell 联动

把重复性工作流封装成 Skill，挂到 Shell 环境里，让 Agent 按固定流程跑。

这种模式特别适合数据处理类任务。拿数据集清洗来说，你可以在 Skill 里定义好标准流程：先检查缺失值比例，超过阈值的列直接丢掉；然后做类型推断和格式标准化；最后输出清洗报告到 `/mnt/data/`。Agent 每次拿到新数据集，都按这个流程走，不用你重复描述一遍。

### 企业级模式：Skills 作为活的 SOP

到了企业场景，Skills 就不只是技术工具了，而是变成了活的 SOP。公司的业务流程改了，对应的 Skill 跟着更新，Agent 的行为自动对齐，不用重新调参。

OpenAI 提到了 Glean 的早期落地案例：用了这种模式之后，准确率从 73% 提升到 85% ，首次响应延迟降低了 18.1% 。挺有意思的一点是，给 Agent 结构化的指导，不仅提高了质量，还加快了速度。模型不用花那么多 token 去想该怎么做，直接按 Skill 里的步骤走就行了。

## 写在最后

回过头来看，OpenAI 这篇文章的核心观点其实就一个：长时间运行的 Agent 需要从单次对话的思维模式升级到持续工作流的思维模式。

Skills 解决怎么做的问题，把经验固化成可复用的指令。Shell 解决在哪做的问题，提供真实的执行环境。Compaction 解决记不住的问题，让 Agent 在长任务中保持连贯。

这三个能力并不是 OpenAI 独有的。Claude Code 的 Skills 和 SubAgent、Codex 的 Shell 执行和 Exec Plan，本质上都在解决同样的问题。各家的具体实现不同，但方向是一致的：让 Agent 从聊天助手进化成能持续干活的工作伙伴。

如果你正在做 Agent 相关的开发，有几个建议：先把最常用的工作流封装成 Skill，别急着做通用的。Shell 环境从本地开始，跑通了再考虑容器化。Compaction 从第一天就用上，别等上下文爆了再补救。

---

原文链接：<https://developers.openai.com/blog/skills-shell-tips>
