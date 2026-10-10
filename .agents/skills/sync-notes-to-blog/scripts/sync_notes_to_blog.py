#!/usr/bin/env python3
"""把 ~/notes/history 的新文章同步到 Hugo 博客。

负责所有确定性的搬运与改写：识别新文章、清理 frontmatter、删除公众号运营残留、
本地化图片、删除公众号结尾。需要理解内容的部分（description 措辞、alt 描述、题记、
faq）由 agent 在脚本跑完后补，脚本会把这些缺口列进报告。

用法（必须在 blog 根目录运行）：
    python3 .claude/skills/sync-notes-to-blog/scripts/sync_notes_to_blog.py --list
    python3 .claude/skills/sync-notes-to-blog/scripts/sync_notes_to_blog.py --dry-run
    python3 .claude/skills/sync-notes-to-blog/scripts/sync_notes_to_blog.py --batch 10
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

DEFAULT_NOTES_DIR = Path.home() / "notes" / "history"
STATIC_IMAGES = Path("static/images")
POSTS_DIR = Path("content/posts")
STATE_FILE = Path(".claude/skills/sync-notes-to-blog/state.json")

# frontmatter 中要删掉的公众号/运营字段
DROP_FM_KEYS = {"mp_url", "stats", "format", "cover"}
# 要删掉的运营标签
DROP_TAGS = {"爆款", "超爆款", "小绿书", "10万+", "十万+"}
# 标签规范形（左边任意写法归一到右边）
TAG_CANON = {
    "ai编程": "AI 编程",
    "ai 编程": "AI 编程",
    "ai记忆": "AI 记忆",
    "ai 记忆": "AI 记忆",
    "automemory": "Auto Memory",
    "auto memory": "Auto Memory",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "ralph loop": "Ralph Loop",
    "claude code": "Claude Code",
    "ai agent": "AI Agent",
    "ai infra": "AI Infra",
    "llm": "LLM",
    "mcp": "MCP",
    "rag": "RAG",
}

# 博客不再带公众号结尾，二维码统一放在 about 页。正文里出现它就说明结尾没清干净。
FOOTER_MARKER = "/images/mp.png"

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(\s*([^)\s]+?)\s*(?:\s+\"([^\"]*)\")?\s*\)")
VALID_IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico", ".avif"}

# 公众号引导段的特征词。整段命中任一即视为运营引导语。
CTA_PATTERNS = [
    re.compile(r"关注\s*\**\s*Feisky"),
    re.compile(r"关注我的公众号"),
    re.compile(r"欢迎关注.{0,12}公众号"),
    re.compile(r"公众号.{0,12}(持续|定期)分享"),
    re.compile(r"长按.{0,10}二维码"),
    re.compile(r"扫码关注"),
    re.compile(r"点赞|在看|转发一下|星标"),
    re.compile(r"\(/images/mp\.png\)"),
]
# 引导段里若出现这些，说明是正文而非纯 CTA，不删
CTA_VETO = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s|>|#)", re.M)


# ---------------------------------------------------------------------------
# 通用工具
# ---------------------------------------------------------------------------


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def slugify_ascii(text: str, maxlen: int = 48) -> str:
    """把任意标题/文件名压成安全的 ASCII slug。

    static/images 现存 774 个文件 100% 是无空格 ASCII；带空格或中文的路径会让
    Markdown 在空格处截断 URL、让图片整个裂掉，所以这里必须转写而不是原样保留。
    """
    text = unicodedata.normalize("NFKD", text)
    out = []
    for ch in text:
        if ch.isascii() and (ch.isalnum() or ch in "-_"):
            out.append(ch)
        elif ch.isascii() and ch in " ./\\":
            out.append("-")
        # 非 ASCII（中文、全角标点）直接丢弃
    slug = re.sub(r"-{2,}", "-", "".join(out)).strip("-.")
    return slug[:maxlen].strip("-.") or "post"


def split_code_aware(text: str) -> list[tuple[str, bool]]:
    """按 fenced code block 切段，返回 [(片段, 是否代码)]。

    所有正文正则改写都必须走这里。不然 `_斜体_` 规则会把
    CLAUDE_CODE_DISABLE_AUTO_MEMORY 写成 CLAUDE*CODE*DISABLE*AUTO*MEMORY，
    autolink 会把 `curl https://x/install.sh | bash` 包成尖括号让命令失效。
    """
    parts: list[tuple[str, bool]] = []
    buf: list[str] = []
    in_code = False
    fence = ""
    for line in text.splitlines(keepends=True):
        m = re.match(r"^(\s*)(`{3,}|~{3,})", line)
        if m and not in_code:
            parts.append(("".join(buf), False))
            buf = [line]
            in_code = True
            fence = m.group(2)[0] * 3
        elif m and in_code and m.group(2).startswith(fence):
            buf.append(line)
            parts.append(("".join(buf), True))
            buf = []
            in_code = False
        else:
            buf.append(line)
    if buf:
        parts.append(("".join(buf), in_code))
    return parts


INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def sub_outside_inline_code(pattern: re.Pattern, repl, text: str) -> str:
    """在跳过行内 `code` 的前提下做替换。"""
    out = []
    pos = 0
    for m in INLINE_CODE_RE.finditer(text):
        out.append(pattern.sub(repl, text[pos : m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(pattern.sub(repl, text[pos:]))
    return "".join(out)


def transform_prose(text: str, fn) -> str:
    """只对非代码的正文片段应用 fn。"""
    return "".join(
        seg if is_code else sub_outside_inline_code_wrapper(seg, fn)
        for seg, is_code in split_code_aware(text)
    )


def sub_outside_inline_code_wrapper(seg: str, fn) -> str:
    out = []
    pos = 0
    for m in INLINE_CODE_RE.finditer(seg):
        out.append(fn(seg[pos : m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fn(seg[pos:]))
    return "".join(out)


# ---------------------------------------------------------------------------
# frontmatter
# ---------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """返回 (frontmatter 行列表, 正文)。无 frontmatter 时返回 ([], 全文)。"""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---\n", 3)
    if end == -1:
        return [], text
    fm = text[4:end].split("\n")
    body = text[end + 5 :]
    return fm, body


def drop_fm_keys(fm: list[str], keys: set[str]) -> tuple[list[str], list[str]]:
    """删除指定的顶层键，含其下所有缩进子行。

    终止条件是「下一个非缩进行 或 列表结束」两者取先到者。9 篇含 stats 的文章里
    stats 全是最后一个键，只按「下一个顶层键」找终止会一路删到文件末尾，
    连 frontmatter 的闭合 --- 和整篇正文都吞掉。
    """
    out: list[str] = []
    dropped: list[str] = []
    i = 0
    while i < len(fm):
        line = fm[i]
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:", line)
        if m and m.group(1) in keys:
            dropped.append(m.group(1))
            i += 1
            while i < len(fm) and (fm[i].startswith((" ", "\t")) or not fm[i].strip()):
                # 空行只有在后面还有缩进行时才算属于本块
                if not fm[i].strip():
                    j = i + 1
                    while j < len(fm) and not fm[j].strip():
                        j += 1
                    if j >= len(fm) or not fm[j].startswith((" ", "\t")):
                        break
                i += 1
            continue
        out.append(line)
        i += 1
    return out, dropped


def get_fm_value(fm: list[str], key: str) -> str | None:
    for line in fm:
        m = re.match(rf"^{re.escape(key)}\s*:\s*(.*)$", line)
        if m:
            return m.group(1).strip()
    return None


def parse_tags(fm: list[str]) -> tuple[list[str] | None, int, int]:
    """解析 tags，同时支持 inline flow 与 block sequence 两种 YAML 形态。

    返回 (标签列表, 起始行号, 结束行号+1)。8 篇用 block 形式，只认 inline
    会让这些文章的运营标签清理静默失效。
    """
    for i, line in enumerate(fm):
        m = re.match(r"^tags\s*:\s*(.*)$", line)
        if not m:
            continue
        rest = m.group(1).strip()
        if rest.startswith("["):
            inner = rest[1 : rest.rfind("]")] if "]" in rest else rest[1:]
            tags = [t.strip().strip("\"'") for t in inner.split(",") if t.strip()]
            return tags, i, i + 1
        if rest:
            return [rest.strip("\"'")], i, i + 1
        tags = []
        j = i + 1
        while j < len(fm) and re.match(r"^\s*-\s+", fm[j]):
            tags.append(re.sub(r"^\s*-\s+", "", fm[j]).strip().strip("\"'"))
            j += 1
        return tags, i, j
    return None, -1, -1


def canon_tag(tag: str) -> str:
    return TAG_CANON.get(tag.strip().lower(), tag.strip())


def yaml_quote(s: str) -> str:
    s = s.strip()
    if s.startswith(('"', "'")) and s.endswith(('"', "'")) and len(s) > 1:
        s = s[1:-1]
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---------------------------------------------------------------------------
# 正文清理
# ---------------------------------------------------------------------------


def norm_title(s: str) -> str:
    """标题比对用的归一化：去空白、去常见标点、转小写。"""
    s = nfc(s).lower()
    return re.sub(r"[\s：:，,。.！!？?、\"'`*_\-—～~（）()\[\]]+", "", s)


def strip_leading_h1(body: str, title: str | None) -> tuple[str, str | None]:
    """删除正文开头与 title 重复的 H1，返回 (新正文, 从 H1 提取到的标题)。

    5 篇 frontmatter 没有 title，正文 H1 是唯一且排版更好的标题来源
    （`# 从手写代码到指挥 AI：AI 大神 Karpathy 的编程转型实录` 带正确的中英空格，
    文件名 slug 则没有）。所以先把 H1 回填成 title，再删 H1。
    """
    lines = body.split("\n")
    idx = next((i for i, l in enumerate(lines) if l.strip()), None)
    if idx is None:
        return body, None
    m = re.match(r"^#\s+(.+?)\s*$", lines[idx])
    if not m:
        return body, None
    h1 = m.group(1).strip()
    # 微信导出正文首行恒为文章大标题（title 缺失时是更好的标题来源，含正确中英空格）。
    # 一律删除：即便与 frontmatter title 文字略有出入（如「23万个…」vs「23 万 OpenClaw…」），
    # 它仍是标题的重述，留着会和页面 H1 重复。只有 title 缺失时才用它回填。
    del lines[idx]
    while idx < len(lines) and not lines[idx].strip():
        del lines[idx]
    return "\n".join(lines), h1


def strip_cover_image(body: str) -> tuple[str, str | None]:
    """删除正文开头的封面图。只认前 6 个非空行内、alt 或文件名含 cover/封面 的。"""
    lines = body.split("\n")
    seen = 0
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        seen += 1
        if seen > 6:
            break
        m = IMAGE_RE.fullmatch(line.strip())
        if not m:
            continue
        alt, url = m.group(1) or "", m.group(2)
        if re.search(r"cover|封面", alt, re.I) or re.search(r"cover|封面", url, re.I):
            removed = line.strip()
            del lines[i]
            while i < len(lines) and not lines[i].strip():
                del lines[i]
            return "\n".join(lines), removed
    return body, None


# 微信话题标签行：`#Claude Code #MCP #AI编程 #context优化`
# 标签内部允许空格（微信就是这么写的），所以不能按 \S+ 切 token，只能整行判定：
#   1) 行首（可有「话题标签：」前缀）就是 `#` 且紧跟非空白非 `#` —— 排除 ATX 标题
#      `# 标题` / `## 小节`，否则 46 篇文章的全部小节标题会被删光；
#   2) 整行至少 2 个 `#`（单个 `#xxx` 太像正文里的 issue 号引用，不碰）；
#   3) 行内不出现句末标点和 markdown 结构字符，避免误伤正文句子。
HASHTAG_LINE = re.compile(
    r"^\s*(?:话题标签[:：]\s*)?"          # 可选前缀
    r"#[^\s#]"                            # 首个标签：# 后紧跟非空白非 #
    r"[^#\n]*"                            # 标签正文（可含空格）
    r"(?:#[^\s#][^#\n]*){1,}"             # 至少还有一个 #标签
    r"$"
)
HASHTAG_VETO = re.compile(r"[。！？；：，、]|\||`|\[|\]|\(|\)")


def strip_hashtag_lines(body: str) -> tuple[str, int]:
    """删除文末的话题标签行（`#GPT5 #提示词工程`）。

    必须排除 `##` 开头：`#` 后跟 `\\S` 会把第二个 `#` 吃掉，于是 `## 写在最后`
    也被当成话题标签，48 篇里 46 篇的全部小节标题会被删光。这里要求 `#` 后
    紧跟非 `#` 非空白字符，且整行只由标签构成，并且只在文末区域和非代码段生效。
    """
    parts = split_code_aware(body)
    total = 0
    # 只处理最后一个非代码片段的尾部
    for pi in range(len(parts) - 1, -1, -1):
        seg, is_code = parts[pi]
        if is_code:
            break
        lines = seg.split("\n")
        keep = []
        removed_here = 0
        for i in range(len(lines) - 1, -1, -1):
            stripped = lines[i].strip()
            if not stripped:
                keep.append(i)
                continue
            tag_body = re.sub(r"^\s*话题标签[:：]\s*", "", stripped)
            if HASHTAG_LINE.match(lines[i]) and not HASHTAG_VETO.search(tag_body):
                lines[i] = None  # type: ignore[call-overload]
                removed_here += 1
                continue
            break
        if removed_here:
            parts[pi] = ("\n".join(l for l in lines if l is not None), False)
            total += removed_here
        break
    return "".join(s for s, _ in parts), total


def strip_cta_block(body: str) -> tuple[str, list[str]]:
    """删除文末的公众号引导语段落。

    「相关资源 / 相关链接」列表也在文末、也用 --- 分隔，必须保住，所以用段落级
    特征识别：整段命中 CTA 特征词、且不含列表项/链接/标题时才删。锚点不能写死成
    「好了今天就聊到这儿」，还有「如果觉得有帮助，欢迎关注我的公众号 Feisky」
    这种变体，漏掉会导致旧引导语留在文末。公众号二维码图（/images/mp.png）也一并删除。
    """
    parts = split_code_aware(body)
    # CTA 只可能在最后一个非代码片段里
    tail_idx = None
    for i in range(len(parts) - 1, -1, -1):
        if not parts[i][1]:
            tail_idx = i
            break
    if tail_idx is None:
        return body, []

    seg = parts[tail_idx][0]
    blocks = re.split(r"\n\s*\n", seg)
    removed: list[str] = []
    while blocks:
        blk = blocks[-1]
        s = blk.strip()
        if not s:
            blocks.pop()
            continue
        if re.fullmatch(r"-{3,}", s) or re.fullmatch(r"\*{3,}", s):
            # 悬空分隔线：只有在它前面已经删过 CTA 时才一并删掉
            if removed:
                blocks.pop()
                continue
            break
        if any(p.search(s) for p in CTA_PATTERNS) and not CTA_VETO.search(s):
            removed.append(s)
            blocks.pop()
            continue
        break
    if not removed:
        return body, []
    parts[tail_idx] = ("\n\n".join(blocks).rstrip() + "\n", False)
    return "".join(s for s, _ in parts), removed


def autolink_bare_urls(text: str) -> str:
    def fn(chunk: str) -> str:
        return re.sub(
            r"(?<![\(<\[\"'=])\bhttps?://[^\s<>\)\]\"']+(?<![.,;:！。，、）])",
            lambda m: f"<{m.group(0)}>",
            chunk,
        )

    return transform_prose(text, fn)


def normalize_spacing(text: str) -> str:
    """中英文之间补空格、百分号周边补空格、`_斜体_` 改 `*斜体*`。"""

    def fn(chunk: str) -> str:
        # 跳过 markdown 链接/图片的 URL 部分
        placeholders: list[str] = []

        def stash(m: re.Match) -> str:
            placeholders.append(m.group(0))
            return f"\x00{len(placeholders) - 1}\x00"

        chunk = re.sub(r"!?\[[^\]]*\]\([^)]*\)|<https?://[^>]+>", stash, chunk)
        cjk = r"一-鿿぀-ヿ"
        chunk = re.sub(rf"([{cjk}])([A-Za-z0-9])", r"\1 \2", chunk)
        chunk = re.sub(rf"([A-Za-z0-9%])([{cjk}])", r"\1 \2", chunk)
        chunk = re.sub(r"\b(\d+)\s*%([^\s])", r"\1% \2", chunk)
        chunk = re.sub(r"(?<![\w\\])_([^_\n]+)_(?![\w])", r"*\1*", chunk)
        for i, p in enumerate(placeholders):
            chunk = chunk.replace(f"\x00{i}\x00", p)
        return chunk

    return transform_prose(text, fn)


# ---------------------------------------------------------------------------
# 图片
# ---------------------------------------------------------------------------


@dataclass
class ImageAction:
    kind: str  # copy | download | skip
    src: str
    dest: str
    alt: str
    ok: bool = True
    err: str = ""


def resolve_local(url: str, md_path: Path, vault_root: Path) -> Path | None:
    u = unquote(url).split("#")[0].split("?")[0]
    if u.startswith("./"):
        u = u[2:]
    cands = [md_path.parent / u, vault_root / u]
    for c in cands:
        if c.exists() and c.is_file():
            return c
    return None


def localize_images(
    body: str,
    md_path: Path,
    vault_root: Path,
    slug: str,
    images_dir: Path,
    dry_run: bool,
    timeout: int,
) -> tuple[str, list[ImageAction]]:
    actions: list[ImageAction] = []

    def repl(m: re.Match) -> str:
        alt, url, title = m.group(1) or "", m.group(2), m.group(3)
        if url.startswith("/images/") or url.startswith("data:"):
            return m.group(0)

        if url.startswith(("http://", "https://")):
            ext = Path(urlparse(url).path).suffix.lower()
            if ext not in VALID_IMG_EXT:
                ext = ".png"
            base = Path(unquote(urlparse(url).path)).stem
            name = f"{slug}-{slugify_ascii(base, 32) or 'img'}{ext}"
            dest = images_dir / uniquify(name, images_dir, url)
            act = ImageAction("download", url, str(dest), alt)
            if not dry_run:
                try:
                    fetch(url, dest, timeout)
                except Exception as exc:  # noqa: BLE001
                    act.ok = False
                    act.err = f"{type(exc).__name__}: {exc}"
            actions.append(act)
            if not act.ok:
                return m.group(0)
            new = f"/images/{dest.name}"
        else:
            src = resolve_local(url, md_path, vault_root)
            if src is None:
                actions.append(ImageAction("copy", url, "", alt, ok=False, err="源文件不存在"))
                return m.group(0)
            name = f"{slug}-{slugify_ascii(src.stem, 32) or 'img'}{src.suffix.lower()}"
            dest = images_dir / uniquify(name, images_dir, str(src))
            act = ImageAction("copy", str(src), str(dest), alt)
            if not dry_run:
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
                except Exception as exc:  # noqa: BLE001
                    act.ok = False
                    act.err = f"{type(exc).__name__}: {exc}"
            actions.append(act)
            if not act.ok:
                return m.group(0)
            new = f"/images/{dest.name}"

        tail = f' "{title}"' if title else ""
        return f"![{alt}]({new}{tail})"

    return IMAGE_RE.sub(repl, body), actions


_NAME_OWNER: dict[str, str] = {}


def uniquify(name: str, images_dir: Path, owner: str) -> str:
    """同名不同源时加序号；同名同源复用同一个目标名（保证重复运行幂等）。"""
    if _NAME_OWNER.get(name) == owner:
        return name
    stem, ext = Path(name).stem, Path(name).suffix
    cand, n = name, 1
    while True:
        prev = _NAME_OWNER.get(cand)
        if prev == owner:
            return cand
        if prev is None and not (images_dir / cand).exists():
            _NAME_OWNER[cand] = owner
            return cand
        if prev is None and (images_dir / cand).exists():
            # 磁盘上已有同名文件：若是本脚本上次写的同一来源，视为可复用
            _NAME_OWNER[cand] = owner
            return cand
        n += 1
        cand = f"{stem}-{n}{ext}"


def fetch(url: str, dest: Path, timeout: int) -> None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; blog-sync/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        data = resp.read()
    if not data:
        raise ValueError("空响应")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


# ---------------------------------------------------------------------------
# 单篇处理
# ---------------------------------------------------------------------------


@dataclass
class Result:
    name: str
    status: str = "ok"  # ok | skipped | error
    reason: str = ""
    dropped_keys: list[str] = field(default_factory=list)
    dropped_tags: list[str] = field(default_factory=list)
    images: list[ImageAction] = field(default_factory=list)
    cta_removed: list[str] = field(default_factory=list)
    cover_removed: str | None = None
    hashtags_removed: int = 0
    needs_description: bool = False
    empty_alts: int = 0
    source_url: str | None = None
    is_draft: bool = False
    warnings: list[str] = field(default_factory=list)


def process(
    name: str,
    notes_dir: Path,
    vault_root: Path,
    blog_root: Path,
    dry_run: bool,
    date_seq: int,
    timeout: int,
) -> Result:
    res = Result(name=name)
    src = notes_dir / name
    text = src.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if not fm:
        fm = []

    res.source_url = get_fm_value(fm, "source")
    if get_fm_value(fm, "draft") == "true":
        res.is_draft = True

    fm, dropped = drop_fm_keys(fm, DROP_FM_KEYS | {"source"})
    res.dropped_keys = dropped

    title = get_fm_value(fm, "title")
    if title:
        title = title.strip().strip("\"'")

    body, h1 = strip_leading_h1(body, title)
    if not title:
        title = h1 or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", Path(name).stem)
        if not h1:
            res.warnings.append("title 由文件名推导，建议人工确认")

    body, res.cover_removed = strip_cover_image(body)
    body, res.hashtags_removed = strip_hashtag_lines(body)
    body, res.cta_removed = strip_cta_block(body)

    slug = slugify_ascii(Path(name).stem, 40)
    body, res.images = localize_images(
        body, src, vault_root, slug, blog_root / STATIC_IMAGES, dry_run, timeout
    )
    body = autolink_bare_urls(body)
    body = normalize_spacing(body)

    res.empty_alts = sum(1 for m in IMAGE_RE.finditer(body) if not (m.group(1) or "").strip())

    body = body.rstrip() + "\n"

    # ---- 重建 frontmatter ----
    date_raw = get_fm_value(fm, "date")
    date_val = normalize_date(date_raw, name, date_seq)
    tags, ts, te = parse_tags(fm)
    if tags is not None:
        kept = []
        for t in tags:
            if t.strip() in DROP_TAGS:
                res.dropped_tags.append(t.strip())
            else:
                c = canon_tag(t)
                if c not in kept:
                    kept.append(c)
        tag_line = "tags: [" + ", ".join(kept) + "]"
    else:
        tag_line = None
        res.warnings.append("缺少 tags，需要 agent 补")

    desc = get_fm_value(fm, "description")
    res.needs_description = not desc

    rebuilt = ["---", f"title: {yaml_quote(title)}", f"date: {date_val}"]
    rebuilt.append("draft: true" if res.is_draft else "draft: false")
    if tag_line:
        rebuilt.append(tag_line)
    if desc:
        rebuilt.append(f"description: {yaml_quote(desc)}")
    # 保留其他未识别的自定义键（category/layout/image/faq 等）
    known = {"title", "date", "draft", "tags", "description"}
    i = 0
    while i < len(fm):
        line = fm[i]
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:", line)
        if m and m.group(1) not in known:
            rebuilt.append(line)
            i += 1
            while i < len(fm) and (fm[i].startswith((" ", "\t")) or re.match(r"^\s*-\s", fm[i])):
                rebuilt.append(fm[i])
                i += 1
            continue
        if m and m.group(1) == "tags":
            i = te if te > 0 else i + 1
            continue
        i += 1
    rebuilt.append("---")

    out = "\n".join(rebuilt) + "\n\n" + body.lstrip("\n")

    if "——" in out or "—" in out:
        res.warnings.append("正文含破折号，需人工替换（源文即有，脚本不自动改写正文语义）")

    if not dry_run:
        dest = blog_root / POSTS_DIR / name
        dest.write_text(out, encoding="utf-8")
    return res


def normalize_date(raw: str | None, filename: str, seq: int) -> str:
    """补齐为 ISO 8601 带时区。同日多篇按序递增分钟，避免排序不稳定。"""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", filename)
    file_date = m.group(1) if m else None
    if raw:
        v = raw.strip().strip("\"'")
        if re.match(r"^\d{4}-\d{2}-\d{2}T[\d:]+(?:[+-]\d{2}:\d{2}|Z)$", v):
            return v
        if re.match(r"^\d{4}-\d{2}-\d{2}T[\d:]+$", v):
            return v + "+08:00"
        if re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            return f"{v}T{10 + seq // 60:02d}:{seq % 60:02d}:00+08:00"
    if file_date:
        return f"{file_date}T{10 + seq // 60:02d}:{seq % 60:02d}:00+08:00"
    return "1970-01-01T00:00:00+08:00"


# ---------------------------------------------------------------------------
# 完成度探针与状态
# ---------------------------------------------------------------------------


def completeness(path: Path) -> list[str]:
    """检查一篇已在 content/posts 的文章是否已完成加工。

    只靠「文件名已存在 = 跳过」会让半成品永久卡住：第一次运行复制了 48 篇，
    agent 写到第 20 篇时中断，重跑时差集为空，剩下 28 篇再也不会被拾起。
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ["无法读取"]
    fm, body = split_frontmatter(text)
    gaps = []
    if any(re.match(rf"^{k}\s*:", l) for l in fm for k in DROP_FM_KEYS):
        gaps.append("残留公众号/运营字段")
    tags, _, _ = parse_tags(fm)
    if tags and any(t.strip() in DROP_TAGS for t in tags):
        gaps.append("残留运营标签")
    if not get_fm_value(fm, "description"):
        gaps.append("缺 description")
    if FOOTER_MARKER in body:
        gaps.append("残留公众号结尾")
    for m in IMAGE_RE.finditer(body):
        if not m.group(2).startswith(("/images/", "data:", "http")):
            gaps.append("图片引用未本地化")
            break
    return gaps


