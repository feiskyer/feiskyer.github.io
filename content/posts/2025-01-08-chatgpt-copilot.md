---
title: "推荐一款 VSCode AI 插件 —— Chatgpt Copilot"
date: 2025-01-08T20:30:51+08:00
tags: [AI, Copilot]
draft: false
---

今天我想和大家分享一个 **ChatGPT Copilot** VSCode 插件。这是一款完全开源的 AI 助手, 目前在 VSCode 市场的下载量已突破 400k。它的核心功能非常简洁 - 在 VSCode 侧边栏中提供了一个灵活的类 ChatGPT 聊天工具。它不仅支持接入各种主流 AI 模型, 还允许用户在对话中添加文件和图片等聊天上下文。

## 开发背景

作为 Github Copilot 资深用户，其实在开发过程中用的最多的还是 Github Copilot，它在大部分编程任务中已经可以大致满足要求。然而, 它也存在一些局限性:

* 仅适用于编程任务
* 无法切换 AI 模型
* 不支持修改系统提示 (system prompt)
* 经常响应速度慢

在 VSCode 插件市场上, 虽然有不少 AI 插件可供选择, 但它们要么收费, 要么存在数据泄露风险。所以也就有了这么一个完全开源、并且不收集任何用户数据的插件。尤其是使用本地大模型时，不会把任何数据发送到互联网。

## 核心特性

<div align=center>
 <img src="/assets/image-20250109215246111.png"/>
</div>

1. **AI 模型支持**: 支持 OpenAI、Claude、Gemini、Ollama、Azure 以及各类 OpenAI 兼容的大模型。

2. **智能聊天**: 提供类似 ChatGPT 的对话功能, 并支持通过 `@` 符号将文本、代码或图片添加到对话上下文中。

3. **自定义系统提示**: 允许用户自定义 System Prompt, 并可通过 `#` 符号在对话中随时切换不同的系统提示。

4. **代码辅助功能**: 提供基本的代码编辑和协助功能。用户可以选中代码, 然后通过右键菜单或快捷键进行代码解释、错误修复、单元测试生成等操作。

## 快速上手

想要体验 ChatGPT Copilot? 只需几个简单步骤:

<div align=center>
 <img src="/assets/image-20250109215343918.png"/>
</div>

1. 在 VSCode 扩展市场搜索 "ChatGPT Copilot"，认准上面的 LOGO。
2. 安装完成后, 在侧边栏打开聊天窗口。
3. 点击 "Update settings" 配置你的 API key。
4. 返回聊天窗口, 开始你的 AI 辅助编程之旅!



## 项目开源

插件是完全开源的，项目地址 <https://github.com/feiskyer/chatgpt-copilot>，欢迎大家 star、fork 和贡献代码！
