---
tags:
  - personal-english-book
  - english-learning
  - peb/study
  - java
  - spring
aliases:
  - Spring Framework 学习笔记
  - Spring Framework
  - Spring
---

# Spring Framework — Spring 框架

Spring is the **de facto** standard for building **enterprise Java** applications. It **inverts control** of object creation, wires dependencies, and provides modules for web, data, and messaging—so you focus on business logic instead of plumbing.

Spring 是构建**企业级 Java** 应用的**事实标准**。它**反转**对象创建的控制权、装配依赖，并提供 Web、数据与消息等模块——让你专注业务逻辑而非基础设施胶水代码。

**索引：** [[learning-notes/personal-english-book/README|个人英文材料书索引]]

**Related:** [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]]（动态代理 ↔ AOP） · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]]（`@RestControllerAdvice`）

---

## Overview — 概述

### Spring vs Spring Boot — Spring 与 Spring Boot

| | **Spring Framework** | **Spring Boot** |
|--|----------------------|-----------------|
| Role — 角色 | Core IoC, AOP, MVC, TX — 核心容器与模块 | Opinionated starter on top of Spring — 在 Spring 之上的约定式启动器 |
| Config — 配置 | You assemble beans explicitly — 显式装配 Bean | **Auto-configuration** + starters — **自动配置** + starter 依赖 |
| Goal — 目标 | Flexible enterprise toolkit — 灵活的企业工具箱 | Fast path to a running app — 尽快跑起一个应用 |

Most production code today is **Spring Boot**, but the ideas below are **Spring Framework** fundamentals that Boot still rests on.

如今多数生产代码是 **Spring Boot**，但下面的概念仍是 Boot 所依赖的 **Spring Framework** 根基。

### Key Modules — 关键模块

1. **Core / IoC container** — 核心 / IoC 容器（Bean、依赖注入）
2. **AOP** — 面向切面编程（横切关注点）
3. **Spring MVC / WebFlux** — Web 层（Servlet 或响应式）
4. **Data access & transactions** — 数据访问与事务
5. **Spring Boot** — 自动配置、内嵌服务器、Actuator

---

## Core Concepts — 核心概念

### 1. IoC & Dependency Injection — 控制反转与依赖注入

**Inversion of control (IoC)** flips who creates and wires objects: instead of your code `new`-ing collaborators, a **container** creates beans and **injects** dependencies.

**控制反转（IoC）** 翻转「谁创建、谁装配」：不再由业务代码 `new` 协作者，而是由**容器**创建 Bean 并**注入**依赖。

**Dependency injection (DI)** is the main IoC technique in Spring: the container **supplies** required collaborators (constructor, setter, or field).

**依赖注入（DI）** 是 Spring 中主要的 IoC 手段：容器**提供**所需协作者（构造器、Setter 或字段）。

```java
// Prefer constructor injection — 优先构造器注入
@Service
public class OrderService {
    private final PaymentClient paymentClient;

    public OrderService(PaymentClient paymentClient) {
        this.paymentClient = paymentClient;
    }
}
```

**Why it matters — 意义**: loose coupling, easier testing (swap fakes), and a single place to manage object graphs — 松耦合、易测（可换假实现）、对象图集中管理。

Traditional flow: **your code calls libraries**. With IoC: **the framework calls your code** and hands you ready-made collaborators.

传统：业务代码调用库。IoC：框架调用你的代码，并交给你已装配好的协作者。

### 2. Beans & ApplicationContext — Bean 与应用上下文

A **bean** is an object managed by the Spring container. The **`ApplicationContext`** is the central IoC interface: it loads configuration, creates beans, and serves as a rich factory.

**Bean** 是由 Spring 容器管理的对象。**`ApplicationContext`** 是核心 IoC 接口：加载配置、创建 Bean，并充当功能丰富的工厂。

| Interface | Role | 作用 |
|-----------|------|------|
| **`BeanFactory`** | Basic container — 基础容器 | getBean, lazy by default — 默认惰性 |
| **`ApplicationContext`** | Full-featured IoC — 完整 IoC | Events, i18n, eager singleton load — 事件、国际化、单例预加载 |

You rarely call `getBean` in app code; you **declare** dependencies and let the container inject them.

应用代码很少直接 `getBean`；通常**声明**依赖，让容器注入。

