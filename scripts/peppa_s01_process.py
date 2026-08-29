#!/usr/bin/env python3
"""Peppa Pig S01 markdown: OCR fixes, scene headings (EN·简中), vocabulary + GA IPA."""

from __future__ import annotations

import argparse
import glob
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
OCR_IL_TSV = SCRIPT_DIR / "peppa_s01_ocr_il.tsv"

DEFAULT_DIR = SCRIPT_DIR.parent / "learning-notes/tv-series/peppa-pig/s01/scripts"

EPISODE_ZH = {
    "Muddy Puddles": "泥坑",
    "Mr Dinosaur is Lost": "恐龙先生不见了",
    "Polly Parrot": "鹦鹉波莉",
    "Best Friend": "好朋友",
    "Hide and Seek": "捉迷藏",
    "The Playgroup": "幼儿园游戏小组",
    "Mummy Pig at Work": "猪妈妈上班",
    "Camping": "露营",
    "Gardening": "种菜",
    "Bicycles": "自行车",
    "The New Car": "新车",
    "Snow": "下雪",
    "Flying a Kite": "放风筝",
    "My Cousin Chloe": "堂姐克洛伊",
    "Daddy Loses his Glasses": "爸爸的眼镜不见了",
    "Hiccups": "打嗝",
    "Picnic": "野餐",
    "Mummy Pigs Birthday": "猪妈妈的生日",
    "Dressing Up": "换装游戏",
    "The School Fete": "学校游园会",
    "Musical Instruments": "乐器",
    "Babysitting": "临时保姆",
    "New Shoes": "新鞋子",
    "Ballet Lesson": "芭蕾课",
    "The Tooth Fairy": "牙仙子",
    "Treasure Hunt": "寻宝",
    "Not Very Well": "不太舒服",
    "Windy Castle": "风息堡",
    "Pancakes": "煎饼",
    "The Museum": "博物馆",
    "Secrets": "秘密",
    "Thunderstorm": "雷雨",
    "Piggy in the Middle": "中间的小猪",
    "Fancy Dress Party": "化装舞会",
    "Very Hot Day": "炎热的夏天",
    "Mister Skinnylegs": "瘦腿蜘蛛",
    "Lunch": "午餐",
    "Sleepy Princess": "贪睡公主",
    "The Tree House": "树屋",
    "Daddy Gets Fit": "爸爸的健身计划",
    "Shopping": "买东西",
    "Chloes puppet show": "克洛伊木偶戏",
    "My Birthday Party": "生日派对",
    "The Playground": "游乐场",
    "Tidying Up": "收拾房间",
    "Frogs and Worms and Butterflies": "青蛙、毛毛虫与蝴蝶",
    "Daddy Puts up a Picture": "爸爸挂画",
    "At the Beach": "海滩",
    "Cleaning the Car": "洗车",
    "Grandpa Pigs Boat": "爷爷的船",
    "Daddys Movie Camera": "爸爸的摄像机",
    "The School Play": "校园剧",
}


PHRASE_FIXES_ORDERED = (
    ("Ganny Ig!", "Granny Pig!"),
    ("Ganny Ig.", "Granny Pig."),
    ("Papa Ig!", "Grandpa Pig!"),
    ("Papa Ig.", "Grandpa Pig."),
    ("Ganggy Ig!", "Grandpa Pig!"),
    ("Ganggy Ig", "Grandpa Pig"),
    ("Baba Ig!", "Grandpa Pig!"),
    ("Baba Ig.", "Grandpa Pig."),
)


TIME_SCENE_PAT = re.compile(
    r"^(Later|Soon|Meanwhile|That night|The next day|Next day|The next morning|Later on)\.?\s*$",
    re.IGNORECASE,
)

SCENE_MARK_RE = re.compile(r"^(### Cold open|^### Scene ·|^### Closing ·)")
VOCAB_HEADER_RE = re.compile(r"^## Episode vocabulary", re.MULTILINE)


def load_il_pairs(tsv: Path) -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    if not tsv.is_file():
        return rows
    for line in tsv.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("wrong\t"):
            continue
        cols = line.split("\t")
        if len(cols) < 2:
            continue
        w, ok = cols[0].strip(), cols[1].strip()
        if w and ok and w.lower() != ok.lower():
            rows.append((w, ok))
    rows.sort(key=lambda x: (-len(x[0]), x[0]))
    return rows


