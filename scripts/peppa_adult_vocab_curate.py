#!/usr/bin/env python3
"""Curate Peppa S01 Episode vocabulary tables for adult learners (see subtitle-vocabulary-tables skill)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from peppa_lemma_zh_data import zh_for_lemma

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DIR = REPO / "learning-notes/tv-series/Peppa Pig S01.英文剧本"
VOCAB_HEADER = "## Episode vocabulary（本集词汇）"
EMPTY_ADULT_VOCAB_NOTE = "*本集无符合成人向收束标准的词条（剔除后无表内行）。*"
ADULT_NOTE = (
    "*成人向精简：读者默认 **简中母语、成人**，目标含工作/亲子口语。**「低频」**兼指「通用英语里仍少遇」或「**对中国成人学习者仍值得本集收束**」—后者**不等于**台词里出现次数少，也**勿唯英美 zipf / 儿童剧里常见**就删。"
    "收录笔误对照、拼写/读音/搭配难点、术语；剔除无教学价值的超高频碎片、纯拟声、迟疑音。*"
)

# Very-high-frequency lemmas an adult engineer is assumed to already know (CEFR A1–early A2 band).
# Matches `.cursor/skills/subtitle-vocabulary-tables/SKILL.md` "Exclude trivial tokens".
ADULT_VOCAB_EXCLUDE_CORE_LEMMAS: frozenset[str] = frozenset(
    {
        # pronouns & pointers
        "he",
        "she",
        "it",
        "we",
        "they",
        "you",
        "i",
        "me",
        "him",
        "her",
        "us",
        "them",
        "my",
        "your",
        "his",
        "our",
        "their",
        "this",
        "that",
        "these",
        "those",
        "there",
        "here",
         # common WH / polarity (if they ever surface as headwords)
        "what",
        "who",
        "where",
        "when",
        "why",
        "how",
        "yes",
        "no",
        "not",
        "and",
        "or",
        "but",
        # user-called-out examples + same band
        "car",
        "bus",
        "petals",
        "petal",
        # core aux / modals
        "should",
        "could",
        "can",
        "will",
        "would",
        "shall",
        "may",
        "might",
        "must",
        "am",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "having",
        "do",
        "does",
        "did",
        "doing",
        "done",
        # people / counting (when they appear as lone headwords)
        "children",
        "child",
        # skill examples + same tier verbs/adjectives
        "go",
        "goes",
        "went",
        "going",
        "gone",
        "come",
        "comes",
        "came",
        "coming",
        "get",
        "gets",
        "got",
        "getting",
        "make",
        "makes",
        "made",
        "making",
        "look",
        "looks",
        "looked",
        "looking",
        "see",
        "sees",
        "seen",
        "seeing",
        "know",
        "knows",
        "knew",
        "known",
        "knowing",
        "want",
        "wants",
        "wanted",
        "wanting",
        "like",
        "likes",
        "liked",
        "liking",
        "good",
        "bad",
        "big",
        "small",
        "new",
        "old",
        "play",
        "plays",
        "played",
        "playing",
        "eat",
        "eats",
        "ate",
        "eating",
        "drink",
        "drinks",
        "drank",
        "drinking",
        "sleep",
        "sleeps",
        "slept",
        "sleeping",
        "house",
        "home",
        "school",
        "day",
        "today",
        "now",
        "time",
        "water",
        "food",
        "dog",
        "cat",
        "red",
        "blue",
        "green",
        "yellow",
        "one",
        "two",
        "three",
        "listen",
        "listens",
        "listened",
        "listening",
        "cookie",
        "cookies",
        "muddy",
        "grandpa",
        "grandma",
        "granddad",
        "rabbit",
    }
)

# Lemmas (normalized lower) excluded from adult vocab: subtitle glitches + onomatopoeia / interjections.
ADULT_VOCAB_DROP_LEMMAS: frozenset[str] = frozenset(
    {
        "goodbye bye",
        "erm",
    }
)

ADULT_VOCAB_SOUND_OR_NONLEX_LEMMAS: frozenset[str] = frozenset(
    {
        "argh",
        "baa",
        "mew",
        "purr",
        "splish",
        "splosh",
        "ha-ha",
        "burp",
    }
)


def should_drop_adult_vocab_row(display: str, zh: str) -> bool:
    """Remove OCR phrase garbage, pure onomatopoeia, hesitation fillers, and CEFR-trivial headwords."""
    k = re.sub(r"\s+", " ", display.strip().lower())
    if k in ADULT_VOCAB_EXCLUDE_CORE_LEMMAS:
        return True
    if k in ADULT_VOCAB_DROP_LEMMAS or k in ADULT_VOCAB_SOUND_OR_NONLEX_LEMMAS:
        return True
    z = (zh or "").strip()
    if any(x in z for x in ("字幕碎片", "字幕粘连", "连写碎片")):
        return True
    return False

ROW_RE = re.compile(
    r"^\| (\*\*[^*|]+\*\*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$"
)

# eng-to-ipa misses or returns * for these lemmas (GA-ish).
MANUAL_IPA: dict[str, str] = {
    "sunshade": "/ˈsʌnˌʃeɪd/",
    "lifejackets": "/ˈlaɪfˌʤækɪts/",
    "waterhog": "/ˈwɔtərˌhɔɡ/",
    "seadog": "/ˈsiˌdɔɡ/",
    "hearties": "/ˈhɑrtiz/",
    "ayeaye": "/ˈaɪˌaɪ/",
    "picnicblanket": "/ˈpɪknɪkˌblæŋkɪt/",
    "piggyinthemiddle": "/ˈpɪɡi ɪn ðə ˈmɪdəl/",
    "sandcastle": "/ˈsændˌkæsəl/",
    "playgroup": "/ˈpleɪˌɡruːp/",
    "baa": "/bɑː/",
    "teatime": "/ˈtiːˌtaɪm/",
    "hiccupping": "/ˈhɪkəpɪŋ/",
    "peppa": "/ˈpɛpə/",
}

# Subtitle / OCR surface → lemma hint for IPA + 简中 (extend as needed).
TYPO_LEMMA: dict[str, str] = {
    "dinesaw": "dinosaur",
    "bicycies": "bicycles",
    "peddiing": "pedalling",
    "tricycie": "tricycle",
    "sandcastie": "sandcastle",
    "spiashing": "splashing",
    "poiishing": "polishing",
    "skinnylegs": "skinny legs",
    "waterwings": "water wings",
    "casties": "castles",
    "toweis": "towels",
    "beachbag": "beach bag",
    "paddie": "paddling",
    "afioat": "afloat",
    "rumbiing": "rumbling",
    "fiipping": "flipping",
    "hoopia": "hoopla",
    "spoiiing": "spoiling",
    "siippers": "slippers",
    "iipstick": "lipstick",
    "fooied": "fooled",
    "iistens": "listens",
    "grandp": "grandpa",
    "snowbaii": "snowball",
    "iceiolly": "ice lolly",
    "paddiing": "paddling",
    "piaygroup": "playgroup",
    "thereii": "there",
    "petais": "petals",
    "staik": "stalk",
    "heii": "he",
    "briyant": "brilliant",
    "iemonade": "lemonade",
    "sieepy": "sleepy",
    "booksheif": "bookshelf",
    "trycytops": "triceratops",
    "mapread": "map reading",
    "mapreading": "map reading",
    "coookies": "cookies",
    "pedais": "pedals",
    "pedai": "pedal",
    "pressups": "press-ups",
    "horticuiturist": "horticulturist",
    "iceiandic": "Icelandic",
    "dariings": "darlings",
    "iobbing": "lobbing",
    "iopping": "lopping",
    "acrodion": "accordion",
    "couid": "could",
    "shouid": "should",
    "horray": "hooray",
    "demiplier": "demi-plié",
    "childen": "children",
    "jete": "jeté",
    "chloes": "Chloe's",
    "gazzelle": "gazelle",
    "gazzellemg": "gazelle",
    "photoes": "photos",
    "goona": "gonna",
    "parcei": "parcel",
    "wheeibarrow": "wheelbarrow",
    "fiowerpots": "flower pots",
    "fiowerbed": "flower bed",
    "iuckiest": "luckiest",
    "piggyinthemiddle": "piggy in the middle",
    "picnicblanket": "picnic blanket",
    "brownbear": "brown bear",
    "lifejackets": "life jackets",
    "seadog": "sea dog",
    "hearties": "hearties",
    "ayeaye": "aye-aye",
    "daddys": "daddy's",
    "cooky": "cookie",
    "everyway": "every way",
    "wriggie": "wriggly",
    "meion": "melon",
    "pigetty": "piggy",
    "goodthat": "good that",
    "mistyo": "misty",
    "heiper": "helper",
    "rabbitrr": "rabbit",
    "rabbitmr": "rabbit",
    "georgeg": "George",
    "scarrier": "scarier",
    "mazy": "mazy",
    "meits": "melts",
    "oiiy": "oily",
    "pigthis": "pig this",
    "doggoodbye": "dog goodbye",
    "goodbyebye": "goodbye bye",
    "pigyour": "pig your",
    "oclock": "o'clock",
    "piaster": "plaster",
    "youii": "you",
    "mysterio": "mysterious",
    "tickies": "tickles",
    "spiish": "splish",
    "spiosh": "splosh",
    "welldone": "well done",
    "mihateeze": "might as well",
    "huray": "hooray",
    "teatime": "teatime",
    "spolly": "Polly",
    "garandpa": "grandpa",
    "granpa": "grandpa",
    "tuckin": "tuck in",
    "peppap": "Peppa",
    "demipliernow": "demi-plié",
    "jumppetit": "petit saut",
    "hograce": "arms graceful",
    "daning": "dancing",
    "byebye": "bye-bye",
    "foodspaghetti": "food spaghetti",
    "goodnow": "good now",
    "sawtechdine": "dinosaur",
    "dinedine": "dinosaur",
    "welldine": "dinosaur",
    "sawdone": "dinosaur",
    "sawtiff": "dinosaur",
    "dedine": "dinosaur",
    "sawsaw": "saw",
    "garagehe": "garage",
    "carcan": "car",
    "toodon": "too, don't you",
    "yesbut": "yes, but",
    "arrhg": "argh",
    "gavesgate": "Gavesgate",
    "hahhah": "ha-ha",
    "gpp": "Grandpa Pig",
    "gnp": "Granny Pig",
}


def load_il_map(tsv: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not tsv.is_file():
        return out
    for line in tsv.read_text(encoding="utf-8").splitlines():
        if "\t" not in line or line.startswith("#") or line.startswith("wrong\t"):
            continue
        a, b = line.split("\t", 2)[:2]
        a, b = a.strip(), b.strip()
        if a and b:
            out[a.lower()] = b
    return out


def word_cell_token(cell: str) -> str:
    m = re.match(r"^\*\*(.+)\*\*$", cell.strip())
    return m.group(1).strip() if m else cell.strip()


def is_noise_token(w: str) -> bool:
    """Stretched interjections / growls — excluded from adult table."""
    s = w.strip().lower()
    if len(s) < 2:
        return False
    if re.search(r"(.)\1{2,}", s):
        return True
    if re.fullmatch(r"g+r{2,}[oh]*", s):
        return True
    if re.fullmatch(r"b+r{2,}", s):
        return True
    if re.match(r"^a+r+g+h*$", s):
        return True
    if re.match(r"^(w+h+)(a+|e+|o+)*[h!]*$", s) and len(s) >= 4:
        return True
    if re.match(r"^w+h+e+$", s):
        return True
    if re.match(r"^w+a+h+$", s):
        return True
    if re.match(r"^w+o+o+[ah]*$", s) and len(s) >= 5:
        return True
    if re.match(r"^o+h+$", s) and len(s) >= 4:
        return True
    if re.match(r"^a+h+$", s) and len(s) >= 4:
        return True
    if re.match(r"^m+h+$", s) and len(s) >= 4:
        return True
    if re.match(r"^h+u+h+$", s):
        return True
    if re.match(r"^h+m+$", s) and len(s) >= 4:
        return True
    if re.match(r"^s+h{3,}", s):
        return True
    if re.match(r"^r+a+r+$", s) and len(s) >= 5:
        return True
    if re.match(r"^y+i+p+e+", s):
        return True
    if re.match(r"^e+e+k+!*$", s):
        return True
    if re.match(r"^e+e+u+r+g+h", s):
        return True
    if re.match(r"^h+u+h+h+$", s):
        return True
    if re.match(r"^o+o+f+$", s):
        return True
    if re.match(r"^a+a+a+g+h+$", s):
        return True
    if re.match(r"^r+r+r+", s) and len(s) >= 5 and "o" not in s:
        return True
    if re.match(r"^d+d+d+y$", s):
        return True
    if re.search(r"(gg|dd|mr|np|mp|pp|md|dp|mg|ntp)$", s) and 5 <= len(s) <= 14:
        if s not in {"egg", "add", "grass", "class", "dress", "glass", "press"}:
            return True
    return False


def passes_inclusion_gate(tags: str) -> bool:
    t = tags.strip()
    if not t or t in ("—", "-"):
        return False
    if "多义" in t and not any(
        x in t for x in ("低频", "拼写", "易读错", "有难度", "术语", "技术", "亲子")
    ):
        return False
    return any(x in t for x in ("低频", "拼写", "易读错", "有难度", "术语", "技术", "亲子"))


TAG_ORDER = ["低频", "拼写", "易读错", "有难度", "多义", "术语", "技术", "亲子"]


def resolve_display_lemma(token: str, il_map: dict[str, str]) -> str:
    low = token.strip().lower()
    if low in TYPO_LEMMA:
        return TYPO_LEMMA[low]
    if low in il_map:
        il_ok = il_map[low]
        if il_ok.lower().replace(" ", "") != low.replace(" ", ""):
            return il_ok
    return token.strip()


def _ipa_score(ipa: str) -> int:
    s = (ipa or "").strip()
    if not s or s == "—":
        return 0
    if "*" in s:
        return 1
    return 2


def _better_ipa(a: str, b: str) -> str:
    return a if _ipa_score(a) >= _ipa_score(b) else b


def ipa_for_lemma(display: str) -> str:
    d = display.strip()
    if not d:
        return "—"
    if " " in d:
        ph = try_ipa_phrase(d)
        if ph:
            return ph
    for cand in (d.replace(" ", "-"), d):
        t = try_ipa(cand)
        if t:
            return t
    return "—"


def merge_tag_strings(a: str, b: str) -> str:
    bucket: set[str] = set()
    for part in (a, b):
        for x in part.replace("，", "、").split("、"):
            x = x.strip()
            if x:
                bucket.add(x)
    ordered = [x for x in TAG_ORDER if x in bucket]
    rest = sorted(bucket - set(TAG_ORDER))
    return "、".join(ordered + rest)


def lemma_zh_normalize_body(body: List[str], il_map: dict[str, str]) -> List[str]:
    header: List[str] = []
    rows_in: List[Tuple[str, str, str, str]] = []
    for ln in body:
        if "| Word |" in ln or "| --- |" in ln:
            header.append(ln)
            continue
        mo = ROW_RE.match(ln)
        if not mo:
            continue
        rows_in.append(mo.groups())

    order: List[str] = []
    merged: Dict[str, Tuple[str, str, str, str]] = {}

    for w, ipa, gloss, tags in rows_in:
        tok = word_cell_token(w)
        display = resolve_display_lemma(tok, il_map)
        ipa_new = ipa_for_lemma(display)
        zh = zh_for_lemma(display, gloss)
        if should_drop_adult_vocab_row(display, zh):
            continue
        tag_s = tags.strip()
        k = re.sub(r"\s+", " ", display.strip().lower())
        if k not in merged:
            order.append(k)
            merged[k] = (display, ipa_new, zh, tag_s)
        else:
            d0, i0, z0, t0 = merged[k]
            ip = _better_ipa(i0, ipa_new)
            zh_merged = z0
            if len(zh) > len(zh_merged):
                zh_merged = zh
            if "（请补义项" in zh_merged and "（请补义项" not in zh:
                zh_merged = zh
            merged[k] = (d0, ip, zh_merged, merge_tag_strings(t0, tag_s))

    out: List[str] = list(header)
    for k in order:
        display, ipa_s, zh, tag_s = merged[k]
        out.append(f"| **{display}** | {ipa_s} | {zh} | {tag_s} |")
    return out


def normalize_preamble_adult_note(preamble: List[str]) -> List[str]:
    """Keep Episode vocabulary preamble in sync with ADULT_NOTE policy text."""
    out: List[str] = []
    replaced = False
    for pl in preamble:
        if (not replaced) and ("成人向精简" in pl):
            out.append(ADULT_NOTE)
            replaced = True
            continue
        if replaced and ("成人向精简" in pl):
            continue
        out.append(pl)
    return out


def lemma_zh_curated_file(path: Path, il_map: dict[str, str], dry_run: bool) -> Tuple[bool, str]:
    """Replace typo surfaces with canonical lemmas + 简中 glosses; merge duplicate lemmas."""
    all_lines = path.read_text(encoding="utf-8").splitlines(keepends=False)
    try:
        vidx = all_lines.index(VOCAB_HEADER)
    except ValueError:
        return False, "no vocab header"
    if not already_curated(all_lines, vidx + 1):
        return False, "not curated"
    k = vidx + 1
    while k < len(all_lines) and not all_lines[k].strip().startswith("| Word |"):
        k += 1
    if k >= len(all_lines):
        # Curated block with no markdown table (e.g. only ADULT_NOTE + empty-vocab line).
        end_idx = len(all_lines)
        for i in range(vidx + 1, len(all_lines)):
            if all_lines[i].startswith("## ") and all_lines[i].strip() != VOCAB_HEADER:
                end_idx = i
                break
        preamble = normalize_preamble_adult_note(all_lines[vidx + 1 : end_idx])
        new_all = all_lines[: vidx + 1] + preamble + all_lines[end_idx:]
        new_text = "\n".join(new_all)
        if not new_text.endswith("\n"):
            new_text += "\n"
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
        return True, "preamble only (no table)"
    preamble = normalize_preamble_adult_note(all_lines[vidx + 1 : k])
    body, end_idx = parse_vocab_block(all_lines, k)
    if len(body) < 2:
        return False, "empty table"
    new_body = lemma_zh_normalize_body(body, il_map)
    if len(new_body) <= 2:
        new_all = (
            all_lines[: vidx + 1]
            + preamble
            + ["", EMPTY_ADULT_VOCAB_NOTE, ""]
            + all_lines[end_idx:]
        )
        nrows = 0
    else:
        new_all = all_lines[: vidx + 1] + preamble + new_body + all_lines[end_idx:]
        nrows = len(new_body) - 2

    new_text = "\n".join(new_all)
    if not new_text.endswith("\n"):
        new_text += "\n"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True, f"lemma+zh rows {nrows}"


def try_ipa(lemma: str) -> Optional[str]:
    low = lemma.strip().lower()
    if low in MANUAL_IPA:
        return MANUAL_IPA[low]
    try:
        import eng_to_ipa as ipa_mod

        ip = ipa_mod.convert(lemma)
        if isinstance(ip, list):
            ip = ip[0] if ip else ""
        if not ip or "*" in str(ip):
            return None
        return f"/{ip}/"
    except Exception:
        return None


def try_ipa_phrase(lemma: str) -> Optional[str]:
    """Multi-word lemmas: try each token, concatenate IPA."""
    parts = lemma.split()
    if len(parts) == 1:
        return try_ipa(parts[0])
    ips: List[str] = []
    for p in parts:
        one = try_ipa(p)
        if not one:
            return None
        ips.append(one.strip("/"))
    return "/" + " ".join(ips) + "/"


def ipa_needs_fix(ipa_s: str) -> bool:
    s = ipa_s.strip()
    return s == "—" or "*/" in s or "*" in s


def refine_row(
    word_cell: str,
    ipa: str,
    gloss: str,
    tags: str,
    il_map: dict[str, str],
) -> Tuple[str, str, str, str]:
    token = word_cell_token(word_cell)
    low = token.lower()
    lemma: Optional[str] = None
    if low in TYPO_LEMMA:
        lemma = TYPO_LEMMA[low]
    elif low in il_map:
        il_ok = il_map[low]
        if il_ok.lower().replace(" ", "") != low.replace(" ", ""):
            lemma = il_ok

    ipa_s = ipa.strip()

    if lemma and ipa_needs_fix(ipa_s):
        fixed = try_ipa_phrase(lemma) or try_ipa(lemma.replace(" ", "-"))
        if fixed:
            ipa_s = fixed

    if ipa_needs_fix(ipa_s):
        for cand in (lemma, low):
            if not cand:
                continue
            fixed = try_ipa_phrase(cand) if " " in cand else try_ipa(cand)
            if fixed:
                ipa_s = fixed
                break

    if lemma and " " in lemma:
        ph = try_ipa_phrase(lemma)
        if ph:
            ipa_s = ph

    gloss_s = gloss.strip()
    if lemma and (not gloss_s or len(gloss_s) < 12):
        if "字幕" not in gloss_s and "笔误" not in gloss_s:
            gloss_s = f"字幕笔误；正字 **{lemma}**"
    return word_cell, ipa_s, gloss_s, tags.strip()


def parse_vocab_block(lines: Sequence[str], start: int) -> Tuple[List[str], int]:
    body: List[str] = []
    i = start
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("| Word |") or ln.strip().startswith("| --- |"):
            body.append(ln)
            i += 1
            continue
        if ln.strip().startswith("|") and ROW_RE.match(ln):
            body.append(ln)
            i += 1
            continue
        break
    return body, i


def curate_table_rows(
    body_lines: List[str],
    il_map: dict[str, str],
) -> List[str]:
    header: List[str] = []
    rows_out: List[str] = []
    for ln in body_lines:
        if "| Word |" in ln or "| --- |" in ln:
            header.append(ln)
            continue
        mo = ROW_RE.match(ln)
        if not mo:
            continue
        word_c, ipa, gloss, tags = mo.groups()
        tags_s = tags.strip()
        if not passes_inclusion_gate(tags_s):
            continue
        tok = word_cell_token(word_c)
        if is_noise_token(tok):
            continue
        word_c, ipa, gloss, tags_s = refine_row(word_c, ipa, gloss, tags_s, il_map)
        disp = resolve_display_lemma(tok, il_map)
        zh_row = zh_for_lemma(disp, gloss)
        if should_drop_adult_vocab_row(disp, zh_row):
            continue
        rows_out.append(f"| {word_c} | {ipa} | {gloss} | {tags_s} |")
    return header + rows_out


def already_curated(lines: List[str], idx_after_header: int) -> bool:
    i = idx_after_header
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and "成人向精简" in lines[i]:
        return True
    return False


def process_file(path: Path, il_map: dict[str, str], dry_run: bool) -> Tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    all_lines = text.splitlines(keepends=False)
    try:
        vidx = all_lines.index(VOCAB_HEADER)
    except ValueError:
        return False, "no vocab header"

    if already_curated(all_lines, vidx + 1):
        return False, "already curated"

    k = vidx + 1
    while k < len(all_lines) and not all_lines[k].strip().startswith("| Word |"):
        k += 1
    if k >= len(all_lines):
        return False, "no table"

    body, end_idx = parse_vocab_block(all_lines, k)
    if len(body) < 3:
        return False, "empty table"
    old_data_rows = len(body) - 2
    new_body = curate_table_rows(body, il_map)
    new_data_rows = max(0, len(new_body) - 2)

    new_all = (
        all_lines[: vidx + 1]
        + ["", ADULT_NOTE, ""]
        + new_body
        + all_lines[end_idx:]
    )
    new_text = "\n".join(new_all)
    if not new_text.endswith("\n"):
        new_text += "\n"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True, f"rows {old_data_rows} -> {new_data_rows}"


def refine_curated_file(path: Path, il_map: dict[str, str], dry_run: bool) -> Tuple[bool, str]:
    """Re-run refine_row on an already adult-curated table (IPA / 简中 fixes)."""
    all_lines = path.read_text(encoding="utf-8").splitlines(keepends=False)
    try:
        vidx = all_lines.index(VOCAB_HEADER)
    except ValueError:
        return False, "no vocab header"
    if not already_curated(all_lines, vidx + 1):
        return False, "not curated"
    k = vidx + 1
    while k < len(all_lines) and not all_lines[k].strip().startswith("| Word |"):
        k += 1
    if k >= len(all_lines):
        # Curated block with no markdown table (e.g. only ADULT_NOTE + empty-vocab line).
        end_idx = len(all_lines)
        for i in range(vidx + 1, len(all_lines)):
            if all_lines[i].startswith("## ") and all_lines[i].strip() != VOCAB_HEADER:
                end_idx = i
                break
        preamble = normalize_preamble_adult_note(all_lines[vidx + 1 : end_idx])
        new_all = all_lines[: vidx + 1] + preamble + all_lines[end_idx:]
        new_text = "\n".join(new_all)
        if not new_text.endswith("\n"):
            new_text += "\n"
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
        return True, "preamble only (no table)"
    preamble = normalize_preamble_adult_note(all_lines[vidx + 1 : k])
    body, end_idx = parse_vocab_block(all_lines, k)
    if len(body) < 2:
        return False, "empty table"
    new_body: List[str] = []
    for ln in body:
        if "| Word |" in ln or "| --- |" in ln:
            new_body.append(ln)
            continue
        mo = ROW_RE.match(ln)
        if not mo:
            continue
        w, i, g, t = mo.groups()
        w, i, g, t = refine_row(w, i, g, t, il_map)
        disp = resolve_display_lemma(word_cell_token(w), il_map)
        if should_drop_adult_vocab_row(disp, zh_for_lemma(disp, g)):
            continue
        new_body.append(f"| {w} | {i} | {g} | {t} |")
    new_all = all_lines[: vidx + 1] + preamble + new_body + all_lines[end_idx:]
    new_text = "\n".join(new_all)
    if not new_text.endswith("\n"):
        new_text += "\n"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True, f"refined {len(new_body) - 2} rows"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--lemma-zh",
        action="store_true",
        help="Canonical lemmas + 简中 glosses + dedupe (adult tables only).",
    )
    ap.add_argument(
        "--refine-only",
        action="store_true",
        help="Re-run IPA/gloss hints on curated tables without lemma-zh merge.",
    )
    args = ap.parse_args()
    il_path = REPO / "scripts/peppa_s01_ocr_il.tsv"
    il_map = load_il_map(il_path)
    updated = 0
    for path in sorted(args.dir.glob("Peppa.Pig.S01E*.md")):
        if args.lemma_zh:
            ok, msg = lemma_zh_curated_file(path, il_map, args.dry_run)
        elif args.refine_only:
            ok, msg = refine_curated_file(path, il_map, args.dry_run)
        else:
            ok, msg = process_file(path, il_map, args.dry_run)
        if ok:
            updated += 1
            print(f"OK {path.name}: {msg}")
        else:
            print(f"-- {path.name}: {msg}")
    print(f"Done. Updated {updated} files.")


if __name__ == "__main__":
    main()
