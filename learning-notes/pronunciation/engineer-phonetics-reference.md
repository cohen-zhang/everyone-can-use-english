---
tags:
  - pronunciation
  - personal-english-book
  - english-learning
  - peb/study
  - topic/chinese-learner
aliases:
  - 音标工程师速查
  - 工程师音标速查
  - phonetics-engineer-quick-reference
---
# 工程师音标速查 · Engineer Phonetics Reference

**索引：** [[learning-notes/pronunciation/README|发音资料索引]] · [[learning-notes/personal-english-book/README|个人英文材料书索引]]

**完整教程：** [[learning-notes/pronunciation/english-phonetics-textbook|英文语音完整教程]] —— 系统学习请从此处进入；本页为查词 / 笔记时的速查表。

**相关：** [[learning-notes/pronunciation/phonetics-input-guide|音标输入指南]] · [[learning-notes/pronunciation/syllable-division-ipa-based|音节划分与重音 · IPA]] · [[learning-notes/pronunciation/vocabulary-tricky-pronunciation-149|易读错词汇 149]]

#phonetics #english-learning #engineer-reference #pronunciation #音标 #发音 #英语学习

> **Aze** (阿泽) —— 工程师专用音标速查表。目标不是替代完整语音教程，而是让你在查技术词、做英文笔记、跟读录音时，能快速判断「这个符号怎么读、我最该注意什么」。

---

## 1. 先搞清楚：音素、音标、词典体系

**音素（phoneme）** 是自然语流中不可再分的声音单位；**音标（phonetic symbol）** 是记录音素的符号。学习顺序建议是：**先听声音，再把声音映射到符号**，最后做到「看到音标能发音，听到音素能大致写出音标」。

> 参考来源：[[book/chapter3|《人人都能用英语》ch.3]] · [[1000-hours/sounds-of-american-english/1.1-phonemes|1000h · 1.1 音素与音标]] · [[new-edition-drafts/英文语音简明教程|英文语音简明教程]]

### 1.1 工程师怎么用这页

1. **先查真人发音**：Cambridge / Merriam-Webster / Oxford 等电子词典优先。
2. **只选一个主体系**：日常以自己常用词典为准，不必同时背 D.J.、K.K.、IPA 的所有差异。
3. **只标关键差异**：常规拼读不用全抄；重音、特殊元音、不发音字母、易错辅音才值得标。
4. **用例词绑定记忆**：例如 `cache` 绑定 /kæʃ/，`queue` 绑定 /kjuː/，`linux` 绑定 /ˈlɪnəks/。

### 1.2 D.J. / K.K. / IPA / CEPD

| 体系 | 全称 | 常见用途 | 速查结论 |
| --- | --- | --- | --- |
| **D.J.** | Daniel Jones 音标体系 | 英式发音，常见于英式词典传统标注 | 元音符号与美式差异较多；辅音基本相同 |
| **K.K.** | Kenyon & Knott 音标体系 | 美式发音传统标注 | 常用 `ɑr`、`ɚ`、`ɝ` 等表达美式 r 色彩 |
| **IPA** | International Phonetic Alphabet | 国际音标，用于标注各种语言 | 是大框架；各词典会有自己的实现细节 |
| **CEPD** | Cambridge English Pronouncing Dictionary | 剑桥英语发音词典（1000h 采用） | UK 用 D.J.；US 使用 IPA 风格并加入美式优化 |

### 1.3 Schwa /ə/（弱读元音 · 央元音）

**Schwa** /ʃwɑː/ —— 音标学术语（源自希伯来语 *šəwā*，指「无辅音的元音」）。中文常说 **弱读元音** 或 **央元音**；符号 **`/ə/`**。