def preserve_case(template: str, correct_lower: str) -> str:
    """Map OCR-corrected words back to surface form.

    When the wrong token has more than one capital (e.g. CIean, CheCk), use the
    dictionary's lowercase form. When the wrong token starts with I but the correct
    word starts with l (I/l OCR swap), also use plain lowercase (e.g. Iittle→little).
    """

    if not template or not correct_lower:
        return correct_lower
    if sum(1 for c in template if c.isupper()) > 1:
        return correct_lower
    if template[0] == "I" and correct_lower[0] == "l":
        return correct_lower
    if template.isupper() and template.isalpha() and len(template) <= 4:
        return correct_lower.capitalize()
    if template[:1].isupper():
        return correct_lower[:1].upper() + correct_lower[1:]
    return correct_lower


def sub_whole_word(text: str, wrong: str, right: str) -> str:

    def repl(m: re.Match) -> str:
        return preserve_case(m.group(0), right)

    return re.sub(rf"\b{re.escape(wrong)}\b", repl, text, flags=re.IGNORECASE)


def fix_trailing_capital_w(text: str) -> str:

    try:
        from wordfreq import zipf_frequency

    except Exception:
        zipf_frequency = None

    if not zipf_frequency:
        return text

    pat = re.compile(r"\b[A-Za-z]{2,}W\b")

    def repl(m: re.Match) -> str:
        tok = m.group(0)
        if "'" in tok or tok.endswith("'W"):
            return tok
        if tok.isupper() and len(tok) > 4:
            return tok
        cand = tok[:-1] + "w"
        if zipf_frequency(cand.lower(), "en") >= 3.45:
            return preserve_case(tok, cand.lower())
        return tok

    return pat.sub(repl, text)


def fix_odd_multicaps(text: str) -> str:

    try:
        from wordfreq import zipf_frequency

    except Exception:
        zipf_frequency = None

    if not zipf_frequency:

        return text

    def tweak(line: str) -> str:


        chars: List[str] = []

        i = 0



        while i < len(line):
            if line[i].isalpha():
                j = i + 1



                while j < len(line) and line[j].isalpha():
                    j += 1
                tok = line[i:j]
                lowers = tok.lower()


                uc = sum(
                    c.isupper()


                    for c in tok




                )


                if len(tok) >= 4 and uc >= 2 and zipf_frequency(lowers, "en") >= 3.85:






                    chars.append(lowers)



                else:






                    chars.append(tok)


                i = j




            else:






                chars.append(line[i])


                i += 1



        return "".join(chars)



    return "\n".join(tweak(ln) for ln in text.splitlines()) + ("\n" if text.endswith("\n") else "")


def ii_to_ll_residual(text: str) -> str:
    return re.sub(r"(?<=[A-Za-z])II(?=[A-Za-z])", "ll", text)


def fix_internal_capital_w(text: str) -> str:
    """e.g. doWnstairs, doWn -> down* (OCR used W for w mid-word)."""

    return re.sub(r"(?<=[a-z])W(?=[a-z])", "w", text)


def fix_wont_ocr(text: str) -> str:
    """Won't OCR often uses a capital W; also repair double-n bug from bad subs."""

    text = re.sub(r"wonn't", "won't", text, flags=re.IGNORECASE)
    return re.sub(r"(?i)\bWon['\u2019]t\b", "won't", text)


def fix_internal_single_cap_before_lower(text: str) -> str:
    """watCh -> watch, etc. (one stray capital inside a lowercase word)."""

    def repl(m: re.Match) -> str:
        return m.group(1) + m.group(2).lower() + m.group(3)

    return re.sub(r"(?<=[a-z])([a-z])([A-Z])([a-z]*)", repl, text)


def fix_line_break_then_with(text: str) -> str:

    """play\\nWith -> play\\nwith (dialogue line breaks)."""

    return re.sub(
        r"(?mi)(?<=[a-z,?!.])\s*\n(\s*)(With|Wash|Want|Walk)\b",

        lambda m: "\n" + m.group(1) + m.group(2).lower(),


        text,


    )




