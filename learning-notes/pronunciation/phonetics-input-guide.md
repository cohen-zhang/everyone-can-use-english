---
tags:
  - pronunciation
  - personal-english-book
  - english-learning
  - peb/study
aliases:
  - 音标输入指南
---
# 音标输入指南 —— Phonetics Input Guide for Engineers

**索引：** [[learning-notes/pronunciation/README|发音资料索引]] · [[learning-notes/personal-english-book/README|个人英文材料书索引]]
**相关：** [[learning-notes/pronunciation/phonetics-engineer-quick-reference|音标工程师速查]] · [[learning-notes/pronunciation/syllable-division-ipa-based|音节划分 · IPA]] — 速查表与此篇 **相向互链**。

#phonetics #input-method #tools #markdown #音标输入 #工程师工具

> **Aze** (阿泽) —— 在 Obsidian / Markdown 中输入 IPA 音标的实用方法

---

## 1. 快速输入方案 Quick Input Solutions

### 1.1 macOS 原生输入 Native Input

| 方法 | 操作 | 示例 |
|------|------|------|
| 字符检视器 | `Control + Command + Space` | 搜索 "schwa" 找 ə |
| 长按字母键 | 长按 `a` 选 `æ` | a → æ |
| 国际键盘 | 添加 `ABC - Extended` 键盘 | `Option + b` = ∫ |

### 1.2 VS Code / Cursor 插件

- **IPA Symbols** —— 国际音标快速插入
- **Unicode Input** —— 直接输入 Unicode 编码

### 1.3 常用音标对照表 Common Symbols

| 音标 | Unicode | HTML Entity | 描述 |
|------|---------|-------------|------|
| ə | `U+0259` | `&#601;` | Schwa 央元音 |
| ɑ | `U+0251` | `&#593;` | 开后元音 |
| ɔ | `U+0254` | `&#596;` | 开后圆唇元音 |
| ɪ | `U+026A` | `&#618;` | 短 i |
| ʊ | `U+028A` | `&#650;` | 短 u |
| ʌ | `U+028C` | `&#652;` | 开央元音 |
| ɛ | `U+025B` | `&#603;` | 开 e |
| ŋ | `U+014B` | `&#331;` | 软腭鼻音 |
| ʃ | `U+0283` | `&#643;` | 清齿龈后擦音 |
| ʒ | `U+0292` | `&#658;` | 浊齿龈后擦音 |
| θ | `U+03B8` | `&#952;` | 清齿间擦音 |
| ð | `U+00F0` | `&#240;` | 浊齿间擦音 |
| ɹ | `U+0279` | `&#633;` | 卷舌近音 |
| ɾ | `U+027E` | `&#638;` | 齿龈闪音 |
| ˈ | `U+02C8` | `&#712;` | 主重音 |
| ˌ | `U+02CC` | `&#716;` | 次重音 |
| ː | `U+02D0` | `&#720;` | 长音符号 |

---

## 2. Obsidian 中使用音标 Using Phonetics in Obsidian

### 2.1 HTML 标签方案 (推荐)

使用 `<span class="pho">` 标签配合自定义 CSS：

```html
<span class="pho">ə</span> → <span class="pho">ə</span>
<span class="pho alt">ˈsɪstəm</span> → <span class="pho alt">ˈsɪstəm</span>
```

### 2.2 CSS 样式 CSS Snippet

添加到你的 `.obsidian/snippets/` 文件夹：

```css
/* phonetics.css */
.pho {
  font-family: "Doulos SIL", "Charis SIL", "Arial Unicode MS", serif;
  color: #2e7d32;
  font-weight: 500;
}

.pho.alt {
  background: #e8f5e9;
  padding: 2px 6px;
  border-radius: 4px;
}
```

### 2.3 快捷输入模板 Templater Template

创建模板文件 `templates/phonetic-symbol.md`：

```markdown
<%*
const symbols = {
  schwa: "ə",
  long_a: "ɑː",
  short_a: "ʌ",
  long_i: "iː",
  short_i: "ɪ",
  ng: "ŋ",
  sh: "ʃ",
  th_voiceless: "θ",
  th_voiced: "ð",
  zh: "ʒ",
  primary_stress: "ˈ",
  secondary_stress: "ˌ",
  long_mark: "ː"
};

const choice = await tp.system.suggester(
  Object.keys(symbols),
  Object.values(symbols),
  false,
  "选择音标 Select phonetic symbol"
);
%><% choice %>
```

