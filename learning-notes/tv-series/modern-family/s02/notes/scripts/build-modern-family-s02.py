#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ingest Modern Family S02 bilingual source and emit transcripts + daily-lines.

Usage (from repo root):
  python3 learning-notes/tv-series/modern-family/s02/notes/scripts/build-modern-family-s02.py \\
    --source .tmp-mf-src/S2.txt --all
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

S02_ROOT = Path(__file__).resolve().parents[2]
MF_ROOT = S02_ROOT.parent
TRANSCRIPT_DIR = S02_ROOT / "transcript"
NOTES_DIR = S02_ROOT / "notes"
TITLES_PATH = S02_ROOT / "episode-titles.yaml"
S01_BUILD = MF_ROOT / "s01" / "notes" / "scripts" / "build-modern-family-s01-md.py"

EP_HEADER = re.compile(r"^S02E(\d{2})\s*$")
APPENDIX_START = re.compile(r"^(附录|作者：)")


def _load_s01_mod():
    spec = importlib.util.spec_from_file_location("mf_s01_md", S01_BUILD)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {S01_BUILD}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_titles() -> dict[int, dict]:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(TITLES_PATH.read_text(encoding="utf-8")) or {}
    return {int(k): v for k, v in (data.get("episodes") or {}).items()}


def split_source(text: str) -> dict[int, str]:
    episodes: dict[int, list[str]] = {}
    current: int | None = None
    for line in text.splitlines(keepends=True):
        m = EP_HEADER.match(line.rstrip("\n"))
        if m:
            current = int(m.group(1))
            episodes[current] = []
            continue
        if current is None:
            continue
        stripped = line.strip()
        if stripped == "---" or APPENDIX_START.match(stripped):
            current = None
            continue
        episodes[current].append(line)
    return {ep: "".join(lines) for ep, lines in episodes.items()}


def transcript_header(ep: int) -> str:
    return (
        "Obsidian 互链（生活场景句 · 笔记）："
        f"[[learning-notes/tv-series/modern-family/s02/notes/modern-family-s02e{ep:02d}-daily-lines.md|"
        f"S02E{ep:02d} 生活场景实用英文句]]\n"
        "本目录索引：[[learning-notes/tv-series/modern-family/s02/transcript/README.md|S02 transcript README]]\n"
        f"\nS02E{ep:02d}\n\n"
    )


def write_transcripts(source: Path) -> dict[int, str]:
    raw = source.read_text(encoding="utf-8", errors="replace")
    bodies = split_source(raw)
    if not bodies:
        raise SystemExit(f"No S02Exx markers in {source}")
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    out: dict[int, str] = {}
    for ep, body in sorted(bodies.items()):
        text = transcript_header(ep) + body.lstrip("\n")
        if not text.endswith("\n"):
            text += "\n"
        path = TRANSCRIPT_DIR / f"modern-family-s02e{ep:02d}-transcript.txt"
        path.write_text(text, encoding="utf-8")
        out[ep] = text
        print(f"Wrote {path} ({len(text)} chars)")
    return out