def fix_common_dialogue_caps(text: str) -> str:




    text = re.sub(


        r"(?i)\bI (Love|Like|Know|Think|Want|Hope)\b",

        lambda m: "I " + m.group(1).lower(),


        text,




    )
    text = re.sub(r"(?i)\b(a|the) Lot\b", lambda m: m.group(1) + " lot", text)




    text = re.sub(


        r"(?i)\bto (Look|Ask|Tell|Help|Catch|Hold)\b",


        lambda m: "to " + m.group(1).lower(),


        text,




    )




    text = re.sub(


        r"(?i)\b(a|the) Little\b",

        lambda m: m.group(1) + " little",


        text,




    )




    text = re.sub(


        r"(?i)\bAnd Look\b",


        "And look",


        text,




    )




    text = re.sub(


        r"(?i)\bisn't (Listening|Standing|Sitting)\b",


        lambda m: "isn't " + m.group(1).lower(),


        text,




    )




    text = re.sub(


        r"(?i)\b(spider|The spider) (Likes|Loves)\b",


        lambda m: m.group(1) + " " + m.group(2).lower(),


        text,




    )




    return text



def fix_family_name_verb_capitalization(text: str) -> str:


    """After Peppa/George/…, verbs like Loves/Likes should be lowercase."""


    names = ("Peppa", "George", "Mummy", "Daddy", "Everyone")


    verbs = ("Loves", "Likes", "Looks", "Love", "Look", "Listening", "Playing", "Wants")


    pat = re.compile(


        r"\b(" + "|".join(names) + r") (" + "|".join(re.escape(v) for v in verbs) + r")\b"


    )



    def repl(m: re.Match) -> str:


        return f"{m.group(1)} {m.group(2).lower()}"



    return pat.sub(repl, text)



def fix_little_sibling_phrase(text: str) -> str:
    return re.sub(
        r"\bLittle (brother|sister)\b",
        lambda m: f"little {m.group(1)}",
        text,
        flags=re.IGNORECASE,
    )


def fix_mid_sentence_clean_can_come(text: str) -> str:
    out = re.sub(
        r"(?<=[a-z,']) (Clean|Cleaned|Clear|Quick|Quickly)\b",
        lambda m: " " + m.group(1).lower(),
        text,
    )
    out = re.sub(r"(?<=[a-z]) Can\b", " can", out)
    return out


def fix_space_capital_w_common_verbs(text: str) -> str:
    """After lowercase letter or comma, ' With/Want/Wash/...' should be lowercase."""

    verbs = (
        "With",
        "Want",
        "Wants",
        "Wash",
        "Wear",
        "Water",
        "Where",
        "When",
        "While",
        "Who",
        "Why",
        "Will",
        "Wonder",
        "Worried",
        "Worry",
        "Working",
        "Watching",
        "Walk",
        "Waiting",
    )

    pat = re.compile(r"(?<=[a-z,]) (" + "|".join(re.escape(v) for v in verbs) + r")\b")

    def repl(m: re.Match) -> str:
        return " " + m.group(1).lower()

    return pat.sub(repl, text)


def capitalize_after_blank_lines(text: str) -> str:
    keys = ("can ", "guess ", "come ", "sorry ", "thank ", "goodness ", "oh,", "ooh,")



    trailing_nl = "\n" if text.endswith("\n") else ""

    prev_blank = True

    lines = []






    for line in text.splitlines(keepends=False):


        stripped = line.lstrip()



        if stripped and prev_blank:




            lw = stripped.lower()


            for key in keys:




                if lw.startswith(key):


                    cap = stripped[: len(key)].title() + stripped[len(key) :]                    


                    pad = len(line) - len(stripped)


                    line = (" " * pad) + cap


                    break

        lines.append(line)


        prev_blank = not line.strip()



    return "\n".join(lines) + trailing_nl


def strip_scene_headers(lines: List[str]) -> List[str]:
    return [ln for ln in lines if not SCENE_MARK_RE.match(ln.strip())]


def strip_vocab_section(text: str) -> str:


    mo = VOCAB_HEADER_RE.search(text)


    return (text[: mo.start()].rstrip() + "\n") if mo else text


