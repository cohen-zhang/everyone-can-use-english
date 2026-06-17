#!/usr/bin/env python3
"""Enrich english-song docs: sections, tags, README index tables."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SONG_DIR = ROOT / "learning-notes" / "english-song"
PLAYLIST_JSON = SONG_DIR / "apple-music-english-song-playlist.json"
README = SONG_DIR / "README.md"
CATALOG_JSON = SONG_DIR / "english-song-catalog.json"
PLAYLIST_URL = (
    "https://music.apple.com/cn/playlist/english-song/pl.u-JPAZEGNTD9ABPd1"
)

CURATED = {
    ("Messy", "Lola Young"): "messy-lola-young.md",
    ("Big Big World", "Emilia"): "big-big-world-emilia.md",
}

CURATED_META: dict[tuple[str, str], dict] = {
    ("Messy", "Lola Young"): {
        "topics": ["topic/emotions", "topic/relationships", "topic/self-identity"],
        "genres": ["genre/pop", "genre/rock"],
        "level": "level/medium",
        "era": "era/2020s",
        "uses": ["use/ktv", "use/deep-study"],
        "primary_genre": "Pop rock",
        "genre_display": "Pop · pop rock",
        "topic_display": "情绪 · 关系 · 自我",
        "release_date": "2024-05-30",
        "length": "4:44",
    },
    ("Big Big World", "Emilia"): {
        "topics": ["topic/breakup-loss", "topic/emotions", "topic/love-romance"],
        "genres": ["genre/pop", "genre/ballad"],
        "level": "level/easy",
        "era": "era/classic",
        "uses": ["use/ktv", "use/commute", "use/pronunciation"],
        "primary_genre": "Pop ballad",
        "genre_display": "Pop · ballad",
        "topic_display": "分手·思念 · 情绪 · 恋爱",
        "release_date": "1998-09-17",
        "length": "3:22",
    },
}

ITUNES_GENRE_EN = {
    "原声音乐": "Soundtrack",
    "流行": "Pop",
    "摇滚": "Rock",
    "嘻哈/说唱": "Hip-Hop",
    "乡村": "Country",
    "节奏布鲁斯": "R&B",
    "电子": "Electronic",
    "爵士": "Jazz",
    "古典": "Classical",
}

# --- display labels for README columns ---
TOPIC_LABELS = {
    "topic/love-romance": "恋爱",
    "topic/breakup-loss": "分手·思念",
    "topic/self-identity": "自我",
    "topic/emotions": "情绪",
    "topic/party-energy": "派对·能量",
    "topic/film-ost": "影视原声",
    "topic/life-attitude": "生活态度",
}
GENRE_LABELS = {
    "genre/pop": "Pop",
    "genre/ballad": "Ballad",
    "genre/rock": "Rock",
    "genre/country": "Country",
    "genre/hip-hop": "Hip-hop",
    "genre/jazz-standards": "Jazz",
    "genre/edm": "EDM",
    "genre/r-and-b": "R&B",
}
LEVEL_LABELS = {
    "level/easy": "易",
    "level/medium": "中",
    "level/hard": "难",
}
ERA_LABELS = {
    "era/classic": "经典",
    "era/2000s": "2000s",
    "era/2010s": "2010s",
    "era/2020s": "2020s",
}
USE_LABELS = {
    "use/ktv": "KTV",
    "use/commute": "通勤",
    "use/deep-study": "精研",
    "use/pronunciation": "发音",
}

HIP_HOP_ARTISTS = {
    "eminem", "wiz khalifa", "cardi b", "nicki minaj", "macklemore", "akon",
    "gotye", "nana", "蔡徐坤",
}
COUNTRY_ARTISTS = {
    "old dominion", "rascal flatts", "gord bamford", "gabby barrett",
}
JAZZ_ARTISTS = {
    "frank sinatra", "弗兰克", "sinatra", "小野丽莎", "bill withers",
    "bobby caldwell", "grover washington", "bertie higgins", "手嶌葵",
}
ROCK_ARTISTS = {
    "green day", "linkin park", "queen", "europe", "the beatles",
    "phil collins", "whitney houston",
}
KTV_TITLES = {
    "hey jude", "perfect", "shape of you", "someone you loved", "apologize",
    "counting stars", "love story", "you belong with me", "marry you",
    "take me to your heart", "yesterday once more", "right here waiting",
    "big big world", "casablanca", "stand by me", "my love", "treasure",
    "when i was your man", "somebody that i used to know", "let it go",
    "bad romance", "love the way you lie", "see you again", "levitating",
    "fly me to the moon", "just the two of us", "because you loved me",
}


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "song"


def filename_for(item: dict, used: set[str]) -> str:
    key = (item["title"], item["artist"])
    if key in CURATED:
        return CURATED[key]
    base = slugify(item["title"])
    artist_part = slugify(item["artist"].split(",")[0].split("&")[0])
    candidate = f"{base}-{artist_part}.md"
    if candidate in used:
        candidate = f"{base}-{artist_part}-{item['track']}.md"
    used.add(candidate)
    return candidate


def fetch_itunes(ids: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    chunk = 50
    for i in range(0, len(ids), chunk):
        batch = ids[i : i + chunk]
        url = "https://itunes.apple.com/lookup?id=" + ",".join(batch) + "&entity=song&country=cn"
        req = urllib.request.Request(url, headers={"User-Agent": "enrich-english-song/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            continue
        for r in data.get("results", []):
            if r.get("wrapperType") == "track" and r.get("kind") == "song":
                out[str(r["trackId"])] = r
    return out


def ms_to_length(ms: int | None) -> str:
    if not ms:
        return "—"
    sec = ms // 1000
    return f"{sec // 60}:{sec % 60:02d}"


def era_from_year(year: int | None) -> str:
    if not year:
        return "era/2010s"
    if year < 2000:
        return "era/classic"
    if year < 2010:
        return "era/2000s"
    if year < 2020:
        return "era/2010s"
    return "era/2020s"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def classify(item: dict, itunes: dict | None, lyrics: str) -> dict:
    title = item["title"]
    artist = item["artist"]
    album = item.get("album", "")
    text = norm(f"{title} {artist} {album} {lyrics[:2000] if lyrics else ''}")

    topics: set[str] = set()
    if re.search(
        r"\b(love|heart|kiss|marry|romance|baby|darling|forever|hold you|adore)\b", text
    ):
        topics.add("topic/love-romance")
    if re.search(
        r"\b(miss|goodbye|lonely|apologize|lost|gone|break|tears|waiting|end|leave|used to know|without you)\b",
        text,
    ):
        topics.add("topic/breakup-loss")
    if re.search(r"\b(myself|be me|who i am|identity|messy|perfect girl|let it go|free)\b", text):
        topics.add("topic/self-identity")
    if re.search(r"\b(cry|sad|angry|feel|emotion|happy|afraid|numb|hurt)\b", text):
        topics.add("topic/emotions")
    if re.search(r"\b(dance|party|turn up|levitat|ring|monkey|treasure|glorious)\b", text):
        topics.add("topic/party-energy")
    if re.search(
        r"(soundtrack|motion picture|original|frozen|bodyguard|furious|star is born|stranger things|music and lyrics|netflix)",
        text,
    ):
        topics.add("topic/film-ost")
    if re.search(r"\b(life|dream|world|live|tomorrow|way|believe|hope)\b", text):
        topics.add("topic/life-attitude")
    if not topics:
        topics.add("topic/life-attitude")

    genres: set[str] = set()
    primary = (itunes or {}).get("primaryGenreName", "").lower()
    if "hip" in primary or "rap" in primary:
        genres.add("genre/hip-hop")
    elif "country" in primary:
        genres.add("genre/country")
    elif "rock" in primary:
        genres.add("genre/rock")
    elif "jazz" in primary:
        genres.add("genre/jazz-standards")
    elif "dance" in primary or "electronic" in primary:
        genres.add("genre/edm")
    elif "r&b" in primary or "soul" in primary:
        genres.add("genre/r-and-b")
    else:
        genres.add("genre/pop")

    an = norm(artist.split(",")[0].split("&")[0])
    if any(x in an for x in HIP_HOP_ARTISTS) or "eminem" in text:
        genres.add("genre/hip-hop")
    if any(x in an for x in COUNTRY_ARTISTS):
        genres.add("genre/country")
    if any(x in an for x in JAZZ_ARTISTS):
        genres.add("genre/jazz-standards")
    if any(x in an for x in ROCK_ARTISTS):
        genres.add("genre/rock")
    if re.search(r"\b(slow|ballad|waiting|remember|rose|nothing)\b", text) and "genre/hip-hop" not in genres:
        genres.add("genre/ballad")

    level = "level/medium"
    if any(x in an for x in HIP_HOP_ARTISTS) or "rap" in text:
        level = "level/hard"
    elif genres & {"genre/ballad", "genre/jazz-standards"} or norm(title) in KTV_TITLES:
        if level != "level/hard":
            level = "level/easy"
    word_count = len(re.findall(r"[a-zA-Z']+", lyrics)) if lyrics else 0
    if word_count and word_count < 120 and level != "level/hard":
        level = "level/easy"

    release = (itunes or {}).get("releaseDate", "")
    year = int(release[:4]) if release and len(release) >= 4 else None
    era = era_from_year(year)

    uses: set[str] = set()
    if norm(title) in KTV_TITLES or "love" in text:
        uses.add("use/ktv")
    if level == "level/easy" and "explicit" not in text and "fuck" not in text and "wap" not in text:
        uses.add("use/commute")
    if level in ("level/easy", "level/medium"):
        uses.add("use/deep-study")
    if genres & {"genre/ballad", "genre/pop", "genre/jazz-standards"}:
        uses.add("use/pronunciation")
    if not uses:
        uses.add("use/deep-study")

    primary_raw = (itunes or {}).get("primaryGenreName", "Pop")
    primary_genre = ITUNES_GENRE_EN.get(primary_raw, primary_raw)

    genre_display = " · ".join(
        GENRE_LABELS.get(g, g.removeprefix("genre/")) for g in sorted(genres)
    )
    topic_display = " · ".join(
        TOPIC_LABELS.get(t, t) for t in sorted(topics)
    )

    return {
        "topics": sorted(topics),
        "genres": sorted(genres),
        "level": level,
        "era": era,
        "uses": sorted(uses),
        "year": year,
        "release_date": release[:10] if release else "—",
        "length": ms_to_length((itunes or {}).get("trackTimeMillis")),
        "primary_genre": primary_genre,
        "genre_display": genre_display,
        "topic_display": topic_display,
    }


def meta_for_item(item: dict, itunes: dict | None, lyrics: str) -> dict:
    key = (item["title"], item["artist"])
    if key in CURATED_META:
        m = dict(CURATED_META[key])
        return m
    return classify(item, itunes, lyrics)


def extract_lyrics_body(content: str) -> tuple[str, str]:
    """Return (lyrics_section_header+body, plain lyrics text)."""
    m = re.search(r"(## 歌词 · Lyrics\n)([\s\S]*?)(?=\n## |\Z)", content)
    if not m:
        return "", ""
    section = m.group(1) + m.group(2).rstrip() + "\n"
    plain = m.group(2)
    plain = re.sub(r"^> .*\n", "", plain, flags=re.MULTILINE)
    plain = re.sub(r"^### .*\n", "", plain, flags=re.MULTILINE)
    plain = re.sub(r" — .*", "", plain)
    plain = re.sub(r"\*\([^)]*\)\*", "", plain)
    return section, plain.strip()


def extract_key_phrases(lyrics: str, title: str, limit: int = 8) -> list[tuple[str, str, str]]:
    if not lyrics:
        return []
    lines = [ln.strip() for ln in lyrics.splitlines() if ln.strip()]
    scored: list[tuple[int, str]] = []
    for ln in lines:
        if len(ln) < 8 or ln.lower() == title.lower():
            continue
        score = 0
        if "'" in ln or "n't" in ln:
            score += 2
        if re.search(r"\b(love|heart|miss|never|always|world|life|dream|feel)\b", ln, re.I):
            score += 1
        if len(ln.split()) <= 12:
            score += 1
        scored.append((score, ln))
    scored.sort(key=lambda x: (-x[0], len(x[1])))
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for _, ln in scored:
        key = ln.lower()
        if key in seen:
            continue
        seen.add(key)
        # simple gloss placeholder — learner can refine in curated pass
        gloss = "见歌词上下文"
        note = "跟唱时可注意连读与重音"
        if "n't" in ln or "don't" in ln.lower():
            note = "含缩略 / 否定口语"
        out.append((ln, gloss, note))
        if len(out) >= limit:
            break
    return out


def related_links(topics: set[str]) -> str:
    links = []
    if topics & {"topic/love-romance", "topic/breakup-loss"}:
        links.append(
            "[[learning-notes/personal-english-book/life/romantic-love-song-phrases|浪漫情歌与恋爱口语]]"
        )
    if topics & {"topic/emotions", "topic/self-identity"}:
        links.append(
            "[[learning-notes/personal-english-book/life/emotions-adult-edition|情绪 — 成人版]]"
        )
    if not links:
        return ""
    return "**相关：** " + " · ".join(links) + "\n\n"


def build_tags(meta: dict) -> list[str]:
    base = ["english-song", "english-learning", "playlist/english-song"]
    return base + meta["topics"] + meta["genres"] + [meta["level"], meta["era"]] + meta["uses"]


def build_artist_intro(artist: str, primary_genre: str) -> str:
    return f"""## 歌手简介 · About {artist.split(',')[0].split('&')[0].strip()}

