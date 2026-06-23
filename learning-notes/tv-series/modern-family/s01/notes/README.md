# 《摩登家庭》S01 — 学习材料索引

本目录收录 **第一季（S01）** 与《摩登家庭》相关的英文学习笔记，字幕源文件在 `../transcript/`。

**各集侧栏标题（GitHub Pages）：** 主题词配置在 [[learning-notes/tv-series/modern-family/s01/episode-titles.yaml|episode-titles.yaml]]（与 transcript 场景索引一致）；MkDocs 构建时用于 `notes/*-daily-lines.md` 与 `transcript/*-transcript` 的导航显示名，**不必**批量改文件名。

## Obsidian 双向跳转（Vault 根 = 本仓库根目录时）

- **字幕目录总表（互链另一方）：** [[learning-notes/tv-series/modern-family/s01/transcript/README.md|S01 transcript README]] — `*.txt` 与本目录 `*-daily-lines.md` 在该页 **对查**；各单文件文首另有 **相向** 链到配对笔记或字幕。
- 成人向 **本集词汇表** 栏位规范见 Cursor 技能 **subtitle-vocabulary-tables**；笔记体例与互链习惯见 **english-learning-markdown-docs**。
- **关键角色讲解（成人向）：** [[learning-notes/tv-series/modern-family/s01/notes/characters/README|Modern Family S01 · Character Guides]] — Jay / Gloria / Manny、Claire / Phil / 三娃、Mitchell / Cameron；以剧中原句与口头禅为主，配短文、语域说明与复述练习（非亲子扮演）。

## 文件类型


| 类型                                                | 说明                                                              |
| ------------------------------------------------- | --------------------------------------------------------------- |
| **characters/*.md**                                  | **成人向人物导读**：身份、性格、核心台词、口头禅、名场面与复述练习；索引见 [[learning-notes/tv-series/modern-family/s01/notes/characters/README|Character Guides]]。 |
| **modern-family-s01exx-daily-lines.md**              | **剧情分段**（plot beats）+ **俚语表（仅本集）** + **难词表**；E01 已按新体例重写。俚语 vs 难词（Glossary）分类定义见 [[learning-notes/grammar-lab/english-language-taxonomy|英语语言单位分类]]。 |
| **beats/s01eNN-beats.yaml**                          | 每集剧情分段台词配置（人工精选 8–15 句/段）；生成脚本读取此文件。 |
| **modern-family-s01e02-key-to-being-a-great-dad.md** | **手工编排**的亲子对话体练习（阿泽 / Celine 设定），与自动抽取版互补。                                       |
| **scripts/build-modern-family-s01-daily-lines.py**   | **推荐**：从 beats YAML + transcript 生成 daily-lines；保留 `<!-- MANUAL:* -->` 区块。 |
| **scripts/build-modern-family-s01-md.py**            | **旧版**：按关键词生活桶（出行、居家等）从 `book/摩登家庭` 抽取；E02–E24 仍可能由此生成。 |


## 剧集列表


| 集数    | 生活实用句（notes）                                                                                                                        | 字幕（txt）                                                                              |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| E01   | [modern-family-s01e01-daily-lines.md](modern-family-s01e01-daily-lines.md)                                                       | `../transcript/modern-family-s01e01-transcript.txt`                                  |
| E02   | [modern-family-s01e02-daily-lines.md](modern-family-s01e02-daily-lines.md) + [亲子主题对话](modern-family-s01e02-key-to-being-a-great-dad.md) | `../transcript/modern-family-s01e02-transcript.txt`                                  |
| E03–E24 | `modern-family-s01e03-daily-lines.md` … `modern-family-s01e24-daily-lines.md`                                                   | `../transcript/modern-family-s01e03-transcript.txt` … `../transcript/modern-family-s01e24-transcript.txt` |


**说明：** E12 若字幕文件为空，对应 `modern-family-s01e12-daily-lines.md` 内会有占位说明；补齐字幕后请重新运行脚本。

## 重新生成 daily-lines（推荐流程）

**E01 及后续按新体例的集：**

1. 编辑或新建 `beats/s01eNN-beats.yaml`（参考 `s01e01-beats.yaml`）。
2. 在仓库根目录执行（需 `pip install pyyaml`）：

```bash
python3 learning-notes/tv-series/modern-family/s01/notes/scripts/build-modern-family-s01-daily-lines.py --episode 1
# 或全部已配置 beats：--all
```

脚本会：
- 从 YAML 输出 **剧情分段台词**；
- 扫描 transcript，在 **§A/B/C 俚语表** 中只列 **本集实际出现** 的表达；
- 保留笔记里 `<!-- MANUAL:HEAD -->` / `VOCAB` / `TIPS` 之间的手工内容。

**旧版关键词桶（legacy）：**

```bash
python3 learning-notes/tv-series/modern-family/s01/notes/scripts/build-modern-family-s01-md.py
```

## 另见

- 主题向亲子摘录：**[[learning-notes/tv-series/modern-family/s01/notes/parenting-eating-daily-phrases.md|吃 / Eat]]** · **[[learning-notes/tv-series/modern-family/s01/notes/parenting-praise-and-blessings.md|夸奖与祝福]]**（均链回本索引与 [[learning-notes/tv-series/modern-family/s01/transcript/README.md|字幕目录]]）；夸奖主题另见日常扩展 **[[learning-notes/parenting-english/daily-life/parenting-praise-kids-daily-phrases.md|夸奖、赞美小朋友 — 亲子日常英文]]**。
- 手写精编（夏威夷机场主题示例）：[[learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e22-daily-lines.md|S01E22 精编版]]（可与同集 [[learning-notes/tv-series/modern-family/s01/notes/modern-family-s01e22-daily-lines.md|自动抽取版]] 对照）。
- 关键角色成人导读：[[learning-notes/tv-series/modern-family/s01/notes/characters/README|Modern Family S01 · Character Guides]]。

