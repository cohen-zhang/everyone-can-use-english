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
    ('Relax, Take It Easy', 'MIKA'): 'relax-take-it-easy-mika.md',
    ('I Am You (Remastered 2021)', 'Kim Taylor'): 'i-am-you-kim-taylor.md',
    ("Can't Complain", 'Relient K'): 'cant-complain-relient-k.md',
    ('Everybody Knows', 'Sigrid'): 'everybody-knows-sigrid.md',
    ('I Like Me Better', 'LAUV'): 'i-like-me-better-lauv.md',
    ('7 rings', 'Ariana Grande'): '7-rings-ariana-grande.md',
    ('Better Man', 'Robbie Williams'): 'better-man-robbie-williams.md',
    ('Hey Jude', 'The Beatles'): 'hey-jude-the-beatles.md',
    ('Sealed With a Kiss', 'Dana Winner'): 'sealed-with-a-kiss-dana-winner.md',
    ('Right Now (Na Na Na)', 'Akon'): 'right-now-akon.md',
    ('Love the Way You Lie (feat. Rihanna)', 'Eminem'): 'love-the-way-you-lie-eminem.md',
    ('This Is the Life', 'Amy Macdonald'): 'this-is-the-life-amy-macdonald.md',
    ('I Will Follow You', 'Ricky Nelson'): 'i-will-follow-you-ricky-nelson.md',
    ('Take Me To Your Heart', 'Michael Learns to Rock'): 'take-me-to-your-heart-michael-learns-to-rock.md',
    ('Right Here Waiting', '理查德·马克斯'): 'right-here-waiting-理查德马克斯.md',
    ('Black Sheep', 'Gin Wigmore'): 'black-sheep-gin-wigmore.md',
    ('bad guy', 'Billie Eilish'): 'bad-guy-billie-eilish.md',
    ('High on Life (feat. Bonn)', 'Martin Garrix'): 'high-on-life-martin-garrix.md',
    ('Always Remember Us This Way', 'Brenda Mullen'): 'always-remember-us-this-way-brenda-mullen.md',
    ('Dreamer', 'Europe'): 'dreamer-europe.md',
    ('When Your Lips Are So Close', 'Gord Bamford'): 'when-your-lips-are-so-close-gord-bamford.md',
    ('Against All Odds (Take a Look at Me Now)', 'Phil Collins'): 'against-all-odds-phil-collins.md',
    ('Stand By Me', 'Seal'): 'stand-by-me-seal.md',
    ('Who Wants To Live Forever', 'Queen'): 'who-wants-to-live-forever-queen.md',
    ('The Old Man', '菲尔・科尔特'): 'the-old-man-菲尔科尔特.md',
    ('The Old Man', 'Yom & Aurélien Naffrichoux'): 'the-old-man-yom.md',
    ("Promises Don't Come Easy", '陈曦'): 'promises-dont-come-easy-陈曦.md',
    ('What Can I Do (Promises)', 'Caron Nightingale'): 'what-can-i-do-caron-nightingale.md',
    ('Love Story (Taylor’s Version)', 'Taylor Swift'): 'love-story-taylor-swift.md',
    ('Yesterday Once More', 'Carpenters'): 'yesterday-once-more-carpenters.md',
    ('Sealed With a Kiss', 'The Lettermen'): 'sealed-with-a-kiss-the-lettermen.md',
    ('No Such Thing as a Broken Heart', 'Old Dominion'): 'no-such-thing-as-a-broken-heart-old-dominion.md',
    ('These Days', 'Rascal Flatts'): 'these-days-rascal-flatts.md',
    ('Because of You', 'Ne-Yo'): 'because-of-you-ne-yo.md',
    ('Shape of You', 'Ed Sheeran'): 'shape-of-you-ed-sheeran.md',
    ('Because You Loved Me (Theme from "Up Close and Personal")', 'Céline Dion'): 'because-you-loved-me-céline-dion.md',
    ('Like I Can', 'Sam Smith'): 'like-i-can-sam-smith.md',
    ('Die With A Smile', 'Lady Gaga & Bruno Mars'): 'die-with-a-smile-lady-gaga.md',
    ('Bad Romance', 'Lady Gaga'): 'bad-romance-lady-gaga.md',
    ('Let It Go', 'Idina Menzel'): 'let-it-go-idina-menzel.md',
    ('Lights (Single Version)', 'Ellie Goulding'): 'lights-ellie-goulding.md',
    ('Young Dumb & Broke', 'Khalid'): 'young-dumb-broke-khalid.md',
    ('Glorious (feat. Skylar Grey)', 'Macklemore'): 'glorious-macklemore.md',
    ('Perfect', 'Ed Sheeran'): 'perfect-ed-sheeran.md',
    ('Numb', 'LINKIN PARK'): 'numb-linkin-park.md',
    ('Numb Little Bug', 'Em Beihold'): 'numb-little-bug-em-beihold.md',
    ('Adore You', 'Harry Styles'): 'adore-you-harry-styles.md',
    ("I Don't Think I'm Okay", 'Bazzi'): 'i-dont-think-im-okay-bazzi.md',
    ('Someone You Loved', 'Lewis Capaldi'): 'someone-you-loved-lewis-capaldi.md',
    ('The Other', 'LAUV'): 'the-other-lauv.md',
    ('Head In The Clouds', 'Hayd'): 'head-in-the-clouds-hayd.md',
    ('When You Look At Me', 'Sara Kays'): 'when-you-look-at-me-sara-kays.md',
    ("That's Us", 'Anson Seabra'): 'thats-us-anson-seabra.md',
    ("It's You", 'Ali Gatie'): 'its-you-ali-gatie.md',
    ('Counting Stars', 'OneRepublic'): 'counting-stars-onerepublic.md',
    ('I Hope You Never Fall in Love Again', 'KiD RAiN'): 'i-hope-you-never-fall-in-love-again-kid-rain.md',
    ('Messy', 'Lola Young'): 'messy-lola-young.md',
    ('Please Please Please', 'Sabrina Carpenter'): 'please-please-please-sabrina-carpenter.md',
    ('Good Cry', 'Noah Cyrus'): 'good-cry-noah-cyrus.md',
    ('July (Apple Music Home Session)', 'Rhys Lewis'): 'july-rhys-lewis.md',
    ('Dance Like No One’s Watching', 'Gabby Barrett'): 'dance-like-no-ones-watching-gabby-barrett.md',
    ('Gentle Heart', 'Joshua Hyslop'): 'gentle-heart-joshua-hyslop.md',
    ('Take Control', 'Kodaline'): 'take-control-kodaline.md',
    ('Marry You', 'Bruno Mars'): 'marry-you-bruno-mars.md',
    ('My Love (Radio Edit)', 'Westlife'): 'my-love-westlife.md',
    ('Dance Monkey', 'Tones And I'): 'dance-monkey-tones-and-i.md',
    ('Grace', 'Lewis Capaldi'): 'grace-lewis-capaldi.md',
    ("What You Won't Do for Love", 'Bobby Caldwell'): 'what-you-wont-do-for-love-bobby-caldwell.md',
    ('Just the Two of Us', 'Grover Washington, Jr. with Bill Withers'): 'just-the-two-of-us-grover-washington.md',
    ('Fallen', 'Lola Amour'): 'fallen-lola-amour.md',
    ('Julie.', 'Gallant'): 'julie-gallant.md',
    ('Say It Again', 'Betty Wright'): 'say-it-again-betty-wright.md',
    ('Way Back Into Love (Demo Version)', 'Hugh Grant & Drew Barrymore'): 'way-back-into-love-hugh-grant.md',
    ('Two Is Better Than One (feat. Taylor Swift)', 'BOYS LIKE GIRLS'): 'two-is-better-than-one-boys-like-girls.md',
    ('Treasure', 'Bruno Mars'): 'treasure-bruno-mars.md',
    ('You Belong With Me', 'Taylor Swift'): 'you-belong-with-me-taylor-swift.md',
    ('Take Me Back to London (feat. Stormzy)', 'Ed Sheeran'): 'take-me-back-to-london-ed-sheeran.md',
    ('South of the Border (feat. Camila Cabello & Cardi B)', 'Ed Sheeran'): 'south-of-the-border-ed-sheeran.md',
    ("Ain't My Fault (R3hab Remix)", 'Zara Larsson & R3HAB'): 'aint-my-fault-zara-larsson.md',
    ('Vicious Girl', 'CALVO'): 'vicious-girl-calvo.md',
    ('Big Big World', 'Emilia'): 'big-big-world-emilia.md',
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
