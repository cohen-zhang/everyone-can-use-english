---
name: english-learning-markdown-docs
description: Produces English-learning materials as Markdown with fixed English plus Simplified Chinese glosses, emphasized finance/tech and child-scene vocabulary, and readable layout. Uses learner name **阿泽** (nickname **泽哥**) and child labels 不多 / Celine when appropriate. Redacts unrelated private identifiers for shareable output. After new or finished notes under learning-notes/, search related docs and add bidirectional Obsidian wikilinks (see skill body). Use when writing notes, journals, vocabulary sheets, dialogues, parenting-and-work English material. For subtitle/episode **word tables** (本集词汇, Episode vocabulary), use **subtitle-vocabulary-tables** instead or in addition.
---

# English-learning Markdown documents

## When to apply

Use this skill whenever the user asks for **documents, notes, or exports** related to English learning (personal study, parenting, or teaching helpers), not only when they say “Markdown.” Default to **Markdown** unless they explicitly request another format.

## Output format

- **Default**: GitHub-flavored Markdown (`.md`). One topic per logical section; use `##` / `###` hierarchy consistently; avoid skipping heading levels.
- **Readability**: Short paragraphs; blank line between blocks; use bullet or numbered lists for steps and vocabulary; use tables only when they improve scanning (e.g. word / IPA / meaning / example).
- **Vocabulary tables**: When building **subtitle or episode word lists** (`Episode vocabulary`, 本集词汇), follow project skill **subtitle-vocabulary-tables** (`/.cursor/skills/subtitle-vocabulary-tables/SKILL.md`).
- **Bilingual layout**: Follow **「英 + 简中」对照** throughout (see section **Bilingual layout (English + 简中)** below). English stays primary for lines meant to be spoken aloud.
- **Code and tools**: Fenced code blocks with language tags when showing snippets; inline backticks for commands, keys, and file names.

## Audience

Assume readers are:

1. **Software engineers** learning English: familiar with technical terms in English; may need plain explanations of informal or business English; appreciate concise, accurate wording.
2. **Parents** helping children learn English: prefer clear, repeatable language patterns, gentle difficulty, and age-appropriate examples when the user specifies the child’s level.

Avoid unexplained jargon about language teaching unless the user asks for it. Prefer practical, usable sentences over textbook-only formalism unless context requires formality.

## Bilingual layout (English + 简中)

- **Default**: Every meaningful English unit (phrase, sentence, or table row) appears **with** a concise **Simplified Chinese** gloss—same line (e.g. `English` — 简中) or the line directly below; in tables, use dedicated English / 中文 columns when it improves scanning.
- **Learner identity**: **阿泽**；同事可能称呼 **泽哥**。在自我介绍、职场对话、情景练习中可自然使用；若用户要求对外分享或全文匿名，再改为占位称呼。
- **Highlight (priority review)**: Terms tied to **financial-industry systems and business**, and **software development** (engineering, architecture, delivery, toolchain, roles), mark clearly: **bold** for the English term, a `术语` / `技术` tag in lists, or an extra column with 简中 + short memory hook.

## Child-focused vocabulary (不多 / Celine)

- **Child labels**: 昵称 **不多**；英文名 **Celine**。亲子日常、带娃场景、儿童用词表、简单对话示例中可使用这些名字，保持全文一致。
- **Highlight (priority review)**: Vocabulary for **child age bands**, parenting, parent–child interaction, school/life routines, and kid-friendly phrasing—same marking style as technical terms (**bold**, tag like `亲子`, or dedicated column) so it is easy to separate from finance/tech rows when both appear in one file.

## Privacy and redaction

Before treating text as **final** or **shareable**, **strip or replace** sensitive details:

| Kind | Action |
|------|--------|
| Employers, products, clients, internal codenames | Replace with generic labels (`Company A`, `Project X`) or role-only descriptions |
| Real names (self, family, colleagues, children) | For **shareable** or **anonymous** docs, use placeholders consistent in-file. For **this user’s private learning notes**, use the names and labels in the sections above unless they ask to anonymize |
| Addresses, phone numbers, emails, IDs, URLs with tokens | Remove or anonymize; keep structure only if pedagogically needed (e.g. `user@example.com`) |
| Locations that identify individuals | Generalize (`a city in …`, `our neighborhood`) |

If the user pastes raw material, **redact in the delivered document** and do not echo secrets in summaries unless the user explicitly needs a redaction review list.

## Quality bar

- **Unified style**: Same heading style, list style, and terminology across the file.
- **Scannable**: Headings and first lines of sections should orient the reader quickly.
- **Honest level**: If a phrase is idiomatic or region-specific, note it briefly when it matters for learners.

## Obsidian cross-links after new docs（新文档后的互链检查）

When adding or substantially finishing a **new** learning note under `learning-notes/` (especially `parenting-english/`): **search the vault for related notes** and add **bidirectional** wikilinks so Obsidian graph and backlinks stay useful.

1. **What to link**: Same **scene** (e.g. tidy / emotions / grooming), overlapping **vocabulary or patterns** (e.g. action verbs + opposites game), **game ↔ drill** pairs, or an existing **index / README** that lists that topic.
2. **Conventions** (match this repo):
   - Prefer **full path from vault root**, with a display name:  
     `[[learning-notes/parenting-english/.../file-name|短标题或节名]]`  
     (Same pattern as in `parenting-peppa-pig-notes.md` and `Peppa Pig S01.英文剧本/README.md`.)
   - **相向互链**: the new file links to the related note **and** that note gains a **相关** / **（扩展）** line (or list item) linking back—briefly state which **section or table** the reader should open.
3. **Avoid**: Linking only one direction; stuffing unrelated links for “coverage.” Skip or defer if the overlap is vague (e.g. a methodological note vs. a phrase list) unless the user asks to wire the graph anyway.
4. **Vault root**: Remind the user (if relevant) that wikilinks resolve cleanly when the Obsidian vault root includes `learning-notes/` (or the same tree used in those full paths).

## Optional reference

For extended typography notes or team-specific templates, add `reference.md` next to this file and link it here; keep `SKILL.md` under 500 lines.
