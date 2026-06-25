# 个人知识库 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 Sphinx + MyST + ABlog + GitHub Pages 搭建个人知识库，包含博客风格首页、分类/标签系统、CI/CD 自动部署。

**Architecture:** Sphinx 作为构建引擎，MyST-Parser 解析 Markdown，ABlog 扩展提供博客功能（文章列表、分类、标签、归档、RSS），pydata_sphinx_theme 提供现代主题，GitHub Actions 自动构建部署到 GitHub Pages。

**Tech Stack:** Python 3, Sphinx 7+, MyST-Parser 3+, ABlog 0.11+, pydata-sphinx-theme 0.15+, sphinx-design 0.5+

---

## File Map

| 文件 | 职责 | 操作 |
|------|------|------|
| `requirements.txt` | 声明 Python 依赖 | Create |
| `.gitignore` | 排除构建产物和 Python 缓存 | Create |
| `.github/workflows/deploy.yml` | CI/CD 自动构建部署 | Create |
| `source/conf.py` | Sphinx 核心配置（扩展、主题、ABlog、排除规则） | Create |
| `source/index.md` | 首页，使用 ABlog postlist 指令展示文章列表 | Create |
| `source/_templates/postlist.html` | 覆写 ABlog 博客列表模板，卡片流布局 | Create |
| `source/_templates/recent.html` | 覆写 ABlog 最近文章侧边栏组件 | Create |
| `source/_static/custom.css` | 自定义样式，博客卡片、标签徽章、排版微调 | Create |
| `README.md` | 项目说明，本地构建和写作指南 | Modify |

---

### Task 1: Python 依赖文件

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: 创建 requirements.txt**

```text
sphinx>=7.0
myst-parser>=3.0
ablog>=0.11
pydata-sphinx-theme>=0.15
sphinx-design>=0.5
```

- [ ] **Step 2: 安装依赖验证**

Run: `pip install -r requirements.txt`
Expected: 所有包安装成功，无版本冲突。

- [ ] **Step 3: 创建 .gitignore**

```
# Sphinx 构建产物
build/

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 4: 提交**

```bash
git add requirements.txt .gitignore
git commit -m "chore: add Python dependencies and .gitignore"
```

---

### Task 2: Sphinx 核心配置

**Files:**
- Create: `source/conf.py`

- [ ] **Step 1: 创建 source/conf.py**

```python
# Sphinx 个人知识库配置文件

import os
import sys

# -- 项目信息 -----------------------------------------------------

project = '晚吟的知识库'
author = '晚吟'
copyright = '2026, 晚吟'
language = 'zh_CN'

# -- 通用配置 -----------------------------------------------------

extensions = [
    'myst_parser',
    'ablog',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_design',
]

master_doc = 'index'

# 文件后缀映射：.md 用 MyST 解析
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# 排除不在公开站点出现的目录
exclude_patterns = [
    'private/*',
    'drafts/*',
    '_templates/*',
]

# -- MyST-Parser 配置 ---------------------------------------------

myst_enable_extensions = [
    'dollarmath',
    'colon_fence',
    'substitution',
]

myst_heading_anchors = 3

# MyST 通用 frontmatter 字段（用于 ABlog）
myst_footnote_transition = True

# -- ABlog 博客配置 -----------------------------------------------

# 博客路径前缀
blog_path = 'blog'
blog_title = '晚吟的知识库'
blog_baseurl = 'https://<YOUR_USERNAME>.github.io/knowledge-base/'

# 文章作者
blog_authors = {
    '晚吟': ('晚吟', None),
}
blog_default_author = '晚吟'

# 语言映射
blog_languages = {
    'zh': ('中文', 'zh'),
}

# 从文件名自动提取日期（YYYY-MM-DD-slug 格式）
# ABlog 默认支持此行为，无需额外配置

# -- HTML 输出配置 -------------------------------------------------

