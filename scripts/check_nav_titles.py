#!/usr/bin/env python3
"""Fail the GitHub Pages build if a sidebar link is titled None.

MkDocs prints the Python value None when a page was not read, which happens
with ``mkdocs serve --dirty``. A clean ``mkdocs build`` should still be
checked so that title never ships in the published nav.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAV_LINK = re.compile(
    r'<a href="([^"]*)" class="md-nav__link[^"]*">\s*'
    r'<span class="md-ellipsis">\s*(.*?)\s*</span>',
    re.DOTALL,
)
TAG = re.compile(r"<[^>]+>")
WHITESPACE = re.compile(r"\s+")


def visible_title(raw: str) -> str:
    text = TAG.sub("", raw)
    return WHITESPACE.sub(" ", text).strip()


def broken_nav_links(html: str) -> list[tuple[str, str]]:
    broken: list[tuple[str, str]] = []
    for href, raw in NAV_LINK.findall(html):
        title = visible_title(raw)
        if title.lower() == "none":
            broken.append((href, title))
    return broken


def check_site(site_dir: Path) -> list[str]:
    problems: list[str] = []
    pages = sorted(site_dir.rglob("*.html"))
    if not pages:
        return [f"no HTML pages under {site_dir}"]
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="replace")
        for href, title in broken_nav_links(html):
            rel = page.relative_to(site_dir)
            problems.append(f"{rel}: sidebar title {title!r} -> {href}")
    return problems


def main(argv: list[str]) -> int:
    site_dir = Path(argv[1] if len(argv) > 1 else "site")
    if not site_dir.is_dir():
        print(f"site directory not found: {site_dir}", file=sys.stderr)
        print("run mkdocs build first", file=sys.stderr)
        return 2
    problems = check_site(site_dir)
    if problems:
        print(f"sidebar titles failed ({len(problems)}):", file=sys.stderr)
        for line in problems[:40]:
            print(f"  {line}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
        return 1
    print(f"sidebar titles ok ({site_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
