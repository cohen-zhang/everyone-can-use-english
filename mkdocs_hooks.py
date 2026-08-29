"""MkDocs hooks: Obsidian-style wikilinks + vault-root paths → normal Markdown (docs_dir = learning-notes/)."""

from __future__ import annotations

import os
import re
from pathlib import Path, PurePosixPath

try:
    import yaml
except ImportError:  # pragma: no cover - optional at hook import time
    yaml = None

# Allow \| inside table cells; path may include #fragment before |title.
WIKI_LINK = re.compile(
    r"(?<!!)\[\[((?:[^\]\\]|\\.)+?)(?:\\?\|((?:[^\]\\]|\\.)+?))?\]\]"
)
MD_LEARNING_NOTES = re.compile(r"\]\(([^)]*learning-notes/[^)]+)\)")
MD_TRANSCRIPT_LINK = re.compile(r"\]\(([^)]*/transcript/[^)]+\.(?:txt|ya?ml))\)")
SOURCE_EXTS = (".txt", ".yaml", ".yml")

_stem_to_paths: dict[str, list[str]] | None = None
_repo_root: Path | None = None
_docs_dir: Path | None = None
_episode_titles: dict[int, dict[str, str]] | None = None

EPISODE_NUM = re.compile(r"s(\d+)e(\d+)", re.IGNORECASE)
SCENE_INDEX_THEME = re.compile(
    r"##\s*场景分段索引（S\d+E\d+\s*·\s*(.+?)）\s*$", re.MULTILINE
)


def _episode_num_from_name(name: str) -> int | None:
    match = EPISODE_NUM.search(name)
    return int(match.group(2)) if match else None


def _load_episode_titles(docs_dir: Path) -> dict[int, dict[str, str]]:
    path = docs_dir / "tv-series/modern-family/s01/episode-titles.yaml"
    if not path.is_file() or yaml is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    episodes = data.get("episodes") or {}
    return {int(ep): meta for ep, meta in episodes.items()}


def _episode_theme(ep: int | None, titles: dict[int, dict[str, str]]) -> str:
    if not ep:
        return ""
    return str((titles.get(ep) or {}).get("theme") or "").strip()


def _theme_from_transcript_txt(txt_path: Path) -> str:
    match = SCENE_INDEX_THEME.search(txt_path.read_text(encoding="utf-8", errors="replace"))
    return match.group(1).strip() if match else ""


def _page_title_for_episode(
    ep: int, kind: str, titles: dict[int, dict[str, str]]
) -> str | None:
    theme = _episode_theme(ep, titles)
    if not theme:
        return None
    suffix = {
        "transcript": "字幕",
        "daily-lines": "场景句",
        "key-dad": "亲子对话",
        "transcript-hand": "精编场景句",
    }.get(kind)
    if not suffix:
        return None
    return f"S01E{ep:02d} · {theme} — {suffix}"


def _kind_from_path(src_path: str) -> tuple[int | None, str | None]:
    src = src_path.replace("\\", "/")
    if "tv-series/modern-family/s01" not in src:
        return None, None
    ep = _episode_num_from_name(src)
    if not ep:
        return None, None
    name = Path(src).name
    if "/transcript/" in src and name.endswith("-transcript.md"):
        return ep, "transcript"
    if "/transcript/" in src and "daily-lines" in name:
        return ep, "transcript-hand"
    if "/notes/" in src and name.endswith("-daily-lines.md"):
        return ep, "daily-lines"
    if "key-to-being-a-great-dad" in name:
        return ep, "key-dad"
    return ep, None


def _default_link_title(raw: str) -> str:
    ep = _episode_num_from_name(raw)
    titles = _episode_titles or {}
    if ep and titles:
        if "-transcript" in raw or raw.endswith(".txt"):
            theme = _episode_theme(ep, titles)
            if theme:
                return f"S01E{ep:02d} · {theme} — 字幕"
        if "-daily-lines" in raw:
            theme = _episode_theme(ep, titles)
            if theme:
                return f"S01E{ep:02d} · {theme} — 场景句"
    return PurePosixPath(raw.replace("\\", "/")).name


def _fence_code(content: str, lang: str = "text") -> str:
    """Wrap content in a fenced code block (longer fence if body contains ```)."""
    fence = "```"
    while f"{fence}{lang}" in content or content.rstrip().endswith(fence):
        fence += "`"
    return f"{fence}{lang}\n{content}\n{fence}\n"


def _episode_label_from_name(name: str) -> str:
    match = re.search(r"s(\d+)e(\d+)", name, re.IGNORECASE)
    if match:
        return f"S{match.group(1)}E{match.group(2)}"
    return Path(name).stem


def _cleanup_generated_transcript_pages(transcript_dir: Path) -> None:
    for pattern in ("*-transcript.md", "*-scenes.md"):
        for path in transcript_dir.glob(pattern):
            path.unlink()


def _generate_transcript_md_pages(docs_dir: Path, titles: dict[int, dict[str, str]]) -> None:
    """Build companion ``.md`` pages for ``transcript/`` ``.txt`` and ``.yaml`` sources."""
    for transcript_dir in docs_dir.rglob("transcript"):
        if not transcript_dir.is_dir():
            continue
        _cleanup_generated_transcript_pages(transcript_dir)

        for txt_path in sorted(transcript_dir.glob("*-transcript.txt")):
            body = txt_path.read_text(encoding="utf-8", errors="replace")
            label = _episode_label_from_name(txt_path.name)
            ep = _episode_num_from_name(txt_path.name)
            theme = _episode_theme(ep, titles) or _theme_from_transcript_txt(txt_path)
            if theme:
                page_title = f"{label} · {theme} — 字幕"
            else:
                page_title = f"{label} 字幕全文"
            md_path = txt_path.with_suffix(".md")
            md_path.write_text(
                f"---\ntitle: {page_title}\n---\n\n"
                f"# {page_title}\n\n"
                f"**导航：** [字幕目录](README.md)\n\n"
                f"原文（`{txt_path.name}`）：\n\n"
                f"{_fence_code(body)}",
                encoding="utf-8",
            )

        for yaml_path in sorted(transcript_dir.glob("*-scenes.yaml")):
            body = yaml_path.read_text(encoding="utf-8", errors="replace")
            md_path = yaml_path.with_suffix(".md")
            md_path.write_text(
                f"# {_episode_label_from_name(yaml_path.name)} 场景分段配置\n\n"
                f"**导航：** [字幕目录](README.md)\n\n"
                f"源文件（`{yaml_path.name}`）：\n\n"
                f"{_fence_code(body, 'yaml')}",
                encoding="utf-8",
            )


def on_config(config, **kwargs):
    global _stem_to_paths, _repo_root, _docs_dir, _episode_titles
    _stem_to_paths = None
    _repo_root = Path(config.config_file_path).resolve().parent
    _docs_dir = Path(config.docs_dir)
    if not _docs_dir.is_absolute():
        _docs_dir = _repo_root / _docs_dir
    _episode_titles = _load_episode_titles(_docs_dir)
    _generate_transcript_md_pages(_docs_dir, _episode_titles)
    return config


def on_pre_page(page, **kwargs):
    ep, kind = _kind_from_path(page.file.src_path)
    if ep and kind and _episode_titles:
        title = _page_title_for_episode(ep, kind, _episode_titles)
        if title:
            page.title = title
    return page


def _index(files) -> dict[str, list[str]]:
    global _stem_to_paths
    if _stem_to_paths is not None:
        return _stem_to_paths
    by_stem: dict[str, list[str]] = {}
    for f in files.documentation_pages():
        p = f.src_path.replace("\\", "/")
        if not p.endswith(".md"):
            continue
        stem = p[:-3]
        key = stem.split("/")[-1]
        by_stem.setdefault(key, []).append(stem)
    _stem_to_paths = by_stem
    return _stem_to_paths


def _strip_docs_prefix(slug: str) -> str:
    s = slug.strip()
    if s.startswith("learning-notes/"):
        s = s[len("learning-notes/") :]
    return s.strip()


def _source_to_md_slug(slug: str) -> str:
    """Map ``transcript/`` ``.txt`` / ``.yaml`` slugs to generated ``.md`` stems."""
    s = slug
    for ext in SOURCE_EXTS:
        if s.endswith(ext):
            return str(PurePosixPath(s).with_suffix(".md"))[:-3]
    return s


def _resolve_target_stem(slug: str, files, page) -> str | None:
    """Return path stem relative to docs_dir (no .md), or None."""
    s = _strip_docs_prefix(slug)
    if not s:
        return None
    s = _source_to_md_slug(s)
    if s.endswith(".md"):
        s = s[:-3]
    if "/" in s:
        if any(f.src_path.replace("\\", "/") == s + ".md" for f in files.documentation_pages()):
            return s
        return None
    matches = _index(files).get(s, [])
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        cur_dir = PurePosixPath(page.file.src_path.replace("\\", "/")).parent.as_posix()
        for st in matches:
            if PurePosixPath(st).parent.as_posix() == cur_dir:
                return st
    return None


def _rel_url(from_src: str, to_md_src: str) -> str:
    fd = os.path.dirname(from_src.replace("\\", "/")) or "."
    tt = to_md_src.replace("\\", "/")
    rel = os.path.relpath(tt, fd)
    return rel.replace("\\", "/")


def _resolve_docs_md_path(page_src: str, link: str) -> str | None:
    """Resolve a Markdown link target to a docs-relative ``.md`` path."""
    page_dir = PurePosixPath(page_src.replace("\\", "/")).parent
    target = PurePosixPath(link.replace("\\", "/"))
    if not target.is_absolute() and "://" not in link:
        target = page_dir / target
    normalized = PurePosixPath(
        os.path.normpath(target.as_posix()).replace("\\", "/")
    )
    if normalized.suffix != ".md":
        normalized = normalized.with_suffix(".md")
    return normalized.as_posix()


def _wiki_replacer(markdown: str, page, files):
    cur = page.file.src_path.replace("\\", "/")

    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        title = (m.group(2) or "").strip() or _default_link_title(raw)
        frag = ""
        if "#" in raw:
            raw, _, frag_part = raw.partition("#")
            raw = raw.strip()
            frag = "#" + frag_part.strip()
        if raw.startswith("!"):
            return m.group(0)
        stem = _resolve_target_stem(raw, files, page)
        if not stem:
            return m.group(0)
        target_md = stem + ".md"
        if not any(f.src_path.replace("\\", "/") == target_md for f in files.documentation_pages()):
            return m.group(0)
        return f"[{title}]({_rel_url(cur, target_md)}{frag})"

    return WIKI_LINK.sub(repl, markdown)


def _md_learning_notes_replacer(markdown: str, page, files):
    cur = page.file.src_path.replace("\\", "/")

    def repl(m: re.Match) -> str:
        inner = m.group(1)
        frag = ""
        if "#" in inner:
            path_part, _, rest = inner.partition("#")
            frag = "#" + rest
            inner = path_part
        i = inner.find("learning-notes/")
        if i < 0:
            return m.group(0)
        tail = inner[i + len("learning-notes/") :].lstrip("/")
        if tail.endswith(SOURCE_EXTS):
            tail = str(PurePosixPath(tail).with_suffix(".md"))
        elif not tail.endswith(".md"):
            tail = tail + ".md"
        if not any(f.src_path.replace("\\", "/") == tail for f in files.documentation_pages()):
            return m.group(0)
        return f"]({_rel_url(cur, tail)}{frag})"

    return MD_LEARNING_NOTES.sub(repl, markdown)


def _md_transcript_link_replacer(markdown: str, page, files):
    cur = page.file.src_path.replace("\\", "/")

    def repl(m: re.Match) -> str:
        inner = m.group(1)
        frag = ""
        if "#" in inner:
            path_part, _, rest = inner.partition("#")
            frag = "#" + rest
            inner = path_part
        if not inner.endswith(SOURCE_EXTS):
            return m.group(0)
        md_rel = _resolve_docs_md_path(cur, inner)
        if not md_rel or not any(
            f.src_path.replace("\\", "/") == md_rel for f in files.documentation_pages()
        ):
            return m.group(0)
        return f"]({_rel_url(cur, md_rel)}{frag})"

    return MD_TRANSCRIPT_LINK.sub(repl, markdown)


def on_page_markdown(markdown, page, files, **kwargs):
    if files is None:
        return markdown
    out = _wiki_replacer(markdown, page, files)
    out = _md_learning_notes_replacer(out, page, files)
    out = _md_transcript_link_replacer(out, page, files)
    out = _hard_break_song_lyrics(out, page)
    return out


def _hard_break_song_lyrics(markdown: str, page) -> str:
    """Preserve per-line breaks in english-song lyric blocks on GitHub Pages.

    CommonMark collapses single newlines inside a paragraph; song notes store
    one lyric line per newline. Append Markdown hard-break spaces so MkDocs
    renders each line separately.
    """
    src = getattr(getattr(page, "file", None), "src_path", "") or ""
    src = src.replace("\\", "/")
    if not src.startswith("english-song/"):
        return markdown

    lines = markdown.splitlines(keepends=True)
    out: list[str] = []
    in_lyrics = False

    for line in lines:
        raw = line[:-1] if line.endswith("\n") else line
        newline = "\n" if line.endswith("\n") else ""
        stripped = raw.strip()

        if re.match(r"^##\s+", stripped):
            in_lyrics = bool(re.match(r"^##\s+歌词", stripped))
            out.append(line)
            continue

        if not in_lyrics:
            out.append(line)
            continue

        # Keep structure lines unchanged.
        if (
            not stripped
            or stripped.startswith("#")
            or stripped.startswith(">")
            or stripped.startswith("|")
            or stripped.startswith("```")
            or stripped == "---"
            or stripped.startswith("![")
        ):
            out.append(line)
            continue

        # Already a hard break, or HTML break.
        if raw.rstrip("\r").endswith("  ") or raw.rstrip().endswith("<br>"):
            out.append(line)
            continue

        out.append(raw.rstrip() + "  " + newline)

    return "".join(out)


def _is_section_index_page(node) -> bool:
    """True for folder index/README pages (URL is the section folder itself)."""
    file = getattr(node, "file", None)
    if file is not None:
        name = getattr(file, "name", None) or ""
        src = (
            getattr(file, "src_uri", None)
            or getattr(file, "src_path", None)
            or ""
        ).replace("\\", "/")
        base = Path(src).name if src else name
        if base in ("index.md", "README.md") or name in ("index.md", "README.md"):
            return True
    return False


def _dir_parts_for_leaf(node) -> list[str] | None:
    """Directory path parts for a nav leaf (decoded URL segments)."""
    from urllib.parse import unquote

    url = getattr(node, "url", None) or ""
    parts = [unquote(p) for p in url.strip("/").split("/") if p]
    if not parts:
        return None
    # index.md / README.md URLs point at the folder; keep full path.
    if _is_section_index_page(node):
        return parts
    if len(parts) == 1:
        return parts
    return parts[:-1]


def _collect_dir_prefixes(nodes) -> list[list[str]]:
    """Collect directory prefixes from nav leaves (index-aware)."""
    prefixes: list[list[str]] = []
    for node in nodes or []:
        kids = getattr(node, "children", None)
        if kids:
            prefixes.extend(_collect_dir_prefixes(kids))
            continue
        pref = _dir_parts_for_leaf(node)
        if pref:
            prefixes.append(pref)
    return prefixes


def _section_dir_from_children(item) -> str | None:
    """Infer the docs folder name from a section's page URLs."""
    prefixes = _collect_dir_prefixes(getattr(item, "children", None) or [])
    if not prefixes:
        url = getattr(item, "url", None) or ""
        from urllib.parse import unquote

        parts = [unquote(p) for p in url.strip("/").split("/") if p]
        return parts[-1] if parts else None

    # Prefer the longest shared directory path, but if an index leaf made a
    # shorter prefix (parent folder), use the longest among non-parent-only paths.
    # Example bug without index-aware dirs:
    #   index → [personal-english-book]
    #   page  → [personal-english-book, one-minute-drill]
    #   common → personal-english-book  (wrong section title)
    common = prefixes[0][:]
    for pref in prefixes[1:]:
        i = 0
        while i < len(common) and i < len(pref) and common[i] == pref[i]:
            i += 1
        common = common[:i]
        if not common:
            break
    if not common:
        return None
    return common[-1]


def _rename_nav_sections(items) -> None:
    for item in items or []:
        children = getattr(item, "children", None)
        if children:
            folder = _section_dir_from_children(item)
            if folder:
                # Prefer bilingual / friendly label when configured.
                item.title = _NAV_FOLDER_DISPLAY.get(folder, folder)
            elif getattr(item, "title", None) in _NAV_SECTION_TITLES:
                item.title = _NAV_SECTION_TITLES[item.title]
            _rename_nav_sections(children)
        else:
            title = getattr(item, "title", None)
            if title in _NAV_SECTION_TITLES:
                item.title = _NAV_SECTION_TITLES[title]


# Folder slug (from URL) → left-nav display title (Chinese-first).
_NAV_FOLDER_DISPLAY = {
    "tv-series": "美剧与影视",
    "english-song": "英文歌曲",
    "parenting-english": "亲子英语",
    "personal-english-book": "个人材料书",
    "pronunciation": "发音",
    "grammar-lab": "语法",
    "breakup-loss": "分手·思念",
    "love-romance": "恋爱·浪漫",
    "emotions": "情绪",
    "life-attitude": "生活态度",
    "relationships": "关系",
    "celine-kids": "儿歌·亲子",
    "children-song": "日常儿歌",
    "classic-books-with-holes": "洞洞书跟读",
    "daily-life": "日常生活",
    "communication-patterns": "沟通句式",
    "vocabulary": "词汇",
    "games-and-activities": "游戏与活动",
    "school-life": "校园生活",
    "learning-management": "学习管理",
    "reference-guides": "参考指南",
    "modern-family": "摩登家庭",
    "a-day-in-the-life-of-jeff": "Jeff 的一天",
    "peppa-pig": "小猪佩奇",
    "scripts": "剧本与语料",
    "characters": "人物",
    "s01": "第一季",
    "notes": "笔记",
    "transcript": "字幕",
    "one-minute-drill": "1分钟练习",
    "study": "学习",
    "life": "生活",
    "work": "工作",
    "investing": "投资",
    "mind-body-brain-health": "身心脑健康",
    "vocab-story": "词汇故事",
    "analysis-sentence": "句子分析",
    "50-first-dates": "初恋50次",
    "finding-nemo": "海底总动员",
    "forrest-gump": "阿甘正传",
    "kung-fu-panda": "功夫熊猫",
    "spider-man-into-the-spider-verse": "蜘蛛侠：平行宇宙",
    "the-matrix": "黑客帝国",
    "the-pursuit-of-happyness": "当幸福来敲门",
    "the-shawshank-redemption": "肖申克的救赎",
    "the-truman-show": "楚门的世界",
    "the-wolf-of-wall-street": "华尔街之狼",
    "wall-e": "机器人总动员",
    "zootopia": "疯狂动物城",
}

# Fallback: Material Title Case → Chinese (when folder slug cannot be inferred).
_NAV_SECTION_TITLES = {
    "English song": "英文歌曲",
    "Breakup loss": "分手·思念",
    "Love romance": "恋爱·浪漫",
    "Emotions": "情绪",
    "Life attitude": "生活态度",
    "Relationships": "关系",
    "Celine kids": "儿歌·亲子",
    "Children song": "日常儿歌",
    "Classic books with holes": "洞洞书跟读",
    "Parenting english": "亲子英语",
    "Personal english book": "个人材料书",
    "Grammar lab": "语法",
    "Tv series": "美剧与影视",
    "Communication patterns": "沟通句式",
    "Daily life": "日常生活",
    "Games and activities": "游戏与活动",
    "Learning management": "学习管理",
    "Reference guides": "参考指南",
    "School life": "校园生活",
    "Mind body brain health": "身心脑健康",
    "Vocab story": "词汇故事",
    "A day in the life of jeff": "Jeff 的一天",
    "Modern family": "摩登家庭",
    "Peppa pig": "小猪佩奇",
    "Pronunciation": "发音",
    "Vocabulary": "词汇",
    "Investing": "投资",
    "Life": "生活",
    "Study": "学习",
    "Work": "工作",
    "One minute drill": "1分钟练习",
    "Analysis sentence": "句子分析",
}


def on_nav(nav, config, files, **kwargs):
    _rename_nav_sections(getattr(nav, "items", None) or nav)
    return nav
