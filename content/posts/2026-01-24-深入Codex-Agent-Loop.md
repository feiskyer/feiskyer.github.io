---
title: "深入 Codex Agent Loop：OpenAI 详解智能体核心循环"
date: 2026-01-24T10:00:00+08:00
draft: false
tags: [AI, Agent, OpenAI, Codex, LLM]
description: "本文编译自 OpenAI 工程博客，深入讲解 Codex CLI 的 Agent Loop 实现细节，包括 Prompt 构建、模型推理、工具调用、上下文管理和性能优化。"
---

> 题记：本文编译自 OpenAI 工程博客《[Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)》，作者是 OpenAI 技术人员 Michael Bolin。本文在翻译基础上做了整理和补充，希望能帮大家理解 Codex CLI 背后的 Agent 架构。

用过 Codex CLI 或者 Claude Code 这类 AI 编程助手的朋友，应该都对 Agent Loop 这个词不陌生。说白了，就是 AI Agent 在接收到你的指令后，反复“思考-调用工具-观察结果-再思考”的循环过程。

这个循环具体是怎么实现的？Prompt 怎么组织的？工具调用怎么处理？上下文窗口快满了怎么办？这些细节，OpenAI 之前一直没公开讲过。

昨天 OpenAI 终于把 Codex CLI 的核心实现逻辑拆开讲了一遍。我自己做 Agent 项目 [Koder](https://github.com/feiskyer/koder) 时，实际上也是应用了类似的逻辑，读完觉得有不少启发，翻译分享给大家。

Codex CLI 本身就是个开源项目，代码在 <https://github.com/openai/codex> 。文章里提到的很多设计决策，都能在 GitHub 的 Issues 和 PRs 里找到更详细的讨论。

顺便提一下，Sam Altman 同一时间在社交媒体上透露，接下来一个月还会有更多 Codex 相关的发布，并且 OpenAI 正在为 AI 编程工具的安全性做准备，计划通过防御加速策略帮助开发者更快修补漏洞。看来 Codex 这条产品线，OpenAI 是认真要发力了。

![Sam Altman 发文预告 Codex 后续发布与安全准备](/images/2026-01-24-Codex-Agent-Loop-image-20260124214213355.png)

## 什么是 Agent Loop

每个 AI Agent 的核心都有一个 Agent Loop。简化版示意图如下所示：

![Agent Loop 示意图](/images/2026-01-24-Codex-Agent-Loop-image-20260124222242257.png)



整个流程可以这么理解：

1. Agent 接收用户输入，把它包装成发给模型的文本指令，也就是 Prompt。Prompt 发给模型做推理，文本会先被转成 token，模型生成新的 token 作为输出，再转回文本变成响应。因为 token 是逐个生成的，很多 LLM 应用会显示流式输出。

2. 接下来，模型要么直接给用户一个最终回复，要么请求执行一个工具调用，比如“运行 `ls` 命令并返回结果”。如果是工具调用，Agent 执行完后把结果追加到原来的 Prompt 里，再次查询模型。这个过程一直重复，直到模型不再发起工具调用，而是生成一条给用户的最终消息，在 OpenAI 的模型 API 里这叫 assistant message。

因为 Agent 可以执行修改本地环境的工具调用，它的输出不仅仅是文字消息。很多场景下，AI Agent 的主要产出是它在你电脑上写的代码。不管怎样，每一轮都会以一条 assistant message 结束，比如“我已经添加了你要求的 `architecture.md` 文件”，这表示当前轮次完成，控制权交还给用户。

从用户输入到 Agent 响应的这一趟，叫做对话的一个轮次，在 Codex 里也叫一个 thread。一个轮次内部可能包含多次“模型推理 ↔ 工具调用”的迭代。每次你发送新消息继续对话时，之前的对话历史都会作为新 Prompt 的一部分发给模型：

![多轮对话示意图](/images/2026-01-24-Codex-Agent-Loop-image-20260124222307635.png)

这意味着对话越长，发给模型的 Prompt 也越长。每个模型都有一个上下文窗口，就是一次推理能用的最大 token 数，同时包含输入和输出。你可以想象，Agent 在一个轮次里发起几百次工具调用，很可能就把上下文窗口撑爆了。上下文窗口管理是 Agent 的重要职责之一。

接下来看看 Codex 是怎么运行 Agent Loop 的。

## 模型推理

Codex CLI 通过 HTTP 请求调用 [Responses API](https://platform.openai.com/docs/api-reference/responses) 来执行模型推理。这个 API 端点可以[自定义配置](https://developers.openai.com/codex/config-advanced#custom-model-providers)，只要实现了 [Responses API 规范](https://www.openresponses.org/)就能接入：

- 用 ChatGPT 登录时，端点是 `https://chatgpt.com/backend-api/codex/responses`
- 用 API Key 认证时，端点是 `https://api.openai.com/v1/responses`
- 用 `--oss` 参数配合 [gpt-oss](https://openai.com/index/introducing-gpt-oss/) 本地模型时，默认是 `http://localhost:11434/v1/responses`
- 也可以用 Azure 等云厂商托管的 Responses API

### 构建初始 Prompt

作为用户，你不需要直接指定完整 Prompt。你只需要在请求里指定各种输入类型，Responses API 服务端会决定如何组织成模型能理解的格式。

初始 Prompt 里，每一项都关联一个 `role`，表示内容的权重优先级。角色按优先级从高到低是：`system`、`developer`、`user`、`assistant`。

[Responses API](https://platform.openai.com/docs/api-reference/responses/create) 接收 JSON 请求体，参数很多，重点需要关注这三个：

- [`instructions`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-instructions)：插入到模型上下文中的系统消息
- [`tools`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-tools)：模型可以调用的工具列表
- [`input`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-input)：发给模型的文本、图像或文件输入列表

在 Codex 里，`instructions` 字段会从 `~/.codex/config.toml` 的 [`model_instructions_file`](https://github.com/openai/codex/blob/338f2d634b2360ef3c899cac7e61a22c6b49c94f/codex-rs/core/src/config/mod.rs#L1474-L1483) 读取，没配置就用模型默认的 [base_instructions](https://github.com/openai/codex/blob/338f2d634b2360ef3c899cac7e61a22c6b49c94f/codex-rs/core/src/codex.rs#L279-L288)。模型特定的指令打包在 CLI 里，比如 [`gpt-5.2-codex_prompt.md`](https://github.com/openai/codex/blob/e958d0337e98f6398771917867d7de689dab3b7a/codex-rs/core/gpt-5.2-codex_prompt.md)。

`tools` 字段是工具定义列表，对于 Codex 来说包括 CLI 自带的工具、Responses API 提供的工具、用户配置的工具（通常来自 MCP Server）：

```json
[
  // Codex 默认的 shell 工具，用于在本地启动新进程
  {
    "type": "function",
    "name": "shell",
    "description": "Runs a shell command and returns its output...",
    "strict": false,
    "parameters": {
      "type": "object",
      "properties": {
        "command": {"type": "array", "description": "The command to execute", ...},
        "workdir": {"description": "The working directory...", ...},
        "timeout_ms": {"description": "The timeout for the command...", ...}
      },
      "required": ["command"]
    }
  },

  // Codex 内置的计划工具
  {
    "type": "function",
    "name": "update_plan",
    "description": "Updates the task plan...",
    "parameters": {
      "type": "object",
      "properties": {"plan":..., "explanation":...},
      "required": ["plan"]
    }
  },

  // Responses API 提供的网页搜索工具
  {"type": "web_search", "external_web_access": false},

  // 用户配置的 MCP Server
  {
    "type": "function",
    "name": "mcp__weather__get-forecast",
    "description": "Get weather alerts for a US state",
    "parameters": {
      "type": "object",
      "properties": {"latitude": {...}, "longitude": {...}},
      "required": ["latitude", "longitude"]
    }
  }
]
```

JSON 请求体的 `input` 字段是一个列表。Codex 在添加用户消息之前，会[先插入以下内容](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L1387-L1415)：

1. 一条 `role=developer` 的消息，描述仅适用于 Codex 自带 `shell` 工具的沙箱环境。其他工具（比如来自 MCP Server 的）不受 Codex 沙箱限制，需要自己负责安全防护。这条消息基于模板生成，关键内容来自打包进 CLI 的 Markdown 文件：

    ```xml
    <permissions instructions>
      - 描述沙箱的文件权限和网络访问规则
      - 何时需要请求用户授权执行 shell 命令
      - Codex 可写入的文件夹列表
    </permissions instructions>
    ```

2. 一条可选的 `role=developer` 消息，内容是用户 `config.toml` 里的 `developer_instructions` 值。

3. 一条可选的 `role=user` 消息，包含用户指令。这些指令[从多个来源汇总](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/project_doc.rs#L37-L42)，越具体的越靠后：

   - `$CODEX_HOME` 目录下的 `AGENTS.override.md` 和 `AGENTS.md`

   - 在大小限制内（默认 32 KB），从 Git 根目录到当前工作目录的每个文件夹，查找 `AGENTS.override.md`、`AGENTS.md` 等文件

   - 如果配置了 [Skills](https://developers.openai.com/codex/skills/)：Skills 介绍、元数据、使用说明

4. 一条 `role=user` 消息，描述 Agent 当前运行的本地环境，[包括当前工作目录和用户的 shell](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/environment_context.rs#L51-L71)：

    ```xml
    <environment_context>
      <cwd>/Users/mbolin/code/codex5</cwd>
      <shell>zsh</shell>
    </environment_context>
    ```

完成上述初始化后，Codex 才把用户消息追加到 `input` 里。

`input` 的每个元素都是 JSON 对象，包含 `type`、`role` 和 `content` 字段：

```json
{
  "type": "message",
  "role": "user",
  "content": [
    {"type": "input_text", "text": "Add an architecture diagram to the README.md"}
  ]
}
```

Codex 构建好完整 JSON 请求体后，带着 `Authorization` 头发送 HTTP POST 请求。

OpenAI 的 Responses API 服务器收到请求后，按下图方式把 JSON 转成模型的 Prompt：

![Prompt 结构示意图](/images/2026-01-24-Codex-Agent-Loop-image-20260124222344900.png)



如图所示，Prompt 的前三项顺序是服务器决定的，不是客户端。这三项里，只有系统消息的内容是服务器控制的，`tools` 和 `instructions` 都是客户端指定的。后面跟着的就是 JSON 请求体里的 `input`。

到这里，完整的 Prompt 就准备好了，可以开始发给模型执行了。

### 对话流程

发给 Responses API 的 HTTP 请求启动了 Codex 对话的第一个轮次。服务器用 Server-Sent Events（[SSE](https://en.wikipedia.org/wiki/Server-sent_events)）流式响应，每个事件的 `data` 是 JSON 对象，`type` 字段以 `response` 开头：

```json
data: {"type":"response.reasoning_summary_text.delta","delta":"ah ", ...}
data: {"type":"response.reasoning_summary_text.delta","delta":"ha!", ...}
data: {"type":"response.reasoning_summary_text.done", "item_id":...}
data: {"type":"response.output_item.added", "item":{...}}
data: {"type":"response.output_text.delta", "delta":"forty-", ...}
data: {"type":"response.output_text.delta", "delta":"two!", ...}
data: {"type":"response.completed","response":{...}}
```

Codex [消费这个事件流](https://github.com/openai/codex/blob/2a68b74b9bf16b64e285495c1b149d7d6ac8bdf4/codex-rs/codex-api/src/sse/responses.rs#L334-L342)，重新发布为内部事件对象。`response.output_text.delta` 这样的事件支持 UI 流式输出，`response.output_item.added` 这样的事件会被转成对象，追加到后续 Responses API 调用的 `input` 里。

假设第一次请求返回了两个 `response.output_item.done` 事件：一个 `type=reasoning`，一个 `type=function_call`。带着工具调用结果再次查询模型时，这些事件必须体现在 JSON 的 `input` 字段里：

```json
[
  /* ... 原来 input 数组的 5 个项目 ... */
  {
    "type": "reasoning",
    "summary": [
      "type": "summary_text",
      "text": "**Adding an architecture diagram for README.md**\n\nI need to..."
    ],
    "encrypted_content": "gAAAAABpaDWNMxMeLw..."
  },
  {
    "type": "function_call",
    "name": "shell",
    "arguments": "{\"command\":\"cat README.md\",\"workdir\":\"/Users/mbolin/code/codex5\"}",
    "call_id": "call_8675309..."
  },
  {
    "type": "function_call_output",
    "call_id": "call_8675309...",
    "output": "<p align=\"center\"><code>npm i -g @openai/codex</code>..."
  }
]
```

后续查询模型时的 Prompt 结构就变成了这样：

![工具调用后的 Prompt](/images/2026-01-24-Codex-Agent-Loop-image-20260124222408150.png)

特别注意，旧的 Prompt 是新 Prompt 的精确前缀。这是刻意设计的，因为这样可以利用 Prompt 缓存，让后续请求更高效。

推理和工具调用之间可能有很多次迭代。Prompt 会不断增长，直到最终收到一条 assistant message，表示当前轮次结束：

```
data: {"type":"response.output_text.done","text": "I added a diagram to explain...", ...}
data: {"type":"response.completed","response":{...}}
```

在 Codex CLI 里，assistant message 展示给用户，输入框聚焦，提示用户轮到他们继续对话了。如果用户回复，上一轮的 assistant message 和新消息都要追加到下一次请求的 `input` 里：

```json
[
  /* ... 上次请求的所有内容 ... */
  {
    "type": "message",
    "role": "assistant",
    "content": [
      {"type": "output_text", "text": "I added a diagram to explain the client/server architecture."}
    ]
  },
  {
    "type": "message",
    "role": "user",
    "content": [
      {"type": "input_text", "text": "That's not bad, but the diagram is missing the bike shed."}
    ]
  }
]
```

因为继续对话，发给 Responses API 的 `input` 长度持续增加：

![多轮对话 Prompt 增长](/images/2026-01-24-Codex-Agent-Loop-image-20260124222428634.png)

那这个不断增长的 Prompt 对性能有什么影响？

### 性能优化

你可能会问：整个对话过程中发给 Responses API 的 JSON 数据量不是平方级增长吗？没错。Responses API 支持可选的 [`previous_response_id`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-previous_response_id) 参数来缓解这个问题，但 Codex 目前并没有使用，主要是为了保持请求完全无状态，并支持零数据留存（Zero Data Retention, ZDR）配置。

> 不用 `previous_response_id` 对 Responses API 提供方来说更简单，因为每个请求都是无状态的。这也方便支持选择了 [ZDR](https://platform.openai.com/docs/guides/migrate-to-responses#4-decide-when-to-use-statefulness) 的客户（存储支持 `previous_response_id` 所需的数据与 ZDR 相矛盾）。ZDR 客户不会因此失去利用之前轮次推理消息的能力，因为相关的 `encrypted_content` 可以在服务器端解密。OpenAI 保存 ZDR 客户的解密密钥，但不保存他们的数据。

一般来说，模型采样的成本远高于网络传输成本，采样是效率优化的主要目标。这就是为什么 **Prompt 缓存**如此重要，它让我们可以复用之前推理调用的计算结果。当缓存命中时，**模型采样是线性而非平方级的**。OpenAI 的 [Prompt 缓存文档](https://platform.openai.com/docs/guides/prompt-caching#structuring-prompts)解释得更详细：

> 只有 Prompt 的精确前缀匹配才能命中缓存。要获得缓存收益，把静态内容（如指令和示例）放在 Prompt 开头，把动态内容（如用户特定信息）放在末尾。这同样适用于图像和工具，它们在不同请求之间必须完全一致。

有了这个背景，来看看哪些操作会导致 Codex 缓存未命中：

- 在对话中途修改可用的 `tools`
- 更换目标模型（会改变原始 Prompt 的第三项，因为它包含模型特定的指令）
- 更改沙箱配置、审批模式或当前工作目录

Codex 团队在引入新功能时必须谨慎，避免破坏 Prompt 缓存。举个例子，最初支持 MCP 工具时引入了一个 [bug：没有按一致的顺序枚举工具](https://github.com/openai/codex/pull/2611)，导致缓存未命中。MCP 工具特别棘手，因为 MCP Server 可以通过 [`notifications/tools/list_changed`](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#list-changed-notification) 通知动态修改工具列表。在长对话中途响应这个通知可能导致代价高昂的缓存未命中。

在可能的情况下，处理对话中途的配置变更时，会追加一条新消息到 `input`，而不是修改之前的消息。如果沙箱配置或审批模式改变，会[插入](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L1037-L1057)一条新的 `role=developer` 消息；如果当前工作目录改变，会[插入](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L1017-L1035)一条新的 `role=user` 消息。

想尽办法确保缓存命中以优化性能。还有另一个关键资源需要管理，即上下文窗口。

### 上下文压缩

避免上下文窗口耗尽的策略是：当 token 数超过某个阈值时，压缩对话。用一个更小的、能代表原对话的新消息列表替换 `input`，让 Agent 能带着对之前发生的事情的理解继续工作。

早期的[压缩实现](https://github.com/openai/codex/pull/1527)需要用户手动执行 `/compact` 命令，用现有对话加上自定义的[摘要指令](https://github.com/openai/codex/blob/e2c994e32a31415e87070bef28ed698968d2e549/SUMMARY.md)查询 Responses API。Codex 用生成的摘要作为后续对话轮次的[新 `input`](https://github.com/openai/codex/blob/e2c994e32a31415e87070bef28ed698968d2e549/codex-rs/core/src/codex.rs#L1424)。

后来 Responses API 演进出了专门的 [`/responses/compact` API](https://platform.openai.com/docs/guides/conversation-state#compaction-advanced)，可以更高效地执行压缩。它返回一个[列表](https://platform.openai.com/docs/api-reference/responses/compacted-object)，可以替代之前的 `input` 继续对话，同时释放上下文窗口。这个列表包含一个特殊的 `type=compaction` 项，带有不透明的 `encrypted_content`，保留了模型对原始对话的理解。现在，当超过 [`auto_compact_limit`](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L2558-L2560) 时，Codex 会自动使用这个 API 压缩对话。

## 后续文章预告

OpenAI 说后续还会有更多文章，深入探讨 CLI 的架构、工具使用的实现细节，以及 Codex 的沙箱模型。后续的文章我也会继续翻译过来，欢迎关注公众号等待续文。

## 写在最后

这篇文章把 Codex CLI 的 Agent Loop 实现拆解得很细致。对于正在做或者想做 AI Agent 的朋友，有几点我觉得特别值得关注：

1. **Prompt 结构设计**：静态内容放前面、动态内容放后面，是利用 Prompt 缓存的关键。这个原则看似简单，但很多人在实际开发中容易忽略。

2. **上下文管理**：对话越长，上下文窗口管理越重要。压缩策略是必备的，不然长对话很快就会撑爆窗口。

3. **工具调用的抽象**：Codex 把工具调用抽象得很干净，对接 MCP Server 也很灵活。不过 MCP 工具动态变化可能破坏缓存这个点，确实需要注意。

如果你对实现细节感兴趣，强烈建议去翻翻 Codex 的开源代码，很多设计决策的讨论都在 GitHub Issues 和 PRs 里。

---

**相关资源：**

- Unrolling the Codex agent loop：<https://openai.com/index/unrolling-the-codex-agent-loop/>
- Codex CLI 开源仓库：<https://github.com/openai/codex>
- Responses API 文档：<https://platform.openai.com/docs/api-reference/responses>
- Open Responses 规范：<https://www.openresponses.org/>
- Codex CLI 配置文档：<https://developers.openai.com/codex/config-advanced>
- Koder: <https://github.com/feiskyer/koder>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
