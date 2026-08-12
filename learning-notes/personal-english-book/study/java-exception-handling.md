---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
aliases:
  - Java Exception Handling
  - 异常处理
  - Java 异常
---

# Java Exception Handling — Java 异常处理

Exceptions are Java's way to signal that something went wrong **outside the normal flow**. This note covers the Throwable hierarchy, checked vs unchecked exceptions, resource cleanup, business exception design, and common anti-patterns.

异常是 Java 在**正常流程之外**发出问题信号的方式。本文涵盖 Throwable 层级、受检与非受检异常、资源清理、业务异常设计与常见反面模式。

**Demo bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

**Demo repo:** https://github.com/zhangze2/awesome-demo/tree/master/exception · **Local sibling:** `../awesome-java-demo/exception/`

---

## Overview — 概述

### What is an exception? — 什么是异常？

An **exception** is an event that **disrupts the normal flow** of a program. When it is **thrown**, the runtime unwinds the call stack until a matching **handler** (`catch`) is found — or the thread dies.

**异常**是**打断程序正常流程**的事件。异常被**抛出**后，运行时沿调用栈回溯，直到找到匹配的**处理器**（`catch`）——否则线程终止。

### The Throwable Hierarchy — Throwable 层级

```
Throwable
├── Error — serious JVM problems, don't catch — 严重 JVM 问题，不要捕获
│   └── OutOfMemoryError, StackOverflowError, ...
└── Exception — recoverable conditions — 可恢复状况
    ├── RuntimeException (unchecked) — 非受检
    │   └── NullPointerException, IllegalArgumentException, ...
    └── checked: IOException, SQLException, ... — 受检：编译器强制处理
```

### Key Principles — 核心原则

1. **Catch specific exceptions** — 捕获具体异常，而非一把梭 `Exception`
2. **Don't swallow** — never catch and ignore — 不要吞掉异常
3. **Clean up deterministically** — finally / try-with-resources — 确定性清理
4. **Fail fast, recover gracefully** — 快速失败，优雅恢复

---

## Core Concepts — 核心概念

### 1. Checked vs Unchecked — 受检 vs 非受检

**Checked exceptions** must be declared (`throws`) or caught — the compiler enforces it. **Unchecked exceptions** (`RuntimeException` and subclasses) signal programming bugs and don't require declarations.

**受检异常**必须声明（`throws`）或捕获——编译器强制。**非受检异常**（`RuntimeException` 及其子类）表示编程错误，无需声明。

```java
// Checked — must handle or declare — 必须处理或声明
String text = Files.readString(Path.of("f.txt")); // throws IOException

// Unchecked — a programming bug — 编程错误
int length = name.length(); // NullPointerException if name is null — name 为 null 时 NPE
```

**Guideline — 准则**: use checked for **recoverable** conditions a caller can handle; unchecked for **contract violations** — 调用方可恢复的状况用受检；违反契约用非受检。

### 2. try / catch / finally — 异常处理三板斧

```java
try {
    riskyOperation();
} catch (SpecificException e) {   // Catch specific first — 先捕获具体异常
    log.error("risky op failed", e);
    throw new BusinessException("OPERATION_FAILED", 1001, e);
} finally {
    cleanup();                    // Always runs — 总会执行
}
```

**Pitfall — 陷阱**: throwing inside `finally` **swallows** the original exception — 在 `finally` 中抛出异常会**吞掉**原异常（见 demo `FinallyExceptionDemo`）。

### 3. Custom Business Exceptions — 自定义业务异常

Business exceptions carry an **error code** for API responses and extend `RuntimeException` to avoid polluting signatures.

业务异常携带**错误码**供 API 响应使用，并继承 `RuntimeException` 避免污染方法签名。

```java
public class BusinessException extends RuntimeException {
    private final int errorCode;

    public BusinessException(String message, int errorCode) {
        super(message);
        this.errorCode = errorCode;
    }
}
```

### 4. NPE Defense — 空指针防护

`NullPointerException` is the most common runtime crash. Defenses: **null checks at boundaries**, `Optional` for absent values, `Objects.requireNonNull` for contracts.

`NullPointerException` 是最常见的运行时崩溃。防护手段：**边界处判空**、用 `Optional` 表达可能缺失的值、用 `Objects.requireNonNull` 校验契约。

```java
Objects.requireNonNull(order, "order must not be null");
String name = Optional.ofNullable(user).map(User::getName).orElse("anonymous");
```

### 5. Global Exception Handling — 全局异常处理

In Spring, `@RestControllerAdvice` turns exceptions into uniform API responses in one place — no try/catch scattered across controllers. （扩展：[[learning-notes/personal-english-book/study/spring-framework-notes|Spring Framework · MVC]]）

在 Spring 中，`@RestControllerAdvice` 在一处把异常统一转换为 API 响应——控制器里不再散落 try/catch。

```java
@RestControllerAdvice
public class RestControllerExceptionHandler {
    @ExceptionHandler(BusinessException.class)
    public APIResponse<Void> handleBusiness(BusinessException e) {
        return APIResponse.error(e.getErrorCode(), e.getMessage());
    }
}
```

### 6. Anti-patterns — 反面模式