def keyword_block(meta: dict) -> str:
    lines = []
    for item in meta.get("keywords") or []:
        if " — " in item:
            en, zh = item.split(" — ", 1)
            lines.append(f"- **{en.strip()}** — {zh.strip()}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def format_daily_lines(mod, ep: int, meta: dict, pairs: list[tuple[str, str]]) -> str:
    theme = meta.get("theme") or ""
    title = f"# 《摩登家庭》S02E{ep:02d} — 生活场景实用英文句"
    plot_zh = (meta.get("plot_zh") or "").strip()
    plot_en = (meta.get("plot_en") or "").strip()
    keys = keyword_block(meta)
    buckets: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for e, z in pairs:
        buckets[mod.bucket_for(e)].append((e, z))
    order = [n for n, _ in mod.BUCKET_RULES] + ["其它实用表达"]
    sections: list[str] = []
    for name in order:
        items = buckets.get(name)
        if not items:
            continue
        sections.append(f"## {name}\n\n")
        for e, z in items[:80]:
            if z:
                sections.append(f"- **{e}** — {z}\n")
            else:
                sections.append(f"- **{e}**\n")
        sections.append("\n")
    return f"""{title}

素材来源（英中字幕行）：[`modern-family-s02e{ep:02d}-transcript.txt`](../transcript/modern-family-s02e{ep:02d}-transcript.txt)。

**Obsidian（全台词 · 相向）：** [[learning-notes/tv-series/modern-family/s02/transcript/modern-family-s02e{ep:02d}-transcript.txt|S02E{ep:02d} 字幕全文]] · [[learning-notes/tv-series/modern-family/s02/transcript/README.md|S02 字幕目录]]

## 本集剧情简介

{plot_zh}

**English version:** {plot_en}

### 剧情关键词

{keys}

本页由脚本从字幕**抽取可朗读的英文句**并保留对应**简中**；已去重、略去过短行。**语境**（讽刺、玩笑、双关）未逐条标注，朗读前可快速扫一眼中文。主题：{theme}。

---

{"".join(sections)}---

## 使用提示

- 每集条目较多时，按场景选 **10–15 句** 精读即可，不必一次背完。
- 重跑本页：`s02/notes/scripts/build-modern-family-s02.py --notes`。
- 第一季对照：[[learning-notes/tv-series/modern-family/s01/notes/README|S01 notes 索引]]。

*自动生成：对双关、反话需结合剧集理解；重要场合请再查词典或语料库确认语气。*
"""


def write_notes(mod, titles: dict[int, dict], transcripts: dict[int, str] | None = None) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    episodes = sorted(titles) if transcripts is None else sorted(transcripts)
    if transcripts is None:
        episodes = []
        for path in sorted(TRANSCRIPT_DIR.glob("modern-family-s02e*-transcript.txt")):
            m = re.search(r"s02e(\d+)", path.name, re.I)
            if m:
                episodes.append(int(m.group(1)))
    for ep in episodes:
        path = TRANSCRIPT_DIR / f"modern-family-s02e{ep:02d}-transcript.txt"
        raw = transcripts[ep] if transcripts and ep in transcripts else path.read_text(
            encoding="utf-8", errors="replace"
        )
        pairs = mod.parse_pairs(raw)
        pairs = [(e, z) for e, z in pairs if mod.usable(e)]
        pairs = mod.dedupe_preserve(pairs)[:220]
        meta = titles.get(ep) or {}
        md = format_daily_lines(mod, ep, meta, pairs)
        out = NOTES_DIR / f"modern-family-s02e{ep:02d}-daily-lines.md"
        out.write_text(md, encoding="utf-8")
        print(f"Wrote {out.name} ({len(pairs)} pairs)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Combined S2.txt with S02Exx markers")
    parser.add_argument("--ingest", action="store_true", help="Split source into transcript/*.txt")
    parser.add_argument("--notes", action="store_true", help="Build notes/*-daily-lines.md")
    parser.add_argument("--all", action="store_true", help="Ingest (if --source) + notes")
    args = parser.parse_args()
    if args.all:
        args.ingest = bool(args.source)
        args.notes = True
    if not args.ingest and not args.notes:
        parser.error("Specify --ingest, --notes, or --all")
    if args.ingest and not args.source:
        parser.error("--ingest requires --source")

    titles = load_titles()
    mod = _load_s01_mod()
    transcripts = None
    if args.ingest:
        transcripts = write_transcripts(args.source)
        for ep, text in transcripts.items():
            try:
                pairs = mod.parse_pairs(text)
            except SystemExit as exc:
                raise SystemExit(f"S02E{ep:02d}: {exc}") from exc
            print(f"  S02E{ep:02d} EN/ZH pairs: {len(pairs)}")
    if args.notes:
        write_notes(mod, titles, transcripts)


if __name__ == "__main__":
    main()
