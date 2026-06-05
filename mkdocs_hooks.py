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


def on_config(config, **kwargs):
    global _stem_to_paths, _repo_root, _docs_dir
    _stem_to_paths = None
    _repo_root = Path(config.config_file_path).resolve().parent
    _docs_dir = Path(config.docs_dir)
    if not _docs_dir.is_absolute():
        _docs_dir = _repo_root / _docs_dir
    _mirror_book_into_docs(_docs_dir, _repo_root)
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


def _resolve_target_stem(slug: str, files, page) -> str | None:
    """Return path stem relative to docs_dir (no .md), or None."""
    s = _strip_docs_prefix(slug)
    if not s:
        return None
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
        if not tail.endswith(".md"):
            tail = tail + ".md"
        if not any(f.src_path.replace("\\", "/") == tail for f in files.documentation_pages()):
            return m.group(0)
        return f"]({_rel_url(cur, tail)}{frag})"

    return MD_LEARNING_NOTES.sub(repl, markdown)


def on_page_markdown(markdown, page, files, **kwargs):
    if files is None:
        return markdown
    out = _wiki_replacer(markdown, page, files)
    out = _md_learning_notes_replacer(out, page, files)
    return out
