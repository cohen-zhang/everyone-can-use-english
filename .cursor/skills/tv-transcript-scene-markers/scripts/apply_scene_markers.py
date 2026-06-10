#!/usr/bin/env python3
"""Insert TV transcript scene markers between complete EN/ZH subtitle blocks.

Usage:
  python apply_scene_markers.py <transcript.txt> <scenes.yaml>

Exits 1 if any anchor is missing or if a scene marker would split an EN/ZH pair.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def norm_en(line: str) -> str:
    s = line.strip()
    if s.startswith("- "):
        s = s[2:]
    return re.sub(r"\s+", " ", s).strip()


def is_scene_line(line: str) -> bool:
    s = line.strip()
    return (
        s == "----------------------"
        or s.startswith("【场景")
        or s.startswith("★ ")
        or s.startswith("## 场景分段索引")
        or (s.startswith("|") and "场景" in s)
    )


def parse_blocks(body_lines: list[str]) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        if is_scene_line(line) or not line.strip():
            i += 1
            continue
        if line.startswith("- "):
            en = line.rstrip("\n")
            zh = ""
            if (
                i + 1 < len(body_lines)
                and body_lines[i + 1].strip()
                and not body_lines[i + 1].startswith("- ")
                and not is_scene_line(body_lines[i + 1])
            ):
                zh = body_lines[i + 1].rstrip("\n")
                i += 2
            else:
                i += 1
            blocks.append((en, zh))
            continue
        if blocks and not blocks[-1][1] and line.strip():
            blocks[-1] = (blocks[-1][0], line.rstrip("\n"))
        i += 1
    return blocks


def scene_header(scene: dict, total: str) -> list[str]:
    return [
        "----------------------",
        f"【场景 {scene['id']} / {total}】{scene['place']}",
        f"★ 剧情：{scene['plot']}",
        f"★ 人物：{scene['characters']}",
        f"★ 时间线：{scene['timeline']}",
        "----------------------",
    ]


def build_index(cfg: dict) -> list[str]:
    episode = cfg.get("episode", "")
    arc = cfg.get("episode_arc", "")
    note = cfg.get("timeline_note", "")
    total = len(cfg["scenes"])
    lines = [
        f"## 场景分段索引（{episode} · {arc}）",
        "",
        f"字幕正文按镜头插入 `【场景 xx / {total}】`；{note}。",
        "",
        "| 场景 | 地点 | 剧情要点 |",
        "| ---: | --- | --- |",
    ]
    for row in cfg.get("index_groups", []):
        lines.append(
            f"| {row['scenes']} | {row['place']} | {row['summary']} |"
        )
    lines.append("")
    return lines


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def extract_header(all_lines: list[str], body_start: int) -> list[str]:
    """Keep wikilinks + episode label only; drop any prior scene index table."""
    header: list[str] = []
    in_index = False
    for i in range(body_start):
        line = all_lines[i]
        stripped = line.strip()
        if stripped.startswith("## 场景分段索引"):
            in_index = True
            continue
        if in_index:
            # index = heading + blanks + intro line + markdown table rows
            if stripped.startswith("|") or stripped == "":
                continue
            if "字幕正文按镜头插入" in stripped:
                continue
            in_index = False
        if is_scene_line(line):
            continue
        if stripped.startswith("|"):
            continue
        if "字幕正文按镜头插入" in stripped and "##" not in stripped:
            continue
        header.append(line.rstrip("\n"))
    while header and not header[-1].strip():
        header.pop()
    return header


def find_body_start(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if line.startswith("- ") and i > 3:
            return i
    raise SystemExit("No subtitle blocks found (- English lines)")


def apply(transcript_path: Path, config_path: Path) -> None:
    cfg = load_yaml(config_path)
    scenes = cfg["scenes"]
    total = str(len(scenes))
    anchors = [norm_en(s["anchor"]) if not s["anchor"].startswith("-") else norm_en(s["anchor"]) for s in scenes]
    # anchors in yaml are without leading "-"
    anchors = [re.sub(r"\s+", " ", a.strip()) for a in anchors]

    raw = transcript_path.read_text(encoding="utf-8")
    all_lines = raw.splitlines(keepends=True)
    body_start = find_body_start(all_lines)

    header = extract_header(all_lines, body_start)
    body_lines = all_lines[body_start:]
    blocks = parse_blocks([l.rstrip("\n") for l in body_lines])

    def matches_anchor(en_n: str, anchor: str) -> bool:
        if en_n == anchor:
            return True
        if en_n.startswith(anchor):
            return True
        # subtitle lines with leading space after "-"
        if en_n.lstrip() == anchor.lstrip():
            return True
        return False

    scene_at = [None] * len(blocks)
    ai = 0
    for bi, (en, _zh) in enumerate(blocks):
        en_n = norm_en(en)
        if ai >= len(anchors):
            break
        if matches_anchor(en_n, anchors[ai]):
            scene_at[bi] = ai
            ai += 1

    if ai < len(anchors):
        missing = anchors[ai:]
        raise SystemExit(f"Anchors not found ({len(anchors) - ai}): {missing[:3]}...")

    out: list[str] = []
    out.extend(header)
    out.append("")
    out.extend(build_index(cfg))

    for bi, (en, zh) in enumerate(blocks):
        if scene_at[bi] is not None:
            out.extend(scene_header(scenes[scene_at[bi]], total))
        out.append(en)
        if zh:
            out.append(zh)
        out.append("")

    while out and out[-1] == "":
        out.pop()
    out.append("")

    result = "\n".join(out)
    transcript_path.write_text(result, encoding="utf-8")

    # validate split pairs
    result_lines = result.splitlines()
    splits = []
    for i, line in enumerate(result_lines):
        if line.startswith("- ") and i + 1 < len(result_lines):
            nxt = result_lines[i + 1].strip()
            if nxt.startswith("----------------------") or nxt.startswith("【场景"):
                splits.append(line[:70])
    if splits:
        raise SystemExit(f"Split EN/ZH pairs: {len(splits)} e.g. {splits[0]}")
    print(f"OK: {len(blocks)} blocks, {len(scenes)} scenes, 0 split pairs")


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        raise SystemExit(2)
    apply(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
