# LLM Wiki 使用示例

## 示例 1: 研究项目 - 机器学习论文

### 初始化

```
./bin/init-wiki.sh ml-research
cd ml-research
```

### 第 1 天 - 摄取第一篇论文

```
请帮我摄取 raw/sources/attention-is-all-you-need.pdf

重点提取：
1. 核心创新点
2. 架构设计
3. 实验结果
4. 相关工作
```

**LLM 会**：
- 创建 `wiki/summaries/attention-is-all-you-need.md`
- 创建/更新 `wiki/entities/Google.md`, `wiki/entities/Transformer.md`
- 创建/更新 `wiki/concepts/Self-Attention.md`, `wiki/concepts/Multi-Head Attention.md`
- 更新 `wiki/index.md`
- 记录到 `wiki/log.md`

### 第 2 天 - 查询和对比

```
查询 wiki：Transformer 相比 RNN 和 CNN 的优势是什么？

请生成一个对比表格，作为新页面保存到 wiki/synthesis/
```

### 第 3 天 - 摄取第二篇论文

```
请帮我摄取 raw/sources/bert.md

更新相关实体页面：
- Google 的 NLP 研究时间线
- Transformer 架构的演进
```

### 第 4 天 - 深度查询

```
查询 wiki：从 Attention 到 BERT，架构演进的关键里程碑是什么？

请创建一个时间线页面，保存到 wiki/synthesis/timeline.md
```

### 第 5 天 - 健康检查

```
对 wiki 进行健康检查

特别关注：
1. Attention 机制在不同论文中的描述是否一致
2. 是否有孤立的概念页面
3. 缺失的交叉引用
```

## 示例 2: 读书笔记 - 小说

### 初始化

```
./bin/init-wiki.sh novel-卡片库
cd novel-卡片库
```

### 第 1 章处理

```
请帮我摄取 chapter-01.md

任务：
1. 创建章节摘要
2. 识别所有角色，创建角色页面
3. 识别重要地点，创建地点页面
4. 记录关键情节
```

### 第 2 章处理

```
请帮我摄取 chapter-02.md

更新：
1. 现有角色的描述和关系
2. 创建新角色页面
3. 更新情节时间线
4. 添加章节间的联系
```

### 中途查询

```
查询 wiki：角色 A 和角色 B 的关系是如何发展的？

请创建一个关系图页面，包含：
- 初次相遇
- 关键互动
- 关系变化
```

### 完成后总结

```
查询 wiki：生成一个完整的角色列表和关系图

格式：
1. 按出场顺序排列
2. 标注主要/次要角色
3. 包含角色关系网络
```

## 示例 3: 产品知识库

### 初始化

```
./bin/init-wiki.sh product-kb
cd product-kb
```

### 摄取产品文档

```
请帮我摄取产品文档目录 raw/sources/docs/

包括：
- 用户手册
- API 文档
- 架构文档
- 常见问题
```

### 创建功能页面

```
为以下功能创建 wiki 页面：
1. 用户认证
2. 数据同步
3. 权限管理

每个页面包含：
- 功能描述
- 使用场景
- 技术实现
- 已知问题
- 相关功能
```

### 查询和对比

```
查询 wiki：对比不同认证方式的优缺点

生成对比表格，保存到 wiki/synthesis/auth-comparison.md
```

### 定期维护

```
每周执行：
1. 摄取新的更新日志
2. 更新功能页面
3. 运行健康检查
4. 更新索引
```

## 示例 4: 学习笔记 - 编程语言

### 初始化

```
./bin/init-wiki.sh rust-learning
cd rust-learning
```

### 按主题摄取

```
请帮我摄取并整理以下主题：

1. 所有权系统
   - raw/sources/ownership.md
   - 创建概念页面：所有权、借用、生命周期

2. 并发编程
   - raw/sources/concurrency.md
   - 更新相关概念页面

3. 错误处理
   - raw/sources/error-handling.md
   - 创建对比页面：Result vs Option
```

### 创建学习路径

```
查询 wiki：生成 Rust 学习路径

包括：
1. 基础概念（按难度排序）
2. 实践项目建议
3. 常见陷阱和解决方案
```

### 复习和测试

```
查询 wiki：给我出 10 道关于所有权系统的测试题

然后：
1. 我回答问题
2. LLM 评判答案
3. 更新我的知识薄弱点页面
```

## 示例 5: 会议记录和决策

### 初始化

```
./bin/init-wiki.sh team-wiki
cd team-wiki
```

### 摄取会议记录

```
请帮我摄取 meeting-2026-04-08.md

提取：
1. 参与人员（更新人员页面）
2. 讨论主题（创建/更新主题页面）
3. 决策事项（创建决策页面）
4. 行动项（创建任务页面）
```

### 追踪决策

```
查询 wiki：关于项目 X 的所有决策

生成：
- 决策时间线
- 决策理由
- 影响分析
- 相关讨论
```

### 定期回顾

```
每周回顾：

查询 wiki：本周的重要决策和行动项

生成报告：
1. 新决策
2. 进度更新
3. 风险和问题
4. 下周计划
```

## 高级用法

### 使用 Frontmatter 增强

```markdown
---
title: Transformer 架构
type: concept
date: 2026-04-08
tags: [深度学习, NLP, 架构]
sources: [attention-is-all-you-need, bert, gpt]
related: [Self-Attention, Encoder-Decoder]
confidence: high
---

# Transformer 架构

## 核心思想
...
```

### 使用 Dataview 查询

```dataview
TABLE title, date, confidence, sources
FROM "wiki/concepts"
WHERE contains(tags, "NLP")
SORT date DESC
```

### 创建自定义模板

创建 `wiki/.templates/summary.md`：

```markdown
---
title: "{{title}}"
type: summary
date: {{date}}
tags: {{tags}}
---

# {{title}}

## 源文件
- 文件名: {{filename}}
- 作者: {{author}}
- 日期: {{pub_date}}

## 核心内容
{{content}}

## 关键要点
{{key_points}}

## 相关内容
{{related}}
```

## 常见场景

### 场景 1: 快速查找

```
我在找一个概念，但记不清具体名称

查询 wiki：帮我找所有关于"注意力"的页面
```

### 场景 2: 深度理解

```
我想深入理解某个主题

查询 wiki：关于"所有权"，给我一个完整的学习路径

包括：
1. 基础概念
2. 进阶内容
3. 实践建议
4. 常见误区
```

### 场景 3: 发现连接

```
我想知道两个概念的关系

查询 wiki："概念A"和"概念B"有什么关系？

请分析：
1. 直接关联
2. 间接关联
3. 历史演进
4. 应用场景
```

### 场景 4: 生成内容

```
我需要基于 wiki 生成一份报告

查询 wiki：基于所有关于"主题X"的页面，生成一份技术报告

格式：
1. 执行摘要
2. 背景介绍
3. 核心内容
4. 对比分析
5. 结论建议
```

---

这些示例展示了 LLM Wiki 在不同场景下的应用。核心思想是：**让 LLM 做所有繁琐的维护工作，你只需要策展源文件、提出好问题、思考这意味着什么**。
