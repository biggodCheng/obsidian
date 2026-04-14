---
name: ob-search
description: 在 Obsidian 知识库中搜索笔记卡片，支持关键词、标签、类型过滤。当用户说"找一下"、"搜索"、"列出"、"查找"、"关于xxx的笔记"时触发。
user-invocable: true
---

# Lobster Search - 知识库搜索

在 Obsidian 知识库中搜索笔记卡片和 Wiki 页面。

## 执行入口

```
python .claude/skills/ob-search/search.py [关键词] [--type 类型] [--tags "标签1,标签2"] [--confidence low|medium|high] [--scope 卡片库|wiki|all] [--concepts "概念1,概念2"] [--list] [--show-content] [--json]
```

依赖：`.lobster/lobster_utils.py` + `.lobster/config.json`

## 工作流

### Step 1: 解析用户意图

从用户输入中提取搜索参数：

| 用户说法 | 映射到 CLI 参数 |
|---------|----------------|
| "找一下关于用户体验的判断卡" | `search.py 用户体验 --type 判断卡` |
| "搜索带#产品标签的方法卡" | `search.py "" --tags 产品 --type 方法卡` |
| "列出所有笔记" | `search.py --list` |
| "查找关于冷启动的wiki" | `search.py 冷启动 --scope wiki` |
| "找到关于用户转化的笔记" | `search.py 用户转化` |

**意图解析规则**：
- 提到具体卡片类型（"判断卡"/"方法卡"/"案例卡"/"信息卡"/"日常工作"）→ `--type <类型>`
- 提到标签（"带#产品标签" / "标签含产品"）→ `--tags 产品`（去掉#号）
- 提到"wiki"/"知识库" → `--scope wiki` 或 `--scope all`
- 提到"概念"/"关联" → `--concepts <概念名>`
- 无关键词只想浏览 → `--list`
- 想看内容详情 → 加 `--show-content`

### Step 2: 构造并执行搜索

```bash
# 关键词搜索
python .claude/skills/ob-search/search.py "用户体验" --type 判断卡 --show-content

# 标签+类型过滤（无关键词时传空字符串）
python .claude/skills/ob-search/search.py "" --tags 产品 --type 方法卡

# 列出所有笔记
python .claude/skills/ob-search/search.py --list

# Wiki 概念关联搜索
python .claude/skills/ob-search/search.py --concepts "冷启动策略,增长飞轮"

# 全范围搜索
python .claude/skills/ob-search/search.py "用户增长" --scope all --show-content
```

### Step 3: 格式化返回结果

将 CLI 输出整理为用户友好的格式：
- 文件名和路径
- 卡片类型
- 标题
- 标签
- 匹配内容摘要（如使用了 --show-content）

### Step 4: 结果为空时的处理

如果搜索结果为空：
1. 告知用户未找到匹配结果
2. 建议扩大搜索范围（去掉类型过滤、使用更宽泛的关键词、尝试 `--scope all`）

## CLI 参数速查

| 参数 | 缩写 | 说明 | 示例 |
|------|------|------|------|
| `query` | - | 搜索关键词（位置参数，可选） | `search.py 用户体验` |
| `--type` | `-t` | 按类型过滤 | `--type 判断卡` |
| `--tags` | - | 按标签过滤（逗号分隔，去#号） | `--tags 产品,设计` |
| `--confidence` | `-c` | 按信心程度过滤 | `--confidence high` |
| `--scope` | - | 搜索范围：卡片库/wiki/all | `--scope all` |
| `--concepts` | - | 按Wiki概念搜索关联卡片 | `--concepts 冷启动` |
| `--list` | `-l` | 列出所有笔记（不搜索） | `--list` |
| `--show-content` | - | 显示匹配上下文预览 | `--show-content` |
| `--json` | `-j` | JSON 格式输出 | `--json` |

## 边界条件

- **搜索结果过多（>20条）** → 展示前 20 条，询问是否继续或缩小范围
- **零结果** → 建议扩大范围或换关键词
- **config.json 不存在** → 检查 `.lobster/config.json` 是否存在
- **vault 初始化失败** → 报错并提示检查 lobster_utils.py
- **标签含#号** → 自动去除（`#产品` → `产品`）

## 使用示例

```
找一下关于用户体验的判断卡
→ python .claude/skills/ob-search/search.py "用户体验" --type 判断卡 --show-content

搜索所有带#产品标签的方法卡
→ python .claude/skills/ob-search/search.py "" --tags "产品" --type 方法卡

列出所有笔记
→ python .claude/skills/ob-search/search.py --list

查看待办事项
→ python .claude/skills/ob-search/search.py "" --type 日常工作

搜索wiki中的冷启动相关概念
→ python .claude/skills/ob-search/search.py "冷启动" --scope wiki --show-content
```
