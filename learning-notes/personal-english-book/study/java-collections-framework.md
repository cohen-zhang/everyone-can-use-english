# Java Collections Framework — Java 集合框架

The Java Collections Framework provides a set of interfaces and classes for storing and manipulating groups of data. It was introduced in Java 1.2 and is part of the `java.util` package.

Java 集合框架提供了一组接口和类，用于存储和操作数据组。它在 Java 1.2 中引入，是 `java.util` 包的一部分。

## Overview — 概述

### What is the Collections Framework? — 什么是集合框架？

The **Collections Framework** is a unified architecture for representing and manipulating collections. All classes that implement the Collection interface share a common set of methods, making them **interoperable** and **polymorphic**.

**集合框架**是用于表示和操作集合的统一架构。所有实现 Collection 接口的类都共享一组通用方法，使它们具有**互操作性**和**多态性**。

### Core Benefits — 核心优势

1. **Reduces programming effort** — 减少编程工作
2. **Increases performance** — 提高性能
3. **Interoperability between unrelated APIs** — 无关 API 之间的互操作性
4. **Designs with high quality** — 高质量设计

## Architecture — 架构

### Interface Hierarchy — 接口层次结构

The framework follows a clear **inheritance hierarchy** with base interfaces and specialized implementations:

框架遵循清晰的**继承层次结构**，具有基础接口和专用实现：

```
Collection (Interface)
├── List (Interface) — Ordered collection, allows duplicates — 有序集合，允许重复
├── Set (Interface) — No duplicates, no guaranteed order — 不允许重复，无保证顺序
└── Queue (Interface) — FIFO ordering — 先进先出排序

Map (Interface) — Key-value pairs, not part of Collection hierarchy — 键值对，不属于 Collection 层次
```

### Key Interfaces — 关键接口

#### Collection — 集合接口

The **root interface** of the framework. Represents a group of objects known as **elements**. Provides basic operations like add, remove, and contains.

框架的**根接口**。表示一组称为**元素**的对象。提供基本操作，如 add、remove 和 contains。

#### List — 列表接口

**Ordered collection** that allows **duplicate elements**. Elements can be accessed by their **integer index** (position). Common implementations include ArrayList and LinkedList.

**有序集合**，允许**重复元素**。元素可以通过其**整数索引**（位置）访问。常见实现包括 ArrayList 和 LinkedList。

**Key Characteristics**:
- **Positional access** — 位置访问
- **Search operations** — 搜索操作
- **Range operations** — 范围操作
- **Insertion order preserved** — 保持插入顺序

#### Set — 集合接口

Collection that **cannot contain duplicate elements**. Models the mathematical **set abstraction**. Used when uniqueness matters more than order.

**不能包含重复元素**的集合。模拟数学上的**集合抽象**。当唯一性比顺序更重要时使用。

**Key Characteristics**:
- **No duplicates** — 无重复元素
- **No guaranteed order** (unless using LinkedHashSet or TreeSet) — 无保证顺序（除非使用 LinkedHashSet 或 TreeSet）
- **Efficient membership testing** — 高效的成员资格测试

#### Map — 映射接口

Object that maps **keys to values**. Cannot contain duplicate keys; each key maps to at most one value. Not a true Collection, but part of the framework.

将**键映射到值**的对象。不能包含重复的键；每个键最多映射到一个值。不是真正的 Collection，但是框架的一部分。

**Key Characteristics**:
- **Key-value pairs** — 键值对
- **Unique keys** — 唯一键
- **Fast lookups by key** — 通过键快速查找
- **No guaranteed order** (unless using LinkedHashMap or TreeMap) — 无保证顺序（除非使用 LinkedHashMap 或 TreeMap）

## Common Implementations — 常见实现

### List Implementations — List 实现

#### ArrayList

**Resizable-array** implementation. Provides fast **random access** and slow **insertion/deletion** in the middle of the list.

**可调整大小的数组**实现。提供快速的**随机访问**和在列表中间较慢的**插入/删除**。