def verify_images(blog_root: Path, names: list[str]) -> list[str]:
    """核对每篇文章引用的 /images/ 文件真实存在。

    Hugo 的 render-image.html 只是原样输出 <img src>，缺图不会让构建失败，
    所以「hugo 构建通过」证明不了图片没丢，必须单独查磁盘。
    """
    bad = []
    for n in names:
        p = blog_root / POSTS_DIR / n
        if not p.exists():
            continue
        for m in IMAGE_RE.finditer(p.read_text(encoding="utf-8")):
            url = m.group(2)
            if not url.startswith("/images/"):
                continue
            f = blog_root / "static" / url.lstrip("/")
            if not f.exists():
                bad.append(f"{n}: {url}")
    return bad


def load_state(blog_root: Path) -> dict:
    p = blog_root / STATE_FILE
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
    return {}


def save_state(blog_root: Path, state: dict) -> None:
    p = blog_root / STATE_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def find_candidates(notes_dir: Path, blog_root: Path) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """返回 (全新文章, [(已存在但未完成的文章, 缺口)])。"""
    posts = blog_root / POSTS_DIR
    existing = {nfc(n) for n in os.listdir(posts)}
    fresh, partial = [], []
    for n in sorted(os.listdir(notes_dir)):
        if not n.endswith(".md") or n == "README.md":
            continue
        if nfc(n) in existing:
            gaps = completeness(posts / n)
            # 缺 description 是 agent 的活，单独列出但不算「机械未完成」
            mech = [g for g in gaps if g != "缺 description"]
            if mech:
                partial.append((n, gaps))
        else:
            fresh.append(n)
    return fresh, partial