html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    'show_toc_level': 2,
    'navbar_align': 'left',
    'navbar_start': ['navbar-logo'],
    'navbar_center': ['navbar-nav'],
    'navbar_end': ['navbar-icon-links'],
    'secondary_sidebar_items': ['page-toc', 'ablog/recent.html'],
    'footer_start': ['copyright'],
    'footer_end': ['theme-version'],
    'github_url': 'https://github.com/<YOUR_USERNAME>/knowledge-base',
    'icon_links': [],
}

html_static_path = ['_static']
templates_path = ['_templates']

html_css_files = [
    'custom.css',
]

# 侧边栏配置
html_sidebars = {
    'blog/**': [
        'ablog/postcard.html',
        'ablog/recent.html',
        'ablog/tagcloud.html',
        'ablog/archives.html',
    ],
    '**': [
        'search-field.html',
        'sidebar-nav-bs.html',
        'ablog/recent.html',
    ],
}

# -- Intersphinx --------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- TODO 扩展 ----------------------------------------------------

todo_include_todos = False
```

- [ ] **Step 2: 提交**

```bash
git add source/conf.py
git commit -m "feat: add Sphinx core configuration"
```

---

### Task 3: 自定义 ABlog 模板 —— 博客列表页

**Files:**
- Create: `source/_templates/postlist.html`

**说明：** 覆写 ABlog 默认的博文列表模板，实现卡片流布局（标题 + 日期 + 标签 + 摘要，网格排列）。

- [ ] **Step 1: 创建 source/_templates/postlist.html**

```html
{% extends "page.html" %}

{% block body %}
<div class="ablog-bloglist">

  {% if ablog %}
    <div class="blog-card-grid">
      {% for post in ablog %}
        <article class="blog-card">
          <header class="blog-card-header">
            <h2 class="blog-card-title">
              <a href="{{ pathto(post.docname) }}{{ anchor(post) }}">{{ post.title }}</a>
            </h2>
            <div class="blog-card-meta">
              {% if post.date %}
                <time class="blog-card-date" datetime="{{ post.date.isoformat() }}">
                  {{ post.date.strftime('%Y-%m-%d') }}
                </time>
              {% endif %}
              {% if post.category %}
                <span class="blog-card-category">
                  <a href="{{ pathto(blog_path) }}/category/{{ post.category }}.html">
                    {{ post.category }}
                  </a>
                </span>
              {% endif %}
            </div>
          </header>

          {% if post.excerpt %}
            <div class="blog-card-excerpt">
              {{ post.excerpt }}
            </div>
          {% endif %}

          {% if post.tags %}
            <footer class="blog-card-footer">
              <div class="blog-card-tags">
                {% for tag in post.tags %}
                  <a href="{{ pathto(blog_path) }}/tag/{{ tag }}.html"
                     class="blog-tag">#{{ tag }}</a>
                {% endfor %}
              </div>
            </footer>
          {% endif %}
        </article>
      {% endfor %}
    </div>
  {% else %}
    <p>暂无文章。</p>
  {% endif %}

</div>
{% endblock %}
```

- [ ] **Step 2: 创建 source/_templates/recent.html**（最近文章侧边栏）

```html
<div class="ablog-sidebar-item">
  <h3 class="ablog-sidebar-title">
    <a href="{{ pathto(blog_path) }}">📝 最近文章</a>
  </h3>
  <ul class="ablog-recent-posts">
    {% set recent_posts = ablog.recent(10, paths=['blog']) %}
    {% for p in recent_posts %}
      <li>
        <a href="{{ pathto(p.docname) }}{{ anchor(p) }}">{{ p.title }}</a>
        {% if p.date %}
          <span class="recent-post-date">{{ p.date.strftime('%m-%d') }}</span>
        {% endif %}
      </li>
    {% endfor %}
  </ul>
</div>
```

- [ ] **Step 3: 提交**

```bash
git add source/_templates/
git commit -m "feat: add custom ABlog templates for blog cards and recent posts"
```

---

### Task 4: 自定义 CSS 样式

**Files:**
- Create: `source/_static/custom.css`

- [ ] **Step 1: 创建 source/_static/custom.css**

```css
/* ================================================================
   个人知识库自定义样式
   ================================================================ */

