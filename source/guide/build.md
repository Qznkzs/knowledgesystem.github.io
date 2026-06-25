# 知识库构建文档

## 环境要求

| 组件 | 最低版本 | 说明 |
|------|---------|------|
| Python | 3.9+ | 推荐 3.12 |
| pip | 21.0+ | Python 包管理器 |
| Git | 2.30+ | 版本控制和自动部署 |

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:Qznkzs/knowledgesystem.github.io.git
cd knowledgesystem.github.io
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

依赖清单：
- `sphinx>=7.0` —— 文档构建引擎
- `myst-parser>=3.0` —— Markdown 解析（MyST）
- `ablog>=0.11` —— 博客功能（文章列表、标签、分类、RSS）
- `pydata-sphinx-theme>=0.15` —— 现代响应式主题
- `sphinx-design>=0.5` —— 卡片、网格等 UI 组件

### 3. 本地构建

```bash
# 清理旧构建（可选）
rm -rf build/

# 构建 HTML 站点
sphinx-build -b html source/ build/
```

构建产物在 `build/` 目录下。

### 4. 本地预览

```bash
python -m http.server 8080 -d build/
```

浏览器打开 `http://localhost:8080` 即可预览站点。

### 5. 包含私有内容的本地构建

如果你需要在本地预览包含 `private/` 和 `drafts/` 目录中内容的完整站点：

```bash
# 方式一：临时修改 conf.py 中的 exclude_patterns，注释掉 private 和 drafts
# 然后正常构建

# 方式二：使用环境变量控制（需在 conf.py 中自行扩展）
sphinx-build -b html source/ build_with_private/
```

> **注意：** 不要在公开部署时包含私有内容。GitHub Actions 部署使用默认的 `exclude_patterns`。

## CI/CD 自动部署

### 工作流说明

文件位置：`.github/workflows/deploy.yml`

触发条件：
- **自动触发**：向 `main` 分支推送代码
- **手动触发**：在 GitHub Actions 页面点击 "Run workflow"

工作流步骤：

```
git push (main 分支)
    ↓
GitHub Actions 触发
    ↓
Checkout 代码
    ↓
Setup Python 3.12
    ↓
pip install -r requirements.txt
    ↓
sphinx-build -b html source/ build/
    ↓
Deploy to GitHub Pages
    ↓
站点更新至 qznkzs.github.io/knowledgesystem.github.io
```

### 首次启用 GitHub Pages

首次部署需要完成以下步骤，否则访问站点会显示 404：

**1. 确认仓库为 Public（公开）**

进入仓库 **Settings > General**，滚动到页面底部 **Danger Zone**：

- 确认 **Visibility** 显示为 **Public**
- 如果是 **Private**，点击 **Change visibility** → 选择 **Public**

> 免费版 GitHub Pages 只支持公开仓库。私有仓库需要 GitHub Pro/Team/Enterprise 订阅。

**2. 启用 GitHub Pages 并设置部署源**

进入仓库 **Settings > Pages**，在 **Build and deployment** 区域：

- **Source** 下拉选择 **GitHub Actions**（不是 "Deploy from a branch"）

**3. 触发首次部署**

如果代码已经推送（`git push`），进入仓库 **Actions** 标签页：
- 找到 **Deploy Knowledge Base** workflow
- 点击 **Run workflow** → **Run workflow**（手动触发）
- 等待 workflow 运行完成（约 1-2 分钟）

**4. 确认部署成功**

workflow 完成后，点击那次运行记录：
- 展开 **build-and-deploy** job
- 查看 **Deploy to GitHub Pages** 步骤的日志，末尾会显示实际部署 URL

**5. 验证站点**

浏览器访问部署地址，确认首页能正常打开。

> **常见 404 原因汇总：**
>
> | 原因 | 解决方案 |
> |------|---------|
> | 仓库是 Private | Settings > General > 改为 Public |
> | Pages 未启用 | Settings > Pages > Source 选 GitHub Actions |
> | Workflow 未运行 | Actions > 手动触发 Run workflow |
> | Workflow 权限不足 | Settings > Actions > General > Workflow permissions 选 "Read and write permissions" |
> | 仅推送了代码，以为会自动部署 | 首次必须在 Actions 中手动触发一次，之后每次 push 会自动部署 |

### 查看部署状态

进入仓库的 **Actions** 标签页，查看最新的 workflow 运行状态。

