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
from typing import List, Dict, Optional, Any


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
        return self.frontmatter.get('status', 'new')

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
                    if 'status' in filters and note.status != filters['status']:
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
        filename = f"{date_str}-{card_type}-{slug}.md"
        filepath = self.notes_dir / filename

        # 确保 notes 目录存在
        self.notes_dir.mkdir(parents=True, exist_ok=True)

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
