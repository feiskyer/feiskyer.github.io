---
title: "OpenAI Codex 零基础入门指南"
date: 2025-09-04T22:20:28+08:00
draft: false
tags: [AI, Vibe Coding, Codex, OpenAI]
description: "OpenAI Codex 零基础入门指南，介绍 Codex Cloud、Codex CLI 和 VSCode 扩展三大产品形态，分析它相比 Claude Code 在开源、GPT-5 指令遵循、慷慨限额和外接模型方面的优势与上手技巧。"
---

Codex 是 OpenAI 推出的 AI 编程工具，包含三个核心产品：

- **Codex Cloud**（云端托管版）
- **Codex CLI**（本地终端工具）
- **VSCode 扩展**（IDE 集成版）。

尤其是 VSCode 扩展版的 Codex，界面简洁不说，还把本地的 Codex CLI 和托管 ChatGPT Codex 整合在了一起，吸引了一大波 Vibe Coding 粉。

再配合 Claude Opus/Sonnet 4 降智以及 Cursor 涨价风波，Codex 这波直接赢麻了，两周内暴涨10倍！

![](/images/20251127091133.png)

## 为什么 Codex 值得上手

根据这段时间的使用，OpenAI Codex 具有以下几个 Claude Code 不具备的优势：

1. Codex 完全开源，并且社区活跃；
2. GPT-5 指令遵循大幅领先，不像 Claude 那样随便发挥；

3. ChatGPT 限额慷慨，GPT-5 Plus 用户每5小时 30-150 条消息，Pro 用户每5小时 300-1500 条消息；

4. 原生支持外接模型，你甚至可以同时配置多个不同的 AI 模型，随时切换使用。

这儿再分享几个 Codex + GPT-5 high 完胜 Claude Code 的场景：

1. 参考 A 实现 B 这种需求明确的场景，Codex 会看懂已有代码，照样子写新代码，不碰其他无关代码；而 Claude Code 则会分析项目、重构代码、顺便可能还会尝试做各种优化。

2. 新增测试用例，Codex 会看懂现有测试后补充新的测试用例，不多不少，就是我想要的。

3. 修小 bug （比如 CSS 样式问题），Codex 改完 CSS 就收手了，而 Claude Code 大多数情况下都会顺手做一些优化，导致代码变复杂。

## 快速安装

Codex 支持 macOS、Ubuntu/Debian 以及 Windows WSL2。安装起来也比较方便：

```sh
# 方法一：使用NodeJS
npm install -g @openai/codex

# 方法二：使用Homebrew
brew install codex
```

安装完成后直接在终端中执行 `codex` 即可。

## 登录配置

### 使用 ChatGPT

如果你订阅了 ChatGPT，那首次运行 Codex 时，你可以选择通过 ChatGPT 账户登录：

![](/images/20251127091207.png)

登录后，你的认证信息会保存在 `~/.codex/auth.json` 文件中，默认使用 GPT-5 模型。你可以通过 `/model` 命令来切换 GPT-5 模型的不同版本，推荐使用 GPT-5 high 。

> 注意 ChatGPT 账户限额：
>
> * Plus/Business、Enterprise/Edu 订阅：每5小时可发送 30-150 条消息；
> * Pro 订阅：每5小时可发送 300-1500 条消息；

### 使用 API Key（按量付费）

如果没有订阅 ChatGPT，你也可以通过自定义的 API Key 使用。比如：

```sh
# 设置环境变量
export OPENAI_API_KEY="your-api-key-here"

# 启动Codex
codex
```

对于其他 AI 服务商，则需要在配置文件 `~/.codex/config.toml`  中修改，比如以下是几个 Open Router、Ollama、Azure 等的配置示例：

```toml
model = "gpt-5"
model_reasoning_effort = "high"
model_provider = "openrouter"

[model_providers.openrouter]
name = "Open Router"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"
wire_api = "chat"
query_params = {}

[model_providers.ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"

[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"  # Or "OPENAI_API_KEY", whichever you use.
query_params = { api-version = "2025-04-01-preview" }
```

配置完成后，在使用时先导出环境变量再运行 codex 即可：

```sh
export OPENROUTER_API_KEY="your-api-key-here"

# 使用-m覆盖默认模型
codex -m openai/gpt-5
```

### 服务器认证（SSH用户必看）

那么，在没有浏览器的服务器上能不能使用呢？这里有个巧妙的方法：

```bash
# 本地机器先完成认证，然后复制认证文件
scp ~/.codex/auth.json user@remote:~/.codex/auth.json

# 然后在远程服务器上就可以通过ChatGPT认证使用codex了
```

说实话，这个设计还是挺贴心的，考虑到了各种使用场景。

---

## 入门使用

### 基础命令速查

```bash
# 交互式TUI模式
codex

# 带初始提示启动
codex "fix lint errors"

# 非交互式自动化模式
codex exec "explain utils.ts"

# 沙盒自动模式
codex --full-auto "create the fanciest todo-list app"

# 非沙盒自动模式
codex --dangerously-bypass-approvals-and-sandbox "create the fanciest todo-list app"
```

### 提示词示例

| ✨    | 提示词                                                       | 功能                                                |
| ---- | ------------------------------------------------------------ | --------------------------------------------------- |
| 1    | `codex "Refactor the Dashboard component to React Hooks"`    | Codex 重写了类组件，运行了 `npm test`，并显示了差异 |
| 2    | `codex "Generate SQL migrations for adding a users table"`   | 推断你的ORM，创建迁移文件，并在沙盒数据库中运行它们 |
| 3    | `codex "Write unit tests for utils/date.ts"`                 | 生成测试，执行测试，并反复迭代直到通过              |
| 4    | `codex "Bulk-rename *.jpeg -> *.jpg with git mv"`            | 安全地重命名文件并更新导入/使用                     |
| 5    | `codex "Explain what this regex does: ^(?=.*[A-Z]).{8,}$"`   | 输入一步步的解释                                    |
| 6    | `codex "Carefully review this repo, and propose 3 high impact well-scoped PRs"` | 建议在当前代码库中提出有影响力的PR                  |
| 7    | `codex "Look for vulnerabilities and create a security review report"` | 发现并解释安全漏洞                                  |

