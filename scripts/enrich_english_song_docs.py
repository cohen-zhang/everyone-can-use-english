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
    ('I Got You (feat. Johnning)', 'Janji'): 'i-got-you-janji.md',
    ('Apologize', 'OneRepublic'): 'apologize-onerepublic.md',
    ('One Man Band', 'Old Dominion'): 'one-man-band-old-dominion.md',
    ('See You Again (feat. Charlie Puth)', 'Wiz Khalifa'): 'see-you-again-wiz-khalifa.md',
    ('We Don’t Talk Anymore (feat. Selena Gomez)', 'Charlie Puth'): 'we-dont-talk-anymore-charlie-puth.md',
    ('Sunny', '藤井风'): 'sunny-藤井风.md',
    ('Fly Me To The Moon', '小野丽莎'): 'fly-me-to-the-moon-小野丽莎.md',
    ('Fly Me to the Moon (feat. Count Basie and His Orchestra)', '弗兰克・辛纳特拉'): 'fly-me-to-the-moon-弗兰克辛纳特拉.md',
    ('Casablanca', 'Bertie Higgins'): 'casablanca-bertie-higgins.md',
    ('Wake Me Up When September Ends', 'Green Day'): 'wake-me-up-when-september-ends-green-day.md',
    ('I Have Nothing', 'Whitney Houston'): 'i-have-nothing-whitney-houston.md',
    ('Everybody', 'Ingrid Michaelson'): 'everybody-ingrid-michaelson.md',
    ('WHERE IS MY HUSBAND!', 'RAYE'): 'where-is-my-husband-raye.md',
    ("California Dreamin'", 'The Beach Boys'): 'california-dreamin-the-beach-boys.md',
    ('If You Leave', 'Orchestral Manoeuvres In the Dark'): 'if-you-leave-orchestral-manoeuvres-in-the-dark.md',
    ('Always Remember Us This Way', 'Lady Gaga'): 'always-remember-us-this-way-lady-gaga.md',
    ('Right Now (Na Na Na)', 'Aamir'): 'right-now-aamir.md',
    ('Just One Last Dance (feat. Natural)', 'Sarah Connor'): 'just-one-last-dance-sarah-connor.md',
    ('Lonely', 'NANA'): 'lonely-nana.md',
    ('Deadman', '蔡徐坤'): 'deadman-蔡徐坤.md',
    ('Catch a Grenade (The Hooligans Remix)', 'Bruno Mars'): 'catch-a-grenade-bruno-mars.md',
    ('Levitating', 'Dua Lipa'): 'levitating-dua-lipa.md',
    ('The Rose', '手嶌葵'): 'the-rose-手嶌葵.md',
    ('WAP (feat. Megan Thee Stallion)', 'Cardi B'): 'wap-cardi-b.md',
    ('Anaconda', 'Nicki Minaj'): 'anaconda-nicki-minaj.md',
    ('When I Was Your Man', 'Bruno Mars'): 'when-i-was-your-man-bruno-mars.md',
    ('Somebody That I Used to Know (feat. Kimbra)', 'Gotye'): 'somebody-that-i-used-to-know-gotye.md',
    ('Walking Away', 'ChianoSky'): 'walking-away-chianosky.md',
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


def normalize_apostrophes(text: str) -> str:
    return text.replace("\u2019", "'").replace("\u2018", "'").replace("\u2032", "'")


CURATED_LOOKUP: dict[tuple[str, str], str] = {
    (normalize_apostrophes(title), artist): fname for (title, artist), fname in CURATED.items()
}


def curated_filename(item: dict) -> str | None:
    return CURATED_LOOKUP.get((normalize_apostrophes(item["title"]), item["artist"]))


def filename_for(item: dict, used: set[str]) -> str:
    if fname := curated_filename(item):
        return fname
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
        lines.append(f"- 副歌 *{title.split('(')[0].strip()}* 适合 KTV 跟唱，先听清副歌再练主歌。")
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
        curated = "精编" if c.get("curated") else "—"
        return (
            f"| {c['track']} | {c['title']} | {c['artist']} | {curated} | {c['topic_display']} | "
            f"{c['genre_display']} | {LEVEL_LABELS.get(c['level'], c['level'])} | "
            f"{ERA_LABELS.get(c['era'], c['era'])} | "
            f"{' · '.join(USE_LABELS.get(u, u) for u in c['uses'])} | "
            f"[[learning-notes/english-song/{link}|{title}]] |"
        )

    master = [
        "| # | 歌名 | 歌手 | 精编 | 主题 | 曲风 | 难度 | 年代 | 场景 | 笔记 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
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
    curated_rows = [c for c in catalog if c.get("curated")]
    curated_table = "\n".join(
        f"| {c['track']} | {c['title']} | {c['artist']} | "
        f"[[learning-notes/english-song/{c['file'].removesuffix('.md')}|{c['title']}]] |"
        for c in sorted(curated_rows, key=lambda x: x["track"])
    )

    todo_table = (
        "\n".join(
            f"| {c['track']} | {c['title']} | {c['artist']} | "
            f"[[learning-notes/english-song/{c['file'].removesuffix('.md')}|笔记]] |"
            for c in todo
        )
        if todo
        else "| — | — | — | — |"
    )

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

以下 **{len(curated_rows)}** 首含歌手/歌曲简介、英中对照歌词与重点表达（播放列表 **#1–#80**，以及 #90）：

| # | 歌曲 | 歌手 | 笔记 |
| --- | --- | --- | --- |
{curated_table}

## 歌词待补充

{len(todo)} 首文档已建章，歌词仍待手动补充：

| # | 歌名 | 歌手 | 笔记 |
| --- | --- | --- | --- |
{todo_table}
"""


def main() -> None:
    items: list[dict] = json.loads(PLAYLIST_JSON.read_text(encoding="utf-8"))
    used: set[str] = set(CURATED.values())
    ids = [it["id"] for it in items]
    itunes_map = fetch_itunes(ids)

    catalog: list[dict] = []
    stats = {"updated": 0, "curated": 0, "skipped": 0}

    for item in items:
        fname = filename_for(item, used)
        path = SONG_DIR / fname
        itunes = itunes_map.get(item["id"])

        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        lyrics_section, plain_lyrics = extract_lyrics_body(existing)
        meta = meta_for_item(item, itunes, plain_lyrics)
        phrases = extract_key_phrases(plain_lyrics, item["title"])

        is_curated = curated_filename(item) is not None
        if is_curated:
            stats["curated"] += 1
        elif path.exists():
            stats["skipped"] += 1
        else:
            doc = build_full_doc(item, meta, lyrics_section, phrases, curated=False)
            path.write_text(doc, encoding="utf-8")
            stats["updated"] += 1

        lyrics_missing = (
            not plain_lyrics or "暂未自动获取" in existing
        ) and not is_curated

        catalog.append(
            {
                "track": item["track"],
                "title": item["title"],
                "artist": item["artist"],
                "file": fname,
                "curated": is_curated,
                "topics": meta["topics"],
                "genres": meta["genres"],
                "level": meta["level"],
                "era": meta["era"],
                "uses": meta["uses"],
                "topic_display": meta["topic_display"],
                "genre_display": meta["genre_display"],
                "lyrics_missing": lyrics_missing and not is_curated,
            }
        )

    CATALOG_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    README.write_text(build_readme(catalog), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
