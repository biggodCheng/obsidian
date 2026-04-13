# LLM Wiki - 使用文档

## 快速开始

### 1. 初始化 Wiki

```bash
# 使用初始化脚本
./bin/init-wiki.sh
```

这会创建以下目录结构：

```
your-wiki/
├── raw/                    # 原始源文件
│   ├── sources/
│   └── assets/
├── wiki/                   # LLM 维护的 wiki
│   ├── entities/
│   ├── concepts/
│   ├── summaries/
│   └── synthesis/
├── wiki/index.md           # 内容索引
├── wiki/log.md             # 操作日志
└── CLAUDE.md               # Schema 配置
```

### 2. 配置 Claude

编辑 `CLAUDE.md`，根据你的需求自定义配置。

### 3. 摄取文档

```
请帮我摄取这个文档到 wiki：[文档路径或 URL]
```

### 4. 查询 Wiki

```
查询 wiki：[你的问题]
```

### 5. 健康检查

```
对 wiki 进行健康检查
```

## 命令参考

### 摄取操作

```
# 摄取单个文件
请帮我摄取 raw/sources/article.pdf

# 摄取并讨论
请帮我摄取这个文档，并讨论关键要点：raw/sources/paper.md

# 批量摄取
请帮我摄取 raw/sources/ 目录下的所有文档
```

### 查询操作

```
# 简单查询
查询 wiki：什么是 X？

# 对比查询
查询 wiki：对比 A 和 B 的区别

# 综合查询
查询 wiki：总结关于主题 X 的所有内容
```

### 维护操作

```
# 健康检查
对 wiki 进行健康检查

# 更新索引
请更新 wiki/index.md

# 查找孤立页面
找出 wiki 中的孤立页面
```

## 最佳实践

### 摄取建议

1. **一次一个**：一次摄取一个源文件
2. **保持参与**：阅读摘要，检查更新
3. **指导 LLM**：告诉它什么重要

### 查询建议

1. **归档答案**：将有价值的答案作为新页面保存
2. **多种格式**：使用 markdown、表格、幻灯片等
3. **引用来源**：确保答案引用源文件

### 维护建议

1. **定期 Lint**：每周进行一次健康检查
2. **更新日志**：每次操作后更新 log.md
3. **清理孤立**：定期处理孤立页面

## 工具集成

### Obsidian

推荐使用 Obsidian 作为 wiki 的前端：

1. **打开 Wiki 目录**
   ```
   obsidian://open?vault=your-wiki&path=wiki
   ```

2. **安装插件**
   - Dataview：查询 frontmatter
   - Graph Analysis：可视化知识图谱
   - Marp：生成幻灯片

3. **使用 Web Clipper**
   - 安装 Obsidian Web Clipper 浏览器扩展
   - 快速将网页转换为 markdown

### 搜索

- **小规模**（< 100 页）：使用 wiki/index.md
- **中规模**（100-1000 页）：使用 ripgrep + grep
- **大规模**（> 1000 页）：考虑 qmd 或 Meilisearch

## 示例工作流

### 研究项目

```
# 第 1 天
请帮我摄取 raw/sources/paper1.pdf

# 第 2 天
查询 wiki：paper1 的主要贡献是什么？
请帮我摄取 raw/sources/paper2.pdf

# 第 3 天
查询 wiki：paper1 和 paper2 的方法有什么区别？

# 第 4 天
对 wiki 进行健康检查
```

### 读书笔记

```
# 第 1 章
请帮我摄取第 1 章并创建角色页面

# 第 2 章
请帮我摄取第 2 章并更新角色关系图

# 完成
查询 wiki：总结整个故事的主线
```

### 团队知识库

```
# 每周例会
请将会议记录摄取到 wiki

# 项目文档
请更新项目 X 的 wiki 页面

# 季度回顾
对 wiki 进行健康检查和总结
```

## 故障排除

### 问题：Wiki 增长过快

**解决方案**：
- 定期进行 Lint
- 删除重复或过时内容
- 考虑使用更精细的分类

### 问题：查询结果不准确

**解决方案**：
- 更新 wiki/index.md
- 检查相关页面是否有足够的交叉引用
- 考虑重新摄取相关源文件

### 问题：Wiki 中有矛盾

**解决方案**：
- 运行健康检查
- 查看日志找到相关源文件
- 手动审查并解决矛盾

## 进阶技巧

### 使用 Frontmatter

在 wiki 页面中添加 YAML frontmatter：

```markdown
---
title: 页面标题
date: 2026-04-08
tags: [tag1, tag2]
sources: 3
related: [page1, page2]
confidence: high
---
```

### 使用 Dataview

在 Obsidian 中使用 Dataview 插件查询：

```dataview
TABLE title, date, sources
FROM "wiki"
WHERE contains(tags, "important")
SORT date DESC
```

### 使用 Graph

使用 Obsidian 的图形视图：
- 查看知识连接
- 识别孤立页面
- 发现隐藏关系

## 资源

- [原始概念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Obsidian 下载](https://obsidian.md/)
- [Obsidian Web Clipper](https://github.com/obsidianmd/obsidian-web-clipper)

---

**提示**：这个 skill 的核心是让 LLM 做所有繁琐的维护工作，你只需要策展源文件、提出好问题、思考这意味着什么。