**Best Use Cases**:
- Frequent access by index — 频繁通过索引访问
- Adding/removing elements only at the end — 仅在末尾添加/删除元素
- When memory efficiency matters — 当内存效率重要时

**Time Complexity**:
- Access: O(1) — 访问
- Insert at end: O(1) amortized — 末尾插入（均摊）
- Insert in middle: O(n) — 中间插入
- Delete: O(n) — 删除

#### LinkedList

**Doubly-linked list** implementation. Provides fast **insertion/deletion** but slow **random access**.

**双向链表**实现。提供快速的**插入/删除**但缓慢的**随机访问**。

**Best Use Cases**:
- Frequent insertions/deletions at both ends — 频繁在两端插入/删除
- Implementing queues and stacks — 实现队列和栈
- When iteration is more common than indexed access — 当迭代比索引访问更常见时

**Time Complexity**:
- Access: O(n) — 访问
- Insert at beginning/end: O(1) — 开头/结尾插入
- Insert in middle: O(n) to reach position — 中间插入（到达位置）
- Delete: O(1) once position reached — 删除（到达位置后）

### Set Implementations — Set 实现

#### HashSet

**Hash table** implementation. Fastest operations but **no ordering guarantees**. Uses `hashCode()` and `equals()` for uniqueness.

**哈希表**实现。操作最快但**无顺序保证**。使用 `hashCode()` 和 `equals()` 确保唯一性。

**Best Use Cases**:
- Fast lookups — 快速查找
- When order doesn't matter — 当顺序不重要时
- Unique collections — 唯一集合

**Time Complexity**:
- Add, remove, contains: O(1) average — 添加、删除、包含（平均）

#### LinkedHashSet

**Hash table + linked list** implementation. Maintains **insertion order** while providing fast operations.

**哈希表 + 链表**实现。在提供快速操作的同时保持**插入顺序**。

**Best Use Cases**:
- Fast operations with predictable iteration order — 具有可预测迭代顺序的快速操作
- When insertion order matters — 当插入顺序重要时

#### TreeSet

**Red-black tree** implementation. Maintains elements in **sorted order**. Slower than HashSet but provides ordering.

**红黑树**实现。以**排序顺序**维护元素。比 HashSet 慢但提供排序。

**Best Use Cases**:
- Sorted collections — 排序集合
- Range operations — 范围操作
- When natural ordering is required — 当需要自然排序时

**Time Complexity**:
- Add, remove, contains: O(log n) — 添加、删除、包含

### Map Implementations — Map 实现

#### HashMap

**Hash table** implementation. Provides **constant-time** performance for basic operations. Allows one null key and multiple null values.

**哈希表**实现。为基本操作提供**常数时间**性能。允许一个 null 键和多个 null 值。

**Best Use Cases**:
- Fast key-value lookups — 快速键值查找
- Caching — 缓存
- General-purpose mapping — 通用映射

**Time Complexity**:
- Get, put, remove: O(1) average — 获取、放置、删除（平均）

#### LinkedHashMap

**HashMap + linked list** implementation. Maintains **insertion order** (or access order with constructor flag).

**HashMap + 链表**实现。保持**插入顺序**（或使用构造函数标志的访问顺序）。

**Best Use Cases**:
- LRU caches — LRU 缓存
- When insertion order matters — 当插入顺序重要时
- Building predictable maps — 构建可预测的映射

#### TreeMap

**Red-black tree** implementation. Maintains keys in **sorted order**. Provides guaranteed log(n) time cost.

**红黑树**实现。以**排序顺序**维护键。提供保证的 log(n) 时间成本。

**Best Use Cases**:
- Sorted mappings — 排序映射
- Range operations on keys — 键的范围操作
- When natural ordering is required — 当需要自然排序时

## Key Operations — 关键操作

### Common Collection Operations — 通用集合操作

#### Bulk Operations — 批量操作

- **containsAll()** — Checks if collection contains all elements — 检查集合是否包含所有元素
- **addAll()** — Adds all elements from another collection — 添加另一个集合的所有元素
- **removeAll()** — Removes all elements in another collection — 删除另一个集合的所有元素
- **retainAll()** — Keeps only elements in another collection — 仅保留另一个集合中的元素

