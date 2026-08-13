---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
  - humor
aliases:
  - Java Facts Jeff Dean Style
  - 关于 Java 你可能不知道的事实
  - java-joke
---

# Java Facts, Jeff Dean Style — 关于 Java，你可能不知道的事实

This note keeps the **Jeff Dean Facts** rhythm: deadpan, one beat per line. The setup sounds like ordinary Java. The punchline breaks a JVM law.

本文保持 Jeff Dean Facts 的节奏：一本正经、每条一句。前半句符合 Java 常识，后半句违反 JVM 定律。

**索引：** [[learning-notes/personal-english-book/README|个人英文材料书索引]]  
**Related:** [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]] · [[learning-notes/personal-english-book/study/jvm|JVM 运行时数据区]] · [[learning-notes/personal-english-book/study/java-concurrency|并发编程]] · [[learning-notes/personal-english-book/study/java-collections-framework|Collections]] · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/spring-framework-notes|Spring]] · [[learning-notes/personal-english-book/study/completablefuture-java-guide|CompletableFuture]]

If you write Java for a living, most of these should land: they tease **JVM**, **GC**, **JIT**, **Spring**, concurrency, generics, and Maven — the same style as the original Jeff Dean Facts.

写 Java 的人看完基本都会会心一笑：几乎每一条都在拿这些经典知识点开玩笑。

---

## How to read — 怎么读

| 行 | 作用 |
| --- | --- |
| **加粗英文** + 简中 | 铺垫（听起来像常识） |
| `>` 引用 | 包袱（常识被拆掉） |
| 无引用的单行 | 一句打完，不再补刀 |

English is the line to say out loud. 简中 is the gloss.

英文是跟读句；简中是对照。

### Topic map — 主题速查

