# LLM Wiki

这是一个使用 LLM 维护的持久化知识库。

## 快速开始

1. **摄取文档**
   ```
   请帮我摄取 raw/sources/example.pdf
   ```

2. **查询知识**
   ```
   查询 wiki：[你的问题]
   ```

3. **健康检查**
   ```
   对 wiki 进行健康检查
   ```

## 目录结构

```
.
├── raw/              # 原始源文件（只读）
│   ├── sources/      # 源文件
│   └── assets/       # 附件
├── wiki/             # LLM 维护的 wiki
│   ├── index.md      # 索引
│   ├── log.md        # 日志
│   ├── 实体卡/       # 实体页面
│   ├── 概念卡/     # 概念页面
│   ├── 摘要卡/      # 摘要页面
│   └── 综合卡/      # 综合页面
└── CLAUDE.md         # 配置文件
```

## 核心理念

不同于传统 RAG，LLM Wiki 会**增量构建和维护**一个结构化的 markdown wiki。

- 传统 RAG：每次查询时重新检索和合成
- LLM Wiki：一次性编译，持续维护

## 使用 Obsidian

推荐使用 Obsidian 查看和编辑 wiki：

1. 下载 [Obsidian](https://obsidian.md/)
2. 打开此目录作为 vault
3. 使用图形视图查看知识连接

## 详细文档

见 `.claude/skills/llm-wiki/README.md`

---

初始化时间: {{date}}