def intro_title_pair(path: Path) -> Tuple[str, str]:
    stem = path.stem
    mo = re.search(r"S01E\d+\.(.+)$", stem)


    slug = mo.group(1) if mo else stem
    ep_en = slug.replace(".", " ")
    zh = EPISODE_ZH.get(ep_en, "本集剧情")
    return ep_en, zh


def english_label_from_chunk(lines: Sequence[str]) -> str:
    for ln in lines:
        st = ln.strip()
        if st.startswith(("**", "###")):


            continue
        ws = re.findall(r"[A-Za-z']+", st)
        if not ws:


            continue
        frag = ws[: min(6, len(ws))]
        frag[0] = frag[0].title()
        tiny = {"a", "an", "the", "to", "in", "on", "at", "and", "or", "of"}

        formatted = []

        for w in frag:


            wl = w.lower()


            formatted.append(wl if wl in tiny else (w[:1].upper() + w[1:]))


        label = " ".join(formatted)
        return label[:72] + ("…" if len(label) > 72 else "")


    return "Story beat"


def add_scene_headers(text: str, _ep_en: str, ep_zh: str) -> str:
    raw_lines = strip_scene_headers(text.splitlines())

    peppa_idxs = []

    tag_idxs = []


    for i, ln in enumerate(raw_lines):
        st = ln.strip()

        if re.match(r"^I'?m\s+Peppa\s+Pig", st):

            peppa_idxs.append(i)




        if re.match(r"^Peppa\s+pig\.?\s*$", st, re.I):

            tag_idxs.append(i)


    assembled: List[str] = []
    cursor = 0




    title_idx = None


    if raw_lines and raw_lines[0].strip().startswith("**"):
        title_idx = 0


    if title_idx is not None:


        assembled.append(raw_lines[0])


        cursor = 1

        while cursor < len(raw_lines) and not raw_lines[cursor].strip():
            assembled.append(raw_lines[cursor])


            cursor += 1




    idx_peppa = peppa_idxs[0] if peppa_idxs else None


    idx_tag = tag_idxs[0] if tag_idxs else None


    idx_outro = peppa_idxs[-1] if len(peppa_idxs) > 1 else None


    if idx_peppa is None or idx_peppa < cursor:



        body_tail = raw_lines[cursor:]



        return "\n".join(assembled + body_tail).rstrip() + "\n"


    assembled.append("### Cold open · Intro（片头自我介绍）")

    if idx_tag is not None and idx_tag >= idx_peppa:


        nl = idx_tag + 1


        while nl < len(raw_lines) and not raw_lines[nl].strip():


            nl += 1


        marker = nl + 1



        while marker < len(raw_lines) and not raw_lines[marker].strip():



            marker += 1



        cold_end = marker



    else:



        cold_end = min(idx_peppa + 14, len(raw_lines))

    main_cut = len(raw_lines)


    if idx_outro is not None and idx_outro > cold_end + 5 and idx_outro > len(raw_lines) * 0.35:
        main_cut = idx_outro


    assembled.extend(raw_lines[cursor:cold_end])


    story = raw_lines[cold_end:main_cut]

    outro = raw_lines[main_cut:]

    nonempty = sum(1 for ln in story if ln.strip())

    desired = max(3, min(5, nonempty // 42 + (1 if nonempty % 42 > 22 else 0)))

    blocks: List[List[str]] = [[]]

    blank_run = 0


    for ln in story:

        st = ln.strip()

        if TIME_SCENE_PAT.match(st) and sum(1 for x in blocks[-1] if x.strip()) > 10:
            blocks.append([])

        if not st:
            blank_run += 1

            blocks[-1].append(ln)

            if blank_run >= 3 and sum(1 for x in blocks[-1] if x.strip()) > 16:
                blocks.append([])

                blank_run = 0

            continue
        blank_run = 0

        blocks[-1].append(ln)

    blocks = [b for b in blocks if any(x.strip() for x in b)]

    if len(blocks) < desired and nonempty > 40:
        bucket: List[str] = []
        chunk_count = 0

        stride = max(20, nonempty // desired)
        idx = 0

        blocks = []
        for ln in story:
            bucket.append(ln)
            if ln.strip():
                idx += 1
            if idx and idx >= stride and len(blocks) < desired - 1:
                blocks.append(bucket)
                bucket = []
                idx = 0
        if bucket:
            blocks.append(bucket)

    if not blocks:
        blocks = [story]

    for bi, block in enumerate(blocks, start=1):
        label = english_label_from_chunk(block)
        assembled.append(f"### Scene · {label}（{ep_zh} · 段{bi}/{len(blocks)}）")
        assembled.extend(block)
        assembled.append("")

    if outro and any(x.strip() for x in outro):
        assembled.append("### Closing · Outro（片尾）")
        assembled.extend(outro)

    text_out = "\n".join(assembled).rstrip() + "\n"
    return re.sub(r"\n{4,}", "\n\n\n", text_out)


def build_vocab_md(body: str, episode_en: str) -> str:
    try:
        import eng_to_ipa as ipa_mod
        import nltk
        from nltk import pos_tag
        from nltk.corpus import stopwords, wordnet as wn
        from nltk.stem import WordNetLemmatizer
        from nltk.tokenize import word_tokenize
        from wordfreq import zipf_frequency

        for pkg in ("wordnet", "omw-1.4", "stopwords", "punkt_tab", "punkt", "averaged_perceptron_tagger_eng"):
            try:
                if pkg in {"wordnet", "stopwords"}:
                    nltk.data.find(f"corpora/{pkg}")
                else:
                    nltk.data.find(f"tokenizers/{pkg}")
            except LookupError:
                nltk.download(pkg, quiet=True)

    except Exception as exc:
        return f"## Episode vocabulary（本集词汇）\n\n_（依赖不可用：{exc}）_\n"

    plain = body
    plain = re.sub(r"^###.*$", "", plain, flags=re.MULTILINE)
    plain = plain.replace("**", " ")
    lemmer = WordNetLemmatizer()
    sw = set(stopwords.words("english"))
    sw.update(["peppa", "george", "mummy", "daddy", "pig", "pigs", "oh", "ha", "la", "um", "mm"])

    def wn_pos(tag):
        if tag.startswith("J"):
            return wn.ADJ


        if tag.startswith("V"):






            return wn.VERB

        if tag.startswith("R"):






            return wn.ADV

        return wn.NOUN

    cand: dict[str, float] = {}
    tagged = pos_tag(word_tokenize(re.sub(r"[`_]+", " ", plain)))

    for tok, tag in tagged:


        letters = "".join(ch for ch in tok if ch.isalpha())


        if len(letters) < 3:


            continue

        lw = letters.lower()


        if lw in sw:


            continue

        lemma = lemmer.lemmatize(lw, pos=wn_pos(tag))

        if lemma in sw:


            continue




        syn_n = len(wn.synsets(lemma))



        z = zipf_frequency(lemma, "en")



        score = max(0, 4.0 - z) * 2 + syn_n / 6 + len(lemma) / 12


        keep = False


        if z < 4.7:
            keep = True




        if syn_n >= 6:






            keep = True






        if len(lemma) >= 9:






            keep = True






        if keep:


            cand[lemma] = max(cand.get(lemma, 0), score)



    title_words = [x.lower() for x in re.findall(r"[A-Za-z]+", episode_en) if len(x) >= 5 and x.lower() not in sw]



    tops = sorted(cand.items(), key=lambda kv: (-kv[1], kv[0]))


    sel = []


    for lemma, _ in tops:




        if len(sel) >= 28:






            break


        sel.append(lemma)


    for tw in title_words:




        if tw not in sel and len(sel) < 32:






            sel.append(tw)


    lines = [
        "## Episode vocabulary（本集词汇）",
        "",
        "*词频 zipf 小于 4 标「低频」；义项数不少于 6 标「多义」；IPA 为 eng-to-ipa（GA）；中文优先 OMW，否则英文释义截断。*",
        "",
        "| Word | IPA (GA) | 简中义项 | 标签 |",
        "| --- | --- | --- | --- |",
    ]

    for lemma in sel:




        z = zipf_frequency(lemma, "en")



        syns = wn.synsets(lemma)


        poly = len(syns)


        try:





            ip = ipa_mod.convert(lemma)


            if isinstance(ip, list):


                ip = ip[0] if ip else ""


            ipa_s = f"/{ip}/" if ip else "—"


        except Exception:






            ipa_s = "—"



        zh = ""


        if syns:





            try:





                zh_list = syns[0].lemma_names("cmn")


                zh = zh_list[0].replace("+", "") if zh_list else syns[0].definition()





            except Exception:






                zh = syns[0].definition()


        zh_short = zh.strip()


        zh_short = zh_short[:58] + ("…" if len(zh_short) > 58 else "")


        tags = []



        if z < 4.0:






            tags.append("低频")


        if poly >= 6:






            tags.append("多义")



        if len(lemma) >= 10:


            tags.append("拼写")



        tag_s = "、".join(tags) if tags else "—"


        lines.append(f"| **{lemma}** | {ipa_s} | {zh_short} | {tag_s} |")


    lines.append("")


    return "\n".join(lines)


def pipeline_ocr(text: str, pairs: Sequence[Tuple[str, str]]) -> str:
    out = text


    for a, b in PHRASE_FIXES_ORDERED:
        out = out.replace(a, b)


    out = (
        out.replace("I'II", "I'll")
        .replace("We'II", "We'll")


        .replace("we'II", "we'll")




    )


    for w, r in pairs:


        out = sub_whole_word(out, w, r)


    out = fix_trailing_capital_w(out)


    out = fix_odd_multicaps(out)


    out = ii_to_ll_residual(out)

    out = fix_internal_capital_w(out)

    out = fix_wont_ocr(out)

    out = fix_internal_single_cap_before_lower(out)

    out = fix_line_break_then_with(out)

    out = fix_common_dialogue_caps(out)

    out = fix_space_capital_w_common_verbs(out)

    out = fix_family_name_verb_capitalization(out)

    out = fix_little_sibling_phrase(out)

    out = fix_mid_sentence_clean_can_come(out)

    out = capitalize_after_blank_lines(out)

    return out


@dataclass


class Result:




    path: Path




    changed: bool







def process_one(path: Path, do_ocr: bool, do_scenes: bool, do_vocab: bool) -> Result:




    original = path.read_text(encoding="utf-8")


    text = original


    pairs = load_il_pairs(OCR_IL_TSV)

    if do_ocr:
        text = pipeline_ocr(text, pairs)

    ep_en, ep_zh = intro_title_pair(path)

    if do_scenes or do_vocab:
        text = strip_vocab_section(text)

    if do_scenes:
        text = add_scene_headers(text, ep_en, ep_zh)

    if do_vocab:
        text = strip_vocab_section(text).rstrip() + "\n\n" + build_vocab_md(text + "\n", ep_en)


    path.write_text(text, encoding="utf-8")


    return Result(path=path, changed=text != original)


def main() -> None:
    parser = argparse.ArgumentParser()


    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR)



    parser.add_argument("--fix-ocr", action="store_true")


    parser.add_argument("--add-scenes", action="store_true")


    parser.add_argument("--vocab", action="store_true")


    parser.add_argument("--all", action="store_true")


    parser.add_argument("--report", type=Path, default=None)


    args = parser.parse_args()



    modes = any((args.fix_ocr, args.add_scenes, args.vocab, args.all))



    if args.all or not modes:


        flags = (True, True, True)




    else:


        flags = (args.fix_ocr, args.add_scenes, args.vocab)




    do_ocr, do_scenes, do_vocab = flags



    episodes = sorted(glob.glob(str(args.dir / "Peppa.Pig.S01E*.md")))



    if not episodes:


        raise SystemExit(f"No files in {args.dir}")


    summaries = []

    for fp in episodes:


        summary = process_one(Path(fp), do_ocr, do_scenes, do_vocab)



        summaries.append(f"{fp}\t{'changed' if summary.changed else 'unchanged'}")


    payload = "\n".join(summaries) + "\n"


    if args.report:


        args.report.parent.mkdir(parents=True, exist_ok=True)


        args.report.write_text(payload, encoding="utf-8")




if __name__ == "__main__":


    main()
