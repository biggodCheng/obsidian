---
name: ob-note
description: 笔记管理技能 - 快速记录洞察和笔记卡片
user-invocable: true
---

# Lobster Note - 笔记管理

快速创建和管理 Obsidian 知识库中的笔记卡片。

## When to Use

当用户说：
- "这个洞察很重要，记个笔记"
- "记一下: xxx"
- "创建判断卡: xxx"
- "记录方法: xxx"
- "添加案例笔记"

## How It Works

使用 `lobster_utils.py` 核心工具模块：
- 快速创建各类型笔记卡片
- 自动生成 frontmatter
- 支持判断卡、方法卡、案例卡、信息卡
- 自动添加创建日期和状态

## Card Types

### 判断卡 (Judgment)
- 最核心的资产类型
- 记录"怎么判断"的决策
- 高商业护城河价值

### 方法卡 (Method)
- 记录具体做法和流程
- 可复用的操作步骤

### 案例卡 (Case)
- 记录真实发生的事件
- 验证过的事实依据

### 信息卡 (Information)
- 基础信息记录
- 最低价值类型

## Usage Examples

```
记一下判断卡: 降价10%可以增加30%销量
创建方法卡: A/B测试五步法
记录案例: 客户A的转化率提升过程
添加信息卡: 产品参数表
```

## Output

返回创建的笔记信息：
- 文件路径
- 卡片类型
- 标题
- 标签
