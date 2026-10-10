---
title: "GitHub Spec Kit 把规范驱动开发标准化了，AI 编程终于有章法了"
date: 2025-09-29T22:20:28+08:00
draft: false
tags: [AI, Vibe Coding, Codex, Claude Code]
description: "介绍 GitHub 拥有 27k 星标的 Spec Kit，它通过 Constitution、Specify、Plan、Tasks、Implement 等标准化步骤把规范驱动开发标准化，解决 AI 编程凭运气、代码偏离意图的 vibe-coding 危机。"
---

你在用 AI 编程时，是否遇到过这样的情况？你向 Claude Code 提出需求后，它生成了一大段代码，虽然能编译通过，功能也基本实现了，但总有很多细节不尽如人意——架构设计不是你想要的，界面风格也总是差点意思。经过几轮迭代，项目代码变得越来越臃肿，甚至让你失去了阅读和维护的兴趣。

GitHub 显然已经注意到这个问题。拥有 27k 星标的 Spec Kit 正是他们提出的解决方案：将规范驱动开发彻底标准化，让 AI 编程不再“碰运气”，而是有章可循。通过 Constitution、Specify、Plan、Tasks、Implement 等标准化步骤，Spec Kit 将“人的经验”转化为“机器可执行的规范”，确保 AI 生成的代码既满足业务需求，又符合工程标准。

## GitHub 为什么要做 Spec Kit？

随着 AI 编程工具的普及，GitHub 发现了一个严重的问题：“**vibe-coding 危机**”。你描述了需求，AI 生成了一堆看似正确的代码，但总有些地方不对劲。有时代码无法编译，有时只解决了部分问题，完全偏离了你的真实意图，有时选用的技术栈也不是你想要的。

发生这个根本问题不在 AI 的编码能力，而在我们的使用方式：

1. vibe-coding 带有很强的随机性：一个模糊的提示如“给我的应用添加照片分享功能”，会强迫 AI 去猜测你的详细需求。AI 会做出合理的假设，但其中一些必然是错误的——而你往往要到深度开发时才发现哪些地方不对。

2. 意图传达的失败：我们经常把 AI 当搜索引擎使用，期望它能“理解”我们的真实需求。但大语言模型虽然在模式完成方面表现出色，却不能读心。缺乏清晰的规范，AI 只能基于常见模式生成通用解决方案。

3. 无法应对复杂系统：在已有代码库中添加功能尤其困难。没有明确的架构约束和集成要求，AI 生成的代码往往像“外挂”一样附加在系统上，而不是原生的组成部分。

4. 质量标准缺失：大多数团队的安全策略、合规规则、设计系统约束要么存在某人脑子里，要么埋在没人看的 wiki 中，要么散落在无法搜索的 Slack 对话里。AI 无法获取这些关键信息。

针对这些问题，GitHub 提出的解决方案是将规范变为可执行的活文档。当规范能够自动转化为可运行的代码时，它就决定了最终的构建内容。Spec Kit 的核心理念是：**将稳定的“what”（做什么）与灵活的“how”（怎么做）分离**，让意图成为事实的源头，而不是仅依赖于代码。

## Spec Kit 是什么？

Spec Kit 的核心工作原理是**让规范成为工程流程的中心**。不是写完规范就扔一边，而是让规范驱动实现、检查清单和任务分解。你的主要角色是“导演”，而 AI 负责“编剧”。

Spec Kit 的工作流程分为四个阶段，每个阶段都有明确的检查点：

1. **Specify 阶段**：你提供高层次的需求描述，AI 生成详细的规范。此阶段关注“做什么”和“为什么”，不涉及具体技术栈。

2. **Plan 阶段**：你提供技术方向和约束条件，AI 制定全面的技术实现方案。

3. **Tasks 阶段**：AI 将规范和方案细化为可操作的小任务，每个任务都能独立实现和测试。

4. **Implement 阶段**：AI 逐步完成各项任务，你只需审查每次聚焦的变更，而不是一次性查看大量代码。

这里需要注意的是，每个阶段都有特定职责，只有当前阶段完全验证后才能进入下个阶段。

在这四个必须的工作流程之外，Spec Kit 还加入了一些补充可选的阶段，让你可以更好帮助 AI 完成你的意图：

