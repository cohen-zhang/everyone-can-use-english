# IntelliJ IDEA — Video script (developer voice, English)

> **Use:** Read aloud or teleprompter. Pauses marked with `/`. Casual, not a manual.

---

## Opening (hook)

Hey — if you ship Java or Kotlin for a living, you’ve probably spent more hours in **IntelliJ IDEA** than in your actual IDE-themed dreams. / Let’s walk through what matters: the UI names you’ll hear in tutorials, the menus you’ll actually click when things break, and the features that quietly save your sanity.

---

## What it is (in one breath)

**IntelliJ IDEA** is JetBrains’ flagship IDE for the JVM ecosystem — think Java, Kotlin, Gradle, Spring, Android, and a pile of frameworks baked in. / It’s not “just an editor”; it’s a **refactoring machine** with a debugger glued to the side. Fair warning: once you get used to it, going back to a plain text editor feels… wrong.

---

## The UI — where everything lives

**Settings** — This is mission control. Editor style, plugins, keymaps — if the IDE annoys you, the fix is probably here. / Real talk: you’ll open this menu more often than you admit.

**Project Structure** — Modules, libraries, SDKs — the skeleton of your app. / When imports go weird or the wrong JDK is selected, this is where you land.

**File Properties** — Metadata for the file you’ve got selected. Quick sanity check before you blame Git for something local.

**Local History** — IDEA quietly snapshots your edits. / Deleted something dumb an hour ago? This is your “oops” button before you panic.

**Appearance & Behavior** — Themes, fonts, window behavior — make it look less like a 2005 spreadsheet if you want.

**Keymap** — Your shortcuts live here. / Pro tip: pick one scheme and stop — muscle memory beats “optimized” layouts every time.

**Editor** — Code completion, auto-import, inspections — the nerdy heart of the product. / This is where “it feels slow” usually gets fixed.

**Plugins** — Extra languages, themes, tools. / Install what you need; too many plugins = startup time from another dimension.

**Version Control** — Git integration settings — how diffs look, what gets ignored, the usual.

**Build, Execution, Deployment** — Run configs, compilers, deployment targets. / When “it runs on my machine” fails, start here.

**Languages & Frameworks** — Spring, JPA, SQL dialects — framework-specific magic lives in this bucket.

**Tools** — External tools, terminal, database viewers — the grab bag of utilities.

**Other Settings** — The junk drawer. Still worth peeking when you can’t find something anywhere else.

---

## Operations — stuff you actually click

**Save All** — Flush every dirty buffer to disk. / Old habit from other editors; still useful before you switch branches.

**Reload All from Disk** — Disk won out over the editor — force the IDE to trust the filesystem again. / Handy after a messy `git checkout` or script rewrite.

**Repair IDE** — When the IDE itself feels broken, this tries to patch itself up. / First aid before the nuclear option.

**Invalidate Caches** — “Turn it off and on again,” IDE edition. / Clears internal caches; you’ll restart, grab coffee, come back — often fixes phantom red squiggles.

**Manage IDE Settings** — Export, import, or reset your setup. / New laptop day? This is how you clone your comfort zone.

**New Projects Setup** — Defaults for fresh projects — JDK, code style, plugins. / Saves you from repeating the same five clicks forever.

**Save File as Template** — Turn a file into a reusable starter. / Great for boilerplate you’re tired of typing.

**Export** — Ship something out of the IDE — project bits, settings, whatever the dialog offers.

**Print** — Yes, people still print. / Maybe your PM, not you — but the option’s there.

**Power Save Mode** — Throttles background work to save battery. / On a long flight, your laptop might thank you.

**Exit** — Done for today. / Close IDEA before the fan sounds like a jet engine.

---

## Features — why we put up with the RAM usage

**Auto Import** — Types in scope without hand-writing `import` lines all day. / When it works, you barely notice; when it doesn’t, you notice *loudly*.

**Code Completion** — Tab your way through APIs instead of memorizing every package. / Case sensitivity settings matter — don’t fight the defaults unless you enjoy pain.

**Breadcrumbs** — Little trail above the editor: where you are in the class or file. / Navigation without losing the forest for the trees.

**Code Folding** — Collapse methods and blocks so your screen isn’t 90% boilerplate. / Fold, skim, unfold — you know the drill.

**Console** — Run output, test output, logs — soft wraps here mean long lines don’t wreck your layout. / Readable stack traces > horizontal scrolling.

---

## Closing (sign-off)

That’s the map — **Settings** when something feels off, **Invalidate Caches** when the universe is wrong, **Project Structure** when the build is lying to you. / IDEA’s a beast, but once it clicks, you’re not “typing code” — you’re **moving through a codebase** with guardrails. / Now go break something and let Local History save you.

---

---

# 附录：界面 / 操作 / 功能 — 中英文关键词（原笔记整理）

## 一、界面相关


| English                      | 中文             |
| ---------------------------- | -------------- |
| Settings                     | 设置：编辑器、插件、快捷键等 |
| Project Structure            | 项目结构：模块、库、SDK  |
| File Properties              | 文件属性           |
| Local History                | 本地历史：恢复与对比     |
| Appearance & Behavior        | 外观与行为：主题、字体等   |
| Keymap                       | 快捷键方案          |
| Editor                       | 编辑器相关设置        |
| Plugins                      | 插件             |
| Version Control              | 版本控制           |
| Build, Execution, Deployment | 构建、执行、部署       |
| Languages & Frameworks       | 语言与框架          |
| Tools                        | 工具集            |
| Other Settings               | 其它配置           |


## 二、操作相关


| English               | 中文         |
| --------------------- | ---------- |
| Save All              | 保存所有       |
| Reload All from Disk  | 从磁盘重新加载    |
| Repair IDE            | 修复 IDE     |
| Invalidate Caches     | 清理缓存（常需重启） |
| Manage IDE Settings   | 导入/导出/重置设置 |
| New Projects Setup    | 新项目默认配置    |
| Save File as Template | 文件存为模板     |
| Export / Print        | 导出 / 打印    |
| Power Save Mode       | 省电模式       |
| Exit                  | 退出         |


## 三、功能特性


| English         | 中文                |
| --------------- | ----------------- |
| Auto Import     | 自动导入              |
| Code Completion | 代码补全              |
| Breadcrumbs     | 面包屑导航             |
| Code Folding    | 代码折叠              |
| Console         | 控制台（如 soft wraps） |


**参考资料（原链）：** CSDN 等 IDEA 英文界面与配置笔记（File 菜单、Editor 配置、Version Control 等）。