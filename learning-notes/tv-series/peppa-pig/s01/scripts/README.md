---
title: Peppa Pig 第一季（S01）英文剧本学习库
aliases:
  - 小猪佩奇 S01 剧本
  - Peppa Pig S01 transcripts
description: 每集一幕式英文台词 + 成人向本集词汇表；供跟读、OCR 对照与批量脚本维护。仓库内以本目录（Peppa Pig）为规范路径。
tags:
  - tv-series/peppa-pig
  - english-learning
  - transcript
  - vocabulary
series: Peppa Pig
season: 1
episode_count: 52
cssclasses:
  - moc
---

# Peppa Pig S01 · 英文剧本（文件夹说明）

> **给 AI / 检索用速览**：本目录共 **52** 份剧集 Markdown，命名 `Peppa.Pig.S01E{NN}.{Title}.md`；正文为**整集英文台词**（按场景分段），文末（多数集）有 `## Episode vocabulary（本集词汇）` **成人向精简词表**。维护词表与合并正字可执行仓库内 `scripts/peppa_adult_vocab_curate.py`（见下文「自动化」）。

规范路径为本目录 `tv-series/peppa-pig/s01/scripts/`（kebab-case）。

### 给自动化 / RAG 的硬信息（可原样抽取）

- **系列**：Peppa Pig Season 1（52 episodes）
- **单集文件 glob**：`Peppa.Pig.S01E*.md`（本目录内）
- **词汇区锚点**：Markdown 二级标题 `## Episode vocabulary（本集词汇）`
- **词表列名**：`Word | IPA (GA) | 简中义项 | 标签`
- **批量维护入口**：仓库根执行 `python3 scripts/peppa_adult_vocab_curate.py --lemma-zh`（默认目录=本文件夹）

---

## Obsidian 使用建议

| 用途 | 建议 |
| --- | --- |
| **图谱 / 反向链接** | 将本仓库或 `learning-notes/` 作为库根时，可用 `[[Peppa.Pig.S01E01.Muddy.Puddles]]` 等形式链到单集（文件名在库内唯一时最省事）。若有多套副本，请用**完整相对路径**链到本文件夹下的文件。 |
| **亲子手记（与本页双向跳转）** | **[[learning-notes/parenting-english/games-and-activities/parenting-peppa-pig-notes|Peppa Pig 与几则笔记（不多的 Peppa Pig 手记）]]**：该手记内已链回本说明页 **`[[learning-notes/tv-series/peppa-pig/s01/scripts/README|Peppa Pig S01 README]]`**，图谱与 outgoing / incoming backlinks 会互显；从手记仍可短链跳入各集 **`[[Peppa.Pig.S01ENN…]]`**。 |
| **问句清单（按沟通意图分类）** | **[[learning-notes/tv-series/peppa-pig/s01/scripts/peppa-pig-s01-question-bank-by-category|Peppa Pig S01 问句清单（按沟通意图分类）]]**：从全 52 集台词精选高频可复用问句，按请求/许可、意愿/邀请、状态/确认、Wh- 探询等归类，每条标注来源集；与 **[[learning-notes/parenting-english/communication-patterns/parenting-question-bank-by-category|亲子问句分类清单]]** 同文风、可对照复用。 |
| **情绪词汇/句子（按分类）** | **[[learning-notes/tv-series/peppa-pig/s01/scripts/peppa-pig-s01-emotions-by-category|Peppa Pig S01 情绪词汇与句子（按分类）]]**：从全 52 集台词提取 happy / scared / not well / Don't worry 等情绪词与可跟读句，与 **[[learning-notes/parenting-english/daily-life/parenting-emotions-kids-edition|情绪 · 亲子]]**、**[[learning-notes/personal-english-book/life/emotions-adult-edition|情绪 · 成人版]]** 相向互链。 |
| **家庭人物讲解（亲子对话）** | **[[learning-notes/tv-series/peppa-pig/s01/scripts/characters/README|Peppa Pig S01 · Family Character Guides]]**：分别介绍 Peppa、George、Mummy Pig、Daddy Pig、Granny Pig、Grandpa Pig、Chloe 与亲戚称呼，按身份、关系、兴趣、食物、好笑场景和亲子 Q&A 组织；与 **[[learning-notes/parenting-english/games-and-activities/parenting-peppa-pig-notes|Peppa Pig 手记]]** 相向互链。 |
| **暑假 60 天打印学习计划** | **[[learning-notes/parenting-english/learning-management/learning-plan-60d-summer-peppa|暑假 60 天学习计划]]** + [[learning-notes/parenting-english/learning-management/summer-60d-print/peppa-s01-e01-e45-print-lines|精选台词（E01–E45 打印版）]] + [[learning-notes/parenting-english/learning-management/summer-60d-mom-operation-card|妈妈操作卡]]；与 **[[learning-notes/parenting-english/learning-management/learning-plan-90d-parenting-english|90 天亲子计划]]** 相向互链。 |
| **亲子词汇扩展（职业／扮装）** | **[[learning-notes/parenting-english/vocabulary/parenting-jobs-roles-vocab|职业与角色 — Jobs, Roles & Pretend Play]]** 以 **[[Peppa.Pig.S01E19.Dressing.Up|S01E19 Dressing Up]]** 为示例集；单集文末 **Related** 节与此页 **相向互链**。 |
| **标签** | 本 README 已设 frontmatter `tags`；若你希望按集打标签，可在单集笔记顶部增加 YAML（示例见下节）。 |
| **搜索** | 全文搜 `Episode vocabulary` 可列出所有含词表的集；搜 `本集无符合成人向收束标准` 可找到词表被脚本清空后的集。 |
| **大纲 / 大纲面板** | 单集文件结构通常为：`### Scene · …` 多级标题；在大纲中可快速跳转场景。 |
| **Dataview（可选插件）** | 若你为每集补上 `episode: 4` 等字段，可用 `TABLE episode, file.link FROM "…本目录…"` 生成剧集目录。未加 frontmatter 时，用 `SORT file.name ASC` 即可按文件名排序。 |

