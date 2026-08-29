# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal English learning notes repository (name retained from an earlier clone of [ZuodaoTech/everyone-can-use-english](https://github.com/ZuodaoTech/everyone-can-use-english)). Upstream open-source trees are **not** part of this repo; they may exist only as a local archive under `backup/upstream/` (gitignored). Public mapping to upstream resources lives in the root `README.md`.

Main content:

- **learning-notes/** — Personal English learning materials (Markdown), built with MkDocs Material
- **scripts/** — Python helpers for Peppa Pig vocabulary, English song notes, TTS, etc.

## Common Development Commands

```bash
# Local preview of learning-notes (MkDocs Material)
pip install -r requirements-docs.txt
mkdocs serve

# Build for GitHub Pages
mkdocs build
```

Optional script deps:

```bash
pip install -r requirements-peppa-tools.txt   # Peppa / OCR tooling
pip install -r requirements-tts.txt          # edge TTS helpers
```

## Architecture

### Learning Notes (MkDocs)

- MkDocs Material theme with Chinese language support; top **tabs** for the six zones (`tv-series`, `english-song`, `parenting-english`, `personal-english-book`, `pronunciation`, `grammar-lab`)
- **Custom Python hooks** (`mkdocs_hooks.py`) convert Obsidian-style wikilinks to regular Markdown links, generate companion pages for transcript `.txt` / scene YAML, and rename nav folders to Chinese titles
- Sidebar is slimmed via `not_in_nav` in `mkdocs.yml`: hide `tv-series/**/transcript/**`, Peppa episode scripts, and individual song pages under theme folders (keep theme `README.md` hubs). Leaves remain searchable
- Built and deployed via [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml) to GitHub Pages

### Where to put new notes

| Content | Directory |
| --- | --- |
| Movie / series vocabulary & episode notes | `learning-notes/tv-series/<title>/` |
| Song notes | `learning-notes/english-song/<theme>/` (kids songs → `celine-kids/`) |
| Parenting English | `learning-notes/parenting-english/<area>/` |
| Personal life / work / study materials | `learning-notes/personal-english-book/<area>/` |
| Pronunciation | `learning-notes/pronunciation/` |
| Grammar | `learning-notes/grammar-lab/` |

Do not put bulk transcripts or Peppa episode scripts into sidebar-critical hubs; follow existing `transcript/` / `scripts/` layouts so `not_in_nav` keeps applying.

### Python Scripts

Scripts in `scripts/`:

- `peppa_*` — Peppa Pig vocabulary / OCR / dialogue processing
- `generate_english_song_docs.py` / `enrich_english_song_docs.py` — song note generation
- `edge_tts_article.py` — TTS helpers

## Code Conventions

### File Naming

- Use `kebab-case` for all new files and directories
- English file names with Chinese content where appropriate

### Obsidian Wikilinks in Learning Notes

- Prefer full paths from vault root: `[[learning-notes/path/to/file|Display Name]]`
- Custom hooks convert these to relative links during MkDocs build
- Links to upstream *1000 hours* / *人人都能用英语* content should use HTTPS URLs (1000h.org or upstream GitHub), not local `1000-hours/` / `book/` paths

### English Learning Content

When working with learning materials, use the custom Cursor skills:

- **english-learning-markdown-docs**: For creating bilingual learning materials
- **subtitle-vocabulary-tables**: For generating vocabulary tables from subtitles

## CI/CD

- **Docs deployment**: `.github/workflows/github-pages.yml` (only workflow retained)

## Important Files

- `mkdocs.yml` — MkDocs configuration for learning-notes
- `mkdocs_hooks.py` — Obsidian wikilink conversion and transcript page generation
- `requirements-docs.txt` — MkDocs / Material / jieba deps
- `jieba_user_dict.txt` — Custom jieba dict for search
- `.cursor/skills/` — Custom Cursor skills for English learning content
- `README.md` — Personal usage notes + upstream link mapping
