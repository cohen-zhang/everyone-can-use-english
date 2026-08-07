---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
aliases:
  - Java IO & Streams
  - Java IO
  - IO 流
---

# Java IO & Streams — Java IO 流

Java I/O is a **data pipeline**: bytes and characters flow between your program and files, network sockets, or memory. This note covers byte streams, char streams, buffering, NIO, and resource management.

Java I/O 是一条**数据管道**：字节与字符在程序与文件、网络套接字或内存之间流动。本文涵盖字节流、字符流、缓冲、NIO 与资源管理。

**Demo bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

**Demo repo:** https://github.com/zhangze2/awesome-demo/tree/master/io · **Local sibling:** `../awesome-java-demo/io/`

---

## Overview — 概述

### The Pipeline Mental Model — 管道心智模型

An **InputStream** represents an input **stream of bytes**; an **OutputStream** an output stream. Everything else — readers, buffers, channels — builds on this abstraction.

**InputStream** 表示字节**输入流**；**OutputStream** 表示输出流。其余一切——Reader、缓冲、Channel——都建立在此抽象之上。

### Key Distinctions — 关键区分

1. **Byte streams** (`InputStream`/`OutputStream`) — raw binary data — 字节流：原始二进制
2. **Char streams** (`Reader`/`Writer`) — text with an explicit **charset** — 字符流：带明确**字符集**的文本
3. **Blocking IO (BIO)** vs **NIO** — 阻塞式 IO 与非阻塞/多路复用 IO
4. **Resource management** — close handles deterministically — 资源管理：确定性关闭句柄

---

## Core Concepts — 核心概念

### 1. Byte Streams — 字节流

`FileInputStream` / `FileOutputStream` read and write raw bytes. The classic copy loop reads into a **buffer** until the stream returns `-1` (end of stream).

`FileInputStream` / `FileOutputStream` 读写原始字节。经典拷贝循环读入**缓冲区**，直到流返回 `-1`（流结束）。

```java
byte[] buffer = new byte[8192];
int n;
while ((n = in.read(buffer)) != -1) { // read returns count — 返回读取字节数
    out.write(buffer, 0, n);
}
```

### 2. Buffered Streams — 缓冲流

**Buffered** streams batch many small reads/writes into fewer **system calls**, dramatically improving throughput.

**缓冲**流把大量小读写合并为少量**系统调用**，显著提升吞吐。

```java
try (var in = new BufferedInputStream(new FileInputStream("a.bin"))) {
    return in.readAllBytes();
}
```

### 3. The Bridge: Bytes → Chars — 桥接：字节转字符

`InputStreamReader` **decodes** bytes into characters using a **charset** — always specify UTF-8 explicitly to avoid platform-dependent bugs.

`InputStreamReader` 用**字符集**把字节**解码**为字符——务必显式指定 UTF-8，避免依赖平台的缺陷。

```java
Reader reader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
```

### 4. NIO: Buffers, Channels, Files — NIO：缓冲区、通道、Files

NIO centers on **Channel** + **Buffer**: put data into a `ByteBuffer`, **flip** it to read back, then get. Modern code often prefers the `Files` utility for whole-file operations.

NIO 以 **Channel** + **Buffer** 为核心：向 `ByteBuffer` 写入数据，**flip（翻转）**后读出。整文件操作优先用 `Files` 工具类。

```java
ByteBuffer buf = ByteBuffer.allocate(64);
buf.put("hi".getBytes(StandardCharsets.UTF_8));
buf.flip();                     // prepare for reading — 切换为读模式
while (buf.hasRemaining()) System.out.print((char) buf.get());

List<String> lines = Files.readAllLines(Path.of("notes.txt"), StandardCharsets.UTF_8);
```

### 5. Try-with-resources — 自动关闭资源

The **try-with-resources** statement declares resources that are **automatically closed**, even on exception. Leaking handles is a classic production bug.

**try-with-resources** 语句声明的资源会被**自动关闭**，即使发生异常。句柄泄漏是经典生产事故。

```java
try (FileInputStream in = new FileInputStream("data.bin")) { // auto-closed — 自动关闭
    process(in);
}
```

**Anti-pattern — 反面案例**: opening a stream without closing it (see `StreamWithoutCloseExample` in the demo) — 打开流却不关闭（见 demo 中 `StreamWithoutCloseExample`）。

### 6. BIO vs NIO Networking — BIO 与 NIO 网络编程

**BIO**: `ServerSocket` + **blocking** read — one thread per connection. **NIO**: a **Selector** is a multiplexor of **selectable channels** — one thread handles many connections.

