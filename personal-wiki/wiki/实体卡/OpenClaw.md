---
title: OpenClaw
type: 实体卡
date: 2026-04-12
tags:
  - OpenClaw
  - multi-agent
  - AI平台
  - agent框架
sources:
  - https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
  - skill与tool的分层
  - skill三层发现机制
  - DracoVibeCoding
lobster_cards:
  - Tool是能力Skill是方法
  - skill三层放置策略
---

# OpenClaw

## 简介

OpenClaw 是一个多智能体（multi-agent）AI 平台/框架，支持运行多个 AI Agent 实例进行协作。

## 核心能力

- 多 Agent 协作管理
- Skills 分层发现机制（全局安装层、共享层、workspace 私有层）
- sessions_spawn 子代理拉起机制
- Agency-agents 导入管理
- Tool 权限控制

## 目录结构

```
~/.openclaw/
├── workspace/          # main agent workspace
│   └── skills/
├── agents/
└── agency-agents/      # imported agents
    ├── software-architect/
    │   └── skills/
    ├── product-manager/
    │   └── skills/
    └── security-engineer/
        └── skills/
```

## 关键概念

- [[skill与tool的分层]]
- [[skill三层发现机制]]

## 相关文章
- [[OpenClaw多Agent Skills分层调用机制]]

## Lobster 卡片
- [[Tool是能力Skill是方法]]
- [[skill三层放置策略]]
