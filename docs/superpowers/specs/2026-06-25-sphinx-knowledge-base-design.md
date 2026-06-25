# 个人知识库设计文档：Sphinx + Git + Read the Docs 方案

**作者：** 晚吟
**日期：** 2026-06-25
**状态：** 已确认

---

## 1. 项目概述

基于 Sphinx + MyST + ABlog + GitHub Pages 搭建个人知识库，博客风格首页，支持 Markdown/RST 混写，零成本部署。

**目标用户：** 嵌入式工程师（本人），主力记录嵌入式领域知识，同时容纳计算机基础、工具效率、职业发展、生活杂谈等内容。

---

## 2. 技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| 构建引擎 | Sphinx | 用户指定，Python 文档构建标准 |
| Markdown 解析 | MyST-Parser | 桥接 Markdown 写作习惯和 Sphinx 生态 |
| 博客功能 | ABlog | 文章列表、分类、标签、归档、RSS 全部内置 |
| 主题 | pydata_sphinx_theme | 暗色模式、响应式、顶部导航，比 ABlog 默认主题现代 |
| 部署平台 | GitHub Pages | 免费、HTTPS、自动部署 |
| CI/CD | GitHub Actions | 自动构建 → 部署到 gh-pages 分支 |
| 版本控制 | Git | 知识即代码，完整历史记录 |

---

## 3. 仓库目录结构

```
knowledge-base/
├── .github/workflows/deploy.yml   # GitHub Actions 自动构建部署
├── source/
│   ├── conf.py                   # Sphinx 配置（扩展、主题、ABlog 设置）
│   ├── index.md                  # 首页（博客列表页）
│   ├── _templates/               # 自定义 Jinja2 模板（覆写 ABlog 模板）
│   ├── _static/                  # 自定义 CSS、JS、图片
│   ├── embedded/                 # 🎯 主力：嵌入式
│   │   ├── mcu/                  #   MCU / 单片机（stm32, esp32 等）
│   │   ├── rtos/                 #   实时操作系统（FreeRTOS, RT-Thread 等）
│   │   ├── linux/                #   嵌入式 Linux（kernel, drivers, yocto）
│   │   ├── hardware/             #   硬件设计 / 原理图 / PCB
│   │   └── toolchain/            #   工具链 / 调试 / CI
│   ├── cs/                       # 计算机基础（数据结构、算法、网络等）
│   ├── tools/                    # 工具 / 效率 / 环境配置
│   ├── career/                   # 工作经历 / 项目复盘 / 职场思考
│   ├── life/                     # 生活 / 阅读 / 杂谈
│   ├── drafts/                   # 草稿（不构建进站点）
│   └── private/                  # 私有内容（构建时排除）
├── requirements.txt              # Python 依赖
└── README.md
```

**设计原则：**
- 每个子目录代表一个大分类，一篇文章只属于一个分类
- 跨分类的精细检索靠标签实现
- `drafts/` 和 `private/` 通过 `exclude_patterns` 排除，不进入公开站点

---

## 4. Sphinx 配置核心

### 4.1 扩展清单

```python
extensions = [
    'myst_parser',              # Markdown 解析
    'ablog',                    # 博客功能
    'sphinx.ext.intersphinx',   # 跨文档引用
    'sphinx.ext.todo',          # TODO 标记
    'sphinx_design',            # 卡片、网格等 UI 组件
]
```

### 4.2 MyST 配置

```python
myst_enable_extensions = [
    'dollarmath',        # LaTeX 数学公式
    'colon_fence',       # ::: 语法做 admonition 卡片
    'substitution',      # 变量替换
]

# 文件扩展名映射：.md 文件用 MyST 解析
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
```

### 4.3 ABlog 配置

- 文章日期来源：文件名 `YYYY-MM-DD-slug.md` 自动提取
- 博客路径前缀：`/blog/`
- 自动生成分类页、标签页、归档页、RSS Feed

### 4.4 排除私有内容

```python
exclude_patterns = ['private/*', 'drafts/*']
```

### 4.5 主题配置

```python
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'show_toc_level': 2,
    'navbar_align': 'left',
    'github_url': 'https://github.com/<username>/knowledge-base',
}
```

---

## 5. 模板定制

只需覆写两个 ABlog 模板文件，放在 `source/_templates/` 下：

| 文件 | 用途 | 改动量 |
|------|------|--------|
| `postlist.html` | 首页博客列表，定制为卡片流布局 | ~60 行 |
| `recent.html` | 侧边栏"最近文章"小组件 | ~30 行 |

不修改上游主题源码，仅在 `_templates/` 中覆写。

---

## 6. 写作流程

### 6.1 创建文章

1. 在对应分类目录下新建文件，文件名为 `YYYY-MM-DD-slug.md`
   - 例：`source/embedded/rtos/2026-06-25-freertos-task-scheduling.md`
2. 文章头部写 frontmatter（可选）：
   ```yaml
   ---
   author: 晚吟
   tags:
     - freertos
     - 任务调度
     - 踩坑
   ---
   ```
3. 正文用 Markdown 写，需要复杂排版时混用 RST 指令
4. `git add → git commit → git push`，自动部署

### 6.2 标签 vs 分类

| 维度 | 分类（目录） | 标签（frontmatter） |
|------|-------------|-------------------|
| 来源 | 文件路径 | 文章 frontmatter |
| 关系 | 一篇文章一个分类 | 一篇文章多标签 |
| 用途 | 大范围归属 | 跨分类精准检索 |
| 示例 | `embedded/rtos/` | `#freertos` `#任务调度` `#stm32` |

### 6.3 RSS

ABlog 自动生成 Atom Feed，地址为 `/blog/atom.xml`，可用 RSS 阅读器订阅。

---

## 7. 构建与部署

### 7.1 CI/CD 流程

```
git push (main 分支)
    ↓
GitHub Actions 触发
    ↓
pip install -r requirements.txt
    ↓
sphinx-build source/ build/
    ↓
deploy to gh-pages 分支
    ↓
自动部署到 <username>.github.io/knowledge-base
```

### 7.2 私有内容保护

- `private/` 和 `drafts/` 目录不在公开站点中出现
- 本地可通过临时去掉 `exclude_patterns` 生成包含私有文章的本地版本
- 整个知识库是 Git 仓库中的纯文本 Markdown 文件，数据完全自控，无厂商锁定

---

## 8. 外部依赖

```
# requirements.txt
sphinx>=7.0
myst-parser>=3.0
ablog>=0.11
pydata-sphinx-theme>=0.15
sphinx-design>=0.5
```

---

## 9. 非目标（本次不做）

- 评论系统（Disqus/Giscus）—— 后续按需添加
- 全文搜索—— pydata-sphinx-theme 自带本地搜索，可后续接入 Algolia
- 自定义域名
- 多语言支持
- 自动化测试
