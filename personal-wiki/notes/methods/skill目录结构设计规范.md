---
type: method
confidence: medium
tags:
- skill
- 目录结构
- 工程规范
- OpenClaw
status: new
created: 2026-04-12
updated: 2026-04-12
wiki_concepts:
- skill与tool的分层
- OpenClaw
sources:
- https://mp.weixin.qq.com/s/rFecRxZ1ci2aQd9QSunUFQ
related:
- Tool是能力Skill是方法
- skill三层放置策略
---
# Skill 目录结构设计规范

## 方法描述

一个标准 skill 的目录结构：

```
some-skill/
├── SKILL.md          # 核心入口文件（必需）
├── references/       # 详细参考文档
│   └── workflow.md
└── scripts/          # 复用脚本
    └── helper.py
```

### SKILL.md 职责
- 说明 skill 什么时候触发
- 定义先做什么、再做什么的流程
- 列出需要读取的参考文件
- 指定需要调用的脚本或工具

### references/ 职责
- API 参考
- 工作流说明
- 复杂规则
- 错误处理手册

### scripts/ 职责
- 格式转换脚本
- 导入导出脚本
- 自动化辅助工具

## 关键原则

Skill 不是"只有一个 markdown 文件"，而是一组围绕某种任务组织起来的资源。

## 相关 Wiki 概念
- [[skill与tool的分层]]