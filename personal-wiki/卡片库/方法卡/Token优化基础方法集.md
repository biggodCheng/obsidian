---
type: 方法卡
confidence: high
tags:
  - AI
  - Token优化
  - 方法论
  - 成本优化
created: 2026-05-08
updated: 2026-05-08
wiki_concepts:
  - Token
  - Token经济学
  - Prompt Caching
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - 输出Token成本是输入的5倍
  - Claude Code深度优化方法
---

# Token优化基础方法集

## 方法内容

### 1. 让 AI 少说废话
- 提示词加「不要解释，直接给结果」或「Skip the preamble」
- 减少 30-50% 输出 Token
- 输出价格是输入 5 倍，省输出比省输入更有效

### 2. 精准表达，避免模糊提问
- 不要「帮我写一篇周报」
- 要「帮我写本周周报，做了三件事：1... 2... 3... 风格简洁」
- 模糊提问的来回纠错是最隐蔽的 Token 浪费

### 3. 同类需求整合一次输入
- 三个需求合并一次提问，比分三次问省很多 Token
- 瓶颈在输出端不在输入端

### 4. 结构化输出限制
- 「用表格输出」比自然语言省 3-5 倍
- 「每条不超过两句话」防止展开论述
- 「只列要点，不要解释」砍掉最占 Token 的部分
- 「回复控制在 200 字以内」直接设上限

### 5. 利用 Prompt Caching
- 保持对话节奏，避免 5 分钟缓存过期
- 连续对话中未变化内容只收 10% 价格

## 相关 Wiki 概念
- [[Token]]
- [[Token经济学]]
- [[Prompt Caching]]

## 来源
- [[搞懂Token-AI账单至少省一半]]

## 相关卡片
- [[输出Token成本是输入的5倍]]
- [[Claude Code深度优化方法]]