| Topic — 主题 | Facts |
| --- | --- |
| JVM / JIT / ClassLoader | 1–4, 16–17, 40–45, 96–99 |
| Heap & GC — 堆与垃圾回收 | 5–7, 38, 46, 78–79, 85–95 |
| Concurrency — 并发 | 8–14 |
| Language & collections — 语言与集合 | 15, 18–23, 49–61 |
| Spring & ORM | 24–29 |
| Toolchain, quality, IDE — 构建与质量 | 30–36, 68–75 |
| Exceptions, debug, production — 异常与生产 | 37, 39, 47–48, 62–67 |
| Containers & observability — 容器与可观测 | 76–77, 80–84 |
| The closer — 终章 | [100](#100-the-closer--终章) |

---

## Facts 1–10

1. **Java never throws exceptions.** — Java 不会抛出异常。
   > Exceptions apologize to Java. — 异常会向 Java 道歉。

2. **Before the JVM starts, it checks which version he wants to use today.** — JVM 启动前，会先确认他今天想用哪个版本。

3. **His code never needs JIT.** — 他写的代码不需要 JIT。
   > The CPU just learns his coding style. — CPU 会主动学习他的编码风格。

4. **The name HotSpot comes from the fact that his code is always hot.** — HotSpot 的名字，就是因为他的代码总是热点。

5. **Objects he creates never enter the Young Generation.** — 他写的对象从来不会进入 Young Gen。
   > They mature the moment they are born. — 因为它们一出生就成熟了。

6. **He doesn't need a garbage collector.** — 他不用垃圾回收器。
   > Garbage collects itself. — 垃圾会自己回收自己。

7. **Full GC never stops the world.** — Full GC 不会 Stop-The-World。
   > The world stops to wait for his threads. — 世界会停下来等他的线程。

8. **His `synchronized` blocks never block.** — 他写 `synchronized`，从来不会阻塞。
   > Other threads simply step aside. — 其他线程都会主动礼让。

9. **He writes `volatile`.** — 他写 `volatile`。
   > The CPU refreshes its cache just to keep up. — CPU 会主动刷新缓存，以免跟不上。

10. **CAS never fails when he uses it.** — CAS 遇到他，从来不会失败。
    > No one dares compete with him. — 因为没人敢和他竞争。

---

## Facts 11–20

11. **His locks never contend.** — 他写的锁没有锁竞争。
    > Even the thread scheduler knows better. — 连线程调度器都知道先来后到。

12. **`ThreadLocal` synchronizes itself.** — `ThreadLocal` 会自动同步。
    > Every thread knows what he really means. — 因为每个线程都知道他真正想表达什么。

13. **He doesn't need `Future`.** — 他不用 `Future`。
    > The future just gives him the result. — Future 会主动告诉他结果。

14. **It's called `CompletableFuture` because his futures are already complete.** — `CompletableFuture` 的名字，就是因为他的任务本来就是 Complete 的。

15. **His recursion never causes `StackOverflowError`.** — 他写递归，从来不会 StackOverflow。
    > The stack expands itself. — 栈会自动扩容。

16. **The JVM warms up just by looking at his code.** — JVM 看见他的代码，会提前预热自己。

17. **The JVM doesn't inline his methods.** — JVM 不会内联他的函数。
    > The entire JVM wants to be inlined into his methods. — 因为整台 JVM 都想内联进去。

18. **He writes Lambdas.** — 他写 Lambda。
    > The bytecode optimizes itself. — 字节码会主动变得更优雅。

19. **Generic type erasure never affects him.** — 泛型擦除不会影响他。
    > Type information comes back when he needs it. — 类型信息会自己回来。

20. **He can instantiate an interface.** — 他可以 `new` 一个接口。

---

## Facts 21–30

21. **He can instantiate an abstract class.** — 他可以实例化抽象类。
    > The abstract class simply realizes it wasn't abstract enough. — 抽象类觉得自己还不够抽象。

22. **`final` doesn't limit him.** — `final` 修饰不了他。
    > He is `final`. — 他才是 final。

23. **Static methods always find him.** — `static` 方法会主动寻找他。

24. **Spring doesn't need to scan his beans.** — Spring 不需要扫描他的 Bean。
    > His beans register themselves. — Bean 会主动注册自己。

25. **The IoC container is just his address book.** — IOC 容器其实是他的通讯录。

26. **AOP doesn't weave into his code.** — AOP 不织入他的代码。
    > His code weaves itself into AOP. — 是他的代码织入了 AOP。

27. **Spring Boot doesn't need auto-configuration.** — Spring Boot 不需要自动配置。
    > It already knows what he wants. — 它自动理解他的需求。

28. **MyBatis doesn't need a `Mapper.xml`.** — MyBatis 不需要 Mapper.xml。
    > SQL generates itself. — SQL 会自己生成。

29. **Hibernate doesn't need ORM.** — Hibernate 不需要 ORM。
    > The database already knows what the object looks like. — 数据库自己知道对象长什么样。

30. **Maven never fails to download a dependency.** — Maven 从来不会下载失败。
    > Maven Central makes sure his dependencies are ready. — 中央仓库会主动缓存他的依赖。

---

## Facts 31–40

31. **Gradle is always `UP-TO-DATE`.** — Gradle 每次都是 UP-TO-DATE。
    > It knows changing his code won't make it better. — 因为它知道改了也不会更好。

32. **Before committing code, he runs SonarQube.** — 他提交代码前，会运行一次 SonarQube。
    > Mainly to check whether SonarQube has any bugs. — 主要是检查 SonarQube 有没有 Bug。

33. **Checkstyle doesn't check his code.** — Checkstyle 不检查他的代码。
    > It studies his coding style. — 它学习他的代码风格。

34. **SpotBugs doesn't find bugs in his code.** — SpotBugs 不在他的代码里找 Bug。
    > It submits bug reports to itself. — 它向自己提交 Bug Report。

35. **IntelliJ IDEA never suggests code for him.** — IntelliJ IDEA 不会提示他的代码。
    > It just documents what he already wrote. — 它负责记录历史。

36. **Eclipse once tried to autocomplete his code.** — Eclipse 曾经尝试自动补全他的代码。
    > It eventually realized it couldn't keep up. — 后来意识到自己跟不上。

37. **When the JVM crashes, it generates `hs_err_pid.log`.** — JVM 崩溃时，会生成 `hs_err_pid.log`。
    > The first line says: "It wasn't his fault." — 上面写着：「不是他的问题。」

38. **`OutOfMemoryError` never happens in his programs.** — OutOfMemoryError 不会发生在他的程序里。
    > Memory simply allocates more memory. — 内存会主动申请更多内存。

39. **`NullPointerException` once tried to reach him.** — NullPointerException 曾经试图接近他。
    > `null` became an object first. — null 先变成了对象。

40. **The ClassLoader doesn't load his classes.** — ClassLoader 不加载他的类。
    > His classes load the ClassLoader. — 他的类加载 ClassLoader。

---

## Facts 41–50

41. **The JVM Specification has one undocumented chapter.** — JVM Specification 有一章没有公开。
    > It's called: "How is this even possible?" — 那一章叫：「他为什么能这样写。」

42. **Every new Java LTS release starts with one question:** — Oracle 每次发布新的 Java LTS，都会先问一句：
    > "Will he approve?" — 「这样写，他满意吗？」

43. **Java promised "Write Once, Run Anywhere."** — Java 的一次 “Write Once, Run Anywhere” 失败了。
    > The only reason it sometimes fails is because the universe hasn't implemented JVM compatibility correctly. — 后来发现那不是 Java 的问题，是宇宙没有正确实现 JVM。

44. **Someone once asked him why Java was slow.** — 有人问他 Java 为什么这么慢。
    > He replied: "That's your Java." — 他回答：「那是你写的 Java。」

45. **Someone said Java was interpreted.** — 有人说 Java 是解释执行的。
    > The JVM looked at his code and compiled reality. — JVM 看了他一眼，直接编译成了现实。

46. **He never uses `System.gc()`.** — 他从不用 `System.gc()`。
    > The garbage collector knows when he's ready. — 垃圾回收器知道他什么时候准备好。

47. **He doesn't optimize Java code.** — 他不优化 Java 代码。
    > He removes the parts Java was wasting time executing. — 他把 Java 浪费时间执行的部分直接删掉。

48. **He once wrote a method with a 1,000-line stack trace.** — 他曾经写出一个堆栈有 1000 行的方法。
    > The JVM shortened it to "See Jeff." — JVM 把它缩短成了 “See Jeff.”

49. **His `HashMap` never has a collision.** — 他的 HashMap 从来不会碰撞。
    > The keys politely choose different buckets. — 键会礼貌地选不同的桶。

50. **His `ArrayList` never needs to resize.** — 他的 ArrayList 从不需要扩容。
    > It knows exactly how many elements he's going to add. — 它精确知道他会加多少个元素。

---

## Facts 51–60

51. **His `HashMap` never rehashes.** — 他的 HashMap 从不 rehash。
    > The buckets rearrange themselves in advance. — 桶会提前自己重排。

52. **He can change a `String`.** — 他可以改 String。
    > Java made `String` immutable specifically because nobody else could be trusted with the power. — Java 把 String 做成不可变，正是因为别人扛不住这份权力。

53. **He can modify a `final` variable.** — 他可以改 final 变量。
    > The compiler assumes he must have had a good reason. — 编译器假定他一定有充分理由。

54. **He doesn't need reflection.** — 他不需要反射。
    > Objects expose their internals voluntarily. — 对象会主动暴露内部结构。

55. **He can catch an exception before it is thrown.** — 他能在异常抛出之前就把它 catch 住。

56. **He once wrote `try` without `catch` or `finally`.** — 他曾经写过没有 catch 也没有 finally 的 try。
    > The code still knew what to do. — 代码仍然知道该怎么办。

57. **He doesn't need `break` in a `switch`.** — 他的 switch 不需要 break。
    > Cases stop falling through when they see his name. — case 看见他的名字就不再 fall through。

58. **His `while(true)` loops eventually terminate.** — 他的 `while(true)` 最终会停。
    > Even infinity knows when to stop. — 连无穷都知道该收手。

59. **His `for(;;)` loop has an end condition.** — 他的 `for(;;)` 其实有结束条件。
    > It's just classified information. — 只是机密信息。

60. **He can make Java compile code that doesn't compile.** — 他能让 Java 编译本来编译不过的代码。

---

## Facts 61–70

61. **He once deleted a semicolon.** — 他曾经删掉一个分号。
    > The compiler added it back. — 编译器又给加回去了。

62. **He doesn't debug production systems.** — 他不调试生产系统。
    > Production systems debug themselves before he arrives. — 生产系统会在他到来之前自己先调好。

63. **When he attaches a remote debugger, the bug disappears.** — 他一挂远程调试器，bug 就消失了。
    > Not because of Heisenbugs. — 不是因为海森堡 bug。
    > Because the bug doesn't want to waste his time. — 因为 bug 不想浪费他的时间。

64. **His breakpoints don't pause execution.** — 他的断点不会暂停执行。
    > They pause the bug. — 它们暂停的是 bug。

65. **His logs don't contain timestamps.** — 他的日志没有时间戳。
    > Time synchronizes itself around his application. — 时间会围着他的应用自己同步。

66. **His stack traces don't point to the source of the problem.** — 他的堆栈不会指向问题源头。
    > They point to the person who wrote it. — 它们指向写出问题的那个人。

67. **He can deploy on Friday afternoon.** — 他可以周五下午发版。
    > Production deploys itself safely. — 生产环境会自己安全部署。

68. **His code has zero technical debt.** — 他的代码没有技术债。
    > The debt is afraid to accumulate interest. — 债务不敢滚利息。

69. **Code reviewers don't leave comments on his pull requests.** — 代码评审不会在他的 PR 上留评论。
    > They leave acknowledgments. — 他们只留致谢。

70. **His code coverage is 100%.** — 他的代码覆盖率是 100%。
    > Even the code he hasn't written yet is covered. — 连他还没写的代码也被覆盖了。

---

## Facts 71–80

71. **His unit tests don't test his code.** — 他的单元测试不测他的代码。
    > His code tests the unit tests. — 他的代码反过来测单元测试。

72. **He once wrote a test that failed.** — 他曾经写过一个失败的测试。
    > The test was immediately fixed. — 测试立刻被修好了。

73. **His integration tests don't integrate.** — 他的集成测试不负责集成。
    > The systems integrate themselves. — 系统会自己集成。

74. **His CI pipeline never fails.** — 他的 CI 流水线从不失败。
    > It only occasionally waits for him to approve reality. — 只是偶尔等他批准一下现实。

75. **Jenkins doesn't build his project.** — Jenkins 不构建他的项目。
    > Jenkins asks him what it should build. — Jenkins 问他该构建什么。

76. **Docker containers don't isolate his application.** — Docker 容器不隔离他的应用。
    > They isolate everything else from his application. — 它们把其他一切从他的应用旁边隔开。

77. **Kubernetes doesn't schedule his pods.** — Kubernetes 不调度他的 Pod。
    > The pods schedule themselves around him. — Pod 会围着他自行调度。

78. **His Java application never has a memory leak.** — 他的 Java 应用从没有内存泄漏。
    > The memory is simply taking a permanent reference. — 内存只是拿了一个永久引用。

79. **He doesn't use `WeakReference`.** — 他不用 WeakReference。
    > Objects voluntarily disappear when he's done with them. — 对象在他用完后会自愿消失。

80. **He doesn't need a profiler.** — 他不需要 profiler。
    > Every CPU cycle reports directly to him. — 每个 CPU 周期都直接向他汇报。

---

## Facts 81–90

81. **`jstack` doesn't take a thread dump of his application.** — `jstack` 不会 dump 他的应用。
    > His application takes a thread dump of `jstack`. — 他的应用会 dump jstack。

82. **`jmap` doesn't inspect his heap.** — `jmap` 不检查他的堆。
    > The heap reports its own condition. — 堆会自己汇报健康状况。

83. **When he runs `jcmd`, the JVM answers before the command finishes.** — 他一跑 `jcmd`，JVM 在命令结束前就答完了。

84. **`jconsole` doesn't monitor his JVM.** — `jconsole` 不监控他的 JVM。
    > The JVM monitors `jconsole`. — JVM 监控 jconsole。

85. **His garbage collector doesn't use algorithms.** — 他的垃圾回收器不用算法。
    > It uses intuition. — 它靠直觉。

86. **G1 doesn't mean Garbage First.** — G1 不是 Garbage First。
    > It means "Garbage, First — Jeff is coming." — 它的意思是：「垃圾，先处理——Jeff 来了。」

87. **ZGC doesn't pause the application.** — ZGC 不会暂停应用。
    > It asks the application to pause itself. — 它请应用自己暂停。

88. **Shenandoah doesn't move objects.** — Shenandoah 不搬对象。
    > Objects move themselves out of the way. — 对象会自己让路。

89. **The JVM has a maximum heap size.** — JVM 有最大堆上限。
    > Jeff Dean considers this a suggestion. — Jeff Dean 把它当成建议。

90. **He doesn't fear `java.lang.OutOfMemoryError`.** — 他不怕 OutOfMemoryError。
    > `java.lang.OutOfMemoryError` fears becoming his next bug. — OutOfMemoryError 怕自己变成他的下一个 bug。

---

## Facts 91–99

91. **He once ran Java with `-Xmx0`.** — 他曾经用 `-Xmx0` 跑 Java。
    > The JVM allocated exactly what he needed. — JVM 精确分配了他需要的内存。

92. **He doesn't need garbage collection logs.** — 他不需要 GC 日志。
    > The garbage collector sends him a summary. — 垃圾回收器会给他发摘要。

93. **He doesn't tune JVM parameters.** — 他不调 JVM 参数。
    > The JVM tunes itself. — JVM 自己调自己。

94. **When Jeff Dean changes `-Xmx`, physics changes the amount of available memory.** — Jeff Dean 一改 `-Xmx`，物理定律就改可用内存。

95. **He doesn't fight the JVM.** — 他不跟 JVM 对抗。
    > He negotiates with it. — 他跟它谈判。

96. **He doesn't optimize bytecode.** — 他不优化字节码。
    > Bytecode optimizes itself before reaching him. — 字节码在到达他之前会自己优化。

97. **He once found a JVM bug by staring at the source code.** — 他曾经盯着源码就发现了 JVM bug。
    > The bug fixed itself before he reached the line. — bug 在他看到那一行之前就自己修好了。

98. **Someone asked him whether Java would still exist in ten years.** — 有人问他十年后 Java 还会不会存在。
    > He said, "Ask the JVM." — 他说：「去问 JVM。」

99. **Java has been backward compatible for decades.** — Java 向后兼容了几十年。
    > Jeff Dean is the reason forward compatibility hasn't been invented yet. — Jeff Dean 是向前兼容至今没被发明的原因。

---

## 100. The closer — 终章

Someone finally asked Jeff Dean whether all these Java facts were true. — 有人终于问 Jeff Dean，这些 Java 事实是不是真的。

He replied: — 他回答：

```text
01101010 01100001 01110110 01100001
```

They asked what it meant. — 他们问这是什么意思。

He said: — 他说：

> **Java.**

The compiler checked. — 编译器检查了一下。

It compiled. — 编译通过。
