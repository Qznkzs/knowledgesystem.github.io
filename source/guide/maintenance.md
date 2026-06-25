# 知识库维护文档

## 日常维护

### 新增分类

如果需要增加新的大分类（如 `iot/`、`ai/` 等）：

1. 在 `source/` 下创建目录：

```bash
mkdir -p source/iot/
```

2. 创建分类索引页 `source/iot/index.md`：

```markdown
# 物联网

:::{toctree}
:maxdepth: 2
:glob:

*
:::
```

3. 在首页 `source/index.md` 的分类导航区新增一张卡片：

```markdown
:::{grid-item-card} 🌐 物联网
:link: blog/category/iot.html

MQTT · 传感器 · 边缘计算
:::
```

4. 本地构建验证，确认无误后提交推送。

### 新增子分类

在已有分类下增加子目录（如 `embedded/fpga/`）：

```bash
mkdir -p source/embedded/fpga/
```

然后在父分类的 `index.md` 的 toctree glob 中添加通配符：

```markdown
:::{toctree}
:maxdepth: 2
:glob:

mcu/*
rtos/*
linux/*
hardware/*
toolchain/*
fpga/*
:::
```

### 添加标签

标签无需预先定义——在文章的 frontmatter 中使用新标签名即可，ABlog 会自动生成对应的标签聚合页面。

### 备份知识库

因为整个知识库就是 Git 仓库中的纯文本文件，备份非常简单：

```bash
# 方式一：推送到 GitHub（推荐，每篇文章写完就 push）
git push origin main

# 方式二：打包备份
tar -czf knowledge-base-backup-$(date +%Y%m%d).tar.gz \
    --exclude='build' \
    --exclude='__pycache__' \
    --exclude='.git' \
    .

# 方式三：克隆到其他位置作为备份
git clone git@github.com:Qznkzs/knowledgesystem.github.io.git ~/backup/knowledge-base
```

> **数据安全原则：** 纯 Markdown 文件没有厂商锁定。即使 Sphinx/ABlog 不再维护，你的文章依然是可读的文本文件，可以被任何 Markdown 工具打开。

### 恢复知识库

```bash
git clone git@github.com:Qznkzs/knowledgesystem.github.io.git
cd knowledgesystem.github.io
pip install -r requirements.txt
sphinx-build -b html source/ build/
```

## 自定义主题

### 修改配色

`pydata_sphinx_theme` 使用 CSS 变量控制颜色。在 `source/_static/custom.css` 中添加：

```css
:root {
  /* 主色调 */
  --pst-color-primary: #2563eb;      /* 链接、按钮等 */
  --pst-color-link: #2563eb;         /* 链接颜色 */

  /* 代码块主题 */
  --pst-color-inline-code: #d63384;  /* 行内代码 */
}
```

PyData 主题支持的完整 CSS 变量列表参见：
https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/styling.html

### 修改字体

```css
html {
  --pst-font-family-base: 'Noto Sans SC', system-ui, sans-serif;
  --pst-font-family-heading: 'Noto Serif SC', Georgia, serif;
  --pst-font-family-monospace: 'JetBrains Mono', 'Fira Code', monospace;
}
```

### 更换主题

如果将来想更换为其他 Sphinx 主题：

1. 在 `conf.py` 中修改 `html_theme`：

```python
# 例如切换到 Furo 主题
html_theme = 'furo'
```

2. 安装新主题：

```bash
pip install furo
```

3. 更新 `requirements.txt`，添加新主题依赖。

4. 调整 `html_theme_options` 以匹配新主题的配置项。

5. 本地构建验证，样式可能需要重新调整。

## 进阶配置

### 启用评论系统

以 Giscus（基于 GitHub Discussions）为例：

