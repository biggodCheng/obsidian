---
type: judgment
confidence: high
tags:
- skill
- multi-agent
- agent架构
- 共享机制
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill三层发现机制
- skill与tool的分层
- OpenClaw
sources:
- https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
- sub-agent不是main的克隆而是子会话实例
- skill三层放置策略
---
# Main 的私有 Skill 不天然共享给其他 Agent

## 判断内容

Main agent 的本地 workspace skill，并不天然等于所有 imported agent 的本地 skill。共享与否取决于 skill 放在哪一层：

| Skill 放置层 | 共享情况 |
|-------------|----------|
| 全局安装层 | main、agency-agents、sub-agent 通常都可用 |
| 共享层（~/.openclaw/skills） | 跨 workspace 更大概率可见 |
| Main workspace 私有层 | 不应默认其他 agent 也能用 |

**关键判断**：对于只放在 main workspace 的 skill，最稳妥的态度不是拍脑袋，而是做实测。

## 适用条件

- 设计 multi-agent 协作架构时
- 排查 "为什么别的 agent 用不了这个 skill" 问题时

## 相关 Wiki 概念
- [[skill三层发现机制]]
- [[skill与tool的分层]]
## 来源
- [https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ](https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ)