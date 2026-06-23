"""MkDocs hooks: Obsidian-style wikilinks + vault-root paths → normal Markdown (docs_dir = learning-notes/)."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path, PurePosixPath

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


def _mirror_book_into_docs(docs_dir: Path, repo_root: Path) -> None:
    """Mirror repo ``book/`` into ``learning-notes/book/`` so GHP can serve 人人都能用英语."""
    src = repo_root / "book"
    target = docs_dir / "book"
    if not src.is_dir():
        return
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target)


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


def _generate_transcript_md_pages(docs_dir: Path) -> None:
    """Build companion ``.md`` pages for ``transcript/`` ``.txt`` and ``.yaml`` sources."""
    for transcript_dir in docs_dir.rglob("transcript"):
        if not transcript_dir.is_dir():
            continue
        _cleanup_generated_transcript_pages(transcript_dir)

        for txt_path in sorted(transcript_dir.glob("*-transcript.txt")):
            body = txt_path.read_text(encoding="utf-8", errors="replace")
            label = _episode_label_from_name(txt_path.name)
            md_path = txt_path.with_suffix(".md")
            md_path.write_text(
                f"# {label} 字幕全文\n\n"
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
    global _stem_to_paths, _repo_root, _docs_dir
    _stem_to_paths = None
    _repo_root = Path(config.config_file_path).resolve().parent
    _docs_dir = Path(config.docs_dir)
    if not _docs_dir.is_absolute():
        _docs_dir = _repo_root / _docs_dir
    _mirror_book_into_docs(_docs_dir, _repo_root)
    _generate_transcript_md_pages(_docs_dir)
    return config


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
        title = (m.group(2) or "").strip() or PurePosixPath(raw.replace("\\", "/")).name
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
    return out
