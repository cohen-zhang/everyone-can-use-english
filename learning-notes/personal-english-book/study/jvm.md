---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
  - jvm
aliases:
  - JVM Runtime Data Areas
  - JVM 运行时数据区
  - JVM 内存地图
---

# JVM Runtime Data Areas — JVM 运行时数据区完全图解

**索引：** [[learning-notes/personal-english-book/README|个人英文材料书索引]]  
**精读版：** [[learning-notes/personal-english-book/study/jvm-internals|JVM Internals · 内部机制]]（类加载、GC 日志、OOM 排查）  
**Demo：** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

一句话：JVM **Runtime Data Areas**（运行时数据区）就是 Java 程序跑起来时，JVM 给它准备的一整套**内存工作空间**。

把 JVM 想成一座大型酒店：

| 区域 `术语` | 酒店类比 | 放什么 |
| --- | --- | --- |
| **Heap**（堆） | 大仓库 | 大量对象 |
| **JVM Stack**（虚拟机栈） | 每个员工自己的办公桌 | 方法调用 / 栈帧 |
| **Method Area / Metaspace**（方法区 / 元空间） | 档案室 | 类的「说明书」 |
| **PC Register**（程序计数器） | 下一步工作便签 | 下一条指令位置 |
| **Native Method Stack**（本地方法栈） | Native / C/C++ 工作台 | JNI 调用 |

---

## 1. 总览 — Shared vs Per-Thread

理解 JVM 内存，先分清：**哪些是所有线程共享的？哪些是每个线程自己的？**

```text
                         JVM Runtime Data Areas
                         JVM 运行时数据区
                                  │
             ┌────────────────────┴────────────────────┐
             │                                         │
       Shared / 共享区域                         Per-Thread / 线程私有
             │                                         │
    ┌────────┴─────────┐              ┌───────────────┼───────────────┐
    │                  │              │               │               │
    ▼                  ▼              ▼               ▼               ▼
┌───────────┐    ┌──────────────┐  ┌────────┐   ┌────────────┐  ┌──────────────┐
│   Heap    │    │ Method Area  │  │   PC   │   │ JVM Stack  │  │ Native Method│
│   堆      │    │   方法区      │  │Register│   │    栈       │  │     Stack    │
│ Objects   │    │ Class Meta   │  │程序计数器│   │ Stack Frame│  │   本地方法栈  │
│ 对象      │    │ Constant Pool│  │ Next   │   │ Local Var  │  │ JNI / Native │
│ GC 重点   │    │ 运行时常量池  │  │ Instr. │   │ Operand    │  │ C/C++        │
└───────────┘    └──────────────┘  └────────┘   └────────────┘  └──────────────┘
```

```text
                    JVM Process
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
   Shared Memory                    Thread Private
    共享内存                         线程私有内存
        │                                 │
   ┌────┴─────┐                 ┌─────────┼─────────┐
   │          │                 │         │         │
   ▼          ▼                 ▼         ▼         ▼
 Heap     Method Area           PC      JVM Stack  Native Stack
 堆        方法区              程序计数器   虚拟机栈    本地方法栈
   │          │
   └────┬─────┘
        │
     GC 主要关注 — Garbage Collection
```

### Shared — 共享区域

**Heap（堆）** — 所有 Java 线程共享。绝大多数 `new` 出来的对象都住在这里。**Garbage Collector**（垃圾收集器）主要在这里干活。

```java
new Object()
new String()
new User()
new byte[1024]
```

**Method Area（方法区）** — 所有线程共享。保存与 **Class** 有关的信息：

- **Class Metadata** — 类元数据
- 方法 / 字段信息
- **Runtime Constant Pool** — 运行时常量池
- 类结构

在现代 **HotSpot** 里，方法区的主要实现是 **Metaspace**（元空间）。

### Per-Thread — 线程私有

每创建一个 Java **Thread**，JVM 都给它准备自己的运行空间：

```text
                    JVM
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       Thread-1   Thread-2   Thread-3
          │          │          │
     ┌────┼────┐ ┌───┼────┐ ┌───┼────┐
     │    │    │ │   │    │ │   │    │
     PC  Stack Native PC Stack Native PC Stack Native
```

一个线程的 **Stack** 出问题，不等于整个 JVM 的 **Heap** 出问题。所以会看到两种完全不同的「内存错误」：

- `StackOverflowError` — 栈太深
- `OutOfMemoryError` — 堆 / 元空间装不下

---

## 2. Heap — 堆

