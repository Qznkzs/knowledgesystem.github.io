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
