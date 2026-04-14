---
type: 判断卡
confidence: high
tags:
  - Go
  - 部署
  - 静态二进制
created: 2026-04-14
updated: 2026-04-14
wiki_concepts:
  - 最穷技术栈与独立开发
sources:
  - 最穷技术栈与独立开发
related:
  - SQLite比Postgres快10倍
  - 企业云思维是成本陷阱
---

# Go静态二进制是部署革命

## 判断内容

**Go编译出来就是一个几MB的单文件二进制。没有pip install，没有虚拟环境，没有"我本地跑得好好的"。**

Python / Ruby / Node 在1GB机器上最大的问题不是慢，是光启动就吃掉一半内存。

**判断标准**：
- 如果你需要复杂部署环境 → 不是最优解
- 如果你想一键部署 → Go静态二进制是革命
- 如果你的机器资源有限 → Go是最佳选择

**部署对比**：

**Python/Ruby/Node**：
- 需要pip install、虚拟环境
- 基线内存占用高（如gunicorn 4 workers吃掉500MB）
- 容易出现"我本地跑得好好的"

**Go静态二进制**：
- 几MB单文件
- 无依赖
- 部署就是：`scp binary server:/usr/local/bin/ && systemctl restart app`

**性能表现**：
- 一台$5 VPS能撑每秒几万请求
- 内存占用极低
- 启动速度极快

**适用场景**：
- 资源受限的环境（如1GB内存的VPS）
- 需要简单部署的产品
- 追求极致性能

**不适用场景**：
- 需要动态语言的灵活性（如热更新）
- 团队已经有大量Python/Ruby代码库
- 特定语言生态的必需库

**核心原则**：
部署就是复制一个文件。这不只是方便，这是革命。

## 相关 Wiki 概念
- [[Go]]
- [[部署]]

## 来源
- [[最穷技术栈与独立开发]]

## 相关卡片
- [[SQLite比Postgres快10倍]]
- [[企业云思维是成本陷阱]]