#### Array Operations — 数组操作

- **toArray()** — Converts collection to array — 将集合转换为数组
- **Arrays.asList()** — Converts array to list — 将数组转换为列表

### List-Specific Operations — List 特定操作

- **get(index)** — Retrieves element at position — 检索位置的元素
- **set(index, element)** — Replaces element at position — 替换位置的元素
- **indexOf()** — Returns first occurrence index — 返回第一次出现的索引
- **lastIndexOf()** — Returns last occurrence index — 返回最后一次出现的索引
- **subList()** — Returns view of portion of list — 返回列表部分的视图

### Map-Specific Operations — Map 特定操作

- **put(key, value)** — Associates value with key — 将值与键关联
- **get(key)** — Returns value for key — 返回键的值
- **containsKey()** — Checks if key exists — 检查键是否存在
- **containsValue()** — Checks if value exists — 检查值是否存在
- **keySet()** — Returns set of keys — 返回键集合
- **values()** — Returns collection of values — 返回值集合
- **entrySet()** — Returns set of key-value pairs — 返回键值对集合

## Design Patterns — 设计模式

### Iteration Patterns — 迭代模式

#### Iterator Pattern

Provides a uniform way to access collection elements **without exposing** the underlying representation. Works with all collection types.

提供一种统一的方式来访问集合元素，**不暴露**底层表示。适用于所有集合类型。

```java
Iterator<String> iterator = collection.iterator();
while (iterator.hasNext()) {
    String element = iterator.next();
    // Process element — 处理元素
}
```

#### For-Each Loop

Enhanced for loop provides **syntactic sugar** over iterators. More readable and less error-prone.

增强的 for 循环在迭代器之上提供**语法糖**。更易读且更不容易出错。

```java
for (String element : collection) {
    // Process element — 处理元素
}
```

### Factory Methods — 工厂方法

#### Collections Utility Class

Provides **static factory methods** for creating immutable, empty, or synchronized collections.

提供用于创建不可变、空或同步集合的**静态工厂方法**。

- **Collections.unmodifiableCollection()** — Creates read-only view — 创建只读视图
- **Collections.emptyList()** — Returns empty list — 返回空列表
- **Collections.synchronizedList()** — Creates thread-safe wrapper — 创建线程安全包装器

#### List.of() and Set.of() (Java 9+)

Concise factory methods for creating **immutable collections**. More readable than traditional constructors.

用于创建**不可变集合**的简洁工厂方法。比传统构造函数更易读。

## Performance Considerations — 性能考虑

### Choosing the Right Implementation — 选择正确的实现

**Choose ArrayList** when:
- Frequent random access by index — 频繁通过索引随机访问
- Mostly adding/removing at the end — 主要在末尾添加/删除
- Memory efficiency is important — 内存效率重要

**Choose LinkedList** when:
- Frequent additions/deletions at beginning or middle — 频繁在开头或中间添加/删除
- Implementing queues/stacks — 实现队列/栈

**Choose HashSet** when:
- Fast lookups are critical — 快速查找很关键
- Order doesn't matter — 顺序不重要
- Unique elements required — 需要唯一元素

**Choose TreeSet** when:
- Sorted order is required — 需要排序顺序
- Range operations are needed — 需要范围操作

**Choose HashMap** when:
- Fast key-value lookups — 快速键值查找
- No ordering requirements — 无排序要求

**Choose TreeMap** when:
- Sorted keys are required — 需要排序键
- Range operations on keys — 键的范围操作

### Memory Efficiency — 内存效率

- **ArrayList** has minimal overhead — 具有最小开销
- **LinkedList** has higher overhead due to node objects — 由于节点对象具有更高开销
- **HashSet** requires additional memory for hash table — 需要额外的哈希表内存
- **TreeSet** requires more memory for tree structure — 树结构需要更多内存

## Thread Safety — 线程安全

### Synchronized Wrappers — 同步包装器

The `Collections` class provides methods to create **thread-safe** wrappers:

