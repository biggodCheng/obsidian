---
title: Prompt Caching
type: 概念卡
date: 2026-05-08
tags:
  - AI
  - Token
  - 缓存
  - 成本优化
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - Token经济学
  - 上下文窗口
lobster_cards:
  - Token优化基础方法集
lobster_type:
  - 方法卡
---

# Prompt Caching

## 摘要
Claude 和 GPT 的缓存机制：连续对话中未变化的内容命中缓存，只收正常价格的 10%。

## 核心规则
- 前面的内容（系统提示、工具定义等）没变化时自动命中缓存
- 缓存命中率高的部分只收 10% 价格
- 有效期 5 分钟，超过未发消息则缓存失效

## 实践建议
- 保持一定的对话节奏，避免缓存过期
- 不要中间去泡个茶回来发现缓存全失效了
- CLAUDE.md 等固定内容在缓存启用后几乎免费

## Lobster 卡片
- [[Token优化基础方法集]]

## 来源
- [[搞懂Token-AI账单至少省一半]]
