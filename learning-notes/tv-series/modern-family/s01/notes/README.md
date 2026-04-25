# 《摩登家庭》S01 — 学习材料索引

本目录收录 **第一季（S01）** 与《摩登家庭》相关的英文学习笔记，字幕源文件在 `../transcript/`。

## 文件类型


| 类型                                                | 说明                                                              |
| ------------------------------------------------- | --------------------------------------------------------------- |
| **modern-family-s01exx-daily-lines.md**              | 从对应 `modern-family-s01exx-transcript.txt` **自动抽取**英中句对，按粗分类（出行、居家、亲子等）分组；适合快速刷句、跟读。 |
| **modern-family-s01e02-key-to-being-a-great-dad.md** | **手工编排**的亲子对话体练习（张泽 / Celine 设定），与自动抽取版互补。                                       |
| **scripts/build-modern-family-s01-md.py**            | 生成「生活实用英文句」的脚本；字幕更新后可重新运行。                                                   |


## 剧集列表


| 集数    | 生活实用句（notes）                                                                                                                        | 字幕（txt）                                                                              |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| E01   | [modern-family-s01e01-daily-lines.md](modern-family-s01e01-daily-lines.md)                                                       | `../transcript/modern-family-s01e01-transcript.txt`                                  |
| E02   | [modern-family-s01e02-daily-lines.md](modern-family-s01e02-daily-lines.md) + [亲子主题对话](modern-family-s01e02-key-to-being-a-great-dad.md) | `../transcript/modern-family-s01e02-transcript.txt`                                  |
| E03–E24 | `modern-family-s01e03-daily-lines.md` … `modern-family-s01e24-daily-lines.md`                                                   | `../transcript/modern-family-s01e03-transcript.txt` … `../transcript/modern-family-s01e24-transcript.txt` |


**说明：** E12 若字幕文件为空，对应 `modern-family-s01e12-daily-lines.md` 内会有占位说明；补齐字幕后请重新运行脚本。

## 重新生成「生活实用英文句」

在仓库根目录执行：

```bash
python3 learning-notes/tv-series/modern-family/s01/notes/scripts/build-modern-family-s01-md.py
```

## 另见

- 手写精编（夏威夷机场主题示例）：`../transcript/modern-family-s01e22-daily-lines.md`（可与 `modern-family-s01e22-daily-lines.md` 同时对照：前者偏人工场景归纳，后者为全量自动抽取子集）。

