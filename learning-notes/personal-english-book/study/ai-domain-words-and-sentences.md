---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - vocabulary/ai
aliases:
  - AI 领域单词与句子
  - AI domain English
---

# AI 领域 · 单词与句子表达

**索引：** [[learning-notes/personal-english-book/README|个人英文材料书索引]] · [[learning-notes/personal-english-book/study/index|study · 学习]]
**相关：**
- [[learning-notes/personal-english-book/vocab-story/2026.03.18 计算机专业AI|计算机专业 AI 词汇（322）]] — 计科混排词表；本页只收大模型研发口语
- [[learning-notes/personal-english-book/study/computer-science-vocab-interesting|有趣计科词汇]] — 工具与系统词的趣味记法
- [[learning-notes/personal-english-book/work/r-and-d-workflow|研发流程]] — 立项、演示、发布话术
- [[learning-notes/personal-english-book/work/专业术语|工作专业术语]] — 复现、影响域、编译等研发语块

> **分工：** 322 词表按计科学习场景铺开。本页给 **阿泽** 在评审、站会、排障里直接开口：词、语块、短句都按「先英后中」排，技术词加粗。

## 本页在做什么

按一条真实链路组织：**模型与训练 → 提示与上下文 → 检索增强 → 工具与智能体 → 评测 → 推理与上线 → 协作口语句**。每句控制在能一口气读完的长度。下文顺序：**语块速查 → 分主题词句 → 易混 → 朗读串联**。

---

## 重点可复用语块（Reusable chunks）

| 语块 | 英文示例 | 用途 |
| --- | --- | --- |
| 大语言模型 `技术` | *large language model* / *LLM* | 开口先定对象 |
| 上下文窗口 `技术` | *context window* | 超长就裁 |
| 提示词 `技术` | *prompt* / *system prompt* | 改行为，先改提示 |
| 检索增强 `技术` | *retrieval-augmented generation* / *RAG* | 先查再答 |
| 幻觉 `技术` | *hallucination* | 答得顺、事实错 |
| 工具调用 `技术` | *tool call* / *function calling* | 模型去调接口 |
| 人工把关 `技术` | *human in the loop* | 高风险步骤停一下 |
| 评测集 `技术` | *eval set* / *golden set* | 改完要回归 |
| 推理延迟 `技术` | *inference latency* | 上线看等待 |
| 降级 `技术` | *fall back to a smaller model* | 超时或限流 |

---

## A. 模型与训练（Model and training）

| 英文 | IPA | 简中 | 记忆钩 |
| --- | --- | --- | --- |
| **model** `技术` | /ˈmɑːdl/ | 模型 | 会答题的那一套权重 |
| **weights** `技术` | /weɪts/ | 权重 | 训练写进文件里的数字 |
| **token** `技术` | /ˈtoʊkən/ | 词元 | 模型读写的最小块，不等于英文单词 |
| **embedding** `技术` | /ɪmˈbedɪŋ/ | 向量表示 | 把文本变成可比较的一串数 |
| **pretrain** `技术` | /ˌpriːˈtreɪn/ | 预训练 | 先在海量文本上打底 |
| **fine-tune** `技术` | /ˌfaɪn ˈtuːn/ | 微调 | 用你的任务数据再收一收 |
| **checkpoint** `技术` | /ˈtʃekpɔɪnt/ | 检查点 | 训练中途存下来的一版权重 |
| **overfit** `技术` | /ˌoʊvərˈfɪt/ | 过拟合 | 训练集很熟，新题就慌 |

**可复用句**

- **We start from a base model, then fine-tune on our task data.** — 我们从基座模型出发，再用任务数据微调。
- **One English word can split into several tokens.** — 一个英文单词可能被切成好几个 token。
- **Save a checkpoint before you change the learning rate.** — 改学习率之前先存一个检查点。
- **It memorized the training set. That is overfitting.** — 它把训练集背下来了。这就是过拟合。

---

## B. 提示与上下文（Prompt and context）

| 英文 | IPA | 简中 | 记忆钩 |
| --- | --- | --- | --- |
| **prompt** `技术` | /prɑːmpt/ | 提示词 | 你交给模型的任务说明 |
| **system prompt** `技术` | — | 系统提示 | 定角色和底线，用户看不见也生效 |
| **context window** `技术` | /ˈkɑːntekst ˈwɪndoʊ/ | 上下文窗口 | 这一轮模型能看见的总长度 |
| **few-shot** `技术` | /ˈfjuː ʃɑːt/ | 少样本 | 提示里放两三条例子 |
| **temperature** `技术` | /ˈtemprətʃər/ | 温度 | 越高越散，越低越稳 |
| **hallucination** `技术` | /həˌluːsɪˈneɪʃn/ | 幻觉 | 语气自信，内容是编的 |
| **ground** `技术` | /ɡraʊnd/ | 把回答钉在依据上 | *ground the answer in the docs* |

