---
author: 晚吟
tags:
  - claude-code
  - 会话管理
  - 效率
---

```{post} 2026-06-25
:category: claude-code
```

# Claude Code 会话管理

会话（Session）是 Claude Code 中与项目目录关联的已保存对话。Claude Code 在你工作时将对话本地存储，因此你可以从中断处恢复、分支以尝试不同的方法，或在任务之间切换。

> **环境说明：** 本文以 MobaXterm SSH 连接远程开发机为典型场景。会话管理完全由 Claude Code 自身处理，与终端软件（MobaXterm / iTerm2 / Windows Terminal 等）无关——即使终端断开，会话仍然保留在服务器上。

## 保存机制

Claude Code **默认自动保存**所有对话历史，以 JSONL 格式存储在 `~/.claude/projects/` 目录下。无论是正常退出、`/clear` 清空上下文，还是终端意外断开（如关闭 MobaXterm 标签页），对话记录都不会丢失——**无需任何手动保存操作**。

## 恢复会话

日常使用中，只需要记住两个最常用的命令：

```bash
claude -c    # 继续最近一次会话（等同于 claude --continue）
claude -r    # 调出历史会话列表选择（等同于 claude --resume）
```

完整入口：

| 命令 | 功能 |
|:--|:--|
| `claude -c` / `claude --continue` | 恢复当前目录最近的会话 |
| `claude -r` / `claude --resume` | 打开会话选择器 |
| `claude --resume <name>` | 直接恢复指定名称的会话 |
| `claude --from-pr <number>` | 恢复链接到该 PR 的会话 |
| `/resume` | 从活跃会话内切换到不同对话 |

使用 `claude -p`（非交互模式）或 Agent SDK 创建的会话不会出现在会话选择器中，但仍可通过会话 ID 恢复：

```bash
claude --resume <session-id>
```

### 关键词搜索

如果记得上次对话涉及的内容，可以直接用关键词过滤：

```bash
claude -r "数据库"
claude -r "React"
```

选择器会只显示匹配的会话。

### 核心注意事项

**工作目录绑定：** Claude Code 的会话与当前工作目录强绑定。恢复会话前，务必先 `cd` 进入对应项目目录：

```bash
cd ~/workspace/my-project
claude -c    # 恢复 my-project 的最近会话
```

**避免移动项目文件夹：** 不要随意移动项目目录的位置。Claude Code 内部索引使用绝对路径，移动后恢复功能会因为路径对不上而找不到历史记录。

**MobaXterm 场景：** 关闭 MobaXterm 标签页或网络断开后，会话已自动保存在服务器上。重新 SSH 连接，`cd` 到项目目录，`claude -c` 即可无缝继续。

### 会话选择器查找范围

会话按项目目录存储。默认情况下，选择器显示当前 worktree 的交互式会话。使用 `Ctrl+W` 扩展到所有 worktree，`Ctrl+A` 扩展到整台电脑上每个项目。

按名称恢复会跨当前仓库及其 worktree 解析：

| 命令 | 精确匹配 | 模糊名称 |
|:--|:--|:--|
| `claude --resume <name>` | 直接恢复 | 打开选择器，名称预填充 |
| `/resume <name>` | 直接恢复 | 报告错误；不带参数运行打开选择器 |

## 命名会话

为会话提供描述性名称，便于在会话选择器中查找和按名称恢复。这在并行处理多个任务时尤其重要。

| 时机 | 方法 |
|:--|:--|
| 启动时 | `claude -n api-migration` |
| 会话期间 | `/rename api-migration`（名称会出现在提示栏上） |
| 从选择器 | 选中会话按 `Ctrl+R` |
| Plan Mode 接受计划时 | 自动从计划内容命名 |

命名后，可以直接通过名称恢复：

```bash
claude --resume api-migration
/resume api-migration
```

## 会话选择器

运行 `/resume` 或不带参数运行 `claude --resume` 打开交互式会话选择器。

| 快捷键 | 操作 |
|:--|:--|
| `↑` / `↓` | 导航 |
| `→` / `←` | 展开/折叠分组 |
| `Enter` | 恢复选中会话 |
| `Space` | 预览会话内容 |
| `Ctrl+R` | 重命名 |
| `/` 或可打印字符 | 搜索模式。粘贴 PR URL 可查找创建它的会话 |
| `Ctrl+A` | 显示所有项目的会话，再按返回当前仓库 |
| `Ctrl+W` | 显示当前仓库所有 worktree，再按返回当前 |
| `Ctrl+B` | 过滤当前 git 分支的会话 |
| `Esc` | 退出 |

每行显示：会话名称（或摘要/首个提示）、距上次活动的时间、消息计数和 git 分支。

## 分支会话

分支创建当前对话的副本并切换到其中，保持原始对话完整。适合尝试不同方案而不丢失当前路径。

**会话内分支：**

```
/branch try-streaming-approach
```

**命令行分支：**

```bash
claude --continue --fork-session
```

原始会话保持不变，在会话选择器中仍可用。`/branch` 确认打印两个 ID：新分支和原始分支。

> **注意：** 通过"允许此会话"批准的权限不会转移到新分支。如果在两个终端中恢复同一会话而不分叉，两条消息会交错到同一个文本记录中。

对于会话内的 checkpoint 回退，参见 `/rewind` 命令。

## 管理会话内上下文

| 命令 | 作用 |
|:--|:--|
| `/clear` | 以空上下文重新开始，之前的对话已保存可恢复 |
| `/compact [instructions]` | 用摘要替换历史记录，可选指定重点 |
| `/context` | 显示当前消耗的上下文 |

## 导出和定位会话数据

**导出会话：** 运行 `/export` 将当前对话复制到剪贴板或保存为纯文本文件：

```bash
/export my-session-transcript.txt
```

**文本记录存储：** JSONL 格式，位置为：

```
~/.claude/projects/<project>/<session-id>.jsonl
```

每行是消息、工具调用或元数据的 JSON 对象。

**更改存储位置：**

```bash
export CLAUDE_CONFIG_DIR=/custom/path
```

**保留策略：** 本地文件默认 30 天后自动删除，可通过 `cleanupPeriodDays` 设置更改。

**禁用文本记录：**

```bash
export CLAUDE_CODE_SKIP_PROMPT_HISTORY=true
# 或在非交互模式
claude -p --no-session-persistence
```

## 相关功能

- **Worktrees**：在独立分支上运行隔离的并行会话
- **Checkpointing**：将代码和对话回退到较早时间点
- **上下文窗口**：什么填充上下文、什么在压缩中保留
- **非交互模式**：`claude -p` 下的会话行为

---

> 参考：[Claude Code 官方文档 - 管理会话](https://code.claude.com/docs/zh-CN/sessions)
