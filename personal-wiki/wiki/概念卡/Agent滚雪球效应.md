---
title: Agent滚雪球效应
type: 概念卡
date: 2026-05-08
tags:
  - AI
  - Agent
  - Token
  - 成本
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - Token经济学
  - 上下文窗口
lobster_cards:
  - 方向错了立刻停
  - Agent极端Token消耗案例
  - Claude Code深度优化方法
lobster_type:
  - 判断卡
  - 方法卡
  - 案例卡
---

# Agent滚雪球效应

## 摘要
Agent 模式下每轮对话都带完整上下文，Token 消耗呈指数级增长，如同滚雪球。

## 消耗模型
- 第 1 轮：系统提示 + 指令 = 5000 Token
- 第 2 轮：上面 5000 + AI 回复 + 读取文件 = 15000 Token
- 第 3 轮：上面 15000 + 新操作 = 30000 Token
- 每一轮都把前面所有内容再处理一遍

## 传统聊天 vs Agent
- 传统：100 输入 + 500 输出 = 600 Token
- Agent：100 输入 → 思考 → 读文件 → 分析 → 写代码 → 测试 → 改错 → 再测 → 回复，内部可能转十几轮

## 核心影响
- 一次长会话 Token 消耗可达几十万甚至上百万
- 方向错误时，每轮都在为前面所有错误上下文买单
- 重开对话反而更省

## 应对策略
- 方向错了立刻停
- /clear 切换任务
- /compact 主动压缩
- Subagent 隔离上下文
- Rewind 撤回错误轮次

## Lobster 卡片
- [[方向错了立刻停]]
- [[Agent极端Token消耗案例]]
- [[Claude Code深度优化方法]]

## 来源
- [[搞懂Token-AI账单至少省一半]]
