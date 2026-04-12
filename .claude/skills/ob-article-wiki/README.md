# Lobster-Article-Wiki 融合技能

**一次摄取，双重收益：Wiki 知识网络 + Lobster 价值卡片**

## 快速开始

### 基本用法

```
帮我摄取这个文章：[文章路径/URL]
```

### 明确指定融合模式

```
用 lobster-article-wiki 处理这篇文章
```

## 功能特性

### 双重输出

**Wiki 网络层** (`wiki/`):
- `summaries/` - 文章摘要
- `entities/` - 人名、组织、产品
- `concepts/` - 理论、方法、术语
- `synthesis/` - 综合分析

**Lobster 卡片层** (`notes/`):
- `judgments/` - 判断卡（价值最高）
- `methods/` - 方法卡（可复用流程）
- `cases/` - 案例卡（验证事实）
- `information/` - 信息卡（基础数据）

### 自动化特性

- ✅ 双向交叉引用
- ✅ 智能概念识别
- ✅ 自动链接发现
- ✅ 增量更新机制
- ✅ 索引和日志维护

## 目录结构

```
personal-wiki/
├── raw/sources/           # 源文件（只读）
├── wiki/                  # Wiki 输出
│   ├── index.md
│   ├── log.md
│   ├── entities/
│   ├── concepts/
│   ├── summaries/
│   └── synthesis/
└── notes/                # 卡片输出
    ├── judgments/
    ├── methods/
    ├── cases/
    └── information/
```

## 配置

### 检查配置文件

1. **`.lobster/config.json`** - Lobster 配置
2. **`personal-wiki/CLAUDE.md`** - Wiki 配置

### 必需目录

```bash
# 创建目录
mkdir -p personal-wiki/wiki/{entities,concepts,summaries,synthesis}
mkdir -p personal-wiki/notes/{judgments,methods,cases,information}
```

## 使用示例

### 示例 1：摄取微信文章

```
帮我摄取这篇微信文章：https://mp.weixin.qq.com/s/xxx
```

**输出**:
- Wiki 摘要页面
- 作者实体页面
- 核心概念页面
- 1-3 个判断卡
- 双向链接建立

### 示例 2：处理本地文件

```
处理 personal-wiki/raw/sources/obsidian-theory.md
```

### 示例 3：批量处理

```
处理 personal-wiki/raw/sources/ 目录下的所有 md 文件
```

## 价值导向

### 卡片优先级

| 类型 | 价值 | 优先级 |
|------|------|--------|
| 判断卡 | ⭐⭐⭐⭐⭐ | 最高 |
| 方法卡 | ⭐⭐⭐⭐ | 高 |
| 案例卡 | ⭐⭐⭐ | 中 |
| 信息卡 | ⭐ | 低（谨慎） |

### 创建判断卡的标准

- ✅ 回答"怎么判断"的问题
- ✅ 有明确的适用/不适用条件
- ✅ 可以被验证和应用
- ❌ 纯信息记录（用信息卡或搜索）

## 最佳实践

### 摄取建议

1. **一次一篇** - 保持参与，验证质量
2. **验证输出** - 检查 Wiki 和卡片质量
3. **指导重点** - 告诉 AI 什么最重要
4. **定期回顾** - 检查判断卡的验证状态

### 闭环维护

**验证记录**:
- 每次应用判断卡时记录结果
- 更新 `verification_count`
- 根据反馈调整 `confidence`

**状态流转**:
- `new` → `growing`: 被应用1次
- `growing` → `mature`: 被应用3次以上且反馈良好
- `mature` → `outdated`: 条件变化不再适用

## 故障排除

### 问题：没有创建卡片

**原因**: 文章可能缺乏可提炼的判断

**解决**:
- 明确告诉 AI 要提炼判断卡
- 检查文章是否有决策性内容

### 问题：链接没有建立

**原因**: 概念页面不存在或名称不匹配

**解决**:
- 先创建相关概念页面
- 使用精确的概念名称

### 问题：目录不存在

**解决**:
```bash
# 创建所需目录
mkdir -p personal-wiki/wiki/{entities,concepts,summaries,synthesis}
mkdir -p personal-wiki/notes/{judgments,methods,cases,information}
```

## 高级用法

### 只创建 Wiki

```
只创建 Wiki 摘要，不提取卡片
```

### 只拆卡

```
只提取判断卡，不创建 Wiki 页面
```

### 指定提取重点

```
重点提取这篇文章的判断卡
```

## 相关技能

- **lobster-article** - 单独的文章拆卡
- **llm-wiki** - 单独的 Wiki 构建
- **lobster-note** - 快速记录洞察
- **lobster-search** - 搜索知识库

## 技术实现

### Python 类

- `UnifiedIngestionWorkflow` - 统一摄取工作流
- `BidirectionalLinker` - 双向链接维护器

### 配置文件

- `.lobster/config.json` - Lobster 配置
- `personal-wiki/CLAUDE.md` - Wiki 配置

## 版本

- **版本**: 1.0.0
- **作者**: 基于 lobster-article 和 llm-wiki 融合
- **日期**: 2026-04-12

---

> 融合模式的价值：Wiki 提供知识网络，Lobster 提供价值排序，双向链接形成完整的知识图谱。
