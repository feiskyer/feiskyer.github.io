---
title: "Claude Skills 来了：给 AI 装上专业“技能包”"
date: 2025-10-17T19:00:00+08:00
draft: false
tags: [AI, Vibe Coding, Claude Code, MCP]
---

Anthropic 刚刚为 Claude 推出了 Skills 功能，通过文件夹形式打包指令、脚本和资源，让 Claude 在需要时自动加载专业能力。

Skills 具备**可组合、可移植、效率高、省 Token**四个核心特性。一次创建，就能在 Claude 应用、Claude Code 和 API 中通用。这个功能**改变了我们定制 AI 的方式**——从反复提供上下文，变成了打包一次、随时调用。

## 为什么需要 Skills？

之前每次让 Claude 处理 Excel 或者填 PDF 表单，都得把规则重新讲一遍。公司的品牌规范、表格格式、表单字段这些，每次对话都要重复。时间长了确实有点烦。

Skills 把这个问题解决了。你把这些规则和知识打包成文件夹，Claude 需要的时候自己去读。比如处理 PDF 时，它看到有个 PDF Skill，就会去加载表单填写的说明。

Rakuten 用 Skills 处理财务流程，原来要一天的活儿现在一小时搞定。多个表格处理、异常捕获、报告生成，全自动了。

## Skills 包含什么？

![一个 Skill 就是一个包含 SKILL.md 文件的目录](/images/5cf74d26-0496-4d8d-b9da-8a911098ae45.webp)

### 1. 核心文件 SKILL.md

最基础的就是 `SKILL.md` 这个文件，开头两行元数据：

```yaml
---
name: pdf
description: 处理和填写 PDF 表单
---
```

Claude 启动时会先扫这些名字和描述，粗略判断哪些可能用得上。Anthropic 叫这个设计"渐进式披露"——要用的时候再读完整内容，平时不占 Token。

### 2. 额外的参考文档

内容多了就拆文件。PDF Skill 拆成了三份：

- `SKILL.md`：核心说明
- `reference.md`：API 参考
- `forms.md`：表单填写指南

![SKILL.md 文件结构](/images/8af88f53-33e6-4aad-8676-ac5febfa619e.webp)

Claude 按需读取。遇到表单填写才会去翻 `forms.md`，不需要就放着。

![Skills 可以打包额外的参考文档](/images/5b83dd3c-48b2-464b-acd5-6e42ffed2a9e.webp)

### 3. 可执行代码

Skills 还能包含 Python 脚本等可执行代码。有些操作用代码执行比生成 token 更高效，也更可靠。

比如 PDF Skill 里有个预写好的 Python 脚本，用于提取 PDF 表单字段。Claude 可以直接运行这个脚本，而不需要把脚本内容或 PDF 文件加载到上下文中。

![Skills 可以包含可执行代码](/images/9f3dbf6b-5e3c-4fe9-bbb6-e52262684609.webp)

## 渐进式披露的工作原理

Skills 采用三级披露机制：

![渐进式披露的三个层级](/images/c60ecb4e-f10d-486c-929a-5f99c0ef61f9.webp)

1. **第一级**：启动时加载所有 Skill 的 `name` 和 `description`
2. **第二级**：任务相关时读取完整的 `SKILL.md`
3. **第三级**：按需读取额外的参考文档和资源

比如你发一条消息让 Claude 填写 PDF 表单，上下文窗口的变化是这样的：

![Skills 在上下文窗口中的触发流程](/images/ff220a1c-eae4-466a-833b-aadb15a891da.webp)

1. 初始状态包含系统提示词和所有 Skill 的元数据
2. Claude 触发 PDF Skill，读取 `pdf/SKILL.md`
3. Claude 继续读取 `forms.md` 文件
4. 加载完必要信息后开始处理任务

## 如何使用 Skills？

### 在 Claude 应用中使用

Skills 功能面向 Pro、Max、Team 和 Enterprise 用户开放。打开设置页面就能启用 Skills 功能。

![Claude.ai 中的 Skills 管理界面](/images/012ae8b6-9d01-4985-ae80-d4b581c217bf.webp)

Claude 会根据任务自动触发相关 Skill，你甚至能在思维链中看到 Claude 正在使用哪个 Skill。

创建自定义 Skill 也很简单。通过内置的 "skill-creator" Skill，Claude 会问你一些问题，然后自动生成文件夹结构、编写 `SKILL.md` 文件、打包需要的资源。

### 在 API 中使用

通过新增的 `/v1/skills` 端点，开发者可以管理自定义 Skill 的版本。Skills 需要配合代码执行工具（Code Execution Tool）的 beta 版使用。

Anthropic 提供了一些官方 Skill，比如处理 Excel、PowerPoint、Word、PDF 等。开发者也可以创建自己的 Skill 来扩展 Claude 的能力。

### 在 Claude Code 中使用

在 Claude Code 里安装 Skills 很方便，通过插件市场就能安装：

```bash
# 从官方市场安装
/plugin marketplace add anthropics/skills

# 安装具体的 Skill
/plugin install pdf
```

或者手动把 Skill 文件夹复制到 `~/.claude/skills` 目录。Claude 会在相关任务时自动加载。

## 几个小建议

测试 Skills 时发现几个需要注意的地方：

1. **从评估开始**：先运行 Claude 完成一些任务，观察哪里需要额外上下文，再针对性地创建 Skills
2. **注意文件拆分**：当 `SKILL.md` 内容太多时，把互斥的上下文拆到不同文件，能减少 token 消耗
3. **重视元数据**：`name` 和 `description` 决定了 Claude 会不会触发这个 Skill，要写得准确清晰
4. **迭代很重要**：观察 Claude 如何使用你的 Skill，根据实际情况调整。可以让 Claude 帮你总结成功经验和常见错误

还有就是，Skills 会给 Claude 执行代码的能力，所以确保只安装可信来源的 Skills。如果是第三方 Skill，使用前最好先检查一下代码和依赖。

---

**相关资源：**

- Claude 应用用户指南：<https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills>
- API 开发文档：<https://docs.claude.com/en/api/skills-guide>
- Claude Code 文档：<https://docs.claude.com/en/docs/claude-code/skills>
- 官方示例 Skills：<https://github.com/anthropics/skills>
- Skills Cookbook：<https://github.com/anthropics/claude-cookbooks/tree/main/skills>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