---

## 3. Markdown 音标表示法 Markdown Representation

### 3.1 纯文本方案 Plain Text

| 方案 | 写法 | 显示 |
|------|------|------|
| 斜杠包围 | `/ə/` | /ə/ |
| 方括号 | `[ə]` | [ə] |
| 双斜杠 | `//ˈsɪstəm//` | //ˈsɪstəm// |

### 3.2 代码块方案 Code Block

```markdown
`ə`  ← 行内代码
```

### 3.3 LaTeX 方案 (需插件)

使用 **Obsidian Math+** 或原生 LaTeX：

```latex
$\textschwa$  →  schwa 符号
$\ipa{ə}$     →  需要 tipa 包
```

---

## 4. 音标字体推荐 Font Recommendations

| 字体 | 特点 | 获取 |
|------|------|------|
| **Doulos SIL** | IPA 专用，免费 | [SIL官网](https://software.sil.org/doulos/) |
| **Charis SIL** | 衬线，易读 | [SIL官网](https://software.sil.org/charis/) |
| **Gentium Plus** | 学术风格 | [SIL官网](https://software.sil.org/gentium/) |
| **Arial Unicode MS** | 系统自带 | macOS/Windows |
| **Noto Sans** | Google 出品，覆盖广 | [Google Fonts](https://fonts.google.com/noto) |

---

## 5. 实用命令行工具 CLI Tools

### 5.1 音标转 Unicode

```bash
# 使用 Python 快速查询
python3 -c "print('ə'.encode('unicode_escape'))"  # \u0259

# 反向查询
python3 -c "print('\u0259')"  # ə
```

### 5.2 文本替换脚本

```bash
#!/bin/bash
# phonetic-convert.sh - 将简写转换为音标符号

sed -i '' 's/@schwa@/ə/g' "$1"
sed -i '' 's/@sh@/ʃ/g' "$1"
sed -i '' 's/@th@/θ/g' "$1"
sed -i '' 's/@ng@/ŋ/g' "$1"
```

---

## 6. 速查速记 Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│           IPA 音标速查 (Engineer Edition)              │
├─────────────────────────────────────────────────────┤
│  元音 Vowels                                         │
│  ├─ ə (schwa) - system, about                        │
│  ├─ ɑ (ah)    - database, father                     │
│  ├─ i (ee)    - feature, team                        │
│  ├─ u (oo)    - group, route                         │
│  ├─ e (eh)    - tech, dev                            │
│  └─ ɔ (aw)    - core, deploy                         │
├─────────────────────────────────────────────────────┤
│  辅音 Consonants (清/浊配对)                          │
│  ├─ p/b - pull/build                                 │
│  ├─ t/d - test/debug                                 │
│  ├─ k/g - cache/grep                                 │
│  ├─ f/v - file/variable                              │
│  ├─ s/z - sync/zip                                   │
│  ├─ θ/ð - path/mother                                │
│  └─ ʃ/ʒ - shell/version                              │
├─────────────────────────────────────────────────────┤
│  特殊标记 Special Marks                              │
│  ├─ ˈ   - 主重音 (primary stress)                    │
│  ├─ ˌ   - 次重音 (secondary stress)                  │
│  └─ ː   - 长音 (length mark)                         │
└─────────────────────────────────────────────────────┘
```

---

## 7. 相关文档双向链接 Related Documents

- [[learning-notes/pronunciation/phonetics-engineer-quick-reference|音标速查手册 Main Reference]]
- [[8.1-inputting-phonemes-and-symbols|音标输入详解 Detailed Input Guide]]
- [[1.2-alphabets|字母与音素对应 Alphabets & Phonemes]]
- [[8.2-cepd-phonetics-and-sound|剑桥发音词典 CEPD Guide]]

---

## 8. 待办 / 笔记 TODO / Notes

- [ ] 配置 Obsidian CSS snippet for phonetics
- [ ] 安装 Templater 音标模板
- [ ] 测试不同字体显示效果
- [ ] 补充更多技术词汇发音

---

*Created by Aze (阿泽) for Engineer English Learning*

*Last updated: {{date:YYYY-MM-DD}}*
