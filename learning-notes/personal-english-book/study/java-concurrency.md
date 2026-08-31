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
- Related: [[learning-notes/personal-english-book/study/completablefuture-java-guide|CompletableFuture 指南]] · [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/java-keywords|Java 关键字]]（`synchronized` / `volatile`） · [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]] · [[learning-notes/personal-english-book/study/java-joke-Jeff-Dean|Java Facts · Jeff Dean 风格]]（`synchronized` / `volatile` / CAS 梗）
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

*约 2 分钟 · 拟人口吻 · 讲清原理与场景 · 先英后对照简中*

I am **concurrency**. Programs call me in when one **thread** cannot keep up with I/O, CPU cores, or incoming requests. I let many threads make progress **at the same time**. They share cores — and they share memory. Shared mutable state is why coordination is required.

**简中：** 我是并发。当一条线程跟不上 I/O、CPU 核心或涌入的请求时，程序会把我请来。我让多条线程**同时**推进。它们共享核心，也共享内存。共享可变状态，正是需要协调的原因。

Without coordination, thread interleaving is unpredictable. You get **race conditions** — wrong results that depend on timing. You get **visibility** failures — one thread never sees another's write. You get **deadlock** — threads wait in a circle, each holding what the other needs. I exist to prevent those three failures, not merely to run faster.

**简中：** 缺少协调时，线程交错不可预测。会出现**竞态条件**——结果随时机而错。会出现**可见性**失效——一条线程看不见另一条的写入。会出现**死锁**——线程循环等待，各自握着对方需要的东西。我存在是为了挡住这三类失败，不只是为了跑得更快。

My first rule is: prefer **immutability** and **confine** state. No shared mutable data means no lock. When sharing is unavoidable, use the JUC library — locks, atomics, synchronizers, concurrent collections, and executors. Do not hand-roll thread safety.

**简中：** 第一条原则：优先**不可变**，并**封闭**状态。没有共享可变数据，就不需要锁。必须共享时，用 JUC 库——锁、原子类、同步器、并发容器和执行器。不要手写线程安全。

**Volatile** gives **visibility**, not **atomicity**. I use it for flags such as `running`. `count++` is three steps: read, add, write. Two threads can both read the same value and both write plus one. For compound actions, use **`synchronized`** or an atomic class. **`synchronized`** also gives **mutual exclusion** and a **happens-before** edge: writes before unlock are visible after the next lock.

**简中：** **volatile** 保证**可见性**，不保证**原子性**。我把它用在 `running` 这类标志上。`count++` 是读、加、写三步。两条线程可能读到同一个值，各自只加一。复合动作要用 **`synchronized`** 或原子类。**`synchronized`** 还提供**互斥**和 **happens-before**：解锁前的写入，对下一次加锁可见。

**ReentrantLock** behaves like the built-in monitor, with extras: `tryLock`, timed waits, interruptible acquisition, and fairness. Always **unlock** in a **`finally`** block. Miss that, and the lock is never released — other threads wait forever. **ReadWriteLock** lets many readers proceed together; a writer excludes everyone. Use it on read-heavy caches.

**简中：** **ReentrantLock** 行为接近内置监视器，但多了 `tryLock`、超时等待、可中断获取和公平性。永远在 **`finally`** 里 **unlock**。漏了这一步，锁永不释放——其他线程会一直等。**ReadWriteLock** 允许多读并发，写则独占。适合读多写少的缓存。

A **CountDownLatch** is one-shot: one or more threads wait until N events finish. A **CyclicBarrier** is reusable: a fixed group meets at the same point again and again. A **Semaphore** issues counting permits and caps how many threads enter at once. Pick the synchronizer that matches the wait pattern — do not force one tool to do all three jobs.

**简中：** **CountDownLatch** 是一次性的：一条或多条线程等待 N 个事件完成。**CyclicBarrier** 可复用：固定一组线程反复在同一点会合。**Semaphore** 发放计数许可，限制同时进入的线程数。按等待模式选同步器——不要用一种工具硬扛三种活。

**ConcurrentHashMap** partitions the map, so most operations need no **global lock**. **BlockingQueue** makes producer–consumer straightforward: `put` blocks when the queue is full; `take` blocks when it is empty. Do not share a plain `HashMap` across threads and then add a lock after the bug appears.

**简中：** **ConcurrentHashMap** 对映射分区，多数操作无需**全局锁**。**BlockingQueue** 让生产者–消费者变直接：队列满时 `put` 阻塞，空时 `take` 阻塞。不要先让普通 `HashMap` 跨线程共享，出了 bug 再补一把锁。

Do not create raw threads for every task. Submit work to a **ThreadPoolExecutor** with an explicit queue, core and max size, and a rejection policy. Pools **reuse** threads — creation is expensive. They **bound** concurrency so you do not exhaust memory. A policy such as `CallerRunsPolicy` adds **back-pressure**: when the queue is full, the caller runs the task and slows down. **CompletableFuture** then composes async steps without blocking the caller: `supplyAsync` → `thenApply` → `thenCombine`.

**简中：** 不要为每个任务裸建线程。把工作提交给显式配置了队列、核心/最大线程数和拒绝策略的 **ThreadPoolExecutor**。线程池**复用**线程——创建代价高。它们**约束**并发，避免耗尽内存。`CallerRunsPolicy` 这类策略提供**背压**：队列满时由调用者自己跑任务，从而降速。**CompletableFuture** 再把异步步骤编排起来，而不阻塞调用方：`supplyAsync` → `thenApply` → `thenCombine`。

You need me for I/O-bound services, parallel CPU work, shared caches, producer–consumer pipelines, and request spikes. Follow these rules and I raise throughput. Skip them and I produce races, stale reads, leaked locks, and pool exhaustion. The cost is not speed — it is correctness under interleaving.

**简中：** I/O 密集服务、可并行的 CPU 工作、共享缓存、生产者–消费者流水线、请求峰值，都需要我。按这些规则来，我提高吞吐。跳过它们，就会出现竞态、读到旧值、锁泄漏和线程池耗尽。代价不是速度，而是交错执行下的正确性。
