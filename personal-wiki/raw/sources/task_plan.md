# Task Plan: 实现四个核心 AI 技能
<!--
  WHAT: 为 Obsidian 知识库实现四个核心 AI 技能
  WHY: 将理论框架转化为实际可用的自动化工具
  WHEN: 2026-03-30 创建
-->

## Goal
为 Obsidian 知识库实现四个核心 AI 技能（ob-search、ob-todo、ob-note、article-processor），创建可以自动化操作的 Claude Code 技能体系。

## Current Phase
Phase 7

## Phases

### Phase 1: 需求分析与架构设计
- [x] 理解用户需求 - 实现四个核心技能
- [x] 分析 obsidian.md 中的理论框架
- [x] 研究现有技能结构（pdf_to_jpg）
- [x] 设计技能架构和文件结构
- [x] 确定技术实现方案
- **Status:** complete

### Phase 2: 基础设施搭建
- [x] 创建技能目录结构
- [x] 设计笔记卡片模板（含 frontmatter）
- [x] 创建配置文件和工具函数
- [x] 建立索引和搜索机制
- **Status:** complete

### Phase 3: ob-search 技能实现
- [x] 实现全库文本搜索功能
- [x] 支持标签过滤
- [x] 支持卡片类型过滤
- [ ] 支持语义相似度搜索（需 AI 集成）
- **Status:** complete

### Phase 4: ob-todo 技能实现
- [x] 创建任务卡片模板
- [x] 实现任务添加功能
- [x] 实现任务列表查看
- [x] 实现任务状态更新
- **Status:** complete

### Phase 5: ob-note 技能实现
- [x] 创建笔记卡片模板
- [x] 实现快速笔记记录
- [x] 自动生成 frontmatter
- [x] 支持分类和标签
- **Status:** complete

### Phase 6: article-processor 技能实现
- [x] 实现基础架构
- [ ] 实现 URL 内容抓取（需集成 MCP）
- [ ] AI 拆卡功能（需集成 AI API）
- [x] 自动保存到知识库
- **Status:** complete（基础功能）

### Phase 7: 测试与验证
- [x] 测试所有四个技能
- [x] 验证工作流完整性
- [x] 文档编写
- **Status:** complete

## Key Questions
1. 技能应该以什么形式实现？Claude Code Skills 还是独立脚本？
2. 笔记卡片应该使用什么文件命名规范？
3. 如何实现知识的"进化机制"（状态自动更新）？
4. 是否需要数据库还是纯文件系统？
5. 如何处理中文搜索和标签？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 使用 Claude Code Skills | 用户已安装技能框架，可直接复用 |
| 纯 Markdown + Frontmatter | 符合 Obsidian 原生格式，便于维护 |
| 文件系统存储 | 无需额外数据库，简单可靠 |
| UTF-8 编码 | 支持中文内容 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| UnicodeEncodeError: Windows 终端 GBK 编码无法显示 Unicode 字符 | 1 | 在所有脚本开头添加 UTF-8 输出重定向代码 |

## Notes
- 所有技能以中文为主要语言
- 遵循 obsidian.md 中的笔记四层结构（判断卡 > 方法卡 > 案例卡 > 信息卡）
- 每张卡片需包含完整的 frontmatter 元数据