| | |
|---|---|
| **是什么** | 英语里**出现频率最高**的元音；舌位居中、口型较小、发音轻而短 |
| **何时出现** | 非重读音节里，原元音常**弱读**成 /ə/；功能词（*a*, *the*, *of*, *to*…）在语流中几乎总是 schwa |
| **怎么读** | 不要读成中文「额」或重读的 /ʌ/；听感接近轻、短、含糊的「呃」，嘴唇不必刻意张大 |
| **与 /ʌ/ 区别** | /ʌ/ 在**重读**音节（*bug*, *run*）；/ə/ 在**非重读**（*support* 首音节、*system* 末音节）。美式里 /ʌ/ 有时也听感接近 /ə/（*encourage*） |
| **美式变体** | **`ɚ`** = 带 r 色彩的 schwa（*worker* 末音节）；**`ɝ`** = 带 r 的长元音（*worker* 首音节）。**非重读 /ə/ 不要一律卷舌成 /ɚ/** |

**工程师速记例词：**

| 词 | IPA | schwa 在哪 |
| --- | --- | --- |
| **system** | /ˈsɪstəm/ | 第二音节 `-tem` |
| **support** | /səˈpɔːrt/ | 第一音节 `su-` |
| **about** | /əˈbaʊt/ | 第一音节 `a-` |
| **database** | /ˈdeɪtəbeɪs/ | 中间 `-ta-` |
| **developer** | /dɪˈveləpər/ | `-lop-` 中的 `-lo-` |

深入：[[1000-hours/sounds-of-american-english/3.1.1-ə|1000h · 3.1.1 ə/ɚ/ɝ]] · [[learning-notes/pronunciation/syllable-division-ipa-based#62-词内重音|音节划分 · 词内重音]]

### 1.4 美式标注速查

| 现象 | 常见写法 | 例词 | 提醒 |
| --- | --- | --- | --- |
| 儿化 schwa（**弱读元音 + r**） | `ə` → `ɚ`；`ɜː` / `əː` → `ɝː` / `ɝ` | **worker** /ˈwɝːkɚ/ | 不要见 `ə` 就强行卷舌；看词典 |
| r 色彩双元音 | `ɪə` → `ɪr`；`eə` → `er`；`ʊə` → `ʊr` | **gear** /ɡɪr/ | 美式常用 `r` 收尾 |
| 短元音替换 | `ɒ` → `ɑː` / `ɑ` | **dog** /dɑːɡ/ | UK /ɒ/ 在 US 多接近 /ɑ/ |
| 词尾 happy vowel | 词尾 `ɪ` → `i` | **city** /ˈsɪt̬i/ | `i` 不是长元音 /iː/ |
| 弹舌 t | `t` → `t̬` | **city**, **meeting** | 美式高频，听感接近 /d/ |
| 非重读弱化 | `ɪ` / 其它元音 → `ə`（**schwa 弱读**） | **support** /səˈpɔːrt/ | 非重读音节常向 schwa /ə/ 靠拢（见 §1.3） |

---

## 2. 元音 Vowels —— 先抓共鸣位置和长度

元音的关键不是嘴形，而是**口腔内气流共鸣位置**。中文母语者常把英文元音读得太靠前、太等长；练习时要特别注意长元音、双元音和 /æ/ 的时长。

### 2.1 学习用元音地图

> 这是学习用简化表，不是完整音系论文。完整符号表见 [[1000-hours/sounds-of-american-english/1.1-phonemes|1000h · 1.1 音素与音标]]。

| 组别 | 音标 | 技术 / 职场例词 | 阿泽要点 |
| --- | --- | --- | --- |
| 短 / 核心元音 | `ʌ e ə ɪ ʊ ɒ/ɑ` | **bug**, **tech**, **system**, **linux**, **pull**, **log** | 短但不能糊；`ə` = schwa，非重读常弱化为它 |
| 长 / 对应元音 | `ɑː æ ɜː/ɝ iː uː ɔː` | **database**, **stack**, **server**, **feature**, **queue**, **core** | 不只是短音拉长，很多位置也不同 |
| 双元音 | `aɪ eɪ ɔɪ aʊ əʊ/oʊ eə ɪə ʊə` | **pipeline**, **cache**, **deploy**, **cloud**, **code**, **share**, **gear**, **pure** | 从第一个音滑向第二个音，要够长、够饱满 |

### 2.2 中文母语者优先级

| 优先级 | 音 / 对比 | 常见问题 | 练法 |
| --- | --- | --- | --- |
| 1 | `/æ/` | 读太短，接近 /e/；*apple* 变成 epple | 把 *stack*, *cache*, *application* 的 /æ/ 拉长一点 |
| 2 | `/ɪ/` vs `/iː/` | 把 /ɪ/ 读成长「衣」；*linux* 读成 /ˈlaɪnʌks/ | 对比 **ship/sheep**, **bit/beat**, **linux/feature** |
| 3 | `/ʌ/` ~ `/ə/` | 用中文 a 代替；口腔共鸣太靠前 | 练 **bug**, **run**, **support**, **encourage** |
| 4 | 双元音 | /aɪ/ 读成中文「爱」；/oʊ/ 不滑动 | 练 **API**, **pipeline**, **deploy**, **rollback** |
| 5 | 元音等长 | 每个音节一样长，导致整体过快 | 慢读重音节：**de-ploy**, **re-view**, **da-ta-base** |

### 2.3 重读与弱读

| 状态 | 元音变化 | 例词 |
| --- | --- | --- |
| **重读音节** | 长元音更长，双元音更饱满，短元音也相对更清楚 | **database**, **review**, **deploy** |
| **非重读音节** | 元音常弱化为 **schwa** /ə/ 或 /ɪ/；音高更低 | **system** /ˈsɪstəm/, **support** /səˈpɔːrt/ |
| **句内强读** | 内容词被突出，元音时长和音高更明显 | *We need a **rollback**.* |
| **句内弱读** | 功能词弱化，语流更自然 | *for a*, *to the*, *of the* |

---

## 3. 辅音 Consonants —— 先抓舌尖起始位置

辅音常带来口音，但最影响理解的往往仍是元音。对中文母语者来说，少数辅音要重点练：`t d s z` 的舌尖起始位置、`θ ð`、`v`、词尾 `l`、美式 `r`、以及 `t` 在语流中的变化。

### 3.1 清浊配对

| 清辅音 | 浊辅音 | 技术词汇示例 | 中文 |
| --- | --- | --- | --- |
| /p/ | /b/ | **pull** / **build** | 拉取 / 构建 |
| /t/ | /d/ | **test** / **debug** | 测试 / 调试 |
| /k/ | /ɡ/ | **cache** / **grep** | 缓存 / 搜索 |
| /f/ | /v/ | **file** / **variable** | 文件 / 变量 |
| /s/ | /z/ | **sync** / **zip** | 同步 / 压缩 |
| /θ/ | /ð/ | **path** / **the** | 路径 / 这个 |
| /ʃ/ | /ʒ/ | **shell** / **version** | 壳 / 版本 |
| /tʃ/ | /dʒ/ | **feature** / **merge** | 功能 / 合并 |

### 3.2 中文母语者辅音抓手

| 音 | 关键动作 | 工程 / 日常例词 | 提醒 |
| --- | --- | --- | --- |
| `/t d s z/` | 舌尖起点在上牙龈附近，不是贴牙齿 | **student**, **test**, **debug**, **sync** | 先练 *student/students* |
| `/θ ð/` | 舌尖贴上齿内侧即可，不必夸张伸舌 | **path**, **through**, **the**, **this** | 勿全替换为 /s/ /z/ /t/ /d/ |
| `/v/` | 上齿轻触下唇，声带振动 | **variable**, **version**, **review** | 勿读成 /w/ 或 /b/ |
| `/ʒ/` | 浊摩擦音，类似 *vision* 中的 s | **version**, **casual** | 频率低，先能听出即可 |
| 词尾 `/l/` | 舌尖要完成上抬动作 | **pull**, **local**, **rollback** | 勿读成 /oʊ/ 或吞掉 |
| 美式 `/r/` | 注意 r 色彩，不等于中文儿化 | **server**, **repository**, **parser** | 以词典音频为准 |

### 3.3 `t` / `d` 在语流里的四个高频变化

| 现象 | 条件 | 例子 | 速查说明 |
| --- | --- | --- | --- |
| **弹舌 t** /t̬/ | /t/ 在两个元音之间，常见于美式 | **city**, **meeting**, *set it up* | 听感接近短促 /d/ |
| **失爆 / 省音** | /t d/ 后接辅音 | *might be*, *finished reading* | 不是消失，舌尖动作和停顿仍在 |
| **同化** | /t d/ + /j/ | *don't you* → /doʊntʃu/；*would you* → /wʊdʒu/ | 舌尖位置对了会自然发生 |
| **/s/ 后不送气** | `sp st sk` 等组合 | **study**, **school**, **experience** | 听感像 /sd/ /sg/ /sb/，但不是硬读 b/d/g |

