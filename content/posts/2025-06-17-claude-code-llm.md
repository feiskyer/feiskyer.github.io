---
title: "Claude Code 省钱开挂：一键接入 OpenAI/Gemini/DeepSeek"
date: 2025-06-17T12:20:15+08:00
tags: [AI, Vibe Coding]
draft: false
---

Claude Code 虽然好用，但其订阅和 API 实在是太贵了。很多时候你可能想让 Claude Code 使用其他大模型（如 OpenAI GPT、DeepSeek、Gemini 等）来处理编程任务。虽然 Claude Code 原生设计为与 Anthropic 的 Claude 模型配合使用，但通过 LLM 网关代理，我们可以实现与其他模型的集成。

LLM 网关在 Claude Code 和模型提供商之间提供了一个集中的代理层，具备以下优势：

- **集中认证管理** - 统一的 API 密钥管理
- **使用情况追踪** - 监控团队和项目的使用量
- **成本控制** - 实施预算和频率限制
- **审计日志** - 跟踪所有模型交互以满足合规要求
- **模型路由** - 无需代码更改即可切换提供商

本指南将展示如何使用 [LiteLLM Proxy Server](https://docs.litellm.ai/docs/#litellm-proxy-server-llm-gateway) 来集成不同的大模型。

---

## 第一步：安装 LiteLLM

首先安装 LiteLLM 及其代理功能：

```sh
pip install 'litellm[proxy]'
```

---

## 第二步：配置不同的大模型

### Gemini + Claude Code

> 注意：Google Gemini 原生 API 转换有些问题，这儿使用的是其 OpenAI 兼容格式的 API。

创建配置文件 `config.yaml`：

```yaml
model_list:
- model_name: gemini-2.5-pro
  litellm_params:
    model: openai/gemini-2.5-pro
    api_key: os.environ/GEMINI_API_KEY
    api_base: "https://generativelanguage.googleapis.com/v1beta/openai/"
- model_name: gemini-2.5-flash
  litellm_params:
    model: openai/gemini-2.5-flash
    api_key: os.environ/GEMINI_API_KEY
    api_base: "https://generativelanguage.googleapis.com/v1beta/openai/"
```

启动 LiteLLM 代理服务：

```sh
litellm -c config.yaml
```

在新终端中启动 Claude Code：

```sh
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_MODEL=gemini-2.5-pro
export ANTHROPIC_SMALL_FAST_MODEL=gemini-2.5-flash
export DISABLE_PROMPT_CACHING=1
export ANTHROPIC_AUTH_TOKEN=litellm
claude
```

为了方便使用，你还可以自定义个 alias，简化这些环境变量的定义，比如：

```sh
alias claude='ANTHROPIC_TOKEN=litellm DISABLE_PROMPT_CACHING=1 ANTHROPIC_BASE_URL=http://localhost:4000 ANTHROPIC_MODEL=gemini-2.5-pro ANTHROPIC_SMALL_FAST_MODEL=gemini-2.5-flash claude'

claude
```

---

### DeepSeek + Claude Code

创建配置文件 `config.yaml`：

```yaml
model_list:
- model_name: deepseek-reasoner
  litellm_params:
    model: deepseek/deepseek-reasoner
    api_key: os.environ/DEEPSEEK_API_KEY
```

启动 LiteLLM 代理服务（开启详细调试）：

```sh
litellm -c config.yaml --detailed_debug
```

在新终端中启动 Claude Code：

```sh
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_MODEL=deepseek-reasoner
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-reasoner
export ANTHROPIC_AUTH_TOKEN=litellm
claude
```

---

### OpenAI + Claude Code

创建配置文件 `config.yaml`：

```yaml
model_list:
- model_name: o3
  litellm_params:
    model: openai/o3
    api_key: os.environ/OPENAI_API_KEY
- model_name: gpt-4.1
  litellm_params:
    model: openai/gpt-4.1
    api_key: os.environ/OPENAI_API_KEY
- model_name: gpt-4o
  litellm_params:
    model: openai/gpt-4o
    api_key: os.environ/OPENAI_API_KEY
```

启动 LiteLLM 代理服务：

```sh
litellm -c config.yaml --detailed_debug
```

在新终端中启动 Claude Code：

```sh
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_MODEL=gpt-4.1
export ANTHROPIC_SMALL_FAST_MODEL=gpt-4o
export ANTHROPIC_AUTH_TOKEN=litellm
claude
```

---

### Azure OpenAI + Claude Code

创建配置文件 `config.yaml`：

```yaml
model_list:
- model_name: gpt-4.1
  litellm_params:
    model: azure/gpt-4.1
    api_base: https://<replace-this>.openai.azure.com/
    api_version: "2025-04-01-preview"
    api_key: os.environ/AZURE_OPENAI_API_KEY
- model_name: o3
  litellm_params:
    model: azure/o3
    api_base: https://<replace-this>.openai.azure.com/
    api_version: "2025-04-01-preview"
    api_key: os.environ/AZURE_OPENAI_API_KEY
```

启动 LiteLLM 代理服务：

```sh
litellm -c config.yaml
```

在新终端中启动 Claude Code：

```sh
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_MODEL=o3
export ANTHROPIC_SMALL_FAST_MODEL=gpt-4.1
export ANTHROPIC_AUTH_TOKEN=litellm
claude
```

---

## 第三步：注意事项和最佳实践

### 环境变量说明

- `ANTHROPIC_BASE_URL`: 指向 LiteLLM 代理服务的地址
- `ANTHROPIC_MODEL`: 主要模型，用于复杂的编程任务
- `ANTHROPIC_SMALL_FAST_MODEL`: 快速模型，用于简单的辅助任务
- `DISABLE_PROMPT_CACHING`: 某些模型可能需要禁用提示缓存
- `ANTHROPIC_AUTH_TOKEN`：用于跳过 Anthropic 登陆验证

### 模型选择建议

- **开发和调试**: 使用快速模型（如 GPT-4o、Gemini Flash）
- **复杂编程任务**: 使用高性能模型（如 O3、Gemini 2.5 Pro、DeepSeek R1）
- **成本控制**: 结合使用不同规格的模型以平衡性能和成本

### 常见问题

1. **连接问题**: 确保 LiteLLM 代理服务正在运行
2. **API 密钥**: 确保环境变量中的 API 密钥正确设置
3. **模型兼容性**: 部分 Claude Code 特性可能需要调整才能与其他模型良好配合
4. **搜索不可用**：很多大模型 API 并不支持内置的搜索工具，需要借助 MCP 来实现
5. **提示词缓存**：部分大模型 API 不支持提示词缓存，需要通过 DISABLE_PROMPT_CACHING 把它关掉

---

## 总结

通过 LiteLLM 代理，你可以让 Claude Code 与各种大模型协作，包括：

- **Google Gemini**: 强大的多模态能力
- **DeepSeek**: 优秀的推理能力和性价比
- **OpenAI GPT**: 成熟稳定的编程辅助
- **Azure OpenAI**: 企业级的安全和合规保障

这种集成方式让你能够根据具体需求选择最合适的模型，同时享受 Claude Code 出色的开发体验。记住，不同模型的特点和能力各有差异，建议根据实际使用场景进行测试和优化。

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
