---
name: ob-search
description: 在 Obsidian 知识库中搜索笔记卡片，支持关键词、标签、类型过滤
user-invocable: true
---

# Lobster Search - 知识库搜索

在 Obsidian 知识库中搜索笔记卡片。

## When to Use

当用户说：
- "找一下 xxx" / "xxx 在哪"
- "搜索关于 xxx 的判断卡"
- "查找带 xxx 标签的笔记"
- "列出所有方法卡"
- "找到关于用户转化的笔记"

## How It Works

使用 `lobster_utils.py` 核心工具模块：
- 扫描 卡片库 目录下的所有 .md 文件
- 解析 frontmatter 元数据
- 支持关键词搜索（标题、内容、标签）
- 支持按类型过滤（判断卡/方法卡/案例卡/信息卡/日常工作）
- 支持按状态过滤（new/growing/mature/outdated/discarded）
- 支持按标签过滤
- 按相关度排序返回结果

## Configuration

技能会读取知识库配置文件 `.lobster/config.json`：

```json
{
  "vault_path": "d:\\DATA\\cgq-obsidian",
  "notes_dir": "d:\\DATA\\cgq-obsidian\\卡片库",
  "templates_dir": "d:\\DATA\\cgq-obsidian\\templates"
}
```

## Usage Examples

```
找一下关于用户体验的判断卡
搜索带#产品标签的笔记
列出所有方法卡
```

## Output

返回匹配的笔记列表，包含：
- 文件名
- 卡片类型
- 标题
- 标签
- 状态
- 相关度分数
