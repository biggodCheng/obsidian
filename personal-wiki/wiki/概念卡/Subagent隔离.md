---
title: Subagent隔离
type: 概念卡
date: 2026-05-08
tags:
  - AI
  - Claude Code
  - Token优化
  - Agent
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - 上下文窗口
  - Agent滚雪球效应
lobster_cards:
  - Claude Code深度优化方法
lobster_type:
  - 方法卡
---

# Subagent隔离

## 摘要
让 Claude 用 Subagent 做调查性工作，Subagent 在独立上下文窗口运行，只返回摘要给主对话，大幅减少主上下文膨胀。

## 核心机制
- Subagent 在独立的上下文窗口运行
- 可能读了 6000 Token 的文件，但只返回 400 Token 的摘要
- 主上下文只增加 400 Token，而非 6000
- 设置 CLAUDE_CODE_SUBAGENT_MODEL=haiku 让子代理默认用便宜模型

## 适用场景
- 调查性工作：「用子代理去调查 auth 模块是怎么处理 token 刷新的」
- 文件搜索和阅读
- 代码分析
- 任何不需要留在主上下文中的信息收集

## Lobster 卡片
- [[Claude Code深度优化方法]]

## 来源
- [[搞懂Token-AI账单至少省一半]]
