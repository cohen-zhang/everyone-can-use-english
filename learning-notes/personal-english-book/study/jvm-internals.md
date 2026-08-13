---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
  - jvm
aliases:
  - JVM Internals
  - JVM 内部机制
  - JVM
---

# JVM Internals — JVM 内部机制

The JVM executes Java **bytecode**: it **loads** classes, manages **memory areas**, and reclaims garbage automatically. Understanding these internals turns mysterious crashes into diagnosable events.

JVM 执行 Java **字节码**：负责**加载**类、管理**内存区域**并自动回收垃圾。理解这些内部机制，能把神秘的崩溃变成可诊断的事件。

**Demo bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]  
**轻松一笑：** [[learning-notes/personal-english-book/study/java-joke-Jeff-Dean|Java Facts · Jeff Dean 风格]]（GC / JIT / ClassLoader 梗）

**Demo repo:** https://github.com/zhangze2/awesome-demo/tree/master/jvm-tool · **Local sibling:** `../awesome-java-demo/jvm-tool/`

---

## Overview — 概述

### What the JVM does — JVM 做了什么

Your `.java` file compiles to **bytecode** (`.class`). At runtime the JVM **loads** classes, allocates objects in the **heap**, runs each thread with its own **stack**, and runs **GC** to reclaim dead objects.

`.java` 文件编译为**字节码**（`.class`）。运行时 JVM **加载**类、在**堆**中分配对象、为每个线程维护独立**栈**，并通过 **GC** 回收死亡对象。

### Key Areas — 关键领域

1. **Class loading** — 类加载（双亲委派）
2. **Runtime data areas** — 运行时数据区
3. **Garbage collection** — 垃圾回收
4. **Diagnostics** — 诊断（GC 日志、堆转储）

---

## Core Concepts — 核心概念

### 1. Class Loaders & the Delegation Model — 类加载器与双亲委派

Class loaders use a **delegation model**: before loading a class itself, a loader **delegates** to its parent, up to the bootstrap loader.

类加载器采用**委派模型**：加载类之前，先**委派**给父加载器，逐级向上直到启动类加载器。

```
Bootstrap ClassLoader        — JDK core (java.lang.*) — JDK 核心类
    ↑ parent — 父
Extension / Platform Loader  — JDK extensions — 扩展类
    ↑ parent
Application ClassLoader      — your classpath — 应用类路径
```

**Why it matters — 意义**: core classes load exactly once from a trusted source; user code cannot shadow `java.lang.String` — 核心类只从可信来源加载一次；用户代码无法覆盖 `java.lang.String`。

### 2. Runtime Data Areas — 运行时数据区

| Area | Holds | 内容 | Per-… |
|------|-------|------|-------|
| **Heap** | objects, arrays — 对象、数组 | shared — 共享 |
| **Method area / Metaspace** | class metadata — 类元数据 | shared |
| **JVM stack** | frames: locals, operands — 栈帧：局部变量、操作数 | thread — 每线程 |
| **PC register** | current instruction — 当前指令 | thread |
| **Native stack** | JNI calls — 本地方法 | thread |

**StackOverflowError** = stack frames too deep (unbounded recursion); **OutOfMemoryError** = heap cannot fit a new object.

**StackOverflowError** = 栈帧过深（无限递归）；**OutOfMemoryError** = 堆放不下新对象。

### 3. Garbage Collection Basics — 垃圾回收基础

GC identifies **live** objects reachable from **GC roots** (stack locals, statics) and reclaims the rest. The heap is **generational**: most objects die young in the **young generation**; survivors promote to the **old generation**.

GC 从 **GC roots**（栈局部变量、静态引用）出发标记**存活**对象并回收其余。堆是**分代**的：多数对象在**年轻代**很快死亡；幸存者晋升到**老年代**。

- **Minor GC** — cleans young generation, fast — 清理年轻代，快
- **Full GC** — cleans the whole heap, expensive — 清理整个堆，昂贵
- Collectors: G1 (default), ZGC / Shenandoah (low pause) — 收集器：G1（默认）、ZGC / Shenandoah（低停顿）

### 4. Reading GC Logs — 读懂 GC 日志