### 3. Configuration Styles — 配置方式

| Style | Example | Notes |
|-------|---------|-------|
| **Java config** `技术` | `@Configuration` + `@Bean` | Preferred for libraries & explicit wiring — 库与显式装配首选 |
| **Component scan** `技术` | `@ComponentScan` + stereotypes | Convention over XML — 约定优于 XML |
| **XML** | `<bean …>` | Legacy; still in older codebases — 遗留；旧项目仍见 |

```java
@Configuration
@ComponentScan("com.example.app")
public class AppConfig {

    @Bean
    public Clock clock() {
        return Clock.systemUTC();
    }
}
```

### 4. Stereotype Annotations — 刻板注解（组件注解）

| Annotation | Typical layer | 典型分层 |
|------------|---------------|----------|
| **`@Component`** | Generic bean — 通用组件 | any |
| **`@Service`** | Business logic — 业务逻辑 | service |
| **`@Repository`** | Data access (+ persistence exception translation) — 数据访问（含持久化异常转换） | dao |
| **`@Controller` / `@RestController`** | Web endpoints — Web 端点 | web |

`@RestController` = `@Controller` + `@ResponseBody` — every method writes the response body (usually JSON).

`@RestController` = `@Controller` + `@ResponseBody`——方法返回值写入响应体（通常是 JSON）。

### 5. Injection & Autowiring — 注入与自动装配

| Mechanism | Preference | 偏好 |
|-----------|------------|------|
| **Constructor injection** | **Preferred** — required deps, immutable fields — **首选**：必选依赖、字段不可变 | high |
| **Setter injection** | Optional / reconfigurable deps — 可选或可重配依赖 | medium |
| **Field `@Autowired`** | Convenient but harder to test — 省事但更难测 | avoid in new code |

```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    private final OrderService orderService;

    // Single constructor: @Autowired is optional since Spring 4.3
    // 单一构造器：Spring 4.3 起可省略 @Autowired
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }
}
```

**Qualifiers — 限定符**: when multiple beans share a type, use `@Qualifier("beanName")` or `@Primary` — 同类型多 Bean 时用 `@Qualifier` 或 `@Primary`。

### 6. Bean Scopes & Lifecycle — Bean 作用域与生命周期

| Scope | Meaning | 含义 |
|-------|---------|------|
| **`singleton`** (default) | One instance per container — 每个容器一个实例 | default |
| **`prototype`** | New instance per lookup — 每次获取新建 | |
| **`request` / `session`** | Web-aware scopes — Web 作用域 | Servlet apps |

**Lifecycle hooks (simplified) — 生命周期（简化）**:

1. Instantiate — 实例化  
2. Populate properties / inject deps — 填充属性 / 注入依赖  
3. `BeanPostProcessor` / `@PostConstruct` — 后置处理 / 初始化回调  
4. Bean ready — Bean 可用  
5. `@PreDestroy` / destroy — 销毁  

```java
@Component
public class CacheWarmup {
    @PostConstruct
    void warm() { /* load cache — 预热缓存 */ }

    @PreDestroy
    void shutdown() { /* flush — 刷盘 / 释放 */ }
}
```

### 7. AOP — 面向切面编程

**Aspect-oriented programming (AOP)** separates **cross-cutting concerns** (logging, metrics, transactions, security) from business methods via **proxies**.

**面向切面编程（AOP）** 用**代理**把**横切关注点**（日志、指标、事务、安全）从业务方法中拆开。

Spring AOP is mostly **proxy-based** (JDK interface proxy or CGLIB subclass)—same idea as in [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础 · 动态代理]].

Spring AOP 主要是**基于代理**（JDK 接口代理或 CGLIB 子类）——与 Java 基础中的动态代理同一思路。

| Term `术语` | Meaning | 中文 |
|-------------|---------|------|
| **Aspect** | Modularized cross-cut | 切面 |
| **Advice** | Action at a join point (`@Before`, `@Around`, …) | 通知 |
| **Join point** | A point during execution (method call in Spring) | 连接点 |
| **Pointcut** | Expression matching join points | 切点 |
| **Proxy** | Object wrapping the target | 代理 |

**Pitfall — 注意**: self-invocation inside the same class **bypasses** the proxy—`@Transactional` / `@Async` on an internal call may not run. Extract to another bean or use AspectJ weaving.