1. 在仓库 Settings 中启用 Discussions
2. 安装 [Giscus GitHub App](https://github.com/apps/giscus)
3. 在 `source/_templates/` 下创建自定义页面模板，在文章底部嵌入 Giscus 脚本

```html
<!-- 添加到 post 模板底部 -->
<script src="https://giscus.app/client.js"
    data-repo="Qznkzs/knowledgesystem.github.io"
    data-repo-id="<YOUR_REPO_ID>"
    data-category="Announcements"
    data-category-id="<YOUR_CATEGORY_ID>"
    data-mapping="pathname"
    data-reactions-enabled="1"
    async>
</script>
```

### 添加统计分析

在 `conf.py` 中添加 Google Analytics 或其他统计服务的 ID：

```python
html_theme_options = {
    # ...
    'analytics': {
        'google_analytics_id': 'G-XXXXXXXXXX',
    },
}
```

### 自定义域名

1. 购买域名（如 `yourname.com`）
2. 在域名 DNS 中添加 CNAME 记录指向 `qznkzs.github.io`
3. 在仓库 `source/` 目录下创建 `CNAME` 文件，内容为你的域名
4. 在 `conf.py` 中更新 `blog_baseurl`：

```python
blog_baseurl = 'https://yourname.com/'
```

5. 在 GitHub 仓库 Settings > Pages 中填写自定义域名

### 全文搜索增强

默认使用 pydata-sphinx-theme 内置的客户端搜索（无需后端）。如需更强大的搜索，可以接入 Algolia DocSearch：

1. 申请 [DocSearch](https://docsearch.algolia.com/)（开源项目免费）
2. 按文档配置爬虫
3. 在 `conf.py` 中添加 Algolia 配置

## 依赖版本管理

### 锁定版本（推荐）

当知识库稳定运行后，建议锁定依赖版本以避免意外升级导致构建失败：

```text
# requirements.txt
sphinx==8.1.3
myst-parser==4.0.1
ablog==0.11.12
pydata-sphinx-theme==0.19.0
sphinx-design==0.6.1
```

获取当前安装的精确版本：

```bash
pip freeze | grep -E "sphinx|myst|ablog|pydata-sphinx-theme|sphinx-design" > requirements.txt
```

### 定期升级检查

建议每 3-6 个月检查一次依赖更新：

```bash
# 查看可升级的包
pip list --outdated

# 逐包升级测试
pip install --upgrade sphinx
sphinx-build -b html source/ build/  # 验证构建

pip install --upgrade myst-parser
sphinx-build -b html source/ build/  # 验证构建

# ... 依此类推
```

## 常见问题

### Q: 如何修改网站标题和描述？

编辑 `source/conf.py`：

```python
project = '你的网站标题'
blog_title = '你的博客标题'
```

### Q: 如何修改首页副标题？

编辑 `source/index.md` 中 `# 晚吟的知识库` 下方的文字。

### Q: 文章太多，首页加载慢怎么办？

可以在 `{postlist}` 指令中限制数量（需 ABlog 支持），或使用分页。

### Q: 如何在文章中嵌入视频？

```markdown
```{raw} html
<iframe width="560" height="315"
  src="https://www.youtube.com/embed/VIDEO_ID"
  frameborder="0" allowfullscreen>
</iframe>
```
```

### Q: 如何导出为 PDF？

```bash
# 需要安装 LaTeX（如 texlive）
sphinx-build -b latex source/ build/latex/
cd build/latex/
make
```

### Q: 构建很慢怎么办？

Sphinx 支持增量构建——只重新构建修改过的文件。日常使用时直接运行 `sphinx-build` 即可，只有首次是全量构建。

### Q: 文章中有中文搜索不到？

pydata-sphinx-theme 内置的搜索支持中文分词。如果搜索效果不理想，可考虑接入 Algolia DocSearch。

## 迁移到其他平台

由于所有文章都是纯 Markdown 文件，迁移到其他平台非常简单：

### 迁移到 Hugo

```bash
hugo new site my-blog
# 将 source/ 下的 .md 文件移动到 Hugo 的 content/ 目录
# 调整 frontmatter 格式（Hugo 使用 TOML/YAML frontmatter）
```

### 迁移到 Obsidian

直接把整个仓库用 Obsidian 打开即可——Obsidian 原生支持 Markdown 和 `[[wikilinks]]`。

### 迁移到 Notion

批量导入 Markdown 文件（Notion 支持 `.md` 导入）。

### 迁移到 Hexo

```bash
hexo init my-blog
# 将 .md 文件放入 source/_posts/
# frontmatter 格式基本兼容，可能需要微调
```

## 数据完整性检查

定期运行以下检查：

```bash
# 1. 检查 Git 仓库状态
git status

# 2. 检查是否有文件名不符合规范
find source/ -name "*.md" ! -name "index.md" | while read f; do
    basename "$f" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}-' || echo "不规范: $f"
done

# 3. 构建并检查 warning
sphinx-build -b html source/ build/ -W 2>&1 | grep -i warning

# 4. 检查是否有孤立文件（未被 toctree 引用）
# 构建时关注 "文档没有加入到任何目录树中" 的 warning
```