**English**

**{artist}** is a recording artist associated with **{primary_genre}** and popular music. This note is tied to your Apple Music playlist [English song]({PLAYLIST_URL}).

**中文**

**{artist}** 是与 **{primary_genre}** 及流行音乐相关的歌手/组合。本笔记对应 Apple Music 播放列表 [English song]({PLAYLIST_URL})。"""


def build_song_intro(title: str, artist: str, album: str, meta: dict) -> str:
    topics_en = ", ".join(t.replace("topic/", "") for t in meta["topics"])
    return f"""## 歌曲简介 · About the Song

**English**

**"{title}"** by **{artist}** is a **{meta['primary_genre']}** track from *{album}*. Themes in the lyrics often touch on **{topics_en.replace('-', ' ')}**, useful for spoken English and sing-along practice.

**中文**

**"{title}"**（**{artist}**）收录于 *{album}*，属 **{meta['primary_genre']}** 风格。歌词主题多与 **{meta['topic_display']}** 相关，适合跟唱与口语表达练习。

| 项目 | English | 信息 |
| --- | --- | --- |
| 专辑 | Album | *{album}* |
| 发行 | Release date | {meta['release_date']} |
| 曲风 | Genre | {meta['genre_display']} |
| 时长 | Length | {meta['length']} |
| 播放列表 | Playlist | [English song]({PLAYLIST_URL}) · #{meta.get('track', '—')} |"""


