#!/usr/bin/env python3
"""Download kid-friendly animal photos for the parenting animal vocab pages.

Parses learning-notes/parenting-english/vocabulary/parenting-animals-vocab.md,
keeps categories A–I (creatures), and writes WebP files plus
animals-manifest.yml / ATTRIBUTION.md under
learning-notes/parenting-english/assets/animals/.

Sources (commercial-friendly licenses only: CC0 / PD / CC BY / CC BY-SA):
  1. Wikimedia Commons file used as the English Wikipedia article lead image
  2. Wikimedia Commons search
  3. iNaturalist taxon default photo or top-voted observation photo (fallback)

Examples:
  python3 scripts/download_animal_images.py --only donkey,dolphin,bear
  python3 scripts/download_animal_images.py --star-only
  python3 scripts/download_animal_images.py
  python3 scripts/download_animal_images.py --dry-run
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import time
from pathlib import Path

import requests
import yaml
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_MD = REPO_ROOT / "learning-notes/parenting-english/vocabulary/parenting-animals-vocab.md"
ASSETS_DIR = REPO_ROOT / "learning-notes/parenting-english/assets/animals"
MANIFEST_PATH = ASSETS_DIR / "animals-manifest.yml"
ATTRIBUTION_PATH = ASSETS_DIR / "ATTRIBUTION.md"

INAT_API = "https://api.inaturalist.org/v1"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = (
    "EveryoneCanUseEnglish-AnimalImages/1.0 "
    "(personal English learning notes; github.com/cohen-zhang/everyone-can-use-english)"
)

OK_LICENSES = {"cc0", "pd", "cc-by", "cc-by-sa"}
MAX_EDGE = 800
WEBP_QUALITY = 82

# Non-creature / abstract / adult-slang rows that may appear inside A–I tables.
SKIP_WORDS = frozenset(
    w.lower()
    for w in {
        "aquarium", "honey", "grain", "wheat", "nest", "claw", "paw", "fin",
        "shell", "toes", "cocoon", "bloom", "acorn", "hop", "howl", "scamper",
        "mammal", "mammalian", "reptile", "amphibian", "avian", "canine",
        "feline", "murine", "primate", "rodent", "insect", "bug", "critter",
        "pest", "vertebrate", "homo", "seafood", "sushi", "ruminate", "musk",
        "cattle", "oxen", "crickets", "mice", "bitch", "pussy", "cock",
    }
)

# Vocab spelling -> canonical image slug.
ALIASES: dict[str, str] = {
    "racoon": "raccoon",
    "ladybird": "ladybug",
    "Chihuahua": "chihuahua",
    "Labrador": "labrador-retriever",
    "tigress": "tiger",
    "grizzly": "grizzly-bear",
    "chimp": "chimpanzee",
    "rhino": "rhinoceros",
    "jay": "blue-jay",
    "martin": "purple-martin",
    "kitty": "kitten",
    "bunny": "rabbit",
    "blowfish": "pufferfish",
}

# slug -> iNaturalist taxon name (scientific names keep results precise).
INAT_TAXA: dict[str, str] = {
    "dog": "Canis familiaris",
    "puppy": "Canis familiaris",
    "cat": "Felis catus",
    "kitten": "Felis catus",
    "hamster": "Mesocricetus auratus",
    "rabbit": "Oryctolagus cuniculus",
    "canary": "Serinus canaria",
    "chicken": "Gallus gallus",
    "hen": "Gallus gallus",
    "rooster": "Gallus gallus",
    "cow": "Bos taurus",
    "bull": "Bos taurus",
    "duck": "Anas platyrhynchos",
    "horse": "Equus caballus",
    "goat": "Capra hircus",
    "pig": "Sus scrofa domesticus",
    "sheep": "Ovis aries",
    "lamb": "Ovis aries",
    "buffalo": "Bison bison",
    "boar": "Sus scrofa",
    "mule": "Equus asinus × caballus",
    "donkey": "Equus asinus",
    "turkey": "Meleagris gallopavo",
    "goose": "Anser anser",
    "bird": "Erithacus rubecula",
    "owl": "Tyto alba",
    "dove": "Zenaida macroura",
    "penguin": "Aptenodytes forsteri",
    "parrot": "Ara macao",
    "pigeon": "Columba livia",
    "eagle": "Haliaeetus leucocephalus",
    "swan": "Cygnus olor",
    "flamingo": "Phoenicopterus roseus",
    "seagull": "Larus argentatus",
    "swallow": "Hirundo rustica",
    "crow": "Corvus brachyrhynchos",
    "robin": "Turdus migratorius",
    "blue-jay": "Cyanocitta cristata",
    "peacock": "Pavo cristatus",
    "sparrow": "Passer domesticus",
    "purple-martin": "Progne subis",
    "bee": "Apis mellifera",
    "ant": "Camponotus pennsylvanicus",
    "butterfly": "Danaus plexippus",
    "ladybug": "Coccinella septempunctata",
    "spider": "Araneus diadematus",
    "scorpion": "Centruroides vittatus",
    "caterpillar": "Papilio machaon",
    "moth": "Actias luna",
    "wasp": "Polistes dominula",
    "worm": "Lumbricus terrestris",
    "beetle": "Lucanus cervus",
    "hornet": "Vespa crabro",
    "dragonfly": "Anax junius",
    "cricket": "Acheta domesticus",
    "grasshopper": "Dissosteira carolina",
    "cicada": "Magicicada septendecim",
    "mosquito": "Aedes aegypti",
    "centipede": "Scolopendra heros",
    "frog": "Agalychnis callidryas",
    "snake": "Pantherophis guttatus",
    "turtle": "Chelonia mydas",
    "lizard": "Podarcis muralis",
    "toad": "Bufo bufo",
    "tortoise": "Chelonoidis niger",
    "iguana": "Iguana iguana",
    "crocodile": "Crocodylus niloticus",
    "alligator": "Alligator mississippiensis",
    "python": "Python regius",
    "dolphin": "Tursiops truncatus",
    "crab": "Callinectes sapidus",
    "whale": "Megaptera novaeangliae",
    "seal": "Phoca vitulina",
    "crayfish": "Procambarus clarkii",
    "pufferfish": "Arothron hispidus",
    "clownfish": "Amphiprion ocellaris",
    "clam": "Mercenaria mercenaria",
    "scallop": "Argopecten irradians",
    "tuna": "Thunnus albacares",
    "oysters": "Magallana gigas",
    "shrimp": "Palaemon serratus",
    "squid": "Sepioteuthis lessoniana",
    "jellyfish": "Aurelia aurita",
    "octopus": "Octopus vulgaris",
    "lobster": "Homarus americanus",
    "otter": "Enhydra lutris",
    "lion": "Panthera leo",
    "mouse": "Mus musculus",
    "fox": "Vulpes vulpes",
    "wolf": "Canis lupus",
    "deer": "Odocoileus virginianus",
    "panda": "Ailuropoda melanoleuca",
    "zebra": "Equus quagga",
    "squirrel": "Sciurus carolinensis",
    "giraffe": "Giraffa camelopardalis",
    "bear": "Ursus arctos",
    "sloth": "Bradypus variegatus",
    "hedgehog": "Erinaceus europaeus",
    "cougar": "Puma concolor",
    "grizzly-bear": "Ursus arctos horribilis",
    "vole": "Microtus pennsylvanicus",
    "chimpanzee": "Pan troglodytes",
    "badger": "Meles meles",
    "skunk": "Mephitis mephitis",
    "moose": "Alces alces",
    "camel": "Camelus dromedarius",
    "raccoon": "Procyon lotor",
    "bat": "Pteropus giganteus",
    "ape": "Pongo pygmaeus",
    "gorilla": "Gorilla gorilla",
    "mole": "Talpa europaea",
    "rat": "Rattus norvegicus",
    "beaver": "Castor canadensis",
    "rhinoceros": "Ceratotherium simum",
    "leopard": "Panthera pardus",
    "ocelot": "Leopardus pardalis",
    "tiger": "Panthera tigris",
    "weasel": "Mustela nivalis",
    "platypus": "Ornithorhynchus anatinus",
    "anteater": "Myrmecophaga tridactyla",
    "capybara": "Hydrochoerus hydrochaeris",
    "armadillo": "Dasypus novemcinctus",
    "hyena": "Crocuta crocuta",
    "pangolin": "Smutsia temminckii",
    "mammoth": "Mammuthus primigenius",
}

# iNaturalist "Life Stage" annotation: term_id=1, Larva=6.
INAT_LIFE_STAGE: dict[str, int] = {"caterpillar": 6}

# slug -> English Wikipedia article whose lead image shows one clear, typical animal.
# Slugs not listed use the capitalized slug (e.g. "giraffe" -> "Giraffe").
WIKI_TITLES: dict[str, str] = {
    "labrador-retriever": "Labrador Retriever",
    "chihuahua": "Chihuahua (dog)",
    "terrier": "Jack Russell Terrier",
    "hamster": "Golden hamster",
    "canary": "Domestic canary",
    "hen": "Chicken",
    "cow": "Cattle",
    "pig": "Domestic pig",
    "buffalo": "American bison",
    "boar": "Wild boar",
    "turkey": "Domestic turkey",
    "bird": "European robin",
    "dove": "Mourning dove",
    "penguin": "Emperor penguin",
    "parrot": "Scarlet macaw",
    "pigeon": "Rock dove",
    "eagle": "Bald eagle",
    "swan": "Mute swan",
    "seagull": "Gull",
    "swallow": "Barn swallow",
    "crow": "American crow",
    "robin": "American robin",
    "blue-jay": "Blue jay",
    "peacock": "Indian peafowl",
    "sparrow": "House sparrow",
    "purple-martin": "Purple martin",
    "bee": "Western honey bee",
    "butterfly": "Monarch butterfly",
    "ladybug": "Coccinella septempunctata",
    "moth": "Luna moth",
    "worm": "Earthworm",
    "mosquito": "Aedes albopictus",
    "cricket": "Cricket (insect)",
    "turtle": "Green sea turtle",
    "toad": "Common toad",
    "iguana": "Green iguana",
    "alligator": "American alligator",
    "python": "Ball python",
    "dolphin": "Common bottlenose dolphin",
    "whale": "Humpback whale",
    "seal": "Harbor seal",
    "pufferfish": "Tetraodontidae",
    "clownfish": "Ocellaris clownfish",
    "oysters": "Oyster",
    "lobster": "American lobster",
    "otter": "Sea otter",
    "mouse": "House mouse",
    "fox": "Red fox",
    "panda": "Giant panda",
    "bear": "Brown bear",
    "grizzly-bear": "Grizzly bear",
    "camel": "Dromedary",
    "bat": "Indian flying fox",
    "ape": "Bornean orangutan",
    "mole": "European mole",
    "rat": "Brown rat",
    "rhinoceros": "White rhinoceros",
    "weasel": "Least weasel",
    "anteater": "Giant anteater",
    "armadillo": "Nine-banded armadillo",
    "hyena": "Spotted hyena",
    "mammoth": "Woolly mammoth",
    "phoenix": "Phoenix (mythology)",
    # Generic articles lead with collages; pick one typical species instead.
    "duck": "Mallard",
    "beetle": "Lucanus cervus",
    "centipede": "Scolopendra subspinipes",
    "tuna": "Yellowfin tuna",
    "deer": "White-tailed deer",
    "squirrel": "Eastern gray squirrel",
    "pangolin": "Sunda pangolin",
}

# Wikipedia lead image would be wrong or shared (e.g. "Lamb" -> lamb meat,
# hen/rooster -> the same chicken pair, bulldog -> 1863 studio photo).
WIKI_SKIP = frozenset({"lamb", "hen", "rooster", "bulldog"})

# Pinned Commons files (tried first) when the Wikipedia lead image is atypical for kids.
COMMONS_FILES: dict[str, list[str]] = {
    "bulldog": ["Bulldog inglese.jpg", "Bulldog adult male.jpg"],
}

# Commons search terms (used when the Wikipedia lead image is missing or non-free).
COMMONS_QUERIES: dict[str, str] = {
    "lamb": "lamb sheep baby",
    "hen": "hen chicken",
    "rooster": "rooster crowing",
    "puppy": "puppy dog",
    "kitten": "kitten",
    "chihuahua": "Chihuahua dog",
    "labrador-retriever": "Labrador Retriever dog",
    "bulldog": "English bulldog dog -1863 -painting -drawing",
    "terrier": "Jack Russell Terrier",
    "poodle": "Poodle dog",
    "mammoth": "woolly mammoth reconstruction",
    "phoenix": "phoenix bestiary",
    "unicorn": "unicorn illustration",
    "dragon": "dragon illustration",
    "mermaid": "mermaid illustration",
    "fairy": "fairy illustration",
}

# Word cell may carry a trailing " · [看图](…){ … }" link added by link_animal_images.py.
ROW_RE = re.compile(r"^\|\s*(?P<diff>[^|]+)\|\s*(?P<no>[^|]+)\|\s*`(?P<word>[^`]+)`[^|]*\|")
HEADING_RE = re.compile(r"^###\s+(?P<label>.+)$")


def slugify(word: str) -> str:
    canonical = ALIASES.get(word, ALIASES.get(word.lower(), word))
    s = canonical.strip().lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-]+", "", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def parse_vocab(path: Path) -> list[dict]:
    """Return unique creature rows from categories A–I."""
    entries: list[dict] = []
    seen: set[str] = set()
    category: str | None = None
    category_ok = False
    for line in path.read_text(encoding="utf-8").splitlines():
        hm = HEADING_RE.match(line)
        if hm:
            label = hm.group("label").strip()
            category = label
            category_ok = bool(re.match(r"^[A-I]\.", label))
            continue
        rm = ROW_RE.match(line)
        if not rm or not category_ok:
            continue
        word = rm.group("word").strip()
        if word.lower() in SKIP_WORDS:
            continue
        slug = slugify(word)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        diff = rm.group("diff").strip()
        entries.append(
            {
                "word": word,
                "slug": slug,
                "difficulty": diff,
                "category": category,
                "star_only": diff.startswith("⭐ 启蒙"),
            }
        )
    return entries


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {"animals": {}}
    data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    if not data.get("animals"):
        data["animals"] = {}
    return data


def save_manifest(data: dict) -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    header = (
        "# Animal image manifest for parenting-english vocab / Guess-Guess Animals.\n"
        "# Generated by scripts/download_animal_images.py — edit via the script.\n"
    )
    body = yaml.safe_dump(
        {"animals": dict(sorted(data["animals"].items()))},
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )
    MANIFEST_PATH.write_text(header + body, encoding="utf-8")


def write_attribution(data: dict) -> None:
    lines = [
        "# Animal image attributions",
        "",
        "Photos in this folder support the parenting animal vocab and the Guess-Guess Animals game.",
        "They come from [iNaturalist](https://www.inaturalist.org/) and "
        "[Wikimedia Commons](https://commons.wikimedia.org/) under CC0, public domain, CC BY, "
        "or CC BY-SA. Images were resized and converted to WebP.",
        "",
        "| Slug | License | Author | Source |",
        "| --- | --- | --- | --- |",
    ]
    for slug, info in sorted((data.get("animals") or {}).items()):
        if not info or info.get("status") != "ok":
            continue
        author = (info.get("artist") or "—").replace("|", "/")
        license_ = (info.get("license") or "—").replace("|", "/")
        source = info.get("source_page") or ""
        link = f"[link]({source})" if source else "—"
        lines.append(f"| `{slug}` | {license_} | {author} | {link} |")
    lines.append("")
    ATTRIBUTION_PATH.write_text("\n".join(lines), encoding="utf-8")


def get_json(session: requests.Session, url: str, params: dict, timeout: int, retries: int = 5) -> dict:
    """GET JSON with backoff; honors Retry-After on HTTP 429 (Wikimedia rate limits)."""
    last: str = ""
    for attempt in range(retries + 1):
        try:
            r = session.get(url, params=params, timeout=timeout)
            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After", "")
                wait = int(retry_after) if retry_after.isdigit() else 10 * (attempt + 1)
                last = f"HTTP 429 (waited {wait}s)"
                time.sleep(min(wait, 120))
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as exc:
            last = str(exc)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"request failed: {url} ({last})")


def inat_photo_candidate(photo: dict, source_page: str) -> dict | None:
    code = (photo.get("license_code") or "").lower()
    if code not in OK_LICENSES:
        return None
    url = photo.get("medium_url") or photo.get("url") or ""
    if not url:
        return None
    url = re.sub(r"/(square|small|medium|thumb)\.", "/large.", url)
    return {
        "url": url,
        "license": code.upper().replace("PD", "Public Domain"),
        "artist": photo.get("attribution_name") or photo.get("attribution") or "",
        "attribution": photo.get("attribution") or "",
        "source_page": source_page,
        "provider": "iNaturalist",
    }


def inat_candidates(session: requests.Session, slug: str) -> list[dict]:
    name = INAT_TAXA.get(slug)
    if not name:
        return []
    data = get_json(session, f"{INAT_API}/taxa", {"q": name, "per_page": 10}, timeout=30)
    results = data.get("results") or []
    if not results:
        return []
    exact = [t for t in results if (t.get("name") or "").lower() == name.lower()]
    taxon = (exact or results)[0]
    taxon_id = taxon["id"]
    taxon_page = f"https://www.inaturalist.org/taxa/{taxon_id}"
    out: list[dict] = []

    if slug not in INAT_LIFE_STAGE and taxon.get("default_photo"):
        photo_id = taxon["default_photo"].get("id")
        page = f"https://www.inaturalist.org/photos/{photo_id}" if photo_id else taxon_page
        cand = inat_photo_candidate(taxon["default_photo"], page)
        if cand:
            cand["title"] = f"{taxon.get('preferred_common_name') or ''} ({taxon.get('name')})".strip()
            out.append(cand)

    params = {
        "taxon_id": taxon_id,
        "photos": "true",
        "photo_license": ",".join(sorted(OK_LICENSES)),
        "order_by": "votes",
        "order": "desc",
        "per_page": 8,
    }
    if slug in INAT_LIFE_STAGE:
        params["term_id"] = 1
        params["term_value_id"] = INAT_LIFE_STAGE[slug]
    obs = get_json(session, f"{INAT_API}/observations", params, timeout=30)
    for o in obs.get("results") or []:
        for photo in (o.get("photos") or [])[:1]:
            cand = inat_photo_candidate(photo, f"https://www.inaturalist.org/observations/{o['id']}")
            if cand:
                cand["title"] = f"{taxon.get('preferred_common_name') or ''} ({taxon.get('name')})".strip()
                out.append(cand)
    return out


COMMONS_IMAGEINFO = {
    "prop": "imageinfo",
    "iiprop": "url|extmetadata|mime",
    "iiurlwidth": MAX_EDGE,
}


def strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text or "")).strip()


def commons_pages_to_candidates(pages: list[dict], provider: str) -> list[dict]:
    """Convert Commons imageinfo pages into download candidates (free licenses only)."""
    out: list[dict] = []
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        mime = (info.get("mime") or "").lower()
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            continue
        meta = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in (info.get("extmetadata") or {}).items()}
        license_ = strip_html(meta.get("LicenseShortName") or "")
        blob = license_.lower()
        if "nc" in re.split(r"[\s\-]+", blob) or "noncommercial" in blob or "nd" in re.split(r"[\s\-]+", blob):
            continue
        if not any(k in blob for k in ("public domain", "cc0", "cc by", "cc-by", "pd")):
            continue
        title = page.get("title") or ""
        out.append(
            {
                "url": info.get("thumburl") or info.get("url"),
                "license": license_,
                "artist": strip_html(meta.get("Artist") or "")[:200],
                "attribution": "",
                "source_page": f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}",
                "provider": provider,
                "title": title,
            }
        )
    return out


def pinned_candidates(session: requests.Session, slug: str) -> list[dict]:
    """Explicit Commons files from COMMONS_FILES (skips missing / non-free ones)."""
    files = COMMONS_FILES.get(slug)
    if not files:
        return []
    info = get_json(
        session,
        COMMONS_API,
        {"action": "query", "format": "json", "titles": "|".join(f"File:{f}" for f in files), **COMMONS_IMAGEINFO},
        timeout=20,
    )
    pages = [p for p in ((info.get("query") or {}).get("pages") or {}).values() if "missing" not in p]
    return commons_pages_to_candidates(pages, "Wikimedia Commons (pinned file)")


def wikipedia_candidates(session: requests.Session, slug: str) -> list[dict]:
    """Lead image of the English Wikipedia article, if it is a free file on Commons."""
    if slug in WIKI_SKIP:
        return []
    article = WIKI_TITLES.get(slug) or slug.replace("-", " ").capitalize()
    data = get_json(
        session,
        WIKIPEDIA_API,
        {
            "action": "query",
            "format": "json",
            "titles": article,
            "redirects": 1,
            "prop": "pageimages",
            "piprop": "name",
        },
        timeout=20,
    )
    pages = list(((data.get("query") or {}).get("pages") or {}).values())
    file_name = next((p.get("pageimage") for p in pages if p.get("pageimage")), None)
    if not file_name:
        return []
    info = get_json(
        session,
        COMMONS_API,
        {"action": "query", "format": "json", "titles": f"File:{file_name}", **COMMONS_IMAGEINFO},
        timeout=20,
    )
    commons_pages = [
        p for p in ((info.get("query") or {}).get("pages") or {}).values() if "missing" not in p
    ]
    cands = commons_pages_to_candidates(commons_pages, "Wikimedia Commons (Wikipedia lead image)")
    for c in cands:
        c["wikipedia_article"] = article
    return cands


def commons_candidates(session: requests.Session, slug: str) -> list[dict]:
    query = COMMONS_QUERIES.get(slug) or f"{slug.replace('-', ' ')} animal"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6,
        "gsrlimit": 8,
        **COMMONS_IMAGEINFO,
    }
    data = get_json(session, COMMONS_API, params, timeout=20, retries=1)
    pages = sorted(
        ((data.get("query") or {}).get("pages") or {}).values(),
        key=lambda p: p.get("index", 0),
    )
    return commons_pages_to_candidates(pages, "Wikimedia Commons")


def download_webp(session: requests.Session, url: str, dest: Path, retries: int = 4) -> None:
    content = b""
    for attempt in range(retries + 1):
        r = session.get(url, timeout=60)
        if r.status_code == 429 and attempt < retries:
            retry_after = r.headers.get("Retry-After", "")
            time.sleep(min(int(retry_after) if retry_after.isdigit() else 10 * (attempt + 1), 120))
            continue
        r.raise_for_status()
        content = r.content
        break
    img = Image.open(io.BytesIO(content))
    if img.mode in ("P", "RGBA", "LA"):
        rgba = img.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (255, 255, 255))
        bg.paste(rgba, mask=rgba.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")
    w, h = img.size
    scale = min(1.0, MAX_EDGE / max(w, h))
    if scale < 1.0:
        img = img.resize((round(w * scale), round(h * scale)), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)


def fetch_one(session: requests.Session, entry: dict) -> dict:
    slug = entry["slug"]
    dest = ASSETS_DIR / f"{slug}.webp"
    errors: list[str] = []
    candidates: list[dict] = []
    for finder in (pinned_candidates, wikipedia_candidates, commons_candidates, inat_candidates):
        try:
            candidates.extend(finder(session, slug))
        except Exception as exc:  # noqa: BLE001 — try next provider
            errors.append(f"{finder.__name__}: {exc}")
        if candidates:
            break
    for cand in candidates:
        try:
            download_webp(session, cand["url"], dest)
        except Exception as exc:  # noqa: BLE001 — try next candidate
            errors.append(str(exc))
            continue
        return {
            "status": "ok",
            "word": entry["word"],
            "file": dest.name,
            "provider": cand["provider"],
            "title": cand.get("title", ""),
            "license": cand["license"],
            "artist": cand["artist"],
            "attribution": cand.get("attribution", ""),
            "source_page": cand["source_page"],
            "wikipedia_article": cand.get("wikipedia_article", ""),
            "category": entry["category"],
            "difficulty": entry["difficulty"],
        }
    return {
        "status": "missing",
        "word": entry["word"],
        "category": entry["category"],
        "difficulty": entry["difficulty"],
        "error": "; ".join(errors)[:300] or "no commercial-friendly image found",
    }


def select_targets(entries: list[dict], only: set[str] | None, star_only: bool, category: str) -> list[dict]:
    out = entries
    if only:
        wanted = {slugify(x) for x in only}
        out = [e for e in out if e["slug"] in wanted]
        have = {e["slug"] for e in out}
        for slug in sorted(wanted - have):
            out.append({"word": slug, "slug": slug, "difficulty": "manual", "category": "manual", "star_only": False})
    if star_only:
        out = [e for e in out if e["star_only"]]
    if category:
        out = [e for e in out if category.lower() in (e["category"] or "").lower()]
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", default="", help="Comma-separated words/slugs, e.g. donkey,raccoon")
    parser.add_argument("--star-only", action="store_true", help="Only ⭐ 启蒙 rows")
    parser.add_argument("--category", default="", help="Substring of category heading, e.g. 'A.' or 农场")
    parser.add_argument("--force", action="store_true", help="Re-download even if the WebP exists")
    parser.add_argument("--dry-run", action="store_true", help="List targets without downloading")
    parser.add_argument("--sleep", type=float, default=3.0, help="Seconds between animals (API politeness)")
    args = parser.parse_args(argv)

    entries = parse_vocab(VOCAB_MD)
    only = {x.strip() for x in args.only.split(",") if x.strip()} or None
    targets = select_targets(entries, only, args.star_only, args.category)
    if not targets:
        print("No matching animals.", file=sys.stderr)
        return 1
    print(f"Targets: {len(targets)} (vocab creatures: {len(entries)})")

    if args.dry_run:
        for e in targets:
            slug = e["slug"]
            wiki = "-" if slug in WIKI_SKIP else (WIKI_TITLES.get(slug) or slug.replace("-", " ").capitalize())
            print(f"  {slug:<20} wiki={wiki!r:<32} {e['category']}")
        return 0

    manifest = load_manifest()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    counts = {"ok": 0, "skipped": 0, "missing": 0}

    for i, entry in enumerate(targets, 1):
        slug = entry["slug"]
        dest = ASSETS_DIR / f"{slug}.webp"
        prior = manifest["animals"].get(slug) or {}
        if dest.exists() and not args.force and prior.get("status") == "ok":
            counts["skipped"] += 1
            print(f"[{i}/{len(targets)}] {slug}: skipped (exists)")
            continue
        result = fetch_one(session, entry)
        manifest["animals"][slug] = result
        counts[result["status"]] += 1
        detail = result.get("title") if result["status"] == "ok" else result.get("error")
        print(f"[{i}/{len(targets)}] {slug}: {result['status']} — {detail}", flush=True)
        save_manifest(manifest)  # checkpoint so partial runs are kept
        if i < len(targets):
            time.sleep(args.sleep)

    save_manifest(manifest)
    write_attribution(manifest)
    print(f"Done. ok={counts['ok']} skipped={counts['skipped']} missing={counts['missing']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
