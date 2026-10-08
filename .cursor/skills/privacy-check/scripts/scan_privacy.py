#!/usr/bin/env python3
"""Flag high-confidence privacy patterns in a git diff or given files.

Does not judge Chinese personal names, school names, or company names.
The agent still reads the diff for those.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "national-id",
        re.compile(
            r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)"
        ),
    ),
    (
        "card-number",
        re.compile(r"(?<!\d)(?:\d[ -]?){15,18}\d(?!\d)"),
    ),
    (
        "mobile",
        re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    ),
    (
        "email",
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ),
    (
        "class-id",
        re.compile(r"[一二三四五六七八九十\d]{1,3}\s*[（(]\s*\d{1,2}\s*[）)]\s*班"),
    ),
]

SKIP_PARTS = {
    ".git",
    "privacy-check",
}


def diff_text() -> str:
    chunks: list[str] = []
    for args in (
        ["git", "diff", "--cached", "--no-ext-diff", "-U0"],
        ["git", "diff", "--no-ext-diff", "-U0"],
    ):
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr.strip() or "git diff failed", file=sys.stderr)
            sys.exit(2)
        chunks.append(result.stdout)
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if untracked.returncode != 0:
        print(untracked.stderr.strip() or "git ls-files failed", file=sys.stderr)
        sys.exit(2)
    for rel in untracked.stdout.splitlines():
        path = ROOT / rel
        if not path.is_file() or _skip(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        body = "\n".join(f"+{line}" for line in text.splitlines())
        chunks.append(f"diff --git a/{rel} b/{rel}\n--- /dev/null\n+++ b/{rel}\n{body}")
    return "\n".join(chunks)


def _skip(path: Path) -> bool:
    return bool(set(path.parts) & SKIP_PARTS)


def added_lines(diff: str) -> list[tuple[str, str]]:
    file = ""
    rows: list[tuple[str, str]] = []
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            file = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            rows.append((file or "(diff)", line[1:]))
    return rows


def main() -> int:
    if len(sys.argv) > 1:
        rows: list[tuple[str, str]] = []
        for arg in sys.argv[1:]:
            path = Path(arg)
            if _skip(path):
                continue
            text = path.read_text(encoding="utf-8")
            rows.extend((str(path), line) for line in text.splitlines())
    else:
        rows = added_lines(diff_text())

    hits = 0
    for file, line in rows:
        if "privacy-check" in file.replace("\\", "/"):
            continue
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                hits += 1
                print(f"{kind}\t{file}")
                break
    if hits:
        print(f"{hits} privacy pattern hit(s). Do not commit.", file=sys.stderr)
        return 1
    print("no pattern hits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
