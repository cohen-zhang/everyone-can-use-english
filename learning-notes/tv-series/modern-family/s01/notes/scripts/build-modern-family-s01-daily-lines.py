#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Modern Family S01 daily-lines notes from:
  - beats/s01eNN-beats.yaml  (剧情分段台词)
  - transcript/modern-family-s01eNN-transcript.txt
  - scripts/modern-family-slang-patterns.yaml (本集俚语扫描)

Preserves manual blocks in existing notes between:
  <!-- MANUAL:HEAD --> ... <!-- /MANUAL:HEAD -->
  <!-- MANUAL:VOCAB --> ... <!-- /MANUAL:VOCAB -->
  <!-- MANUAL:TIPS --> ... <!-- /MANUAL:TIPS -->

Usage:
  python3 build-modern-family-s01-daily-lines.py --episode 1
  python3 build-modern-family-s01-daily-lines.py --all
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

NOTES_DIR = Path(__file__).resolve().parent.parent
TRANSCRIPT_DIR = NOTES_DIR.parent / "transcript"
BEATS_DIR = NOTES_DIR / "beats"
SLANG_YAML = Path(__file__).resolve().parent / "modern-family-slang-patterns.yaml"


def parse_transcript_pairs(text: str) -> list[tuple[str, str]]:
    ens: list[str] = []
    zhs: list[str] = []
    started = False
    for line in text.splitlines():
        if line.startswith("- "):
            started = True
            ens.append(line[2:].strip())
            continue
        if not started:
            continue
        s = line.strip()
        if (
            not s
            or s == "----------------------"
            or s.startswith("【场景")
            or s.startswith("★ ")
            or s.startswith("#")
            or s.startswith("|")
        ):
            continue
        zhs.append(s)
    if ens and len(ens) != len(zhs):
        raise SystemExit(f"transcript EN/ZH mismatch: EN={len(ens)} ZH={len(zhs)}")
    return list(zip(ens, zhs))


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def find_slang_hits(transcript: str, patterns_cfg: dict) -> dict[str, list[dict]]:
    hits: dict[str, list[dict]] = {
        "catchphrase": [],
        "slang_tone": [],
        "meme_pragmatic": [],
    }
    for cat_key, cat in patterns_cfg.get("categories", {}).items():
        for item in cat.get("items", []):
            pat = re.compile(item["pattern"])
            examples: list[str] = []
            for line in transcript.splitlines():
                if line.startswith("- ") and pat.search(line):
                    examples.append(line[2:].strip())
            if examples:
                entry = {**item, "examples": examples[:3]}
                hits[cat_key].append(entry)
    return hits


def format_plot_beats(beats_data: dict) -> str:
    out: list[str] = [
        "## 剧情分段台词（Plot beats）\n\n",
        "> 按 **叙事线** 分段，非关键词生活桶。每段 8–15 句；口头禅详见下节 **俚语表**（剧情段不重复罗列）。\n\n",
    ]
    for beat in beats_data.get("beats", []):
        out.append(f"### {beat['title']}\n\n")
        if beat.get("scene_note"):
            out.append(f"*{beat['scene_note']}*\n\n")
        for line in beat.get("lines", []):
            en = line["en"]
            zh = line.get("zh", "")
            out.append(f"- **{en}** — {zh}\n")
        out.append("\n")
    return "".join(out)


def format_slang_tables(hits: dict[str, list[dict]], patterns_cfg: dict) -> str:
    out: list[str] = [
        "## 俚语 · 口头禅 · 口头梗（本集）\n\n",
        "> 仅列 **本集 transcript 实际出现** 的表达；与文末 **难词表（词汇）** 区分。\n\n",
        "### 分类说明\n\n",
        "| 类型 | 英文标签 | 记什么 | 位置 |\n",
        "| --- | --- | --- | --- |\n",
        "| **词汇** | vocabulary | 可查词典的单词 | 文末 **难词表** |\n",
        "| **高频口头禅** | catchphrase | 独立情绪/催促句 | §A |\n",
        "| **俚语感** | slang tone | 粗口强化、评价 | §B |\n",
        "| **口头梗** | meme / pragmatic | 固定搭配、语用梗 | §C |\n\n",
        "---\n\n",
    ]
    for cat_key in ("catchphrase", "slang_tone", "meme_pragmatic"):
        items = hits.get(cat_key, [])
        if not items:
            continue
        cat = patterns_cfg["categories"][cat_key]
        out.append(f"### {cat['label']}\n\n")
        out.append(
            "| 表达 | IPA（美） | 简中 | 语气 / 用法 | 本集台词示例 | 扩展 / 更礼貌 |\n"
        )
        out.append("| --- | --- | --- | --- | --- | --- |\n")
        for item in items:
            ex = " / ".join(f"*{e}*" for e in item.get("examples", [])[:2])
            out.append(
                f"| **{item['head']}** | {item.get('ipa', '')} | {item.get('zh', '')} | "
                f"{item.get('usage', '')} | {ex} | {item.get('polite', '')} |\n"
            )
        out.append("\n---\n\n")
    return "".join(out)


