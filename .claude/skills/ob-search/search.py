#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lobster Search - 知识库搜索工具
在 Obsidian 知识库中搜索笔记卡片
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 修复 Windows 终端编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加工具模块路径
vault_path = Path(r"d:\DATA\cgq-obsidian")
utils_path = vault_path / ".lobster" / "lobster_utils.py"

if utils_path.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("lobster_utils", utils_path)
    lobster_utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lobster_utils)
else:
    print("错误: 找不到 lobster_utils.py", file=sys.stderr)
    sys.exit(1)


def print_note(note, show_content=False, index=None):
    """打印笔记信息"""
    if index is not None:
        print(f"\n[{index}] ", end="")
    else:
        print("\n---")

    print(f"文件: {note.filepath.name}")
    print(f"类型: {note.card_type}")
    print(f"标题: {note.title}")
    print(f"状态: {note.status}")
    if note.tags:
        print(f"标签: {', '.join(note.tags)}")
    if note.confidence:
        print(f"信心: {note.confidence}")

    if show_content and note.content:
        # 显示前 200 字符
        preview = note.content[:200] + "..." if len(note.content) > 200 else note.content
        print(f"\n内容预览:\n{preview}")


def main():
    parser = argparse.ArgumentParser(
        description='在 Obsidian 知识库中搜索笔记卡片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python search.py 用户体验
  python search.py "判断卡" --type judgment
  python search.py 产品 --tags 产品,设计
  python search.py 方法 --type method --status mature
  python search.py "用户转化" --show-content
        '''
    )

    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--type', '-t', choices=['judgment', 'method', 'case', 'information', 'todo'],
                        help='按卡片类型过滤')
    parser.add_argument('--status', '-s', help='按状态过滤 (new/growing/mature/outdated/discarded/pending/completed)')
    parser.add_argument('--tags', help='按标签过滤，逗号分隔')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有笔记（不搜索）')
    parser.add_argument('--show-content', '-c', action='store_true',
                        help='显示内容预览')
    parser.add_argument('--json', '-j', action='store_true',
                        help='以 JSON 格式输出')
    parser.add_argument('--vault', help='知识库路径（默认使用配置文件中的路径）')

    args = parser.parse_args()

    # 初始化知识库
    vault_path_override = args.vault if args.vault else None

    if vault_path_override:
        # 使用指定的路径
        class CustomConfig:
            def __init__(self, path):
                self.notes_dir = Path(path) / "notes"

        config = CustomConfig(vault_path_override)
        vault = lobster_utils.LobsterVault(config)
    else:
        # 使用默认配置
        vault = lobster_utils.LobsterVault()

    # 列出所有笔记或搜索
    if args.list or not args.query:
        filters = {}
        if args.type:
            filters['type'] = args.type
        if args.status:
            filters['status'] = args.status
        if args.tags:
            filters['tags'] = [t.strip() for t in args.tags.split(',')]

        notes = vault.list_notes(filters)
    else:
        filters = {}
        if args.type:
            filters['type'] = args.type
        if args.status:
            filters['status'] = args.status
        if args.tags:
            filters['tags'] = [t.strip() for t in args.tags.split(',')]

        notes = vault.search(args.query, filters)

    # 输出结果
    if args.json:
        # JSON 输出
        results = []
        for note in notes:
            results.append({
                'file': str(note.filepath),
                'type': note.card_type,
                'title': note.title,
                'status': note.status,
                'tags': note.tags,
                'confidence': note.confidence
            })
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        # 文本输出
        if not notes:
            print("未找到匹配的笔记")
        else:
            print(f"找到 {len(notes)} 条笔记:")
            for i, note in enumerate(notes, 1):
                print_note(note, show_content=args.show_content, index=i)

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
