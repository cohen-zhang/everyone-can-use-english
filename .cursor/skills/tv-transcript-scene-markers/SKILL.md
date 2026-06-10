---
name: tv-transcript-scene-markers
disable-model-invocation: true
description: >-
  Segments US TV bilingual transcript .txt files by shot/scene for dialogue context:
  scene index table, 【场景 xx / N】 blocks (地点·剧情·人物·时间线), anchors on first English
  line per scene. Never splits an English line from its Chinese gloss. Use when marking
  镜头场景、场景分段、transcript scene breaks, Modern Family / tv-series transcript layout,
  or fixing markers that broke 英中字幕对.
---

# TV transcript scene markers（美剧台词 · 场景分段）

Use when the user wants **shot/scene boundaries** in a **bilingual subtitle transcript** (this repo: `learning-notes/tv-series/**/transcript/*-transcript.txt`), not vocabulary tables (**subtitle-vocabulary-tables**) or extracted study lines (**english-learning-markdown-docs**).

**Reference implementation:** [[learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-transcript.txt|S01E09 transcript]] · scene config [[learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-scenes.yaml|S01E09 scenes.yaml]]

**Loading**: `disable-model-invocation: true` — enable with **@tv-transcript-scene-markers** when segmenting or fixing scene markers.

---

## Input assumptions（本仓库字幕格式）

Each **subtitle block** is exactly:

```text
- English line (may start with spaces after `-`)
 Chinese gloss line (no leading `-`)

```

Blank line between blocks is optional. File **header** (keep untouched):

1. Obsidian wikilinks to `notes/*-daily-lines.md` and `transcript/README.md`
2. Episode label line (e.g. `S01E09`)
3. Optional existing `## 场景分段索引` (replace when re-segmenting)

**Do not** change English/Chinese line text when only adding scene markers.

---

## Output layout

### 1) Scene index（文首，紧接集号后）

```markdown
## 场景分段索引（S01E09 · 本集主线一句话）

字幕正文按镜头插入 `【场景 xx / N】`；若有闪回/交叉剪辑，在首段说明。

| 场景 | 地点 | 剧情要点 |
| ---: | --- | --- |
| 01 | 医院 | … |
| 02–04 | 邓菲家 | … |
```

- **N** = total scene count in body markers.
- Group rows when 3+ consecutive scenes share one location arc.

### 2) Scene separator block（插在字幕块**之间**）

```text
----------------------
【场景 16 / 26】Jay 家 · 客厅
★ 剧情：曼尼受挫；歌洛莉亚：做真实的自己。
★ 人物：Gloria, Manny
★ 时间线：派对中段
----------------------
```

| Field | Rule |
| --- | --- |
| **地点** | Setting + optional sub-location (`邓菲后院 · 滑索事故`) |
| **剧情** | One sentence; what changes in this beat |
| **人物** | Speaking / on-screen principals; use show names |
| **时间线** | Story chronology vs flashback (`片头闪回框` / `与派对平行剪辑`) |

### 3) Placement rule（硬性）

Insert the separator **after** the previous block’s **Chinese** line and **before** the **next** block’s `- English` line.

**Wrong** (splits pair):

```text
- Let's go. We're gonna be late.
----------------------
【场景 16 / 26】…
----------------------
 快走吧  要迟到了 
```

**Right:**

```text
- Let's go. We're gonna be late.
 快走吧  要迟到了 

----------------------
【场景 16 / 26】…
----------------------
- Mind if I come in?
 介意我也进来吗 
```

---

## Workflow

### Step 1 — Read full transcript

Skim for **location shifts**, **parallel storylines** (e.g. A/B/C plots), **flashback frames**, and **act breaks**. Note non-linear editing explicitly in the index intro.

### Step 2 — Draft scene list

Aim for **15–30 scenes** per ~22-min sitcom episode (fewer if coarse, more if multiple parallel threads).

Per scene record:

- `id` — `01`, `02`, … zero-padded
- `place`, `plot`, `characters`, `timeline` — for separator block
- `anchor` — **exact** first English line of the scene (copy from `- …` line, strip leading `-` only for matching)

**Anchor rules:**

- One anchor per scene; must be unique in file order.
- Anchor = **first line of new scene**, not last line of previous scene.
- If two scenes share a location, still change anchor when **plot beat** changes (new conflict, new arrivals).

### Step 3 — Write `*-scenes.yaml` beside transcript

Use the schema in [reference.md](reference.md). Example path:

`learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-scenes.yaml`

### Step 4 — Apply markers with script

From repo root:

```bash
python .cursor/skills/tv-transcript-scene-markers/scripts/apply_scene_markers.py \
  learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-transcript.txt \
  learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-scenes.yaml
```

Script preserves header wikilinks, rebuilds index table, inserts separators, and **exits non-zero** if any English line is immediately followed by a scene marker (split pair).

### Step 5 — Manual fix pass

Script cannot infer scenes. After apply:

- Spot-check 3–5 boundaries (cold open, mid-act swap, tag).
- Re-run script after editing YAML anchors only (do not hand-edit dozens of separators).

---

## Scene planning heuristics（sitcom）

| Signal | Often a new scene |
| --- | --- |
| Location name in dialogue / stage sense | New room, car, store, hospital |
| New storyline thread | e.g. party prep vs Jay/Manny vs Cam/Fizbo |
| Time jump | `Later`, `That night`, return to opening frame |
| Ensemble split | Subgroup leaves; cut to another house |

| Keep same scene | |
| --- | --- |
| Same room, continuous argument | |
| Quick intercut (phone) | Optional: one scene with note in 时间线 |

---

## Validation checklist

- [ ] Every `- English` line has Chinese on the next line (or document rare exceptions).
- [ ] `grep` / script: **0** split pairs (English then `----------------------` or `【场景`).
- [ ] Scene IDs contiguous `01 … N`; body count matches index `N`.
- [ ] Header Obsidian links still present.
- [ ] Anchors appear in chronological **file** order (not necessarily story order if flashbacks).

---

## Related skills & links

- **subtitle-vocabulary-tables** — per-episode word tables, not scene layout.
- **english-learning-markdown-docs** — `*-daily-lines.md` study sheets; add one line in notes pointing to scene index in `.txt` if helpful.
- After new scene work on Modern Family S01, ensure [[learning-notes/tv-series/modern-family/s01/transcript/README.md|transcript README]] still lists the episode pair.

## Additional reference

- Full S01E09 scene table + YAML sample: [reference.md](reference.md)
