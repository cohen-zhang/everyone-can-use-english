---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
aliases:
  - Java Fundamentals
  - Java 基础
---

# Java Fundamentals — Java 基础

Java is a **statically typed**, **object-oriented** language that compiles to **bytecode** and runs on the JVM. This note covers the language core: data types, the String pool, references, and dynamic proxies.

Java 是一门**静态类型**、**面向对象**的语言，编译为**字节码**并在 JVM 上运行。本文涵盖语言核心：数据类型、String 常量池、引用与动态代理。

**Demo bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

**Demo repo:** https://github.com/zhangze2/awesome-demo/tree/master/java-base · **Local sibling:** `../awesome-java-demo/java-base/`

---

## Overview — 概述

### Language Basics — 语言基础

Java programs are organized into **classes**. Every value has a **type** known at compile time, which enables early error detection and better tooling.

Java 程序由**类**组织。每个值在编译期都有确定的**类型**，这使错误能尽早暴露、工具链更强大。

### Key Principles — 核心原则

1. **Write once, run anywhere** — 一次编写，到处运行（字节码 + JVM）
2. **Statically typed** — 静态类型（编译期检查）
3. **Object-oriented** — 面向对象（封装、继承、多态）
4. **Automatic memory management** — 自动内存管理（GC，见 [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]]）

---

## Core Concepts — 核心概念

### 1. Primitive Types & Wrappers — 基本类型与包装类

Java has **8 primitive types** (`int`, `long`, `double`, `boolean`, ...) that are stored **by value**, and **wrapper classes** (`Integer`, `Long`, ...) that are objects. **Autoboxing** converts between them automatically.

Java 有 **8 种基本类型**（`int`、`long`、`double`、`boolean` 等），按**值**存储；**包装类**（`Integer`、`Long` 等）是对象。**自动装箱**在两者之间自动转换。

```java
int primitive = 42;              // Stored by value — 按值存储
Integer boxed = primitive;       // Autoboxing — 自动装箱
int back = boxed;                // Unboxing — 拆箱
```

**Pitfall — 注意**: `Integer` can be `null`; unboxing `null` throws `NullPointerException` — 包装类可为 `null`，拆箱时抛 NPE。

### 2. String & the Constant Pool — String 与常量池

`String` is **immutable**. Literals live in the **string constant pool**, so `"a" == "a"` is true, while `new String("a")` creates a distinct object on the heap.

`String` 是**不可变**的。字面量存放在**字符串常量池**，故 `"a" == "a"` 为真，而 `new String("a")` 会在堆上创建独立对象。

```java
String a = "hello";
String b = "hello";
String c = new String("hello");
System.out.println(a == b);          // true — same pooled object — 同一池化对象
System.out.println(a == c);          // false — different object — 不同对象
System.out.println(a.equals(c));     // true — same content — 内容相同
System.out.println(a == c.intern()); // true — canonical representation — 规范表示
```

**Official**: `String.intern()` returns "a **canonical representation** for the string object." — 官方：返回该字符串对象的**规范表示**。

### 3. Reference Types — 引用类型

Beyond strong references, Java provides **SoftReference**, **WeakReference**, and **PhantomReference** for memory-sensitive caching and cleanup hooks.

除强引用外，Java 还提供**软引用**、**弱引用**、**虚引用**，用于内存敏感缓存与清理钩子。

- **Strong** — keeps the object alive — 阻止对象被回收
- **Soft** — collected only when memory is low — 内存不足时才回收（适合缓存）
- **Weak** — collected at the next GC — 下次 GC 即回收（`WeakHashMap`）

### 4. JDK Dynamic Proxy — JDK 动态代理

`Proxy.newProxyInstance` creates a runtime class implementing given **interfaces**; every method call is routed through an `InvocationHandler`. This powers AOP, RPC stubs, and mocking frameworks.

`Proxy.newProxyInstance` 在运行时生成实现指定**接口**的类；所有方法调用经由 `InvocationHandler` 转发。这是 AOP、RPC 桩与 Mock 框架的基础。

```java
Object proxy = Proxy.newProxyInstance(
    loader,                        // ClassLoader — 类加载器
    new Class<?>[]{Service.class}, // Interfaces — 接口
    (obj, method, args) -> {       // InvocationHandler — 调用处理器
        System.out.println("before " + method.getName());
        return method.invoke(target, args);
    });
```

**Limitation — 局限**: interfaces only; for concrete classes use CGLIB / ByteBuddy — 只能代理接口；代理具体类需 CGLIB / ByteBuddy。

**See also**: [[learning-notes/personal-english-book/study/spring-framework-notes|Spring Framework]] — Spring AOP 同样基于 JDK / CGLIB 代理。

### 5. Fail-fast Iterators — 快速失败迭代器

