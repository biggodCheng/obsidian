---
title: Skill与Tool的分层
type: concept
date: 2026-04-12
tags:
- skill
- tool
- agent架构
- 分层设计
sources:
- https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
- skill三层发现机制
- OpenClaw
lobster_cards:
- Tool是能力Skill是方法
- main的私有skill不天然共享给其他agent
- skill三层放置策略
- skill目录结构设计规范
---
# Skill 与 Tool 的分层

## 定义

在多 Agent 系统中，Tool 和 Skill 是两个不同层次的概念：

| 维度 | Tool | Skill |
|------|------|-------|
| 本质 | 能力层 | 方法层 |
| 回答的问题 | 能不能做？ | 怎么做？按什么步骤？ |
| 类比 | 手和脚 | 作战手册/标准流程 |
| 示例 | read, write, exec, browser | SKILL.md + references/ + scripts/ |

## 关键洞察

> "一个 agent 看得见某个 skill"，并不自动等于"它一定能把这个 skill 完整执行成功"。

因为 Skill 只是指导，真正落地还取决于：
- Tool 权限是否足够
- 文件路径是否可访问
- 当前 workspace 是否能看到对应资源
- Skill 是否被 agent 的技能过滤规则允许

## Skill 的目录结构

```
some-skill/
├── SKILL.md          # 入口：触发条件、流程步骤、依赖资源
├── references/       # 详细说明：API参考、工作流、错误处理
│   └── workflow.md
└── scripts/          # 复用脚本：格式转换、导入导出
    └── helper.py
```

## 相关概念
- [[skill三层发现机制]]

## Lobster 卡片
- [[main的私有skill不天然共享给其他agent]]
- [[skill三层放置策略]]
- [[Tool是能力Skill是方法]]
- [[skill目录结构设计规范]]

## 来源
- [[OpenClaw多Agent Skills分层调用机制]]