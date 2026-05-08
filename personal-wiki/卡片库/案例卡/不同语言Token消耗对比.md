---
type: 案例卡
confidence: high
tags:
  - AI
  - Token
  - 语言差异
  - 计费
created: 2026-05-08
updated: 2026-05-08
wiki_concepts:
  - Token
  - Token经济学
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - Token优化基础方法集
  - Agent极端Token消耗案例
---

# 不同语言Token消耗对比

## 案例内容
同一句话「我很喜欢这个应用」在不同语言版本下的 Token 消耗对比，验证了训练语料词频决定切分效率的规律。

## 关键数据
- 英文 "I love this app"：4 个 Token
- 简体中文「我很喜欢这个应用」：5 个 Token
- 繁体中文「我很喜歡這個應用」：8 个 Token

## 案例分析
- 英文：love、this、app 都是高频词，各占 1 个 Token
- 简体中文：「喜欢」「这个」「应用」是常见词组，被合并成单个 Token
- 繁体中文：「喜歡」拆成「喜」+「歡」，「這個」拆成「這」+「個」，「應用」拆成「應」+「用」，每个都打散

## 规律总结
- 英文最省（训练语料中英文最高频）
- 简体中文稍贵
- 繁体中文和生僻词最贵
- 根本原因：训练数据中的词频决定 Token 切分效率
- 国产模型中文语料更全，中文 Token 效率更高

## 相关 Wiki 概念
- [[Token]]
- [[Token经济学]]

## 来源
- [[搞懂Token-AI账单至少省一半]]

## 相关卡片
- [[Token优化基础方法集]]
- [[Agent极端Token消耗案例]]
