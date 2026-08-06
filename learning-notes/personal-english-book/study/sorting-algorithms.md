---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
  - algorithms
aliases:
  - Sorting Algorithms
  - 排序算法
  - Java sort module
---

# Sorting Algorithms — 排序算法

Sorting algorithms rearrange elements into a defined order (usually ascending or descending). This note is English reading practice for Java engineers; each section maps to one schema unit under the demo repo’s `sort/` module.

排序算法按既定顺序（通常升序或降序）重排元素。本文面向 Java 工程师的英文阅读练习；各小节对应 demo 仓库 `sort/` 模块中的一个图式单元。

**Demo bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

**Demo repo:** https://github.com/zhangze2/awesome-demo/tree/master/sort · **Local sibling:** `../awesome-java-demo/sort/`

**Visual / Cookbook:**

- [Halfrost LeetCode Cookbook · Sorting](https://books.halfrost.com/leetcode/ChapterTwo/Sorting/)
- [VisuAlgo · Sorting](https://visualgo.net/zh/sorting?slide=4)

---

## Overview — 概述

### What is a sorting algorithm? — 什么是排序算法？

A **sorting algorithm** takes a collection and produces a permutation where elements follow a total order (for example, `Comparable` or a `Comparator`). Engineers care about **time complexity**, **space complexity**, and **stability**.

**排序算法**接收一个集合，产出按全序排列的置换（例如通过 `Comparable` 或 `Comparator`）。工程师关注**时间复杂度**、**空间复杂度**和**稳定性**。

### Core vocabulary hooks — 核心概念钩子

1. **Stable** — equal keys keep their relative order — 相等键保持相对顺序
2. **In-place** — only a constant amount of extra memory — 仅常数额外内存
3. **Adaptive** — faster on nearly sorted input — 近乎有序时更快
4. **Divide and conquer** — split, solve, combine — 分治：拆分、求解、合并
5. **Hybrid** — mix algorithms (e.g. quick + insertion cutoff) — 混合算法（如快排 + 插入收尾）

---

## Complexity & Stability Cheat Sheet — 复杂度与稳定性速查

| Algorithm | Avg Time | Worst Time | Space | Stable | Schema |
|-----------|----------|------------|-------|--------|--------|
| Bubble Sort | O(n²) | O(n²) | O(1) | Yes | `BubbleSort` |
| Selection Sort | O(n²) | O(n²) | O(1) | No | `SelectionSort` |
| Insertion Sort | O(n²) | O(n²) | O(1) | Yes | `InsertSort` |
| Shell Sort | O(n log² n)~O(n^(3/2)) | depends on gap | O(1) | No | `ShellSort` |
| Quick Sort | O(n log n) | O(n²) | O(log n) | No | `QuickSort` |
| Improved Quick Sort | O(n log n) | closer to O(n log n) | O(1) stack | No | `ImprovedQuickSort` |
| Merge Sort | O(n log n) | O(n log n) | O(n) | Yes | `MergeSort` |
| Improved Merge Sort | O(n log n) | O(n log n) | O(n) | Yes* | `ImprovedMergeSort` |
| Heap Sort | O(n log n) | O(n log n) | O(1) | No | `HeapSort` |

\*Stability of the hybrid depends on how ties are resolved during merge and the insertion cutoff.  
\*混合版的稳定性取决于归并时平局如何处理，以及插入排序的截断阈值。

---

## Bubble Sort — 冒泡排序

Bubble Sort repeatedly walks the array and **swaps adjacent elements** that are out of order. After each outer pass, one more extreme value “**bubbles**” into its final position.

冒泡排序反复扫描数组，交换**相邻逆序**元素。每轮外层遍历后，又有一个极值“**冒泡**”到最终位置。

**How it works — 步骤**

1. Compare neighboring pairs from one end of the unsorted range toward the other. — 在未排序区间内比较相邻元素
2. Swap whenever the order violates ascending (or descending) order. — 违反目标顺序则交换
3. Shrink the unsorted range by one after each full pass. — 每轮结束后缩小未排序区间
4. Optional early exit: if a pass performs no swaps, the array is already sorted. — 可选提前退出：某轮无交换则已有序

**Characteristics — 特性**

- **Stable**: equal elements keep relative order when you only swap on `<` / `>`, never on `==`. — **稳定**：仅在 `<` / `>` 时交换
- **In-place**: constant extra memory. — **原地**
- **Adaptive** (with early exit): nearly sorted input finishes in roughly O(n). — **自适应**（带提前退出）
- Teaching value high; too slow for large random data. — 教学价值高；大数据随机输入太慢

**When to use — 何时用**: tiny arrays, nearly sorted streams, or pedagogy. Prefer insertion sort for small real workloads. — 极小数组、近乎有序、教学；真实小数据优先插入排序。

---

## Selection Sort — 选择排序

Selection Sort repeatedly finds the **minimum** (or maximum) in the remaining unsorted suffix and swaps it into the next fixed position. Slogan in the demo repo: “还会发现更好的” — keep updating the candidate index, then swap once.

选择排序反复在未排序后缀中找**最小（或最大）**值，再与下一个固定位置交换。Demo 口诀：“还会发现更好的”——持续更新候选下标，最后只交换一次。

**How it works — 步骤**

1. For index `i` from `0` to `n-2`, assume `i` holds the current minimum. — 假定 `i` 处为当前最小
2. Scan `i+1 … n-1` and remember the index of the true minimum. — 扫描并记录真正最小下标
3. Swap that minimum into position `i`. — 交换到位置 `i`
4. The prefix `0 … i` is then permanently sorted. — 前缀永久有序

**Characteristics — 特性**

- **Unstable**: a long-range swap can move equal keys past each other. — **不稳定**：远距离交换可能打乱相等键
- **Always Θ(n²) comparisons**, even on sorted input; swaps ≤ n−1. — 比较次数恒为 Θ(n²)；交换至多 n−1
- **In-place**, simple control flow, rarely best in practice. — 原地、控制流简单，实践中很少最优

**When to use — 何时用**: when write cost dominates and you must **minimize swaps**. — 写代价主导、必须**尽量少交换**时。

---

## Insertion Sort — 插入排序

Insertion Sort builds a **sorted prefix** on the left. For each new element, it slides that element leftward until the prefix remains ordered — “put the current item into the right pocket on the left.”

插入排序在左侧构建**有序前缀**。对每个新元素，向左滑动直到前缀仍有序——“把当前元素插进左侧正确口袋”。

**How it works — 步骤**

1. Start at index `1`; treat `data[0]` as a sorted prefix of length 1. — 从下标 `1` 开始
2. Take `data[i]` as the key (or swap leftward while out of order). — 取当前键（或边比边换）
3. Shift larger left neighbors one slot right (optimized: temp + assignment). — 较大左邻右移一格
4. Place the key into the hole; grow the prefix by one. — 键落入空位，前缀加一

**Characteristics — 特性**

- **Stable** when the inner loop stops on `>` (not `>=`). — **稳定**（内层用 `>` 而非 `>=`）
- **Adaptive**: best case O(n) on already sorted data. — **自适应**：已有序时最优 O(n)
- Excellent for small n and as a cleanup phase after quicksort / mergesort cutoffs. — 适合小 n，以及快排/归并的收尾阶段

**When to use — 何时用**: n ≲ 10–50, online / streaming insertion, or hybrid base case. — 小规模、在线插入、或混合算法的基例。

---

## Shell Sort — 希尔排序

Shell Sort is **insertion sort on interleaved sub-sequences** defined by a decreasing **gap** sequence. Large gaps move elements far in few swaps; the final gap of `1` is ordinary insertion on a nearly ordered array.

希尔排序是按递减**间隔（gap）**序列，对交错子序列做插入排序。大间隔用少次交换把元素挪远；最终 gap=`1` 即对近乎有序数组做普通插入。

**How it works — 步骤**

1. Choose a gap sequence (halving, Knuth’s `h = 3h+1`, or similar). — 选择间隔序列
2. For each gap `h`, run insertion sort on each residue class (`i, i+h, i+2h, …`). — 对每个余类做插入
3. Reduce `h` until `h = 1`, then finish with a full insertion pass. — 缩小至 `1` 收尾

**Characteristics — 特性**

- **Not stable** in general. — 一般**不稳定**
- **In-place**; cost depends heavily on the gap sequence. — **原地**；代价强烈依赖间隔序列
- Faster than plain insertion on medium n without O(n) auxiliary memory. — 中等规模常快于纯插入，且无需 O(n) 辅助内存

**When to use — 何时用**: embedded / memory-tight contexts wanting better-than-quadratic behavior without recursion or extra buffers. — 内存紧、不想要递归或额外缓冲、又要好于平方级。

---

## Quick Sort — 快速排序

Quick Sort is **divide-and-conquer**: pick a **pivot**, **partition** so left is smaller and right is larger, then recurse on both sides. The classic form in the demo uses “dig a hole and fill” with `list[low]` as the initial pivot.

快速排序是**分治**：选**基准（pivot）**，**分区**使左小右大，再递归两侧。Demo 经典版用“挖坑填数”，初始 pivot 为 `list[low]`。

**How it works — 步骤**

1. Choose a pivot and conceptually dig a hole at its index. — 选基准并挖坑
2. From the right, find a value smaller than the pivot and fill; from the left, find a larger value and fill. — 右找小、左找大填坑
3. When pointers meet, put the pivot into the final hole — that index is the split point. — 指针相遇，基准归位即分割点
4. Recursively sort the left and right sub-ranges. — 递归左右区间

**Characteristics — 特性**

- **Average O(n log n)**; **worst O(n²)** when pivots are consistently poor. — 平均 O(n log n)；劣质 pivot 时最坏 O(n²)
- **Not stable**; partition moves equal keys unpredictably. — **不稳定**
- **In-place** aside from O(log n) average recursion stack. — 除递归栈外基本原地
- Cache-friendly; usually fastest general-purpose comparison sort when well engineered. — 缓存友好；工程化后通常最快

**When to use — 何时用**: default for large random in-memory arrays; avoid naive pivot on adversarial input. — 大随机内存数组默认选择；对抗输入避免天真 pivot。

---

## Improved Quick Sort — 改进快速排序

`ImprovedQuickSort` replaces deep recursion with an **explicit stack**, picks a **middle pivot**, and stops partitioning when a segment is shorter than a threshold (`THRESHOLD = 10`), finishing with **insertion sort**.

`ImprovedQuickSort` 用**显式栈**代替深度递归，选**中间 pivot**，区间短于阈值时停止分区，用**插入排序**收尾。

**Improvements — 改进点**

1. **Iterative control**: push / pop interval bounds to avoid call-stack overflow. — **迭代控制**：避免调用栈溢出
2. **Better pivot**: middle index reduces some bad partitions. — **更好的 pivot**
3. **Hybrid cutoff**: tiny segments go to insertion sort. — **混合截断**：小段交给插入排序

**When to use — 何时用**: production-minded teaching of how real libraries harden quicksort (not full introsort / three-way partition). — 面向生产的教学示意（尚未完整 introsort / 三路划分）。

---

## Merge Sort — 归并排序

Merge Sort splits the array in half, sorts each half recursively, then **merges** two already-sorted runs into one sorted run using an **auxiliary buffer**.

归并排序将数组对半拆分、递归排序，再用**辅助缓冲**把两段已有序的 run **归并**成一段。

**How it works — 步骤**

1. If `left == right`, the singleton range is sorted. — 单元素区间已有序
2. Recursively sort `[left, mid]` and `[mid+1, right]`. — 递归左右半区
3. Copy the range into `temp` (or allocate a scratch array). — 拷入临时数组
4. Walk two pointers; always emit the smaller head into the original array. — 双指针取较小头写出

**Characteristics — 特性**

- **Guaranteed O(n log n)** — predictable, unlike quicksort’s worst case. — **保证 O(n log n)**
- **Stable** when the merge prefers the left run on ties (`<=`). — 平局取左则**稳定**
- Needs **O(n) extra memory**. — 需要 **O(n) 额外内存**
- Naturally parallelizable; backbone of external / linked-list sorting. — 易并行；外排与链表排序的骨干

**When to use — 何时用**: need stable sort, guaranteed bounds, or sorting linked structures. JDK `Arrays.sort` for objects is TimSort (merge-based hybrid). — 要稳定、要保证上界、或排链表；JDK 对象排序为 TimSort。

---

## Improved Merge Sort — 改进归并排序

`ImprovedMergeSort` switches to insertion sort when a sub-range length falls below `THRESHOLD`, and uses a bitonic-style fill of the temporary buffer (left ascending, right descending) to simplify the merge loop.

子区间长度低于 `THRESHOLD` 时改用插入排序；临时缓冲按双调风格填充（左升右降），简化归并循环。

**Why hybridize — 为何混合**

- Recursion and merge bookkeeping dominate cost on tiny ranges. — 小区间上递归与归并记账占主导
- Insertion sort has excellent constants for n ≤ ~10. — 插入在 n ≤ ~10 常数优秀
- Same big-O as mergesort, better wall-clock time. — 大 O 相同，墙钟时间更好

---

## Heap Sort — 堆排序

Heap Sort turns the array into a binary **heap** (usually a **max-heap** for ascending order), then repeatedly extracts the heap top into the sorted suffix.

堆排序把数组建成二叉**堆**（升序通常用**大顶堆**），再反复把堆顶抽到有序后缀。

**How it works — 步骤**

1. **Build heap**: sift down from the last non-leaf `(n-1)/2` down to the root. — **建堆**：从最后一个非叶节点向下调整
2. **Extract**: swap the root with the last unsorted element; shrink the heap size by one. — **抽取**：堆顶与末尾交换，堆缩小
3. **Restore**: sift the new root down (`adjustHeap`) within the reduced heap. — **恢复**：对新根做下沉调整
4. Repeat until one element remains. — 重复至只剩一个元素

**Characteristics — 特性**

- **O(n log n)** worst case with **O(1) auxiliary space**. — 最坏 O(n log n)，辅助空间 O(1)
- **Not stable**. — **不稳定**
- Usually slower than well-tuned quicksort (poor locality), but attractive for hard upper bounds without O(n) extra memory. — 通常慢于调优快排（局部性差），但适合要硬上界且无 O(n) 额外内存

**When to use — 何时用**: memory-constrained guaranteed O(n log n); priority-queue mental model for “always pull the extreme value.” — 内存受限且要保证 O(n log n)；优先队列心智模型。

---

## How to Choose — 选型口诀

| Situation — 场景 | Prefer — 优先 |
|------------------|---------------|
| Tiny / nearly sorted — 极小 / 近乎有序 | Insertion Sort |
| Need stability + guaranteed O(n log n) — 要稳定 + 保证上界 | Merge Sort (or TimSort) |
| General in-memory, speed first — 内存内通用、要速度 | Quick Sort / Improved Quick Sort |
| Guaranteed O(n log n), O(1) extra space — 保证上界、常数额外空间 | Heap Sort |
| Teaching adjacency swaps — 教相邻交换 | Bubble Sort |
| Minimize swaps — 尽量少交换 | Selection Sort |
| Medium n, no extra buffer — 中等 n、无额外缓冲 | Shell Sort |

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **Sort** | /sɔːrt/ | 排序 | Rearrange elements into a defined order |
| **Algorithm** | /ˈælɡərɪðəm/ | 算法 | A step-by-step procedure for solving a problem |
| **Complexity** | /kəmˈpleksəti/ | 复杂度 | How cost (time/space) grows with input size |
| **Stable** | /ˈsteɪbəl/ | 稳定的 | Equal keys keep their relative order after sorting |
| **In-place** | /ɪn ˈpleɪs/ | 原地的 | Uses only a constant amount of extra memory |
| **Adaptive** | /əˈdæptɪv/ | 自适应的 | Runs faster on nearly sorted (or special) input |
| **Pivot** | /ˈpɪvət/ | 基准 | The reference element used to partition in quicksort |
| **Partition** | /pɑːrˈtɪʃən/ | 分区 | Rearrange so elements on one side relate to the pivot |
| **Merge** | /mɜːrdʒ/ | 归并 | Combine two sorted runs into one sorted run |
| **Heap** | /hiːp/ | 堆 | A tree-based structure with parent–child ordering rules |
| **Gap** | /ɡæp/ | 间隔 | The stride used by Shell sort’s interleaved subsequences |
| **Threshold** | /ˈθreʃhoʊld/ | 阈值 | Cutoff size where a hybrid switches algorithms |
| **Recursion** | /rɪˈkɜːrʒən/ | 递归 | A function solving a problem by calling itself on smaller input |
| **Auxiliary** | /ɔːɡˈzɪliəri/ | 辅助的 | Extra memory or structure used by an algorithm |
| **Adjacent** | /əˈdʒeɪsənt/ | 相邻的 | Next to each other in the array |
| **Swap** | /swɑːp/ | 交换 | Exchange the positions of two elements |
| **Guaranteed** | /ˌɡærənˈtiːd/ | 有保证的 | Worst-case bound that always holds |
| **Hybrid** | /ˈhaɪbrɪd/ | 混合的 | Combining two or more algorithms |

---

## Common Interview Questions — 常见面试问题

### Q: What's the difference between stable and unstable sorts?

**A**: A **stable** sort keeps the relative order of equal keys. A **unstable** sort may reorder them. Stability matters when you sort by one key and then another (e.g. sort by name, then by grade) and want the first order preserved within ties.

**稳定**排序保持相等键的相对顺序；**不稳定**排序可能打乱它们。当你先按一个键再按另一个键排序、且希望平局内保留前一次顺序时，稳定性很重要。

### Q: When would you prefer mergesort over quicksort?

**A**: Prefer **mergesort** when you need **stability**, a **guaranteed O(n log n)** bound, or when sorting linked structures. Prefer **quicksort** for general in-memory speed when instability is acceptable and pivots are well chosen.

需要**稳定性**、**保证 O(n log n)**，或排序链表时优先**归并**；内存内要速度、可接受不稳定且 pivot 选得好时优先**快排**。

### Q: Why is insertion sort still useful if it’s O(n²)?

**A**: On **tiny** or **nearly sorted** ranges it has excellent constants and is **adaptive** (best case O(n)). Many production sorts use it as a **hybrid base case** after a cutoff threshold.

在**极小**或**近乎有序**区间上常数优秀且**自适应**（最优 O(n)）。许多生产级排序在阈值以下用它作**混合基例**。

### Q: How does heap sort achieve O(n log n) with O(1) extra space?

**A**: It **builds a heap** in the array, then repeatedly **extracts** the extreme value into the sorted suffix and **sifts down** to restore the heap. No O(n) merge buffer is required—only local variables (and possibly a small recursion stack for sift).

在数组内**建堆**，再反复把极值**抽取**到有序后缀并**下沉调整**恢复堆。不需要 O(n) 归并缓冲——只需局部变量（下沉时或有少量递归栈）。

---

## Further Reading — 延伸阅读

- [Halfrost LeetCode Cookbook · Sorting](https://books.halfrost.com/leetcode/ChapterTwo/Sorting/)
- [VisuAlgo · Sorting visualization](https://visualgo.net/zh/sorting?slide=4)
- Related: **`Comparable` vs `Comparator`**, **`Arrays.sort` / TimSort**, **priority queue**, [[learning-notes/personal-english-book/study/java-collections-framework|Collections Framework]] — 相关：比较接口、JDK 排序 / TimSort、优先队列、[[learning-notes/personal-english-book/study/java-collections-framework|集合框架]]
- Source README in demo: https://github.com/zhangze2/awesome-demo/blob/master/sort/README.md

---

## Runnable demos — 可运行图式（awesome-java-demo）

**Bridge:** [[learning-notes/personal-english-book/study/awesome-java-demo-bridge|awesome-java-demo bridge]]

| Topic | Demo class | Run (demo repo root) |
|-------|------------|----------------------|
| Bubble / Shell / Improved* | via `SortUtil` / tests | `mvn -pl sort test` |
| Selection Sort | `sort.SelectionSort` | `mvn -pl sort test` · `SelectionSortTest` |
| Insertion Sort | `sort.InsertSort` | `mvn -pl sort test` · `InsertSortTest` |
| Quick Sort | `sort.QuickSort` | `mvn -pl sort test` · `QuickSortTest` |
| Merge Sort | `sort.MergeSort` | `mvn -pl sort test` · `MergeSortTest` |
| Heap Sort | `sort.HeapSort` | see class `main` / module tests |

```bash
cd sort && mvn test
# or from awesome-java-demo repo root
mvn -pl sort test
```

**English README (demo):** https://github.com/zhangze2/awesome-demo/blob/master/sort/README.md

**Tags**: `技术`, `Java`, `排序`, `算法`, `复杂度`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Stable sorts keep equal keys in order.** — 稳定排序保持相等键的顺序。
- **Insertion sort wins on tiny ranges.** — 插入排序在极小区间上取胜。
- **Quick sort partitions around a pivot.** — 快速排序围绕基准分区。
- **Merge sort needs an auxiliary buffer.** — 归并排序需要辅助缓冲。
- **Heap sort guarantees O(n log n) in place.** — 堆排序原地保证 O(n log n)。
- **Choose by stability, space, and input size.** — 按稳定性、空间和输入规模选型。

### B. 一段串联（连续口语）

**Stable sorts keep equal keys in order. Insertion sort wins on tiny ranges. Quick sort partitions around a pivot. Merge sort needs an auxiliary buffer. Heap sort guarantees O(n log n) in place. Choose by stability, space, and input size.**

**简中：** 稳定排序保持相等键的顺序。插入排序在极小区间上取胜。快速排序围绕基准分区。归并排序需要辅助缓冲。堆排序原地保证 O(n log n)。按稳定性、空间和输入规模选型。

### C. 一分钟复盘（5 句）

1. **Stable sorts keep equal keys in order.** — 稳定排序保持相等键的顺序。
2. **Insertion sort wins on tiny ranges.** — 插入排序在极小区间上取胜。
3. **Quick sort partitions around a pivot.** — 快速排序围绕基准分区。
4. **Merge sort needs an auxiliary buffer.** — 归并排序需要辅助缓冲。
5. **Heap sort guarantees O(n log n) in place.** — 堆排序原地保证 O(n log n)。