def extract_manual_block(text: str, name: str) -> str | None:
    m = re.search(
        rf"<!-- MANUAL:{name} -->(.*?)<!-- /MANUAL:{name} -->",
        text,
        re.DOTALL,
    )
    return m.group(1).strip() if m else None


def default_manual_head(ep: int) -> str:
    return f"""
## 本集剧情简介

（在此填写剧情简介与关键词 — `<!-- MANUAL:HEAD -->` 区块）

**English version:** …

### 剧情关键词

- …

本页结构：**剧情分段** → **俚语表（本集）** → **难词表（词汇）**。台词源：[[learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e{ep:02d}-transcript.txt|S01E{ep:02d} 字幕全文]]。
"""


def build_episode(ep: int, patterns_cfg: dict, dry_run: bool = False) -> None:
    beats_path = BEATS_DIR / f"s01e{ep:02d}-beats.yaml"
    transcript_path = TRANSCRIPT_DIR / f"modern-family-s01e{ep:02d}-transcript.txt"
    out_path = NOTES_DIR / f"modern-family-s01e{ep:02d}-daily-lines.md"

    if not beats_path.exists():
        print(f"Skip E{ep:02d}: no beats file {beats_path.name}")
        return
    if not transcript_path.exists():
        print(f"Skip E{ep:02d}: no transcript")
        return

    beats_data = load_yaml(beats_path)
    transcript = transcript_path.read_text(encoding="utf-8", errors="replace")
    hits = find_slang_hits(transcript, patterns_cfg)

    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    manual_head = extract_manual_block(existing, "HEAD") or default_manual_head(ep)
    manual_vocab = extract_manual_block(existing, "VOCAB")
    manual_tips = extract_manual_block(existing, "TIPS")

    title = f"# 《摩登家庭》S01E{ep:02d} — 生活场景实用英文句"
    header = f"""{title}

素材来源：`[modern-family-s01e{ep:02d}-transcript.txt](../transcript/modern-family-s01e{ep:02d}-transcript.txt)`。

**Obsidian：** [[learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e{ep:02d}-transcript.txt|S01E{ep:02d} 字幕全文]] · [[learning-notes/tv-series/modern-family/s01/notes/README.md|S01 notes 索引]] · 分段配置：[[learning-notes/tv-series/modern-family/s01/notes/beats/s01e{ep:02d}-beats.yaml|s01e{ep:02d}-beats.yaml]]

<!-- MANUAL:HEAD -->
{manual_head}
<!-- /MANUAL:HEAD -->

---

"""

    body = format_plot_beats(beats_data) + "\n---\n\n" + format_slang_tables(hits, patterns_cfg)

    vocab_section = ""
    if manual_vocab:
        vocab_section = f"""
## 难词表（词汇 · Vocabulary）

<!-- MANUAL:VOCAB -->
{manual_vocab}
<!-- /MANUAL:VOCAB -->
"""
    else:
        vocab_section = """
## 难词表（词汇 · Vocabulary）

<!-- MANUAL:VOCAB -->
*（在此维护本集词汇表 — 不含口头禅；见 `subtitle-vocabulary-tables` 规范）*

| Word | IPA (GA) | 简中义项 | 标签 |
| --- | --- | --- | --- |
<!-- /MANUAL:VOCAB -->
"""

    if manual_tips:
        tips = f"""
## 使用提示

<!-- MANUAL:TIPS -->
{manual_tips}
<!-- /MANUAL:TIPS -->
"""
    else:
        tips = """
## 使用提示

<!-- MANUAL:TIPS -->
- 每集精读 **1 个剧情段**（8–15 句）+ **俚语表** + **5–10 个难词** 即可。
- **背诵顺序：** 剧情段 → §A 口头禅 → §C 口头梗 → 难词表。
- 更新台词：改 `beats/s01eNN-beats.yaml` 后重跑本脚本；**MANUAL** 区块不会被覆盖。
<!-- /MANUAL:TIPS -->
"""

    full = header + body + vocab_section + tips + "\n"

    if dry_run:
        print(f"Would write {out_path.name} ({len(full)} chars)")
        return
    out_path.write_text(full, encoding="utf-8")
    print(f"Wrote {out_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=int, help="Episode number 1-24")
    parser.add_argument("--all", action="store_true", help="All episodes with beats yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    patterns_cfg = load_yaml(SLANG_YAML)

    if args.all:
        for p in sorted(BEATS_DIR.glob("s01e*-beats.yaml")):
            m = re.search(r"s01e(\d+)-beats", p.name)
            if m:
                build_episode(int(m.group(1)), patterns_cfg, args.dry_run)
    elif args.episode:
        build_episode(args.episode, patterns_cfg, args.dry_run)
    else:
        parser.error("Specify --episode N or --all")


if __name__ == "__main__":
    main()
