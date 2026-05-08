---
type: 判断卡
confidence: high
tags:
  - AI
  - Claude Code
  - Token优化
  - 配置
created: 2026-05-08
updated: 2026-05-08
wiki_concepts:
  - claudeignore
  - 上下文窗口
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - Claude Code深度优化方法
  - 方向错了立刻停
---

# claudeignore是投入产出比最高的单一优化

## 判断内容
.claudeignore 是投入产出比最高的单一 Token 优化手段。仅加一个 .next/ 就能减少 30-40% 上下文消耗，一次配置每轮受益。

## 判断依据
- 语法与 .gitignore 相同，配置成本极低
- 排除 node_modules/、dist/、coverage/、.next/ 等目录
- 这些文件在分析项目时会被自动读入上下文，白白占用 Token
- 每轮对话都受益，不需要额外操作

## 适用条件
- 使用 Claude Code 或类似 AI 编程工具
- 项目包含日志文件、测试数据、依赖目录、构建产物等
- 必须在项目根目录创建 .claudeignore 文件

## 相关 Wiki 概念
- [[claudeignore]]
- [[上下文窗口]]

## 来源
- [[搞懂Token-AI账单至少省一半]]

## 相关卡片
- [[Claude Code深度优化方法]]
- [[方向错了立刻停]]