def main() -> int:
    ap = argparse.ArgumentParser(description="同步 notes/history 新文章到 Hugo 博客")
    ap.add_argument("--notes-dir", type=Path, default=DEFAULT_NOTES_DIR)
    ap.add_argument("--blog-root", type=Path, default=Path.cwd())
    ap.add_argument("--dry-run", action="store_true", help="只预演不落盘")
    ap.add_argument("--list", action="store_true", help="只列出待同步候选")
    ap.add_argument("--only", action="append", default=[], help="只处理指定文件名，可重复")
    ap.add_argument("--batch", type=int, default=0, help="本次最多处理几篇（0=不限）")
    ap.add_argument("--include-drafts", action="store_true", help="同步 draft: true 的文章")
    ap.add_argument("--reprocess", action="store_true", help="重新处理未完成的已存在文章")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    blog_root = args.blog_root.resolve()
    notes_dir = args.notes_dir.resolve()
    vault_root = notes_dir.parent

    if not (blog_root / POSTS_DIR).is_dir() or not (blog_root / "config.toml").is_file():
        print(f"错误：{blog_root} 看起来不是 blog 根目录（缺 content/posts 或 config.toml）", file=sys.stderr)
        return 2
    if not notes_dir.is_dir():
        print(f"错误：源目录不存在 {notes_dir}", file=sys.stderr)
        return 2

    fresh, partial = find_candidates(notes_dir, blog_root)

    if args.list:
        print(f"待同步（全新）：{len(fresh)} 篇")
        for n in fresh:
            print("  +", n)
        if partial:
            print(f"\n已存在但加工未完成：{len(partial)} 篇（用 --reprocess 续处理）")
            for n, gaps in partial:
                print(f"  ! {n}  [{', '.join(gaps)}]")
        return 0

    targets = list(fresh)
    if args.reprocess:
        targets += [n for n, _ in partial]
    if args.only:
        want = {nfc(o) for o in args.only}
        targets = [n for n in targets if nfc(n) in want or nfc(Path(n).name) in want]
        if not targets:
            print("错误：--only 指定的文件不在待同步集合里", file=sys.stderr)
            return 2

    skipped_drafts = []
    if not args.include_drafts:
        keep = []
        for n in targets:
            head = (notes_dir / n).read_text(encoding="utf-8")[:600]
            if re.search(r"^draft:\s*true", head, re.M):
                skipped_drafts.append(n)
            else:
                keep.append(n)
        targets = keep

    if args.batch:
        targets = targets[: args.batch]

    if not targets:
        print("没有需要同步的文章。")
        if skipped_drafts:
            print(f"（跳过 {len(skipped_drafts)} 篇 draft，用 --include-drafts 处理）")
        return 0

    # 同日多篇需要稳定的时间 tie-break
    seq: dict[str, int] = {}
    results: list[Result] = []
    for n in targets:
        day = n[:10]
        s = seq.get(day, 0)
        seq[day] = s + 1
        try:
            results.append(
                process(n, notes_dir, vault_root, blog_root, args.dry_run, s, args.timeout)
            )
        except Exception as exc:  # noqa: BLE001
            r = Result(name=n, status="error", reason=f"{type(exc).__name__}: {exc}")
            results.append(r)

    report(results, skipped_drafts, args.dry_run, blog_root, targets)

    hard = [r for r in results if r.status == "error"]
    img_fail = [a for r in results for a in r.images if not a.ok]
    missing = [] if args.dry_run else verify_images(blog_root, [r.name for r in results if r.status == "ok"])

    if not args.dry_run:
        state = load_state(blog_root)
        for r in results:
            if r.status == "ok":
                state[r.name] = {
                    "mechanical": "done",
                    "needs_description": r.needs_description,
                    "empty_alts": r.empty_alts,
                    "source_url": r.source_url,
                }
        save_state(blog_root, state)

    if hard or img_fail or missing:
        print("\n=== 硬错误 ===", file=sys.stderr)
        for r in hard:
            print(f"  处理失败 {r.name}: {r.reason}", file=sys.stderr)
        for a in img_fail:
            print(f"  图片失败 {a.kind} {a.src}: {a.err}", file=sys.stderr)
        for m in missing:
            print(f"  图片引用指向不存在的文件 {m}", file=sys.stderr)
        return 1
    return 0


