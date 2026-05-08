---
type: 方法卡
confidence: high
tags:
  - AI
  - Claude Code
  - Token优化
  - 编程工具
created: 2026-05-08
updated: 2026-05-08
wiki_concepts:
  - claudeignore
  - 上下文窗口
  - Subagent隔离
  - Agent滚雪球效应
sources:
  - 搞懂Token-AI账单至少省一半
related:
  - claudeignore是投入产出比最高的单一优化
  - Token优化基础方法集
---

# Claude Code深度优化方法

## 方法内容

### 上下文管理（最核心杠杆）
- /clear：切换任务时必用，清除无关上下文
- /compact：60-70% 时主动压缩，可加指令指定保留内容
- /btw：问小问题不进入上下文
- /context：诊断每个元素占多少 Token
- Rewind（两下 Esc）：撤回上一轮，比 /clear 更精细

### 项目配置
- .claudeignore 必须有（减少 30-40% 上下文消耗）
- CLAUDE.md 控制在 200 行以内（每轮对话的固定税）
- 专项指令移入 Skills（不调用时不加载）
- 精简 MCP Server（禁用不活跃的 Server）
- 善用 !bash 直接喂精准信息（省来回试探轮次）

### 执行策略
- Plan Mode 先规划再执行（Shift+Tab 进入）
- /effort 调节思考深度（low/medium/high）
- 按任务切模型：Sonnet 日常编码 / Opus 复杂架构 / Haiku 批量简单任务
- Subagent 隔离调查性工作（主上下文只增加摘要）
- 精确指定文件和行号（避免触发广泛文件搜索）
- 一个任务一个会话
- 给验证目标而非模糊指令

### Hooks 预处理
- 测试结果自动过滤只保留 FAIL/ERROR
- 代码格式化自动化
- 把不必要信息拦在上下文之外

### 多会话协作
- 长任务结束时让 Claude 写 300 字交接摘要
- 下次新会话直接给摘要，避免重新探索

## 相关 Wiki 概念
- [[claudeignore]]
- [[上下文窗口]]
- [[Subagent隔离]]
- [[Agent滚雪球效应]]

## 来源
- [[搞懂Token-AI账单至少省一半]]

## 相关卡片
- [[claudeignore是投入产出比最高的单一优化]]
- [[Token优化基础方法集]]