同类内部自调用会**绕过**代理——内部调用上的 `@Transactional` / `@Async` 可能不生效。抽到另一个 Bean，或用 AspectJ 织入。

### 8. Spring MVC (Web) — Spring MVC（Web）

A request hits the **`DispatcherServlet`**, which routes to a **controller**, runs the method, and writes the response (view or body).

请求进入 **`DispatcherServlet`**，路由到**控制器**，执行方法并写出响应（视图或响应体）。

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public UserDto get(@PathVariable long id) {
        return userService.find(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDto create(@Valid @RequestBody CreateUserRequest req) {
        return userService.create(req);
    }
}
```

Global API errors: `@RestControllerAdvice` + `@ExceptionHandler` — see [[learning-notes/personal-english-book/study/java-exception-handling|异常处理 · 全局异常处理]].

全局 API 错误：`@RestControllerAdvice` + `@ExceptionHandler`——见异常处理笔记。

### 9. Transactions — 事务

`@Transactional` starts a transaction around a method (usually on a **proxy**). Default: rollback on **unchecked** exceptions (`RuntimeException`).

`@Transactional` 在方法外开启事务（通常经**代理**）。默认：对**非检查**异常（`RuntimeException`）回滚。

```java
@Service
public class TransferService {

    @Transactional
    public void transfer(long fromId, long toId, BigDecimal amount) {
        accountRepo.debit(fromId, amount);
        accountRepo.credit(toId, amount);
    }
}
```

**Tips — 要点**:

- Put `@Transactional` on **public** methods of Spring beans (proxy limitation) — 标在 Spring Bean 的 **public** 方法上（代理限制）
- Prefer **service** layer over repository/controller — 优先放在 **service** 层
- Tune `propagation`, `isolation`, `readOnly` when needed — 必要时调整传播、隔离级别、`readOnly`
- For checked exceptions: `rollbackFor = Exception.class` — 检查异常需显式 `rollbackFor`

### 10. Profiles & Externalized Config — Profile 与外部化配置

**Profiles** activate environment-specific beans (`dev`, `test`, `prod`). **Properties** / YAML externalize URLs, credentials, feature flags.

**Profile** 激活环境相关 Bean（`dev` / `test` / `prod`）。**Properties** / YAML 外部化 URL、凭证、功能开关。

```java
@Configuration
@Profile("prod")
public class ProdMailConfig { /* real SMTP — 真实 SMTP */ }

// application.yml
// spring.profiles.active: dev
```

Spring Boot: `application.properties` / `application.yml`, plus env vars and command-line args with clear **override order**.

Spring Boot：`application.properties` / `application.yml`，再叠加环境变量与命令行参数（有明确**覆盖顺序**）。

### 11. Spring Boot Essentials — Spring Boot 要点

| Idea `技术` | What it means | 含义 |
|-------------|----------------|------|
| **Starters** | Curated dependency sets (`spring-boot-starter-web`) | 精选依赖集合 |
| **Auto-configuration** | Beans created from classpath + properties | 按类路径与配置自动建 Bean |
| **Embedded server** | Tomcat/Netty inside the JAR | JAR 内嵌服务器 |
| **Actuator** | Health, metrics, info endpoints | 健康检查与指标端点 |

```java
@SpringBootApplication  // @Configuration + @EnableAutoConfiguration + @ComponentScan
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

---

## Vocabulary — 词汇表

| Term | IPA（美） | 中文 | Definition |
|------|-----------|------|------------|
| **IoC** | /ˌaɪ oʊ ˈsiː/ | 控制反转 | Framework owns the call flow and object wiring |
| **Dependency injection** | /dɪˈpendənsi ɪnˈdʒekʃən/ | 依赖注入 | Container supplies collaborators to a bean |
| **Bean** | /biːn/ | Bean / 组件 | An object managed by the Spring container |
| **Application context** | /ˌæplɪˈkeɪʃən ˈkɑːntekst/ | 应用上下文 | Full IoC container API in Spring |
| **Wire / wiring** | /waɪr/ | 装配 | Connecting beans to their dependencies |
| **Stereotype** | /ˈsteriətaɪp/ | 刻板注解 | Layer annotation like `@Service` |
| **Autowired** | /ˈɔːtoʊˌwaɪərd/ | 自动装配的 | Injected by type (and qualifier) |
| **Singleton** | /ˈsɪŋɡəltən/ | 单例 | One shared instance per container |
| **Prototype** | /ˈproʊtətaɪp/ | 原型 | New instance each time you ask |
| **AOP** | /ˌeɪ oʊ ˈpiː/ | 面向切面编程 | Modularizing cross-cutting concerns |
| **Aspect** | /ˈæspekt/ | 切面 | A module that implements cross-cuts |
| **Advice** | /ədˈvaɪs/ | 通知 | Code that runs at matched join points |
| **Pointcut** | /ˈpɔɪntkʌt/ | 切点 | Expression selecting join points |
| **Proxy** | /ˈprɑːksi/ | 代理 | Wrapper that intercepts calls |
| **Cross-cutting concern** | /krɔːs ˈkʌtɪŋ kənˈsɜːrn/ | 横切关注点 | Logic that spans many modules |
| **DispatcherServlet** | /dɪˈspætʃər ˈsɜːrvlet/ | 前端控制器 | Front controller for Spring MVC |
| **Transactional** | /trænˈzækʃənəl/ | 事务性的 | Runs inside a DB transaction boundary |
| **Propagation** | /ˌprɑːpəˈɡeɪʃən/ | 传播行为 | How nested `@Transactional` calls join/create TX |
| **Profile** | /ˈproʊfaɪl/ | 配置档 | Named set of beans/properties per environment |
| **Auto-configuration** | /ˈɔːtoʊ kənˌfɪɡjəˈreɪʃən/ | 自动配置 | Boot creates beans from classpath cues |
| **Starter** | /ˈstɑːrtər/ | 启动器依赖 | Opinionated dependency BOM for a feature |
| **Actuator** | /ˈæktʃueɪtər/ | 执行器 / 运维端点 | Production-ready ops endpoints |

---

## Common Interview Questions — 常见面试问题

### Q1 · What is Spring Framework?

**A:** Spring makes it easy to create **Java enterprise applications**. It provides everything you need to embrace the Java language in an enterprise environment, with support for Groovy and Kotlin as alternative languages on the JVM, and with the flexibility to create many kinds of architectures depending on an **application’s** needs.

Spring 让开发 Java 企业应用更简单；在 JVM 上支持 Java，并可用 Groovy、Kotlin；可按应用需求搭不同架构。

### Q2 · What is IoC (inversion of control)?

**A:** IoC **inverts the flow of control** versus traditional procedural code. Custom code receives control from a **generic framework**: the framework **calls into** your task-specific code and often **injects** collaborators (DI), instead of your code owning every `new` and library call.

IoC 把「谁调用谁」反过来：传统写法是业务代码去调通用库；IoC 下常由框架来调你写的业务代码，并注入协作者（DI）。

### Q3 · IoC vs DI — are they the same?

**A:** **IoC** is the broader principle (framework owns the flow). **DI** is the concrete mechanism Spring uses to supply dependencies. DI is a form of IoC; Spring’s container is an IoC container that performs DI.

**IoC** 是更宽的原则（框架掌控流程）。**DI** 是 Spring 供给依赖的具体机制。DI 是 IoC 的一种形式；Spring 容器是执行 DI 的 IoC 容器。

### Q4 · Why prefer constructor injection?

**A:** Required dependencies are **explicit** and fields can be `final` (**immutable**). The object is always fully initialized; unit tests can `new` the class with mocks without Spring. Field injection hides deps and complicates testing.

必选依赖**显式**，字段可 `final`（**不可变**）。对象始终完整初始化；单测可直接 `new` 并传入 mock，无需启动 Spring。字段注入隐藏依赖、增加测试成本。

### Q5 · How does `@Transactional` work?

**A:** Spring creates a **proxy** around the bean. External calls hit the proxy, which opens a transaction, invokes the method, then commits or rolls back. **Self-invocation** skips the proxy, so the annotation may not apply.

Spring 在 Bean 外包一层**代理**。外部调用先经代理：开事务 → 调方法 → 提交或回滚。**自调用**绕过代理，注解可能不生效。

### Q6 · JDK proxy vs CGLIB in Spring AOP?

**A:** If the bean implements an **interface**, Spring may use a **JDK dynamic proxy**. If there is no suitable interface (or CGLIB is forced), Spring subclasses the class with **CGLIB**. `final` classes/methods resist CGLIB interception.

若 Bean 实现了**接口**，可用 **JDK 动态代理**；否则（或强制 CGLIB）用 **CGLIB** 生成子类。`final` 类/方法难以被 CGLIB 拦截。

### Q7 · What is the difference between `@Component`, `@Service`, and `@Repository`?

**A:** All mark a class for **component scanning**. Semantically they document the **layer**. `@Repository` additionally enables **persistence exception translation** into Spring’s `DataAccessException` hierarchy.

三者都会被**组件扫描**。语义上标注**分层**。`@Repository` 额外支持把持久化异常**转换**为 Spring 的 `DataAccessException` 体系。

### Q8 · Singleton bean and thread safety?

**A:** The default scope is **singleton**—one instance shared by all requests. The bean itself must be **stateless** or carefully synchronized; put request state in method locals, `ThreadLocal`, or request-scoped beans—not in mutable singleton fields.

默认作用域是**单例**——所有请求共享一个实例。Bean 应**无状态**或仔细同步；请求状态放方法局部变量、`ThreadLocal` 或 request 作用域 Bean，不要放可变单例字段。

### Q9 · BeanFactory vs ApplicationContext?

**A:** `BeanFactory` is the minimal IoC SPI. `ApplicationContext` extends it with **enterprise features**: internationalization, event publishing, easier integration, and typically **eager** singleton initialization. Prefer `ApplicationContext` in applications.

`BeanFactory` 是最小 IoC SPI。`ApplicationContext` 扩展了**企业特性**：国际化、事件发布、更易集成，且通常**预加载**单例。应用中优先用 `ApplicationContext`。

### Q10 · What does Spring Boot auto-configuration do?

**A:** Boot looks at the **classpath**, existing beans, and properties, then **conditionally** registers sensible defaults (e.g. a `DataSource` when a DB driver is present). You override by defining your own bean or changing properties.

Boot 根据**类路径**、已有 Bean 与配置项，**有条件地**注册合理默认（例如存在数据库驱动时配置 `DataSource`）。可通过自定义 Bean 或改配置覆盖。

---

## Further Reading — 延伸阅读

- [Spring Framework Reference](https://docs.spring.io/spring-framework/reference/)
- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Baeldung: Spring IoC](https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring)
- [Baeldung: Spring AOP](https://www.baeldung.com/spring-aop)
- Related: [[learning-notes/personal-english-book/study/java-fundamentals|Java 基础]] · [[learning-notes/personal-english-book/study/java-exception-handling|异常处理]] · [[learning-notes/personal-english-book/study/java-concurrency|并发]] · [[learning-notes/personal-english-book/study/jvm-internals|JVM 内部机制]]

**Tags**: `技术`, `Java`, `Spring`, `IoC`, `AOP`, `Spring Boot`

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 词汇来自上文 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Spring inverts control and injects dependencies.** — Spring 反转控制权并注入依赖。
- **Prefer constructor injection for required collaborators.** — 必选协作者优先用构造器注入。
- **AOP wraps cross-cutting concerns with proxies.** — AOP 用代理包装横切关注点。
- **Transactional methods need an external call through the proxy.** — 事务方法需经代理的外部调用。
- **Spring Boot auto-configures beans from the classpath.** — Spring Boot 根据类路径自动配置 Bean。

### B. 一段串联（连续口语）

**Spring inverts control and injects dependencies. Prefer constructor injection for required collaborators. AOP wraps cross-cutting concerns with proxies. Transactional methods need an external call through the proxy. Spring Boot auto-configures beans from the classpath.**

**简中：** Spring 反转控制权并注入依赖。必选协作者优先用构造器注入。AOP 用代理包装横切关注点。事务方法需经代理的外部调用。Spring Boot 根据类路径自动配置 Bean。

### C. 一分钟复盘（5 句）

1. **Spring inverts control and injects dependencies.** — Spring 反转控制权并注入依赖。
2. **Prefer constructor injection for required collaborators.** — 必选协作者优先用构造器注入。
3. **AOP wraps cross-cutting concerns with proxies.** — AOP 用代理包装横切关注点。
4. **Transactional methods need an external call through the proxy.** — 事务方法需经代理的外部调用。
5. **Spring Boot auto-configures beans from the classpath.** — Spring Boot 根据类路径自动配置 Bean。
