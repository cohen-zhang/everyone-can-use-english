# CompletableFuture in Java — 异步编程工具

CompletableFuture is a powerful class in Java that represents a future result of an asynchronous computation. It was introduced in Java 8 as part of the `java.util.concurrent` package.

CompletableFuture 是 Java 中的一个强大的类，表示异步计算的未来结果。它作为 `java.util.concurrent` 包的一部分在 Java 8 中引入。

## Overview — 概述

### What is CompletableFuture? — 什么是 CompletableFuture？

**CompletableFuture** provides a more flexible and functional approach to **asynchronous programming** compared to the older `Future` interface. It allows you to chain multiple operations together and handle exceptions gracefully.

与较旧的 `Future` 接口相比，**CompletableFuture** 为**异步编程**提供了更灵活和功能性的方法。它允许您将多个操作链接在一起，并优雅地处理异常。

### Key Features — 主要特性

1. **Non-blocking operations** — 非阻塞操作
2. **Chaining and composition** — 链式调用与组合
3. **Exception handling** — 异常处理
4. **Combining multiple futures** — 组合多个 Future

## Core Concepts — 核心概念

### 1. Creating CompletableFutures — 创建 CompletableFuture

```java
// Supply async — 异步供应并返回结果
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Hello, World!";
});

// Run async — 异步执行，无返回值
CompletableFuture<Void> voidFuture = CompletableFuture.runAsync(() -> {
    System.out.println("Executing asynchronously");
});
```

**Supply** vs **Run**:
- `supplyAsync()` — Returns a result — 返回结果
- `runAsync()` — No return value — 无返回值

### 2. Chaining Operations — 链式操作

```java
CompletableFuture.supplyAsync(() -> "hello")
    .thenApplyAsync(String::toUpperCase)  // Transform — 转换
    .thenAcceptAsync(System.out::println) // Consume — 消费
    .thenRunAsync(() -> {                 // Run final action — 执行最终操作
        System.out.println("Processing complete");
    });
```

**Key Methods**:
- `thenApply()` — Transform the result — 转换结果
- `thenAccept()` — Consume the result — 消费结果
- `thenRun()` — Execute code without accessing result — 执行代码但不访问结果

### 3. Exception Handling — 异常处理

```java
CompletableFuture.supplyAsync(() -> {
    if (true) throw new RuntimeException("Something went wrong");
    return "Success";
})
.exceptionally(ex -> {
    System.out.println("Error: " + ex.getMessage());
    return "Fallback value"; // Provide fallback — 提供回退值
});
```

**Handle** provides more control:
```java
CompletableFuture.supplyAsync(() -> "result")
    .handle((result, ex) -> {
        if (ex != null) {
            return "Error recovery"; // Handle exception — 处理异常
        }
        return result; // Handle success — 处理成功
    });
```

### 4. Combining Multiple Futures — 组合多个 Future

```java
// Combine two futures — 组合两个 Future
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

future1.thenCombine(future2, (s1, s2) -> s1 + " " + s2)
       .thenAccept(System.out::println); // Output: Hello World
```

**Wait for all futures to complete** — 等待所有 Future 完成：
```java
CompletableFuture<Void> allFutures = CompletableFuture.allOf(
    future1, future2, future3
);
```

**Wait for any future to complete** — 等待任意一个 Future 完成：
```java
CompletableFuture<Object> anyFuture = CompletableFuture.anyOf(
    future1, future2, future3
);
```

## Practical Example — 实际示例

### User Profile Loading — 用户资料加载

```java
public CompletableFuture<User> getUserWithProfileAsync(String userId) {
    return CompletableFuture.supplyAsync(() -> {
        // Fetch user from database — 从数据库获取用户
        return userRepository.findById(userId);
    })
    .thenComposeAsync(user -> {
        // Fetch profile asynchronously — 异步获取资料
        return CompletableFuture.supplyAsync(() ->
            profileService.getProfile(user.getId())
        ).thenApply(profile -> {
            user.setProfile(profile);
            return user;
        });
    })
    .exceptionally(ex -> {
        log.error("Failed to load user: {}", ex.getMessage());
        return new User(); // Return default user — 返回默认用户
    });
}
```

