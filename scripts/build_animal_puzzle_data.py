#!/usr/bin/env python3
"""Build the browser data used by the parent-child animal memory game."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_MD = (
    REPO_ROOT
    / "learning-notes/parenting-english/vocabulary/parenting-animals-vocab.md"
)
ASSETS_DIR = REPO_ROOT / "learning-notes/parenting-english/assets/animals"
MANIFEST_PATH = ASSETS_DIR / "animals-manifest.yml"
JSON_PATH = REPO_ROOT / "learning-notes/assets/data/animal-puzzle.json"
HTML_PATH = (
    REPO_ROOT
    / "learning-notes/parenting-english/games-and-activities/animal-puzzle.html"
)

CATEGORIES = {
    "cat-pets": ("A", "宠物", "Pets"),
    "cat-farm": ("B", "农场", "Farm"),
    "cat-birds": ("C", "鸟类", "Birds"),
    "cat-bugs": ("D", "昆虫", "Bugs"),
    "cat-reptile": ("E", "爬行与两栖", "Reptiles & amphibians"),
    "cat-marine": ("F", "海洋", "Marine animals"),
    "cat-land": ("G", "陆地野生", "Wild land animals"),
    "cat-prehistoric": ("H", "史前动物", "Prehistoric animals"),
    "cat-myth": ("I", "神话动物", "Mythical animals"),
}

ANCHOR_RE = re.compile(r'<a\s+id="(?P<id>cat-[^"]+)"></a>')
WORD_RE = re.compile(r"`(?P<word>[^`]+)`")
IMAGE_RE = re.compile(r"\.\./assets/animals/(?P<file>[^)]+\.webp)")
US_IPA_RE = re.compile(r"美\s*:\s*(?P<ipa>/[^/]+/)")
ANY_IPA_RE = re.compile(r"(?P<ipa>/[^/]+/)")
EMBED_RE = re.compile(
    r"(const EMBEDDED_DATA = )\{.*?\n\s*\};",
    flags=re.DOTALL,
)


def clean_cell(value: str) -> str:
    """Remove light Markdown decoration while preserving readable content."""
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\[看图\]\([^)]+\)\{[^}]*\}", "", value)
    value = value.replace("`", "").replace("**", "")
    return re.sub(r"\s+", " ", value).strip()


def short_gloss(gloss: str) -> str:
    gloss = clean_cell(gloss)
    gloss = re.sub(r"^[a-z]+\.\s*", "", gloss, flags=re.IGNORECASE)
    gloss = re.sub(r"^\([^)]*\)\s*", "", gloss)
    return re.split(r"[；;，,（(]|\s+[a-z]+\.\s*", gloss, maxsplit=1)[0].strip()


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def preferred_ipa(value: str) -> str:
    match = US_IPA_RE.search(value) or ANY_IPA_RE.search(value)
    return match.group("ipa") if match else clean_cell(value)


def parse_vocab() -> list[dict[str, str]]:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    available = manifest.get("animals") or {}
    current: tuple[str, str, str] | None = None
    entries: list[dict[str, str]] = []

    for line in VOCAB_MD.read_text(encoding="utf-8").splitlines():
        anchor = ANCHOR_RE.search(line)
        if anchor:
            current = CATEGORIES.get(anchor.group("id"))
            continue
        if current is None or not line.startswith("|") or "`" not in line:
            continue

        cells = split_row(line)
        if len(cells) < 7:
            continue
        word_match = WORD_RE.search(cells[2])
        image_match = IMAGE_RE.search(cells[2])
        if not word_match or not image_match:
            continue

        word = word_match.group("word").strip()
        image_file = image_match.group("file")
        slug = Path(image_file).stem
        info = available.get(slug) or {}
        if (
            info.get("status") != "ok"
            or not (ASSETS_DIR / image_file).is_file()
        ):
            continue

        key, zh_label, en_label = current
        meaning = clean_cell(cells[4])
        idiom = clean_cell(cells[6])
        if idiom in {"", "—", "-"}:
            idiom = "暂无常见的亲子友好表达"
        entries.append(
            {
                "id": f"{key.lower()}-{re.sub(r'[^a-z0-9]+', '-', word.lower()).strip('-')}",
                "en": word,
                "zh": short_gloss(meaning),
                "ipa": preferred_ipa(cells[3]),
                "meaning": meaning,
                "hint": clean_cell(cells[5]),
                "idiom": idiom,
                "category": key,
                "categoryZh": zh_label,
                "categoryEn": en_label,
                "image": f"../assets/animals/{image_file}",
                "difficulty": clean_cell(cells[0]),
            }
        )
    return entries


def payload() -> dict:
    animals = parse_vocab()
    counts = {
        key: sum(animal["category"] == key for animal in animals)
        for key, _, _ in CATEGORIES.values()
    }
    return {
        "version": 1,
        "categories": [
            {"id": key, "zh": zh, "en": en, "count": counts[key]}
            for key, zh, en in CATEGORIES.values()
            if counts[key]
        ],
        "animals": animals,
    }


def write_if_changed(path: Path, text: str) -> None:
    # mkdocs serve watches docs_dir; rewriting identical files triggers a rebuild loop.
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def write_data(data: dict, sync_html: bool = True) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2)
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_if_changed(JSON_PATH, rendered + "\n")

    if sync_html and HTML_PATH.is_file():
        html = HTML_PATH.read_text(encoding="utf-8")
        updated, count = EMBED_RE.subn(
            lambda match: match.group(1) + rendered + ";", html, count=1
        )
        if not count:
            raise RuntimeError(f"EMBEDDED_DATA marker not found in {HTML_PATH}")
        write_if_changed(HTML_PATH, updated)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-html", action="store_true", help="Only write the JSON data file."
    )
    args = parser.parse_args()
    data = payload()
    write_data(data, sync_html=not args.no_html)
    print(
        f"Wrote {len(data['animals'])} animals across "
        f"{len(data['categories'])} categories."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