def build_key_phrases_table(phrases: list[tuple[str, str, str]]) -> str:
    if not phrases:
        return """## 重点表达 · Key Phrases

> 歌词待补充后，可在此整理习语与高频句型。
"""
    rows = ["| English | 简中 | 备注 |", "| --- | --- | --- |"]
    for en, zh, note in phrases:
        en_esc = en.replace("|", "\\|")
        if len(en_esc) > 60:
            en_esc = en_esc[:57] + "…"
        rows.append(f"| *{en_esc}* | {zh} | {note} |")
    return "## 重点表达 · Key Phrases\n\n" + "\n".join(rows) + "\n"


def build_listening_notes(meta: dict, title: str) -> str:
    level = LEVEL_LABELS.get(meta["level"], meta["level"])
    uses = "、".join(USE_LABELS.get(u, u) for u in meta["uses"])
    lines = [
        "## 听歌提示 · Listening Notes",
        "",
        f"- **难度：** {level}（`{meta['level']}`）",
        f"- **推荐场景：** {uses}",
        f"- **年代标签：** {ERA_LABELS.get(meta['era'], meta['era'])}",
    ]
    if "use/ktv" in meta["uses"]:
        lines.append(f"- 副歌 *{title.split('(')[0].strip()}* 适合 KTV 跟唱，先听清副歌再练 Verse。")
    if meta["level"] == "level/hard":
        lines.append("- 语速较快或词汇密度高，建议先慢速跟读再原速。")
    if "genre/jazz-standards" in meta["genres"]:
        lines.append("- 爵士标准曲，注意弱读与节奏 swing 感。")
    return "\n".join(lines) + "\n"


