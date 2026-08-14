---
title: "OpenAI承认Chat API是周末草台班子产品，是时候切换到 Responses API了"
date: 2025-09-29T20:20:28+08:00
draft: false
tags: [AI, Vibe Coding, Codex, OpenAI]
description: "OpenAI 承认 Chat Completions API 是仓促赶出的草台产品，推出全新 Responses API 作为下一代方案，原生支持推理状态保持与多模态交互，缓存利用率提升 40-80%，本文详解其设计动机、技术优势与迁移要点。"
---

刚刚，OpenAI 在最新发布的《Why we built the Responses API》 中承认，作为 AI 界 API 事实标准的 Chat Completions API 就是一个周末快速赶出来的草台产品，存在着各种各样的限制。所以，作为 Chat Completions API 的下一代演进方案，OpenAI 在 2025 年 3 月发布了全新的 Responses API（`/v1/responses`） 。根据官方基准测试，它在缓存利用率方面可以提升 40-80%，而在 TAUBench 评测（Benchmark for Tool-Agent-User Interaction in Real-World Domains）中性能提升 5%，并原生支持推理状态保持和多模态交互。

## 为什么需要 Responses API？

作为一个草台产品，Chat Completions API 存在诸多技术限制，包括：

- **状态管理开销**：每次请求需要重新传输完整对话历史，导致 token 消耗呈线性增长。
- **推理链断裂**：模型的 Chain-of-Thought（CoT）在请求间无法保持，影响多步推理任务的连贯性。
- **多模态集成不足**：文本、图像、音频等模态需要通过额外的适配层处理。
- **工具调用效率低**：Function calling 需要客户端往返处理，增加延迟和复杂度。

而 Responses API 最大的改进是引入状态管理，不用每次都传完整历史了。说白了就是服务端帮你存着之前的对话，你只管传新消息就行。多模态这块也整合得不错，图片音频文本一把梭，不用各种转换了。

此外，还有两个非常强大的功能是：1）推理保持——模型的思考过程可以持续，不会每次都“失忆”；2）工具调用直接在服务端运行，大大减少了网络往返时间。

## 如何使用 Responses API

OpenAI SDK 已经提供了 Responses API 的完整支持，使用起来非常方便。比如，一个最简单的例子是：

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

而在需要维持状态的会话中，只需要在新的 API 调用中传入上次的 `response.id` 和新的消息即可，无需再像 Chat Completion 那样传入历史消息：

```python

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="tell me a joke",
)
print(response.output_text)

second_response = client.responses.create(
    model="gpt-4o-mini",
    previous_response_id=response.id,
    input=[{"role": "user", "content": "explain why this is funny."}],
)
print(second_response.output_text)
```

## 如何迁移遗留代码

对于遗留代码，你可以参考 Responses API，手动修改 OpenAI  API 的调用。对于很多 AI 应用来说，这个步骤可能并不轻松，这儿有两个推荐的迁移方法：

* 第一，可以把 Responses API 的文档发给 Codex、Claude Code 这类 AI 编程工具，让 AI 帮你完成迁移，并修改或添加相关测试；
* 第二，使用 OpenAI 开源的 [OpenAI Completions → Responses Migration Pack](https://github.com/openai/completions-responses-migration-pack)，让它帮你调起 Codex 来做迁移：

```sh
git clone https://github.com/openai/completions-responses-migration-pack
cd completions-responses-migration-pack

bash scripts/completions-to-responses-upgrade.sh --repo /path/to/repo --no-interactive
```

> 如果你使用 Codex 作为日常开发工具，OpenAI Completions → Responses Migration Pack 也是一个很好的参考资料，其他类似的遗留代码迁移问题其实都可以通过类似方法实现。

## 写在最后

看看 OpenAI 这几年的 API 演进，真是一部血泪史：

| API 版本 | 发布时期 | 核心特性 | 真实情况 |
|---------|---------|---------|----------|
| Completions | 2020.6 | 文本补全 | 最简单但挺稳定 |
| Chat Completions | 2023.3 | 对话接口 | 周末草台产品，但撑起了 ChatGPT |
| Assistants (Beta) | 2023.11 | Agent 框架 | 太贵太慢，2026年8月要废弃了 |
| Responses | 2025.3 | 推理保持 | 终于像个正经产品了 |

随着推理模型成为主流，新的 Responses API 显然就是为了推理模型而设计。再加上新兴的 Agent 所必须的状态维护和工具调用，是时候迁移到更稳定可靠的 Responses API 了。

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