Iterators returned by `ArrayList` are **fail-fast**: modifying the collection structurally during iteration (outside the iterator's own methods) throws `ConcurrentModificationException`.

`ArrayList` 返回的迭代器是**快速失败**的：迭代期间对集合做结构性修改（不经迭代器自身方法）会抛 `ConcurrentModificationException`。

**See also**: [[learning-notes/personal-english-book/study/java-collections-framework|Java Collections Framework]] — 详见集合框架笔记。

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Statically typed** | /ˈstætɪkli taɪpt/ | 静态类型的 | Types are checked at compile time |
| **Bytecode** | /ˈbaɪtkoʊd/ | 字节码 | Intermediate code executed by the JVM |
| **Primitive** | /ˈprɪmətɪv/ | 基本类型 | A built-in value type stored directly, e.g. `int` |
| **Wrapper** | /ˈræpər/ | 包装类 | An object class wrapping a primitive, e.g. `Integer` |
| **Autoboxing** | /ˌɔːtoʊˈbɑːksɪŋ/ | 自动装箱 | Automatic conversion from primitive to wrapper |
| **Immutable** | /ɪˈmjuːtəbəl/ | 不可变的 | Cannot be changed once created |
| **Constant pool** | /ˈkɑːnstənt puːl/ | 常量池 | A cache of literals and constants per class / runtime |
| **Canonical** | /kəˈnɑːnɪkəl/ | 规范的 | The single standard form of an object |
| **Reference** | /ˈrefrəns/ | 引用 | A handle to an object on the heap |
| **Proxy** | /ˈprɑːksi/ | 代理 | An object standing in for another, intercepting calls |
| **Invocation handler** | /ˌɪnvəˈkeɪʃən ˈhændlər/ | 调用处理器 | Receives every method call on a dynamic proxy |
| **Interface** | /ˈɪntərfeɪs/ | 接口 | A contract of abstract methods a class can implement |
| **Fail-fast** | /feɪl fæst/ | 快速失败 | Detecting misuse immediately by throwing an exception |
| **Heap** | /hiːp/ | 堆 | The runtime memory area where objects live |
| **Encapsulation** | /ɪnˌkæpsəˈleɪʃən/ | 封装 | Hiding internal state behind methods |
| **Inheritance** | /ɪnˈherɪtəns/ | 继承 | A class reusing and extending a parent class |

---

## Common Interview Questions — 常见面试问题

### Q: Why is String immutable?

**A**: Immutability makes String **thread-safe**, allows the **constant pool** to share literals safely, and lets the cached **hash code** be reused (crucial for `HashMap` keys).

不可变性使 String **线程安全**、让**常量池**能安全共享字面量，并可缓存**哈希码**复用（对 `HashMap` 键至关重要）。

### Q: `==` vs `equals()` — what's the difference?

**A**: `==` compares **references** (identity); `equals()` compares **content** (equality) if overridden. Always use `equals()` for objects unless you truly mean identity.

`==` 比较**引用**（同一性）；`equals()` 在被重写后比较**内容**（相等性）。对象比较一律用 `equals()`，除非确实要判同一。

### Q: When does autoboxing cause problems?

**A**: (1) Unboxing `null` throws NPE; (2) in loops, repeated boxing/unboxing adds allocation overhead; (3) `Integer` cache surprises: `Integer.valueOf(127) == Integer.valueOf(127)` but not for `128`.

（1）拆箱 `null` 抛 NPE；（2）循环中反复装箱/拆箱带来分配开销；（3）`Integer` 缓存陷阱：127 内 `==` 成立，128 起不成立。

### Q: What can a JDK dynamic proxy not do?

**A**: It can only proxy **interfaces**. Classes need bytecode-level tools like CGLIB or ByteBuddy. Also, `final` methods cannot be intercepted.

只能代理**接口**。代理类需要 CGLIB、ByteBuddy 等字节码工具；`final` 方法也无法被拦截。

---

## Further Reading — 延伸阅读

- [The Java Language Specification](https://docs.oracle.com/javase/specs/)
- [Baeldung: Java String Pool](https://www.baeldung.com/java-string-pool)
- [Baeldung: Dynamic Proxies in Java](https://www.baeldung.com/java-dynamic-proxies)
- Related: [[learning-notes/personal-english-book/study/java-collections-framework|Collections Framework]] · [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]] · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/spring-framework-notes|Spring Framework]]
- Source README (demo): https://github.com/zhangze2/awesome-demo/blob/master/java-base/README.en.md

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (demo repo root) |
|-------|------------|----------------------|
| String intern / pool | `string.StringInternExample` | `mvn -pl java-base -q compile` · `java -cp java-base/target/classes string.StringInternExample` |
| JDK dynamic proxy | `proxy.JdkDynamicProxy` | `java -cp java-base/target/classes proxy.JdkDynamicProxy` |
| Fail-fast iterator | `collection.ArrayListFailFastExample` | `java -cp java-base/target/classes collection.ArrayListFailFastExample` |
| HashMap basics | `HashMapTest` | `java -cp java-base/target/classes HashMapTest` |

**English README (demo):** https://github.com/zhangze2/awesome-demo/blob/master/java-base/README.en.md

**Tags**: `技术`, `Java`, `基础`, `面向对象`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Java is statically typed and object-oriented.** — Java 是静态类型、面向对象的。
- **String literals live in the constant pool.** — 字符串字面量存放在常量池中。
- **Use equals, never ==, for object content.** — 比较对象内容用 equals，不要用 ==。
- **A dynamic proxy routes calls through a handler.** — 动态代理把调用路由到处理器。
- **Fail-fast iterators detect structural changes.** — 快速失败迭代器能发现结构性修改。

### B. 一段串联（连续口语）

**Java is statically typed and object-oriented. String literals live in the constant pool. Use equals, never ==, for object content. A dynamic proxy routes calls through a handler. Fail-fast iterators detect structural changes.**

**简中：** Java 是静态类型、面向对象的。字符串字面量存放在常量池中。比较对象内容用 equals，不要用 ==。动态代理把调用路由到处理器。快速失败迭代器能发现结构性修改。

### C. 一分钟复盘（5 句）

1. **Java is statically typed and object-oriented.** — Java 是静态类型、面向对象的。
2. **String literals live in the constant pool.** — 字符串字面量存放在常量池中。
3. **Use equals, never ==, for object content.** — 比较对象内容用 equals，不要用 ==。
4. **A dynamic proxy routes calls through a handler.** — 动态代理把调用路由到处理器。
5. **Fail-fast iterators detect structural changes.** — 快速失败迭代器能发现结构性修改。