def merge_frontmatter_tags(content: str, new_tags: list[str]) -> str:
    m = re.match(r"^---\n([\s\S]*?)\n---\n", content)
    if not m:
        return content
    fm = m.group(1)
    alias_m = re.search(r"^aliases:\n((?:  - .+\n)*)", fm, re.MULTILINE)
    aliases: list[str] = []
    if alias_m:
        aliases = re.findall(r"^  - (.+)$", alias_m.group(1), re.MULTILINE)
    keep_aliases = [
        a
        for a in aliases
        if not a.startswith("topic/")
        and not a.startswith("genre/")
        and not a.startswith("level/")
        and not a.startswith("era/")
        and not a.startswith("use/")
    ]
    tag_lines = "\n".join(f"  - {t}" for t in new_tags)
    alias_lines = "\n".join(f"  - {a}" for a in keep_aliases)
    new_fm = f"---\ntags:\n{tag_lines}\naliases:\n{alias_lines}\n---\n"
    return new_fm + content[m.end() :]


def build_full_doc(
    item: dict,
    meta: dict,
    lyrics_section: str,
    phrases: list[tuple[str, str, str]],
    curated: bool,
) -> str:
    title = item["title"]
    artist = item["artist"]
    meta["track"] = item["track"]
    tags = build_tags(meta)
    alias = f"{title} — {artist}"

    tag_block = "\n".join(f"  - {t}" for t in tags)
    header = f"""---
tags:
{tag_block}
aliases:
  - {alias}
---
# {title} — {artist}

**索引：** [[learning-notes/english-song/README|英文歌曲索引]]

**Apple Music：** [{title}]({item["url"]})

{related_links(set(meta["topics"]))}"""

    if curated:
        # only inject missing sections into existing — handled separately
        return ""

    artist_sec = build_artist_intro(artist, meta["primary_genre"])
    song_sec = build_song_intro(title, artist, item.get("album", "—"), meta)
    key_sec = build_key_phrases_table(phrases)
    listen_sec = build_listening_notes(meta, title)

    lyrics_part = lyrics_section if lyrics_section else "## 歌词 · Lyrics\n\n> 歌词暂未自动获取，可稍后手动补充。\n"

    return (
        header
        + "\n---\n\n"
        + artist_sec
        + "\n\n---\n\n"
        + song_sec
        + "\n\n---\n\n"
        + lyrics_part
        + "\n---\n\n"
        + key_sec
        + "\n---\n\n"
        + listen_sec
    )