`Collections` 类提供创建**线程安全**包装器的方法：

```java
List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
Map<String, String> synchronizedMap = Collections.synchronizedMap(new HashMap<>());
```

**Important**: Must manually synchronize when iterating over synchronized collections.

**重要**：在遍历同步集合时必须手动同步。

### Concurrent Collections — 并发集合

Java provides **concurrent collection** classes in `java.util.concurrent`:

Java 在 `java.util.concurrent` 中提供**并发集合**类：

- **ConcurrentHashMap** — Thread-safe HashMap without explicit synchronization — 线程安全的 HashMap，无需显式同步
- **CopyOnWriteArrayList** — Thread-safe ArrayList optimized for reads — 针对读取优化的线程安全 ArrayList
- **ConcurrentSkipListSet** — Thread-safe sorted set — 线程安全的排序集合

## Common Algorithms — 常见算法

### Sorting — 排序

```java
Collections.sort(list); // Natural order — 自然顺序
Collections.sort(list, comparator); // Custom order — 自定义顺序
```

### Searching — 搜索

```java
int index = Collections.binarySearch(sortedList, key); // Requires sorted list — 需要排序列表
boolean found = collection.contains(element); // Linear search — 线性搜索
```

### Shuffling — 洗牌

```java
Collections.shuffle(list); // Randomizes order — 随机化顺序
```

### Reversing — 反转

```java
Collections.reverse(list); // Reverses order — 反转顺序
```

## Best Practices — 最佳实践

### 1. Declare Using Interfaces — 使用接口声明

```java
// Good — 好的做法
List<String> list = new ArrayList<>();
Set<String> set = new HashSet<>();
Map<String, String> map = new HashMap<>();

// Avoid — 避免
ArrayList<String> list = new ArrayList<>();
```

**Benefit**: Allows easy implementation changes without affecting client code.

**好处**：允许轻松更改实现而不影响客户端代码。

### 2. Initialize with Capacity — 用容量初始化

```java
// Good — Specify expected size — 指定预期大小
List<String> list = new ArrayList<>(1000);

// Avoid — Default capacity may cause resizing — 默认容量可能导致调整大小
List<String> list = new ArrayList<>();
```

**Benefit**: Prevents costly resizing operations.

**好处**：防止昂贵的调整大小操作。

### 3. Use Immutable Collections — 使用不可变集合

```java
// Java 9+ — Java 9+
List<String> immutable = List.of("a", "b", "c");

// Earlier versions — 早期版本
List<String> immutable = Collections.unmodifiableList(list);
```

**Benefit**: Prevents accidental modification, thread-safe by default.

**好处**：防止意外修改，默认线程安全。

### 4. Prefer Enhanced For Loop — 偏好增强 for 循环

```java
// Good — Clearer and less error-prone — 更清晰且更不容易出错
for (String item : collection) {
    // Process — 处理
}

// Avoid — More verbose and error-prone — 更冗长且容易出错
for (Iterator<String> it = collection.iterator(); it.hasNext(); ) {
    String item = it.next();
    // Process — 处理
}
```

### 5. Use Streams for Complex Operations — 对复杂操作使用流

```java
// Good — Declarative and readable — 声明式且易读
list.stream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Avoid — Imperative and less readable — 命令式且不易读
List<String> result = new ArrayList<>();
for (String s : list) {
    if (s.startsWith("A")) {
        result.add(s.toUpperCase());
    }
}
```

## Vocabulary — 词汇表

