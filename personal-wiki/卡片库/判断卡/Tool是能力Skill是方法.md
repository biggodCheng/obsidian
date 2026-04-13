---
type: 判断卡
confidence: high
tags:
- skill
- tool
- agent架构
- 分层设计
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill与tool的分层
- skill三层发现机制
- OpenClaw
sources:
- OpenClaw多Agent Skills分层调用机制
related:
- skill目录结构设计规范
---
# Tool 是能力，Skill 是方法

## 判断内容

在多 Agent 系统中，Tool 和 Skill 处于不同层次：

- **Tool = 能力层**：决定 agent "能不能做"（能不能读文件、能不能写文件、能不能起子代理）
- **Skill = 方法层**：决定 agent "怎么做"（按什么步骤做、什么时候用这套流程最合适）

**关键推论**：agent 看得见某个 skill，不等于它能完整执行成功。执行成功还依赖 tool 权限、文件路径可访问性、workspace 可见范围、技能过滤规则。

## 适用条件

- 适用于所有多 Agent 框架（不仅限于 OpenClaw）
- 适用于 skill 设计和 tool 权限配置的架构决策

## 不适用场景

- 单一工具调用的简单场景（无 skill 概念时无意义）

## 相关卡片
- [[skill目录结构设计规范]]

## 相关 Wiki 概念
- [[skill与tool的分层]]
- [[skill三层发现机制]]
## 来源
- [https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ](https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ)