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
| 2 | io | `mvn -pl io -q compile exec:java` | [[learning-notes/personal-english-book/study/computer-science-vocab-interesting\|CS vocabulary]] |
| 3 | jvm-tool | `java -cp jvm-tool/target/classes com.zz.ClassLoaderDemo` | [[learning-notes/personal-english-book/study/computer-science-vocab-interesting\|CS vocabulary]] |
| 4 | concurrency | `mvn -pl concurrency -q compile exec:java` | [[learning-notes/personal-english-book/study/completablefuture-java-guide\|CompletableFuture guide]] |

**Demo bridge (mirror):** https://github.com/zhangze2/awesome-demo/blob/master/docs/english/peb-bridge.md

---

## Schema → entry class

| Topic | Class (demo repo) | English README |
|-------|-------------------|----------------|
| fail-fast / ArrayList | `collection.ArrayListFailFastExample` | `java-base/README.en.md` |
| String intern | `string.StringInternExample` | `java-base/README.en.md` |
| JDK dynamic proxy | `proxy.JdkDynamicProxy` | `java-base/README.en.md` |
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
