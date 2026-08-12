---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
aliases:
  - Java Keywords
  - Java 关键字
---

# Java Keywords — Java 关键字

A **keyword** is a reserved word with a fixed meaning. You cannot use it as a class, method, or variable name. This note groups the classic keywords, unused reserved words, and newer **contextual keywords**.

**关键字**是有固定含义的保留词。不能拿它当类名、方法名或变量名。本文按组梳理经典关键字、未使用的保留字，以及较新的**上下文关键字**。

**Index:** [[learning-notes/personal-english-book/README|个人英文材料书索引]]  
**Related:** [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]]（8 种基本类型都是关键字） · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/java-concurrency|并发编程]]

---

## Overview — 概述

### Keyword vs identifier — 关键字 vs 标识符

An **identifier** is a name you invent (`orderId`, `AccountService`). A **keyword** is a name the language already owns (`class`, `return`, `if`).

**标识符**是你起的名字；**关键字**是语言已经占用的名字。

`true`, `false`, and `null` are **reserved literals**, not keywords in the JLS — but you still cannot reuse them. — `true` / `false` / `null` 在规范里是**保留字面量**，不是关键字，但同样不能当名字用。

### Key Principles — 核心原则

1. **Don't fight the compiler** — 不要用关键字当标识符；IDE 会标红
2. **Access first, then meaning** — 先分清 `public` / `private` / `protected`，再记控制流
3. **Contextual ≠ free** — `var` / `record` / `sealed` 在特定位置仍是保留的 — 上下文关键字在特定语法位置仍不能乱写
4. **`const` and `goto` are traps** — 保留但未实现；常量用 `final`，不要写 `goto`

---

## 1. Primitive type keywords — 基本类型关键字

