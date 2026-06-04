---
tags:
  - personal-english-book
  - english-learning
  - peb/work
aliases:
  - 研发流程表达
  - R&D workflow English
---
# 研发流程 · 工作英语

**索引：** [[learning-notes/personal-english-book/README|个人英文材料书索引]]
**相关：** [[learning-notes/personal-english-book/work/work-english-instant-messaging|工作 IM 沟通]] · [[learning-notes/personal-english-book/work/高性能高可用|高性能 · 高可用]] · [[learning-notes/personal-english-book/work/专业术语|工作专业术语]] · [[learning-notes/personal-english-book/work/financial-system-issue-analysis|金融系统问题梳理]]

> **分工说明：** 版本周期、延期提醒、冒烟等通用 IM 句式见 [[learning-notes/personal-english-book/work/work-english-instant-messaging#研发流程周期|工作 IM · 研发流程周期]]；本页侧重**立项、演示日检查清单、开发同步、缺陷与客户沟通、发布评审**。

---

## 本页在做什么

整理研发协作中的**固定流程话术**与**演示 / 发布检查项**中英对照，便于会前通知、演示日分工、发布件评审。下文顺序：**语块 → 会议与立项 → 演示清单 → 开发沟通 → 缺陷与客户 → 发布 → 预留扩充**。

---

## 重点可复用语块（Reusable chunks）

| 语块 | 英文示例 | 用途 |
| --- | --- | --- |
| 版本启动会 | *version kickoff meeting* / *release kickoff* | 会前通知 |
| 提前评估版本计划 | *review the release plan in advance* | 会前要求 |
| 立项 | *project kickoff* / *initiate the project* / *set up the release* | 版本启动 |
| 送测时间 | *test submission date* / *handoff to QA* | 排期 |
| 发布时间 | *release date* / *go-live date* | 排期 |
| 拉会沟通 | *schedule a separate sync* / *set up a meeting* | 协调 |
| 工作量 / 工时 | *effort estimate* / *workload* | 排期表 |
| 挡板环境 | *stub environment* / *simulator / mock environment* | 演示环境 |
| 演示环境 | *demo environment* | 环境 |
| 豁免前后对比 | *before vs after exemption* | 验证 |
| 主备切换 | *primary–standby failover* | HA 演练 |
| rejoin | *rejoin* | HA 演练 |
| RPO = 0 | *RPO = 0*（可脚注：*zero data loss*） | HA 指标 |
| 强撤 | *forced cancel* / *force cancel* | 交易监控 |
| 指定成交 | *designated trade / next designated fill* | 流程验证 |
| 影响域 | *impact scope* | 发布评审 |
| 发布件评审 | *release package review* | 发布 |
| 评审不通过 | *review failed* / *not approved* | 结论 |
| 规划缺陷 | *defects in scope for this release* | 发布说明 |
| 初稿 | *first draft* | 文档 / 方案 |
| 梳理开发方案 | *walk through the implementation plan* | 开发同步 |

---

## A. 版本会议与排期（IM）

| 中文 | 英文（改进稿） |
| --- | --- |
| 明天上午版本启动会，请各位提前评估版本计划。 | We have a **version kickoff** tomorrow morning. Please **review the release plan** in advance. |
| 我下午才有时间更新，上午要准备客户演示事项。 | I can **update this afternoon** only—I’m **prepping the client demo** this morning. |
| 工作量是直接写到这个表格里吗？ | Should I **enter the effort estimates directly** in this spreadsheet? |

---

## B. 立项（Project kickoff）

| 中文 | 英文（改进稿） |
| --- | --- |
| v132 这个版本要立项一下。 | We need to **kick off project setup for v132**. |
| 要今天立项吗？送测及发布时间有预期吗？需要额外拉会沟通吗？ | Do we need to **kick off today**? Any expected **test handoff** and **release dates**? Should we **schedule a separate sync**? |

**可合并为一段（邮件 / 群公告）**

> We need to kick off **v132**. Can we confirm today whether we start setup now, and what the expected **QA handoff** and **release** dates are? Let me know if we need a separate meeting.

---

## C. 研发流程检查清单（演示日）

*演示日分工模板；负责人用 `xx` 占位，按场次替换。*

### C.1 环境准备 · Environment setup

| 中文 | 英文 |
| --- | --- |
| 演示环境：34 | **Demo environment:** 34 |
| 挡板环境配置：xx | **Stub / mock environment config:** xx |

### C.2 现货调度 · Spot scheduling（技术）

| 中文 | 英文 |
| --- | --- |
| 上午验证（前端 + Java），实时指令正常。 | **Morning check** (frontend + Java): **real-time instructions** work as expected. |
| 准备好场景，验证豁免前后对比。 | Prepare **test scenarios** and verify **before vs after exemption**. |

### C.3 交易簿记 · Transaction bookkeeping（技术）

| 中文 | 英文 |
| --- | --- |
| 基础功能演示：增 / 删 / 改 / 查，当前无明显问题。 | **CRUD demo**: create / read / update / delete—**no obvious issues** so far. |

### C.4 持仓负数调整 · Position negative adjustment（技术）

| 中文 | 英文 |
| --- | --- |
| 持仓调整为负数（4 个场景），上午重点关注后台持仓是否正常；前端：xx。 | Run **four scenarios** with **negative positions**. This morning, focus on whether **backend positions** stay correct; frontend owner: **xx**. |

**检查项 Check items**

| 项 | 英文 |
| --- | --- |
| a. 对冲账户持仓 | Hedging account positions |
| b. 柜台账户持仓 | Counter account positions |
| c. 已卖空明细 | Short-sale details |
| d. 对冲账户受限股 | Restricted shares in the hedging account |

### C.5 IME 主备切换 · IME primary / standby（技术）

| 中文 | 英文 |
| --- | --- |
| IME 主备：xx | IME primary / standby owner: **xx** |

**演练项 Drill items**

| 项 | 中文要点 | 英文 |
| --- | --- | --- |
| a | 主挂 → 自动切备，备升主，下单正常 | When the **primary fails**, verify **auto-failover to standby**, **standby promotion**, and **order placement** still works. |
| b | 主备都挂 → 拉起后续 IME | When **both** are down, **bring up the next IME instance** and verify recovery. |
| c | 仅留实例 2；实例 1 **rejoin**；再杀实例 2 | Keep **only instance 2**; **rejoin** original instance 1; then **stop instance 2** and verify primary behavior. |
| d | 预留补充 | *Reserved — additional drill items.* |
| e | **RPO = 0** 故障恢复 / 热切（带流量必保；演示可无流量） | **Fault recovery / hot switch** with **RPO = 0** (required under **live traffic**; demo may run **without traffic**). |

| 中文 | 英文 |
| --- | --- |
| 额外验证：启停、rejoin 流程是否正常。 | **Extra check:** verify **start/stop** and **rejoin** flows. |

*更多 HA 用语见 [[learning-notes/personal-english-book/work/高性能高可用|高性能 · 高可用]]。*

### C.6 用户信息透传 · User info pass-through（技术）

| 中文 | 英文 |
| --- | --- |
| `userinfo` 是否支持 pass-through。 | Confirm whether **`userinfo` supports pass-through**. |

### C.7 异常监控与强制撤单 · Monitoring & forced cancellation（技术）

| 项 | 中文 | 英文 |
| --- | --- | --- |
| a | 补充完整 ut 并验证 | Complete **`ut` coverage** and verify. |
| b | 上午验证实时指令 | Verify **real-time instructions** in the morning. |
| c | 强撤标记字段显示 | Verify the **forced-cancel marker** displays correctly. |
| d | 「下一笔指定成交」流程 | Verify the **next designated fill** flow. |

| 中文 | 英文 |
| --- | --- |
| 我搞个初稿出来。 | I’ll **put together a first draft**. |

---

## D. 开发讨论（IM）

| 中文 | 英文（改进稿） |
| --- | --- |
| 暂时没有其他问题，我今天把具体怎么开发梳理了一下，在开始写代码了。 | **No open questions for now.** I **walked through the implementation plan** today and **started coding**. |

---

## E. Bug 修复与客户沟通

| 中文 | 英文（改进稿） |
| --- | --- |
| 有变动可以再沟通，但我理解 v132 不修 v200 也要修的吧，是不是差别不大？ | We can **sync again if things change**, but my read is: even if we **don’t fix it in v132**, we still need it in **v200**—**isn’t the gap small**? |
| 这里后面三个哪个是不好修的？ | **Which of the last three** is the **hardest to fix**? |
| 你判断一下吧，还有哪个 v132 放不进来的我们再找客户沟通即可。 | **Please call it.** Anything we **can’t fit into v132**, we can **align with the client** again. |
| 好的，那这个可以再找客户聊一下。 | OK—let’s **take this back to the client**. |

---

## F. 发布与发布件评审

| 中文 | 英文（改进稿） |
| --- | --- |
| 这几个缺陷的影响域补充一下，今天要做发布件评审。 | Please **fill in the impact scope** for these defects—we have a **release package review** today. |
| 我这边刚刚更新了一版，规划缺陷都包含了。 | I **just pushed an update**; it **includes all defects planned for this release**. |
| 结论就是不通过。 | **Conclusion: not approved** / **The review did not pass.** |

---

## G. 词汇速查（本篇已收录）

| 中文 | 英文 |
| --- | --- |
| 版本启动会 | version kickoff (meeting) |
| 立项 | project kickoff / initiate the project |
| 送测 | submit for testing / handoff to QA |
| 挡板环境 | stub / mock environment |
| 实时指令 | real-time instructions |
| 主备切换 | primary–standby failover |
| 发布件 | release package |
| 不通过 | not approved / did not pass (review) |

---

## H. 待扩充 · 需求与设计（预留）

| 主题 | 状态 |
| --- | --- |
| 需求评审、内部宣讲 | 可链 [[learning-notes/personal-english-book/work/work-english-instant-messaging|工作 IM]] |
| 工时评估、任务拆分 | 待补充 |
| 技术方案评审 | 待补充 |

---

## I. 待扩充 · 测试与质量（预留）

| 主题 | 状态 |
| --- | --- |
| 提测、冒烟、回归 checklist 英文 | 待补充 |
| 缺陷等级、复现、影响域模板 | 可链 [[learning-notes/personal-english-book/work/专业术语|工作专业术语]] |
| 演示日以外的 HA / 压测条目 | 可链 [[learning-notes/personal-english-book/work/高性能高可用|高性能高可用]] |

---

## J. 待扩充 · 发布与上线（预留）

| 主题 | 状态 |
| --- | --- |
| 发布件评审通过 / 有条件通过话术 | 待补充 |
| 上线窗口、回滚、变更公告 | 待补充 |
| 客户沟通邮件模板 | 待补充 |

---

## 笔记与修订

| 日期 | 说明 |
| --- | --- |
| — | 重组：演示日清单表化、与 IM 专页分工；英文改进稿；预留 H–J；链 HA / 术语 / 金融梳理。 |
