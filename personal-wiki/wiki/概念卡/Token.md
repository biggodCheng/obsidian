---
title: Token
type: 概念卡
date: 2026-05-08
tags:
  - AI
  - Token
  - 计费
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - Token经济学
  - 上下文窗口
  - BPE
lobster_cards:
  - 输出Token成本是输入的5倍
  - 不同语言Token消耗对比
  - Token优化基础方法集
lobster_type:
  - 判断卡
  - 方法卡
  - 案例卡
---

# Token

## 摘要
Token 是 AI 的最小阅读单位，不是字也不是词。通过 BPE（字节对编码）算法按词频切分文本。

## 核心特征
- 高频词整体保留为 1 个 Token（如 hello）
- 低频词拆成碎片（如 indescribable → in + describ + able，3 个 Token）
- 中文基本一个字一个 Token，偶尔两字合成一个
- 代码中的空格、换行、括号全都是 Token
- 格式优美但缩进深的代码，Token 数可能比压缩版多 30-40%

## 语言差异
- 英文最省（高频词整体保留）
- 简体中文稍贵
- 繁体中文最贵（低频字被拆成字节级碎片）
- 根本原因：训练数据中的词频决定切分效率

## 计费逻辑
- 不是按说了多少话，而是按 AI 需要处理多少碎片
- 每个 Token 都要经过模型全部参数的计算
- Token = 算力的代名词

## Lobster 卡片
- [[输出Token成本是输入的5倍]]
- [[不同语言Token消耗对比]]
- [[Token优化基础方法集]]

## 来源
- [[搞懂Token-AI账单至少省一半]]
