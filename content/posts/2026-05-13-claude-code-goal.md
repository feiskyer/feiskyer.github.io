---
title: "Claude Code 也有 /goal 了，跟 Codex 的有什么不一样"
date: 2026-05-13T10:00:00+08:00
draft: false
tags: [Claude Code, /goal, Codex, Ralph Loop, AI Agent, 长时任务]
description: "Claude Code 新增 /goal 命令，靠一个独立小模型评估任务是否真的完成，从而实现无人值守跑长任务。本文详细拆解它的实现原理和 Stop hook 机制，并与 Ralph Loop、Codex /goal 做对比，附具体使用技巧和踩坑经验。"
---

上周写了一篇 [Codex /goal 上线后，我把 Ralph Loop 卸了](https://mp.weixin.qq.com/s/qwjxsGpMacLNy93g6dz4Aw)，顺带吐槽了 Claude Code + Ralph Loop 跑长任务各种不靠谱。没想到没过几天，Anthropic 就在新版 Claude Code 里把 `/goal` 命令抄过来了。官方推文直接说了，这就是 Claude Code 内置的 Ralph Loop（Ralph Loop 只是一个插件）。

用了几个场景，发现 /goal 确实比 Ralph Loop 好用不少，用起来也简单，一句 `/goal` 就能启动，终于不用盯着 Agent 干活了。今天就带你一起看下这个新功能以及它背后的工作原理。

## 使用方法

升级 Claude Code 到最新版本之后，`/goal` 后面跟一个完成条件，Claude Code 就会一直干到条件满足为止，比如：

```
/goal 所有 test/auth 目录下的测试通过,lint 也没有报错
```

跟普通对话的区别是，每轮结束后 Claude Code 不会停下来等你输入，而是自动开始下一轮。界面上会显示一个 `/goal active` 的状态条，标注运行时长。

具体的使用方法如下所示：

![Claude Code /goal 使用图解](/images/2026-05-13-claude-code-goal-goal-usage-guide-compressed.jpg)

其实可用的命令也就三个：

- `/goal <条件>`：设置目标，立即开始执行
- `/goal`：查看状态，包括条件、时长、轮次、token 用量
- `/goal clear`：取消当前目标（也可以用 stop、cancel、reset）

需要你注意的是，条件怎么写很关键。写得模糊，模型还是有可能会糊弄你。比如这样写：

```
/goal 给这个项目写完整的测试
```

“完整”没有定义，模型可以写几十个空壳测试，全部通过，然后宣布完成。所以建议你换成更具体的条件，比如：

```
/goal 给 src/auth/ 下所有函数写单元测试,要求:
1. 每个测试必须包含真实断言,不能只有空壳
2. 测试覆盖率达到 80% 以上
3. npm test 退出码为 0
4. 不修改 src/ 下的源代码
5. 20 轮后未完成则停止
```

最后，我还加了条轮次上限，这个也很有用，防止 Claude Code 无限跑下去。

如果由于各种原因，中途退出了（比如到了 5 小时上限），后面再开启时可以用 `--resume` 恢复目标继续执行。注意，你给它设置的条件最长支持 4000 个字符，可以写得很细了。

另外，还有两个比较好用的搭配：

第一个，`/goal` 跟 auto 模式搭配效果最好。auto 去掉每个工具调用的人工确认步骤，`/goal` 去掉每轮结束的等待，两个一起开就是完全无人值守。

第二个，在非交互模式开启，在自动化或者 SKILL 场景里面特别有用：

```bash
claude -p "/goal CHANGELOG.md 包含本周所有合并的 PR 记录"
```

## 实现原理

`/goal` 本质上是一个 session 级别的 prompt-based Stop hook。这一句话就把它跟 Ralph Loop 区分开了。

![Claude Code /goal 运行原理](/images/2026-05-13-claude-code-goal-goal-architecture-compressed.jpg)

你设置一个 `/goal` 条件后，Claude Code（Opus 或 Sonnet）正常工作，读文件、改代码、跑测试。每轮结束后，系统把完成条件和当前对话记录发给一个独立的小模型（默认是 Haiku）。这个模型返回 yes/no 和一条理由。如果 no，理由会注入下一轮对话，告诉 Claude 还差什么，然后自动开始下一轮。如果 yes，goal 标记为完成，记录到对话记录里。

关键是这个评估模型不能调用任何工具，它只能基于对话记录里已有的文字来判断。

评估的提示词很短，从 GitHub 上提取的系统提示词来看，核心逻辑是：

```
You are evaluating a stop-condition hook in Claude Code.
Read the conversation transcript carefully, then judge
whether the user-provided condition is satisfied.

Your response must be a JSON object with one of these shapes:
- {"ok": true, "reason": "<quote evidence from the
  transcript that satisfies the condition>"}
- {"ok": false, "reason": "<quote what is missing or
  what blocks the condition>"}

Always include a "reason" field, quoting specific text from
the transcript whenever possible. If the transcript does not
contain clear evidence that the condition is satisfied,
return {"ok": false, "reason": "insufficient evidence
in transcript"}
```

注意最后一条：找不到明确证据就默认返回证据不足。评估模型的默认立场是没做完，必须在对话记录里找到实锤才会放行。

不过实际用下来也是有不少问题的。评估模型只看对话文字，不能自己跑命令验证，所以如果工作模型在对话里写了“测试全通过”但实际没跑测试，评估模型看到的证据是充分的，自然会放行。想用好 `/goal`，条件里最好写明具体的验证命令，让 AI 没法绕过。

## 跟 Ralph Loop 比

Ralph Loop 的核心机制是 Stop hook 拦截：Claude 干完一轮尝试退出时，hook 检查是否达到完成条件，没达到就把原始 prompt 重新注入。完成判断靠精确字符串匹配，Claude 输出 `<promise>DONE</promise>` 就算完成。prompt 里反复强调“不要撒谎来退出循环”，但模型嘛，说不撒谎就不撒谎了？

跟 `/goal` 比，最关键的差距在完成判断。Ralph Loop 是模型自己说了算，输出一个标记就能退出，bash 脚本做字符串匹配放行，没有任何独立验证。`/goal` 换成了一个独立的小模型来评估，至少不是自己批改自己的试卷了。另外 Ralph Loop 每轮都会把原始 prompt 原封不动重新注入，跑多了上下文里堆满重复内容，虽然 Claude Code 的 compaction 还是会生效，但这些重复注入本身就是噪音。

顺便提一下，Claude Code 还有个 `/loop` 命令，按时间间隔触发下一轮（比如每 5 分钟跑一次），适合轮询类定时任务。`/goal` 是每轮结束后立即触发下一轮，适合连续执行的目标。

## 跟 Codex /goal 比

上篇文章里聊过，Codex `/goal` 的核心设计是三层：状态持久化（state-db）、权限控制（模型只能标记 complete，不能自行退出）、强制自审（`continuation.md` 要求拆检查清单，逐项对照真实文件和测试结果）。

Claude Code `/goal` 走了一条不同的路：不依赖工作模型的自查能力，而是引入独立的评估模型。

实际体验上两者差距明显。Codex 在目标执行和自审过程中可以通过工具来形成验证证据，grep 代码、跑测试、核对 spec，工作模型想造假成本很高。Claude Code 的评估模型只看对话文字，验证深度差一个量级，所以我自己跑下来还是 Codex 强得多（这也跟模型能力有关，Codex 搭配 GPT-5.5 才能达到最好的效果）。

## 写在最后

翻这几个方案的实现原理时，突然想到了最近一直在关注的 Agent harness 这个话题。你会发现不管是 Claude Code  /goal 的评估循环还是 Codex /goal 的权限控制，关键的约束都不是写在提示词里的，而是写在代码里的。Claude Code 用代码层面的 Stop hook 来驱动循环，Codex 的运行时每轮自动注入一段自审提示词，强制模型拆检查清单、逐项验证，模型不能自己选择要不要自审，代码替它做了强制自审。

CLAUDE.md 和 AGENTS.md 里写的规则模型可能忽略，但代码层面的 hook 100% 总会触发。这也是为什么 Agent harness 是必要的，光靠模型自觉是不够的，需要有人在外面用代码控制 AI 行为和边界。

回到 `/goal` 本身，对于验收条件清晰、按照 SPEC/PLAN 就能逐步完成的任务，它是目前最省心的选择。但要注意 token 消耗问题，`/goal` 模式下每轮都是完整的 Opus/Sonnet 调用，跑十几轮下来主模型的 token 用量轻松翻几倍（Haiku 评估的开销相对很小，主要成本还是多轮主模型调用）。建议在条件里加上轮次上限，保护好你的 token 账单。

---

相关链接：

- Claude Code /goal 官方文档：<https://code.claude.com/docs/en/goal>
- 上篇 Codex /goal 推荐：<https://mp.weixin.qq.com/s/qwjxsGpMacLNy93g6dz4Aw>
- Claude Code GitHub：<https://github.com/anthropics/claude-code>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![Feisky 公众号二维码](/images/mp.png)
