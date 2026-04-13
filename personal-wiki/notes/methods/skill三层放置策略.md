---
type: method
confidence: high
tags:
- skill
- multi-agent
- 分层设计
- 架构实践
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill三层发现机制
- skill与tool的分层
- OpenClaw
sources:
- https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
- main的私有skill不天然共享给其他agent
- 同名skill多层共存需标注来源
---
# Skill 三层放置策略

## 方法描述

在设计 multi-agent 系统的 skill 放置层级时，按以下三类分：

### 第一类：官方通用 Skill
- **位置**：OpenClaw 安装级全局目录（node_modules/openclaw/skills）
- **适合**：随系统分发、大多数环境复用、不依赖私人目录结构

### 第二类：机器级共享 Skill（最关键）
- **位置**：`~/.openclaw/skills` 或 `~/.agents/skills`
- **适合**：多个 agent 共同使用、跨 agent 公共能力、main 和 agency-agents 都需要稳定看到
- **适用场景**：公司内部通用 skill、整套 multi-agent 公共工作流

### 第三类：Workspace 私有 Skill
- **位置**：`~/.openclaw/workspace/skills` 或 `~/.openclaw/agency-agents/<agent-id>/skills`
- **适合**：特定 agent 专用流程、项目临时 skill、不想全局暴露的本地 workflow
- **注意**：不要默认当作全系统共享能力

## 决策依据

问自己一个问题：**这个 skill 需要被多少个 agent 使用？**
- 所有 → 第一类（全局层）
- 多个但不是所有 → 第二类（共享层）
- 仅一个 → 第三类（私有层）

## 相关 Wiki 概念
- [[skill三层发现机制]]
- [[skill与tool的分层]]