#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse 美剧/摩登家庭 S01/摩登家庭 S01-XX.txt and emit book/摩登家庭/S01EXX-生活实用英文句.md"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TXT_DIR = ROOT / "美剧" / "摩登家庭 S01"
OUT_DIR = ROOT / "book" / "摩登家庭"

def _wb(word: str) -> re.Pattern[str]:
    """Whole-word match (ASCII letters); avoids e.g. 'trip' in 'stripped'."""
    return re.compile(rf"(?i)\b{re.escape(word)}\b")


# Avoid substring traps: "lesbian" contains "plane", "legate" contains "gate".
_RE_PLANE = re.compile(r"(?i)airplane|\bplane\b")
_RE_FLIGHT = re.compile(r"(?i)\bflight\b")

# (section title, list of plain substrings OR compiled whole-word patterns)
BUCKET_RULES: list[tuple[str, list[str | re.Pattern[str]]]] = [
    (
        "出行与旅行",
        [
            _RE_FLIGHT,
            _RE_PLANE,
            "airport",
            _wb("gate"),
            "luggage",
            "boarding pass",
            "board the",
            "hotel",
            _wb("trip"),
            "vacation",
            _wb("drive"),
            _wb("car"),
            "freeway",
            "traffic",
            "parking",
            _wb("taxi"),
            "uber",
            "maui",
            "hawaii",
        ],
    ),
    (
        "家事与居家",
        [
            "garbage",
            "trash",
            "kitchen",
            "upstairs",
            "downstairs",
            "bedroom",
            "dinner",
            "breakfast",
            "laundry",
            "garage",
            _wb("couch"),
            "our house",
            "at home",
            "living room",
        ],
    ),
    (
        "亲子与学校",
        [
            _wb("kids"),
            "school",
            "homework",
            "daughter",
            _wb("son"),
            "baby",
            "parent",
            "teacher",
        ],
    ),
    ("电话与信息", ["text me", "texted", "phone", "a text", "message", "email", "call you"]),
    (
        "工作与职场",
        [
            _wb("office"),
            "meeting",
            "client",
            "business",
            _wb("boss"),
            "my job",
            "at work",
            "realtor",
        ],
    ),
    (
        "约会与恋爱",
        [
            _wb("date"),
            "boyfriend",
            "girlfriend",
            "love you",
            "married",
            "honey",
            "sweetheart",
        ],
    ),
    (
        "情绪与道歉",
        [
            "sorry",
            "worry",
            "upset",
            _wb("mad"),
            "angry",
            "happy",
            "sad",
            "nervous",
            "afraid",
            "freaked",
            "relax",
            "stressed",
            "depressing",
        ],
    ),
    (
        "社交与礼貌",
        [
            "thank you",
            "thanks",
            "please",
            "excuse me",
            "you're welcome",
            "hi,",
            "hey,",
            "hello",
        ],
    ),
    (
        "请求与建议",
        [
            "could you",
            "would you",
            "can you",
            "let's ",
            "why don't",
            "you should",
            "need to",
            "have to",
        ],
    ),
]

SKIP_ENGLISH_RE = re.compile(
    r"^[\d\s\-–—:.,!?'\"]+$|^[A-Z]{1,4}$|^\[|^Music|^♪"
)


def episode_num_from_name(path: Path) -> int:
    m = re.search(r"S01-(\d+)", path.name)
    if not m:
        raise ValueError(path.name)
    return int(m.group(1))


