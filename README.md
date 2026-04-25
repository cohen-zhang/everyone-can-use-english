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
- 长期沉淀为**自己的英文材料书**（例如 `learning-notes/personal-english-book/`、`learning-notes/parenting-english/` 等目录下的 Markdown）。

个人内容与上游开源内容并存；若需同步上游更新，请在本地自行合并处理。

---

## 个人学习目录重构（目录名已完成）

本次已完成“目录名重构”（未改文件名）。个人学习资料已集中到 `learning-notes/` 下。

### 当前目录树（目录改名后）

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
    从娃娃抓起的漫画英语语法.md
    英语语法之语法体系-（英语兔）.md
    语法王国.md

  parenting-english/
    ...（原 book/不多 内容，待下一步按场景拆分子目录）

  personal-english-book/
    ...（原 book/MyOwnEnglishBook 内容）
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

### 目录变更说明表

| 变更类型 | 旧路径 | 新路径 | 状态 | 说明 |
| --- | --- | --- | --- | --- |
| 目录迁移 | `语法/` | `learning-notes/grammar-lab/` | 已完成 | 语法资料已集中到 grammar-lab |
| 目录迁移 | `美剧/摩登家庭 S01/` | `learning-notes/tv-series/modern-family/s01/transcript/` | 已完成 | 原始台词 txt 归档 |
| 目录迁移 | `book/摩登家庭/` | `learning-notes/tv-series/modern-family/s01/notes/` | 已完成 | 摩登家庭笔记 md 归档 |
| 目录迁移 | `book/A Day in the Life of Jeff/` | `learning-notes/tv-series/a-day-in-the-life-of-jeff/episode-notes/` | 已完成 | Jeff 系列内容归档 |
| 目录迁移 | `book/不多/` | `learning-notes/parenting-english/` | 已完成 | 亲子英文资料主目录 |
| 目录迁移 | `book/MyOwnEnglishBook/` | `learning-notes/personal-english-book/` | 已完成 | 个人英语材料书目录 |
| 目录清理 | `美剧/` | （移除） | 已完成 | 子目录迁移后空目录已删除 |

### 下一步（仅文件名）

- 保持目录不变，仅重命名文件为统一 `kebab-case`
- 优先处理 `learning-notes/parenting-english/` 与 `learning-notes/personal-english-book/`
- 完成后统一更新内部链接

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

> 已完成第 1 步（目录名）；下一步执行第 2 步（文件名统一），最后集中更新内部链接。

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
