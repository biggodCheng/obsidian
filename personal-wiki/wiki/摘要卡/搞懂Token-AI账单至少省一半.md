---
title: 搞懂Token-AI账单至少省一半
type: 摘要
date: 2026-05-08
tags:
  - Token
  - AI成本优化
  - Claude Code
  - Agent
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - Token
  - Token经济学
  - 上下文窗口
  - Agent滚雪球效应
  - Prompt Caching
  - claudeignore
  - Subagent隔离
  - stormzhang
lobster_cards:
  - 输出Token成本是输入的5倍
  - 选对模型比什么都重要
  - claudeignore是投入产出比最高的单一优化
  - 方向错了立刻停
  - Token优化基础方法集
  - Claude Code深度优化方法
  - Agent极端Token消耗案例
  - 不同语言Token消耗对比
lobster_type:
  - 判断卡
  - 方法卡
  - 案例卡
---

# 搞懂Token-AI账单至少省一半

## 摘要
stormzhang 从底层逻辑到实操省钱，一次性讲透 Token 优化。核心观点：理解 Token 计费机制是 AI 时代的基础能力，合理优化可省 40-50% 成本。

## 核心要点

### Token 基础
- Token 是 AI 最小阅读单位，不是字也不是词
- BPE 算法按词频切分：高频词整体保留，低频词拆成碎片
- 中文比英文更费 Token，繁体最贵（训练语料词频决定）
- 代码空格、换行、括号全都是 Token

### Token 经济学
- 输出 Token 价格是输入的 5 倍（串行生成 vs 并行处理）
- 隐性 Token：系统提示词、对话历史、工具描述、项目文件
- 上下文窗口是「视野」不是「记忆」，越长越贵

### Agent 时代的消耗变化
- Agent 模式带来滚雪球效应，每轮都带完整上下文
- 极端案例：49 个子任务并行 2.5 小时花费 8000-15000 美金

### 基础优化方法
- 让 AI 少说废话（省 30-50% 输出 Token）
- 精准表达避免模糊提问
- 同类需求整合一次输入
- 结构化输出限制（表格比长文省 7 倍）
- 选对模型（Opus 只比 Sonnet 强 1.2% 但贵 67%）
- 要 diff 不要全文、先最小实现再迭代
- 方向错了立刻停、利用 Prompt Caching

### Claude Code 深度优化
- .claudeignore 减少 30-40% 上下文消耗
- /clear 切换任务、/compact 主动压缩、/effort 调节思考深度
- CLAUDE.md 控制在 200 行以内
- Subagent 隔离上下文、按任务切模型
- Rewind 撤回错误轮次
- Hooks 预处理长输出

## Lobster 卡片
- [[输出Token成本是输入的5倍]]
- [[选对模型比什么都重要]]
- [[claudeignore是投入产出比最高的单一优化]]
- [[方向错了立刻停]]
- [[Token优化基础方法集]]
- [[Claude Code深度优化方法]]
- [[Agent极端Token消耗案例]]
- [[不同语言Token消耗对比]]

## 来源
- [[搞懂Token-AI账单至少省一半]]
