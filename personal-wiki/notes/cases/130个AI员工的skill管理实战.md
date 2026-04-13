---
type: case
confidence: medium
tags:
- OpenClaw
- multi-agent
- skill管理
- 实战案例
status: new
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill三层发现机制
- OpenClaw
- DracoVibeCoding
sources:
- https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
- skill三层放置策略
- main的私有skill不天然共享给其他agent
---
# 130 个 AI 员工的 Skill 管理实战

## 案例描述

DracoVibeCoding 在企业微信中通过 OpenClaw + The Agency 运行了 130+ 个 AI Agent 实例，在此基础上总结出 skills 分层管理机制。

## 背景问题

在 130+ agent 的规模下，skill 管理面临的核心问题：
- skill 和 tool 边界不清
- skill 目录层级混乱
- main agent 能用的 skill，sub-agent 不一定能用
- 不同 agent 之间 skill 共享关系不明确
- 同名 skill 在不同位置可能导致行为不一致

## 解决方案

采用三层 skill 发现机制：
1. 全局安装层放系统级通用 skill
2. 共享层（~/.openclaw/skills）放跨 agent 复用的自定义 skill
3. 各 agent workspace 私有层放角色专用 skill

## 关键经验

- 机制上先看层次，落实上一定要抽样实测
- 实测比纯目录猜测更可靠
- Skill 放哪不只是目录问题，而是架构问题

## 相关 Wiki 概念
- [[OpenClaw]]
- [[skill三层发现机制]]
- [[DracoVibeCoding]]