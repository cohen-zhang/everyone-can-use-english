<div align="center">
  <img src="./enjoy/assets/icon.png" alt="Clash" width="128" />
</div>

<h3 align="center">
AI 是当今世界上最好的外语老师，Enjoy 做 AI 最好的助教。
</h3>

[![Deploy 1000h website](https://github.com/ZuodaoTech/everyone-can-use-english/actions/workflows/deploy-1000h.yml/badge.svg)](https://github.com/ZuodaoTech/everyone-can-use-english/actions/workflows/deploy-1000h.yml)
[![Test Enjoy App](https://github.com/ZuodaoTech/everyone-can-use-english/actions/workflows/test-enjoy-app.yml/badge.svg)](https://github.com/ZuodaoTech/everyone-can-use-english/actions/workflows/test-enjoy-app.yml)
[![Release Enjoy App](https://github.com/ZuodaoTech/everyone-can-use-english/actions/workflows/release-enjoy-app.yml/badge.svg)](https://github.com/ZuodaoTech/everyone-can-use-english/actions/workflows/release-enjoy-app.yml)
![Latest Version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fenjoy.bot%2Fapi%2Fconfig%2Fapp_version&query=%24.version&label=Latest&link=https%3A%2F%2F1000h.org%2Fenjoy-app%2Finstall.html)
![Recording Duration](https://img.shields.io/endpoint?url=https%3A%2F%2Fenjoy.bot%2Fapi%2Fbadges%2Frecordings)

## 本仓库个人用途说明

本仓库为开源项目 [ZuodaoTech/everyone-can-use-english](https://github.com/ZuodaoTech/everyone-can-use-english) 的 clone，在上游代码与书籍内容之外，用于个人英文学习：

- 整理笔记与摘录；
- 从 Eudic 词典 APP 中导出单词表（序号、单词、音标、解释（包含笔记））PDF 文件，使用 MicroSoft Markitdown 命令行工具转为 markdown 格式
- 编写或生成与工作、生活、亲子等场景相关的英文材料（短文、对话、聊天用语等）；
- 长期沉淀为**自己的英文材料书**（例如 `learning-notes/personal-english-book/`、`learning-notes/parenting-english/` 等目录下的 Markdown）。

### 在线阅读（GitHub Pages）

`learning-notes/` 会通过 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 构建为静态站点，并由工作流 [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml) 发布到 **GitHub Pages**（地址形如 `https://<GitHub 用户名>.github.io/<仓库名>/`，与当前仓库的 owner、name 一致）。

1. 在仓库 **Settings → Pages → Build and deployment** 中，将 **Source** 设为 **GitHub Actions**（首次部署后可在同一页看到站点 URL）。
2. 将 **`main` 或 `master`**（或你在 [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml) 的 `on.push.branches` 里列出的分支）推送到 GitHub，或手动运行该 workflow；之后只要改动 `learning-notes/`、`mkdocs.yml`、`mkdocs_hooks.py` 或 `requirements-docs.txt` 即会重新构建。
3. 本地预览：`pip install -r requirements-docs.txt && mkdocs serve`，浏览器打开 `http://127.0.0.1:8000/`。

若你使用 **fork**，可将 `mkdocs.yml` 中的 `repo_url` / `edit_uri` 改成自己的仓库地址，便于「编辑此页」跳转正确。

个人内容与上游开源内容并存；若需同步上游更新，请在本地自行合并处理。

---

## 个人学习目录（最新）

个人学习资料已统一收敛到 `learning-notes/`，目录与文件名采用英文 `kebab-case`，并已完成内部链接修复。

### 目录树（按当前实际结构）

```text
learning-notes/
  tv-series/
    modern-family/
      s01/
        transcript/   # 原始台词与转录（txt/md）
        notes/        # 每集学习笔记（md）
    a-day-in-the-life-of-jeff/
      episode-notes/  # Jeff 系列逐集笔记与转录

  grammar-lab/        # 语法学习与语法体系

  parenting-english/  # 亲子场景英语（不多 / Celine）
    daily-life/               # 日常生活
    communication-patterns/   # 互动句型
    vocabulary/               # 主题词汇
    games-and-activities/     # 游戏与练习
    school-life/              # 校园与课程
    learning-management/      # 学习管理
    reference-guides/         # 索引与说明

  personal-english-book/
    life/             # 生活主题英语
    work/             # 工作与职场英语
    study/            # 学习与技术英语
    hedging-platform-bos-overview-design/  # 专题技术文档
```

### 分类说明（英文目录名对应中文）

| 英文目录 | 中文说明 | 典型内容 |
| --- | --- | --- |
| `tv-series` | 美剧与情景素材 | `modern-family`、`a-day-in-the-life-of-jeff` |
| `grammar-lab` | 语法实验室 | 语法体系、语法笔记、语法专项材料 |
| `parenting-english` | 亲子英语资料库 | 日常场景、词汇表、互动游戏、学习计划与索引 |
| `daily-life` | 日常生活子类 | 吃饭、穿衣、手机、地铁、情绪、礼仪等 |
| `communication-patterns` | 互动句型子类 | `Can you` 提问与回应句型 |
| `vocabulary` | 词汇子类 | 动作、动物、食物、符号、表情词汇 |
| `games-and-activities` | 游戏练习子类 | 猜词游戏、互动练习、动画笔记 |
| `school-life` | 校园子类 | 小学课程相关词汇 |
| `learning-management` | 学习管理子类 | 90天计划、复盘与跟踪 |
| `reference-guides` | 参考说明子类 | 场景索引、讲解示范文档 |
| `personal-english-book` | 个人英语材料书 | 生活、工作、学习三大分区 |
| `life` | 生活场景 | 情绪、天气、社区、日常表达 |
| `work` | 工作场景 | IM沟通、会议、出差、流程与业务表达 |
| `study` | 学习场景 | 技术英语、学习日志、术语积累 |

### 文件列表与中文说明（按目录）

以下清单基于当前 `learning-notes/` 实际文件遍历结果整理。

#### `grammar-lab/`（语法实验室）

| 文件 | 中文说明 |
| --- | --- |
| `english-grammar-system-overview-yingyutu.md` | 英语语法体系总览（英语兔） |
| `grammar-kingdom-notes.md` | 语法王国主题笔记 |
| `kids-comic-grammar-foundations.md` | 面向儿童启蒙的漫画语法基础 |

#### `parenting-english/`（亲子英语资料库）

**`daily-life/`（日常生活）**

| 文件 | 中文说明 |
| --- | --- |
| `daily-life/parenting-eating-daily-phrases.md` | 吃饭场景日常表达 |
| `daily-life/parenting-emotions-kids-edition.md` | 儿童情绪表达 |
| `daily-life/parenting-girl-grooming-daily-phrases.md` | 女孩梳妆打扮场景表达 |
| `daily-life/parenting-home-appliance-daily-phrases.md` | 家电使用场景表达 |
| `daily-life/parenting-metro-scenario-phrases.md` | 地铁出行场景表达 |
| `daily-life/parenting-one-day-of-celine.md` | Celine 的一天（第一部分） |
| `daily-life/parenting-one-day-of-celine-part-2.md` | Celine 的一天（第二部分） |
| `daily-life/parenting-phone-daily-phrases.md` | 手机使用场景表达 |
| `daily-life/parenting-praise-and-blessings.md` | 夸奖与祝福表达 |
| `daily-life/parenting-self-talk-phrases.md` | 自我鼓励/自我暗示表达 |
| `daily-life/parenting-shenzhen-dressing-daily-phrases.md` | 穿衣日常表达（深圳场景） |
| `daily-life/parenting-table-manners-daily-phrases.md` | 礼貌与餐桌礼仪表达 |
| `daily-life/parenting-tidy-up-daily-phrases.md` | 收拾整理场景表达 |

**`communication-patterns/`（互动句型）**

| 文件 | 中文说明 |
| --- | --- |
| `communication-patterns/parenting-can-you-prompts.md` | `Can you` 句型提问模板 |
| `communication-patterns/parenting-can-you-questions.md` | `Can you` 句型问答练习 |

**`vocabulary/`（主题词汇）**

| 文件 | 中文说明 |
| --- | --- |
| `vocabulary/parenting-actions-vocab.md` | 亲子动作类词汇 |
| `vocabulary/parenting-animals-vocab.md` | 动物词汇表 |
| `vocabulary/parenting-china-food-common-vocab.md` | 中国常见食物词汇 |
| `vocabulary/parenting-emoji-bilingual-vocab.md` | Emoji 表情中英对照词汇 |
| `vocabulary/parenting-symbols-common-vocab.md` | 常见符号词汇 |

**`games-and-activities/`（游戏与练习）**

| 文件 | 中文说明 |
| --- | --- |
| `games-and-activities/parenting-animal-guessing-game-log.md` | 动物猜猜猜游戏记录 |
| `games-and-activities/parenting-exercise-practice.md` | 亲子英语练习稿 |
| `games-and-activities/parenting-expression-guessing-game.md` | 表情猜猜猜互动游戏 |
| `games-and-activities/parenting-peppa-pig-notes.md` | 小猪佩奇相关学习笔记 |

**`school-life/`（校园场景）**

| 文件 | 中文说明 |
| --- | --- |
| `school-life/parenting-primary-school-subjects-vocab.md` | 小学学科词汇（深圳场景） |

**`learning-management/`（学习管理）**

| 文件 | 中文说明 |
| --- | --- |
| `learning-management/learning-plan-90d-parenting-english.md` | 90天亲子英文学习计划 |

**`reference-guides/`（索引与说明）**

| 文件 | 中文说明 |
| --- | --- |
| `reference-guides/parenting-celine-life-scenario-index.md` | Celine 生活场景索引 |
| `reference-guides/parenting-jeff-demo-guide.md` | Jeff 博士讲解示范说明 |

#### `personal-english-book/`（个人英语材料书）

**Obsidian：** 全量笔记列表、`tags`（含 `peb/*` 分区）与主题互链见 **`learning-notes/personal-english-book/README.md`**（个人英文材料书 MOC）。

| 文件 | 中文说明 |
| --- | --- |
| `README.md` | 材料书索引（MOC、wikilink、主题互链） |
| `project-overview-design.md` | 个人项目/主题的概要设计 |

**`life/`（生活）**

| 文件 | 中文说明 |
| --- | --- |
| `andy-warhol-notes.md` | 安迪沃霍尔主题笔记 |
| `community-management-english.md` | 小区生活与物业沟通英语 |
| `emotions-adult-edition.md` | 成人情绪表达 |
| `focus-notes.md` | 专注/注意力主题笔记 |
| `introduce-myself.md` | 自我介绍表达 |
| `personal-matters.md` | 个人事务表达 |
| `spoken-catchphrases-reduplicatives-adverbs.md` | 口头禅、叠词与口语副词 |
| `praise-my-wife-expressions.md` | 夸奖配偶表达 |
| `romantic-love-song-phrases.md` | 浪漫情歌与恋爱口语 |
| `classic-film-love-and-like-quotes.md` | 经典电影爱与喜欢台词 |
| `weather-daily-expressions.md` | 天气场景表达 |
| `world-cinema-quick-notes.md` | 世界电影随记 |

**`mind-body-brain-health/`（身心健康与脑科学）**

| 文件 | 中文说明 |
| --- | --- |
| `README.md` | 身心健康与脑科学索引（运动、营养、快乐激素） |
| `fitness-daily-expressions.md` | 健身场景日常表达 |
| `nutrition-weight-management-basics.md` | 饮食与体重管理基础 |
| `brain-happy-hormones.md` | 大脑快乐激素（多巴胺、血清素等） |

**`work/`（工作）**

| 文件 | 中文说明 |
| --- | --- |
| `business-trip.md` | 出差场景表达 |
| `do-not-go-gentle-into-that-good-night.md` | 名句/诗歌表达学习笔记 |
| `financial-system-issue-analysis.md` | 金融系统问题梳理 |
| `organizing-a-meeting-via-feishu.md` | 飞书组织会议表达 |
| `r-and-d-workflow.md` | 研发流程表达 |
| `work-english-client-wechat.md` | 客户侧微信沟通英语 |
| `work-english-instant-messaging.md` | 工作 IM 沟通表达 |
| `work-travel-and-business-trip.md` | 工作出行与出差表达 |
| `workplace-admin-english.md` | 行政与办公场景表达 |

**`study/`（学习）**

| 文件 | 中文说明 |
| --- | --- |
| `computer-science-vocab-interesting.md` | 有趣的计算机专业词汇 |
| `english-journal-apple-note.md` | 英文学习日志（Apple Notes） |
| `idea-editor-intro-video-script.md` | IDEA 编辑器介绍视频脚本 |
| `java-developer-work-diary.md` | Java 开发者工作日记 |
| `spring-framework-notes.md` | Spring Framework 学习笔记 |

**`investing/`（投资英语场景）**

| 文件 | 中文说明 |
| --- | --- |
| `README.md` | 投资英语场景索引（个人投资者视角） |
| `stock-trading-investor-essentials.md` | 股票交易 — 投资者必备词汇与例句 |
| `crypto-exchange-app-scenarios.md` | 加密货币 — 交易所 APP 常用场景 |
| `stock-and-commodity-broker-notes.md` | 证券与商品经纪访谈实录 |

**`hedging-platform-bos-overview-design/`（专题技术文档）**

| 文件/目录 | 中文说明 |
| --- | --- |
| `hedging-platform-bos-overview-design.md` | 对冲交易平台 BOS 概要设计主文档 |
| `hedging-platform-bos-overview-design.md.backup` | 主文档备份 |
| `images/` | 文档配图目录（系统架构图、流程图、示意图） |

#### `tv-series/`（美剧与情景素材）

**`a-day-in-the-life-of-jeff/episode-notes/`**

| 文件模式/文件 | 中文说明 |
| --- | --- |
| `jeff-e01-getting-up-notes.md` | Jeff 第1集起床场景学习笔记 |
| `jeff-e01-getting-up-transcript.txt` ... `jeff-e10-ready-for-bed-transcript.txt` | Jeff 第1-10集逐集转录文本 |

**`modern-family/s01/transcript/`**

| 文件模式/文件 | 中文说明 |
| --- | --- |
| `modern-family-s01e01-transcript.txt` ... `modern-family-s01e24-transcript.txt` | 摩登家庭 S01 第1-24集转录文本 |
| `modern-family-s01e22-daily-lines.md` | S01E22 的人工整理实用句 |

**`modern-family/s01/notes/`**

| 文件模式/文件 | 中文说明 |
| --- | --- |
| `modern-family-s01e01-daily-lines.md` ... `modern-family-s01e24-daily-lines.md` | 摩登家庭 S01 各集生活实用句笔记 |
| `modern-family-s01e02-key-to-being-a-great-dad.md` | S01E02 亲子主题精编对话笔记 |
| `readme.md` | 本目录索引与使用说明 |
| `scripts/build-modern-family-s01-md.py` | 批量生成 S01 笔记的脚本 |

### 命名与维护规则（简版）

- 文件夹与文件统一使用 `kebab-case`
- `kebab-case` 含义：全部小写单词，用中划线 `-` 连接，不使用空格、下划线或中文标点
- 示例：`parenting-phone-daily-phrases.md`、`modern-family-s01e01-transcript.txt`
- 反例：`Parenting_Phone.md`、`parenting phone.md`、`亲子-手机.md`
- 学习文档优先使用 `.md`，原始文本使用 `.txt`
- 新增文件时保持“主题-场景-用途”风格，便于检索与长期维护
- 如新增子目录，请在本节同步补充中文说明

---

## 网页版

Enjoy 全新版本已经上线，可访问 [https://enjoy.bot](https://enjoy.bot) 直接使用。

![](./enjoy/snapshots/screenshot-video.png)
![](./enjoy/snapshots/screenshot-ebook.png)
![](./enjoy/snapshots/screenshot-flashcard.png)
![](./enjoy/snapshots/screenshot-course.png)

## 浏览器插件

Enjoy 浏览器插件已经上线，支持 YouTube 和 Netflix。可访问 [Chrome Web Store](https://chromewebstore.google.com/detail/enjoy-echo/hiijpdndbjfnffibdhajdanjekbnalob) 安装使用。

![](./enjoy/snapshots/screenshot-youtube.png)
![](./enjoy/snapshots/screenshot-netflix.png)

---

## 桌面版

新版桌面版将会是对网页版的套壳和增强，即将发布。


## 相关阅读

### 一千小时（2024）

- [简要说明](https://1000h.org/intro.html)
- [训练任务](https://1000h.org/training-tasks/kick-off.html)
- [语音塑造](https://1000h.org/sounds-of-american-english/0-intro.html)
- [大脑内部](https://1000h.org/in-the-brain/01-inifinite.html)
- [自我训练](https://1000h.org/self-training/00-intro.html)

### 人人都能用英语（2010）

- [简介](./book/README.md)
- [第一章：起点](./book/chapter1.md)
- [第二章：口语](./book/chapter2.md)
- [第三章：语音](./book/chapter3.md)
- [第四章：朗读](./book/chapter4.md)
- [第五章：词典](./book/chapter5.md)
- [第六章：语法](./book/chapter6.md)
- [第七章：精读](./book/chapter7.md)
- [第八章：叮嘱](./book/chapter8.md)
- [后记](./book/end.md)

## 常见问题

请查询 [文档 FAQ](https://1000h.org/enjoy-app/faq.html)。
