---
title: Skill三层发现机制
type: concept
date: 2026-04-12
tags:
  - skill
  - agent架构
  - 分层设计
  - multi-agent
sources:
  - https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
  - skill与tool的分层
  - OpenClaw
lobster_cards:
  - skill三层放置策略
  - main的私有skill不天然共享给其他agent
  - 同名skill多层共存需标注来源
---

# Skill 三层发现机制

## 概述

OpenClaw 的 Skill 不是从一个统一目录加载，而是从三个层次依次发现：

```
┌─────────────────────────────────────┐
│  第一层：全局安装层                    │  ← OpenClaw 安装包自带
│  node_modules/openclaw/skills       │
├─────────────────────────────────────┤
│  第二层：机器级共享层                  │  ← 跨 agent 复用
│  ~/.openclaw/skills                 │
│  ~/.agents/skills                   │
├─────────────────────────────────────┤
│  第三层：Agent Workspace 私有层       │  ← 单 agent 专用
│  ~/.openclaw/workspace/skills       │
│  ~/.openclaw/agency-agents/<id>/skills │
└─────────────────────────────────────┘
```

## 三层对比

| 层级 | 位置 | 共享范围 | 适用场景 |
|------|------|----------|----------|
| 全局安装层 | `node_modules/openclaw/skills` | 所有 agent | 系统级通用能力 |
| 共享层 | `~/.openclaw/skills` | 跨 workspace | 多 agent 复用的自定义 skill |
| 私有层 | `<agent-workspace>/skills` | 仅当前 agent | 角色专用流程 |

## 共享可见性规则

- **全局层 skill**：main、agency-agents、sub-agent 通常都可用
- **共享层 skill**：main 和 agency-agents 更大概率都可见
- **私有层 skill**：只有当前 agent 最容易使用，其他 agent 不天然共享

## 同名 Skill 冲突

同名 skill 同时存在于多层时，可能出现：
- 修改的不是实际生效的那份
- 不同 agent 运行时读到不同版本

解决方案：标注来源（官方内置版 / 本机共享版 / 私有版 / 本地覆盖版）

## 相关概念
- [[skill与tool的分层]]

## Lobster 卡片
- [[skill三层放置策略]]
- [[main的私有skill不天然共享给其他agent]]
- [[同名skill多层共存需标注来源]]

## 来源
- [[OpenClaw多Agent Skills分层调用机制]]