---

## 4. 工程师高频词发音

更多易错词见 [[learning-notes/pronunciation/vocabulary-tricky-pronunciation-149|易读错词汇 149]]；这里保留技术场景里最常查的一批。

### 4.1 技术术语 Tech Terms

| 词汇 | IPA | 常见误读 | 备注 |
| --- | --- | --- | --- |
| **repository** | /rɪˈpɑːzətɔːri/ | repo*z*itory ❌ | Git 仓库；重音在第二音节 |
| **queue** | /kjuː/ | *que*ue ❌ | 队列；一个音节，和字母 Q 同音 |
| **cache** | /kæʃ/ | /kætʃ/ 或 /ˈkæʃeɪ/ ❌ | 缓存；`ch` 发 /ʃ/ |
| **schema** | /ˈskiːmə/ | /ˈʃiːmə/ ❌ | 模式；`sch` 发 /sk/ |
| **daemon** | /ˈdiːmən/ | /ˈdeɪmən/ ❌ | 守护进程；`ae` 发 /iː/ |
| **kubernetes** | /ˌkuːbərˈnetiz/ | 字母逐个念 ❌ | K8s；重音在 **net** |
| **nginx** | /ˌendʒɪnˈeks/ | n-g-i-n-x ❌ | 常读 “engine X” |
| **linux** | /ˈlɪnəks/ | /ˈlaɪnʌks/ ❌ | `i` 是短 /ɪ/ |
| **varchar** | /ˈvɑːrkær/ | /vɑːrˈtʃɑːr/ ❌ | 可变字符；`char` 不读 /tʃɑːr/ |
| **sudo** | /ˈsuːduː/ | /ˈsʌdoʊ/ ❌ | 超级用户执行；`su` 发 /suː/ |

