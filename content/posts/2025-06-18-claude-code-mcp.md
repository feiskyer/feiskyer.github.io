---
title: "Claude Code MCP 扩展：外部工具接入指南"
date: 2025-06-18T18:19:45+08:00
tags: [AI, Vibe Coding, Claude Code]
draft: false
---

Claude Code 虽然内置了丰富的工具，但在某些场景下你可能需要接入外部服务或自定义工具。Model Context Protocol (MCP) 正是为此而生的开放协议，它让 Claude Code 能够无缝集成各种外部工具和数据源，大大扩展了其能力边界。

MCP 的核心优势包括：

- **标准化接口** - 统一的协议让集成变得简单可靠
- **安全可控** - 细粒度的权限管理确保系统安全
- **生态丰富** - 大量现成的 MCP 服务器可直接使用
- **易于扩展** - 支持自定义工具和数据源集成

本文将详细介绍如何为 Claude Code 配置和使用 MCP 服务器。

> **安全提醒**：使用第三方 MCP 服务器需要自担风险。务必确保信任所使用的 MCP 服务器，特别是涉及网络交互的服务器，防范潜在的提示注入攻击和私有数据泄漏。

---

## 了解 Claude Code 内置工具

在添加外部工具之前，先了解 Claude Code 的内置工具能力：

| 工具名称 | 功能描述 | 需要权限 |
| --- | --- | --- |
| **Agent** | 运行子代理处理复杂多步骤任务 | 否 |
| **Bash** | 执行 shell 命令 | 是 |
| **Edit** | 对文件进行精确编辑 | 是 |
| **Glob** | 基于模式匹配查找文件 | 否 |
| **Grep** | 在文件内容中搜索模式 | 否 |
| **LS** | 列出文件和目录 | 否 |
| **MultiEdit** | 对单个文件执行多项原子性编辑 | 是 |
| **NotebookEdit** | 修改 Jupyter notebook 单元格 | 是 |
| **NotebookRead** | 读取并显示 Jupyter notebook 内容 | 否 |
| **Read** | 读取文件内容 | 否 |
| **TodoRead** | 读取当前会话的任务列表 | 否 |
| **TodoWrite** | 创建和管理结构化任务列表 | 否 |
| **WebFetch** | 从指定 URL 获取内容 | 是 |
| **WebSearch** | 执行带域名过滤的网络搜索 | 是 |
| **Write** | 创建或覆盖文件 | 是 |

这儿注意，WebSearch 是 Anthropic API 提供的内置搜索工具，使用非 Claude 模型时需要借助 MCP 将其替换掉。

---

## Claude Code 工具调用权限管理

### 查看和管理权限

使用 `/permissions` 命令或编辑 `settings.json` 文件来管理工具权限：

```bash
# 在 Claude Code 中查看权限设置
> /permissions
```

### 权限规则说明

权限规则遵循 `Tool(optional-specifier)` 格式：

- **允许规则（allow）**：Claude Code 可无需用户确认直接使用指定工具
- **拒绝规则（deny）**：阻止 Claude Code 使用指定工具，优先级高于允许规则
- **工具名称**：仅指定工具名表示匹配该工具的任何使用

### 配置示例

创建或编辑 `~/.claude/settings.json`：

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

---

## 添加和管理 MCP 服务器

你可以使用 `claude mcp add` 命令来添加 MCP 服务器：

```sh
Usage: claude mcp add [options] <name> <commandOrUrl> [args...]

Add a server

Options:
  -s, --scope <scope>          Configuration scope (local, user, or project) (default: "local")
  -t, --transport <transport>  Transport type (stdio, sse, http) (default: "stdio")
  -e, --env <env...>           Set environment variables (e.g. -e KEY=value)
  -H, --header <header...>     Set HTTP headers for SSE transport (e.g. -H "X-Api-Key: abc123" -H "X-Custom: value")
  -h, --help                   Display help for command
```

这其中，需要注意 `-s` 或 `--scope` 标志用来指定配置存储位置：

- **local**（默认）：仅在当前项目中可用
- **project**：通过 `.mcp.json` 文件与项目成员共享
- **user**：跨所有项目可用

### 添加 stdio 模式的 MCP 服务器

stdio 模式是最常见的 MCP 服务器连接方式：

```bash
# 基本语法
claude mcp add <name> <command> [args...]

# 示例：添加 Context7
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

### 添加 HTTP/SSE 模式的 MCP 服务器

对于基于 HTTP 或 SSE 的 MCP 服务器：

```bash
# 基本语法
claude mcp add --transport sse <name> <url>
claude mcp add --transport http <name> <url>

