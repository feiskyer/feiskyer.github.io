---
title: "通过 MCP 为 Claude Code 接入外部工具"
date: 2025-06-18T18:19:45+08:00
tags: [AI, Vibe Coding]
draft: false
---

Model Context Protocol (MCP) 是一个开放协议，使大语言模型能够访问外部工具和数据源。关于 MCP 的更多详细信息，请参阅 [MCP 文档](https://modelcontextprotocol.io/introduction)。

> 使用第三方 MCP 服务器需要自担风险。确保您信任 MCP 服务器，特别是当使用与互联网交互的 MCP 服务器时要格外小心，因为这些可能会使您面临提示注入风险。


## Tools available to Claude

Claude Code has access to a set of powerful tools that help it understand and modify your codebase:

| Tool | Description | Permission Required |
| --- |  --- |  --- |
| **Agent** | Runs a sub-agent to handle complex, multi-step tasks | No |
| --- |  --- |  --- |
| **Bash** | Executes shell commands in your environment | Yes |
| **Edit** | Makes targeted edits to specific files | Yes |
| **Glob** | Finds files based on pattern matching | No |
| **Grep** | Searches for patterns in file contents | No |
| **LS** | Lists files and directories | No |
| **MultiEdit** | Performs multiple edits on a single file atomically | Yes |
| **NotebookEdit** | Modifies Jupyter notebook cells | Yes |
| **NotebookRead** | Reads and displays Jupyter notebook contents | No |
| **Read** | Reads the contents of files | No |
| **TodoRead** | Reads the current session's task list | No |
| **TodoWrite** | Creates and manages structured task lists | No |
| **WebFetch** | Fetches content from a specified URL | Yes |
| **WebSearch** | Performs web searches with domain filtering | Yes |
| **Write** | Creates or overwrites files | Yes |


## Configuring permissions

You can view & manage Claude Code’s tool permissions with `/permissions` or inside `settings.json`. This UI lists all permission rules and the settings.json file they are sourced from.

Allow rules will allow Claude Code to use the specified tool without further manual approval.
Deny rules will prevent Claude Code from using the specified tool. Deny rules take precedence over allow rules.
Permission rules use the format: Tool(optional-specifier)

A rule that is just the tool name matched any use of that tool. For example, adding Bash to the list of allow rules would allow Claude Code to use the Bash tool without requiring user approval.

here is an example of settings.json:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)"
    ]
  }
}
```

## 配置 MCP 服务器

### 添加 MCP stdio 服务器

```bash
# 基本语法
claude mcp add <name> <command> [args...]

# 示例：添加本地服务器
claude mcp add my-server -e API_KEY=123 -- /path/to/server arg1 arg2
```

### 添加 MCP SSE 服务器

```bash
# 基本语法
claude mcp add --transport sse <name> <url>

# 示例：添加 SSE 服务器
claude mcp add --transport sse sse-server https://example.com/sse-endpoint
```

### 从 JSON 添加 MCP 服务器

```bash
# 基本语法
claude mcp add-json <name> '<json>'

# 示例：使用 JSON 配置添加 stdio 服务器
claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
```

## 从 Claude Desktop 导入 MCP 服务器

假设您已经在 Claude Desktop 中配置了 MCP 服务器，并希望在 Claude Code 中使用相同的服务器，而无需手动重新配置它们。

```bash
claude mcp add-from-claude-desktop
```

运行命令后，您将看到一个交互式对话框，允许您选择要导入的服务器。


### 管理 MCP 服务器

```bash
# 列出所有配置的服务器
claude mcp list

# получить详细信息for specific服务器
claude mcp get my-server

# 删除服务器
claude mcp remove my-server
```

## MCP 小提示

* 使用 `-s` 或 `--scope` 标志指定配置存储位置：
  * `local`（默认）：仅在当前项目中对您可用（在旧版本中称为 `project`）
  * `project`：通过 `.mcp.json` 文件与项目中的每个人共享
  * `user`：跨所有项目对您可用（在旧版本中称为 `global`）
* 使用 `-e` 或 `--env` 标志设置环境变量（例如，`-e KEY=value`）
* 使用 MCP_TIMEOUT 环境变量配置 MCP 服务器启动超时（例如，`MCP_TIMEOUT=10000 claude` 设置 10 秒超时）
* 随时使用 Claude Code 中的 `/mcp` 命令检查 MCP 服务器状态
* MCP 遵循客户端-服务器架构，其中 Claude Code（客户端）可以连接到多个专门的服务器

## 将 Claude Code 用作 MCP 服务器

假设您希望将 Claude Code 本身用作其他应用程序可以连接的 MCP 服务器，为它们提供 Claude 的工具和功能。

### 启动 Claude 作为 MCP 服务器

```bash
# 基本语法
claude mcp serve
```

### 从其他应用程序连接

您可以从任何 MCP 客户端连接到 Claude Code MCP 服务器，例如 Claude Desktop。如果您使用 Claude Desktop，可以使用此配置添加 Claude Code MCP 服务器：

```json
{
  "command": "claude",
  "args": ["mcp", "serve"],
  "env": {}
}
```

## 使用示例

下面以 Gemini 为例，来看看具体的使用方法。

创建 LiteLLM 配置文件 `litellm_config.yaml`：

```yaml
model_list:
- model_name: "gemini-2.5-pro"
  litellm_params:
    model: "openai/gemini-2.5-pro"
    api_key: "os.environ/GEMINI_API_KEY"
    api_base: "https://generativelanguage.googleapis.com/v1beta/openai/"
- model_name: "gemini-2.5-flash"
  litellm_params:
    model: "openai/gemini-2.5-flash"
    api_key: "os.environ/GEMINI_API_KEY"
    api_base: "https://generativelanguage.googleapis.com/v1beta/openai/"
```

运行LiteLLM：

```sh
export GEMINI_API_KEY="<replace-your-key>"
litellm -c litellm_config.yaml
```

在你的 SHELL 配置中添加 alias（路径为 `$HOME/.zshrc`或 `$HOME/.bashrc`：

```sh
alias claude='ANTHROPIC_AUTH_TOKEN=litellm DISABLE_PROMPT_CACHING=1 ANTHROPIC_BASE_URL=http://localhost:4000 ANTHROPIC_MODEL=gemini-2.5-pro ANTHROPIC_SMALL_FAST_MODEL=gemini-2.5-flash claude'
```