| Term | 中文 | Definition |
|------|------|------------|
| **Collection** | 集合 | An object that groups multiple elements into a single unit |
| **Interface** | 接口 | A reference type in Java, similar to a class that only contains abstract methods |
| **Implementation** | 实现 | A concrete class that provides the actual functionality of an interface |
| **Duplicate** | 重复 | Having more than one instance of the same element |
| **Ordered** | 有序的 | Maintaining a specific sequence of elements |
| **Hash table** | 哈希表 | A data structure that uses a hash function to compute an index |
| **Red-black tree** | 红黑树 | A self-balancing binary search tree |
| **Polymorphic** | 多态的 | Having many forms, allowing objects of different types to be treated as objects of a common type |
| **Interoperable** | 可互操作的 | Able to work together with other systems or components |
| **Immutable** | 不可变的 | Cannot be changed once created |
| **Synchronized** | 同步的 | Thread-safe, allowing only one thread to access at a time |
| **Concurrent** | 并发的 | Handling multiple tasks simultaneously |
| **Iterator** | 迭代器 | An object that enables traversing a collection |
| **Capacity** | 容量 | The maximum number of elements a collection can hold |
| **Resizing** | 调整大小 | Changing the capacity of a collection dynamically |

## Common Interview Questions — 常见面试问题

### Q: What's the difference between ArrayList and LinkedList?

**A**: ArrayList uses a **resizable array** and provides fast **random access** but slow insertions/deletions in the middle. LinkedList uses a **doubly-linked list** and provides fast insertions/deletions but slow random access. ArrayList is generally better for most use cases due to better **cache locality** and lower **memory overhead**.

ArrayList 使用**可调整大小的数组**，提供快速的**随机访问**但在中间插入/删除缓慢。LinkedList 使用**双向链表**，提供快速的插入/删除但随机访问缓慢。由于更好的**缓存局部性**和更低的**内存开销**，ArrayList 通常更适合大多数用例。

### Q: When should I use Set instead of List?

**A**: Use Set when you need to ensure **uniqueness** of elements and don't care about order or when you want to eliminate duplicates from a collection. Use List when you need to maintain **insertion order** or allow duplicate elements, or when you need **positional access** to elements.

当需要确保元素的**唯一性**且不关心顺序，或者想要从集合中消除重复元素时，使用 Set。当需要保持**插入顺序**或允许重复元素，或者需要对元素进行**位置访问**时，使用 List。

### Q: What's the difference between HashMap and TreeMap?

**A**: HashMap provides **constant-time** performance and doesn't guarantee any order. TreeMap provides **logarithmic-time** performance and maintains keys in **sorted order**. HashMap is generally faster and more memory-efficient, while TreeMap is useful when you need **sorted keys** or **range operations**.

HashMap 提供**常数时间**性能，不保证任何顺序。TreeMap 提供**对数时间**性能，以**排序顺序**维护键。HashMap 通常更快且更节省内存，而 TreeMap 在需要**排序键**或**范围操作**时很有用。

### Q: How does HashSet ensure uniqueness?

**A**: HashSet uses the **hashCode()** method to determine the bucket for an element and the **equals()** method to check for equality. When adding an element, it first computes the hash code to find the bucket, then uses equals() to check if the element already exists in that bucket. Proper implementation of both methods is crucial for correct behavior.

HashSet 使用 **hashCode()** 方法确定元素的桶，并使用 **equals()** 方法检查相等性。添加元素时，它首先计算哈希码以找到桶，然后使用 equals() 检查该元素是否已存在于该桶中。正确实现这两个方法对于正确行为至关重要。

---

## Further Reading — 延伸阅读

- [Java Collections Framework Documentation](https://docs.oracle.com/javase/8/docs/technotes/guides/collections/)
- [Baeldung: Guide to Java Collections](https://www.baeldung.com/java-collections)
- Related: **`Generics`**, **`Streams`**, **`Comparable` vs `Comparator`** — 相关：`泛型`、`流`、`Comparable` 与 `Comparator`

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (repo root) |
|-------|------------|-----------------|
| fail-fast / ArrayList | `collection.ArrayListFailFastExample` | `mvn -pl java-base -q compile` · `java -cp java-base/target/classes collection.ArrayListFailFastExample` |
| String intern | `string.StringInternExample` | `java -cp java-base/target/classes string.StringInternExample` |
| HashMap basics | `HashMapTest` | `java -cp java-base/target/classes HashMapTest` |

**English README:** https://github.com/zhangze2/awesome-demo/blob/master/java-base/README.en.md

**Tags**: `技术`, `Java`, `集合`, `数据结构`, `算法`