```bash
java -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xms64m -Xmx64m \
  -cp jvm-tool/target/classes com.zz.GcLogAnalysisExample
```

```
[GC (Allocation Failure) [PSYoungGen: 15872K->2544K(17920K)] 15872K->4120K(58880K), 0.0031 secs]
```

Read it as: **cause** (Allocation Failure) → young gen **before→after (capacity)** → total heap **before→after** → **pause time**.

读法：**原因**（分配失败）→ 年轻代**回收前→后（容量）** → 整堆**回收前→后** → **停顿时间**。

### 5. OutOfMemoryError & Heap Dumps — OOM 与堆转储

`OutOfMemoryError` is thrown when the JVM **cannot allocate an object** because it is **out of heap space**. Add `-XX:+HeapDumpOnOutOfMemoryError` to capture a **heap dump** for post-mortem analysis.

当 JVM 因**堆空间不足**而**无法分配对象**时抛出 `OutOfMemoryError`。加 `-XX:+HeapDumpOnOutOfMemoryError` 可在出错时保存**堆转储**供事后分析。

```java
// Demo: allocate until OOM (danger — 危险演示)
List<byte[]> leak = new ArrayList<>();
while (true) leak.add(new byte[1024 * 1024]);
```

### 6. Common JVM Flags — 常用 JVM 参数

| Flag | Meaning | 含义 |
|------|---------|------|
| `-Xms` / `-Xmx` | initial / max heap — 初始 / 最大堆 | `-Xms512m -Xmx2g` |
| `-XX:+PrintGCDetails` | verbose GC log — 打印 GC 细节 | diagnostics — 诊断 |
| `-XX:+HeapDumpOnOutOfMemoryError` | dump on OOM — OOM 时转储 | production safety — 生产保障 |
| `-XX:MaxMetaspaceSize` | cap class metadata — 元空间上限 | prevent runaway — 防失控 |

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Bytecode** | /ˈbaɪtkoʊd/ | 字节码 | Compiled Java code executed by the JVM |
| **Class loader** | /klæs ˈloʊdər/ | 类加载器 | Loads class definitions into the JVM |
| **Delegation model** | /ˌdelɪˈɡeɪʃən ˈmɑːdəl/ | 委派模型 | Loaders ask their parent before loading themselves |
| **Bootstrap** | /ˈbuːtstræp/ | 启动类加载器 | The root loader for JDK core classes |
| **Heap** | /hiːp/ | 堆 | Shared memory area holding all objects |
| **Stack** | /stæk/ | 栈 | Per-thread memory for method frames |
| **Metaspace** | /ˈmetəspeɪs/ | 元空间 | Native memory holding class metadata |
| **Garbage collection** | /ˈɡɑːrbɪdʒ kəˈlekʃən/ | 垃圾回收 | Automatic reclamation of dead objects |
| **GC root** | /dʒiː siː ruːt/ | GC 根 | Starting points for reachability analysis |
| **Reachable** | /ˈriːtʃəbəl/ | 可达的 | Accessible from a GC root, so kept alive |
| **Young generation** | /jʌŋ ˌdʒenəˈreɪʃən/ | 年轻代 | Heap region where new objects are born |
| **Old generation** | /oʊld ˌdʒenəˈreɪʃən/ | 老年代 | Heap region for long-lived survivors |
| **Heap dump** | /hiːp dʌmp/ | 堆转储 | A snapshot of all objects for analysis |
| **Out of memory** | /aʊt əv ˈmeməri/ | 内存溢出 | No heap space left for a new object |
| **Allocation** | /ˌæləˈkeɪʃən/ | 分配 | Reserving memory for a new object |
| **Pause** | /pɔːz/ | 停顿 | Time the application stops during GC |

---

## Common Interview Questions — 常见面试问题

### Q: Explain the parent-delegation model and why it exists.

**A**: Every loader **delegates** to its parent first; the bootstrap loader gets the final say for JDK classes. This guarantees core classes load **once, from a trusted source**, and prevents user code from shadowing `java.lang.*`.

每个加载器先**委派**给父级；JDK 类最终由启动加载器定夺。这保证核心类**只从可信来源加载一次**，并防止用户代码覆盖 `java.lang.*`。

### Q: StackOverflowError vs OutOfMemoryError?