5. **Constitution 阶段**：放在 Specify 之前，建立项目的管理原则和开发指导方针，指导所有后续的开发工作。
6. **Clarify 阶段**：放在 Plan 阶段之后，澄清规范中不够明确的需求，避免或减少后续工作返工。
7. **Analyze 阶段**：放在 Taks 阶段之后，分析任务一致性和覆盖度，确保整个项目的实现质量。

Spec Kit 将这些阶段都转换成了 / 命令，并在每个阶段执行结束后自动提醒你接下来的步骤，所以你并不需要严格记住这些阶段的顺序。

## Spec Kit 环境搭建

首先是安装 Spec Kit，GitHub 推荐用 uv 来装：

```bash
# 持久化安装（推荐）
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 一次性使用
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

推荐使用持久化安装，后续在多个项目中使用时也会更方便。

安装完成后，接下来是初始化项目：

```bash
# 创建新项目
specify init my-taskify-app --ai claude

# 也支持已有项目
cd <project-path>
specify init . --ai claude
```

这一步会让你选择 AI agent，支持 Claude Code、GitHub Copilot、Cursor、Gemini CLI 等等。我这儿直接选的 Claude Code：

![](/images/20251127092009.png)

接下来，它还会提醒你选择脚本类型，Linux/WSL 选择 sh，Windows 选择 PowerShell。选择之后，Spec Kit 会创建相关的 / 命令，并指导你接下来的使用流程：

![](/images/20251127092041.png)

以 Linux 为例，初始化完成后，Spec Kit 会创建下面这些新的文件：

![](/images/2025112709999.png)

可以看到，Spec Kit 创建了一系列的 / 命令、脚本以及模版。这些命令的作用是什么呢？接下来再来看看每个命令的具体工作原理。

## Spec Kit 工作原理

### 1. Constitution：建立项目原则

第一步是用 `/constitution` 命令建立项目的管理原则和开发指导方针，这些原则将指导所有后续的开发工作。

使用示例：

```md
/constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

这个命令实际上是处理一个 **模板填充系统**。它会：

1. **加载 constitution 模板**：读取 `.specify/memory/constitution.md` 中的模板；
2. **识别占位符**：找到所有 `[ALL_CAPS_IDENTIFIER]` 格式的占位符，如 `[PROJECT_NAME]`、`[PRINCIPLE_1_NAME]` 等；
3. **收集具体值**：从用户输入、已有仓库上下文、或推断中获取占位符的实际值；
4. **版本控制**：按语义版本规则自动更新 `CONSTITUTION_VERSION`（MAJOR、MINOR、PATCH）；
5. **一致性传播**：检查并更新所有相关模板文件，确保新原则在整个工具链中生效；
6. **生成同步报告**：在文件顶部添加 HTML 注释，记录修改历史和影响的模板。

**关键设计**：Constitution 不只是一个文档，它是整个工具链的“基本法则”，所有后续命令都必须严格遵守这里定义的原则。比如你在这里定义了“必须使用 TypeScript”，那么后续的 plan 和 tasks 都会自动遵循这个约束。

### 2. Specify：创建项目规范

接下来是 `/specify` 命令，用来描述你要构建什么以及为什么要构建。重点关注用户体验需求，即“做什么”和“为什么”，不涉及具体技术栈。

使用示例：

```md
/specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

这个命令背后的工作机制是：

1. **运行分支创建脚本**：执行 `.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS"`，创建新的 feature 分支并返回 JSON 格式的分支名和规范文件路径；
2. **加载规范模板**：读取 `.specify/templates/spec-template.md` 了解必需的章节结构；
3. **智能内容生成**：将你的自然语言描述转换为结构化规范，替换模板中的占位符但保持顺序和标题；
4. **规范文件写入**：在新分支的指定路径创建完整的 spec.md 文件。

**关键设计**：整个过程只需要运行一次创建脚本。脚本会自动处理 Git 分支切换和文件初始化，然后 AI 在此基础上填充具体内容。

### 3. Clarify：需求澄清

在 plan 阶段之前，还有一个重要的可选步骤是 `/clarify` 命令，用于澄清规范中不够明确的地方。这是在创建技术计划之前的结构化澄清工作流，避免或减少下游的返工。

使用示例：

```md
/clarify
```

