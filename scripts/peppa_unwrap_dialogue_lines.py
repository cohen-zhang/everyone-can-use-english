#!/usr/bin/env python3
"""Join Peppa S01 markdown dialogue lines where one sentence was split across blank lines."""

from __future__ import annotations

import re
import sys
from pathlib import Path

VOCAB_MARK = "## Episode vocabulary"


def utterance_complete(text: str) -> bool:
    s = text.rstrip()
    if not s:
        return True
    while s and s[-1] in '\'"\'")»]':
        s = s[:-1].rstrip()
    if not s:
        return True
    if s.endswith("...") or s.endswith("…"):
        return True
    return s[-1] in ".!?"


def is_episode_title_line(line: str) -> bool:
    st = line.strip()
    return st.startswith("**") and st.endswith("**")


def unwrap_dialogue_segment(lines: list[str]) -> list[str]:
    """Merge broken sentences; segment has no ### lines."""
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        st = line.strip()
        if is_episode_title_line(line):
            out.append(line)
            i += 1
            continue
        if not st:
            out.append(line)
            i += 1
            continue
        acc = line.rstrip()
        i += 1
        while i < n:
            nxt = lines[i]
            nxt_st = nxt.strip()
            if is_episode_title_line(nxt):
                break
            if not nxt_st:
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j >= n:
                    break
                if utterance_complete(acc):
                    break
                acc = re.sub(r" +", " ", (acc + " " + lines[j].strip()).strip())
                i = j + 1
                continue
            if utterance_complete(acc):
                break
            acc = re.sub(r" +", " ", (acc + " " + nxt_st).strip())
            i += 1
        out.append(acc)
    return out


def unwrap_with_scene_headers(lines: list[str]) -> list[str]:
    chunks: list[list[str]] = []
    cur: list[str] = []
    for line in lines:
        if line.strip().startswith("###"):
            if cur:
                chunks.append(cur)
                cur = []
            chunks.append([line])
        else:
            cur.append(line)
    if cur:
        chunks.append(cur)

    out: list[str] = []
    for ch in chunks:
        if len(ch) == 1 and ch[0].strip().startswith("###"):
            out.append(ch[0])
        else:
            out.extend(unwrap_dialogue_segment(ch))

    i = 0
    while i < len(out):
        if out[i].strip().startswith("###") and i > 0:
            p = i - 1
            while p >= 0 and (
                not out[p].strip()
                or out[p].strip().startswith("###")
                or is_episode_title_line(out[p])
            ):
                p -= 1
            if p >= 0 and not utterance_complete(out[p]):
                j = i + 1
                while j < len(out) and not out[j].strip():
                    j += 1
                if j < len(out):
                    nxt = out[j]
                    nst = nxt.strip()
                    if (
                        nst
                        and not nst.startswith("###")
                        and not nst.startswith(VOCAB_MARK)
                        and not is_episode_title_line(nxt)
                    ):
                        out[p] = re.sub(r" +", " ", (out[p].rstrip() + " " + nst).strip())
                        del out[j]
                        continue
        i += 1
    return out


def process_file(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if VOCAB_MARK in raw:
        idx = raw.index(VOCAB_MARK)
        head = raw[:idx]
        tail = raw[idx:]
    else:
        head = raw
        tail = ""

    head_lines = head.splitlines(keepends=False)
    body_lines = unwrap_with_scene_headers(head_lines)
    body = "\n".join(body_lines).rstrip()
    result = body + ("\n\n" + tail.lstrip("\n") if tail else "\n")
    if not result.endswith("\n"):
        result += "\n"
    return result


def main() -> None:
    bases = [
        Path(__file__).resolve().parent.parent / "learning-notes/tv-series/peppa-pig/s01/scripts",
        Path(__file__).resolve().parent.parent / "learning-notes/tv-series/peppa-pig/s01/scripts",
    ]
    roots = [r for r in bases if r.is_dir()]
    if not roots:
        print("Missing Peppa/Peper S01 英文剧本 directories under learning-notes/tv-series/", file=sys.stderr)
        sys.exit(1)
    for root in roots:
        for path in sorted(root.glob("*.md")):
            path.write_text(process_file(path), encoding="utf-8")
            print(path)


if __name__ == "__main__":
    main()