def parse_pairs(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    pairs: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("- "):
            eng = line[2:].strip()
            zh = ""
            if i + 1 < len(lines):
                nxt = lines[i + 1]
                if nxt.strip() and not nxt.startswith("- "):
                    zh = nxt.strip()
                    i += 1
            if eng:
                pairs.append((eng, zh))
        i += 1
    return pairs


def usable(eng: str) -> bool:
    e = eng.strip()
    if len(e) < 6:
        return False
    if not re.search(r"[a-zA-Z]", e):
        return False
    if SKIP_ENGLISH_RE.match(e):
        return False
    # Skip lines that are mostly Spanish etc. if no common English words — keep if has spaces and Latin
    if len(e) > 160:
        return False
    return True


def _key_matches(eng: str, low: str, key: str | re.Pattern[str]) -> bool:
    if isinstance(key, re.Pattern):
        return key.search(eng) is not None
    return key in low


def bucket_for(eng: str) -> str:
    low = eng.lower()
    for name, keys in BUCKET_RULES:
        if any(_key_matches(eng, low, k) for k in keys):
            return name
    return "其它实用表达"


def dedupe_preserve(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for e, z in pairs:
        key = re.sub(r"\s+", " ", e.lower().strip())
        if key in seen:
            continue
        seen.add(key)
        out.append((e, z))
    return out


def format_md(ep: int, pairs: list[tuple[str, str]], empty_reason: str | None = None) -> str:
    title = f"《摩登家庭》S01E{ep:02d} — 生活场景实用英文句"
    rel_txt = f"../../美剧/摩登家庭 S01/摩登家庭 S01-{ep:02d}.txt"
    if empty_reason:
        return f"""# {title}

素材来源：[`美剧/摩登家庭 S01/摩登家庭 S01-{ep:02d}.txt`]({rel_txt})。

{empty_reason}

可在补齐字幕后重新运行 `book/摩登家庭/scripts/build_modern_family_s01_md.py` 生成句子列表。
"""

    header = f"""# {title}

素材来源（英中字幕行）：[`美剧/摩登家庭 S01/摩登家庭 S01-{ep:02d}.txt`]({rel_txt})。

本页由脚本从字幕**抽取可朗读的英文句**并保留对应**简中**；已去重、略去过短行。**语境**（讽刺、玩笑、双关）未逐条标注，朗读前可快速扫一眼中文。

---

"""

    buckets: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for e, z in pairs:
        buckets[bucket_for(e)].append((e, z))

    # Stable section order
    order = [n for n, _ in BUCKET_RULES] + ["其它实用表达"]
    sections: list[str] = []
    for name in order:
        items = buckets.get(name)
        if not items:
            continue
        sections.append(f"## {name}\n\n")
        for e, z in items[:80]:  # cap per section to keep file size reasonable
            if z:
                sections.append(f"- **{e}** — {z}\n")
            else:
                sections.append(f"- **{e}**\n")
        sections.append("\n")

    footer = """---

## 使用提示

- 每集条目较多时，按场景选 **10–15 句** 精读即可，不必一次背完。
- 想对照 **亲子对话体** 练习，见同目录 `S01E02-What's the key to being a great dad.md`（手工编排示例）。

*自动生成：对双关、反话需结合剧集理解；重要场合请再查词典或语料库确认语气。*

"""
    return header + "".join(sections) + footer


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "scripts").mkdir(parents=True, exist_ok=True)

    txt_files = sorted(TXT_DIR.glob("摩登家庭 S01-*.txt"))
    if not txt_files:
        raise SystemExit(f"No txt files in {TXT_DIR}")

    for path in txt_files:
        ep = episode_num_from_name(path)
        raw = path.read_text(encoding="utf-8", errors="replace")
        pairs = parse_pairs(raw)
        pairs = [(e, z) for e, z in pairs if usable(e)]
        pairs = dedupe_preserve(pairs)
        # Global cap: keep file readable
        pairs = pairs[:220]
        if not pairs:
            md = format_md(
                ep,
                [],
                empty_reason="**当前字幕文件为空或仅有标题，暂无可用对白行。**",
            )
        else:
            md = format_md(ep, pairs)
        out_path = OUT_DIR / f"S01E{ep:02d}-生活实用英文句.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"Wrote {out_path.name} ({len(pairs)} pairs)")


if __name__ == "__main__":
    main()
