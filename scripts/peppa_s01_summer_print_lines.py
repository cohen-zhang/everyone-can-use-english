#!/usr/bin/env python3
"""Extract 15–25 print-friendly dialogue lines per Peppa S01 episode (E01–E45)."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EP_DIR = REPO / "learning-notes/tv-series/Peppa Pig S01.英文剧本"
OUT_DIR = REPO / "learning-notes/parenting-english/learning-management/summer-60d-print"
OUT_FILE = OUT_DIR / "peppa-s01-e01-e45-print-lines.md"

EPISODE_TITLES = {
    1: "Muddy Puddles",
    2: "Mr. Dinosaur is Lost",
    3: "Polly Parrot",
    4: "Best Friend",
    5: "Hide and Seek",
    6: "The Playgroup",
    7: "Mummy Pig at Work",
    8: "Camping",
    9: "Gardening",
    10: "Bicycles",
    11: "The New Car",
    12: "Snow",
    13: "Flying a Kite",
    14: "My Cousin Chloe",
    15: "Daddy Loses his Glasses",
    16: "Hiccups",
    17: "Picnic",
    18: "Mummy Pig's Birthday",
    19: "Dressing Up",
    20: "The School Fete",
    21: "Musical Instruments",
    22: "Babysitting",
    23: "New Shoes",
    24: "Ballet Lesson",
    25: "The Tooth Fairy",
    26: "Treasure Hunt",
    27: "Not Very Well",
    28: "Windy Castle",
    29: "Pancakes",
    30: "The Museum",
    31: "Secrets",
    32: "Thunderstorm",
    33: "Piggy in the Middle",
    34: "Fancy Dress Party",
    35: "Very Hot Day",
    36: "Mister Skinnylegs",
    37: "Lunch",
    38: "Sleepy Princess",
    39: "The Tree House",
    40: "Daddy Gets Fit",
    41: "Shopping",
    42: "Chloe's puppet show",
    43: "My Birthday Party",
    44: "The Playground",
    45: "Tidying Up",
}

# Shared intro / high-frequency lines (mom reference gloss)
GLOSS = {
    "I'm Peppa Pig.": "我是 Peppa Pig。",
    "This is my little brother, George.": "这是我的弟弟 George。",
    "This is Mummy Pig.": "这是猪妈妈。",
    "And this is Daddy Pig.": "这是猪爸爸。",
    "Come on, George.": "来吧，George。",
    "Yes, Daddy.": "好的，爸爸。",
    "No, Daddy.": "不，爸爸。",
    "Sorry, Mummy.": "对不起，妈妈。",
    "Thank you, Mummy.": "谢谢你，妈妈。",
    "Thank you, Daddy.": "谢谢你，爸爸。",
    "Let's go.": "我们走吧。",
    "Are you ready?": "你准备好了吗？",
    "I love muddy puddles.": "我喜欢泥坑。",
    "It's only mud.": "只是泥而已。",
    "Let me think...": "让我想想……",
    "Goodness me.": "天哪。",
    "Ho. Ho.": "呵呵。",
    "Oh, dear.": "哎呀。",
    "Oh, well.": "哦，好吧。",
    "Can we go out to play?": "我们能出去玩吗？",
    "Daddy, it's stopped raining.": "爸爸，雨停了。",
    "Peppa loves jumping in muddy puddles.": "Peppa 喜欢在泥坑里跳。",
    "So, Peppa and George cannot play outside.": "所以 Peppa 和 George 不能出去玩。",
    "Alright, run along you two.": "好吧，你们俩去玩吧。",
    "Look, George. There's a really big puddle.": "看，George，有个好大的泥坑。",
    "I must check if it's safe for you.": "我得看看这对你安不安全。",
    "Guess what we've been doing.": "猜猜我们刚才在干什么。",
    "Have you just had a bath?": "你们刚洗完澡吗？",
    "Yes, we can all play in the garden.": "好，我们都可以在花园里玩。",
}


def episode_path(num: int) -> Path | None:
    pattern = f"Peppa.Pig.S01E{num:02d}.*.md"
    matches = sorted(EP_DIR.glob(pattern))
    return matches[0] if matches else None


def is_dialogue_line(line: str) -> bool:
    s = line.strip()
    if not s or len(s) < 4:
        return False
    if s.startswith("#") or s.startswith("|") or s.startswith("**"):
        return False
    if s.startswith("*") and s.endswith("*"):
        return False
    if not re.search(r"[a-zA-Z]", s):
        return False
    # Skip lone episode title slug lines (short title case)
    if re.fullmatch(r"[A-Za-z][A-Za-z .']{0,40}", s) and s[0].isupper() and "." not in s and "?" not in s and "!" not in s:
        words = s.split()
        if len(words) <= 4 and not any(w.lower() in ("i", "we", "you", "the", "my", "is", "are") for w in words):
            return False
    return True


def normalize(line: str) -> str:
    s = line.strip()
    s = re.sub(r"\s+", " ", s)
    # Fix common OCR casing in repo
    s = s.replace("Cannot", "cannot").replace("Let's", "Let's").replace("Come and", "come and")
    return s


def select_lines(all_lines: list[str], target: int = 20) -> list[str]:
    if len(all_lines) <= target:
        return all_lines

    seen: set[str] = set()
    unique: list[str] = []
    for ln in all_lines:
        key = ln.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(ln)

    if len(unique) <= target:
        return unique

    # Always keep first 4 (intro) if present
    head = unique[:4]
    rest = unique[4:]
    n_rest = target - len(head)
    if n_rest <= 0:
        return head[:target]

    step = max(1, len(rest) // n_rest)
    picked = [rest[i] for i in range(0, len(rest), step)][:n_rest]
    return head + picked


def extract_dialogue(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## Episode vocabulary"):
            break
        if is_dialogue_line(raw):
            lines.append(normalize(raw))
    return select_lines(lines, target=20)


def load_external_glosses() -> dict[str, str]:
    """Build EN→简中 map from question bank, emotions, and character guides."""
    gloss = dict(GLOSS)
    repo = REPO

    def add_from_table_rows(text: str) -> None:
        for line in text.splitlines():
            if not line.startswith("|") or line.startswith("| ---"):
                continue
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) < 2:
                continue
            eng = re.sub(r"\*\*", "", parts[0]).strip()
            zh = parts[1].strip()
            if eng and zh and re.search(r"[\u4e00-\u9fff]", zh):
                gloss[eng] = zh
                gloss[eng.rstrip(".?!")] = zh

    for rel in (
        "learning-notes/tv-series/Peppa Pig S01.英文剧本/peppa-pig-s01-question-bank-by-category.md",
        "learning-notes/tv-series/Peppa Pig S01.英文剧本/peppa-pig-s01-emotions-by-category.md",
        "learning-notes/parenting-english/games-and-activities/parenting-peppa-pig-notes.md",
    ):
        p = repo / rel
        if p.exists():
            add_from_table_rows(p.read_text(encoding="utf-8"))

    char_dir = repo / "learning-notes/tv-series/Peppa Pig S01.英文剧本/characters"
    for md in char_dir.glob("*.md"):
        if md.name == "README.md":
            continue
        add_from_table_rows(md.read_text(encoding="utf-8"))

    return gloss


EXTERNAL_GLOSS: dict[str, str] | None = None


def get_gloss_dict() -> dict[str, str]:
    global EXTERNAL_GLOSS
    if EXTERNAL_GLOSS is None:
        EXTERNAL_GLOSS = load_external_glosses()
    return EXTERNAL_GLOSS


def gloss_line(english: str) -> str:
    g = get_gloss_dict()
    if english in g:
        return g[english]
    key = english.rstrip(".?!")
    if key in g:
        return g[key]
    for k, v in g.items():
        if k.lower() == english.lower():
            return v
    return "（见本集动画 / 完整剧本）"


def build_markdown(episodes: dict[int, list[str]]) -> str:
    """Print-only markdown: no YAML, wikilinks, index, or Related section."""
    parts = [
        "# Peppa Pig S01 · 精选台词（E01–E45）",
        "",
        "Celine 暑假跟读 · 每集 15–20 句 · A4 · 14–16 pt · 行距 1.5",
        "正面英文（孩子）· 背面简中（妈妈）或整表双面印。",
        "未标注简中的句子，妈妈可对照《小猪佩奇第一季 双语》或动画。",
        "",
    ]

    for num in sorted(episodes):
        title = EPISODE_TITLES.get(num, f"Episode {num}")
        parts.append(f"## S01E{num:02d} · {title}")
        parts.append("")
        parts.append("| # | English | 简中（妈妈参考） |")
        parts.append("| --- | --- | --- |")
        for i, eng in enumerate(episodes[num], 1):
            zh = gloss_line(eng)
            eng_esc = eng.replace("|", "\\|")
            zh_esc = zh.replace("|", "\\|")
            parts.append(f"| {i} | {eng_esc} | {zh_esc} |")
        parts.append("")

    return "\n".join(parts)


def main() -> None:
    episodes: dict[int, list[str]] = {}
    for num in range(1, 46):
        path = episode_path(num)
        if not path:
            raise SystemExit(f"Missing episode file for E{num:02d}")
        episodes[num] = extract_dialogue(path)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_markdown(episodes), encoding="utf-8")
    print(f"Wrote {OUT_FILE} ({len(episodes)} episodes)")


if __name__ == "__main__":
    main()
