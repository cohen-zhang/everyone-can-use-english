# 每日语音文本

纯英文朗读稿，供跟读、Enjoy 导入。GitHub Pages 顶栏 **每日语音文本** 即本目录。

## 朗读目录

### 亲子英语 · 日常生活

- [[每日语音文本/parenting-english/daily-life/parenting-bathing-daily-phrases|洗澡日常]]
- [[每日语音文本/parenting-english/daily-life/parenting-emotions-kids-edition|情绪]]
- [[每日语音文本/parenting-english/daily-life/parenting-family-rules-routine-daily-phrases|家庭守则与作息]]
- [[每日语音文本/parenting-english/daily-life/parenting-girl-grooming-daily-phrases|梳妆打扮]]
- [[每日语音文本/parenting-english/daily-life/parenting-haircut-daily-phrases|理发]]
- [[每日语音文本/parenting-english/daily-life/parenting-hiking-with-kids-daily-phrases|亲子 Hiking]]
- [[每日语音文本/parenting-english/daily-life/parenting-home-appliance-daily-phrases|电器使用日常]]
- [[每日语音文本/parenting-english/daily-life/parenting-homework-check-in-daily-phrases|家庭作业打卡]]
- [[每日语音文本/parenting-english/daily-life/parenting-metro-scenario-phrases|地铁场景]]
- [[每日语音文本/parenting-english/daily-life/parenting-phone-daily-phrases|手机使用日常]]
- [[每日语音文本/parenting-english/daily-life/parenting-praise-kids-daily-phrases|夸奖、赞美小朋友]]
- [[每日语音文本/parenting-english/daily-life/parenting-shenzhen-dressing-daily-phrases|穿衣日常]]
- [[每日语音文本/parenting-english/daily-life/parenting-shenzhen-park-daily-phrases|深圳公园场景]]
- [[每日语音文本/parenting-english/daily-life/parenting-space-cosmos-daily-phrases|宇宙 · 航天]]
- [[每日语音文本/parenting-english/daily-life/parenting-table-manners-daily-phrases|日常礼貌与餐桌礼仪]]
- [[每日语音文本/parenting-english/daily-life/parenting-tidy-up-daily-phrases|收拾整理日常]]
- [[每日语音文本/parenting-english/daily-life/parenting-time-expressions-daily-phrases|时间表达汇总]]

### 亲子英语 · 词汇

- [[每日语音文本/parenting-english/vocabulary/parenting-actions-vocab|动作 — 日常物品场景]]
- [[每日语音文本/parenting-english/vocabulary/parenting-actions-vocab-extended-routines|动作动词 — 分类总表]]
- [[每日语音文本/parenting-english/vocabulary/parenting-animals-vocab|动物单词]]
- [[每日语音文本/parenting-english/vocabulary/parenting-china-food-common-vocab|中国常见食物]]
- [[每日语音文本/parenting-english/vocabulary/color|颜色]]
- [[每日语音文本/parenting-english/vocabulary/parenting-countries-continents-oceans-vocab|大洲 · 大洋 · 常见国家]]
- [[每日语音文本/parenting-english/vocabulary/parenting-emoji-bilingual-vocab|Emoji 表情]]
- [[每日语音文本/parenting-english/vocabulary/parenting-jobs-roles-vocab|职业与角色]]
- [[每日语音文本/parenting-english/vocabulary/parenting-materials-shapes-dimensions-vocab|物体材质 · 形状 · 维度]]
- [[每日语音文本/parenting-english/vocabulary/parenting-seasons-months-zodiac-planets-space-vocab|季节 · 月份 · 星座 · 行星]]
- [[每日语音文本/parenting-english/vocabulary/parenting-symbols-common-vocab|常见符号]]

### 其他

- [[每日语音文本/world-cinema-quick-notes|World cinema]]

---

本目录也存放脚本生成的 **MP3 + WebVTT 字幕**（不进网页）。

## 环境准备（首次）

在项目根目录执行：

```bash
python3 -m venv .venv-tts
.venv-tts/bin/pip install -r requirements-tts.txt
```

依赖说明见根目录 [`requirements-tts.txt`](https://github.com/cohen-zhang/everyone-can-use-english/blob/master/requirements-tts.txt)。  
TTS 引擎为 [edge-tts](https://github.com/rany2/edge-tts)，调用 Microsoft Edge 在线语音服务，**需要联网**。

## 基本用法

在项目根目录，对任意文本文件生成同名的 `.mp3` 和 `.vtt`（输出到**与源文件相同目录**）：

```bash
.venv-tts/bin/python scripts/edge_tts_article.py "每日语音文本/你的文件.md"
```

**示例（本目录已有）：**

```bash
.venv-tts/bin/python scripts/edge_tts_article.py "每日语音文本/world-cinema-quick-notes.md"
```

生成结果：

- `每日语音文本/world-cinema-quick-notes.mp3`
- `每日语音文本/world-cinema-quick-notes.vtt`

默认音色：**`en-US-GuyNeural`**（美音男声）。

## 常用选项

| 选项 | 说明 |
|------|------|
| `-v VOICE` / `--voice VOICE` | 更换音色，如 `en-US-JennyNeural` |
| `-o DIR` / `--output-dir DIR` | 指定输出目录（默认与源文件同目录） |
| `--print-text` | 只打印提取出的英文，不生成音频 |
| `--raw` | 不提取，整文件原样朗读 |
| `--stop-at-h2` | 遇到第一个 `##` 标题时停止提取（适合长笔记只读开头段落） |

**换女声：**

```bash
.venv-tts/bin/python scripts/edge_tts_article.py "每日语音文本/通勤.md" -v en-US-JennyNeural
```

**预览提取结果：**

```bash
.venv-tts/bin/python scripts/edge_tts_article.py "每日语音文本/通勤.md" --print-text
```

**列出可用英文音色：**

```bash
.venv-tts/bin/pip show edge-tts   # 确认已安装
.venv-tts/bin/edge-tts --list-voices | grep en-
```

## 文本文件怎么写

本目录文件以**纯英文段落**为主即可，例如：

```markdown


First paragraph of English text.

Second paragraph continues here.
```

脚本会自动：

- 跳过 YAML frontmatter（`---` 包裹的元数据）
- 跳过以 `#` 开头的标题、引用块、wikilink 索引行
- 跳过中文为主的行
- 去掉 `**粗体**`、链接等 Markdown 标记

若文件**几乎全是英文**（如本目录多数文件），无需额外处理；若从 `learning-notes/` 复制完整笔记，可用 `--stop-at-h2` 只朗读正文第一段，或单独复制英文到本目录。

## 输出说明

| 文件 | 用途 |
|------|------|
| `.mp3` | 朗读音频，可用系统播放器或 Enjoy 导入 |
| `.vtt` | WebVTT 字幕，按句分段，可与 MP3 对照听读 |

重新运行脚本会**覆盖**同名 `.mp3` / `.vtt`。

## 推荐音色（英文）

| 音色 | 说明 |
|------|------|
| `en-US-GuyNeural` | 美音男声（默认） |
| `en-US-JennyNeural` | 美音女声 |
| `en-GB-ThomasNeural` | 英音男声 |
| `en-GB-MaisieNeural` | 英音女声 |

## 相关文件

- 转换脚本：[`scripts/edge_tts_article.py`](https://github.com/cohen-zhang/everyone-can-use-english/blob/master/scripts/edge_tts_article.py)
