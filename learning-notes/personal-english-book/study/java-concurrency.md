---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
aliases:
  - Java Concurrency
  - 并发编程
  - Java 并发
---

# Java Concurrency — Java 并发编程

Concurrency means multiple threads make progress **at the same time** — sharing CPU cores and, dangerously, shared memory. This note covers the JUC toolkit: locks, synchronizers, concurrent collections, and executors.

并发指多个线程**同时**推进——共享 CPU 核心，也危险地共享内存。本文涵盖 JUC 工具箱：锁、同步器、并发容器与执行器。

**Demo bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

**Demo repo:** https://github.com/zhangze2/awesome-demo/tree/master/concurrency · **Local sibling:** `../awesome-java-demo/concurrency/`

---

## Overview — 概述

### Why concurrency is hard — 并发为何难

Threads interleave unpredictably. Without coordination you get **race conditions** (wrong results), **visibility failures** (stale reads), and **deadlock** (circular waiting).

线程交错执行不可预测。缺少协调就会出现**竞态条件**（结果错误）、**可见性失效**（读到旧值）与**死锁**（循环等待）。

### The JUC Toolkit — JUC 工具箱

`java.util.concurrent` families: **locks / atomics / synchronizers / concurrent collections / executors**.

`java.util.concurrent` 家族：**锁 / 原子类 / 同步器 / 并发容器 / 执行器**。

### Key Principles — 核心原则

1. **Prefer immutability** — no shared mutable state, no locks — 优先不可变：无共享可变状态则无需锁
2. **Confine state** — thread-local or single-owner — 封闭状态：线程本地或单一持有者
3. **Use library tools** — don't hand-roll thread safety — 用库工具，别手写线程安全
4. **Unlock in finally** — always release locks — 在 finally 中释放锁

---

## Core Concepts — 核心概念

### 1. synchronized & volatile — 内置锁与可见性

`synchronized` gives **mutual exclusion** plus a **happens-before** edge (changes before unlock are visible after the next lock). `volatile` guarantees **visibility** but **not atomicity**.

`synchronized` 提供**互斥**并建立 **happens-before** 关系（解锁前的修改对下一次加锁可见）。`volatile` 保证**可见性**但不保证**原子性**。

```java
private int count;
public synchronized void increment() { count++; } // atomic + visible — 原子且可见

private volatile boolean running; // visibility only — 仅保证可见性
```

**Rule of thumb — 经验法则**: `volatile` for flags; `synchronized`/atomics for compound actions like `count++` — 标志位用 `volatile`；`count++` 这类复合动作用 `synchronized` 或原子类。

### 2. ReentrantLock — 可重入锁

A **reentrant** mutual exclusion lock with the same behavior as the implicit monitor lock — but with extras: `tryLock`, timed waits, fairness options.

**可重入**互斥锁，行为与内置监视器锁相同——但多了 `tryLock`、超时等待、公平性选项。

```java
lock.lock();
try {
    // critical section — 临界区
} finally {
    lock.unlock(); // Always unlock in finally — 永远在 finally 解锁
}
```

`ReadWriteLock` lets many **readers** proceed together while a **writer** excludes everyone — great for read-heavy caches.

`ReadWriteLock` 允许多**读**并发而**写**独占——适合读多写少的缓存。

### 3. Synchronizers — 同步器

| Tool | One-liner | 一句话 |
|------|-----------|--------|
| **CountDownLatch** | One-shot: wait until N events complete | 一次性：等待 N 个事件完成 |
| **CyclicBarrier** | Reusable: threads meet at a barrier point | 可复用：线程在屏障点会合 |
| **Semaphore** | Counting permits — limit concurrency | 计数许可——限制并发数 |

```java
CountDownLatch latch = new CountDownLatch(3);
// workers call latch.countDown()
latch.await(); // main thread waits for all — 主线程等待全部完成
```

### 4. Concurrent Collections — 并发容器

**ConcurrentHashMap** partitions the map so most operations need no global lock. **BlockingQueue** makes producer–consumer trivial: `put` blocks when full, `take` blocks when empty.

**ConcurrentHashMap** 对映射分区，多数操作无需全局锁。**BlockingQueue** 让生产者–消费者模式变简单：满时 `put` 阻塞，空时 `take` 阻塞。

### 5. Executors & Thread Pools — 执行器与线程池

Don't create raw threads; submit tasks to a **ThreadPoolExecutor** with explicit queue, pool sizes, and rejection policy.

不要裸建线程；把任务提交给显式配置队列、池大小与拒绝策略的 **ThreadPoolExecutor**。

```java
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    4, 8, 60, TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(100),
    new ThreadPoolExecutor.CallerRunsPolicy()); // back-pressure — 背压
```

### 6. CompletableFuture — 异步编排

Compose async pipelines without blocking: `supplyAsync` → `thenApply` → `thenCombine`. **Deep dive:** [[learning-notes/personal-english-book/study/completablefuture-java-guide|CompletableFuture 指南]].

不阻塞地编排异步流水线：`supplyAsync` → `thenApply` → `thenCombine`。**深入阅读：** [[learning-notes/personal-english-book/study/completablefuture-java-guide|CompletableFuture 指南]]。

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Concurrency** | /kənˈkɜːrənsi/ | 并发 | Multiple tasks making progress together |
| **Thread** | /θred/ | 线程 | The smallest unit of scheduled execution |
| **Race condition** | /reɪs kənˈdɪʃən/ | 竞态条件 | Result depends on unpredictable interleaving |
| **Visibility** | /ˌvɪzəˈbɪləti/ | 可见性 | Whether one thread sees another's writes |
| **Atomicity** | /ˌætəˈmɪsəti/ | 原子性 | An operation that happens entirely or not at all |
| **Mutual exclusion** | /ˈmjuːtʃuəl ɪkˈskluːʒən/ | 互斥 | Only one thread in the critical section |
| **Reentrant** | /riːˈɛntrənt/ | 可重入的 | A lock the same thread can acquire repeatedly |
| **Deadlock** | /ˈdedlɑːk/ | 死锁 | Threads blocked forever, each holding what another needs |
| **Synchronizer** | /ˈsɪŋkrənaɪzər/ | 同步器 | A coordination aid like latch, barrier, semaphore |
| **Latch** | /lætʃ/ | 闩锁 | One-shot gate released when a count reaches zero |
| **Barrier** | /ˈbæriər/ | 屏障 | Point where threads wait until all arrive |
| **Semaphore** | /ˈseməfɔːr/ | 信号量 | Counting permits limiting concurrent access |
| **Executor** | /ɪɡˈzekjətər/ | 执行器 | A service running submitted tasks on pooled threads |
| **Happens-before** | /ˈhæpənz bɪˈfɔːr/ | 先于发生关系 | Memory ordering guarantee between actions |
| **Critical section** | /ˈkrɪtɪkəl ˈsekʃən/ | 临界区 | Code that must not run concurrently |
| **Back-pressure** | /bæk ˈpreʃər/ | 背压 | Slowing producers when consumers fall behind |

---

## Common Interview Questions — 常见面试问题

### Q: synchronized vs ReentrantLock — which to choose?

**A**: `synchronized` is simpler and auto-releases. Choose `ReentrantLock` when you need `tryLock` (avoid deadlock), timed waits, interruptible acquisition, or fairness. Always `unlock` in `finally`.

`synchronized` 更简单且自动释放。需要 `tryLock`（避免死锁）、超时等待、可中断获取或公平性时选 `ReentrantLock`，且永远在 `finally` 中解锁。

### Q: Why is `count++` not thread-safe even with volatile?

**A**: `count++` is three steps — read, add, write. `volatile` makes each step visible but the **compound action** is not atomic; two threads can both read the same value and both write +1.

`count++` 是读、加、写三步。`volatile` 让每步可见，但**复合动作**不是原子的；两个线程可能读到同一个值，各自只加一。

### Q: CountDownLatch vs CyclicBarrier?

**A**: A **latch** is one-shot: one or more threads wait until N events complete. A **barrier** is reusable: a fixed group of threads repeatedly meet at the same point.

**闩锁**一次性：线程等待 N 个事件完成；**屏障**可复用：固定一组线程反复在同一点会合。

### Q: Why prefer ThreadPoolExecutor over new Thread()?

**A**: Pools **reuse** threads (creation is expensive), **bound** concurrency (queues + max size prevent resource exhaustion), and add **back-pressure** via rejection policies.

线程池**复用**线程（创建昂贵）、**约束**并发（队列 + 最大池防资源耗尽），并通过拒绝策略提供**背压**。

---

## Further Reading — 延伸阅读

- [java.util.concurrent package](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/package-summary.html)
- *Java Concurrency in Practice* (Brian Goetz)
- [Baeldung: Java Concurrency](https://www.baeldung.com/java-concurrency)
- Related: [[learning-notes/personal-english-book/study/completablefuture-java-guide|CompletableFuture 指南]] · [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]]
- Source README (demo): https://github.com/zhangze2/awesome-demo/blob/master/concurrency/README.en.md · Metaphor guide: [JUC_GUIDE](https://github.com/zhangze2/awesome-demo/blob/master/concurrency/JUC_GUIDE.md)

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (demo repo root) |
|-------|------------|----------------------|
| JUC menu (12 tools) | `concurrency.juc.JUCDemoRunner` | `mvn -pl concurrency -q compile exec:java` · `java -cp concurrency/target/classes concurrency.ConcurrencyDemoRunner juc` |
| ReentrantLock | `concurrency.juc.lock.ReentrantLockExample` | `java -cp concurrency/target/classes concurrency.juc.lock.ReentrantLockExample` |
| CountDownLatch | `concurrency.juc.sync.CountDownLatchExample` | `java -cp concurrency/target/classes concurrency.juc.sync.CountDownLatchExample` |
| Semaphore | `concurrency.juc.sync.SemaphoreExample` | `java -cp concurrency/target/classes concurrency.juc.sync.SemaphoreExample` |
| ConcurrentHashMap | `concurrency.juc.collection.ConcurrentHashMapExample` | `java -cp concurrency/target/classes concurrency.juc.collection.ConcurrentHashMapExample` |
| Thread pool | `concurrency.juc.executor.ThreadPoolExecutorExample` | `java -cp concurrency/target/classes concurrency.juc.executor.ThreadPoolExecutorExample` |
| CompletableFuture | `concurrency.juc.executor.CompletableFutureExample` | see [[learning-notes/personal-english-book/study/completablefuture-java-guide|CompletableFuture 指南]] |

**English README (demo):** https://github.com/zhangze2/awesome-demo/blob/master/concurrency/README.en.md

**Tags**: `技术`, `Java`, `并发`, `JUC`, `多线程`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Volatile gives visibility, not atomicity.** — volatile 保证可见性，不保证原子性。
- **Always unlock in a finally block.** — 永远在 finally 块里解锁。
- **A latch waits for N events to finish.** — 闩锁等待 N 个事件完成。
- **ConcurrentHashMap avoids a global lock.** — ConcurrentHashMap 避免全局锁。
- **Pools reuse threads and add back-pressure.** — 线程池复用线程并提供背压。

### B. 一段串联（连续口语）

**Volatile gives visibility, not atomicity. Always unlock in a finally block. A latch waits for N events to finish. ConcurrentHashMap avoids a global lock. Pools reuse threads and add back-pressure.**

**简中：** volatile 保证可见性，不保证原子性。永远在 finally 块里解锁。闩锁等待 N 个事件完成。ConcurrentHashMap 避免全局锁。线程池复用线程并提供背压。

### C. 一分钟复盘（5 句）

1. **Volatile gives visibility, not atomicity.** — volatile 保证可见性，不保证原子性。
2. **Always unlock in a finally block.** — 永远在 finally 块里解锁。
3. **A latch waits for N events to finish.** — 闩锁等待 N 个事件完成。
4. **ConcurrentHashMap avoids a global lock.** — ConcurrentHashMap 避免全局锁。
5. **Pools reuse threads and add back-pressure.** — 线程池复用线程并提供背压。