### 2.1 干什么？

Heap = JVM 的大型 **Object Warehouse**（对象仓库）。

```java
User user = new User();
```

```text
                 Heap
                  │
                  ▼
          ┌────────────────┐
          │   User Object  │
          │ name = "Tom"   │
          │ age  = 18      │
          └────────────────┘
                  ▲
                  │ reference（引用）
            JVM Stack
                  │
                  ▼
              user
```

**变量 `user` 和 `User` 对象不是同一个东西。** `user` 通常保存的是对 Heap 中对象的 **reference**（引用）。

### 2.2 内部世界 — 分代

经典逻辑模型（思想，不是所有现代 GC 的物理布局）：

```text
                         Heap
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
       Young Generation          Old Generation
          新生代                    老年代
             │
       ┌─────┼─────┐
       │     │     │
       ▼     ▼     ▼
     Eden   S0     S1
     伊甸园  Survivor  Survivor
```

| 区域 | 简中 | 谁住这儿 |
| --- | --- | --- |
| **Eden** | 伊甸园 | 新对象出生 |
| **Survivor** (S0 / S1) | 幸存者区 | 活过一轮 GC 的对象 |
| **Old Generation** | 老年代 | 长期存活对象 |

G1 / ZGC / Shenandoah 内部实现各不相同。先理解**对象生命周期**和 **GC** 思想，再死记物理布局。

### 2.3 Object Lifecycle — 对象的一生

```java
User user = new User();
```

```text
             Java Code
                 │  new User()
                 ▼
             ┌─────────┐
             │   Eden  │  新生对象
             └────┬────┘
                  │ Minor GC
          ┌───────┴───────┐
          ▼               ▼
       死对象           活对象
      Garbage          Survives
          │               │
          ▼               ▼
       被回收          Survivor
                          │ 多次 GC
                          ▼
                    Old Generation
                         老年代
```

短命对象很多，长期对象比较少。GC 重点优化的就是：**大量对象很快死亡**。

---

## 3. JVM Stack — 虚拟机栈

Heap 是大仓库；**Stack** 是每个线程自己的办公桌。每个线程拥有自己的 JVM Stack。

```text
Thread-1
   │
   ▼
┌────────────────────────┐
│ JVM Stack              │
│ ┌────────────────────┐ │
│ │ main() Stack Frame │ │
│ ├────────────────────┤ │
│ │ calculate() Frame  │ │
│ ├────────────────────┤ │
│ │ test() Frame       │ │
│ └────────────────────┘ │
└────────────────────────┘
```

### 3.1 Stack Frame — 栈帧

每调用一个方法，就往 Stack 上压一个新 **Frame**（栈帧）。返回时弹出。特点：**LIFO**（Last In First Out，后进先出）。

```text
       Stack
        │
        ▼
┌──────────────────┐
│ bar() Frame      │  ← 当前正在执行
├──────────────────┤
│ foo() Frame      │
├──────────────────┤
│ main() Frame     │
└──────────────────┘
```

`bar()` 返回后：

```text
┌──────────────────┐
│ foo() Frame      │  ← 当前
├──────────────────┤
│ main() Frame     │
└──────────────────┘
```

### 3.2 栈帧里有什么？

```text
Stack Frame
├── Local Variable Table     局部变量表
├── Operand Stack            操作数栈
├── Dynamic Linking          动态连接
└── Method Return Information  方法返回信息
```

### 3.3 Local Variable Table — 局部变量表

```java
public void hello() {
    int age = 18;
    User user = new User();
}
```

```text
Stack Frame
┌────────────────────────────┐
│ Local Variables            │
│ age  ──────────► 18        │
│ user ──────────► Reference │
└────────────────────────────┘
                         │
                         ▼ Heap
                ┌────────────────┐
                │   User Object  │
                └────────────────┘
```

`user` 这个局部变量属于 **Stack Frame**；`User` 对象通常属于 **Heap**。这是最容易混的一点。

### 3.4 Operand Stack — 操作数栈

JVM 执行字节码时，大量计算走操作数栈。例如 `int c = a + b;`：

```text
        Operand Stack
             ┌───┐
             │ b │
             ├───┤
             │ a │
             └───┘
               │ add
               ▼
             ┌───┐
             │a+b│
             └───┘
```

因此 JVM 是一台 **Stack-Based Virtual Machine**（基于栈的虚拟机）。

---

## 4. PC Register — 程序计数器

**PC** = **Program Counter**。意思是：我现在执行到哪一条了？

