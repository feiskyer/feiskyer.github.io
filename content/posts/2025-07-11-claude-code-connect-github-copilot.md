---
title: "Claude Code 接入 Github Copilot 模型"
date: 2025-07-11T14:44:38+08:00
draft: false
tags: [AI, Vibe Coding]
---

还在为 Claude API 费用发愁？想用最强的 Claude Code 却又舍不得公司提供的 GitHub Copilot 订阅？

作为一个每天都在和各种 AI 编程工具打交道的开发者，我发现很多同学都有这样的困扰。Github Copilot 确实在 2025 年加入了强大的 Agent 模式和 Claude 4 模型支持，比以前好用太多了！但说实话，跟 Claude Code 这种新一代 AI 编程工具相比，在复杂编程任务的处理上还是有明显差距。

既然很多公司都给员工配备了 GitHub Copilot 订阅，那我们能不能 "鱼和熊掌兼得"——用 GitHub Copilot 的模型直接驱动 Claude Code，既享受最强的编程体验，又能省下 Claude 的 API/订阅 费用呢？

今天就带你一起探索这个 "开挂" 玩法！

## 调用 GitHub Copilot API 违规吗？

答案是否定的！根据 GitHub Copilot [官方文档](https://docs.github.com/en/copilot/how-tos/build-copilot-extensions/building-a-copilot-agent-for-your-copilot-extension/using-copilots-llm-for-your-agent) 的说明：

> Copilot 的大型语言模型 (LLM) 是一个强大的大规模语言模型，经过多种数据源的训练，包括代码、文档和其他文本。Copilot 的 LLM 支持 GitHub Copilot 的功能，用于驱动所有 Copilot 功能，包括代码生成、文档生成和代码补全。您可以选择使用 Copilot 的 LLM 来支持您的代理，这在您希望代理能够为用户消息生成补全但又不想管理自己的 LLM 时非常有用。

**简单来说，GitHub Copilot 提供了一个标准的 OpenAI 格式 API 端点：`https://api.githubcopilot.com/chat/completions`**，这意味着支持 OpenAI API 的 Agent 工具理论上都能接入！

为了方便你使用，GitHub 官方还贴心地提供了示例代码：

```ts
  // Use Copilot's LLM to generate a response to the user's
  //  messages, with our extra system messages attached.
  const copilotLLMResponse = await fetch(
    "https://api.githubcopilot.com/chat/completions",
    {
      method: "POST",
      headers: {
        authorization: `Bearer ${tokenForUser}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        messages,
        stream: true,
      }),
    }
  );
```

## 如何让 Claude Code 用上 GitHub Copilot？

理论很美好，现实却有个小问题：**Claude Code 只接受 Anthropic API 格式，而 GitHub Copilot 提供的是 OpenAI 格式**！

不过别担心，既然都是标准格式，自然有办法解决。目前已经有很多工具实现了这个转换，比如：

- **[Aider](https://aider.chat/docs/llms/github.html)**：原生支持 GitHub Copilot；
- **[Cline](https://docs.cline.bot/provider-config/vscode-language-model-api)**：VS Code 插件，通过 VSCode 内置功能同样支持。

对于 Claude Code，我们则需要一个 "翻译官" 来做格式转换。你可以利用 AI 快速 Vibe Code 一个转换工具，当然也可以直接使用相关的开源项目。这里我推荐 **[copilot-api](https://github.com/ericc-ch/copilot-api)**！

这个工具的厉害之处在于：

- **双格式支持**：同时提供 OpenAI 和 Anthropic 兼容的 API 端点；
- **Claude Code 专用优化**：专门为 Claude Code 做了适配；
- **一键启动**：通过 `--claude-code` 参数可以自动配置。

## 手把手教你配置

首先确保你的系统已经安装了 [Node.js](https://nodejs.org/en/download)，然后安装必要的工具：

```sh
npm install -g copilot-api
```

如果你还没有安装 Claude Code，同样一行命令搞定：

```sh
npm install -g @anthropic-ai/claude-code
```

### 启动 copilot-api 代理服务

接下来，打开第一个终端，启动代理服务：

```sh
copilot-api start
```

这时候会提示你进行 GitHub 授权，**一定要注意这一步**：

```sh
...
Please visit https://github.com/login/device and enter code XXXX-XXXX to authenticate
...
```

按照提示访问 GitHub 登录页面，输入设备码完成授权。成功后你会看到可用模型列表以及 API 调用地址：

```sh
...
- claude-3.5-sonnet
- claude-3.7-sonnet
- claude-3.7-sonnet-thought
- claude-sonnet-4
- claude-opus-4
- gemini-2.0-flash-001
- gemini-2.5-pro
- o3
...
  ➜ Listening on: http://localhost:4141/ (all interfaces)
```

看到这么多模型是不是很激动？**特别是 Claude Sonnet 4 和 Claude Opus 4，这些都是可用的！**

### 配置 Claude Code

打开第二个终端，创建 Claude Code 配置文件。在 `~/.claude/settings.json` 中添加以下配置：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:4141",
    "ANTHROPIC_AUTH_TOKEN": "dummy",
    "ANTHROPIC_MODEL": "claude-sonnet-4",
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-3.7-sonnet",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

**配置说明**：

- `ANTHROPIC_BASE_URL`: 指向本地代理服务地址；
- `ANTHROPIC_AUTH_TOKEN`: 填写任意值即可（代理会处理真实的认证）；
- `ANTHROPIC_MODEL`: 主要模型，推荐 `claude-opus-4` 或 `claude-sonnet-4`；
- `ANTHROPIC_SMALL_FAST_MODEL`: 快速模型，用于轻量级任务；
- 后两个参数用于优化性能，减少不必要的调用。

配置完成后，在终端继续执行：

```sh
claude
```

如果一切顺利，你就成功用上了由 GitHub Copilot 驱动的 Claude Code！🎉

## 结语

通过这个方案，我们成功实现了 "鱼和熊掌兼得"——既能享受 Claude Code 的强大编程能力，又能充分利用公司提供的 GitHub Copilot 资源。

最后还要提醒一下，频繁调用时 Github Copilot 可能会有限流问题，特别是高级模型。此时，你可以先切换到稍弱一点的模型继续使用。

你还尝试过类似的组合方案？欢迎在评论区分享你的使用体验！

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)
