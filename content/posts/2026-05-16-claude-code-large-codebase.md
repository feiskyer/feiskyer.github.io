---
title: "Claude Code 在大型代码库里到底怎么用？Anthropic 给出了官方答案"
date: 2026-05-16T10:00:00+08:00
draft: false
tags: [Claude Code, Anthropic, 大型代码库, Harness, AI 编程]
description: "Anthropic 官方博客系统讲解在大型代码库里用好 Claude Code 的方法论：agentic search、CLAUDE.md 分层、Hooks、Skills、Plugins、LSP、MCP、Subagent 七件套，以及配置随模型升级瘦身与组织落地。"
---

> 题记：本文编译自 Anthropic 工程团队官方博客《How Claude Code Works in Large Codebases: Best Practices and Where to Start》，原文链接：<https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start>。本文在翻译基础上做了整理和补充。

Claude Code 在小项目里用着真挺丝滑的，基本上你碰到的问题它都能帮你解决。

不过一旦搬到大代码库，体验就开始打折扣。让它查找一个函数，grep 出来上千条匹配，你的上下文空间直接就被淹没了；改一个子服务，它非要跑全项目的测试用例，跑就跑吧还动不动超时偷懒，有时甚至自作聪明顺手改了一堆不该改的代码。

你在大型代码库里使用 Claude Code 是不是也碰到过这些问题？反正我是经常碰到。

前两天 Anthropic 工程团队发了一篇官方博客 How Claude Code Works in Large Codebases: Best Practices and Where to Start），系统讲解了大型代码仓库中用好 Claude Code 的方法论，推荐所有 Claude Code 用户都读一读。

下面是逐节的翻译，每一节我加上了自己的注解。

## 一、Claude Code 是怎么浏览代码的

Anthropic 博客一开头就讲了一个容易被忽略的事实：Claude Code 在大代码库里搜代码的方式，跟我们一直理解的 RAG 方式是完全不同的思路。

RAG 的做法是把整个代码库做 embedding，查询时检索相关片段。听起来挺合理的，但在大代码库里有个死结：embedding 流程追不上工程团队的提交速度。等你查询的时候，索引反映的是几天甚至几周前的代码，搜出来的可能是已经被重命名的函数，或者已经被删掉的模块。

Claude Code 走的是另一条路，叫 agentic search。它就像一个工程师那样找代码：遍历文件系统、读文件、grep 关键字、跟着 reference 跳转。所有动作都是实时的，不依赖任何索引。

这个差异不是技术孰优孰劣，而是适用场景不同。小到中型、变化没那么频繁的代码库，RAG 可能更快。但大代码库、活跃项目、频繁重构这些场景，agentic 是唯一靠谱的方式。

要用好 agentic search 也有它的前提：你的代码库得让 Claude Code 快速定位到具体的位置。如果目录命名混乱、没有 README、没有任何线索告诉它从哪开始看，再聪明的模型也得绕远路遍历大量无关文件，导致上下文空间被白白浪费。后面 Anthropic 讲的所有最佳实践，本质都是在解决这个问题。

## 二、harness 比模型更重要

Anthropic 在原文里给了一个清单，列出了塑造 Claude Code 能力的 harness 七件套：

- CLAUDE.md
- Hooks
- Skills
- Plugins
- LSP
- MCP servers
- Subagents

这七件套加起来，决定了同样的模型在你手里跑出来是什么效果。

我自己的体验跟这个清单完全一致。同样是 Claude Opus 4.6 模型，裸装 Claude Code 写代码，跟调好 CLAUDE.md 、装备 subagent 、配上 skills 之后相比，效果不是一个量级的。

