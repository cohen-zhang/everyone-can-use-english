---
tags:
  - personal-english-book
  - english-learning
  - peb/study
aliases:
  - awesome-java-demo bridge
  - runnable Java demos
---
# awesome-java-demo Bridge — Runnable Schema Chunks

**Index:** [[learning-notes/personal-english-book/README|Personal English Book MOC]]

**Demo repo (GitHub):** https://github.com/zhangze2/awesome-demo

**Local sibling:** `../awesome-java-demo/` (when both repos live under `learn-wokspace/`)

**English vocabulary (demo repo):** [vocab-java-core](https://github.com/zhangze2/awesome-demo/blob/master/docs/english/vocab-java-core.md)

---

## Path A pilot — run from repo root

| Step | Module | Command | PEB note |
|------|--------|---------|----------|
| 1 | java-base | `mvn -pl java-base -q compile` · `java -cp java-base/target/classes collection.ArrayListFailFastExample` | [[learning-notes/personal-english-book/study/java-collections-framework\|Collections Framework]] |
| 2 | sort | `mvn -pl sort test` | [[learning-notes/personal-english-book/study/sorting-algorithms\|Sorting Algorithms]] |
| 3 | io | `mvn -pl io -q compile exec:java` | [[learning-notes/personal-english-book/study/computer-science-vocab-interesting\|CS vocabulary]] |
| 4 | jvm-tool | `java -cp jvm-tool/target/classes com.zz.ClassLoaderDemo` | [[learning-notes/personal-english-book/study/computer-science-vocab-interesting\|CS vocabulary]] |
| 5 | concurrency | `mvn -pl concurrency -q compile exec:java` | [[learning-notes/personal-english-book/study/completablefuture-java-guide\|CompletableFuture guide]] |

**Demo bridge (mirror):** https://github.com/zhangze2/awesome-demo/blob/master/docs/english/peb-bridge.md

---

## Schema → entry class

| Topic | Class (demo repo) | English README |
|-------|-------------------|----------------|
| fail-fast / ArrayList | `collection.ArrayListFailFastExample` | `java-base/README.en.md` |
| String intern | `string.StringInternExample` | `java-base/README.en.md` |
| JDK dynamic proxy | `proxy.JdkDynamicProxy` | `java-base/README.en.md` |
| Sorting algorithms | `sort.QuickSort` / `MergeSort` / `HeapSort` … | `sort/README.md` · PEB: [[learning-notes/personal-english-book/study/sorting-algorithms\|Sorting Algorithms]] |
| ClassLoader delegation | `com.zz.ClassLoaderDemo` | `jvm-tool/README.en.md` |
| GC heap + logs | `com.zz.GcLogAnalysisExample` | `jvm-tool/README.en.md` |
| Blocking socket | `io.demo.network.SocketEchoExample` | `io/README.en.md` |
| NIO Selector | `io.demo.network.SelectorEchoExample` | `io/README.en.md` |
| ReentrantLock | `concurrency.juc.lock.ReentrantLockExample` | `concurrency/README.en.md` |
| CompletableFuture | `concurrency.juc.executor.CompletableFutureExample` | `concurrency/README.en.md` |

---

## Study workflow

1. Read **English README** in awesome-java-demo.
2. Read matching **PEB** bilingual section (this vault).
3. Look up **IPA + official sentence** in demo [vocab-java-core](https://github.com/zhangze2/awesome-demo/blob/master/docs/english/vocab-java-core.md).
4. Run the schema; read **English Javadoc** in source.

---

*维护：新增 demo 图式时在本表补一行，并在 demo 仓库 `docs/english/peb-bridge.md` 同步。*

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **I review the key words and ideas in this note.** — 我复习本篇的核心单词和要点。
- **I read the examples aloud, then say them again from memory.** — 我先朗读例句，再脱稿复述一遍。
- **I connect one useful phrase to a real situation today.** — 我把一个实用短语连到今天的真实场景里。
- **Short, repeated practice helps the words stay with me.** — 简短而重复的练习能让单词留在记忆里。
- **I use one new phrase in a real conversation today.** — 我今天在真实对话中使用一个新短语。

### B. 一段串联（连续口语）

**I review the key words and ideas in this note. I read the examples aloud, then say them again from memory. I connect one useful phrase to a real situation today. Short, repeated practice helps the words stay with me. I use one new phrase in a real conversation today.**

**简中：** 我复习本篇的核心单词和要点。我先朗读例句，再脱稿复述一遍。我把一个实用短语连到今天的真实场景里。简短而重复的练习能让单词留在记忆里。我今天在真实对话中使用一个新短语。

### C. 一分钟复盘（5 句）

1. **I review the key words and ideas in this note.** — 我复习本篇的核心单词和要点。
2. **I read the examples aloud, then say them again from memory.** — 我先朗读例句，再脱稿复述一遍。
3. **I connect one useful phrase to a real situation today.** — 我把一个实用短语连到今天的真实场景里。
4. **Short, repeated practice helps the words stay with me.** — 简短而重复的练习能让单词留在记忆里。
5. **I use one new phrase in a real conversation today.** — 我今天在真实对话中使用一个新短语。

