#!/usr/bin/env python3
"""Generate english-song markdown docs from Apple Music playlist JSON."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SONG_DIR = ROOT / "learning-notes" / "english-song"
PLAYLIST_JSON = SONG_DIR / "apple-music-english-song-playlist.json"
README = SONG_DIR / "README.md"
PLAYLIST_URL = (
    "https://music.apple.com/cn/playlist/english-song/pl.u-JPAZEGNTD9ABPd1"
)

# Hand-curated docs: skip overwrite, use fixed slug mapping
CURATED = {
    ("Messy", "Lola Young"): "messy-lola-young.md",
    ("Big Big World", "Emilia"): "big-big-world-emilia.md",
}


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "song"


def fetch_json(url: str, timeout: int = 15) -> dict | list | None:
    req = urllib.request.Request(
        url, headers={"User-Agent": "english-song-doc-generator/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        json.JSONDecodeError,
        TimeoutError,
        OSError,
    ):
        return None


def fetch_lyrics(artist: str, title: str) -> tuple[str | None, str]:
    clean_title = re.sub(r"\([^)]*\)", "", title).strip()
    clean_title = re.sub(r"\s*-\s*.*$", "", clean_title).strip()

    q = urllib.parse.quote(f"{artist} {clean_title}")
    data = fetch_json(f"https://lrclib.net/api/search?q={q}")
    if isinstance(data, list) and data:
        for item in data:
            plain = item.get("plainLyrics") or item.get("syncedLyrics")
            if plain:
                src = "lrclib.net"
                if item.get("syncedLyrics") and not item.get("plainLyrics"):
                    plain = re.sub(r"\[\d+:\d+(?:\.\d+)?\]", "", item["syncedLyrics"])
                return plain.strip(), src

    artist_q = urllib.parse.quote(artist)
    title_q = urllib.parse.quote(clean_title)
    data = fetch_json(
        f"https://api.lyrics.ovh/v1/{artist_q}/{title_q}", timeout=8
    )
    if isinstance(data, dict) and data.get("lyrics"):
        return data["lyrics"].strip(), "lyrics.ovh"

    return None, ""


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


def format_lyrics_block(lyrics: str | None) -> str:
    if not lyrics:
        return "> 歌词暂未自动获取，可稍后手动补充。\n"
    lines = [ln.rstrip() for ln in lyrics.splitlines()]
    body = "\n".join(f"{ln}  " if ln else "" for ln in lines)
    return body + "\n"


def build_doc(item: dict, fname: str, lyrics: str | None, source: str) -> str:
    title = item["title"]
    artist = item["artist"]
    alias = f"{title} — {artist}"
    lyrics_note = f"\n> 歌词来源：{source}\n" if source else ""

    return f"""---
tags:
  - english-song
  - english-learning
  - playlist/english-song
aliases:
  - {alias}
---
# {title} — {artist}

**索引：** [[learning-notes/english-song/README|英文歌曲索引]]

**Apple Music：** [{title}]({item["url"]})

| 项目 | English | 信息 |
| --- | --- | --- |
| 专辑 | Album | {item.get("album", "—")} |
| 播放列表 | Playlist | [English song]({PLAYLIST_URL}) · #{item["track"]} |

---

## 歌词 · Lyrics
{lyrics_note}
{format_lyrics_block(lyrics)}"""


def build_readme(items: list[dict], rows: list[tuple[int, str, str, str]]) -> str:
    table_lines = [
        "| # | 歌名 | 歌手 | 笔记 |",
        "| --- | --- | --- | --- |",
    ]
    for track, title, artist, link in rows:
        t = title.replace("|", "\\|")
        a = artist.replace("|", "\\|")
        table_lines.append(f"| {track} | {title} | {artist} | [[learning-notes/english-song/{link}|{t}]] |")

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

## 播放列表清单

{chr(10).join(table_lines)}

## 完整笔记（手工精编）

以下笔记含歌手/歌曲简介、英中对照与重点表达：

| 歌曲 | 歌手 | 笔记 |
| --- | --- | --- |
| **Messy** | Lola Young | [[learning-notes/english-song/messy-lola-young|Messy — Lola Young]] |
| **Big Big World** | Emilia | [[learning-notes/english-song/big-big-world-emilia|Big Big World — Emilia]] |
"""


def main() -> None:
    items: list[dict] = json.loads(PLAYLIST_JSON.read_text(encoding="utf-8"))
    used_names: set[str] = set(CURATED.values())
    rows: list[tuple[int, str, str, str]] = []
    stats = {"created": 0, "skipped": 0, "with_lyrics": 0, "no_lyrics": 0}

    for item in items:
        fname = filename_for(item, used_names)
        link = fname.removesuffix(".md")
        rows.append((item["track"], item["title"], item["artist"], link))

        if fname in CURATED.values():
            stats["skipped"] += 1
            continue

        path = SONG_DIR / fname
        if path.exists():
            stats["skipped"] += 1
            continue

        lyrics, source = fetch_lyrics(item["artist"], item["title"])
        if lyrics:
            stats["with_lyrics"] += 1
        else:
            stats["no_lyrics"] += 1

        path.write_text(build_doc(item, fname, lyrics, source), encoding="utf-8")
        stats["created"] += 1
        time.sleep(0.2)

    README.write_text(build_readme(items, rows), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
