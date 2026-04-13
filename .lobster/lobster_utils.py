#!/usr/bin/env python3
"""
Lobster AI - 核心工具模块
用于 Obsidian 知识库的笔记管理
"""

import os
import json
import re
import yaml
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
        """解析 Markdown 文件的 frontmatter（使用 yaml.safe_load）"""
        lines = content.split('\n')
        if not lines or lines[0] != '---':
            return {}

        fm_lines = []
        end_idx = -1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                end_idx = i
                break
            fm_lines.append(line)

        if not fm_lines:
            return {}

        fm_text = '\n'.join(fm_lines)
        try:
            return yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            return {}

    @staticmethod
    def generate(metadata: Dict[str, Any]) -> str:
        """生成 frontmatter（使用标准 YAML 格式）"""
        fm_text = yaml.dump(metadata, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return f"---\n{fm_text}---"


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

        # 提取正文内容（第二个 --- 之后的部分）
        lines = content.split('\n')
        if lines and lines[0].strip() == '---':
            fm_end = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    fm_end = i
                    break
            if fm_end >= 0:
                self.content = '\n'.join(lines[fm_end + 1:]).strip()
            else:
                self.content = content.strip()
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
                    if 'confidence' in filters and note.confidence != filters['confidence']:
                        continue
                    if 'tags' in filters:
                        filter_tags = set(filters['tags'])
                        if not filter_tags.intersection(set(note.tags)):
                            continue

                notes.append(note)

        return notes

    def search(self, query: str, filters: Dict[str, Any] = None,
               scope: str = "notes", concepts: List[str] = None) -> List[NoteCard]:
        """
        搜索笔记和 Wiki 页面。

        Args:
            query: 搜索关键词
            filters: 元数据过滤（type, status, tags）
            scope: 搜索范围 - "notes"（默认）/ "wiki" / "all"
            concepts: 按 wiki 概念名过滤，返回引用了这些概念的卡片
        """
        results = []

        # 模式 A：按概念搜索
        if concepts:
            return self._search_by_concepts(concepts, filters)

        # 模式 B：关键词搜索
        query_lower = query.lower() if query else ""

        # 搜索 notes 层
        if scope in ("notes", "all"):
            notes = self.list_notes(filters)
            for note in notes:
                if not query_lower:
                    results.append((note, 50))
                    continue

                # 标题匹配
                if query_lower in note.title.lower():
                    results.append((note, 100))
                # wiki_concepts 匹配
                elif query_lower in str(note.frontmatter.get('wiki_concepts', [])).lower():
                    results.append((note, 85))
                # 标签匹配
                elif any(query_lower in tag.lower() for tag in note.tags):
                    results.append((note, 80))
                # 内容匹配
                elif query_lower in note.content.lower():
                    results.append((note, 60))

        # 搜索 wiki 层
        if scope in ("wiki", "all"):
            wiki_dir = Path(self.config.config.get('wiki_dir', 'personal-wiki/wiki'))
            if wiki_dir.exists():
                for md_file in wiki_dir.rglob('*.md'):
                    wiki_note = NoteCard(str(md_file))

                    if not query_lower:
                        results.append((wiki_note, 40))
                        continue

                    # 标题匹配
                    if query_lower in wiki_note.title.lower():
                        results.append((wiki_note, 90))
                    # lobster_cards 匹配
                    elif query_lower in str(wiki_note.frontmatter.get('lobster_cards', [])).lower():
                        results.append((wiki_note, 75))
                    # 标签匹配
                    elif any(query_lower in tag.lower() for tag in wiki_note.tags):
                        results.append((wiki_note, 70))
                    # 内容匹配
                    elif query_lower in wiki_note.content.lower():
                        results.append((wiki_note, 50))

        # 按相关度排序，去重
        results.sort(key=lambda x: x[1], reverse=True)
        seen = set()
        unique_results = []
        for note, score in results:
            if note.filepath not in seen:
                seen.add(note.filepath)
                unique_results.append(note)
        return unique_results

    def _search_by_concepts(self, concepts: List[str], filters: Dict[str, Any] = None) -> List[NoteCard]:
        """按 wiki 概念名搜索关联卡片"""
        results = []
        notes = self.list_notes(filters)

        concept_set = set(c.lower() for c in concepts)
        for note in notes:
            wiki_c = note.frontmatter.get('wiki_concepts', [])
            if isinstance(wiki_c, str):
                wiki_c = [wiki_c]
            if concept_set.intersection(set(str(c).lower() for c in wiki_c)):
                results.append(note)

        return results

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
        self._concept_names: Optional[List[str]] = None

    def _get_concept_names(self) -> List[str]:
        """获取所有 wiki 概念名（文件名去后缀）"""
        if self._concept_names is not None:
            return self._concept_names

        names = []
        if self.concepts_dir.exists():
            for f in self.concepts_dir.glob("*.md"):
                names.append(f.stem)
        # 也包含实体
        if self.entities_dir.exists():
            for f in self.entities_dir.glob("*.md"):
                names.append(f.stem)

        self._concept_names = names
        return names

    def identify_concepts_in_card(self, card: NoteCard) -> List[str]:
        """识别卡片中的关键概念（基于文件名匹配 + 内容匹配）"""
        concepts = []
        concept_names = self._get_concept_names()

        # 搜索范围：标题 + 标签 + 内容
        search_text = f"{card.title} {' '.join(card.tags)} {card.content}".lower()

        for name in concept_names:
            if name.lower() in search_text:
                concepts.append(name)

        return concepts

    def find_matching_concept_pages(self, keywords: List[str]) -> List[Path]:
        """在 wiki/concepts/ 中查找匹配的页面"""
        matching_pages = []

        if not self.concepts_dir.exists():
            return matching_pages

        for concept_file in self.concepts_dir.glob("*.md"):
            name = concept_file.stem.lower()
            # 匹配文件名
            for kw in keywords:
                if kw.lower() in name:
                    matching_pages.append(concept_file)
                    break
            else:
                # 匹配内容
                try:
                    content = concept_file.read_text(encoding='utf-8')
                    for kw in keywords:
                        if kw.lower() in content.lower():
                            matching_pages.append(concept_file)
                            break
                except Exception:
                    pass

        return matching_pages

    def add_wiki_concepts_to_card(self, card_path: Path, concepts: List[str]):
        """给卡片添加 Wiki 概念引用（纯字符串，不用 [[ ]]）"""
        if not concepts:
            return

        card = NoteCard(str(card_path))

        existing = card.frontmatter.get('wiki_concepts', [])
        if isinstance(existing, str):
            existing = [existing]

        new_concepts = list(existing)
        for concept in concepts:
            if concept not in new_concepts:
                new_concepts.append(concept)

        card.frontmatter['wiki_concepts'] = new_concepts
        self._write_frontmatter(card_path, card.frontmatter, card.content)

    def add_lobster_cards_to_wiki(self, wiki_page: str, cards: List[NoteCard]):
        """给 Wiki 页面添加卡片引用"""
        if not cards:
            return

        wiki_path = Path(wiki_page)
        if not wiki_path.exists():
            return

        card = NoteCard(str(wiki_path))

        existing = card.frontmatter.get('lobster_cards', [])
        if isinstance(existing, str):
            existing = [existing]

        new_cards = list(existing)
        for c in cards:
            card_name = c.filepath.stem
            if card_name not in new_cards:
                new_cards.append(card_name)

        card.frontmatter['lobster_cards'] = new_cards
        self._write_frontmatter(wiki_path, card.frontmatter, card.content)

    def scan_and_update_references(self, dry_run: bool = False) -> Dict[str, Any]:
        """扫描所有文件，更新相互引用（双向）"""
        stats = {'cards_scanned': 0, 'concepts_added': 0, 'backlinks_added': 0}

        # 1. 构建概念 → 卡片 反向索引
        concept_to_cards: Dict[str, List[str]] = {}
        all_cards = []
        for card_type in ["judgments", "方法卡", "案例卡", "information", "任务卡"]:
            type_dir = self.notes_dir / card_type
            if type_dir.exists():
                all_cards.extend(type_dir.glob("*.md"))

        # 2. 扫描每张卡片，识别并更新概念引用
        for card_path in all_cards:
            card = NoteCard(str(card_path))
            stats['cards_scanned'] += 1

            concepts = self.identify_concepts_in_card(card)

            if concepts:
                if not dry_run:
                    self.add_wiki_concepts_to_card(card_path, concepts)
                stats['concepts_added'] += len(concepts)

                # 记录反向映射
                card_name = card_path.stem
                for concept in concepts:
                    if concept not in concept_to_cards:
                        concept_to_cards[concept] = []
                    if card_name not in concept_to_cards[concept]:
                        concept_to_cards[concept].append(card_name)

        # 3. 更新 Wiki 概念页的反向引用
        for concept_name, card_names in concept_to_cards.items():
            concept_path = self.concepts_dir / f"{concept_name}.md"
            if not concept_path.exists():
                continue

            wiki_page = NoteCard(str(concept_path))
            existing = wiki_page.frontmatter.get('lobster_cards', [])
            if isinstance(existing, str):
                existing = [existing]

            new_cards = list(existing)
            added = 0
            for card_name in card_names:
                if card_name not in new_cards:
                    new_cards.append(card_name)
                    added += 1

            if added > 0:
                if not dry_run:
                    wiki_page.frontmatter['lobster_cards'] = new_cards
                    self._write_frontmatter(concept_path, wiki_page.frontmatter, wiki_page.content)
                stats['backlinks_added'] += added

        return stats

    @staticmethod
    def _write_frontmatter(file_path: Path, frontmatter: Dict[str, Any], content: str):
        """写回文件：frontmatter + 原始内容"""
        fm_text = Frontmatter.generate(frontmatter)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{fm_text}\n{content}")


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
