---
name: sync-notes-to-blog
description: 把 ~/notes/history 里的新文章同步到本 Hugo 博客。用户说「同步 notes」「同步公众号文章到博客」「把 notes 里的新文章搬过来」「sync notes」时使用。负责复制正文、清理公众号元数据与运营标签、本地化图片、套用博客标准结尾，再由 agent 补 description 与题记。
---

# 同步 notes/history 到博客

`~/notes/history` 是公众号原稿库。本 skill 把其中**尚未同步**的文章搬进 `content/posts/`，
按博客 AGENTS.md 的格式要求加工，可重复运行：跑过一次之后，只处理新增的文章。

## 分工：脚本做机械变换，你做语义判断

脚本 `scripts/sync_notes_to_blog.py` 只做**可判定的机械变换**，剩下需要理解文意的部分留给你。
不要用脚本硬猜 description，也不要手工做脚本已经做掉的事。

### 脚本负责（已验证）

| 项 | 行为 |
|---|---|
| 候选识别 | 对比 `content/posts` 已有文件名（NFC 归一化），只处理新增；`--reprocess` 可重跑加工不完整的旧文章 |
| frontmatter 重建 | 保留 title/date/draft/tags/description + 未识别的自定义键；**删除** `mp_url`、`stats`、`format`、`source` |
| title 补全 | frontmatter 无 title 时，用正文首个 H1 回填（H1 的中英空格排版比文件名 slug 好） |
| date 规范化 | 补齐成 `YYYY-MM-DDT10:00:00+08:00`；同日多篇按序递增分钟，保证排序稳定 |
| tags 清理 | 删 `爆款`/`超爆款`/`小绿书`/`10万+`/`十万+` 等运营标签；规范化大小写（`kubernetes` → `Kubernetes`）；同时支持 inline 与 block 两种 YAML 写法 |
| 正文首个 H1 | 删除（Hugo 模板已渲染 title，留着就是双 H1） |
| 封面图 | 删除正文开头 alt/文件名含 `cover`/`封面` 的图 |
| 话题标签行 | 删除文末 `#Codex #MCP #AI编程` 这类整行标签（**不会**误删 `##` 小节标题） |
| 公众号引导语 | 删除文末 CTA 段落（含「好了今天就聊到这儿…关注 Feisky」「如果觉得有帮助…」等变体），**保留**「相关资源」列表 |
| 图片本地化 | 本地图片复制、远程图片下载到 `static/images/`，重命名为 `<文章slug>-<原名>.<ext>`（纯 ASCII 无空格），引用改写为 `/images/xxx` |
| 标准结尾 | 追加或替换为博客统一结尾（分隔线 + 引导语 + `![Feisky 公众号二维码](/images/mp.png)`），保证全文只有一份 |
| 排版 | 裸 URL 转 autolink、中英文间距规范化，**只作用于非代码区**，代码块与行内代码零改动 |
| 落盘校验 | 写入后逐条检查 `/images/` 引用是否真在磁盘上，有缺失则非零退出 |

### 你负责（脚本会在报告里逐篇列出）

1. **生成 `description`**：120-160 字符，含关键词，面向搜索结果的一句话概括。**这是最主要的人工项**，一般每篇都要补。
2. **补 `tags`**：少数源文没有 tags，脚本会标「缺少 tags，需要 agent 补」。参考同类已有文章的标签体系，3-5 个。
3. **写题记**：脚本删掉 `source:` 字段时会把原文 URL 打印出来。编译/翻译类文章按博客惯例在开头加题记，注明原文出处、作者，并说明「在翻译基础上做了整理和补充」。
4. **补图片 alt**：脚本保留原有 alt，但源文常常是空的，报告会给出空 alt 数量。改成描述性文字。
5. **破折号**：源文若含「——」，脚本会警告但**不自动改**（改写是语义操作）。必须手工换成逗号、句号或括号。这是硬约束，见下。

## 用法

```bash
python3 .Codex/skills/sync-notes-to-blog/scripts/sync_notes_to_blog.py --list
```

标准流程：

1. `--list` 看有多少待同步。
2. `--dry-run` 预演，确认没有异常报告。
3. 去掉 `--dry-run` 真实同步。文章多时用 `--batch 10` 分批，每批同步完立刻做上面的人工项，再跑下一批。一次性灌 40 篇再回头补 description，上下文会不够用。
4. 按报告逐篇补 description / tags / 题记 / alt。
5. `hugo` 构建验证，`git diff --stat` 复核。

常用参数：

| 参数 | 用途 |
|---|---|
| `--list` | 只列候选，不改任何文件 |
| `--dry-run` | 全流程预演，不落盘（图片也不复制） |
| `--only <文件名>` | 只处理指定文章，可重复传 |
| `--batch N` | 本次最多处理 N 篇 |
| `--reprocess` | 重新加工「已存在但没加工完」的文章（残留 mp_url、缺结尾等） |
| `--include-drafts` | 连 `draft: true` 的一起同步（默认跳过并在报告里列出） |
| `--notes-dir` / `--blog-root` | 改源目录 / 博客根目录，默认 `~/notes/history` 与当前目录 |

状态记录在 `.Codex/skills/sync-notes-to-blog/state.json`，但**候选判定以 `content/posts` 的实际文件为准**，
删掉 state.json 不会导致重复同步。

## 硬约束

- **禁止破折号**：不得在任何中文文本里引入「——」或「—」，包括你生成的 description。写入前先 `grep -n '——\|—'` 自查。
- **不改 config.toml**：尤其 `[params].description` 与 `[params.meta].description`，任何情况下都不要动。
- **不碰代码块**：正文里的命令、配置、代码片段一字不改。脚本已经做了代码区隔离，你手工编辑时同样要守住。
- **图片文件名必须纯 ASCII 且无空格**：Hugo 不会报错，但线上会 404。脚本已保证，手工加图时注意。

## 验证

同步完成后必须证明它真的没坏：

```bash
hugo
```

构建应当成功（只有已知的 `languageCode` / `.Site.LanguageCode` deprecation 警告）。再抽查：

- 每篇文末只有一份「Feisky 公众号二维码」
- 小节标题（`##`/`###`）数量与源文一致，没有被话题标签清理误删
- 新增图片在 `static/images/` 里真实存在
- 新文章 frontmatter 都有 `description`

`scripts/` 下的脚本自带图片落盘校验，缺图会非零退出，别忽略退出码。
