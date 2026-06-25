# 知识库使用文档

## 写一篇文章

### 基本步骤

1. 在 `source/` 下选择对应分类目录
2. 创建文件，命名格式：`YYYY-MM-DD-slug.md`
3. 添加 frontmatter 和内容
4. `git add → git commit → git push`，自动部署

### 最小示例

```markdown
---
author: 晚吟
tags:
  - freertos
  - 任务调度
---

```{post} 2026-06-25
```

# FreeRTOS 任务调度笔记

正文内容...
```

### 文件名规范

```
YYYY-MM-DD-短标题.md

示例：
2026-06-25-freertos-task-scheduling.md   ✅
2026-06-25-stm32-点亮led.md              ✅
freertos-notes.md                        ❌ 缺少日期
20260625-notes.md                        ❌ 日期格式错误
```

日期从文件名自动提取，作为文章的发布日期。

## Frontmatter 参考

Frontmatter 是文章开头的 YAML 元数据块，用 `---` 包裹。

### 完整示例

```yaml
---
author: 晚吟
tags:
  - stm32
  - gpio
  - 踩坑
  - 入门
---
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `author` | 否 | 作者名，默认 `晚吟` |
| `tags` | 否 | 标签列表，用于跨分类检索和标签页聚合 |

### `{post}` 指令

每篇文章**必须**在正文开头（frontmatter 之后、标题之前或之后）包含 `{post}` 指令，用于将文章注册为博客文章：

```markdown
```{post} 2026-06-25
```
```

日期应与文件名中的日期一致。

## 分类与标签

### 分类（目录）

分类由文章的**文件路径**决定，一篇文章只属于一个分类。

| 目录 | 分类名 | 适用内容 |
|------|--------|---------|
| `embedded/mcu/` | mcu | STM32、ESP32 等单片机开发 |
| `embedded/rtos/` | rtos | FreeRTOS、RT-Thread 等 |
| `embedded/linux/` | linux | 嵌入式 Linux、驱动、Yocto |
| `embedded/hardware/` | hardware | 原理图、PCB、硬件设计 |
| `embedded/toolchain/` | toolchain | 编译工具链、调试器、CI |
| `cs/` | cs | 数据结构、算法、网络、操作系统 |
| `tools/` | tools | 开发环境、效率工具、脚本 |
| `career/` | career | 工作经历、项目复盘、面试 |
| `life/` | life | 阅读、旅行、日常感悟 |

### 标签

标签在 frontmatter 中自由定义，一篇文章可以有多个标签。标签用于**跨分类**的精细检索。

标签聚合页面自动生成在 `blog/tag/<标签名>.html`。

### 使用建议

- **大类用目录**：这篇文章属于哪个领域，就放哪个目录
- **细粒度用标签**：具体的芯片型号、技术点、文章类型（踩坑/教程/复盘）
- **标签尽量复用**：用已有的标签名可以形成聚合页面，避免 `stm32` 和 `STM32` 这种大小写不一致

推荐的标签体系：

```
技术栈：    stm32, esp32, freertos, rt-thread, linux-kernel, yocto, c, cpp, python
文章类型：  教程, 踩坑, 笔记, 项目复盘, 译文
工具：      gdb, openocd, cmake, docker, vscode
```

## Markdown 写作语法

### 基础语法

支持标准 Markdown：标题、列表、链接、图片、代码块、表格等。

### MyST 扩展语法

#### Admonition（提示框）

```markdown
:::{note}
这是一个提示框。
:::

:::{warning}
这是一个警告框。
:::

:::{tip}
这是一个小技巧。
:::

:::{seealso}
参见相关文档。
:::
```

支持的 admonition 类型：`note`、`warning`、`tip`、`important`、`caution`、`seealso`、`hint`、`attention`、`danger`、`error`。

#### 代码块（带高亮和标题）

````markdown
```{code-block} c
:caption: GPIO 初始化代码
:linenos:

void gpio_init(void) {
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    // ...
}
```
````

#### 数学公式

```markdown
行内公式：$f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} F(\omega) e^{i\omega t} d\omega$

独立公式：

$$F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt$$
```

#### 图片

```markdown
![图片描述](path/to/image.png)

# 带标题
```{image} path/to/image.png
:alt: 图片描述
:width: 600px
:align: center
```
```

#### 表格

```markdown
| 寄存器 | 地址 | 说明 |
|--------|------|------|
| GPIOA_CRL | 0x40010800 | 端口配置低寄存器 |
| GPIOA_CRH | 0x40010804 | 端口配置高寄存器 |
```

#### 交叉引用

```markdown
参考 [FreeRTOS 任务调度笔记](./freertos-task-scheduling.md)。
```

#### 卡片组件（sphinx-design）

```markdown
::::{grid} 2
:gutter: 2

:::{grid-item-card} 标题
内容文字
:::

:::{grid-item-card} 标题2
内容文字
:::
::::
```

## 图片管理

推荐将图片放在文章同目录下：

```
source/embedded/mcu/
├── 2026-06-25-hello-stm32.md
└── images/
    └── stm32-pinout.png
```

文章中引用：

```markdown
![STM32 引脚图](images/stm32-pinout.png)
```

## 草稿与私有内容

### 草稿（drafts/）

放在 `source/drafts/` 目录下，不会出现在公开站点中。

适合：
- 未完成的文章
- 需要反复修改的笔记
- 暂时不确定要不要发表的思考

本地预览草稿：临时注释 `conf.py` 中 `exclude_patterns` 里的 `'drafts/*'`，构建后即可看到。

### 私有内容（private/）

放在 `source/private/` 目录下，同样不会出现在公开站点中。

适合：
- 包含敏感信息的工作记录
- 个人日记
- 不便公开的技术细节

> **安全提示：** `private/` 内容仍然存在于 Git 仓库中。如果你的仓库是公开的，请确保 `private/` 中没有真正的敏感信息。必要时使用私有仓库或单独的私有仓库存放。

## 文章模板

### 技术笔记模板

```markdown
---
author: 晚吟
tags:
  - <芯片/技术>
  - 笔记
---

```{post} YYYY-MM-DD
```

# <标题>

## 背景

为什么要做这个，遇到了什么问题。

## 环境

- 硬件：
- 软件：
- 工具链：

## 过程

### 步骤 1

...

### 步骤 2

...

```代码块```

## 踩坑记录

1. **问题描述**：原因 → 解决方案

## 参考

- [链接标题](https://example.com)
```

### 项目复盘模板

```markdown
---
author: 晚吟
tags:
  - 项目复盘
  - <技术栈>
---

```{post} YYYY-MM-DD
```

# <项目名> 复盘

## 项目概述

- 时间：
- 团队：
- 目标：

## 技术方案

## 做得好的

## 可以改进的

## 经验总结
```

## RSS 订阅

站点自动生成 Atom Feed，地址：

```
https://qznkzs.github.io/knowledgesystem.github.io/blog/atom.xml
```

可以使用任意 RSS 阅读器订阅（如 Feedly、Inoreader、NetNewsWire 等）。