```text
Java Bytecode
0:  iload_1
1:  iload_2
2:  iadd        ← PC
3:  istore_3
4:  return
```

执行完 `iadd` 后，PC 移到下一条。每个线程都有自己的 PC：保存**当前线程下一条要执行的 JVM 指令位置**。

### 为什么必须线程私有？

```text
Thread A                  Thread B
PC → instruction 100      PC → instruction 500
```

如果共享同一个 PC，JVM 就不知道下一步该跑 A 还是 B。所以：**每个线程必须有自己的 PC Register。**

---

## 5. Native Method Stack — 本地方法栈

Java 会走到 Native / 操作系统：

```text
Java → JNI → C / C++ → Operating System
```

例如 `System.currentTimeMillis()`。Native Method Stack = 给 **Native Code** 用的工作台。

---

## 6. Method Area — 方法区

Heap 放「具体的人和物品」；Method Area 更像酒店的建筑档案和员工手册。

```text
Class Metadata
├── Class name
├── Parent class
├── Interfaces
├── Fields
├── Methods
├── Method metadata
└── Runtime Constant Pool
```

```java
public class User {
    private String name;
    public void sayHello() {
        System.out.println("Hello");
    }
}
```

这些「类的说明书」属于 **Class Metadata**。

### 6.1 Metaspace — 元空间

Java 8 以后：**PermGen**（永久代）被移除，改由 **Metaspace** 实现 Method Area。

| 词 | 层级 |
| --- | --- |
| **Method Area** | JVM Specification 里的概念 |
| **Metaspace** | HotSpot 对 Method Area 的一种实现 |

不要把两者当成同义词。

### 6.2 Runtime Constant Pool — 运行时常量池

属于 Method Area 的一部分。可以想成 Class 自带的「常量 / 符号索引表」。运行时 JVM 把相关信息放进来。

**它和 String Pool（字符串池）不是一回事。**

### 6.3 String Pool ≠ Runtime Constant Pool

```text
Runtime Constant Pool
运行时常量池
        │
        ├── 各种常量
        ├── 符号引用
        └── 字符串相关信息
                 │
                 ▼
          String Intern Pool
          字符串驻留池
```

```java
String a = "hello";
String b = "hello";           // 可共享同一驻留对象
String c = new String("hello"); // 通常再 new 一个对象
```

```text
a ─────────────► "hello"   ← String Pool
b ─────────────┘
c ─────────────► "hello"   ← new String Object
```

**String Pool、Heap、Runtime Constant Pool 要分开记。** 字面量 intern 细节见 [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础 · String 常量池]]。

---

## 7. 一段代码在内存里怎么走

```java
public class Demo {
    public static void main(String[] args) {
        int age = 18;
        User user = new User();
        user.setAge(age);
    }
}
```

```text
                     JVM
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
    Method Area      Heap         Thread
    Class Metadata   Objects      JVM Stack
                                     │
                              ┌──────┴──────┐
                              │ main() Frame│
                              │ age = 18    │
                              │ user ───────┼──► User Object
                              └─────────────┘
```

### 从源码到内存

```text
Java Source Code
       │ javac
       ▼
   .class / Bytecode
       │ Class Loader（类加载器）
       ▼
   Runtime Data Areas
       ├── Heap
       ├── Method Area
       ├── JVM Stack
       ├── PC Register
       └── Native Method Stack
                    │
                    ▼
              Execution Engine
                 执行引擎
                    │
                    ▼
               CPU / OS
```

---

## 8. JVM 内存地图（总图）

