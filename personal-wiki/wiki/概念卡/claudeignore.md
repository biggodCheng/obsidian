---
title: claudeignore
type: 概念卡
date: 2026-05-08
tags:
  - AI
  - Claude Code
  - Token优化
  - 配置
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - 上下文窗口
  - Token经济学
lobster_cards:
  - claudeignore是投入产出比最高的单一优化
  - Claude Code深度优化方法
lobster_type:
  - 判断卡
  - 方法卡
---

# claudeignore

## 摘要
.claudeignore 文件用于告诉 Claude Code 哪些文件和目录不要加载到上下文中，语法与 .gitignore 相同。仅加一个 .next/ 就能减少 30-40% 上下文消耗。

## 典型配置
```
*.log
*.png
node_modules/
.next/
dist/
coverage/
__pycache__/
*.pyc
build/
```

## 核心价值
- 投入产出比最高的单一优化
- 排除日志、测试数据、图片素材、依赖目录等
- 每轮对话都受益，不需要额外操作

## Lobster 卡片
- [[claudeignore是投入产出比最高的单一优化]]
- [[Claude Code深度优化方法]]

## 来源
- [[搞懂Token-AI账单至少省一半]]
