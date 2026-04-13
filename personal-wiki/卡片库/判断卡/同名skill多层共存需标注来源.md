---
type: 判断卡
confidence: high
tags:
- skill
- 多层发现
- 命名冲突
- 工程实践
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill三层发现机制
sources:
- OpenClaw多Agent Skills分层调用机制
related:
- skill三层放置策略
---
# 同名 Skill 多层共存需标注来源

## 判断内容

同名 skill 同时存在于多个层时，会产生两个现实问题：
1. 系统最终优先用哪一份？
2. 你修改的是不是当前真正生效的那一份？

**解决方案**：一旦系统化维护 skill，必须标注来源：
- 官方内置版
- 本机共享版
- 某个 agent 私有版
- 对官方 skill 的本地覆盖版

**适用条件**：当开始系统化维护 skill、有多层 skill 管理需求时。

## 相关卡片
- [[skill三层放置策略]]

## 相关 Wiki 概念
- [[skill三层发现机制]]
## 来源
- [https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ](https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ)