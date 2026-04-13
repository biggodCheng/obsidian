---
name: ob-todo
description: 任务管理技能 - 记录、查看、更新任务卡片
user-invocable: true
---

# Lobster 任务卡 - 任务管理

管理 Obsidian 知识库中的任务卡片。

## When to Use

当用户说：
- "记一下明天开会" / "待办 xxx"
- "添加任务: 完成项目报告"
- "查看我的待办事项"
- "列出所有任务"
- "把任务 xxx 标记为完成"

## How It Works

使用 `lobster_utils.py` 核心工具模块：
- 创建新的任务卡片（存放在 `卡片库/任务卡/` 目录）
- 查看所有任务或按状态过滤
- 更新任务状态
- 支持优先级设置

## Task Card Structure

```yaml
---
type: 任务卡
status: 待办
priority: 中
tags: []
created: YYYY-MM-DD
due: YYYY-MM-DD
---
```

## Usage Examples

```
记一下明天下午3点开会
添加任务: 完成项目报告，优先级高
查看我的待办事项
列出所有未完成的任务
把"开会"标记为完成
```

## Output

返回任务信息：
- 任务标题
- 状态（待办/进行中/已完成/已取消）
- 优先级（低/中/高）
- 截止日期
- 子任务列表