这个命令实现了一个 **结构化澄清系统**：

1. **前置检查**：运行 `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` 获取 feature 目录和规范文件路径；
2. **多维度覆盖扫描**：对规范进行系统性的模糊性和覆盖度扫描，涵盖功能范围、数据模型、交互、质量、集成依赖等共计 10 个分类。

3. **智能问题生成**：生成最多 5 个高优先级澄清问题，每个问题都满足下面的条件：
   - 可以通过多选题（2-5 个选项）或短答案（≤5 词）回答；
   - 对架构、数据建模、任务分解等有实质影响；
   - 能显著降低下游返工风险。

4. **交互式问答循环**：一次只问一个问题，获得答案后立即更新规范文件；
5. **增量规范更新**：每个答案都会实时写入规范的相应章节，并在 `## Clarifications` 部分记录。

**关键设计**：最多问 5 个问题，确保澄清过程高效且聚焦。如果你想跳过澄清步骤，需要明确说明，否则后续 plan 命令会检查并要求先运行 clarify。

### 4. Plan：创建技术实现计划

现在进入 `/plan` 阶段。这个阶段你需要提供希望的技术栈、架构和约束条件，AI 会生成全面的技术实现计划。

使用示例：

```md
/plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

这个命令背后会：

1. **环境准备**：运行 `.specify/scripts/bash/setup-plan.sh --json` 获取必要的文件路径；
2. **前置验证**：检查 feature 规范文件中是否存在 `## Clarifications` 章节，如果缺失且存在明显模糊区域，会暂停并要求先运行 `/clarify；`
3. **需求约束分析**：解析 feature 规范中的需求、用户故事、验收标准，读取 constitution 了解原则约束，再分析技术约束和依赖关系；

4. **模板执行**：加载 `.specify/templates/plan-template.md` 并执行其中定义的流程；
5. **分阶段产出**：在指定目录生成多个设计文档：
   - **Phase 0**: `research.md`（技术调研）；
   - **Phase 1**: `data-model.md`、`contracts/` 目录、`quickstart.md`；
   - **Phase 2**: `tasks.md`（任务分解）。

6. **进度跟踪**：实时更新 Progress Tracking 确保所有阶段完成。

**关键设计**：通过可执行的设计模板，规定 AI 严格按照模板中的步骤执行，确保输出的计划具有一致的质量和结构。如果你让 AI 访问其他内部文档，它也可以直接将你的架构模式和标准整合到计划中。

### 5. Tasks：任务分解

用 `/tasks` 命令让 AI 将规范和计划分解为实际的工作任务：

使用示例：

```md
/tasks
```

这个命令实现了 **智能任务分解系统**：

1. **文档分析**：读取所有可用的设计文档：
   - `plan.md`（技术栈和库选择）
   - `data-model.md`（数据实体，如果存在）
   - `contracts/`（API 端点，如果存在）
   - `research.md`（技术决策，如果存在）
   - `quickstart.md`（测试场景，如果存在）

2. **任务生成规则**：
   - **Setup 任务**：项目初始化、依赖管理、代码规范配置；
   - **Test 任务 [P]**：每个 contract 一个测试，每个集成场景一个测试（可并行）；
   - **Core 任务**：每个实体、服务、CLI 命令、端点一个任务；
   - **Integration 任务**：数据库连接、中间件、日志记录；
   - **Polish 任务 [P]**：单元测试、性能优化、文档（可并行）。

3. **依赖关系映射**：
   - 不同文件的任务标记为 `[P]`（可并行）；
   - 同一文件的任务必须串行执行；
   - 严格的依赖顺序：Setup → Tests → Models → Services → Endpoints → Core → Integration → Polish。

4. **TDD 集成**：每个 implementation 任务前都会有对应的 test 任务；

5. **输出格式**：生成编号任务（T001, T002 等），包含具体文件路径、依赖说明、并行执行指南。

**关键设计**：生成的 tasks.md 必须 **立即可执行** —— 每个任务都具体到 LLM 无需额外上下文就能完成。

### 6. Analyze：一致性检查

在 tasks 生成之后、implement 之前，还可以使用 `/analyze` 命令进行跨文档的一致性和覆盖度分析。

使用示例：

```
/analyze
```

这是一个 **非破坏性的质量保证系统**：

