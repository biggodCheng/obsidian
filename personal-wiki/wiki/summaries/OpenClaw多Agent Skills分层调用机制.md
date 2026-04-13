---
title: OpenClaw多Agent模式下Skills的分层调用机制
type: summary
date: 2026-04-12
tags:
  - OpenClaw
  - multi-agent
  - skills
  - tool
  - agent架构
sources:
  - https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
  - skill与tool的分层
  - skill三层发现机制
  - OpenClaw
  - DracoVibeCoding
lobster_cards:
  - Tool是能力Skill是方法
  - sub-agent不是main的克隆而是子会话实例
  - main的私有skill不天然共享给其他agent
  - 同名skill多层共存需标注来源
  - skill三层放置策略
  - skill目录结构设计规范
  - 130个AI员工的skill管理实战
---

# OpenClaw多Agent模式下Skills的分层调用机制

## 摘要

文章系统讲解了 OpenClaw 平台中 skills 机制的完整架构。核心要点：

1. **Skill 与 Tool 的本质区别**：Tool 是能力层（能不能做），Skill 是方法层（怎么做）
2. **Skill 的三层发现机制**：全局安装层、机器级共享层、Agent workspace 私有层
3. **Multi-agent skill 共享**：main agent 的私有 skill 不天然被 sub-agent 共享，跨 agent 共享需放在共享层
4. **Sub-agent 继承模型**：sub-agent 不是 main 的克隆，而是按目标 agent 配置启动的子会话实例
5. **同名 skill 冲突**：多层同名 skill 需标注来源，确认生效优先级

## 文章结构

- 一、Skill 与 Tool 的区别
- 二、Skill 目录结构（SKILL.md + references/ + scripts/）
- 三、Skill 来源三层（全局安装层、共享层、workspace层）
- 四、Main agent 与 agency-agents 的 skill 关系
- 五、Sub-agent 能否用 main 的 skill（三种情况分析）
- 六、实测经验：不要只靠猜目录
- 七、共享 vs 各自一套 skill
- 八、Skill 共享在 multi-agent 中的重要性
- 九、实务设计建议（三类 skill 放置策略）
- 十、Sub-agent 继承模型
- 十一、同名 skill 冲突处理
- 十二、Multi-agent 场景的五条原则
- 十三、总结

## 核心观点

> Skill 不是"一个统一目录里的插件列表"，而是一套分层发现、按 workspace 和共享范围组织起来的工作流系统。

## 关键概念
- [[skill与tool的分层]]
- [[skill三层发现机制]]

## 关键实体
- [[OpenClaw]]
- [[DracoVibeCoding]]

## Lobster 卡片
- [[Tool是能力Skill是方法]]
- [[sub-agent不是main的克隆而是子会话实例]]
- [[main的私有skill不天然共享给其他agent]]
- [[同名skill多层共存需标注来源]]
- [[skill三层放置策略]]
- [[skill目录结构设计规范]]
- [[130个AI员工的skill管理实战]]

## 来源
- 公众号：Draco正在VibeCoding
- 作者：[[DracoVibeCoding]]
- URL：https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