**BIO**：`ServerSocket` + **阻塞**读取——每连接一线程。**NIO**：**Selector** 是**可选择通道**的多路复用器——单线程处理多连接。

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Stream** | /striːm/ | 流 | An ordered sequence of bytes or characters |
| **Pipeline** | /ˈpaɪplaɪn/ | 管道 | A chain of processing stages data flows through |
| **Buffer** | /ˈbʌfər/ | 缓冲区 | Temporary memory holding data in transit |
| **Buffered** | /ˈbʌfərd/ | 缓冲的 | Batching small operations into larger ones |
| **Charset** | /ˈkɑːrset/ | 字符集 | A mapping between bytes and characters |
| **Decode** | /diːˈkoʊd/ | 解码 | Convert bytes into characters |
| **Encode** | /ɪnˈkoʊd/ | 编码 | Convert characters into bytes |
| **Blocking** | /ˈblɑːkɪŋ/ | 阻塞的 | Waiting until an operation completes |
| **Selector** | /sɪˈlektər/ | 选择器 | A multiplexor monitoring many channels at once |
| **Channel** | /ˈtʃænəl/ | 通道 | An NIO endpoint for two-way data transfer |
| **Flip** | /flɪp/ | 翻转 | Switch a ByteBuffer from write mode to read mode |
| **Try-with-resources** | /traɪ wɪð rɪˈsɔːrsɪz/ | 资源自动关闭语句 | Auto-closes declared resources |
| **End of stream** | /end əv striːm/ | 流结束 | Signaled by read returning `-1` |
| **Multiplexor** | /ˈmʌltɪpleksər/ | 多路复用器 | Handles many channels with one selector |
| **Leak** | /liːk/ | 泄漏 | Failing to release a resource |
| **Throughput** | /ˈθruːpʊt/ | 吞吐量 | Amount of data processed per unit time |

---

## Common Interview Questions — 常见面试问题

### Q: InputStream vs Reader — when do you use which?

**A**: Use **byte streams** for binary data (images, zip files); use **char streams** for text, always bridging with an explicit **charset** like UTF-8.

二进制数据（图片、zip）用**字节流**；文本用**字符流**，且始终用显式**字符集**（如 UTF-8）做桥接。

### Q: Why does buffering improve performance?

**A**: Each unbuffered `read()` can cost a **system call**. A buffered stream fills an 8 KB buffer per call, turning thousands of calls into a handful.

未缓冲的每次 `read()` 都可能是一次**系统调用**。缓冲流每次调用填满 8 KB 缓冲区，把成千上万次调用变成寥寥几次。

### Q: What does `flip()` do on a ByteBuffer?

**A**: It sets the **limit** to the current position and resets the position to zero, switching the buffer from write mode to read mode.

它把 **limit** 设为当前位置，并把位置归零，使缓冲区从写模式切换到读模式。

### Q: How does a Selector handle many connections?

**A**: Channels register **interest** (accept/read/write) with one Selector. The selector blocks until at least one channel is ready, then you iterate the ready set — one thread, many connections.

通道向一个 Selector 注册**感兴趣的事件**（accept/read/write）。selector 阻塞到至少一个通道就绪，随后遍历就绪集合——单线程，多连接。

---

## Further Reading — 延伸阅读

- [java.io package summary](https://docs.oracle.com/javase/8/docs/api/java/io/package-summary.html)
- [java.nio package summary](https://docs.oracle.com/javase/8/docs/api/java/nio/package-summary.html)
- [Baeldung: Java IO vs NIO](https://www.baeldung.com/java-io-vs-nio)
- Related: [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/java-concurrency|并发编程]]
- Source README (demo): https://github.com/zhangze2/awesome-demo/blob/master/io/README.en.md

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (demo repo root) |
|-------|------------|----------------------|
| Byte stream / buffer copy | `io.demo.byteflow.FileStreamExample` | `mvn -pl io -q compile exec:java` |
| Bytes → chars (UTF-8) | `io.demo.bridge.InputStreamReaderExample` | `java -cp io/target/classes io.demo.bridge.InputStreamReaderExample` |
| try-with-resources | `io.demo.resource.TryWithResourcesExample` | `java -cp io/target/classes io.demo.resource.TryWithResourcesExample` |
| ByteBuffer flip | `io.demo.nio.ByteBufferExample` | `java -cp io/target/classes io.demo.nio.ByteBufferExample` |
| BIO echo server | `io.demo.network.SocketEchoExample` | `mvn -pl io -q compile exec:java -Dexec.mainClass=io.demo.IODemoRunner -Dexec.args=6.1` |
| NIO selector echo | `io.demo.network.SelectorEchoExample` | `... -Dexec.args=6.2` |

**English README (demo):** https://github.com/zhangze2/awesome-demo/blob/master/io/README.en.md

**Tags**: `技术`, `Java`, `IO`, `NIO`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **An InputStream is a stream of bytes.** — InputStream 是字节流。
- **Buffered streams reduce system calls.** — 缓冲流减少系统调用。
- **Bridge bytes to chars with UTF-8.** — 用 UTF-8 把字节桥接为字符。
- **Flip the buffer before you read.** — 读之前先翻转缓冲区。
- **Try-with-resources closes handles for you.** — try-with-resources 替你关闭句柄。

### B. 一段串联（连续口语）

**An InputStream is a stream of bytes. Buffered streams reduce system calls. Bridge bytes to chars with UTF-8. Flip the buffer before you read. Try-with-resources closes handles for you.**

**简中：** InputStream 是字节流。缓冲流减少系统调用。用 UTF-8 把字节桥接为字符。读之前先翻转缓冲区。try-with-resources 替你关闭句柄。

### C. 一分钟复盘（5 句）

1. **An InputStream is a stream of bytes.** — InputStream 是字节流。
2. **Buffered streams reduce system calls.** — 缓冲流减少系统调用。
3. **Bridge bytes to chars with UTF-8.** — 用 UTF-8 把字节桥接为字符。
4. **Flip the buffer before you read.** — 读之前先翻转缓冲区。
5. **Try-with-resources closes handles for you.** — try-with-resources 替你关闭句柄。
