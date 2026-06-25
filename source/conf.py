# Sphinx 个人知识库配置文件

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
blog_baseurl = 'https://qznkzs.github.io/knowledgesystem.github.io/'

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
    'secondary_sidebar_items': ['page-toc'],
    'footer_start': ['copyright'],
    'footer_end': ['theme-version'],
    'github_url': 'https://github.com/Qznkzs/knowledgesystem.github.io',
    'icon_links': [],
}

html_static_path = ['_static']
templates_path = ['_templates']

html_css_files = [
    'custom.css',
]

# 侧边栏配置（暂时使用 pydata 默认配置，避免与 ABlog 模板冲突）
# html_sidebars = {
#     'blog/**': [
#         'ablog/postcard.html',
#         'ablog/recent.html',
#         'ablog/tagcloud.html',
#         'ablog/archives.html',
#     ],
#     '**': [
#         'search-field.html',
#         'sidebar-nav-bs.html',
#         'ablog/recent.html',
#     ],
# }

# -- Intersphinx --------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- TODO 扩展 ----------------------------------------------------

todo_include_todos = False