### 4.2 职场沟通 Workplace Communication

| 场景 | 表达 | IPA | 中文 |
| --- | --- | --- | --- |
| 代码评审 | **LGTM** | /ˌel dʒiː tiː ˈem/ | Looks Good To Me |
| 每日站会 | **stand-up** | /ˈstænd ʌp/ | 站立会议 |
| 需求评审 | **PRD review** | /ˌpiː ɑːr ˈdiː rɪˌvjuː/ | 产品需求文档评审 |
| 技术方案 | **RFC** | /ˌɑːr ef ˈsiː/ | Request For Comments |
| 紧急修复 | **hotfix** | /ˈhɑːtfɪks/ | 热修复 |
| 回滚操作 | **rollback** | /ˈroʊlbæk/ | 回滚 |

### 4.3 重音与弱读常见模式

完整后缀规律（含 **-ic**、复合词、衍生词）→ [[learning-notes/pronunciation/syllable-division-ipa-based#64-常见重音位置规则|音节划分 · §6.4]]。

| 模式 | 示例 | IPA | 提醒 |
| --- | --- | --- | --- |
| 2 音节动词重音在后 | **deploy**, **record**（v.） | /dɪˈplɔɪ/, /rɪˈkɔːrd/ | de-**ploy** |
| 2 音节名词重音在前 | **server**, **record**（n.） | /ˈsɜːrvər/, /ˈrekɚd/ | **ser**-ver |
| **-ic** | **ceramic**, **specific** | /səˈræmɪk/, /spəˈsɪfɪk/ | 重音在 -ic **前**；*Arabic* 例外 |
| `-er`, `-or` | **developer**, **compiler** | /dɪˈveləpər/, /kəmˈpaɪlər/ | 看词根主重音 |
| `-tion`, `-sion` | **application**, **version** | /ˌæplɪˈkeɪʃn/, /ˈvɜːrʒn/ | 后缀音节弱读 |
| `-ity`, `-ology` | **integrity**, **technology** | /ɪnˈteɡrəti/, /tekˈnɒlədʒi/ | |
| 非重读弱化 | **support**, **database** | /səˈpɔːrt/, /ˈdeɪtəbɑːs/ | 非重读元音 → schwa /ə/ |

---

## 5. 深入学习入口

→ 系统学习路线见 [[learning-notes/pronunciation/english-phonetics-textbook|英文语音完整教程]]。

### 5.1 本仓库发音笔记

- [[learning-notes/pronunciation/syllable-division-ipa-based|音节划分与重音 · IPA]] —— 用 IPA 切音节、标重音。
- [[learning-notes/pronunciation/vocabulary-tricky-pronunciation-149|易读错词汇 149]] —— 技术词、原书 ch.3 示例词、国人易错模式。
- [[learning-notes/pronunciation/world-cinema-quick-notes|世界电影随记]] —— 短文跟读、连读、重音练习。
- [[learning-notes/pronunciation/phonetics-input-guide|音标输入指南]] —— Markdown / Obsidian 里输入 IPA。

### 5.2 1000h 语音教程

- [[1000-hours/sounds-of-american-english/0-intro|语音塑造]] —— 为什么要熟悉音标。
- [[1000-hours/sounds-of-american-english/1.1-phonemes|音素与音标]] —— CEPD 体系、英美音素表。
- [[1000-hours/sounds-of-american-english/3-details|音素详解]] —— 英美音素数量与练习提醒。

### 5.3 原书与新版草稿

- [[book/chapter3|《人人都能用英语》第三章 · 语音]] —— 音标学习策略、语速、停顿、浊化、失爆、同化。
- [[new-edition-drafts/英文语音简明教程|英文语音简明教程]] —— D.J. / K.K. / IPA、元音共鸣位置、辅音舌尖位置。
- [[new-edition-drafts/第一轮讲解/15-元音辅音|元音辅音]] —— 为什么先抓元音，再处理少数关键辅音。

---

## 6. 阿泽使用清单

- 新词先听真人音频，再看 IPA；不要只按拼写猜。
- 先固定一个主词典体系；遇到 `ɚ`、`ɝ`、`t̬`、`i` 等差异时知道它们是什么即可。
- 技术词优先记录三项：**重音位置**、**特殊元音**、**不发音 / 非常规拼写**。
- 跟读时先慢下来：长元音够长，双元音够饱满，/æ/ 不要读太短。
- 辅音重点只抓少数：`t d s z`、`θ ð`、`v`、词尾 `l`、美式 `r`。

---

*Last updated: 2026-06-14*
