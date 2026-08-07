#!/usr/bin/env python3
"""分析英文句子：词性 / 依存关系 / 主句谓语(ROOT) / 主句简化 / 依存结构图。

用法：
    python analyze_sentence.py <句子文件.md> [输出目录]

环境（首次）：
    /usr/local/bin/python3.12 -m venv /tmp/spacy-venv
    /tmp/spacy-venv/bin/pip install spacy cairosvg
    /tmp/spacy-venv/bin/python -m spacy download en_core_web_sm

运行：
    /tmp/spacy-venv/bin/python analyze_sentence.py principleoftheday.md
"""

import sys
from pathlib import Path

import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")


def find_root(sent):
    for token in sent:
        if token.dep_ == "ROOT":
            return token
    return None


def simplified_clause(root):
    """主句简化版：ROOT 的直接子成分 + ROOT 本身（notebook 原版做法）。"""
    children = list(root.children)
    children.insert(1, root)
    return " ".join(str(c) for c in children).strip().replace(" .", ".").capitalize()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else src.parent
    text = src.read_text(encoding="utf-8").strip()

    doc = nlp(text)

    for i, sent in enumerate(doc.sents, 1):
        print(f"\n===== Sentence {i} =====")
        print(sent.text)
        print(f"\n-- Token / POS / DEP --")
        for token in sent:
            print(f"{token.text:15} {token.pos_:8} {token.dep_:12} head={token.head.text}")

        root = find_root(sent)
        print(f"\n-- ROOT (主句谓语) --")
        print(f"{root.text}  (pos={root.pos_})")

        print(f"\n-- 主句简化版 --")
        print(simplified_clause(root))

        svg = displacy.render(sent.as_doc(), style="dep", jupyter=False,
                              options={"distance": 60})
        svg_path = out_dir / f"{src.stem}-sent{i}-dep.svg"
        svg_path.open("w", encoding="utf-8").write(svg)
        print(f"\n-- 依存图 -- {svg_path}")

        try:
            import cairosvg
            png_path = svg_path.with_suffix(".png")
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2)
            print(f"           {png_path}")
        except ImportError:
            pass


if __name__ == "__main__":
    main()
