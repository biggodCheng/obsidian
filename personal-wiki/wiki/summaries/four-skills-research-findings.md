---
title: 四个核心 AI 技能研究发现
type: summary
date: 2026-04-09
tags: [研究记录, 技术决策, 龙虾AI, 需求分析]
sources: [findings]
related: [龙虾AI, ob-search, ob-todo, ob-note, article-processor, 四个核心AI技能实现计划]
confidence: high
status: mature
---

# 四个核心 AI 技能研究发现

## 源文件

`raw/sources/findings.md`

## 概述

记录四个核心 AI 技能实现过程中的研究发现、技术决策和问题解决方案。

## 需求分析

### ob-search（检索技能）

提供全库基础检索能力：
- 支持关键词搜索
- 支持标签过滤
- 支持卡片类型过滤（judgment/method/case/information）
- 返回按相关度排序的结果

### ob-todo（任务管理）

工作卡片/任务管理功能：
- 快速记录任务
- 任务状态追踪
- 任务提醒功能

### ob-note（笔记管理）

随时记录/笔记管理功能：
- 快速创建笔记卡片
- 自动生成 frontmatter
- 支持分类和标签

### article-processor（内容处理）

研究探索/内容处理功能：
- URL 内容抓取
- 正文提取
- AI 拆卡（自动提炼判断卡）

## 研究发现

### Obsidian 技术特性

1. **文件格式**: 纯 Markdown 文件 + YAML Frontmatter
2. **双向链接**: `[[文件名]]` 语法
3. **标签系统**: `#标签名` 语法

### 技能结构

Claude Code Skills 使用以下格式：

```yaml
---
name: skill-name
description: 技能描述
user-invocable: true
---
```

### 笔记卡片 Frontmatter 模板

```yaml
---
type: judgment|method|case|information
confidence: high|medium|low
tags: [标签1, 标签2]
status: new|growing|mature|outdated|discarded
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## 技术决策

| 决策 | 理由 |
|------|------|
| 技能存放位置 | `C:\Users\87044\.claude\skills\lobster-*\` |
| 笔记存放位置 | `d:\DATA\cgq-obsidian\notes\` |
| 卡片命名规范 | `YYYY-MM-DD-{type}-{slug}.md` |
| Frontmatter 格式 | YAML 标准格式 |

## 测试结果

所有四个核心技能测试通过：

| 技能 | 测试内容 | 结果 |
|------|----------|------|
| ob-note | 创建判断卡、方法卡、案例卡、信息卡 | ✅ 成功 |
| ob-search | 搜索并返回匹配的笔记 | ✅ 成功 |
| ob-todo | 添加任务、列出任务 | ✅ 成功 |
| article-processor | 基础架构 | ⚠️ 需集成 MCP |

创建的示例笔记：
- `notes/2026-03-30-judgment-价格敏感度测试.md`
- `notes/2026-03-30-todo-完成四个核心技能测试.md`

## 核心洞察

1. **标准化是关键**: 统一的 frontmatter 格式是所有技能协同工作的基础
2. **命名规范很重要**: `YYYY-MM-DD-{type}-{slug}.md` 格式便于排序和识别
3. **渐进式实现**: 先实现基础功能，再逐步添加高级特性
4. **测试驱动开发**: 每个技能实现后立即测试验证

## 相关实体

- [[龙虾AI]]: 工具集总览
- [[ob-search]]: 检索技能
- [[ob-todo]]: 任务管理技能
- [[ob-note]]: 笔记记录技能
- [[article-processor]]: 文章处理技能

## 相关概念

- [[判断卡]]: 笔记四层结构中价值最高的卡片类型
- [[方法卡]]: 可复用的操作流程
- [[案例卡]]: 验证过的事实依据
- [[信息卡]]: 基础信息记录

## 资源链接

- obsidian.md: 完整理论框架
- `C:\Users\87044\.claude\skills\pdf_to_jpg\`: 技能参考示例
- Obsidian 文档: https://help.obsidian.md/
