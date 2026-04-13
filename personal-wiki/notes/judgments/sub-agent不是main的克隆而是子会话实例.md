---
type: judgment
confidence: high
tags:
- sub-agent
- multi-agent
- agent继承
- OpenClaw
status: new
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill三层发现机制
- OpenClaw
sources:
- https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
- main的私有skill不天然共享给其他agent
---
# Sub-agent 不是 main 的克隆，而是子会话实例

## 判断内容

Sub-agent 不是 main agent 的完全克隆，而是在运行时按目标 agent 配置启动的子会话实例。

它继承的东西包括：
- 目标 agent 的身份与配置
- 目标 agent 的 workspace
- 目标 agent 的 tools policy
- 目标 agent 的 model / subagent 相关设置
- 当前系统能发现的 skills

**推论**：skill 是否可用，必须同时看三点：
1. Skill 是否在当前可发现范围里
2. 子代理有没有执行所需 tools 的权限
3. Skill 的资源文件在子代理边界内能不能读到

## 适用条件

- 适用于 sessions_spawn / 子代理拉起场景
- 适用于评估多 agent 协作中的能力继承问题

## 相关 Wiki 概念
- [[skill三层发现机制]]
- [[OpenClaw]]