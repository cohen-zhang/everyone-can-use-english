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
| `parenting-english` | 亲子英语资料库 | 日常场景、词汇表、互动游戏、90天计划 |
| `personal-english-book` | 个人英语材料书 | 生活、工作、学习三大分区 |
| `life` | 生活场景 | 情绪、天气、社区、日常表达 |
| `work` | 工作场景 | IM沟通、会议、出差、流程与业务表达 |
| `study` | 学习场景 | 技术英语、学习日志、术语积累 |

### 命名与维护规则（简版）

- 文件夹与文件统一使用 `kebab-case`
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