**A**: **StackOverflow** — one thread's call stack grows too deep (usually unbounded recursion). **OOM** — the shared **heap** cannot fit a new allocation (leaks, undersized `-Xmx`).

**StackOverflow**——单线程调用栈过深（通常是无限递归）；**OOM**——共享**堆**放不下新对象（内存泄漏、`-Xmx` 过小）。

### Q: How does generational GC justify itself?

**A**: Empirically, **most objects die young**. Collecting the young generation frequently is cheap and reclaims most garbage; old-generation collections stay rare.

经验表明**大多数对象朝生夕死**。频繁回收年轻代代价低、收效大；老年代回收得以保持低频。

### Q: What do you do when production throws OOM?

**A**: (1) Capture a **heap dump** (`-XX:+HeapDumpOnOutOfMemoryError`); (2) analyze dominators with MAT/JVisualVM to find the leak; (3) review GC logs for rising old-gen usage; (4) fix the leak, not just raise `-Xmx`.

（1）抓取**堆转储**；（2）用 MAT/JVisualVM 分析支配树找泄漏点；（3）看 GC 日志中老年代是否持续上涨；（4）修复泄漏，而不是只调大 `-Xmx`。

---

## Further Reading — 延伸阅读

- [The Java Virtual Machine Specification](https://docs.oracle.com/javase/specs/jvms/se17/html/)
- [Baeldung: JVM Memory Model](https://www.baeldung.com/java-jvm-memory-model)
- [Baeldung: Java ClassLoaders](https://www.baeldung.com/java-classloaders)
- Related: [[learning-notes/personal-english-book/study/jvm|JVM 运行时数据区图解]] · [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/java-concurrency|并发编程]] · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/computer-science-vocab-interesting|有趣计科词汇]]
- Source README (demo): https://github.com/zhangze2/awesome-demo/blob/master/jvm-tool/README.en.md

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (demo repo root) |
|-------|------------|----------------------|
| Class loader delegation | `com.zz.ClassLoaderDemo` | `mvn -pl jvm-tool -q compile` · `java -cp jvm-tool/target/classes com.zz.ClassLoaderDemo` |
| GC log analysis | `com.zz.GcLogAnalysisExample` | `java -XX:+PrintGCDetails -Xms64m -Xmx64m -cp jvm-tool/target/classes com.zz.GcLogAnalysisExample` |
| OOM + heap dump | `com.zz.OutOfMemoryTest` | `java -Xmx32m -XX:+HeapDumpOnOutOfMemoryError -cp jvm-tool/target/classes com.zz.OutOfMemoryTest` (danger — 危险) |

**English README (demo):** https://github.com/zhangze2/awesome-demo/blob/master/jvm-tool/README.en.md

**Tags**: `技术`, `Java`, `JVM`, `GC`, `类加载`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Class loaders delegate to their parents first.** — 类加载器先委派给父级。
- **Objects live in the heap; frames live on the stack.** — 对象住在堆里；栈帧住在栈上。
- **Most objects die young.** — 大多数对象朝生夕死。
- **Read the GC log: cause, before, after, pause.** — 读 GC 日志：原因、回收前、回收后、停顿。
- **Capture a heap dump when memory runs out.** — 内存耗尽时抓取堆转储。

### B. 一段串联（连续口语）

**Class loaders delegate to their parents first. Objects live in the heap; frames live on the stack. Most objects die young. Read the GC log: cause, before, after, pause. Capture a heap dump when memory runs out.**

**简中：** 类加载器先委派给父级。对象住在堆里；栈帧住在栈上。大多数对象朝生夕死。读 GC 日志：原因、回收前、回收后、停顿。内存耗尽时抓取堆转储。

### C. 一分钟复盘（5 句）

1. **Class loaders delegate to their parents first.** — 类加载器先委派给父级。
2. **Objects live in the heap; frames live on the stack.** — 对象住在堆里；栈帧住在栈上。
3. **Most objects die young.** — 大多数对象朝生夕死。
4. **Read the GC log: cause, before, after, pause.** — 读 GC 日志：原因、回收前、回收后、停顿。
5. **Capture a heap dump when memory runs out.** — 内存耗尽时抓取堆转储。