### 可选：单集 YAML 模板（复制到某一集顶部）

```yaml
---
episode: 4
title: Best Friend
tags: [tv-series/peppa-pig, peppa/s01]
---
```

（与现有以粗体标题 `**S1-04 …**` 开头的文风可同时保留，Obsidian 不冲突。）

---

## 单集文件里有什么

1. **剧标头**（可选）：一行粗体，如 `**S1-04 best friend**`。
2. **场景段落**：`### Cold open · Intro（…）` / `### Scene · …` 等，下面是**单行或短行**英文台词（已从 OCR 拆行合并过，便于阅读）。
3. **词汇区**（`## Episode vocabulary（本集词汇）`）  
   - 一段 *成人向精简* 说明；**与** `.cursor/skills/subtitle-vocabulary-tables/SKILL.md` **及** `scripts/peppa_adult_vocab_curate.py` **中的** `ADULT_NOTE` **保持同一套标准**（默认**简中成人**读者视角，不以英美语料高频为唯一删词依据）。  
   - Markdown 表格：`| Word | IPA (GA) | 简中义项 | 标签 |`  
   - **Word 列**：字幕笔误已尽量规范为**正确词形**；极度高频词、纯拟声、无意义碎片会被脚本剔除，故**有些集无表格行**，仅保留说明句。

附加文件：`007 小猪佩奇第一季 双语.pdf` 为参考用双语材料，**不与 Markdown 逐行一一绑定**。

---

## 命名规则（给脚本与 AI）

| 模式 | 含义 |
| --- | --- |
| `Peppa.Pig.S01E01.Muddy.Puddles.md` | 第 1 集，标题slug 为 `Muddy.Puddles` |
| `S01E{NN}` | 季内集号，两位数字 |
| `.` 分隔 | slug 中的空格 / 语义分段 |

---

## 自动化与技能（仓库根目录相对路径）

| 路径 | 作用 |
| --- | --- |
| `scripts/peppa_adult_vocab_curate.py` | 成人向词表：`ADULT_NOTE` 与上列技能对齐；`--lemma-zh` 合并正字、简中义项、去重；内置剔除「超高频 / 拟声 / 字幕碎片」等规则。 |
| `scripts/peppa_lemma_zh_data.py` | 词头 → 简中义项数据（供上者引用）。 |
| `scripts/peppa_s01_ocr_il.tsv` | 字幕纠错 / 映射表（若存在未覆盖的 OCR，可在此增补）。 |
| `.cursor/skills/subtitle-vocabulary-tables/SKILL.md` | 本系列词汇表格列、标签与成人向收录原则说明。 |

典型命令（在仓库根）：

```bash
python3 scripts/peppa_adult_vocab_curate.py --lemma-zh
```

默认处理目录即**本文件夹**（脚本内 `DEFAULT_DIR`）。

---

## 剧集索引（MOC · 链接到本目录内文件）

以下为 Obsidian 兼容的 `[[wikilink]]`（库根包含本目录且笔记名唯一时生效）；否则请改用相对路径 `[[./Peppa.Pig.S01E01.Muddy.Puddles|Peppa.Pig.S01E01.Muddy.Puddles]]` 等。

