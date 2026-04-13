#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lobster Lint - 知识库引用健康检查
检查断链、孤儿卡片、引用一致性
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 自动定位 vault 根目录
def find_vault_path():
    current = Path(__file__).resolve().parent
    for _ in range(5):
        config_path = current / ".lobster" / "config.json"
        if config_path.exists():
            return current
        current = current.parent
    return Path(os.environ.get("LOBSTER_VAULT", "."))

import os
vault_path = find_vault_path()
utils_path = vault_path / ".lobster" / "lobster_utils.py"

if utils_path.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("lobster_utils", utils_path)
    lobster_utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lobster_utils)
else:
    print(f"错误: 找不到 lobster_utils.py", file=sys.stderr)
    sys.exit(1)


class LintChecker:
    """知识库健康检查器"""

    def __init__(self, wiki_dir: Path, notes_dir: Path):
        self.wiki_dir = wiki_dir
        self.notes_dir = notes_dir
        self.concepts_dir = wiki_dir / "概念卡"
        self.entities_dir = wiki_dir / "实体卡"
        self.issues: List[Dict] = []

    def check_all(self) -> List[Dict]:
        """执行所有检查"""
        self.issues = []
        self._check_card_broken_wiki_links()
        self._check_wiki_broken_card_links()
        self._check_orphan_cards()
        self._check_missing_frontmatter()
        self._check_status_consistency()
        return self.issues

    def _check_card_broken_wiki_links(self):
        """检查卡片的 wiki_concepts 是否有对应的 wiki 页面"""
        valid_wiki_names: Set[str] = set()
        for d in [self.concepts_dir, self.entities_dir]:
            if d.exists():
                for f in d.glob("*.md"):
                    valid_wiki_names.add(f.stem)

        for card_type in ["判断卡", "方法卡", "案例卡", "信息卡", "日常工作"]:
            type_dir = self.notes_dir / card_type
            if not type_dir.exists():
                continue
            for md_file in type_dir.glob("*.md"):
                card = lobster_utils.NoteCard(str(md_file))
                wiki_c = card.frontmatter.get('wiki_concepts', [])
                if isinstance(wiki_c, str):
                    wiki_c = [wiki_c]
                for concept in wiki_c:
                    if concept not in valid_wiki_names:
                        self.issues.append({
                            'severity': 'warn',
                            'check': 'broken-wiki-link',
                            'file': str(md_file),
                            'detail': f"wiki_concepts '{concept}' 没有对应的 wiki 页面"
                        })

    def _check_wiki_broken_card_links(self):
        """检查 wiki 页面的 lobster_cards 是否有对应的卡片文件"""
        valid_card_names: Set[str] = set()
        for card_type in ["判断卡", "方法卡", "案例卡", "信息卡", "日常工作"]:
            type_dir = self.notes_dir / card_type
            if type_dir.exists():
                for f in type_dir.glob("*.md"):
                    valid_card_names.add(f.stem)

        # 扫描所有 wiki 页面
        if self.wiki_dir.exists():
            for md_file in self.wiki_dir.rglob("*.md"):
                if md_file.name in ('index.md', 'log.md'):
                    continue
                page = lobster_utils.NoteCard(str(md_file))
                lc = page.frontmatter.get('lobster_cards', [])
                if isinstance(lc, str):
                    lc = [lc]
                for card_name in lc:
                    if card_name not in valid_card_names:
                        self.issues.append({
                            'severity': 'warn',
                            'check': 'broken-card-link',
                            'file': str(md_file),
                            'detail': f"lobster_cards '{card_name}' 没有对应的卡片文件"
                        })

    def _check_orphan_cards(self):
        """检查孤儿卡片（无 wiki_concepts、无 related）"""
        for card_type in ["判断卡", "方法卡", "案例卡"]:
            type_dir = self.notes_dir / card_type
            if not type_dir.exists():
                continue
            for md_file in type_dir.glob("*.md"):
                card = lobster_utils.NoteCard(str(md_file))
                wiki_c = card.frontmatter.get('wiki_concepts', [])
                related = card.frontmatter.get('related', [])
                if (not wiki_c or (isinstance(wiki_c, list) and len(wiki_c) == 0)) and \
                   (not related or (isinstance(related, list) and len(related) == 0)):
                    self.issues.append({
                        'severity': 'info',
                        'check': 'orphan-card',
                        'file': str(md_file),
                        'detail': '卡片没有 wiki_concepts 和 related 引用'
                    })

    def _check_missing_frontmatter(self):
        """检查缺失关键字段的卡片"""
        required_fields = {
            '判断卡': ['type', 'confidence', 'tags', 'created'],
            '方法卡': ['type', 'confidence', 'tags', 'created'],
            '案例卡': ['type', 'confidence', 'tags', 'created'],
        }
        for card_type, fields in required_fields.items():
            type_dir = self.notes_dir / f"{card_type}s"
            if not type_dir.exists():
                continue
            for md_file in type_dir.glob("*.md"):
                card = lobster_utils.NoteCard(str(md_file))
                for field in fields:
                    if field not in card.frontmatter or not card.frontmatter[field]:
                        self.issues.append({
                            'severity': 'warn',
                            'check': 'missing-field',
                            'file': str(md_file),
                            'detail': f"缺少必要字段: {field}"
                        })

    def _check_status_consistency(self):
        """检查 status 字段值是否在合法范围内"""
        valid_statuses = {'new', 'growing', 'mature', 'outdated', 'discarded'}
        for card_type in ["判断卡", "方法卡", "案例卡", "信息卡", "日常工作"]:
            type_dir = self.notes_dir / card_type
            if not type_dir.exists():
                continue
            for md_file in type_dir.glob("*.md"):
                card = lobster_utils.NoteCard(str(md_file))
                status = card.status
                if status and status.lower() not in valid_statuses:
                    self.issues.append({
                        'severity': 'info',
                        'check': 'status-consistency',
                        'file': str(md_file),
                        'detail': f"status 值 '{status}' 不在标准范围内，建议使用: {', '.join(sorted(valid_statuses))}"
                    })


def main():
    parser = argparse.ArgumentParser(description='Lobster 知识库健康检查')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 输出')
    args = parser.parse_args()

    config = lobster_utils.LobsterConfig()
    checker = LintChecker(
        wiki_dir=Path(config.config.get('wiki_dir', 'personal-wiki/wiki')),
        notes_dir=Path(config.notes_dir),
    )

    issues = checker.check_all()

    if args.json:
        import json
        print(json.dumps(issues, ensure_ascii=False, indent=2))
    else:
        if not issues:
            print("✅ 所有检查通过，知识库状态健康")
        else:
            by_severity = {'error': [], 'warn': [], 'info': []}
            for issue in issues:
                by_severity.get(issue['severity'], by_severity['info']).append(issue)

            if by_severity['error']:
                print(f"❌ 错误 ({len(by_severity['error'])} 个):")
                for i in by_severity['error']:
                    print(f"  [{i['check']}] {Path(i['file']).name}: {i['detail']}")

            if by_severity['warn']:
                print(f"⚠️  警告 ({len(by_severity['warn'])} 个):")
                for i in by_severity['warn']:
                    print(f"  [{i['check']}] {Path(i['file']).name}: {i['detail']}")

            if by_severity['info']:
                print(f"ℹ️  提示 ({len(by_severity['info'])} 个):")
                for i in by_severity['info']:
                    print(f"  [{i['check']}] {Path(i['file']).name}: {i['detail']}")

            print(f"\n共 {len(issues)} 个问题")

    return 0 if not issues else 1


if __name__ == '__main__':
    sys.exit(main() or 0)
