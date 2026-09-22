#!/usr/bin/env python3
"""Reformat bilingual TV transcripts to english-song style blocks per scene.

Each scene keeps its 【场景】 header, then:

  #### English
  <one cue per line, no leading "- ">

  #### 中文
  <matching Chinese lines>

Usage:
  python reformat_en_zh_song_style.py <transcript.txt>
  python reformat_en_zh_song_style.py --dir <transcript_dir>
  python reformat_en_zh_song_style.py --dir s01/transcript --dir s02/transcript
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SEP = "----------------------"
EN_HEAD = "#### English"
ZH_HEAD = "#### 中文"


def is_scene_meta(line: str) -> bool:
    s = line.strip()
    return (
        s == SEP
        or s.startswith("【场景")
        or s.startswith("★ ")
        or s.startswith("## 场景分段索引")
        or s in {EN_HEAD, ZH_HEAD}
        or (s.startswith("|") and "场景" in s)
    )


def is_english_cue(line: str) -> bool:
    s = line.strip()
    if not s or is_scene_meta(line):
        return False
    if line.startswith("- "):
        return True
    # Already song-style English (ASCII-heavy, not pure Chinese block)
    if s.startswith("####"):
        return False
    # Heuristic: lines that were `- EN` already handled; leftover EN without dash
    # only count when body is still in old format (called from parse after strip).
    return False


def normalize_en(line: str) -> str:
    s = line.rstrip("\n")
    if s.startswith("- "):
        s = s[2:]
    return s.strip()


def normalize_zh(line: str) -> str:
    return line.strip()


def parse_pairs(body_lines: list[str]) -> list[tuple[str, str]]:
    """Parse EN/ZH cues. Supports old `- EN` blocks and song-style #### blocks."""
    ens: list[str] = []
    zhs: list[str] = []
    mode: str | None = None  # "en" | "zh" | None for legacy

    has_song_heads = any(ln.strip() in {EN_HEAD, ZH_HEAD} for ln in body_lines)
    if has_song_heads:
        for line in body_lines:
            s = line.strip()
            if s == EN_HEAD:
                mode = "en"
                continue
            if s == ZH_HEAD:
                mode = "zh"
                continue
            if not s or is_scene_meta(line):
                continue
            if mode == "en":
                ens.append(normalize_en(line) if line.startswith("- ") else s)
            elif mode == "zh":
                zhs.append(normalize_zh(line))
        if len(ens) != len(zhs):
            raise SystemExit(f"EN/ZH count mismatch: EN={len(ens)} ZH={len(zhs)}")
        return list(zip(ens, zhs))

    for line in body_lines:
        if is_scene_meta(line) or not line.strip():
            continue
        if line.startswith("- "):
            ens.append(normalize_en(line))
        else:
            zhs.append(normalize_zh(line))
    if len(ens) != len(zhs):
        raise SystemExit(f"EN/ZH count mismatch: EN={len(ens)} ZH={len(zhs)}")
    return list(zip(ens, zhs))


def find_first_scene(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if line.strip() == SEP and i + 1 < len(lines) and lines[i + 1].strip().startswith(
            "【场景"
        ):
            return i
    raise SystemExit("No scene marker block found")


def split_scenes(lines: list[str]) -> list[tuple[list[str], list[str]]]:
    """Return [(header_lines, body_lines), ...] for each scene."""
    scenes: list[tuple[list[str], list[str]]] = []
    i = 0
    n = len(lines)
    while i < n:
        if not (
            lines[i].strip() == SEP
            and i + 1 < n
            and lines[i + 1].strip().startswith("【场景")
        ):
            i += 1
            continue
        header: list[str] = []
        while i < n:
            header.append(lines[i])
            if len(header) >= 2 and lines[i].strip() == SEP and header[0].strip() == SEP:
                i += 1
                break
            i += 1
        body: list[str] = []
        while i < n:
            if (
                lines[i].strip() == SEP
                and i + 1 < n
                and lines[i + 1].strip().startswith("【场景")
            ):
                break
            body.append(lines[i])
            i += 1
        scenes.append((header, body))
    return scenes


def emit_scene(header: list[str], pairs: list[tuple[str, str]]) -> list[str]:
    missing = [en for en, zh in pairs if not zh.strip()]
    if missing:
        raise SystemExit(f"English line missing Chinese: {missing[0][:70]}")
    out: list[str] = []
    out.extend(header)
    out.append("")
    out.append(EN_HEAD)
    out.append("")
    for en, _zh in pairs:
        out.append(en)
    out.append("")
    out.append(ZH_HEAD)
    out.append("")
    for _en, zh in pairs:
        out.append(zh)
    out.append("")
    return out


def convert(text: str) -> tuple[str, int, int]:
    lines = text.splitlines()
    start = find_first_scene(lines)
    preamble = lines[:start]
    while preamble and not preamble[-1].strip():
        preamble.pop()
    scenes = split_scenes(lines[start:])
    if not scenes:
        raise SystemExit("No scenes parsed")

    out: list[str] = []
    out.extend(preamble)
    out.append("")
    total_en = 0
    for header, body in scenes:
        pairs = parse_pairs(body)
        if not pairs:
            raise SystemExit(
                f"Empty scene after: {header[1] if len(header) > 1 else header}"
            )
        total_en += len(pairs)
        out.extend(emit_scene(header, pairs))

    while out and out[-1] == "":
        out.pop()
    out.append("")
    return "\n".join(out), len(scenes), total_en


def has_dialogue(text: str) -> bool:
    """True if file looks like it has bilingual dialogue worth converting."""
    if "【场景" not in text:
        return False
    if "- " in text:
        return True
    if EN_HEAD in text:
        return True
    return False


def convert_path(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    if not has_dialogue(raw):
        print(f"SKIP empty/no-scenes: {path.name}")
        return
    new, n_scenes, n_pairs = convert(raw)
    path.write_text(new, encoding="utf-8")
    # verify
    lines = new.splitlines()
    start = find_first_scene(lines)
    scenes = split_scenes(lines[start:])
    for header, body in scenes:
        pairs = parse_pairs(body)
        if not pairs:
            title = header[1] if len(header) > 1 else "?"
            raise SystemExit(f"Empty scene after rewrite: {title}")
    print(f"OK: {path.name}: {n_scenes} scenes, {n_pairs} lines")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("transcript", nargs="?", type=Path)
    ap.add_argument(
        "--dir",
        action="append",
        type=Path,
        dest="dirs",
        help="Directory of *-transcript.txt (repeatable)",
    )
    args = ap.parse_args()
    if args.dirs:
        for d in args.dirs:
            files = sorted(d.glob("*-transcript.txt"))
            if not files:
                raise SystemExit(f"No *-transcript.txt in {d}")
            for p in files:
                try:
                    convert_path(p)
                except SystemExit as exc:
                    print(f"FAIL: {p}: {exc}", file=sys.stderr)
                    raise
        return
    if not args.transcript:
        print(__doc__.strip())
        raise SystemExit(2)
    convert_path(args.transcript)


if __name__ == "__main__":
    main()