常见失败原因：
- 依赖安装失败 → 检查 `requirements.txt` 版本约束
- Sphinx 构建失败 → 本地先运行 `sphinx-build` 排查
- 部署权限不足 → 检查 Settings > Actions > General > Workflow permissions 是否为 "Read and write permissions"

## 目录结构

```
knowledgesystem.github.io/
├── .github/workflows/deploy.yml   # CI/CD 工作流
├── source/                        # 源文件目录（所有文章在这里）
│   ├── conf.py                   # Sphinx 配置文件
│   ├── index.md                  # 首页
│   ├── _templates/               # Jinja2 模板覆盖
│   │   ├── postlist.html         # 博客列表模板
│   │   └── ablog/
│   │       ├── postlist.html     # ABlog 命名空间模板
│   │       └── recent.html       # 最近文章侧边栏
│   ├── _static/                  # 静态资源
│   │   └── custom.css            # 自定义样式
│   ├── embedded/                 # 嵌入式分类
│   │   ├── index.md
│   │   ├── mcu/
│   │   ├── rtos/
│   │   ├── linux/
│   │   ├── hardware/
│   │   └── toolchain/
│   ├── cs/                       # 计算机基础
│   ├── tools/                    # 工具 & 效率
│   ├── career/                   # 职业发展
│   ├── life/                     # 生活杂谈
│   ├── drafts/                   # 草稿（不构建）
│   └── private/                  # 私有内容（不构建）
├── build/                        # 构建产物（不提交到 Git）
├── requirements.txt              # Python 依赖
└── README.md                     # 项目说明
```

## 主题与样式

### 主题

使用 `pydata_sphinx_theme`，支持：
- 亮色 / 暗色模式自动切换
- 响应式布局（桌面 / 平板 / 手机）
- 内置搜索（客户端全文搜索）
- GitHub 图标链接

### 自定义样式

`source/_static/custom.css` 包含：
- 博客卡片网格布局（CSS Grid）
- 卡片悬停动画
- 标签样式
- 侧边栏最近文章样式
- 深色模式适配
- 移动端响应式

修改 `custom.css` 后重新构建即可生效。

### 自定义模板

`source/_templates/` 目录下的文件会覆盖 ABlog 和主题的默认模板：

| 模板文件 | 用途 |
|---------|------|
| `postlist.html` | 博客文章列表页布局 |
| `ablog/postlist.html` | ABlog 命名空间版本 |
| `ablog/recent.html` | 侧边栏"最近文章"组件 |

修改模板后重新构建即可生效。

## 版本升级

### 升级依赖

```bash
# 查看可升级的包
pip list --outdated

# 升级全部依赖
pip install --upgrade -r requirements.txt

# 或逐个升级
pip install --upgrade sphinx
pip install --upgrade myst-parser
```

升级后务必本地构建测试，确认无兼容性问题再推送。

### Sphinx 大版本升级注意事项

Sphinx 主版本升级时，可能需要：
1. 查看 [Sphinx Changelog](https://www.sphinx-doc.org/en/master/changes.html)
2. 检查 `conf.py` 中的配置项是否被废弃
3. 本地构建并修复所有 warning

### ABlog 升级注意事项

ABlog 的 API 在不同版本间可能有变化，升级后检查：
- `{postlist}` 指令是否正常渲染
- 标签和分类页面是否正常生成
- RSS Feed 是否正常输出

## 故障排查

### 构建失败：找不到模块

```bash
# 确认依赖已安装
pip list | grep -E "sphinx|myst|ablog|pydata"

# 重新安装
pip install --force-reinstall -r requirements.txt
```

### 文章未出现在博客列表中

1. 确认文章文件名格式为 `YYYY-MM-DD-slug.md`
2. 确认文章中有 `{post}` 指令（` ```{post} YYYY-MM-DD ``` `）
3. 确认文章在 Sphinx 的文档树中（通过 toctree 引用或 glob 匹配）

### 样式不生效

1. 确认 `custom.css` 在 `source/_static/` 目录下
2. 确认 `conf.py` 中 `html_css_files = ['custom.css']` 配置正确
3. 浏览器强制刷新（Ctrl+Shift+R）

### 搜索功能不工作

本地预览时搜索需要 HTTP 服务（不能直接打开 HTML 文件）。使用 `python -m http.server` 预览。
