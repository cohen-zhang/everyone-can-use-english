# 《摩登家庭》S02 — 学习材料索引

本目录收录 **第二季（S02）** 与《摩登家庭》相关的英文学习笔记，字幕源文件在 `../transcript/`。

**各集侧栏标题（GitHub Pages）：** 本目录显示为 **「第二季 · 场景句」**（与同季 **「第二季 · 英中字幕」** 对照）；叶子标题前缀 `【场景句】S02Exx · {主题}`。主题词配置在 [[learning-notes/tv-series/modern-family/s02/episode-titles.yaml|episode-titles.yaml]]；**不必**批量改文件名。

## Obsidian 双向跳转（Vault 根 = 本仓库根目录时）

- **字幕目录总表（互链另一方）：** [[learning-notes/tv-series/modern-family/s02/transcript/README.md|S02 transcript README]] — `*.txt` 与本目录 `*-daily-lines.md` 在该页 **对查**；各单文件文首另有 **相向** 链到配对笔记或字幕。
- 成人向 **本集词汇表** 栏位规范见 Cursor 技能 **subtitle-vocabulary-tables**；笔记体例与互链习惯见 **english-learning-markdown-docs**。
- **第一季：** [[learning-notes/tv-series/modern-family/s01/notes/README|S01 notes 索引]] · 角色导读仍放在 [[learning-notes/tv-series/modern-family/s01/notes/characters/README|S01 Character Guides]]（人物跨季，不在 S02 重复建档）。

## 文件类型

| 类型 | 说明 |
| --- | --- |
| **modern-family-s02exx-daily-lines.md** | **剧情简介** + 按生活桶抽取的可朗读英中句（与 S01 E02–E24 旧体例一致）。 |
| **scripts/build-modern-family-s02.py** | 从合并 `S2.txt` 拆出 transcript，再生成 daily-lines。 |

## 剧集列表

| 集数 | 生活实用句（notes） | 字幕（txt） |
| --- | --- | --- |
| E01–E24 | `modern-family-s02e01-daily-lines.md` … `modern-family-s02e24-daily-lines.md` | `../transcript/modern-family-s02e01-transcript.txt` … `../transcript/modern-family-s02e24-transcript.txt` |

## 重新生成 daily-lines

在仓库根目录执行（需 `pip install pyyaml`）：

```bash
python3 learning-notes/tv-series/modern-family/s02/notes/scripts/build-modern-family-s02.py \
  --source .tmp-mf-src/S2.txt --all
# 仅重跑笔记（字幕已在 transcript/）：
python3 learning-notes/tv-series/modern-family/s02/notes/scripts/build-modern-family-s02.py --notes
```

脚本会：
- `--ingest`：按 `S02Exx` 拆集，写入 `../transcript/modern-family-s02eNN-transcript.txt`（保留文首 Obsidian 互链）；
- `--notes`：按关键词生活桶抽取句子，写入本目录 `*-daily-lines.md`；剧情简介来自 `../episode-titles.yaml`。

## 另见

- 剧集总入口：[[learning-notes/tv-series/modern-family/README|摩登家庭]]
- 第一季笔记：[[learning-notes/tv-series/modern-family/s01/notes/README|S01 notes]]