**Key Methods Used**:
- `thenCompose()` — FlatMap operation — 扁平映射操作
- `thenApply()` — Map operation — 映射操作
- `exceptionally()` — Error handling — 错误处理

## Common Use Cases — 常见用例

### 1. Parallel API Calls — 并行 API 调用

```java
// Make multiple API calls in parallel — 并行发起多个 API 调用
CompletableFuture<User> userFuture = getUserAsync(userId);
CompletableFuture<List<Order>> ordersFuture = getOrdersAsync(userId);
CompletableFuture<Recommendations> recsFuture = getRecommendationsAsync(userId);

// Combine results — 组合结果
CompletableFuture.allOf(userFuture, ordersFuture, recsFuture)
    .thenRun(() -> {
        User user = userFuture.join();
        List<Order> orders = ordersFuture.join();
        Recommendations recs = recsFuture.join();
        // Process combined data — 处理组合数据
    });
```

### 2. Data Processing Pipeline — 数据处理管道

```java
List<CompletableFuture<ProcessedData>> futures = rawDataList.stream()
    .map(data -> CompletableFuture.supplyAsync(() -> process(data))
        .thenApplyAsync(this::enrich)
        .thenApplyAsync(this::validate))
    .collect(Collectors.toList());

// Wait for all processing to complete — 等待所有处理完成
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
    .thenRun(() -> {
        List<ProcessedData> results = futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());
        // Handle final results — 处理最终结果
    });
```

## Advantages Over Future — 相比 Future 的优势

| Feature | Future | CompletableFuture |
|---------|--------|------------------|
| **Manual completion** — 手动完成 | ❌ No | ✅ Yes |
| **Chaining** — 链式调用 | ❌ No | ✅ Yes |
| **Exception handling** — 异常处理 | ❌ Limited | ✅ Comprehensive |
| **Composition** — 组合操作 | ❌ No | ✅ Yes |
| **Non-blocking** — 非阻塞 | ❌ No | ✅ Yes |

## Best Practices — 最佳实践

### 1. Use Custom Thread Pools — 使用自定义线程池

```java
// Create custom executor — 创建自定义执行器
ExecutorService executor = Executors.newFixedThreadPool(10);

CompletableFuture.supplyAsync(() -> "task", executor)
    .thenApplyAsync(String::toUpperCase, executor);
```

### 2. Avoid Blocking Operations — 避免阻塞操作

```java
// Bad — blocks thread — 阻塞线程
future.get(); // Blocks until complete — 阻塞直到完成

// Good — non-blocking — 非阻塞
future.thenAccept(result -> {
    // Handle result when ready — 准备好时处理结果
});
```

### 3. Handle Timeouts — 处理超时

```java
CompletableFuture.supplyAsync(() -> longRunningTask())
    .orTimeout(5, TimeUnit.SECONDS) // Java 9+ — Java 9+
    .exceptionally(ex -> {
        if (ex instanceof TimeoutException) {
            return "default value"; // Handle timeout — 处理超时
        }
        return "error value";
    });
```

## Vocabulary — 词汇表

| Term | 中文 | Definition |
|------|------|------------|
| **Asynchronous** | 异步的 | Not occurring at the same time — operations that don't block |
| **Computation** | 计算 | The process of calculating something |
| **Chaining** | 链式调用 | Linking multiple operations together in sequence |
| **Exception** | 异常 | An error condition that disrupts normal program flow |
| **Non-blocking** | 非阻塞 | Operations that don't prevent other code from executing |
| **Thread pool** | 线程池 | A collection of reusable threads for executing tasks |
| **Callback** | 回调 | A function passed as an argument to be executed later |
| **Composition** | 组合 | Combining multiple operations or futures together |
| **Timeout** | 超时 | A time limit for an operation to complete |
| **Executor** | 执行器 | An object that manages thread execution |

