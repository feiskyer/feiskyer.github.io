---
title: "Vibe Coding 了一个 MCP AI Hub，给你的 AI Agent 一键接入 100+ AI 模型"
date: 2025-10-11T19:00:00+08:00
draft: false
tags: [Agent, AI, MCP, Claude Code, Vibe Coding]
description: "开源项目 MCP AI Hub 通过 LiteLLM 把 Claude Code、Codex 等 Agent 工具一键接入 100+ AI 模型，只需在配置文件里填好 API Key，就能在同一工具里自由切换 OpenAI、Anthropic、Google 各家模型，本文分享项目由来与使用方法。"
---

之前用 Claude Code 的时候，只能和 Claude Code 配置的单个模型聊天。想用 GPT-5 或者 Gemini 2.5 Pro，得切换到别的工具。这种来回切换不仅麻烦，还会打断思路。为了在一个工具里用上不同的模型，所以就 Vibe Coding 了 MCP AI Hub 这个项目，并开源在 <https://github.com/feiskyer/mcp-ai-hub>。

MCP AI Hub 是一个 MCP 服务器，通过 LiteLLM 把 Codex、Claude Code 等 Agent 工具连接到 100+ AI 模型。你只要在 `~/.ai_hub.yaml` 里配置好 API Key 和你所希望使用的模型，就能在各种 Agent 中随意切换 OpenAI、Anthropic、Google 等各家的模型。

## 为什么做 MCP AI Hub?

用 AI 工具时，我经常会遇到一个问题：每个模型擅长的能力都不同，而每个工具只能用配置好的单个模型，想换个模型打个辅助就得换工具。

而现在有了 MCP AI Hub，在 AI Agent 里就能：

- 用 Claude Code 作为 Agent 收集上下文并做编程开发；
- 用 GPT-5 审核 Claude Code 的修改计划以及代码变更；
- 用 Nano Banana 画示意图。

## MCP AI Hub 包含什么?

MCP AI Hub 通过 LiteLLM 提供统一接口，把不同 AI 服务商的 API 统一起来，主要功能包括：

### 1. 统一的模型接口

不管是 OpenAI、Anthropic 还是 Google，都用同一套 API 调用。

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: "sk-your-openai-key"
      max_tokens: 2048
      temperature: 0.7

  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: "sk-ant-your-anthropic-key"
      max_tokens: 4096
```

### 2. 支持 100+ AI 提供商

参照 [LiteLLM 文档](https://docs.litellm.ai/docs/providers)，MCP AI Hub 支持所有主流 AI 服务商的模型，包括 OpenAI、Google Gemini、Anthropic 以及各类本地大模型。

### 3. 系统提示词配置

可以为每个模型设置专门的系统提示词：

```yaml
global_system_prompt: "你是一个专业的 AI 助手。"

model_list:
  - model_name: gpt-4
    system_prompt: "你是一个精准的代码助手。"
    litellm_params:
      model: openai/gpt-4
      api_key: "sk-your-key"

  - model_name: claude-sonnet
    system_prompt: ""  # 空字符串会禁用全局提示词
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: "sk-ant-your-key"
```

### 4. MCP 工具集成

提供三个核心工具，简单够用：

- **`chat`**：与指定模型对话；
- **`list_models`**：列出所有配置的模型；
- **`get_model_info`**：查看模型配置详情。

## 如何使用

### 快速安装

```bash
# 方式一:从 PyPI 安装
pip install mcp-ai-hub

# 方式二:用 uv 安装(推荐)
uv tool install mcp-ai-hub

# 方式三:从源码安装
pip install git+https://github.com/feiskyer/mcp-ai-hub.git
```

### 配置 API Key

在 `~/.ai_hub.yaml` 里创建配置文件：

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: "sk-your-openai-api-key"
      max_tokens: 2048
      temperature: 0.7

  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: "sk-ant-your-anthropic-api-key"
      max_tokens: 4096
      temperature: 0.7
```

### 连接到 Claude Desktop

编辑配置文件：

**macOS**：`~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ai-hub": {
      "command": "mcp-ai-hub"
    }
  }
}
```

### 连接到 Claude Code

```bash
claude mcp add -s user ai-hub mcp-ai-hub
```

然后在 Claude Code 里就能这样用：

```
用 gpt-4 帮我分析这段代码的性能问题
用 claude-sonnet 写一个快速排序的实现
用 gemini-2.5-flash-image 画XXX图
用 gemini-2.5-pro 总结这个 100 页的文档
```

## 本地模型配置

如果你想用本地模型保护隐私，可以这样配置：

```yaml
model_list:
  - model_name: local-llama
    litellm_params:
      model: openai/llama-2-7b-chat
      api_key: "dummy-key"  # 本地服务器通常接受任意 API key
      api_base: "http://localhost:8080/v1"
      max_tokens: 4000
      temperature: 0.7
```

这样就能用 Ollama 或者 LM Studio 等本地服务了。

## 与 Zen MCP 的对比

可能有人会问，已经有 [Zen MCP](https://github.com/BeehiveInnovations/zen-mcp-server) 了，为什么还要 MCP AI Hub？

Zen MCP 是一个功能非常丰富的 MCP 服务器，提供了 `codereview`、`debug`、`planner`、`consensus` 等十几种工具。每个工具都有自己的多步骤工作流、参数和描述，这些都会消耗 AI Agent 的上下文窗口。所以，这也就带来一个问题：**工具太多会占用大量上下文空间**。

比如，使用 Claude Code 的 /context 可以看到默认配置大概会占用 24.5k 的上下文空间：

![image-20251011213043642](/images/5d18a92f-6032-4a64-b154-336736e5f4c7.png)

**MCP AI Hub 的设计理念恰恰相反**：

- **简单高效**：只提供 3 个核心工具（`chat`、`list_models`、`get_model_info`），没有附加功能；
- **专注模型接入**：不做复杂的工作流，只做一件事 — 连接模型；
- **节省上下文**：工具少，占用的上下文空间就少，给 AI 更多空间思考；
- **灵活组合**：可以和其他 MCP 服务器配合使用，各司其职。

如果你需要的是：在不同 AI 模型间切换、快速接入新的 AI 服务商、保持工具简洁、不浪费上下文空间，那 MCP AI Hub 会是更合适的选择。而如果你需要完整的代码审查、规划、共识等工作流，Zen MCP 会更适合。

---

**项目地址**：<https://github.com/feiskyer/mcp-ai-hub>

**相关资源**：

- LiteLLM 文档：<https://docs.litellm.ai/docs/providers>
- MCP 协议：<https://modelcontextprotocol.com>
- Zen MCP 项目：<https://github.com/BeehiveInnovations/zen-mcp-server>