def enrich_curated(path: Path, meta: dict) -> None:
    content = path.read_text(encoding="utf-8")
    tags = build_tags(meta)
    # keep curated-specific tags
    extra = []
    if "topic/relationships" in content and "topic/relationships" not in tags:
        extra.append("topic/relationships")
    content = merge_frontmatter_tags(content, tags + extra)

    # insert Apple Music link if missing
    if "**Apple Music：**" not in content:
        url = meta.get("url", "")
        title = meta.get("title", path.stem)
        content = content.replace(
            "**索引：**",
            f"**Apple Music：** [{title}]({url})\n\n**索引：**",
            1,
        )

    # add listening notes if missing
    if "## 听歌提示 · Listening Notes" not in content:
        listen = build_listening_notes(meta, meta.get("title", path.stem))
        content = content.rstrip() + "\n\n---\n\n" + listen + "\n"

    path.write_text(content, encoding="utf-8")


def build_readme(catalog: list[dict]) -> str:
    def row(c: dict) -> str:
        link = c["file"].removesuffix(".md")
        title = c["title"].replace("|", "\\|")
        return (
            f"| {c['track']} | {c['title']} | {c['artist']} | {c['topic_display']} | "
            f"{c['genre_display']} | {LEVEL_LABELS.get(c['level'], c['level'])} | "
            f"{ERA_LABELS.get(c['era'], c['era'])} | "
            f"{' · '.join(USE_LABELS.get(u, u) for u in c['uses'])} | "
            f"[[learning-notes/english-song/{link}|{title}]] |"
        )

    master = [
        "| # | 歌名 | 歌手 | 主题 | 曲风 | 难度 | 年代 | 场景 | 笔记 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in catalog:
        master.append(row(c))

    def group_table(key: str, label_map: dict) -> str:
        lines = [f"| {list(label_map.values())[0][:2] if False else '标签'} | # | 歌名 | 歌手 | 笔记 |", "| --- | --- | --- | --- | --- |"]
        lines[0] = "| 标签 | # | 歌名 | 歌手 | 笔记 |"
        lines[1] = "| --- | --- | --- | --- | --- |"
        groups: dict[str, list[dict]] = defaultdict(list)
        for c in catalog:
            for k in c.get(key + "s", c.get(key, [])):
                groups[k].append(c)
        for tag in sorted(groups, key=lambda t: label_map.get(t, t)):
            label = label_map.get(tag, tag)
            for c in sorted(groups[tag], key=lambda x: x["track"]):
                link = c["file"].removesuffix(".md")
                lines.append(
                    f"| {label} | {c['track']} | {c['title']} | {c['artist']} | "
                    f"[[learning-notes/english-song/{link}|笔记]] |"
                )
        return "\n".join(lines)

    topic_table = group_table("topics", TOPIC_LABELS)
    genre_table = group_table("genres", GENRE_LABELS)
    level_lines = ["| 难度 | # | 歌名 | 歌手 | 笔记 |", "| --- | --- | --- | --- | --- |"]
    by_level: dict[str, list] = defaultdict(list)
    for c in catalog:
        by_level[c["level"]].append(c)
    for lv in ["level/easy", "level/medium", "level/hard"]:
        for c in sorted(by_level.get(lv, []), key=lambda x: x["track"]):
            link = c["file"].removesuffix(".md")
            level_lines.append(
                f"| {LEVEL_LABELS[lv]} | {c['track']} | {c['title']} | {c['artist']} | "
                f"[[learning-notes/english-song/{link}|笔记]] |"
            )

    era_lines = ["| 年代 | # | 歌名 | 歌手 | 笔记 |", "| --- | --- | --- | --- | --- |"]
    by_era: dict[str, list] = defaultdict(list)
    for c in catalog:
        by_era[c["era"]].append(c)
    for era in ["era/classic", "era/2000s", "era/2010s", "era/2020s"]:
        for c in sorted(by_era.get(era, []), key=lambda x: x["track"]):
            link = c["file"].removesuffix(".md")
            era_lines.append(
                f"| {ERA_LABELS[era]} | {c['track']} | {c['title']} | {c['artist']} | "
                f"[[learning-notes/english-song/{link}|笔记]] |"
            )

    use_lines = ["| 场景 | # | 歌名 | 歌手 | 笔记 |", "| --- | --- | --- | --- | --- |"]
    by_use: dict[str, list] = defaultdict(list)
    for c in catalog:
        for u in c["uses"]:
            by_use[u].append(c)
    for u in sorted(by_use, key=lambda t: USE_LABELS.get(t, t)):
        for c in sorted(by_use[u], key=lambda x: x["track"]):
            link = c["file"].removesuffix(".md")
            use_lines.append(
                f"| {USE_LABELS.get(u, u)} | {c['track']} | {c['title']} | {c['artist']} | "
                f"[[learning-notes/english-song/{link}|笔记]] |"
            )

    todo = [c for c in catalog if c.get("lyrics_missing")]

    return f"""---
tags:
  - english-song
  - english-learning
aliases:
  - 英文歌曲索引
---
# 英文歌曲 · English Songs

按歌曲整理的英文学习笔记：歌手与歌曲简介、歌词、重点表达。

**Apple Music 播放列表：** [English song]({PLAYLIST_URL})（109 首 · 约 6 小时 46 分钟）

## 播放列表总表

{chr(10).join(master)}

## 按主题 · Topic

{topic_table}

## 按曲风 · Genre

{genre_table}

## 按难度 · Level

{chr(10).join(level_lines)}

## 按年代 · Era

{chr(10).join(era_lines)}

## 按场景 · Use

{chr(10).join(use_lines)}

## 完整笔记（手工精编）

以下笔记含更完整的英中对照与重点表达：

| 歌曲 | 歌手 | 笔记 |
| --- | --- | --- |
| **Messy** | Lola Young | [[learning-notes/english-song/messy-lola-young|Messy — Lola Young]] |
| **Big Big World** | Emilia | [[learning-notes/english-song/big-big-world-emilia|Big Big World — Emilia]] |

## 歌词待补充

{len(todo)} 首文档已建章，歌词仍待手动补充：

| # | 歌名 | 歌手 | 笔记 |
| --- | --- | --- | --- |
"""
    + (
        "\n".join(
            f"| {c['track']} | {c['title']} | {c['artist']} | "
            f"[[learning-notes/english-song/{c['file'].removesuffix('.md')}|笔记]] |"
            for c in todo
        )
        if todo
        else "| — | — | — | — |"
    )
    + "\n"


def main() -> None:
    items: list[dict] = json.loads(PLAYLIST_JSON.read_text(encoding="utf-8"))
    used: set[str] = set(CURATED.values())
    ids = [it["id"] for it in items]
    itunes_map = fetch_itunes(ids)

    catalog: list[dict] = []
    stats = {"updated": 0, "curated": 0}

    for item in items:
        fname = filename_for(item, used)
        path = SONG_DIR / fname
        itunes = itunes_map.get(item["id"])

        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        lyrics_section, plain_lyrics = extract_lyrics_body(existing)
        meta = meta_for_item(item, itunes, plain_lyrics)
        phrases = extract_key_phrases(plain_lyrics, item["title"])

        key = (item["title"], item["artist"])
        if key in CURATED:
            meta.update({"title": item["title"], "url": item["url"]})
            enrich_curated(path, meta)
            stats["curated"] += 1
        else:
            doc = build_full_doc(item, meta, lyrics_section, phrases, curated=False)
            path.write_text(doc, encoding="utf-8")
            stats["updated"] += 1

        catalog.append(
            {
                "track": item["track"],
                "title": item["title"],
                "artist": item["artist"],
                "file": fname,
                "topics": meta["topics"],
                "genres": meta["genres"],
                "level": meta["level"],
                "era": meta["era"],
                "uses": meta["uses"],
                "topic_display": meta["topic_display"],
                "genre_display": meta["genre_display"],
                "lyrics_missing": not plain_lyrics or "暂未自动获取" in existing,
            }
        )

    CATALOG_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    README.write_text(build_readme(catalog), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