```text
┌─────────────────────────────────────────────────────────────┐
│                         JVM Process                         │
│                         JVM 进程                            │
│                                                             │
│   SHARED / 线程共享                                         │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                    HEAP / 堆                         │   │
│   │   Objects / 对象                                    │   │
│   │   Young Generation        Old Generation             │   │
│   │   新生代                  老年代                     │   │
│   │   ┌───────┬──────┐                                  │   │
│   │   │ Eden  │ S0/S1│           GC / 垃圾回收           │   │
│   │   └───────┴──────┘                                  │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │          METHOD AREA / 方法区                       │   │
│   │   Class Metadata / 类元数据                         │   │
│   │   Runtime Constant Pool / 运行时常量池              │   │
│   │   HotSpot → Metaspace / 元空间                      │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   THREAD-PRIVATE / 每线程私有                               │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│   │ Thread A   │  │ Thread B   │  │ Thread C   │           │
│   │ PC         │  │ PC         │  │ PC         │           │
│   │ JVM Stack  │  │ JVM Stack  │  │ JVM Stack  │           │
│   │ Native     │  │ Native     │  │ Native     │           │
│   │ Method Stack│  │ Method Stack│ │ Method Stack│          │
│   └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 五大区域速记表

| Area | 中文 | Shared? | 主要内容 | 生命周期 |
| --- | --- | --- | --- | --- |
| **Heap** | 堆 | 是 | Java Objects | JVM |
| **Method Area** | 方法区 | 是 | Class Metadata | JVM |
| **Metaspace** | 元空间 | 是 | HotSpot 对方法区的实现 | JVM |
| **JVM Stack** | 虚拟机栈 | 否 | Stack Frames | Thread |
| **PC Register** | 程序计数器 | 否 | 当前 / 下一条指令 | Thread |
| **Native Method Stack** | 本地方法栈 | 否 | Native Method 执行 | Thread |

---

## 9. 故障地图 — 哪里会炸

```text
                    JVM Memory
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
      Heap             Stack             Metaspace
       │                 │                  │
OutOfMemoryError   StackOverflowError   OutOfMemoryError
Java heap space                         Metaspace
```

### Heap 爆了 — `OutOfMemoryError: Java heap space`

```java
List<byte[]> list = new ArrayList<>();
while (true) {
    list.add(new byte[1024 * 1024]);
}
```

仓库塞满了，GC 也腾不出足够空间。

### Stack 爆了 — `StackOverflowError`

```java
void test() {
    test();  // unbounded recursion — 无限递归
}
```

这个线程的办公桌已经堆满了调用记录。

### Metaspace 爆了 — `OutOfMemoryError: Metaspace`

不断产生大量 Class / ClassLoader 且无法释放 → 类档案室装不下更多 Class Metadata。

生产排查步骤见 [[learning-notes/personal-english-book/study/jvm-internals#5-outofmemoryerror--heap-dumps--oom-与堆转储|JVM Internals · OOM 与堆转储]]。

---

## 10. GC 到底管谁？

```text
                 Garbage Collector
                        │
                        ▼
                      Heap
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
       Dead Objects            Live Objects
        死亡对象                  存活对象
            │                       │
          回收                    保留
```

GC 问的不是「这块内存有没有变量？」，而是：**这个对象从 GC Roots 出发，还能不能被访问到？**

### GC Roots — 垃圾回收的起点

想象：还有没有人「认识」这个对象？

```text
GC Root
  │
  ▼
Stack Local Variable
  │
  ▼
User Object
  │
  ▼
Address Object
```

能从 GC Roots 走到的对象是 **Reachable**（可达），通常不能当垃圾。走不到就是 **unreachable**，有资格被回收。

---

## 11. 变量 ≠ 对象

```java
User user = new User();
```

不要想成 `Stack = User`。更准确：

```text
Stack
┌───────────────┐
│ user          │
└─────┬─────────┘
      │ reference
      ▼
Heap
┌────────────────┐
│ User Object    │
│ name / age     │
└────────────────┘
```

Stack 主要保存方法执行数据；Object 通常在 Heap。

例外：JIT 可能通过 **Escape Analysis**（逃逸分析）和 **Scalar Replacement**（标量替换），让某些对象不必以完整对象形式存在于堆中。

---

## 12. 一个线程运行时的完整画面

```java
public static void main(String[] args) {
    User user = new User();
    foo(user);
}
static void foo(User user) {
    int age = 18;
}
```

```text
                         JVM
                          │
         ┌────────────────┼─────────────────┐
         │                │                 │
         ▼                ▼                 ▼
   Method Area           Heap          Main Thread
    User.class            │          PC + Stack
                          │
                     ┌────┴────┐
                     │ foo()   │
                     │ age=18  │
                     │ user ───┼──┐
                     ├─────────┤  │
                     │ main()  │  │
                     │ user ───┼──┤
                     └─────────┘  │
                                  ▼
                             User Object
```

这就是 Java 程序运行时内存世界的核心。

---

## 13. 最容易混淆的几组概念

### Heap vs Stack

| | Heap | Stack |
| --- | --- | --- |
| 放什么 | **Objects**（对象） | **Method Frames**（方法调用） |
| 一句话 | 对象主要在 Heap | 方法调用主要在 Stack |

### Method Area vs Metaspace

```text
JVM Specification
       │
       ▼
Method Area          ← 规范概念
       │
       ▼
