#!/usr/bin/env python3
"""
Lobster AI - 核心工具模块
用于 Obsidian 知识库的笔记管理
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple


class LobsterConfig:
    """配置管理"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            # 默认配置路径
            script_dir = Path(__file__).parent
            config_path = script_dir / "config.json"

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    @property
    def vault_path(self) -> str:
        return self.config['vault_path']

    @property
    def notes_dir(self) -> str:
        return self.config['notes_dir']

    @property
    def templates_dir(self) -> str:
        return self.config['templates_dir']

    @property
    def card_types(self) -> List[str]:
        return self.config['card_types']


class Frontmatter:
    """Frontmatter 处理"""

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        """解析 Markdown 文件的 frontmatter"""
        lines = content.split('\n')
        if not lines or lines[0] != '---':
            return {}

        fm_lines = []
        for i, line in enumerate(lines[1:], 1):
            if line == '---':
                break
            fm_lines.append(line)

        # 简单的 YAML 解析（只处理基本格式）
        frontmatter = {}
        for line in fm_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                # 处理列表
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip() for v in value[1:-1].split(',') if v.strip()]
                # 处理布尔值
                elif value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                frontmatter[key] = value

        return frontmatter

    @staticmethod
    def generate(metadata: Dict[str, Any]) -> str:
        """生成 frontmatter"""
        lines = ['---']
        for key, value in metadata.items():
            if isinstance(value, list):
                lines.append(f"{key}: [{', '.join(str(v) for v in value)}]")
            elif isinstance(value, bool):
                lines.append(f"{key}: {str(value).lower()}")
            else:
                lines.append(f"{key}: {value}")
        lines.append('---')
        return '\n'.join(lines)