These eight words **are** the primitive types. Full sizes and wrappers: [[learning-notes/personal-english-book/study/java-fundamentals#1-primitive-types--wrappers--基本类型与包装类|Java 基础 · 基本类型表]].

这八个词**就是**基本类型。位数与包装类见基础笔记表格。

| Keyword `术语` | 简中 | Spoken hook — 口语钩子 |
| --- | --- | --- |
| **`byte`** | 字节型 | A tiny integer. — 很小的整数。 |
| **`short`** | 短整型 | Sixteen bits. Rare in APIs. — 16 位，API 里少见。 |
| **`int`** | 整型 | The default whole number. — 默认整数。 |
| **`long`** | 长整型 | Use `L`. Think timestamps. — 加 `L`；常用于时间戳。 |
| **`float`** | 单精度浮点 | Use `f`. Prefer `double` unless you must. — 加 `f`；除非必要，优先 `double`。 |
| **`double`** | 双精度浮点 | The default decimal. — 默认小数。 |
| **`char`** | 字符 | One UTF-16 code unit, not a full emoji. — 一个 UTF-16 码元，不等于完整 emoji。 |
| **`boolean`** | 布尔 | Only `true` or `false`. — 只有真或假。 |
| **`void`** | 无返回值 | Not a primitive. Means “returns nothing.” — 不是基本类型，表示「不返回值」。 |

---

## 2. Access & class structure — 访问与类型结构

| Keyword `术语` | 简中 | What it does — 作用 |
| --- | --- | --- |
| **`class`** | 类 | Declares a class. — 声明类。 |
| **`interface`** | 接口 | Declares a contract. — 声明契约。 |
| **`enum`** | 枚举 | A fixed set of named constants. — 一组固定的具名常量。 |
| **`package`** | 包 | Names the namespace. — 声明命名空间。 |
| **`import`** | 导入 | Brings a type into scope. — 把类型引进当前文件。 |
| **`extends`** | 继承 | Class / interface inheritance. — 类或接口继承。 |
| **`implements`** | 实现 | A class takes on an interface. — 类实现接口。 |
| **`public`** | 公有 | Visible everywhere. — 到处可见。 |
| **`protected`** | 受保护 | Package + subclasses. — 同包 + 子类。 |
| **`private`** | 私有 | This class only. — 仅本类。 |
| **`static`** | 静态 | Belongs to the type, not an instance. — 属于类型，不属于实例。 |
| **`final`** | 最终 | No subclass / no override / no reassign. — 不可继承 / 不可重写 / 不可再赋值。 |
| **`abstract`** | 抽象 | Incomplete type or method. — 不完整的类型或方法。 |
| **`native`** | 本地 | Implemented in C/C++ via JNI. — 用 JNI 调 C/C++。 |
| **`strictfp`** | 严格浮点 | Legacy FP rounding (rarely used now). — 遗留浮点舍入（现已少用）。 |

Default (package-private) has **no keyword**. Leave the modifier off. — **默认（包可见）没有关键字**，不写修饰符即可。

```java
public final class AccountService implements Transfer {
    private static final int MAX_RETRY = 3;  // constant — 常量用 final，不是 const
}
```

---

## 3. Object & memory — 对象与内存

| Keyword `术语` | 简中 | Spoken line — 口语 |
| --- | --- | --- |
| **`new`** | 新建 | **Allocate** an object on the heap. — 在堆上分配对象。 |
| **`this`** | 当前对象 | The current instance. — 当前实例。 |
| **`super`** | 父类 | The parent class. — 父类。 |
| **`instanceof`** | 实例判断 | Test runtime type (pattern matching in newer Java). — 判断运行时类型。 |
| **`transient`** | 瞬时 | Skip this field in default serialization. — 默认序列化时跳过该字段。 |
| **`volatile`** | 易变 | Visibility across threads — not a lock. — 跨线程可见性，**不是**锁。见 [[learning-notes/personal-english-book/study/java-concurrency|并发编程]]。 |
| **`synchronized`** | 同步 | Intrinsic lock on a method or block. — 方法或代码块上的内置锁。 |
| **`assert`** | 断言 | Debug check; often off in production. — 调试断言；生产环境常关闭。 |

---

## 4. Control flow — 控制流

| Keyword `术语` | 简中 | Note — 备注 |
| --- | --- | --- |
| **`if` / `else`** | 如果 / 否则 | Branch. — 分支。 |
| **`switch` / `case` / `default`** | 选择 / 分支 / 默认 | Also used in switch expressions. — 也用于 switch 表达式。 |
| **`for` / `while` / `do`** | 循环 | `do` always runs once. — `do` 至少执行一次。 |
| **`break` / `continue`** | 跳出 / 继续 | Leave or skip one iteration. — 离开或跳过本轮。 |
| **`return`** | 返回 | Exit the method. — 退出方法。 |

---

## 5. Exceptions — 异常

| Keyword `术语` | 简中 | Pair with — 搭配 |
| --- | --- | --- |
| **`try` / `catch` / `finally`** | 尝试 / 捕获 / 最终 | Cleanup in `finally`; prefer try-with-resources. — 清理放 `finally`；优先 try-with-resources。 |
| **`throw`** | 抛出 | Throw one exception object. — 抛出一个异常对象。 |
| **`throws`** | 声明抛出 | Method signature: checked exceptions. — 方法签名上的受检异常。 |

**See:** [[learning-notes/personal-english-book/study/java-exception-handling|Java 异常处理]]

```java
public void load() throws IOException {   // throws — 声明
    try {
        throw new IOException("boom");    // throw — 抛出
    } catch (IOException e) {
        throw e;
    } finally {
        // always runs — 总会跑
    }
}
```

---

## 6. Unused reserved words — 保留但不用

| Word | Status — 状态 | What to use instead — 改用 |
| --- | --- | --- |
| **`goto`** | Reserved, unused — 保留未实现 | Structured `break` / `return` |
| **`const`** | Reserved, unused — 保留未实现 | **`final`** for constants |

C/C++ muscle memory writes `const int x`. In Java that does not compile. Say **`final int x`**. — 从 C/C++ 带来的 `const` 在 Java 里编不过；常量写 **`final`**。

---

## 7. Contextual keywords (modern Java) — 上下文关键字

These words are reserved **only in certain grammar positions**. Elsewhere they can still be identifiers (until a future JLS tightens them).

这些词只在**特定语法位置**保留。其他地方有时仍能当标识符（未来规范可能收紧）。

| Keyword `术语` | Since | 简中 | Use — 用法 |
| --- | --- | --- | --- |
| **`var`** | 10 | 局部类型推断 | Local variables only. Not a field type. — 仅局部变量，不能当字段类型。 |
| **`yield`** | 14 | switch 产出值 | Switch expressions. — switch 表达式返回值。 |
| **`record`** | 16 | 记录类 | Immutable data carrier. — 不可变数据载体。 |
| **`sealed` / `permits` / `non-sealed`** | 17 | 密封 / 允许 / 非密封 | Restrict subclasses. — 限制谁能继承。 |
| **`when`** | 21 | 模式守卫 | Pattern matching guard. — 模式匹配条件。 |
| **`_`** | 9 / 22 | 未命名 | Java 9: cannot be an identifier. Java 22: unnamed variable. — 9 起不能当名字；22 起作未命名变量。 |

Module-info extras (less common in app code): `module`, `requires`, `exports`, `opens`, `provides`, `uses`, `to`, `with`, `transitive`, `open`. — `module-info.java` 里还有一组模块关键字，业务代码里少见。

```java
var list = new ArrayList<String>();          // var — 局部推断

record Money(String currency, long cents) {} // record — 数据载体

sealed interface Result permits Ok, Err {}   // sealed — 密封层级

int value = switch (status) {
    case 200 -> 1;
    default -> {
        yield 0;                             // yield — 产出
    }
};
```

---

## 8. Interview English — 面试口语

- **A keyword is reserved by the language.** — 关键字是语言保留的。
- **You can't use it as an identifier.** — 不能拿它当标识符。
- **Java has eight primitive type keywords.** — Java 有八个基本类型关键字。
- **`const` is reserved but unused; we write `final`.** — `const` 保留但不用，我们写 `final`。
- **`var` is contextual. It only works for locals.** — `var` 是上下文的，只用于局部变量。
- **`volatile` gives visibility, not mutual exclusion.** — `volatile` 给可见性，不给互斥。

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Keyword** | /ˈkiːwɜːrd/ | 关键字 | A reserved word with language meaning |
| **Reserved word** | /rɪˈzɜːrvd wɜːrd/ | 保留字 | A word you must not reuse as a name |
| **Identifier** | /aɪˈdentɪfaɪər/ | 标识符 | A name you choose for a type, method, or variable |
| **Literal** | /ˈlɪtərəl/ | 字面量 | A fixed value in source, e.g. `true`, `42`, `"hi"` |
| **Modifier** | /ˈmɑːdɪfaɪər/ | 修饰符 | Keywords like `public`, `static`, `final` |
| **Contextual keyword** | /kənˈtekstʃuəl ˈkiːwɜːrd/ | 上下文关键字 | Reserved only in some syntax positions |
| **Access modifier** | /ˈækses ˈmɑːdɪfaɪər/ | 访问修饰符 | `public` / `protected` / `private` |
| **Type inference** | /taɪp ˈɪnfərəns/ | 类型推断 | Compiler guesses the type, as with `var` |
| **Sealed type** | /siːld taɪp/ | 密封类型 | A type that lists allowed subtypes |
| **Unnamed variable** | /ʌnˈneɪmd ˈveriəbl/ | 未命名变量 | `_` when you must not use the value |

---

## Common Interview Questions — 常见面试问题

### Q: Is `true` a keyword?

**A**: No. `true`, `false`, and `null` are **boolean / null literals**. They are still reserved. You cannot name a variable `true`.

不是。它们是**字面量**，但仍被保留，不能当变量名。

### Q: Why doesn't `const` work?

**A**: It is reserved for possible future use. Java constants are **`final`** (and often `static final`).

它被保留以备将来。Java 常量用 **`final`**（常用 `static final`）。

### Q: Can I name a variable `var`?

**A**: Don't. `var` is a **contextual keyword**. In local-variable position it means type inference. Using it as a name just confuses readers and tools.

不要。`var` 是**上下文关键字**。在局部变量位置表示类型推断；拿它当名字只会让人和工具困惑。

### Q: `throw` vs `throws`?

**A**: **`throw`** actually throws an exception object. **`throws`** declares checked exceptions on the method.

**`throw`** 真正抛出异常对象；**`throws`** 在方法上声明受检异常。

---

## Further Reading — 延伸阅读

- [JLS §3.9 Keywords](https://docs.oracle.com/javase/specs/jls/se21/html/jls-3.html#jls-3.9)
- Related: [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/java-concurrency|并发编程]] · [[learning-notes/personal-english-book/study/computer-science-vocab-interesting|有趣计科词汇]]

**Tags**: `技术`, `Java`, `关键字`, `基础`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 先英后对照简中*

### A. 分句场景链

- **A keyword is reserved by the language.** — 关键字是语言保留的。
- **Java has eight primitive type keywords.** — Java 有八个基本类型关键字。
- **You write final, not const.** — 写 final，不写 const。
- **Throw fires an exception; throws declares it.** — throw 抛出异常，throws 声明异常。
- **Var is only for local variables.** — var 只用于局部变量。

### B. 一段串联

**A keyword is reserved by the language. Java has eight primitive type keywords. You write final, not const. Throw fires an exception; throws declares it. Var is only for local variables.**

**简中：** 关键字是语言保留的。Java 有八个基本类型关键字。写 final，不写 const。throw 抛出异常，throws 声明异常。var 只用于局部变量。

### C. 一分钟复盘（5 句）

1. **A keyword is reserved by the language.** — 关键字是语言保留的。
2. **Java has eight primitive type keywords.** — Java 有八个基本类型关键字。
3. **You write final, not const.** — 写 final，不写 const。
4. **Throw fires an exception; throws declares it.** — throw 抛出异常，throws 声明异常。
5. **Var is only for local variables.** — var 只用于局部变量。
