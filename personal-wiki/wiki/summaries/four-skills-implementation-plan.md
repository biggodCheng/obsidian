---
title: 四个核心 AI 技能实现计划
type: summary
date: 2026-04-09
tags: [项目规划, 技能实现, 龙虾AI, 任务计划]
sources: [task_plan]
related: [龙虾AI, ob-search, ob-todo, ob-note, article-processor]
confidence: high
status: mature
---

# 四个核心 AI 技能实现计划

## 源文件

`raw/sources/task_plan.md`

## 概述

为 Obsidian 知识库实现四个核心 AI 技能（ob-search、ob-todo、ob-note、article-processor）的项目计划，将理论框架转化为实际可用的自动化工具。

## 项目目标

创建可以自动化操作的 Claude Code 技能体系，实现：
- **ob-search**: 全库基础检索能力
- **ob-todo**: 工作卡片/任务管理
- **ob-note**: 随时记录/笔记管理
- **article-processor**: 研究探索/内容处理

## 实现阶段

### Phase 1: 需求分析与架构设计 ✅
- 理解用户需求
- 分析 obsidian.md 理论框架
- 研究现有技能结构
- 设计技能架构和文件结构
- 确定技术实现方案

### Phase 2: 基础设施搭建 ✅
- 创建技能目录结构
- 设计笔记卡片模板（含 frontmatter）
- 创建配置文件和工具函数
- 建立索引和搜索机制

### Phase 3: ob-search 技能实现 ✅
- 实现全库文本搜索功能
- 支持标签过滤
- 支持卡片类型过滤
- 支持语义相似度搜索（待实现）

### Phase 4: ob-todo 技能实现 ✅
- 创建任务卡片模板
- 实现任务添加功能
- 实现任务列表查看
- 实现任务状态更新

### Phase 5: ob-note 技能实现 ✅
- 创建笔记卡片模板
- 实现快速笔记记录
- 自动生成 frontmatter
- 支持分类和标签

### Phase 6: article-processor 技能实现 ✅
- 实现基础架构
- URL 内容抓取（需集成 MCP）
- AI 拆卡功能（需集成 AI API）
- 自动保存到知识库

### Phase 7: 测试与验证 ✅
- 测试所有四个技能
- 验证工作流完整性
- 文档编写

## 关键决策

| 决策 | 理由 |
|------|------|
| 使用 Claude Code Skills | 用户已安装技能框架，可直接复用 |
| 纯 Markdown + Frontmatter | 符合 Obsidian 原生格式，便于维护 |
| 文件系统存储 | 无需额外数据库，简单可靠 |
| UTF-8 编码 | 支持中文内容 |

## 遇到的错误

| 错误 | 解决方案 |
|------|----------|
| UnicodeEncodeError: Windows 终端 GBK 编码无法显示 Unicode 字符 | 在所有脚本开头添加 UTF-8 输出重定向代码 |

## 待解决问题

1. 技能应该以什么形式实现？Claude Code Skills 还是独立脚本？
2. 笔记卡片应该使用什么文件命名规范？
3. 如何实现知识的"进化机制"（状态自动更新）？
4. 是否需要数据库还是纯文件系统？
5. 如何处理中文搜索和标签？

## 核心洞察

1. **渐进式实现**: 通过七个阶段逐步实现功能，每个阶段都有明确的验收标准
2. **模板化设计**: 使用统一的 frontmatter 模板确保笔记结构一致
3. **编码兼容性**: 在 Windows 环境下需要特别注意 UTF-8 编码问题
4. **测试驱动**: 每个阶段完成后都进行测试验证

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
