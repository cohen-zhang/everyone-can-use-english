#!/usr/bin/env python3
"""Generate MP3 + WebVTT from English learning Markdown or plain text via edge-tts."""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path

DEFAULT_VOICE = "en-US-GuyNeural"

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
CODE_RE = re.compile(r"`(.+?)`")


def cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    return len(CJK_RE.findall(text)) / len(text)


def strip_md_inline(text: str) -> str:
    text = WIKILINK_RE.sub("", text)
    text = MD_LINK_RE.sub(r"\1", text)
    text = BOLD_RE.sub(r"\1", text)
    text = ITALIC_RE.sub(r"\1", text)
    text = CODE_RE.sub(r"\1", text)
    return text.strip()


def drop_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) >= 3:
        return parts[2]
    return text


def extract_english(text: str, *, stop_at_h2: bool = False) -> str:
    """Pull speakable English from learning-note Markdown."""
    text = drop_frontmatter(text)
    paragraphs: list[str] = []
    current: list[str] = []
    seen_body = False

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue

        if line in ("---", "***", "___"):
            continue

        if line.startswith("#"):
            if stop_at_h2 and seen_body and line.startswith("##"):
                break
            continue

        if line.startswith(">"):
            continue
        if line.startswith("**索引") or line.startswith("**相关"):
            continue
        if WIKILINK_RE.fullmatch(line.strip()):
            continue
        if re.match(r"^\d+\.\s+\*\*", line):
            continue
        if line.startswith("*Compiled") or line.startswith("*Note:"):
            continue

        if line.startswith("|"):
            if re.match(r"^\|[-:\s|]+\|$", line):
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if not cols or cols[0].lower() in ("english", "term"):
                continue
            line = cols[0]
        elif line.startswith(("- ", "* ")):
            line = line[2:].strip()

        if " — " in line:
            line = line.split(" — ", 1)[0].strip()

        line = strip_md_inline(line)
        if not line or cjk_ratio(line) > 0.12:
            continue

        seen_body = True
        current.append(line)

    if current:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs)


def srt_to_vtt(srt: str) -> str:
    """Convert edge-tts SRT output to WebVTT."""
    body = re.sub(
        r"(\d{2}:\d{2}:\d{2}),(\d{3})",
        r"\1.\2",
        srt.strip(),
    )
    return f"WEBVTT\n\n{body}\n"


async def synthesize(text: str, voice: str, mp3_path: Path, vtt_path: Path) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    submaker = edge_tts.SubMaker()

    with mp3_path.open("wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    vtt_path.write_text(srt_to_vtt(submaker.get_srt()), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate MP3 + WebVTT from English Markdown or plain text (edge-tts)."
    )
    parser.add_argument("input", type=Path, help="Input .md or .txt file")
    parser.add_argument(
        "-v",
        "--voice",
        default=DEFAULT_VOICE,
        help=f"TTS voice (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Output directory (default: same as input file)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Use file contents as-is (no Markdown extraction)",
    )
    parser.add_argument(
        "--stop-at-h2",
        action="store_true",
        help="Stop extraction at the first ## heading",
    )
    parser.add_argument(
        "--print-text",
        action="store_true",
        help="Print extracted text and exit without synthesizing",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        print(f"error: file not found: {input_path}", file=sys.stderr)
        return 1

    source = input_path.read_text(encoding="utf-8")
    text = source if args.raw else extract_english(source, stop_at_h2=args.stop_at_h2)
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    if not text:
        print("error: no speakable English text found", file=sys.stderr)
        return 1

    if args.print_text:
        print(text)
        return 0

    out_dir = (args.output_dir or input_path.parent).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem
    mp3_path = out_dir / f"{stem}.mp3"
    vtt_path = out_dir / f"{stem}.vtt"

    asyncio.run(synthesize(text, args.voice, mp3_path, vtt_path))

    print(f"voice:  {args.voice}")
    print(f"chars:  {len(text)}")
    print(f"mp3:    {mp3_path}")
    print(f"vtt:    {vtt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