class NoteCard:
    """笔记卡片"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.frontmatter = {}
        self.content = ""
        self._parse()

    def _parse(self):
        """解析笔记文件"""
        if not self.filepath.exists():
            return

        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        self.frontmatter = Frontmatter.parse(content)

        # 提取正文内容（frontmatter 之后的部分）
        lines = content.split('\n')
        if lines and lines[0] == '---':
            for i, line in enumerate(lines[1:], 1):
                if line == '---':
                    self.content = '\n'.join(lines[i+1:]).strip()
                    break
        else:
            self.content = content.strip()

    @property
    def title(self) -> str:
        """获取标题（从 frontmatter 或第一个标题）"""
        if 'title' in self.frontmatter:
            return self.frontmatter['title']

        # 从内容中提取第一个 # 标题
        for line in self.content.split('\n'):
            if line.startswith('# '):
                return line[2:].strip()

        return self.filepath.stem

    @property
    def card_type(self) -> str:
        """获取卡片类型"""
        return self.frontmatter.get('type', 'unknown')

    @property
    def tags(self) -> List[str]:
        """获取标签"""
        tags = self.frontmatter.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        return tags

    @property
    def status(self) -> str:
        """获取状态"""
        return self.frontmatter.get('status', '待办')

    @property
    def confidence(self) -> str:
        """获取信心程度"""
        return self.frontmatter.get('confidence', 'low')


class LobsterVault:
    """Obsidian 知识库操作"""

    def __init__(self, config: LobsterConfig = None):
        self.config = config or LobsterConfig()
        self.notes_dir = Path(self.config.notes_dir)

    def list_notes(self, filters: Dict[str, Any] = None) -> List[NoteCard]:
        """列出所有笔记"""
        notes = []

        # 扫描 notes 目录
        if self.notes_dir.exists():
            for md_file in self.notes_dir.rglob('*.md'):
                note = NoteCard(str(md_file))

                # 应用过滤器
                if filters:
                    if 'type' in filters and note.card_type != filters['type']:
                        continue
                    if 'status' in filters:
                        filter_status = filters['status']
                        if isinstance(filter_status, list):
                            if note.status not in filter_status:
                                continue
                        elif note.status != filter_status:
                            continue
                    if 'tags' in filters:
                        filter_tags = set(filters['tags'])
                        if not filter_tags.intersection(set(note.tags)):
                            continue

                notes.append(note)

        return notes

    def search(self, query: str, filters: Dict[str, Any] = None) -> List[NoteCard]:
        """搜索笔记"""
        results = []
        notes = self.list_notes(filters)

        query_lower = query.lower()

        for note in notes:
            # 搜索标题
            if query_lower in note.title.lower():
                results.append((note, 100))
                continue

            # 搜索标签
            for tag in note.tags:
                if query_lower in tag.lower():
                    results.append((note, 80))
                    break
            else:
                # 搜索内容
                if query_lower in note.content.lower():
                    results.append((note, 60))

        # 按相关度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [note for note, score in results]

    def create_note(self, card_type: str, title: str, content: str = "",
                    metadata: Dict[str, Any] = None) -> NoteCard:
        """创建新笔记"""
        # 生成文件名
        date_str = datetime.now().strftime('%Y-%m-%d')
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        filename = f"{slug}.md"

        # 根据卡片类型确定子目录
        card_subdirs = self.config.config.get('card_subdirs', {})
        subdir = card_subdirs.get(card_type, card_type)
        target_dir = self.notes_dir / subdir
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / filename

        # 准备元数据
        metadata = metadata or {}
        metadata.update({
            'type': card_type,
            'created': date_str,
            'updated': date_str,
            'title': title
        })

        # 生成文件内容
        frontmatter_str = Frontmatter.generate(metadata)
        full_content = f"{frontmatter_str}\n\n# {title}\n\n{content}"

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        return NoteCard(str(filepath))

    def update_note_status(self, note: NoteCard, new_status: str):
        """更新笔记状态"""
        note.frontmatter['status'] = new_status
        note.frontmatter['updated'] = datetime.now().strftime('%Y-%m-%d')
        # TODO: 实现文件更新逻辑


def slugify(text: str) -> str:
    """将文本转换为 URL 友好的 slug"""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


class UnifiedIngestionWorkflow:
    """统一的摄取工作流 - 融合 Wiki 和 Lobster"""

    def __init__(self, lobster_config: LobsterConfig = None, wiki_dir: str = None):
        self.lobster_config = lobster_config or LobsterConfig()
        self.lobster = LobsterVault(self.lobster_config)
        self.wiki_dir = Path(wiki_dir) if wiki_dir else Path(self.lobster_config.config.get('wiki_dir', 'personal-wiki/wiki'))
        self.notes_dir = Path(self.lobster_config.notes_dir)

    def extract_content(self, source_file: str) -> Dict[str, Any]:
        """从源文件提取内容"""
        # TODO: 实现内容提取逻辑
        return {"title": "", "content": "", "metadata": {}}

    def create_summary(self, content: Dict[str, Any]) -> str:
        """创建 Wiki 摘要页面"""
        # TODO: 实现 Wiki 摘要创建逻辑
        summary_path = self.wiki_dir / "summaries" / f"{slugify(content['title'])}.md"
        return str(summary_path)

    def extract_cards(self, content: Dict[str, Any], summary_path: str) -> List[NoteCard]:
        """从内容中提取 Lobster 卡片"""
        cards = []

        # TODO: 实现智能卡片提取逻辑
        # 1. 识别判断（优先级最高）
        # 2. 识别方法
        # 3. 识别案例

        return cards

    def link_cards_and_concepts(self, cards: List[NoteCard], summary_path: str):
        """建立卡片和 Wiki 概念的双向链接"""
        linker = BidirectionalLinker(self.wiki_dir, self.notes_dir)

        for card in cards:
            # 识别卡片中的关键概念
            concepts = linker.identify_concepts_in_card(card)

            # 给卡片添加 Wiki 概念引用
            if concepts:
                linker.add_wiki_concepts_to_card(card.filepath, concepts)

        # 给 Wiki 页面添加卡片引用
        linker.add_lobster_cards_to_wiki(summary_path, cards)

    def update_index(self, summary_path: str, cards: List[NoteCard]):
        """更新 Wiki 索引"""
        # TODO: 实现索引更新逻辑
        index_path = self.wiki_dir / "index.md"

    def ingest_article(self, source_file: str) -> Tuple[str, List[NoteCard]]:
        """完整的摄取流程"""
        # 1. 提取内容
        content = self.extract_content(source_file)

        # 2. 创建 Wiki 摘要
        summary_page = self.create_summary(content)

        # 3. 提取 Lobster 卡片
        cards = self.extract_cards(content, summary_page)

        # 4. 建立双向链接
        self.link_cards_and_concepts(cards, summary_page)

        # 5. 更新索引
        self.update_index(summary_page, cards)

        return summary_page, cards


class BidirectionalLinker:
    """双向链接维护器 - Wiki 和 Lobster 卡片之间的链接"""

    def __init__(self, wiki_dir: Path, notes_dir: Path):
        self.wiki_dir = wiki_dir
        self.notes_dir = notes_dir
        self.concepts_dir = wiki_dir / "concepts"
        self.entities_dir = wiki_dir / "entities"

    def identify_concepts_in_card(self, card: NoteCard) -> List[str]:
        """识别卡片中的关键概念"""
        concepts = []

        # 扫描卡片内容，查找可能的概念引用
        # TODO: 实现智能概念识别逻辑

        return concepts

    def find_matching_concept_pages(self, keywords: List[str]) -> List[Path]:
        """在 wiki/concepts/ 中查找匹配的页面"""
        matching_pages = []

        if not self.concepts_dir.exists():
            return matching_pages

        for concept_file in self.concepts_dir.glob("*.md"):
            # TODO: 实现关键词匹配逻辑
            pass

        return matching_pages

    def add_wiki_concepts_to_card(self, card_path: Path, concepts: List[str]):
        """给卡片添加 Wiki 概念引用"""
        if not concepts:
            return

        card = NoteCard(str(card_path))

        # 更新 frontmatter
        if 'wiki_concepts' not in card.frontmatter:
            card.frontmatter['wiki_concepts'] = []

        for concept in concepts:
            concept_link = f"[[{concept}]]"
            if concept_link not in card.frontmatter['wiki_concepts']:
                card.frontmatter['wiki_concepts'].append(concept_link)

        # TODO: 写回文件

    def add_lobster_cards_to_wiki(self, wiki_page: str, cards: List[NoteCard]):
        """给 Wiki 页面添加卡片引用"""
        if not cards:
            return

        wiki_path = Path(wiki_page)

        # 读取 Wiki 页面
        # TODO: 实现读取和更新逻辑

    def scan_and_update_references(self):
        """扫描所有文件，更新相互引用"""
        # 1. 扫描所有 Lobster 卡片
        all_cards = []
        for card_type in ["judgments", "methods", "cases", "information"]:
            type_dir = self.notes_dir / card_type
            if type_dir.exists():
                all_cards.extend(type_dir.glob("*.md"))

        # 2. 对于每张卡片，识别相关概念
        for card_path in all_cards:
            card = NoteCard(str(card_path))
            concepts = self.identify_concepts_in_card(card)

            if concepts:
                self.add_wiki_concepts_to_card(card_path, concepts)

        # 3. 扫描所有 Wiki 页面，更新卡片引用
        # TODO: 实现 Wiki 页面扫描和更新逻辑


if __name__ == '__main__':
    # 测试代码
    config = LobsterConfig()
    vault = LobsterVault(config)

    # 列出所有笔记
    notes = vault.list_notes()
    print(f"Found {len(notes)} notes")

    # 搜索测试
    if notes:
        results = vault.search("测试")
        print(f"Search results: {len(results)}")

    # 测试统一摄取工作流
    try:
        workflow = UnifiedIngestionWorkflow()
        print(f"Unified workflow initialized")
        print(f"Wiki dir: {workflow.wiki_dir}")
        print(f"Notes dir: {workflow.notes_dir}")
    except Exception as e:
        print(f"Error initializing workflow: {e}")
