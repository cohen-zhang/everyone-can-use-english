# 每日语音文本

本目录存放**待朗读的英文原文**（`.md` / `.txt`），以及脚本生成的 **MP3 + WebVTT 字幕**。

## 环境准备（首次）

在项目根目录执行：

```bash
python3 -m venv .venv-tts
.venv-tts/bin/pip install -r requirements-tts.txt
```

依赖说明见根目录 [`requirements-tts.txt`](../requirements-tts.txt)。  
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

- 转换脚本：[`scripts/edge_tts_article.py`](../scripts/edge_tts_article.py)
- Jupyter 示例：[`1000-hours/public/jupyter-notebooks/edge-tts.ipynb`](../1000-hours/public/jupyter-notebooks/edge-tts.ipynb)
