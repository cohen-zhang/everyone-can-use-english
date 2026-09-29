#!/usr/bin/env python3
"""Add glightbox "看图" links to the animal vocab table from animals-manifest.yml.

Idempotent: existing `.animal-pic` links in the Word column are removed and
re-added, so re-run after every download batch.

  python3 scripts/link_animal_images.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from download_animal_images import (  # noqa: E402
    ASSETS_DIR,
    MANIFEST_PATH,
    SKIP_WORDS,
    VOCAB_MD,
    slugify,
)

REL_ASSETS = "../assets/animals"
ROW_RE = re.compile(r"^(\|\s*[^|]+\|\s*[^|]+\|\s*)(`(?P<word>[^`]+)`)(?P<extra>[^|]*)(\|\s*[^|]+\|\s*(?P<gloss>[^|]*)\|.*)$")
EXISTING_LINK_RE = re.compile(r"\s*·?\s*\[看图\]\([^)]*\)\{[^}]*animal-pic[^}]*\}")


def short_gloss(gloss: str) -> str:
    """First Chinese sense from the 释义 cell, e.g. 'n. 狗；[美俚]…' -> '狗'."""
    g = unicodedata.normalize("NFKC", gloss).strip()  # PDF radicals: ⼩ -> 小
    g = re.sub(r"^[a-z]+\.\s*", "", g)
    g = re.split(r"[；;，,（(]", g)[0]
    return g.replace('"', "").strip()


def main() -> int:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    animals = manifest.get("animals") or {}
    ok = {slug for slug, info in animals.items() if (info or {}).get("status") == "ok" and (ASSETS_DIR / f"{slug}.webp").exists()}

    lines = VOCAB_MD.read_text(encoding="utf-8").split("\n")
    linked = 0
    for i, line in enumerate(lines):
        m = ROW_RE.match(line)
        if not m:
            continue
        word = m.group("word")
        extra = EXISTING_LINK_RE.sub("", m.group("extra"))
        slug = slugify(word)
        if word.lower() not in SKIP_WORDS and slug in ok:
            desc = f"{word} — {short_gloss(m.group('gloss'))}"
            extra = (
                f" · [看图]({REL_ASSETS}/{slug}.webp)"
                f'{{ .glightbox .animal-pic data-type="image" data-description="{desc}" }}'
                f"{extra.rstrip()} "
            )
            linked += 1
        lines[i] = f"{m.group(1)}{m.group(2)}{extra}{m.group(5)}"
    VOCAB_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Linked {linked} vocab rows ({len(ok)} images available).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
