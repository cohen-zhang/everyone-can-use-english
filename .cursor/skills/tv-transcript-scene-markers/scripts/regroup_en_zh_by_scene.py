#!/usr/bin/env python3
"""Regroup bilingual TV transcripts: per scene, all English then all Chinese.

Usage:
  python regroup_en_zh_by_scene.py <transcript.txt>
  python regroup_en_zh_by_scene.py --dir <transcript_dir>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SEP = "----------------------"


def is_scene_meta(line: str) -> bool:
    s = line.strip()
    return (
        s == SEP
        or s.startswith("【场景")
        or s.startswith("★ ")
        or s.startswith("## 场景分段索引")
        or (s.startswith("|") and "场景" in s)
    )


def parse_pairs(body_lines: list[str]) -> list[tuple[str, str]]:
    """Parse `- EN` / ZH lines. Works for interleaved or EN-block-then-ZH-block."""
    ens: list[str] = []
    zhs: list[str] = []
    for line in body_lines:
        if is_scene_meta(line) or not line.strip():
            continue
        if line.startswith("- "):
            ens.append(line)
        else:
            zhs.append(line)
    if len(ens) != len(zhs):
        raise SystemExit(f"EN/ZH count mismatch: EN={len(ens)} ZH={len(zhs)}")
    return list(zip(ens, zhs))


def find_first_scene(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if line.strip() == SEP and i + 1 < len(lines) and lines[i + 1].strip().startswith("【场景"):
            return i
    raise SystemExit("No scene marker block found")


def split_scenes(lines: list[str]) -> list[tuple[list[str], list[str]]]:
    """Return [(header_lines, body_lines), ...] for each scene."""
    scenes: list[tuple[list[str], list[str]]] = []
    i = 0
    n = len(lines)
    while i < n:
        if not (lines[i].strip() == SEP and i + 1 < n and lines[i + 1].strip().startswith("【场景")):
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
            if lines[i].strip() == SEP and i + 1 < n and lines[i + 1].strip().startswith("【场景"):
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
    for en, _zh in pairs:
        out.append(en)
        out.append("")
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
            raise SystemExit(f"Empty scene after: {header[1] if len(header) > 1 else header}")
        total_en += len(pairs)
        out.extend(emit_scene(header, pairs))

    while out and out[-1] == "":
        out.pop()
    out.append("")
    return "\n".join(out), len(scenes), total_en


def convert_path(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    new, n_scenes, n_pairs = convert(raw)
    path.write_text(new, encoding="utf-8")
    # verify zip counts in output
    lines = new.splitlines()
    start = find_first_scene(lines)
    scenes = split_scenes(lines[start:])
    for header, body in scenes:
        ens = [ln for ln in body if ln.startswith("- ")]
        zhs = [
            ln
            for ln in body
            if ln.strip()
            and not ln.startswith("- ")
            and not is_scene_meta(ln)
        ]
        if len(ens) != len(zhs):
            title = header[1] if len(header) > 1 else "?"
            raise SystemExit(f"Count mismatch in {title}: EN={len(ens)} ZH={len(zhs)}")
    print(f"OK: {path.name}: {n_scenes} scenes, {n_pairs} lines")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript", nargs="?", type=Path)
    ap.add_argument("--dir", type=Path)
    args = ap.parse_args()
    if args.dir:
        files = sorted(args.dir.glob("*-transcript.txt"))
        if not files:
            raise SystemExit(f"No *-transcript.txt in {args.dir}")
        for p in files:
            text = p.read_text(encoding="utf-8")
            if "- " not in text:
                print(f"SKIP empty: {p.name}")
                continue
            convert_path(p)
        return
    if not args.transcript:
        print(__doc__.strip())
        raise SystemExit(2)
    convert_path(args.transcript)


if __name__ == "__main__":
    main()