## 实用技巧

### AGENTS.md 记忆

[AGENTS.md](https://agents.md/) 记忆功能类似 Claude Code 的 CLAUDE.md，让 AI 记住项目特定的指导：

```bash
# 全局配置
~/.codex/AGENTS.md

# 项目配置
./AGENTS.md

# 子目录配置
./components/AGENTS.md
```

你可以在 codex 中输入 `/init` 提示，让 codex 帮你生成初始的 AGENTS.md 文件。

### 自定义命令

Codex 也支持自定义斜杠命令，不过它叫自定义提示词，存放路径为 `~/.codex/prompts/`。自定义命令要求：

* 文件必须是 Markdown 格式；
* 文件名作为命令名称，即最终的命令格式为 `/<filename>`（不带 `.md` 后缀）；
* 自定义命令不支持参数，所以提示词必须要自包含（即在需要补充上下文的场景中，提示词要能指导AI去找到相关上下文）；
* 新建自定义命令后需要重启 Codex 命令才生效。

### 全自动化模式

在 Github Actions 等自动化流程中，你可以配置 Codex 全自动化执行：

```yaml
- name: Update changelog via Codex
  run: |
    npm install -g @openai/codex
    export OPENAI_API_KEY="${{ secrets.OPENAI_KEY }}"
    codex exec --full-auto "update CHANGELOG for next release"
```

## 核心配置详解

`~/.codex/config.toml` 是 Codex 核心配置文件，我调试了半天找到几个关键配置。

首先是全局配置，这些选项需要放在配置文件开头部分：

```toml
# 模型选择（GPT-5 + High推理）
model = "gpt-5"
model_reasoning_effort = "high"

# 默认模型提供商
model_provider = "openai"

# 沙盒策略（支持 read-only、workspace-write以及danger-full-access）
sandbox_mode = "workspace-write"

# 审批策略（支持 on-failure、on-request、untrusted以及never）
approval_policy = "on-failure"
```

然后是模型配置，包含 Model Provider 和 Profile 配置。Model Provider 定义了 AI 提供商的配置，比如API 类型、URL、API Key、Header 等；而 Profile 则定义了模型和AI提供商的一组配置，方便配置的复用。

```toml
# Model Providers
[model_providers.openrouter]
name = "Open Router"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"
wire_api = "chat"
query_params = {}

[model_providers.openai]
name = "OpenAI using Chat Completions"
base_url = "https://api.openai.com/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"

# Profiles
[profiles.o3]
model = "o3"
model_provider = "openai"
approval_policy = "never"
model_reasoning_effort = "high"
model_reasoning_summary = "detailed"

[profiles.gpt5]
model = "openai/gpt-5"
model_provider = "openrouter"
```

配置好之后，你可以通过 Codex 的命令行参数来选择，比如 `codex -p <profile>`；当然，也可以用 `codex -m <model>` 来覆盖默认模型（注意这里使用默认的AI提供商，即OpenAI）。

### MCP 配置

Codex 也支持 MCP 服务，但仅限于 stdio 模式，配置方法如下所示：

```toml
[mcp_servers.server-name]
command = "npx"
args = ["-y", "mcp-server"]
env = { "API_KEY" = "value" }
```

### 网络配置调优

如果遇到网络慢的问题，可以单独调整：

```toml
[model_providers.openai]
request_max_retries = 4            # retry failed HTTP requests
stream_max_retries = 10            # retry dropped SSE streams
stream_idle_timeout_ms = 300000    # 5m idle timeout
```

## Codex VSCode 插件

为了方便使用，Codex 直接提供了一个原生的 VSCode 插件，在插件市场搜索即可安装：

![](/images/images20251127091256.png)

需要注意的是，Codex 插件在首次使用之前必须要登录 ChatGPT 账户。对于订阅了 ChatGPT Plus/Pro 的用户，用起来会非常丝滑。

不过，未订阅 ChatGPT 的用户就很麻烦了，这里推荐一个配置方法：

* 首先，还是按照前面的步骤安装 Codex CLI，并配置好模型提供商、API Key 等；
* 然后注册一个免费用户，使用免费用户登录 VSCode Codex 插件。

这样，你就可以继续使用 BYO 模型继续使用。

## Codex Cloud

Codex Cloud 是一款基于云的软件工程智能体，可以并行处理多项任务。Codex 可以执行各种任务，如编写功能、回答有关代码库的问题、修复错误和提出拉取请求以供审核；每项任务都在自己的云沙箱环境中运行。

![](/images/20251127091418.png)

Codex Cloud 需要订阅 ChatGPT（Plus、Team、Pro 或 Enterprise），可以直接在 <https://chatgpt.com/codex> 或者 ChatGPT App 中使用。

## 总结

经过这段时间的深度体验，说实话，Codex 确实有点东西。

特别是在 Claude Code “随便发挥”的对比下，GPT-5 的指令遵循能力简直是降维打击。你让它改个 CSS，它就只改 CSS；你让它写个测试，它就只写测试，不会顺手给你重构一遍代码。

当然，配置复杂、网络依赖这些问题还是存在的。但如果你订阅了 ChatGPT Plus/Pro，或者就是喜欢折腾不同的 AI 模型，Codex 绝对值得一试。