HotSpot Implementation
       │
       ▼
Metaspace            ← HotSpot 实现
```

### Runtime Constant Pool vs String Pool

| | 归属 |
| --- | --- |
| **Runtime Constant Pool** | Class / Method Area 体系 |
| **String Pool** | JVM 对字符串驻留的运行时机制 |

### JVM Memory vs Physical RAM

JVM 看到的是 **JVM Memory**；操作系统看到的是 **Process Virtual Memory**（进程虚拟内存）；机器看到的是 **Physical Memory / RAM**。

**Heap Size ≠ Java 进程实际占用的全部物理内存。** 一个 JVM 进程还可能吃：

- Heap
- Metaspace
- Thread Stacks
- **Code Cache**
- **Direct Buffers**
- GC 数据结构 / JVM 自身 / Native Memory

所以 `-Xmx 4G` **并不意味着** Java 进程最多只占 4 GB。这是生产排查时非常重要的一点。

---

## 14. 生产排查地图

进程内存往上走时，不要第一反应「Heap 太大？」先拆：

```text
              Java Process
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
     Heap      Metaspace    Native Memory
       │           │           │
    Objects      Classes     Threads / Stack
    对象         类元数据      Direct Buffer
                              Code Cache
```

---

## 15. Cheat Sheet — 速记总图

```text
                 JVM Runtime Data Areas
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
     SHARED                              THREAD-PRIVATE
      共享                                  线程私有
   ┌────┴────┐                    ┌───────────┼───────────┐
   ▼         ▼                    ▼           ▼           ▼
 Heap    Method Area              PC       JVM Stack   Native Stack
 Objects  Class Metadata      Next Instr.  Stack Frame  Native Code
          ├── Runtime Constant Pool
          └── HotSpot → Metaspace
 Heap ├── Young: Eden + Survivor
      └── Old Generation → GC
```

---

## 16. 最终记忆口诀

| 口诀 | English |
| --- | --- |
| Heap 放对象 | Objects live primarily in the **Heap**. |
| Stack 管方法调用 | Each thread has its own **JVM Stack** and **Stack Frames**. |
| PC 记下一步 | **PC Register** tracks the current execution position. |
| Method Area 放 Class 说明书 | **Method Area** stores class-related metadata. |
| Metaspace 是 HotSpot 实现 | **Metaspace** is HotSpot’s main implementation of the Method Area. |
| Native Stack 服务 Native Code | **Native Method Stack** supports native method execution. |

公司类比：

```text
                         JVM 公司
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
     Heap                Method Area          Threads
      仓库                  档案室               员工
    存对象                存 Class 信息     每人自己的工作区
                                                │
                                    ┌───────────┼───────────┐
                                    ▼           ▼           ▼
                                   PC        Stack       Native Stack
                                 下一步       办公桌       Native 工作台
        ▼
      Garbage Collector — 垃圾回收员
        清理没人要的对象
```

城市地图：

| 符号 | 是什么 |
| --- | --- |
| Heap | 仓库 / 城市里的建筑和物品 |
| Method Area | 城市档案馆 |
| JVM Stack | 每个线程自己的办公桌 |
| PC Register | 工作人员手里的下一步指令 |
| Native Method Stack | Native 工程师的专用工作台 |
| GC | 城市清洁工 |
| GC Roots | 仍然「认识」某个对象的人 |
| Heap OOM | 仓库爆满 |
| StackOverflowError | 办公桌上的调用记录堆爆了 |
| Metaspace OOM | 档案室塞满了 Class 信息 |

先把这张地图记住，再学 GC、JMM、类加载、JIT、对象创建、内存泄漏、OOM、Direct Memory，会容易很多。

---

## Further Reading — 延伸阅读

- [[learning-notes/personal-english-book/study/jvm-internals|JVM Internals · 内部机制]] — 类加载、GC 日志、常用参数
- [[learning-notes/personal-english-book/study/java-joke-Jeff-Dean|Java Facts · Jeff Dean 风格]] — Young Gen / Full GC / OOM 梗
- [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] — String intern / 常量池
- [[learning-notes/personal-english-book/study/java-concurrency|并发编程]] — 线程与栈
- [The Java Virtual Machine Specification](https://docs.oracle.com/javase/specs/jvms/se17/html/)
- [Baeldung: JVM Memory Model](https://www.baeldung.com/java-jvm-memory-model)

**Tags**: `技术`, `Java`, `JVM`, `堆`, `栈`, `GC`