- **Swallowing** — `catch (Exception e) {}` — 吞异常：静默失败，极难排查
- **Throwing from finally** — hides the root cause — finally 中抛出：掩盖根因
- **Exception for flow control** — exceptions are expensive — 用异常控流程：代价高昂
- **Over-catch then re-wrap** — losing the stack trace — 过度捕获再包装：丢失堆栈

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Exception** | /ɪkˈsepʃən/ | 异常 | An event that disrupts normal program flow |
| **Throw** | /θroʊ/ | 抛出 | Raise an exception to signal a problem |
| **Catch** | /kætʃ/ | 捕获 | Handle a thrown exception in a catch block |
| **Checked exception** | /tʃekt ɪkˈsepʃən/ | 受检异常 | Must be declared or caught; compiler-enforced |
| **Unchecked exception** | /ʌnˈtʃekt ɪkˈsepʃən/ | 非受检异常 | Runtime exceptions; no declaration required |
| **Stack trace** | /stæk treɪs/ | 堆栈轨迹 | The call chain recorded when an exception occurs |
| **Swallow** | /ˈswɑːloʊ/ | 吞掉 | Catch an exception and silently ignore it |
| **Finally** | /ˈfaɪnəli/ | finally 块 | Code that always runs after try/catch |
| **Recoverable** | /rɪˈkʌvərəbəl/ | 可恢复的 | A condition the caller can reasonably handle |
| **Error code** | /ˈerər koʊd/ | 错误码 | A numeric identifier for an error category |
| **NullPointerException** | /nʌl ˈpɔɪntər ɪkˈsepʃən/ | 空指针异常 | Thrown when dereferencing a null reference |
| **Optional** | /ˈɑːpʃənəl/ | Optional 容器 | A container that may or may not hold a value |
| **Global handler** | /ˈɡloʊbəl ˈhændlər/ | 全局处理器 | Centralized exception-to-response conversion |
| **Root cause** | /ruːt kɔːz/ | 根因 | The original exception in a cause chain |
| **Unwind** | /ʌnˈwaɪnd/ | 回溯 | Walking back up the call stack |
| **Anti-pattern** | /ˈænti ˈpætərn/ | 反面模式 | A common but harmful practice |

---

## Common Interview Questions — 常见面试问题

### Q: What's the difference between Error and Exception?

**A**: **Error** marks serious JVM-level problems (OOM, stack overflow) that applications should not try to catch. **Exception** marks conditions a program may reasonably handle.

**Error** 表示 JVM 级严重问题（OOM、栈溢出），应用不应捕获；**Exception** 表示程序可以合理处理的情况。

### Q: checked vs unchecked — how do you choose?

**A**: Ask: can the caller **recover**? If yes (file not found → prompt again), make it checked. If it's a **programming bug** (null argument), use unchecked.

问自己：调用方能否**恢复**？能（文件不存在→提示重试）则用受检；若是**编程错误**（传了 null），用非受检。

### Q: Why shouldn't you throw from a finally block?

**A**: The exception thrown in `finally` **replaces** the original one from `try`, so the real root cause disappears from the stack trace. Prefer try-with-resources.

`finally` 中抛出的异常会**覆盖** `try` 中的原异常，真正的根因从堆栈中消失。优先使用 try-with-resources。

### Q: Why design business exceptions as unchecked?

**A**: Business failures usually cannot be recovered by the immediate caller, and checked declarations would **pollute every signature** up the stack. A global handler converts them to responses.

业务失败通常无法由直接调用方恢复；受检声明会**污染整条调用链**的签名。全局处理器统一将其转为响应。

---

## Further Reading — 延伸阅读

- [Oracle Tutorial: Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/)
- [Baeldung: Java Exceptions](https://www.baeldung.com/java-exceptions)
- [Baeldung: Common Java Exceptions](https://www.baeldung.com/java-common-exceptions)
- Related: [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/java-keywords|Java 关键字]]（`throw` / `throws` / `try`） · [[learning-notes/personal-english-book/study/java-io-streams|IO 流]] · [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]] · [[learning-notes/personal-english-book/study/spring-framework-notes|Spring Framework]]
- Source README (demo): https://github.com/zhangze2/awesome-demo/blob/master/exception/README.md

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Notes |
|-------|------------|-------|
| Business exception design | `com.example.awesomedemo.BusinessException` | errorCode + RuntimeException |
| Global handler | `com.example.awesomedemo.advice.RestControllerExceptionHandler` | `@RestControllerAdvice` |
| NPE defense | `com.example.awesomedemo.npe.AvoidNullPointerExceptionController` | boundary null checks |
| Anti-patterns | `com.example.awesomedemo.dirty.*` (`ErrorExceptionDemo`, `FinallyExceptionDemo`, ...) | learn from wrong examples — 从错误示例学习 |

Module is a Spring Boot app; run tests / start per module README: `cd exception && mvn spring-boot:run`.

**English README (demo):** https://github.com/zhangze2/awesome-demo/blob/master/exception/README.md (中文为主)

**Tags**: `技术`, `Java`, `异常`, `最佳实践`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Exceptions disrupt the normal flow.** — 异常打断正常流程。
- **Catch specific exceptions, not everything.** — 捕获具体异常，不要一网打尽。
- **Never swallow an exception silently.** — 绝不静默吞掉异常。
- **Business exceptions carry an error code.** — 业务异常携带错误码。
- **A global handler keeps controllers clean.** — 全局处理器让控制器保持干净。

### B. 一段串联（连续口语）

**Exceptions disrupt the normal flow. Catch specific exceptions, not everything. Never swallow an exception silently. Business exceptions carry an error code. A global handler keeps controllers clean.**

**简中：** 异常打断正常流程。捕获具体异常，不要一网打尽。绝不静默吞掉异常。业务异常携带错误码。全局处理器让控制器保持干净。

### C. 一分钟复盘（5 句）

1. **Exceptions disrupt the normal flow.** — 异常打断正常流程。
2. **Catch specific exceptions, not everything.** — 捕获具体异常，不要一网打尽。
3. **Never swallow an exception silently.** — 绝不静默吞掉异常。
4. **Business exceptions carry an error code.** — 业务异常携带错误码。
5. **A global handler keeps controllers clean.** — 全局处理器让控制器保持干净。