def report(
    results: list[Result],
    skipped_drafts: list[str],
    dry_run: bool,
    blog_root: Path,
    targets: list[str],
) -> None:
    mode = "预演" if dry_run else "已写入"
    print(f"=== 同步报告（{mode}）===\n")
    for r in results:
        if r.status == "error":
            print(f"✗ {r.name}\n    {r.reason}")
            continue
        bits = []
        if r.dropped_keys:
            bits.append(f"删字段 {'/'.join(r.dropped_keys)}")
        if r.dropped_tags:
            bits.append(f"删标签 {'/'.join(r.dropped_tags)}")
        if r.cover_removed:
            bits.append("删封面图")
        if r.hashtags_removed:
            bits.append(f"删话题标签 {r.hashtags_removed} 行")
        if r.cta_removed:
            bits.append(f"删除公众号引导语 {len(r.cta_removed)} 段")
        cp = sum(1 for a in r.images if a.kind == "copy" and a.ok)
        dl = sum(1 for a in r.images if a.kind == "download" and a.ok)
        if cp:
            bits.append(f"复制图片 {cp}")
        if dl:
            bits.append(f"下载图片 {dl}")
        print(f"✓ {r.name}\n    {'，'.join(bits) if bits else '无机械改动'}")
        todo = []
        if r.needs_description:
            todo.append("生成 description")
        if r.empty_alts:
            todo.append(f"补 {r.empty_alts} 处图片 alt")
        if r.source_url:
            todo.append(f"把原文出处写成题记：{r.source_url}")
        for w in r.warnings:
            todo.append(w)
        if todo:
            print(f"    待 agent 处理：{'；'.join(todo)}")

    ok = [r for r in results if r.status == "ok"]
    print(f"\n小计：{len(ok)}/{len(results)} 篇成功")
    print(
        f"图片：复制 {sum(1 for r in ok for a in r.images if a.kind == 'copy' and a.ok)}，"
        f"下载 {sum(1 for r in ok for a in r.images if a.kind == 'download' and a.ok)}，"
        f"失败 {sum(1 for r in ok for a in r.images if not a.ok)}"
    )
    need_desc = [r.name for r in ok if r.needs_description]
    if need_desc:
        print(f"待生成 description：{len(need_desc)} 篇")
    if skipped_drafts:
        print(f"跳过 draft: true：{len(skipped_drafts)} 篇 -> {', '.join(skipped_drafts)}")


if __name__ == "__main__":
    sys.exit(main())