### S01E01–E13

- [[Peppa.Pig.S01E01.Muddy.Puddles]]
- [[Peppa.Pig.S01E02.Mr.Dinosaur.is.Lost]]
- [[Peppa.Pig.S01E03.Polly.Parrot]]
- [[Peppa.Pig.S01E04.Best.Friend]]
- [[Peppa.Pig.S01E05.Hide.and.Seek]]
- [[Peppa.Pig.S01E06.The.Playgroup]]
- [[Peppa.Pig.S01E07.Mummy.Pig.at.Work]]
- [[Peppa.Pig.S01E08.Camping]]
- [[Peppa.Pig.S01E09.Gardening]]
- [[Peppa.Pig.S01E10.Bicycles]]
- [[Peppa.Pig.S01E11.The.New.Car]]
- [[Peppa.Pig.S01E12.Snow]]
- [[Peppa.Pig.S01E13.Flying.a.Kite]]

### S01E14–E26

- [[Peppa.Pig.S01E14.My.Cousin.Chloe]]
- [[Peppa.Pig.S01E15.Daddy.Loses.his.Glasses]]
- [[Peppa.Pig.S01E16.Hiccups]]
- [[Peppa.Pig.S01E17.Picnic]]
- [[Peppa.Pig.S01E18.Mummy.Pigs.Birthday]]
- [[Peppa.Pig.S01E19.Dressing.Up]]
- [[Peppa.Pig.S01E20.The.School.Fete]]
- [[Peppa.Pig.S01E21.Musical.Instruments]]
- [[Peppa.Pig.S01E22.Babysitting]]
- [[Peppa.Pig.S01E23.New.Shoes]]
- [[Peppa.Pig.S01E24.Ballet.Lesson]]
- [[Peppa.Pig.S01E25.The.Tooth.Fairy]]
- [[Peppa.Pig.S01E26.Treasure.Hunt]]

### S01E27–E39

- [[Peppa.Pig.S01E27.Not.Very.Well]]
- [[Peppa.Pig.S01E28.Windy.Castle]]
- [[Peppa.Pig.S01E29.Pancakes]]
- [[Peppa.Pig.S01E30.The.Museum]]
- [[Peppa.Pig.S01E31.Secrets]]
- [[Peppa.Pig.S01E32.Thunderstorm]]
- [[Peppa.Pig.S01E33.Piggy.in.the.Middle]]
- [[Peppa.Pig.S01E34.Fancy.Dress.Party]]
- [[Peppa.Pig.S01E35.Very.Hot.Day]]
- [[Peppa.Pig.S01E36.Mister.Skinnylegs]]
- [[Peppa.Pig.S01E37.Lunch]]
- [[Peppa.Pig.S01E38.Sleepy.Princess]]
- [[Peppa.Pig.S01E39.The.Tree.House]]

### S01E40–E52

- [[Peppa.Pig.S01E40.Daddy.Gets.Fit]]
- [[Peppa.Pig.S01E41.Shopping]]
- [[Peppa.Pig.S01E42.Chloes.puppet.show]]
- [[Peppa.Pig.S01E43.My.Birthday.Party]]
- [[Peppa.Pig.S01E44.The.Playground]]
- [[Peppa.Pig.S01E45.Tidying.Up]]
- [[Peppa.Pig.S01E46.Frogs.and.Worms.and.Butterflies]]
- [[Peppa.Pig.S01E47.Daddy.Puts.up.a.Picture]]
- [[Peppa.Pig.S01E48.At.the.Beach]]
- [[Peppa.Pig.S01E49.Cleaning.the.Car]]
- [[Peppa.Pig.S01E50.Grandpa.Pigs.Boat]]
- [[Peppa.Pig.S01E51.Daddys.Movie.Camera]]
- [[Peppa.Pig.S01E52.The.School.Play]]

---

## 可选：Dataview 列表（需安装 Dataview）

将 `PATH` 换成你在 Obsidian 里打开库时，**本目录所对应的路径**（含空格需保留）。

```dataview
LIST file.link
WHERE contains(file.path, "peppa-pig/s01/scripts") AND startswith(file.name, "Peppa.Pig.S01")
SORT file.name ASC
```

（把 `file.path` 中的目录段改成你库里实际路径即可；若 README 与本集在同一文件夹，也可将这条查询放进 Bases / 固定面板。）

---

## 另见

- 亲子/成人笔记文体与阿泽设定：仓库内 `.cursor/skills/english-learning-markdown-docs/SKILL.md`
- 《摩登家庭》S01 笔记索引（结构可参考）：`../modern-family/s01/notes/README.md`
