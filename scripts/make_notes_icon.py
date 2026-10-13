#!/usr/bin/env python3
"""Draw the 1024x1024 「英语学习笔记」 desktop icon in the site's indigo palette.

  uv run --no-project --with pillow python scripts/make_notes_icon.py
  # -> scripts/assets/notes-icon.png
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1024
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "assets" / "notes-icon.png"
FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")

INDIGO_TOP = (92, 107, 192)
INDIGO_BOTTOM = (48, 63, 159)
TEAL = (76, 174, 145)
PAPER = (250, 250, 255)
PAPER_SHADE = (226, 230, 248)
INK = (40, 53, 147)


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def diagonal_gradient() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            t = (x + y) / (2 * SIZE)
            base = lerp(INDIGO_TOP, INDIGO_BOTTOM, t)
            px[x, y] = lerp(base, TEAL, max(0.0, t - 0.55) / 0.45 * 0.5)
    return img


def main() -> None:
    margin, radius = 100, 185
    box = [margin, margin, SIZE - margin, SIZE - margin]

    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [margin, margin + 16, SIZE - margin, SIZE - margin + 16], radius=radius, fill=(0, 0, 0, 100)
    )
    icon.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(20)))

    body = diagonal_gradient().convert("RGBA")
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    body.putalpha(mask)
    icon.alpha_composite(body)

    # Open book.
    book = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(book)
    cx, top, bottom, drop, half = SIZE // 2, 470, 790, 34, 300
    left = [(cx - half, top), (cx - 8, top + drop), (cx - 8, bottom + drop), (cx - half, bottom)]
    right = [(cx + 8, top + drop), (cx + half, top), (cx + half, bottom), (cx + 8, bottom + drop)]
    bd.polygon(left, fill=PAPER + (255,))
    bd.polygon(right, fill=PAPER_SHADE + (255,))
    bd.line([(cx, top + drop), (cx, bottom + drop)], fill=INK + (255,), width=8)
    for i in range(4):
        y = top + 70 + i * 58
        bd.line([(cx - half + 50, y), (cx - 60, y + 10)], fill=INK + (90,), width=12)
        bd.line([(cx + 60, y + 10), (cx + half - 50, y)], fill=INK + (90,), width=12)

    glow = book.filter(ImageFilter.GaussianBlur(24))
    tint = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    tint.putalpha(glow.getchannel("A").point(lambda a: int(a * 0.35)))
    icon.alpha_composite(tint)
    icon.alpha_composite(book)

    # "Aa" above the book.
    d = ImageDraw.Draw(icon)
    font = ImageFont.truetype(str(FONT), 300) if FONT.is_file() else ImageFont.load_default()
    d.text((cx, 330), "Aa", font=font, fill=(255, 255, 255, 255), anchor="mm")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    icon.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
