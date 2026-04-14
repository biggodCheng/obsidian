---
name: ob-todo
description: 任务管理技能 - 记录、查看、更新日常工作片。当用户说"记一下明天开会"、"待办"、"添加任务"、"查看待办事项"、"标记完成"时触发。
user-invocable: true
---

# Lobster Todo - 任务管理

管理 Obsidian 知识库中的日常工作片。

## 执行入口

```
python .claude/skills/ob-todo/todo.py <子命令> [参数]
```

子命令：`add`（添加任务）、`list`（列出任务）、`complete`（标记完成）

依赖：`.lobster/lobster_utils.py`

## 工作流

### Step 1: 解析用户意图

| 用户说法 | 映射到子命令 |
|---------|-------------|
| "记一下明天开会" / "待办: xxx" / "添加任务: xxx" | `todo.py add "开会"` |
| "查看待办" / "列出任务" / "有什么事要做" | `todo.py list` |
| "把开会标记为完成" / "任务完成了" | `todo.py complete <文件路径>` |

**意图解析规则**：
- 用户提"明天/后天/X号"等时间 → 解析为 `--due YYYY-MM-DD`
- 用户提"优先级高/紧急/重要" → `--priority high`
- 用户提"下午3点"等具体时间 → 放入 `--description` 中
- 用户想标记完成 → 需先 `list` 找到文件路径，再 `complete`

### Step 2: 构造并执行命令

```bash
# 添加任务
python .claude/skills/ob-todo/todo.py add "开会" --description "下午3点产品会议" --priority medium

# 添加带截止日期的任务
python .claude/skills/ob-todo/todo.py add "完成项目报告" --priority high --due 2026-04-18 --tags 工作,报告

# 列出待办任务（默认不显示已完成）
python .claude/skills/ob-todo/todo.py list

# 列出所有任务（包括已完成）
python .claude/skills/ob-todo/todo.py list --all

# 按状态过滤
python .claude/skills/ob-todo/todo.py list --status pending
python .claude/skills/ob-todo/todo.py list --status completed

# 标记任务完成（需要文件路径，先从list获取）
python .claude/skills/ob-todo/todo.py complete "d:\DATA\cgq-obsidian\personal-wiki\日常工作\2026-04\2026-04-14-开会.md"
```

### Step 3: 格式化返回结果

将 CLI 输出整理为用户友好的格式。

## CLI 参数速查

### add 子命令

| 参数 | 缩写 | 说明 | 示例 |
|------|------|------|------|
| `title` | - | 任务标题（位置参数） | `add "开会"` |
| `--description` | `-d` | 任务描述 | `-d "下午3点产品会议"` |
| `--priority` | `-p` | 优先级：low/medium/high（默认medium） | `-p high` |
| `--due` | - | 截止日期 YYYY-MM-DD | `--due 2026-04-18` |
| `--tags` | - | 标签（逗号分隔） | `--tags 工作,报告` |

### list 子命令

| 参数 | 缩写 | 说明 | 示例 |
|------|------|------|------|
| `--status` | `-s` | 按状态过滤：pending/in_progress/completed/cancelled | `-s pending` |
| `--all` | `-a` | 显示所有任务（含已完成） | `--all` |

### complete 子命令

| 参数 | 说明 |
|------|------|
| `filepath` | 任务文件路径（从 list 命令获取） |

## 任务文件结构

任务保存到 `personal-wiki/日常工作/YYYY-MM/` 目录，文件名格式：`YYYY-MM-DD-任务名.md`

```yaml
---
type: 日常工作
status: 待办
priority: 中
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
due: YYYY-MM-DD
title: 任务标题
---
```

## 边界条件

- **"标记完成"但未指定任务** → 先执行 `list` 展示待办，让用户选择
- **截止日期已过** → 在结果中标注"已过期"
- **同名任务已存在** → 直接创建（日期前缀保证唯一性）
- **todo.py 执行失败** → 检查 lobster_utils.py 是否存在

## 使用示例

```
记一下明天下午3点开会
→ python .claude/skills/ob-todo/todo.py add "开会" --description "下午3点" --due 2026-04-15

添加任务: 完成项目报告，优先级高
→ python .claude/skills/ob-todo/todo.py add "完成项目报告" --priority high --tags 工作

查看待办
→ python .claude/skills/ob-todo/todo.py list

把"开会"标记为完成
→ 先 list 找路径，再 complete <路径>
```
