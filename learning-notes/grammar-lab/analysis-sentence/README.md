---
tags:
  - grammar-lab
  - english-learning
  - topic/sentence-structure
aliases:
  - 句子分析使用说明
  - spaCy sentence analysis guide
---

# 长难句分析 · 使用说明（spaCy 依存分析）

**索引：** [[learning-notes/grammar-lab/README|语法实验室索引]]

**原理出处：** [第一轮讲解 17 · 疯狂输入](https://github.com/ZuodaoTech/everyone-can-use-english/blob/master/new-edition-drafts/%E7%AC%AC%E4%B8%80%E8%BD%AE%E8%AE%B2%E8%A7%A3/17-%E7%96%AF%E7%8B%82%E8%BE%93%E5%85%A5.md) ——「写个 Python 脚本调用 spaCy 模块，瞬间帮你分析清楚整个句子的结构」；书稿附录 notebook：[spaCy.ipynb](https://github.com/ZuodaoTech/everyone-can-use-english/blob/master/new-edition-drafts/jupyter-notebooks/spaCy.ipynb)。

**本页目的：** 任何一句读不懂的英文长句，丢进本目录，一条命令得到 **词性标注 + 依存关系 + 主句谓语(ROOT) + 依存结构图**，然后自己把「枝叶」摘掉、留下「主干」。

---

## 一、环境安装（一次性）

```bash
/usr/local/bin/python3.12 -m venv /tmp/spacy-venv
/tmp/spacy-venv/bin/pip install spacy cairosvg
/tmp/spacy-venv/bin/python -m spacy download en_core_web_sm
```

> `/tmp` 重启后清空；换个固定位置（如 `~/.venvs/spacy`）即可长期使用。系统自带 Python 3.9 太旧，请用 `/usr/local/bin/python3.12`。

## 二、日常使用（两步）

**第 1 步**：在本目录新建（或打开）一个 `.md` 文件，把要分析的句子粘进去，一句或多句均可。例：`principleoftheday.md`。

**第 2 步**：运行分析脚本：

```bash
cd learning-notes/grammar-lab/analysis-sentence
/tmp/spacy-venv/bin/python analyze_sentence.py principleoftheday.md
```

终端输出三部分，同时在同目录生成 `*-dep.svg` / `*-dep.png` 依存结构图：

| 输出 | 内容 | 用途 |
|------|------|------|
| Token / POS / DEP 表 | 每个词的词性、依存角色、依附对象 | 看清每个词「挂在谁身上」 |
| ROOT | 主句谓语动词 | 全句的「骨架动词」 |
| 主句简化版 | ROOT 与其直接子成分拼接 | 快速主干（**局限见第五节**） |
| 依存图 PNG/SVG | displaCy 可视化 | 直观确认结构 |

## 三、输出解读速查

**词性 POS（常用）：**

| 标签 | 含义 | 简中 |
|------|------|------|
| NOUN / PROPN | 名词 / 专有名词 | 人事物 |
| VERB / AUX | 实义动词 / 助动词（be, do, will…） | 动作 / 辅助 |
| ADJ / ADV | 形容词 / 副词 | 修饰名 / 修饰动形 |
| PRON / DET | 代词 / 限定词（the, a…） | 指代 / 限定 |
| ADP | 介词（in, of, with…） | 依附关系 |
| SCONJ / CCONJ | 从属连词（while, because, if…）/ 并列连词（and, but） | 引从句 / 并列 |
| PART | 小品词（n't, to, 's） | 否定/不定式/所有格 |

**依存 DEP（常用）：**

| 标签 | 含义 | 简中 |
|------|------|------|
| ROOT | 主句谓语 | 全句骨架动词 |
| nsubj | 主语 | 动作的发出者 |
| dobj / pobj | 动词宾语 / 介词宾语 | 承受者 |
| advcl | 状语从句（while/because/if/when 引导） | 让步/原因/条件/时间 |
| relcl | 关系从句（that/which/who 引导定从） | 名词后长定语 |
| acomp / xcomp | 形容词补足语 / 动词不定式补足语 | 系表 / to do |
| amod / advmod | 形容词修饰 / 副词修饰 | 枝叶 |
| mark | 从句引导词标记 | while/because/that 本身 |

> 读法口诀：**先找 ROOT，再找它的 nsubj（主语）和 dobj/acomp（宾/表），其余 advcl / relcl / 介词短语都是枝叶。**

## 四、实例：principleoftheday.md（Dalio《原则》）

**Sentence 1** — ROOT = `is`（系动词），主句是「主系表」：

```
it is especially important to share the things that are most difficult to share
```

- `it` 是**形式主语**，真正主语是不定式 `to share the things …`
- 枝叶 1：`While it might be tempting to limit transparency to the things that can't hurt you` —— **让步状从**（"虽然把透明只留给无伤大雅的事很诱人"）
- 枝叶 2：`that are most difficult to share` —— 定从修饰 `things`
- 枝叶 3：`because if you don't share them you will lose the trust and partnership of the people you are not sharing with` —— **原因状从**，内部还套着 `if` 条件从和 `you are not sharing with` 省略关系词的定从

![Sentence 1 依存图](principleoftheday-sent1-dep.png)

**Sentence 2** — ROOT = `be`，主句：

```
the question should not be whether to share but how
```

- 枝叶：`when faced with the decision to share the hardest things` —— 省略主语的**时间状从**（= when *you are* faced with …）

![Sentence 2 依存图](principleoftheday-sent2-dep.png)

## 五、注意事项与局限

1. **「主句简化版」只对简单句可靠。** 它是 ROOT + 直接子成分的机械拼接；遇到本例这种多从句长句会产生乱序（如 `Be is , it important share , lose.`）。**正确做法**：用 ROOT 定位骨架动词后，按第三节口诀人工摘主干——工具负责「定位」，你负责「取舍」。
2. **模型会犯错。** `en_core_web_sm` 是小模型（快但不够准），歧义结构可能标错；拿不准时换大模型：`python -m spacy download en_core_web_trf`（慢、需更多内存）。
3. **撇号会拆词**：`can't` → `ca` + `n't`，`Earth’s` → `Earth` + `’s`，看表时自动脑补还原。
4. 依存图 SVG 可直接拖进浏览器放大查看；PNG 供笔记内嵌。

## 六、相关笔记

- [[learning-notes/grammar-lab/sentence-expansion-and-component-order|句子扩写与成分换序示范]] — 主谓宾状补成分速查（本页 POS/DEP 表的「岗位」视角）
- [[learning-notes/grammar-lab/english-grammar-system-overview-yingyutu|英语语法体系总览（英语兔）]] — 从句模块提纲
- [[learning-notes/grammar-lab/english-language-taxonomy|英语语言单位分类]] — 句子在语言单位中的位置