# 示例：添加 SSE 服务器
claude mcp add --transport sse api-server https://api.example.com/mcp
```

### 使用 JSON 配置添加服务器

对于复杂的配置需求：

```bash
# 基本语法
claude mcp add-json <name> '<json>'

# 示例：使用 JSON 配置
claude mcp add-json weather-api '{
  "type": "stdio",
  "command": "/path/to/weather-cli",
  "args": ["--api-key", "abc123"],
  "env": {"CACHE_DIR": "/tmp"}
}'
```

### 从 Claude Desktop 导入配置

如果你已经在 Claude Desktop 中配置了 MCP 服务器，可以一键导入：

```bash
# 导入 Claude Desktop 的 MCP 配置
claude mcp add-from-claude-desktop
```

运行后会显示交互式对话框，让你选择要导入的服务器。

---

### 管理 MCP 服务器

### 基本管理命令

```bash
# 列出所有配置的服务器
claude mcp list

# 查看特定服务器详情
claude mcp get my-server

# 删除服务器
claude mcp remove my-server

# 在 Claude Code 中检查服务器状态
> /mcp
```

---

## 将 Claude Code 作为 MCP 服务器

当然，除了接入外部 MCP 服务器，Claude Code 自己也可以作为 MCP 服务器，为其他应用提供服务。

### 启动 Claude Code MCP 服务器

```bash
# 启动 MCP 服务器模式
claude mcp serve
```

### Claude Desktop 连接 Claude Code

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "claude-code": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

---

## Claude Code + Gemini 实战示例

首先，创建 LiteLLM 配置文件 `litellm_config.yaml`：

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

然后，启动 LiteLLM 代理：

```bash
export GEMINI_API_KEY="<your-api-key>"
litellm -c litellm_config.yaml
```

在 shell 配置中添加 alias（`~/.zshrc` 或 `~/.bashrc`），方便后续使用 claude 命令：

```bash
alias claude='ANTHROPIC_AUTH_TOKEN=litellm DISABLE_PROMPT_CACHING=1 ANTHROPIC_BASE_URL=http://localhost:4000 ANTHROPIC_MODEL=gemini-2.5-pro ANTHROPIC_SMALL_FAST_MODEL=gemini-2.5-flash claude'
```

此时，Claude Code 执行网络搜索会直接失败：

![](/images/claude-code-fail.png)

接下来，给 Claude Code 添加网络搜索的 MCP，比如使用Brave（也可以替换成其他你喜欢的网络搜索MCP）：

```sh
BRAVE_API_KEY='<replace-your-key>'
claude mcp add brave-search -e BRAVE_API_KEY=$BRAVE_API_KEY -- npx -y @modelcontextprotocol/server-brave-search
```

然后再次执行网络搜索，Claude Code 会询问你是否同意执行 brave 搜索工具：

![](/images/claude-code-ask.png)

选择同意后，就可以继续搜索你想要的结果了：

![](/images/claude-code-search.png)


---

## 高级配置和最佳实践

### 环境变量管理

使用 `-e` 标志设置环境变量：

```bash
# 设置 API 密钥
claude mcp add api-service -e API_KEY=your-key -e TIMEOUT=30 -- service-command

# 使用环境变量文件
claude mcp add secure-service -e @.env -- secure-command
```

### 超时配置

使用 `MCP_TIMEOUT` 环境变量配置服务器启动超时：

```bash
# 设置 10 秒超时
MCP_TIMEOUT=10000 claude
```

### 安全配置建议

1. **最小权限原则**：只授予必要的工具权限
2. **网络隔离**：对网络相关的 MCP 服务器特别谨慎
3. **定期审计**：定期检查 MCP 服务器配置和权限
4. **日志监控**：关注 MCP 服务器的运行日志

---

## 总结

通过 MCP，Claude Code 的能力边界得到了极大的扩展。你可以：

- **集成外部 API**：搜索、Github、Context7 等各种在线服务
- **连接数据库**：直接查询和操作数据库
- **自定义工具**：开发专属的业务逻辑工具
- **企业集成**：连接内部系统和服务

MCP 让 Claude Code 从一个代码助手进化为一个可无限扩展的智能工作平台。合理配置权限，选择可信的 MCP 服务器，你就能构建出适合自己的 AI 开发环境。

---

欢迎长按下面的二维码关注 **漫谈云原生** 公众号，了解更多云原生和 AI 知识。

![](https://feisky.xyz/assets/mp.png)