/* -- 博客卡片网格 ------------------------------------------------- */
.blog-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin: 1rem 0 2rem;
}

/* -- 单张博客卡片 ------------------------------------------------- */
.blog-card {
  background: var(--pst-color-surface);
  border: 1px solid var(--pst-color-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  display: flex;
  flex-direction: column;
}

.blog-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* -- 卡片标题 ----------------------------------------------------- */
.blog-card-title {
  font-size: 1.2rem;
  margin: 0 0 0.5rem;
  line-height: 1.4;
}

.blog-card-title a {
  color: var(--pst-color-text-base);
  text-decoration: none;
}

.blog-card-title a:hover {
  color: var(--pst-color-link);
}

/* -- 卡片元信息（日期、分类） --------------------------------------- */
.blog-card-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  font-size: 0.85rem;
  color: var(--pst-color-text-muted);
  margin-bottom: 0.75rem;
}

.blog-card-date {
  white-space: nowrap;
}

.blog-card-category a {
  background: var(--pst-color-info-bg);
  color: var(--pst-color-info);
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  text-decoration: none;
}

/* -- 卡片摘要 ----------------------------------------------------- */
.blog-card-excerpt {
  font-size: 0.9rem;
  color: var(--pst-color-text-muted);
  line-height: 1.6;
  flex-grow: 1;
  margin-bottom: 0.75rem;
}

/* -- 卡片标签 ----------------------------------------------------- */
.blog-card-footer {
  margin-top: auto;
}