1. **文档解析**：分析 `spec.md`、`plan.md`、`tasks.md`，构建语义模型；
2. **多维度检测**：
   - **重复检测**：识别近似重复的需求，标记低质量表述；
   - **模糊性检测**：标记含糊形容词（"快速"、"可扩展"、"安全"）缺乏量化标准；
   - **规格不足**：需求缺失可测量结果、任务引用未定义组件；
   - **Constitution 对齐**：检查任何与 MUST 原则冲突的需求或计划；
   - **覆盖度差距**：零任务覆盖的需求、无需求映射的任务；
   - **不一致性**：术语漂移、数据实体引用冲突、任务顺序矛盾。

3. **严重性分级**：CRITICAL/HIGH/MEDIUM/LOW 等；

4. **结构化报告**：生成包含问题 ID、分类、严重性、位置、建议的 Markdown 表格；
5. **行动建议**：基于发现的问题提供具体的修复命令建议。

**关键设计**：严格只读模式，绝不修改文件。如果发现 CRITICAL 问题，建议在 implement 之前解决，从而确保项目质量。

### 7. Implement：根据计划执行所有任务

有了完整的规范和任务清单，接下来就是用 `/implement` 命令让 AI 执行实际开发。

使用示例：

```
/implement
```

这个命令严格按照设计执行所有任务：

1. **全面前置检查**：运行 `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` 确保所有必需文档存在

2. **上下文加载**：
   - **必需文档**：`tasks.md`（任务列表）、`plan.md`（技术架构）
   - **可选文档**：`data-model.md`、`contracts/`、`research.md`、`quickstart.md`

3. **任务编排解析**：
   - 提取任务阶段（Setup、Tests、Core、Integration、Polish）
   - 识别依赖关系（串行 vs 并行 `[P]` 标记）
   - 理解文件级协调（同文件任务必须串行）

4. **分阶段执行**：
   - **严格 TDD**：测试任务在对应实现任务之前执行
   - **依赖尊重**：串行任务按序执行，并行任务可同时运行
   - **文件级同步**：影响同一文件的任务串行化
   - **阶段验证**：每个阶段完成前进行检查点验证

5. **进度跟踪和错误处理**：
   - 每完成一个任务就在 tasks.md 中标记为 `[X]`
   - 非并行任务失败时停止执行
   - 并行任务失败时继续其他成功任务，报告失败任务
   - 提供具体错误上下文用于调试

6. **完成验证**：
   - 验证所有必需任务完成
   - 检查实现功能与原始规范匹配
   - 确认测试通过和覆盖率要求
   - 生成最终状态报告

**关键设计**：严格遵循设计规范和任务清单，确保 AI 按照预定义的约束开发任务。

## 最佳实践

根据 GitHub 官方资料和我的实际测试，Spec Kit 在以下三种核心场景下表现尤为出色：

1. **Greenfield 项目（从 0 到 1）**：启动新项目时，许多人会直接进入编码阶段。但花一些时间制定规范和计划，可以确保 AI 构建的正是你真正需要的系统。这有助于避免因早期架构决策失误而导致的后期重构成本。

2. **现有系统功能开发（从 N 到 N+1）**：这是规范驱动开发最具优势的场景。在复杂的现有代码库中添加新功能往往很困难。通过为新功能制定规范，可以明确其与现有系统的交互方式。在计划阶段设定架构约束，能够确保新代码与原有项目风格一致，而不是简单的外挂模块。

3. **遗留系统现代化**：重构遗留系统时，原有设计意图常常难以追溯。借助 Spec Kit 的规范驱动开发流程，可以用现代规范梳理关键业务逻辑，在计划阶段设计全新架构，然后让 AI 从零重建系统，避免继承原有的技术债务。

当然，Spec Kit 也并非适用于所有场景，比如：

1. **快速原型验证**：如果只是想快速验证一个想法，完整的规范流程可能显得过于繁琐。

2. **高度创新性探索**：当需求尚不明确、需要大量探索时，标准化流程可能会限制创新空间。

3. **个人小型工具项目**：对于个人开发的简单工具类项目，流程带来的开销可能大于实际收益。

以上就是今天的内容，欢迎留言分享你的 vibe coding 实践经验！

更多信息可以查看其 Github 项目 <https://github.com/github/spec-kit>。