## Common Interview Questions — 常见面试问题

### Q: What's the difference between `thenApply` and `thenCompose`?

**A**: `thenApply` is like `map` — it transforms the result synchronously. `thenCompose` is like `flatMap` — it allows you to chain asynchronous operations by returning a new CompletableFuture.

`thenApply` 类似于 `map` — 同步转换结果。`thenCompose` 类似于 `flatMap` — 通过返回新的 CompletableFuture 来链接异步操作。

### Q: How do you handle exceptions in CompletableFuture?

**A**: You can use `exceptionally()` for basic error handling, or `handle()` for more control over both success and error cases. You can also use `whenComplete()` to execute code regardless of success or failure.

可以使用 `exceptionally()` 进行基本错误处理，或使用 `handle()` 对成功和错误情况进行更多控制。也可以使用 `whenComplete()` 无论成功或失败都执行代码。

---

## Further Reading — 延伸阅读

- [Java Documentation: CompletableFuture](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html)
- [Guide to CompletableFuture in Baeldung](https://www.baeldung.com/java-completable-future)
- Related: **`Future`**, **`ExecutorService`**, **`Stream` API** — 相关：`Future`、`ExecutorService`、`Stream` API

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (repo root) |
|-------|------------|-----------------|
| CompletableFuture chain | `concurrency.juc.executor.CompletableFutureExample` | `mvn -pl concurrency -q compile` · `java -cp concurrency/target/classes concurrency.juc.executor.CompletableFutureExample` |
| JUC menu | `concurrency.juc.JUCDemoRunner` | `mvn -pl concurrency -q compile exec:java` |

**English README:** https://github.com/zhangze2/awesome-demo/blob/master/concurrency/README.en.md

**Tags**: `技术`, `Java`, `异步编程`, `并发`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Related: Future, ExecutorService, Stream API** — 相关：Future、ExecutorService、Stream API
- **System.out.println("Processing complete");** — thenRunAsync(() -> {                 // Run final action — 执行最终操作
- **CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");** — // Combine two futures — 组合两个 Future
- **CompletableFuture<User> userFuture = getUserAsync(userId);** — // Make multiple API calls in parallel — 并行发起多个 API 调用
- **Recommendations recs = recsFuture.join();** — // Process combined data — 处理组合数据
- **Guide to CompletableFuture in Baeldung** — Related: Future, ExecutorService, Stream API — 相关：Future、ExecutorService、Stream API

### B. 一段串联（连续口语）

**Related: Future, ExecutorService, Stream API. System.out.println("Processing complete");. CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");. CompletableFuture<User> userFuture = getUserAsync(userId);. Recommendations recs = recsFuture.join();. Guide to CompletableFuture in Baeldung.**

**简中：** 相关：Future、ExecutorService、Stream API。thenRunAsync(() -> {                 // Run final action — 执行最终操作。// Combine two futures — 组合两个 Future。// Make multiple API calls in parallel — 并行发起多个 API 调用。// Process combined data — 处理组合数据。Related: Future, ExecutorService, Stream API — 相关：Future、ExecutorService、Stream API。

### C. 一分钟复盘（5 句）

1. **Related: Future, ExecutorService, Stream API** — 相关：Future、ExecutorService、Stream API
2. **System.out.println("Processing complete");** — thenRunAsync(() -> {                 // Run final action — 执行最终操作
3. **CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");** — // Combine two futures — 组合两个 Future
4. **CompletableFuture<User> userFuture = getUserAsync(userId);** — // Make multiple API calls in parallel — 并行发起多个 API 调用
5. **Recommendations recs = recsFuture.join();** — // Process combined data — 处理组合数据

