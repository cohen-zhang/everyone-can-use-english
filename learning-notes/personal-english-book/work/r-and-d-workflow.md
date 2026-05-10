---
tags:
  - personal-english-book
  - english-learning
  - peb/work
aliases:
  - 研发流程表达
---
# 研发流程表达

**索引：** [[learning-notes/personal-english-book/README|个人英文材料书索引]]

## 研发流程检查清单（演示日）

### 1) 环境准备 Environment Setup

- **演示环境：34** — **Demo environment: 34**
- **挡板环境配置：xx** — **Baffle/stub environment config: xx**

### 2) 现货调度 Spot Scheduling（技术）

- 上午验证（前端 + Java），实时指令正常。  
Morning verification (Frontend + Java), real-time instructions work normally.
- 准备好场景，验证豁免前后对比。  
Prepare test scenarios and verify the comparison before and after exemption.

### 3) 交易簿记 Transaction Bookkeeping（技术）

- 基础功能演示：增 / 删 / 改 / 查，当前无明显问题。  
Demo basic CRUD functions; no obvious issues so far.

### 4) 持仓负数调整 Position Negative Adjustment（技术）

- 持仓调整为负数（4个场景），上午重点关注后台持仓是否正常；前端：`xx`。  
Adjust positions to negative values (4 scenarios); focus on whether backend positions stay correct in the morning; frontend owner: `xx`.
- 检查项 Check items:
  - `a.` 对冲账户持仓 — Hedging account positions
  - `b.` 柜台账户持仓 — Counter account positions
  - `c.` 已卖空明细 — Short-sale details
  - `d.` 对冲账户受限股 — Restricted shares in hedging account

### 5) IME 主备切换 IME Primary/Standby（技术）

- IME 主备：`xx`。  
IME primary/standby: `xx`.
- 演练项 Drill items:
  - `a.` 主挂掉后自动切备，观察备是否升主，并验证下单正常。  
  When primary fails, auto-switch to standby; verify standby promotion and order placement.
  - `b.` 主备都挂掉后，拉起后续 IME，观察是否正常工作。  
  When both are down, bring up the next IME instance and verify recovery.
  - `c.` 仅保留实例 2；对原实例 1 执行 **rejoin**；再杀掉实例 2，观察主是否正常。  
  Keep only instance 2; **rejoin** original instance 1; then stop instance 2 and verify primary behavior.
  - `d.` 预留补充项。  
  Reserved for additional drill items.
  - `e.` **RPO = 0** 的故障恢复 / 热切（带流量时必须保证 **RPO = 0**；演示可不带流量）。  
  Fault recovery/hot switch with **RPO = 0** (must hold under live traffic; demo can run without traffic).
- 额外验证：启停、**rejoin** 流程是否正常。  
Extra check: verify start/stop and **rejoin** flow.

### 6) 用户信息透传 User Info Pass-through（技术）

- `userinfo` 是否支持 **pass-through**。  
Verify whether `userinfo` supports **pass-through**.

### 7) 异常监控与强制撤单 Monitoring & Forced Cancellation（技术）

- `a.` 补充完整 `ut` 并验证。  
Complete `ut` coverage and verify.
- `b.` 上午验证实时指令。  
Verify real-time instructions in the morning.
- `c.` 观察强撤标记字段是否正常显示。  
Verify forced-cancellation marker field displays correctly.
- `d.` 验证“下一笔指定成交”流程。  
Verify the "next designated transaction" flow.
  我搞个初稿出来
   I'll come up with a first draft.
