---
name: subtitle-vocabulary-tables
disable-model-invocation: true
description: >-
  Curates Markdown vocabulary tables from subtitles, episode scripts, or OCR output:
  column layout (Word / IPA GA / 简中义项 / 标签), adult-oriented inclusion (低频、拼写、易读错、有难度),
  excludes trivial high-frequency words and meaningless pure onomatopoeia, handles 字幕笔误 with 正字.
  Use when the user works on episode word lists, 本集词汇, Episode vocabulary sections, 字幕词汇表,
  script-derived glossaries, or asks to filter/simplify per-episode vocabulary in Markdown.
---

# Subtitle & episode vocabulary tables（字幕 / 本集单词表）

Use this skill when the task is **only** building or editing a **tabular word list** tied to subtitles, transcripts, or per-episode notes—not general prose or dialogue formatting. For full document style (bilingual notes, 阿泽, 亲子 labels, privacy), combine as needed with **english-learning-markdown-docs**.

## When to apply

- Adding or shrinking `## Episode vocabulary（本集词汇）` (or similar) under a script.
- Filtering auto-generated tables (e.g. zipf / NLTK noise) into an **adult** short list.
- Normalizing **OCR / 字幕笔误** rows with 正字 + IPA.

**Loading**: This skill uses `disable-model-invocation: true`—it does **not** inject into every chat. Enable it when relevant: **@subtitle-vocabulary-tables** in Composer/Agent, or add this skill to the session for subtitle/script vocabulary work. Use **english-learning-markdown-docs** alongside if you need full note style (阿泽, 亲子, redaction).

## Default table shape

- **Section title**: e.g. `## Episode vocabulary（本集词汇）` or `## Vocabulary（词汇表）`—match the document.
- **Columns** (recommended): `| Word | IPA (GA) | 简中义项 | 标签 |` with header row and `| --- |` separator.
- **Word column**: Surface form **as it appears in the material** when it is a **subtitle/OCR typo**; otherwise the lemma or the form used in context. Bold the English headword: `**stabilizer**`.
- **IPA (GA)**: Real phonemic transcription for the **intended/correct** lemma when the row is a typo correction; avoid placeholders like `/word*/`.
- **简中义项**: Short gloss; for typos, state **正字** and brief meaning (e.g. 字幕笔误；正字 **bicycles**（自行车复数）).
- **标签**: Comma-separated 简中 tags from the controlled set below.

## Audience: adult engineers（成人向 / 默认 software-learner 笔记）

Assume the reader already knows **very high-frequency** English (e.g. *go, make, get, look, good, big, see, come, well*). **Default rule: only keep rows that pass at least one inclusion gate.**

| Gate | Keep when… | 标签示例 |
|------|------------|----------|
| **低频** | The headword is **still a stretch point for an adult engineer in general English** (uncommon in news/books, technical, scene-specific, or easy to misread)—**not** “it only appears a few times in this episode.” | `低频` |
| **拼写** | Spelling is easy to miss (length, doubling, **-ise/-ize**, confusing pairs) **or** the source text has a **字幕/OCR 笔误** worth fixing. | `拼写` |
| **易读错** | Stress, vowel quality, or reduction pattern is commonly wrong for 简中母语者; say **how not to read it** in 简中义项 when useful. | `易读错` |
| **有难度** | Polysemy or collocation matters **in this document** and the gloss adds real value for an adult (otherwise omit “多义 junk”). | `多义`（慎用） |

### Exclude by default from adult tables

- **Fully trivial tokens** for adults: basic adjectives/adverbs/verbs from kid textbooks unless the **current line** has a non-obvious sense, phrasal use, or pronunciation trap.
- **Pure onomatopoeia / stretched spellings** with **no stable pronunciation or lexicon entry** (e.g. *wheeeee, wahhhh, arrgh*): **do not** add unless the user explicitly wants sound-effects trivia.
- **Duplicate rows**: If a typo row already teaches correct spelling and IPA, **do not** repeat the clean lemma on a separate line unless the user asks.

### Lead-in note (curated lists)

One italic line under the `##` heading, e.g.:

*成人向精简：面向已具备工作英语基础的读者；「低频」指**通用英语里相对少遇或仍有收束价值**的词，并非「在本集台词里出现得少」。收录笔误对照、拼写/读音难点、术语；剔除超高频中小学词汇、纯拟声、无价值字幕碎片。*

## Audience: child / beginner tables（亲子或低阶）

When the user targets **儿童或初学者**, widen inclusion: short concrete nouns and classroom phrases are fine; still **avoid** random onomatopoeia clutter unless teaching “sounds.” For `亲子` tagging and child-scene tone, see **english-learning-markdown-docs**.

## Controlled 标签 vocabulary

Use **简中** tags only; prefer: `低频`, `拼写`, `易读错`, `多义`, `术语`, `技术`, `亲子`. Combine with `、` (e.g. `低频、拼写`).

## Quality checks before shipping a table

1. **Every row** has a **简中义项** that justifies why the reader should care.
2. **No machine-garbage definitions** (e.g. irrelevant WordNet senses); fix or drop misleading glosses.
3. **IPA matches the lemma** you teach, not a misspelled surface form.

## Optional reference

When a **raw transcript** (e.g. `.txt`) ships alongside **per-episode Markdown** (study lines or `## Episode vocabulary（本集词汇）`), add a **hub README** that tables the pairs for Obsidian—example: [[learning-notes/tv-series/modern-family/s01/transcript/README.md]] ↔ study notes index in the same season folder. **Regenerate scripts** should preserve or re-append transcript header wikilinks if they touch file tops.

Keep this `SKILL.md` focused; long examples can live in `reference.md` in this folder if needed.
