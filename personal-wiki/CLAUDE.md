# LLM Wiki 配置

## 目录结构

- `raw/` - 原始源文件（只读，LLM 不修改）
  - `sources/` - 源文件存放处
  - `assets/` - 图片等附件

- `wiki/` - LLM 生成的 wiki（读写）
  - `index.md` - 内容索引（每次摄取时更新）
  - `log.md` - 操作日志（追加记录）
  - `entities/` - 实体页面（人名、组织、产品等）
  - `concepts/` - 概念页面（理论、方法、术语等）
  - `summaries/` - 源文件摘要
  - `synthesis/` - 综合分析页面

## 摄取流程

当用户要求摄取源文件时：

1. **读取源文件**：从 `raw/sources/` 读取
2. **讨论要点**：与用户讨论关键要点
3. **创建摘要**：在 `wiki/summaries/` 创建摘要页面
4. **更新相关页面**：
   - 识别源文件中的实体和概念
   - 创建或更新 `wiki/entities/` 中的实体页面
   - 创建或更新 `wiki/concepts/` 中的概念页面
   - 添加交叉引用
5. **更新索引**：更新 `wiki/index.md`
6. **记录日志**：在 `wiki/log.md` 追加条目

单个源文件可能影响 10-15 个 wiki 页面。

## 查询流程

当用户查询 wiki 时：

1. **读取索引**：先读 `wiki/index.md` 找到相关页面
2. **深入页面**：读取相关页面内容
3. **综合答案**：综合信息并引用来源
4. **归档答案**：如果答案有价值，作为新页面保存到 `wiki/synthesis/`

答案格式可以是：
- Markdown 页面
- 对比表格
- 幻灯片（Marp）
- 图表描述

## Lint 流程

当用户要求健康检查时：

1. **检查矛盾**：查找页面之间的矛盾声明
2. **找出孤立**：识别没有入站链接的孤立页面
3. **缺失引用**：找到缺失的交叉引用
4. **数据空白**：识别可以填补的数据空白
5. **生成报告**：创建综合报告
6. **记录日志**：在 `wiki/log.md` 追加条目

## 页面格式

所有 wiki 页面应包含：

```markdown
---
title: 页面标题
type: entity|concept|summary|synthesis
date: YYYY-MM-DD
tags: [tag1, tag2]
sources: [source1, source2]
related: [page1, page2]
---

# 页面标题

## 摘要
一句话概括

## 内容
详细内容...

## 关联
- [[相关页面1]]
- [[相关页面2]]

## 来源
- [[源文件摘要]]
```

## 交叉引用

使用 Obsidian 风格的 wikilinks：
- `[[页面标题]]` - 链接到其他页面
- `[[页面标题|显示文本]]` - 自定义链接文本

确保所有提到的实体和概念都有对应的页面。

## 日志格式

每次操作在 `wiki/log.md` 追加：

```markdown
## [YYYY-MM-DD] ingest | Article Title

**源文件**: `raw/sources/article.pdf`

**操作**:
- 创建摘要: `wiki/summaries/article.md`
- 更新实体: `wiki/entities/entity1.md`, `wiki/entities/entity2.md`
- 更新概念: `wiki/concepts/concept1.md`

**统计**:
- 新增页面: 1
- 更新页面: 3
- 识别实体: 2
- 识别概念: 1
```

## 注意事项

1. **Raw sources 不可变**：LLM 只读，从不修改 `raw/` 目录
2. **Wiki 完全由 LLM 拥有**：LLM 创建、更新、维护所有 wiki 页面
3. **保持一致性**：确保交叉引用始终最新
4. **记录一切**：所有操作都记录在 `wiki/log.md`

---

配置版本: 1.0.0
最后更新: {{date}}
