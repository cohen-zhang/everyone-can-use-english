---
search:
  boost: 2.5
---

# 学习笔记站点

本站由 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 从本仓库 `learning-notes/` 构建。

顶栏为六大分区；侧栏以各区 **README 索引** 为主。单曲、字幕 transcript、Peppa 分集剧本等叶子页仍可搜索打开，但不塞满侧栏。

上游《人人都能用英语》等请见根目录 [README 链接映射](https://github.com/cohen-zhang/everyone-can-use-english#与上游开源项目的关系链接映射)。

## 六大入口

| 分区 | 说明 | 入口 |
| --- | --- | --- |
| 美剧与影视 | 影片词表、Modern Family、Peppa、Jeff 等 | [tv-series](tv-series/README.md) |
| 英文歌曲 | 主题索引 + 播放列表总表；单曲从索引进入 | [english-song](english-song/README.md) |
| 亲子英语 | 日常场景、词汇、游戏、学习计划 | [parenting-english](parenting-english/README.md) |
| 个人材料书 | 生活 / 工作 / 学习 / 投资等 | [personal-english-book](personal-english-book/README.md) |
| 发音 | 音标、节奏、音节与输入 | [pronunciation](pronunciation/README.md) |
| 语法 | 体系总览与句子分析 | [grammar-lab](grammar-lab/README.md) |

### 快捷链

- 发音：[完整教程](pronunciation/english-phonetics-textbook.md) · [句子节奏](pronunciation/sentence-rhythm-by-type.md) · [工程师音标速查](pronunciation/engineer-phonetics-reference.md) · [音标输入](pronunciation/phonetics-input-guide.md)
- 语法：[语言单位分类](grammar-lab/english-language-taxonomy.md) · [语法体系总览](grammar-lab/english-grammar-system-overview-yingyutu.md)
- 歌曲：[音乐基础](english-song/music-english-song-basics.md) · [儿歌·亲子](english-song/celine-kids/README.md)
- 影视：[看电影学英语](tv-series/how-to-learn-english-from-movies.md) · [Peppa](tv-series/peppa-pig/README.md) · [摩登家庭](tv-series/modern-family/README.md)

## 上游阅读（外链）

李笑来《人人都能用英语》不在本站镜像：[上游 book/](https://github.com/ZuodaoTech/everyone-can-use-english/blob/master/book/README.md) · [一千小时](https://1000h.org/intro.html) · [Enjoy](https://enjoy.bot)

完整章节表见仓库根 [README](https://github.com/cohen-zhang/everyone-can-use-english#与上游开源项目的关系链接映射)。

## 说明

- 部分 Obsidian 语法在网页中可能与桌面端不一致；以仓库内 Markdown 为准。
- 新增笔记：按内容放入上表对应分区；`tv-series/**/transcript/**` 与歌曲主题下单曲默认不进侧栏（见 `mkdocs.yml` 的 `not_in_nav`）。
