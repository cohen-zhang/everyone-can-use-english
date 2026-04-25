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
- 编写或生成与工作、生活、亲子等场景相关的英文材料（短文、对话、聊天用语等）；
- 长期沉淀为**自己的英文材料书**（例如 `book/MyOwnEnglishBook/`、`book/不多/` 等目录下的 Markdown）。

个人内容与上游开源内容并存；若需同步上游更新，请在本地自行合并处理。

---

## 个人学习目录重构（现状 + 目标）

当前个人学习资料主要分散在 `美剧/`、`语法/`、`book/`，存在重复目录与命名不统一问题。建议按下面结构逐步迁移。

### 当前目录树（核心部分）

```text
美剧/
  摩登家庭 S01/
    摩登家庭 S01-01.txt ... 摩登家庭 S01-24.txt

语法/
  从娃娃抓起的漫画英语语法.md
  英语语法之语法体系-（英语兔）.md
  语法王国.md

book/
  不多/
  摩登家庭/
  A Day in the Life of Jeff/
  MyOwnEnglishBook/
```

### 目标目录结构（统一英文命名）

```text
learning-notes/
  tv-series/
    modern-family/
      s01/
        transcript/        # 原始字幕/台词 txt
        notes/             # 学习笔记 md
    a-day-in-the-life-of-jeff/
      episode-notes/

  grammar-lab/
    foundations/
    kids-grammar/

  parenting-english/
    daily-life/
    school-life/
    games-and-activities/
    learning-management/

  personal-english-book/
    life/
    work/
    study/
```

### 统一命名规则（文件夹 + 文件）

- 全部使用小写英文 + 连字符：`kebab-case`
- 统一后缀：笔记用 `.md`，原始文本用 `.txt`
- 集合命名：`主题-对象-用途.md`
- 剧集命名：`modern-family-s01e01-transcript.txt`、`modern-family-s01e01-daily-lines.md`
- 亲子命名：`parenting-<scene>-<type>.md`
- 学习管理命名：`learning-plan-90d-parenting-english.md`、`spaced-repetition-tracker-parenting-english.md`

### 第一批重命名映射（建议直接执行）

- `美剧/` -> `learning-notes/tv-series/`
- `语法/` -> `learning-notes/grammar-lab/`
- `book/不多/` -> `learning-notes/parenting-english/`
- `book/MyOwnEnglishBook/` -> `learning-notes/personal-english-book/`
- `book/摩登家庭/` -> `learning-notes/tv-series/modern-family/s01/notes/`
- `美剧/摩登家庭 S01/` -> `learning-notes/tv-series/modern-family/s01/transcript/`
- `book/A Day in the Life of Jeff/` -> `learning-notes/tv-series/a-day-in-the-life-of-jeff/episode-notes/`

### 亲子目录内文件重命名示例

- `电器使用日常.md` -> `parenting-home-appliance-daily-phrases.md`
- `手机使用日常.md` -> `parenting-phone-daily-phrases.md`
- `常见符号-亲子英文.md` -> `parenting-symbols-common-vocab.md`
- `深圳小学课程-亲子英文.md` -> `parenting-primary-school-subjects-vocab.md`
- `日常礼貌与餐桌礼仪-亲子英文.md` -> `parenting-table-manners-daily-phrases.md`
- `中国常见食物-亲子英文.md` -> `parenting-china-food-common-vocab.md`
- `穿衣日常-深圳亲子英文.md` -> `parenting-shenzhen-dressing-daily-phrases.md`
- `梳妆打扮-女孩版亲子英文.md` -> `parenting-girl-grooming-daily-phrases.md`
- `学习计划-90天-亲子英文.md` -> `learning-plan-90d-parenting-english.md`
- `记忆曲线跟踪-亲子英文.md` -> `spaced-repetition-tracker-parenting-english.md`

> 建议分两步：先改“目录名”，再改“文件名”，最后统一更新 README 与内部链接，避免一次性大改难以回滚。

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
