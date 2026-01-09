---
title: "开源我的 Codex 配置：把 AI 编程助手调教成你的专属助理"
date: 2025-10-13T19:00:00+08:00
draft: false
tags: [AI, Codex, OpenAI, GitHub Copilot]
---

继 Claude Code 配置开源后，我把 OpenAI Codex CLI 的配置也开源了，放在 <https://github.com/feiskyer/codex-settings> 上。这套配置支持多种模型提供商（包括 ChatGPT、GitHub Copilot、DeepSeek、Ollama），并把之前 Claude Code 的配置迁移了过来，包括  Kiro 工作流和 GitHub Spec Kit 两套完整的开发流程。

## 为什么需要 Codex 配置？

之前 8 月底的时候 Claude Code 性能降级和限流严重，还喜欢自动脑补，很难让它严格遵循指令，故而我将日常所有的开发工作慢慢迁移到了 Codex 上。

迁移到 Codex 后，我发现每次都要重复配置模型、编写 Prompt 模板。有时候还想试试新出的国产模型，重复配置起来挺麻烦。为了解决这个问题，我把所有配置和 Prompt 模板整理到 GitHub 上，这样直接克隆下来就能用。默认配置用 LiteLLM 做网关，可以统一接入各种模型。

## Codex 配置包含什么？

### 1. 多模型支持

通过 LiteLLM 网关，能接入各种模型提供商。配置更新到 `~/.codex/config.toml` 文件即可：

![image-20251013190357972](/images/567e4222-127c-4bca-b15c-42aeb962f52f.png)

```toml
# 默认配置使用 LiteLLM + GitHub Copilot
model = "gpt-5"
model_provider = "github"
model_reasoning_summary = "detailed"
show_raw_agent_reasoning = true
model_verbosity = "medium"
approval_policy = "on-request"
model_reasoning_effort = "high"

[model_providers.github]
name     = "OpenAI"
base_url = "http://localhost:4000"
http_headers = { "Authorization"= "Bearer sk-dummy"}
wire_api = "chat"

# MCP Tools
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]

[mcp_servers.claude]
command = "claude"
args = ["mcp", "serve"]
```

还支持 ChatGPT、Azure OpenAI、OpenRouter、Kimi、ModelScope 等其他模型厂商，配置文件在 `configs` 目录中。切换配置只要覆盖对应的配置文件，比如：

```bash
cp ~/.codex/configs/chatgpt.toml ~/.codex/config.toml
```

### 2. 两套开发工作流

**GitHub Spec Kit 工作流**：GitHub 官方的规范驱动开发流程。

```bash
# 初始化项目
uvx --from git+https://github.com/github/spec-kit.git specify init .

# 然后按流程执行
/prompts:constitution # 创建项目原则
/prompts:specify      # 定义需求
/prompts:clarify      # 澄清细节
/prompts:plan         # 技术方案
/prompts:tasks        # 任务清单
/prompts:implement    # 执行实现
```

**Kiro 工作流**：从需求到代码的完整流程，和 Claude Code 里的类似。

```bash
/prompts:kiro-spec-creator 用户认证系统
/prompts:kiro-feature-designer 用户认证系统
/prompts:kiro-task-planner 用户认证系统
/prompts:kiro-task-executor 用户认证系统 实现登录接口
```

### 3. 实用 Prompt 模板

除了工作流，还有一些实用的 Prompt：

- `/prompts:github-issue-fixer 1234` - 修复 GitHub Issue 并创建 PR
- `/prompts:github-pr-reviewer 1234` - 审核 PR 并给出建议
- `/prompts:deep-reflector` - 会话总结和后续行动
- `/prompts:ui-engineer` - 前端开发和代码审查

如果你还想添加其他自定义 Prompt，可以把 Markdown 格式的提示词扔到 `prompts/` 目录，用 `$1` 到 `$9` 作为参数占位符：

```markdown
# prompts/my-prompt.md
请帮我实现 $1 功能，使用 $2 技术栈。

具体要求：
$ARGUMENTS
```

## 如何使用？

### 快速安装

![image-20251013190345983](/images/bc0444dc-f971-4eb9-a45d-819eca46f74f.png)

```bash
# 备份原有配置
mv ~/.codex ~/.codex.bak

# 克隆配置仓库
git clone https://github.com/feiskyer/codex-settings.git ~/.codex

# 安装 LiteLLM 和 Codex
pip install -U 'litellm[proxy]'
npm install -g @openai/codex
```

### 配置 LiteLLM

Github Repo 已经自带了 LiteLLM 配置，路径为 `~/.codex/litellm_config.yaml`，内容格式如下所示：

```yaml
general_settings:
  master_key: sk-dummy
litellm_settings:
  drop_params: true
model_list:
- model_name: "*"
  litellm_params:
    model: "github_copilot/*"
    extra_headers:
      editor-version: "vscode/1.104.3"
      editor-plugin-version: "copilot-chat/0.26.7"
      Copilot-Integration-Id: "vscode-chat"
      user-agent: "GitHubCopilotChat/0.26.7"
      x-github-api-version: "2025-04-01"
```

### 启动使用

```bash
# 启动 LiteLLM 代理
litellm --config ~/.codex/litellm_config.yaml

# 在另一个终端运行 Codex
codex
```

然后就能用了。如果要切换模型，比如用 ChatGPT：

```bash
cp ~/.codex/configs/chatgpt.toml ~/.codex/config.toml
codex
```

## 一些小坑和建议

当然，默认的 Codex 配置也有一些需要注意的地方：

1. **LiteLLM 要一直开着**：记得用 tmux 或 screen 在后台运行，不然 Codex 连不上。

2. **模型名称要对应**：LiteLLM 配置里的 `model_name` 要和 Codex 配置的 `model` 一致。

3. **gpt-5-codex 暂不支持**：GitHub Copilot 的 gpt-5-codex 模型需要 Responses API，但目前的代理只支持 Chat API（Azure OpenAI 是支持的）。

其实用下来发现，Codex 在几个场景下特别靠谱：

- **参考 A 实现 B**：需求明确的场景，Codex 会看懂已有代码，照样子写新代码，不会乱动其他地方。
- **新增测试用例**：看懂现有测试后补充新的测试用例，不多不少，正好是你想要的。
- **修小 bug 或实现小 feature**：比如 CSS 样式问题，Codex 改完 CSS 就收手，不会顺手“优化”其他代码。

还有就是，指令要清晰。遇到复杂需求，可以先跟 Codex 聊一会，把需求聊清楚了再开工，效果会好很多。

---

**相关资源：**

- 配置仓库：<https://github.com/feiskyer/codex-settings>
- Codex 官方文档：<https://developers.openai.com/codex/cli/>
- LiteLLM 文档：<https://docs.litellm.ai/>
- Claude Code 配置：<https://github.com/feiskyer/claude-code-settings>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