.blog-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.blog-tag {
  font-size: 0.78rem;
  color: var(--pst-color-link);
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.blog-tag:hover {
  opacity: 1;
  text-decoration: underline;
  color: var(--pst-color-link);
}

/* -- 侧边栏：最近文章 ---------------------------------------------- */
.ablog-sidebar-item {
  margin-bottom: 1.5rem;
}

.ablog-sidebar-title {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
  color: var(--pst-color-text-muted);
}

.ablog-sidebar-title a {
  color: inherit;
  text-decoration: none;
}

.ablog-recent-posts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ablog-recent-posts li {
  padding: 0.3rem 0;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.85rem;
  border-bottom: 1px dotted var(--pst-color-border);
}

.ablog-recent-posts li a {
  flex: 1;
  color: var(--pst-color-text-base);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ablog-recent-posts li a:hover {
  color: var(--pst-color-link);
}

.recent-post-date {
  font-size: 0.75rem;
  color: var(--pst-color-text-muted);
  margin-left: 0.5rem;
  white-space: nowrap;
}

/* -- 深色模式微调 ------------------------------------------------- */
html[data-theme="dark"] .blog-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

/* -- 响应式 ------------------------------------------------------ */
@media (max-width: 768px) {
  .blog-card-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
```

- [ ] **Step 2: 提交**

```bash
git add source/_static/custom.css
git commit -m "feat: add custom CSS for blog card layout and sidebar"
```

---

### Task 5: 首页

**Files:**
- Create: `source/index.md`

- [ ] **Step 1: 创建 source/index.md**

```
---
blog: true
---

# 晚吟的知识库

嵌入式工程师的学习、工作与思考。

---

```{postlist}
:date: "%Y-%m-%d"
:excerpts:
```

---

## 📂 分类导航

::::{grid} 2 2 3 3
:gutter: 3

:::{grid-item-card} 🔧 嵌入式
:link: blog/category/embedded
:link-type: ref

MCU · RTOS · Linux · 硬件 · 工具链
:::

:::{grid-item-card} 💻 计算机基础
:link: blog/category/cs
:link-type: ref

数据结构 · 算法 · 网络 · 操作系统
:::

:::{grid-item-card} 🛠 工具 & 效率
:link: blog/category/tools
:link-type: ref

开发环境 · 调试技巧 · 效率工具
:::

:::{grid-item-card} 💼 职业发展
:link: blog/category/career
:link-type: ref

项目复盘 · 职场思考 · 面试记录
:::

:::{grid-item-card} 🌿 生活杂谈
:link: blog/category/life
:link-type: ref

阅读 · 旅行 · 日常感悟
:::
::::
```

- [ ] **Step 2: 提交**

```bash
git add source/index.md
git commit -m "feat: add homepage with blog list and category navigation"
```

---

### Task 6: 目录结构与示例文章

**Files:**
- Create: `source/embedded/index.md`（分类索引页）
- Create: `source/embedded/mcu/2026-06-25-hello-stm32.md`（示例文章）

- [ ] **Step 1: 创建嵌入式分类索引页 source/embedded/index.md**

```
# 嵌入式

:::{toctree}
:maxdepth: 2
:glob:

mcu/*
rtos/*
linux/*
hardware/*
toolchain/*
:::
```

- [ ] **Step 2: 创建示例文章 source/embedded/mcu/2026-06-25-hello-stm32.md**

```
---
author: 晚吟
tags:
  - stm32
  - 入门
  - 踩坑
---

# STM32 入坑第一课：点亮 LED

这是我的 STM32 学习笔记第一篇文章。

## 环境准备

- 开发板：STM32F103C8T6（Blue Pill）
- 工具链：STM32CubeIDE
- 调试器：ST-Link V2

## GPIO 配置

```c
// 使能 GPIOA 时钟
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

GPIO_InitTypeDef GPIO_InitStructure;
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
GPIO_Init(GPIOA, &GPIO_InitStructure);
```

## 遇到的坑

1. **BOOT0 电平**：烧录后不运行？检查 BOOT0 是否接地
2. **调试器连接**：ST-Link 接线顺序和杜邦线质量很重要

## 小结

点亮第一个 LED 是嵌入式开发的 "Hello World"。
后续会继续记录 FreeRTOS 移植过程。
```

- [ ] **Step 3: 创建各分类目录占位符**

```bash
mkdir -p source/embedded/{mcu,rtos,linux,hardware,toolchain}
mkdir -p source/{cs,tools,career,life,drafts,private}
```

- [ ] **Step 4: 提交**

```bash
git add source/
git commit -m "feat: add category directories and sample article"
```

---

### Task 7: GitHub Actions 自动部署

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: 创建 .github/workflows/deploy.yml**

```yaml
name: Deploy Knowledge Base

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build Sphinx site
        run: sphinx-build -b html source/ build/

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'build'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: 提交**

```bash
git add .github/workflows/deploy.yml
git commit -m "feat: add GitHub Actions deploy workflow"
```

---

### Task 8: 更新 README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 重写 README.md**

```markdown
# 晚吟的知识库

嵌入式工程师的个人知识库，基于 Sphinx + MyST + ABlog 构建，托管于 GitHub Pages。

## 本地构建

```bash
# 安装依赖
pip install -r requirements.txt

# 构建站点
sphinx-build -b html source/ build/

# 本地预览
python -m http.server 8080 -d build/
```

浏览器打开 `http://localhost:8080` 查看。

## 写文章

1. 在 `source/` 下对应分类目录创建 `YYYY-MM-DD-slug.md`
2. 可选：在文件头添加 frontmatter（author, tags）
3. 正文用 Markdown，需要复杂排版可用 RST 指令
4. `git commit && git push`，自动部署

## 目录结构

- `embedded/` — 嵌入式（MCU / RTOS / Linux / 硬件 / 工具链）
- `cs/` — 计算机基础
- `tools/` — 工具 & 效率
- `career/` — 职业发展
- `life/` — 生活杂谈
- `drafts/` — 草稿（不构建）
- `private/` — 私有内容（不构建）
```

- [ ] **Step 2: 提交**

```bash
git add README.md
git commit -m "docs: update README with build and writing guide"
```

---

### Task 9: 推送并验证 GitHub Actions

- [ ] **Step 1: 推送所有代码到 GitHub**

```bash
git push origin main
```

**前置条件：** 确保 GitHub 仓库已创建，remote origin 已配置。

- [ ] **Step 2: 在 GitHub 仓库 Settings > Pages 中确认**

- Source 已自动设置为 "GitHub Actions"
- 等待 Actions workflow 完成，确认部署成功

- [ ] **Step 3: 打开部署地址验证站点**

打开 `https://<YOUR_USERNAME>.github.io/knowledge-base/`，确认：
- 首页显示博客文章列表（示例文章可见）
- 分类导航卡片可点击
- 侧边栏显示最近文章
- 标签可点击并跳转

---

## Post-Implementation 修复记录

以下为初始实现中遇到的问题及修复方案，已纳入后续执行。

### 修复 1：ABlog 模板路径

**问题：** 自定义模板 `recent.html` 放在 `_templates/` 根目录，ABlog 以 `ablog/recent.html` 查找时找不到。

**修复：** 将 ABlog 命名空间模板（recent.html）放入 `_templates/ablog/` 子目录。`postlist.html` 保留在 `_templates/` 根目录（ABlog 以 `postlist.html` 直接查找）。

### 修复 2：PyData Theme 与 ABlog 侧边栏冲突

**问题：** `pydata_sphinx_theme` 0.19.0 的 `update_and_remove_templates` 处理 `ablog/recent.html` 时抛出 `quote_from_bytes() expected bytes` 异常。

**修复：** 注释掉 `html_sidebars` 配置，不显式引用 ABlog 侧边栏模板。改为用 CSS 对 ABlog 默认 HTML 输出做卡片样式。

### 修复 3：分类链接 404 —— 核心修复

**问题：** 首页分类导航卡片链接到 `blog/category/xxx.html`，但 ABlog 不会为每个分类生成独立页面，导致 404。

**根因：**

1. ABlog 的分类（category）必须在 `{post}` 指令中通过 `:category:` 选项声明，**不能只写在 YAML frontmatter 中**
2. ABlog 不会自动为每个分类生成独立 HTML 页面
3. 需要用 `{postlist}` 指令配合 `:category:` 过滤器手动创建分类索引页

**修复步骤：**

- [ ] **F1: 修正 `{post}` 指令** —— 每篇文章的 `{post}` 指令中添加 `:category:` 选项：

````markdown
```{post} 2026-06-25
:category: tools
```
````

- [ ] **F2: 创建分类索引页** —— 每个分类目录下创建 `index.md`，用 `{postlist}` 过滤：

```markdown
# 工具 & 效率

```{postlist}
:category: tools
:date: "%Y-%m-%d"
:excerpts:
```
```

文件清单：
- `source/tools/index.md`（:category: tools）
- `source/cs/index.md`（:category: cs）
- `source/career/index.md`（:category: career）
- `source/life/index.md`（:category: life）
- `source/embedded/index.md`（保留 toctree，嵌入式有子分类不适用单 category 过滤）

- [ ] **F3: 修正首页分类卡片链接** —— 从 `blog/category/xxx.html` 改为 `xxx/index.html`：

| 卡片 | 旧链接 | 新链接 |
|------|--------|--------|
| 🔧 嵌入式 | `blog/category/embedded.html` | `embedded/index.html` |
| 💻 计算机基础 | `blog/category/cs.html` | `cs/index.html` |
| 🛠 工具 & 效率 | `blog/category/tools.html` | `tools/index.html` |
| 💼 职业发展 | `blog/category/career.html` | `career/index.html` |
| 🌿 生活杂谈 | `blog/category/life.html` | `life/index.html` |

### 修复 4：GitHub Pages 首次部署 404

**问题：** 代码推送后访问站点显示 404。

**原因：** 仓库可能为 Private，或者 Settings > Pages 未启用 GitHub Actions 作为部署源，或 workflow 未运行过。

**修复：** 参见 `docs/BUILD.md` 中"首次启用 GitHub Pages"章节的完整 5 步流程。