**可复用句**

- **Put the output format in the system prompt.** — 把输出格式写进系统提示。
- **This prompt is vague. Ask for a JSON object.** — 这条提示太虚。要求返回一个 JSON 对象。
- **We blew the context window. Cut the history.** — 上下文窗口爆了。把历史裁短。
- **Lower the temperature when you need a stable answer.** — 要稳定答案时把温度调低。
- **The model hallucinated a field that is not in the schema.** — 模型编了一个 schema 里没有的字段。
- **Ground every claim in the retrieved passage.** — 每条说法都要落到检索到的段落上。

---

## C. 检索增强（Retrieval-augmented generation）

| 英文 | IPA | 简中 | 记忆钩 |
| --- | --- | --- | --- |
| **RAG** `技术` | /ræɡ/ | 检索增强生成 | 先搜资料，再让模型组织答案 |
| **chunk** `技术` | /tʃʌŋk/ | 切片 | 长文档切成可检索的小段 |
| **vector store** `技术` | — | 向量库 | 按 embedding 找近邻 |
| **rerank** `技术` | /ˌriːˈræŋk/ | 重排序 | 粗召回之后再精排一遍 |
| **citation** `技术` | /saɪˈteɪʃn/ | 引用 | 答案旁边标来源 |
| **stale** `技术` | /steɪl/ | 过期的 | 索引没跟上文档 |

**可复用句**

- **Chunk the doc before you embed it.** — 先切片，再做向量。
- **Retrieval missed the page. The answer had nothing to stand on.** — 检索没捞到那一页。答案没有依据。
- **Rerank the top hits before you stuff them into the prompt.** — 塞进提示之前，先把靠前结果重排。
- **Ask the model to cite the chunk id.** — 让模型标出切片编号。
- **The index is stale. Rebuild it after the doc update.** — 索引过期了。文档更新后重建。

---

## D. 工具与智能体（Tools and agents）

| 英文 | IPA | 简中 | 记忆钩 |
| --- | --- | --- | --- |
| **agent** `技术` | /ˈeɪdʒənt/ | 智能体 | 能规划、能调工具、能多走几步 |
| **tool call** `技术` | — | 工具调用 | 模型选出函数和参数 |
| **schema** `技术` | /ˈskiːmə/ | 结构约定 | 参数和返回值长什么样 |
| **orchestrate** `技术` | /ˈɔːrkɪstreɪt/ | 编排 | 把多步串成一条流程 |
| **guardrail** `技术` | /ˈɡɑːrdreɪl/ | 护栏 | 不许越界的检查 |
| **human in the loop** `技术` | — | 人工在环 | 关键步等人点头 |

**可复用句**

- **The agent picked the wrong tool.** — 智能体选错了工具。
- **Validate the tool arguments against the schema.** — 用 schema 校验工具参数。
- **Do not run the write call until a human approves it.** — 写操作等人批准再执行。
- **Add a guardrail: refuse requests with no source id.** — 加一道护栏：没有来源编号就拒绝。
- **Orchestrate retrieve, answer, then cite.** — 按「检索、作答、引用」编排。

---

## E. 评测（Evaluation）

| 英文 | IPA | 简中 | 记忆钩 |
| --- | --- | --- | --- |
| **eval set** `技术` | — | 评测集 | 固定题目，用来比版本 |
| **golden set** `技术` | — | 金标准集 | 人工认定的正确答案 |
| **benchmark** `技术` | /ˈbentʃmɑːrk/ | 基准测试 | 同一套题比模型 |
| **regression** `技术` | /rɪˈɡreʃn/ | 回退 | 新版本把旧题答差了 |
| **latency** `技术` | /ˈleɪtənsi/ | 延迟 | 用户等多久 |
| **throughput** `技术` | /ˈθruːpʊt/ | 吞吐 | 单位时间能打完多少请求 |

**可复用句**

- **Run the eval set before we ship the prompt change.** — 提示改动上线前先跑评测集。
- **Three golden cases regressed.** — 三个金标准用例退步了。
- **Latency improved, but the answers got sloppier.** — 延迟好了，答案却更松了。
- **Track tokens per request. Cost follows tokens.** — 盯每请求的 token 数。费用跟着 token 走。

---

## F. 推理与上线（Inference and serving）

| 英文 | IPA | 简中 | 记忆钩 |
| --- | --- | --- | --- |
| **inference** `技术` | /ˈɪnfərəns/ | 推理 | 用训好的模型来答题，不再更新权重 |
| **stream** `技术` | /striːm/ | 流式输出 | 边生成边返回 |
| **quantize** `技术` | /ˈkwɑːntaɪz/ | 量化 | 把权重压小，换速度和显存 |
| **rate limit** `技术` | — | 限流 | 超过配额就拒绝或排队 |
| **time out** `技术` | — | 超时 | 等太久就停 |
| **fall back** `技术` | — | 降级 | 主模型不行就换备用 |

**可复用句**

- **Stream the tokens so the UI does not sit blank.** — 把 token 流式吐出去，界面别空等。
- **Quantize the model if memory is the bottleneck.** — 内存是瓶颈就量化模型。
- **We hit the rate limit. Back off and retry.** — 撞上限流了。退避再重试。
- **If the primary times out, fall back to the smaller model.** — 主模型超时就降级到小模型。
- **Log the prompt and the completion on failure.** — 失败时把提示和补全都记下来。

---

## G. 协作口语句（Standup, review, incident）

阿泽在设计评审和事故同步里可直接改几个名词复用。

### G.1 站会

| 中文意图 | 英文 |
| --- | --- |
| 今天接检索 | I am wiring **retrieval** into the service today. |
| 提示还太长 | The **prompt** is still too long for the **context window**. |
| 空上下文会编 | On an empty context, the model **hallucinates**. |
| 评测还没跑 | I have not run the **eval set** yet. |

### G.2 评审

| 中文意图 | 英文 |
| --- | --- |
| 先定输出格式 | Please lock the **output schema** before we tune wording. |
| 不要盲信工具结果 | Do not trust the **tool result** until it matches the **schema**. |
| 引用必须可点回 | Every answer needs a **citation** we can open. |
| 写操作留人审 | Keep a **human in the loop** on write actions. |

### G.3 事故

| 中文意图 | 英文 |
| --- | --- |
| 延迟在加长上限后飙了 | **Latency** jumped after we raised **max tokens**. |
| 索引是旧的 | The bad answers came from a **stale** index. |
| 先降级止血 | **Fall back** now. We can debug the prompt after. |
| 影响面 | The **blast radius** is the search API, not checkout. |

**可合并为一段（事故同步）**

> **Latency** jumped after we raised **max tokens**. Bad answers also came from a **stale** index. We will **fall back** to the smaller model now, rebuild the index, and rerun the **eval set**.

简中：把 max tokens 调高之后延迟跳了上去。错答案还来自一份过期索引。我们现在先降级到小模型，重建索引，再重跑评测集。

---

## H. 易混（Pairs that slip）

| 一对 | 怎么分 |
| --- | --- |
| **model** / **weights** | model 是你调用的那个东西；weights 是它肚子里的参数文件。 |
| **prompt** / **context** | prompt 是你写的指令；context 是这一轮塞进窗口的全部内容，含历史和检索片段。 |
| **fine-tune** / **prompt change** | 微调改权重，要数据和训练；改提示只改文本，当下就能试。 |
| **embedding** / **token** | token 是切出来的片段；embedding 是片段（或整段）对应的向量。 |
| **latency** / **throughput** | latency 是单次等待；throughput 是一分钟能完成多少次。 |
| **hallucination** / **bug** | bug 是程序走错分支；hallucination 是模型编了一段看起来像真的话。 |
| **agent** / **one tool call** | 一次 tool call 只是调一个函数；agent 会自己决定下一步还调不调。 |

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **We start from a base model, then fine-tune on our task data.** — 从基座模型出发，再用任务数据微调。
- **We blew the context window. Cut the history.** — 上下文窗口爆了，把历史裁短。
- **Ground every claim in the retrieved passage.** — 每条说法都落到检索段落上。
- **Validate the tool arguments against the schema.** — 用 schema 校验工具参数。
- **Three golden cases regressed.** — 三个金标准用例退步了。
- **If the primary times out, fall back to the smaller model.** — 主模型超时就降级到小模型。

### B. 一段串联（连续口语）

We start from a base model, then fine-tune on our task data. The prompt still blows the context window, so we cut history and ground every claim in a retrieved passage. Tool arguments must match the schema. Three golden cases regressed, and if the primary times out, we fall back to the smaller model.

**简中：** 我们从基座模型出发，再用任务数据微调。提示仍然撑爆上下文窗口，所以我们裁掉历史，并把每条说法钉在检索段落上。工具参数必须符合 schema。三个金标准用例退步了；主模型一旦超时，就降级到小模型。

### C. 一分钟复盘（6 句）

1. **fine-tune on our task data** — 用任务数据微调
2. **context window** — 上下文窗口
3. **ground every claim** — 每条说法要有依据
4. **tool arguments** / **schema** — 工具参数要符合结构约定
5. **golden cases regressed** — 金标准用例退步
6. **fall back to the smaller model** — 降级到小模型
