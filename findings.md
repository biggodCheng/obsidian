# Findings & Decisions
<!--
  WHAT: 四个核心 AI 技能实现的知识库
  WHY: 记录研究发现、技术决策和问题解决方案
  WHEN: 持续更新
-->

## Requirements
基于 obsidian.md 理论框架，需要实现四个核心 AI 技能：

### ob-search（检索技能）
- 提供全库基础检索能力
- 支持关键词搜索
- 支持标签过滤
- 支持卡片类型过滤（judgment/method/case/information）
- 返回按相关度排序的结果

### ob-todo（任务管理）
- 工作卡片/任务管理
- 快速记录任务
- 任务状态追踪
- 任务提醒功能

### ob-note（笔记管理）
- 随时记录/笔记管理
- 快速创建笔记卡片
- 自动生成 frontmatter
- 支持分类和标签

### article-processor（内容处理）
- 研究探索/内容处理
- URL 内容抓取
- 正文提取
- AI 拆卡（自动提炼判断卡）

## Research Findings
- Obsidian 使用纯 Markdown 文件 + YAML Frontmatter
- 双向链接语法：`[[文件名]]`
- 标签语法：`#标签名`
- 已存在的技能目录：`C:\Users\87044\.claude\skills\`
- 用户已有 pdf_to_jpg 技能作为参考

### 技能结构（skill.md 格式）
```yaml
---
name: skill-name
description: 技能描述
user-invocable: true
---
```

### 笔记卡片 Frontmatter 模板设计
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

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 技能存放位置 | C:\Users\87044\.claude\skills\lobster-*\ |
| 笔记存放位置 | d:\DATA\cgq-obsidian\notes\ |
| 卡片命名规范 | YYYY-MM-DD-{type}-{slug}.md |
| Frontmatter 格式 | YAML 标准格式 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
|       |            |

## Resources
- obsidian.md: 完整理论框架
- C:\Users\87044\.claude\skills\pdf_to_jpg\: 技能参考示例
- Obsidian 文档: https://help.obsidian.md/

## Visual/Browser Findings
-

## Test Results
所有四个核心技能测试通过：
- ob-note: 成功创建判断卡、方法卡、案例卡、信息卡
- ob-search: 成功搜索并返回匹配的笔记
- ob-todo: 成功添加任务、列出任务
- article-processor: 基础架构完成（需集成 MCP 才能完整使用）

创建的示例笔记：
- notes/2026-03-30-judgment-价格敏感度测试.md
- notes/2026-03-30-todo-完成四个核心技能测试.md

---
*持续更新此文件以记录研究发现*