这跟之前 Anthropic 在 Harness 设计那篇文章（《[为什么单 Agent 搞不定复杂应用](https://mp.weixin.qq.com/s/6AexM5_VngU1KDcYCU7gaA)》）里讲的逻辑是一致的：模型能力决定了天花板，harness 决定了你能走到天花板的多少。差的 harness 把模型能力浪费一大半都不夸张。

下面把这七件套一个一个聊聊。

## 三、CLAUDE.md：分层是最大的杠杆

CLAUDE.md 是每个会话启动时自动加载的上下文文件。Claude Code 会从当前目录往上一直走到根目录，把每一层的 CLAUDE.md 都读进来。

这个加载机制是叠加的，所以分层非常关键。Anthropic 给的原则是：根 CLAUDE.md 只放指针和关键注意事项。

Anthropic 还给了几条特实用的具体建议：

第一，给子目录创建 CLAUDE.md，而不是只是在根目录里。Claude 自动会往上走，所以你启动它的时候 cd 到任务相关的子目录，加载到的上下文最聚焦。

第二，lint 和 test 命令按子目录配置。改一个子服务却跑全项目的 test，是大代码库里最常见的浪费。耗时耗力不说，跑出来的输出信息还容易把 context 全淹了。子目录的 CLAUDE.md 应该写清楚“在这个目录下，跑测试用 X，跑 lint 用 Y”。

第三，用 `.ignore` 文件（ripgrep 的标准 ignore 格式）排除生成目录、build 产物、第三方代码这些噪音，同时把 `permissions.deny` 规则写到 `.claude/settings.json` 里。后者会跟着 git 一起 commit 出去，团队每个人都自动生效，不用各自配。如果某些开发者就是要碰生成目录，可以在自己的本地 settings 里覆盖项目级规则，不影响其他人。

第四，如果你的代码库就是没有传统目录结构，那写一个 codebase map：根目录放一个简短的 markdown 文件，列出顶层目录每个是干嘛的，一句话描述，给 Claude Code 一个目录索引。

这一节是整篇文章里最值得反复读的。CLAUDE.md 调好，其他六件套的价值才能放出来。

## 四、Hooks：让你的 setup 自我进化

Hooks 是绑定在事件上的脚本。Stop hook 在 session 结束时跑，Start hook 在开始时跑，另外还有 PreToolUse、PostToolUse 这些。

Anthropic 给了三个典型用法：

第一个是 Stop hook 可以让 Claude 自己回顾这个 session，分析有什么经验值得沉淀，然后主动提议更新 CLAUDE.md。这其实是把 self-improvement 自动化了，让其越用越聪明。

第二个是 Start hook 可以根据当前路径或者当前用户动态加载团队特定的上下文。比如你今天在前端目录，自动加载 UI 团队的约定；明天切到后端目录，自动换成后端的那一套。每个开发者就不用手动维护自己模块的 setup 了。

第三个是强制规则用 hook 而不是 prompt。比如自动跑 lint、提交前必须过 typecheck、危险命令拦截，这些都很适合。Prompt 是建议，hook 是约束，能用 hook 就别只写在 prompt 里。这点跟我自己的体感完全一样：让模型自觉其实远不如代码里拦住它来得靠谱。

在我看来，Hooks 是 Claude Code 里最被低估的扩展点，配置门槛比 skill 低，杀伤力却大。建议先把基础 hook 配上，再去考虑其他扩展。

## 五、Skills 和 Plugins：把好东西散播开

Skills 解决的是“专业能力按需出现”的问题。

大代码库里任务类型几十上百种，每个 session 都把所有能力塞进上下文是不现实的。Skills 用的是 progressive disclosure 的思路：能力描述常驻 context，具体内容只有用到才加载。这次 Anthropic 还提了一个进阶用法，skill 可以按路径 scope，只在特定子目录激活，避免无关 skill 互相打架。

说实话，写好一个 skill 门槛其实不低。Anthropic 之前专门写过一篇（《[写好一个 Skill 有多难](https://mp.weixin.qq.com/s/k_BmfjCByVE2HJz7nqtXRw)》），踩了几百个坑才总结出来一套规则。这次大代码库文档里强调的“按路径 scope”算是新增的进阶建议。

Plugins 解决的是“好配置散播开”的问题。

大代码库里最常见的一个现象是：少数几个老员工把 skill、hook、MCP 配置摸透了用得很爽，新人入职完全不知道有这些东西。这种 tribal knowledge 进不了生产力分布，对组织来说是很可惜的。

Plugin 把 skill、hook、MCP server 打包成一个安装包，新人一条命令装完就跟老员工同样的能力。我自己开源过两个仓库（[claude-code-settings](https://github.com/feiskyer/claude-code-settings) 和 [codex-settings](https://github.com/feiskyer/codex-settings)），初衷就是这个：把自己折腾出来的配置整理出来，让别人不用再走一遍弯路。

升级路径也是 plugin 的优势。所有人都装同一个 plugin，你修了一个 skill 的 bug，下一次更新所有人都拿到。靠口口相传根本做不到这种分发。

## 六、LSP：从 grep 到 symbol

这一段可能是文档里最技术、但也最实用的一节。

Claude Code 默认搜代码靠 grep。grep 在小代码库还行，到了大代码库就是个灾难：你搜一个 `getUser`，可能返回上千个匹配，分布在几百个文件里。Claude 为了搞清楚到底是哪个，得一个个打开看，context 瞬间被烧光。

LSP（Language Server Protocol）是编程 IDE 早就已经在用的东西。它知道你这个 `getUser` 是哪个 class 的方法、有哪些 reference、定义在哪、被谁调用。把 LSP 的能力转给 Claude Code，搜索就从字符串变成了符号。

实际效果差距可能是几十倍。同一个查询，grep 返回的是上千条文本匹配，LSP 返回的可能只有几条，并且每一条都是真正引用这个符号的位置。Claude 不用再去打开一堆无关文件，context 也省下来了。

这个适用前提是你的语言有靠谱的 LSP，对 Go、TypeScript、Java、Python、Rust 这些主流语言都没问题。脚本类语言可能稍微弱一些。

## 七、MCP 和 Subagent：扩展和隔离

MCP server 主要是让 Claude 接入它本来够不到的那些东西：内部工具、私有 API、文档系统等等。我之前在《[MCP 不只是开发工具](https://mp.weixin.qq.com/s/rLwm5v3IFRP7UcOarfqEZg)》里聊过生产级 MCP 怎么搭，这里就不展开了。

这次有个新的角度挺值得提：专门写一个 MCP server，把代码库的结构化搜索包装成 Claude 可以直接调用的工具。比如“查找所有 implements 这个 interface 的 class”、“查找所有调用这个 deprecated API 的地方”。这类查询用 grep 做不到，用 LSP 部分能做，但用专用 MCP 是最干净的。

Subagent 这个我想专门聊一下，因为是我用得最多的一个。

简单来说，Subagent 就是一个独立的 Claude Code 实例，有自己的 context window，接到任务、做完工作、只把最终结果返回给主 agent。

我用 Subagent 用得最多的场景就是 explore/edit 拆分。让一个 read-only 的 Explore subagent 先去摸目录、读文件、画出系统结构，写到一个文件里。主 agent 拿到这份报告，再带着完整图景去改代码。

为什么不让主 agent 自己 explore 自己 edit？因为 explore 阶段会读几十个文件，每个文件成百上千行，主 context 很快就被这些读取结果污染了。等到要写代码的时候，模型注意力已经分散在大量无关的细节上。

把 explore 隔离到 subagent 里，主 agent 只拿到一份精炼的总结，相当于拿到一张地图开始施工，而不是边挖边迷路。这跟之前讲上下文管理那篇文章（《[Claude Code 作者亲授：百万 token 上下文的正确用法](https://mp.weixin.qq.com/s/ihzAIlFQZCe7AlvjLQfeCw)》）里“Subagent 本质上是上下文管理工具”的说法完全一致。

## 八、配置随模型升级要瘦身

这是整篇文档里我觉得最容易被忽视的一节。

> 为旧模型写的指令，可能反过来限制新模型。

模型在不停升级。你为 Sonnet 4.5 写的 CLAUDE.md 提示、为修补当时模型缺陷加的 hook、为绕过当时上下文管理 bug 写的 skill，到了 Opus 4.7 可能不仅没用，反而成了限制。

我自己有个真实例子。早期我在根 CLAUDE.md 里加了一段“请先列出所有计划再执行”，那是因为当时模型容易跳步。等模型升级后，规划能力本来就有了，这条提示反而让 Claude 每次都先输出一段冗长的计划，效率反而降了。

Anthropic 的建议是每 3 到 6 个月，或者每次大版本发布后，专门 review 一次 harness 配置：哪些规则还有意义、哪些已经过时、哪些 hook 可以删、哪些 skill 可以合并。

这个习惯在传统工程里叫技术债清理，放到 harness 上同样适用。CLAUDE.md 跟代码注释一样会腐烂，你不主动清，它就慢慢变成噪音。

## 九、组织准备：DRI、agent manager、跨职能工作组

最后一节是组织层面的，大公司读者可能更关心。

Anthropic 观察到一个规律：Claude Code 推广最顺利的组织，都是在大规模铺开之前先做了一波基础设施建设。少数几个早期采用者负责把 plugin 库搭起来、把 MCP 接好、把 CLAUDE.md 模板写出来，然后才让全员上手。

新出现的一个角色叫 agent manager，是 PM + 工程师的混合角色，专门管理 Claude Code 生态。如果团队没这么奢侈，最起码也要有一个 DRI（Directly Responsible Individual），管 plugin marketplace、管 CLAUDE.md 约定、管 settings 决策。

问题是，光靠工程师自下而上的热情其实不够。热情会催生很多个人配置，但散乱、重复、互相冲突。这种时候需要有人来收口。

大公司还有一层是治理。安全、合规、代码审查流程要早立工作组。原文这点是比较国际化的语境，搬到中国团队还要再加上数据出境、审查留痕，以及敏感行业（金融、政务）的额外要求。这些事情早做比晚做要少很多痛苦。

哪怕你是个人开发者或者小团队，把配置维护这件事当成一个明确的责任分配下来，也比“大家都用一下吧”要有效得多。

## 写在最后

正如 Claude Code 一直在持续不停迭代一样，要用好 Claude Code 的 harness 配置也不是一次配好就一劳永逸的，也需要随着模型迭代一起进化。CLAUDE.md、Hooks、Skills、MCP、LSP、Subagent，每个配置存在的理由都要定期审视，不能因为它已经在那就让它一直在那。

我自己的实践顺序是这样的：所有项目第一步先创建 CLAUDE.md（包括核心子目录中的 CLAUDE.md），然后再根据需要在项目的 .claude 里面配置所需要的 Hook、MCP 和 Skills，然后就可以用 Claude Code 玩起来了。之后在根据实际需要调整优化，并提醒 Claude Code 把经常出错的地方存入它的 Memory。

---

相关资源：

- 原文：<https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start>
- Harness 设计前作：[为什么单 Agent 搞不定复杂应用](https://mp.weixin.qq.com/s/6AexM5_VngU1KDcYCU7gaA)
- 上下文管理：[Claude Code 作者亲授：百万 token 上下文的正确用法](https://mp.weixin.qq.com/s/ihzAIlFQZCe7AlvjLQfeCw)
- Skill 写作经验：[写好一个 Skill 有多难](https://mp.weixin.qq.com/s/k_BmfjCByVE2HJz7nqtXRw)
- 我的 Claude Code 配置：[feiskyer/claude-code-settings](https://github.com/feiskyer/claude-code-settings)
