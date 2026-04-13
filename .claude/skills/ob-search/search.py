#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lobster Search - 知识库搜索工具
在 Obsidian 知识库中搜索笔记卡片和 Wiki 页面
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

# 自动定位 vault 根目录（从 config.json 向上查找）
def find_vault_path():
    """从当前脚本位置向上查找 .lobster/config.json"""
    current = Path(__file__).resolve().parent
    for _ in range(5):
        config_path = current / ".lobster" / "config.json"
        if config_path.exists():
            return current
        current = current.parent
    # fallback: 从环境变量或默认值
    return Path(os.environ.get("LOBSTER_VAULT", "d:\\DATA\\cgq-obsidian"))

vault_path = find_vault_path()
utils_path = vault_path / ".lobster" / "lobster_utils.py"

if utils_path.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("lobster_utils", utils_path)
    lobster_utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lobster_utils)
else:
    print(f"错误: 找不到 lobster_utils.py (搜索路径: {utils_path})", file=sys.stderr)
    sys.exit(1)


def get_match_context(content: str, query: str, context_lines: int = 3) -> str:
    """提取匹配关键词周围的上下文片段"""
    lines = content.split('\n')
    query_lower = query.lower()

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            return '\n'.join(lines[start:end])

    # fallback: 返回前 200 字符
    return content[:200]


def print_note(note, show_content=False, index=None, query=None):
    """打印笔记信息"""
    if index is not None:
        print(f"\n[{index}] ", end="")
    else:
        print("\n---")

    # 显示来源层
    rel_path = note.filepath
    if 'personal-wiki/notes/' in str(rel_path):
        layer = "[卡片]"
    elif 'personal-wiki/wiki/' in str(rel_path):
        layer = "[Wiki]"
    else:
        layer = "[其他]"

    print(f"{layer} {note.filepath.name}")
    print(f"  类型: {note.card_type}")
    print(f"  标题: {note.title}")
    if note.confidence:
        print(f"  信心: {note.confidence}")
    if note.tags:
        print(f"  标签: {', '.join(note.tags)}")

    wiki_c = note.frontmatter.get('wiki_concepts', [])
    if wiki_c:
        print(f"  概念: {', '.join(str(c) for c in wiki_c)}")

    if show_content and note.content:
        if query:
            context = get_match_context(note.content, query)
        else:
            context = note.content[:200] + ("..." if len(note.content) > 200 else "")
        print(f"\n  内容:\n  {context.replace(chr(10), chr(10) + '  ')}")


def main():
    parser = argparse.ArgumentParser(
        description='在 Obsidian 知识库中搜索笔记卡片和 Wiki 页面',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python search.py 用户体验                        # 搜索关键词
  python search.py 社交货币 --scope all            # 同时搜索卡片和 Wiki
  python search.py 社交货币 --scope wiki           # 只搜索 Wiki
  python search.py --concepts 谈判博弈              # 按概念搜索关联卡片
  python search.py --concepts 谈判博弈,社交货币     # 多概念搜索
  python search.py "判断卡" --type judgment
  python search.py 产品 --tags 产品,设计
  python search.py "用户转化" --show-content        # 显示匹配上下文
        '''
    )

    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--type', '-t', choices=['judgment', 'method', '案例卡', 'information', '任务卡'],
                        help='按卡片类型过滤')
    parser.add_argument('--confidence', '-c', choices=['low', 'medium', 'high'],
                        help='按信心程度过滤')
    parser.add_argument('--tags', help='按标签过滤，逗号分隔')
    parser.add_argument('--scope', choices=['notes', 'wiki', 'all'], default='notes',
                        help='搜索范围: notes(默认) / wiki / all')
    parser.add_argument('--concepts', help='按 wiki 概念搜索关联卡片，逗号分隔')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有笔记（不搜索）')
    parser.add_argument('--show-content', '-c', action='store_true',
                        help='显示内容预览（匹配上下文）')
    parser.add_argument('--json', '-j', action='store_true',
                        help='以 JSON 格式输出')

    args = parser.parse_args()

    # 初始化知识库
    try:
        vault = lobster_utils.LobsterVault()
    except Exception as e:
        print(f"错误: 初始化知识库失败 - {e}", file=sys.stderr)
        sys.exit(1)

    # 构建过滤器
    filters = {}
    if args.type:
        filters['type'] = args.type
    if args.confidence:
        filters['confidence'] = args.confidence
    if args.tags:
        filters['tags'] = [t.strip() for t in args.tags.split(',')]

    # 解析 concepts 参数
    concepts = None
    if args.concepts:
        concepts = [c.strip() for c in args.concepts.split(',')]

    # 按概念搜索或关键词搜索
    if args.list or (not args.query and not concepts):
        notes = vault.list_notes(filters if filters else None)
    elif concepts:
        notes = vault.search(args.query or "", filters=filters or None, concepts=concepts)
    else:
        notes = vault.search(args.query, filters=filters or None, scope=args.scope)

    # 输出结果
    if args.json:
        results = []
        for note in notes:
            results.append({
                'file': str(note.filepath),
                'type': note.card_type,
                'title': note.title,
                'status': note.status,
                'tags': note.tags,
                'confidence': note.confidence,
                'wiki_concepts': note.frontmatter.get('wiki_concepts', []),
            })
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not notes:
            print("未找到匹配的笔记")
        else:
            print(f"找到 {len(notes)} 条结果:")
            for i, note in enumerate(notes, 1):
                print_note(note, show_content=args.show_content, index=i, query=args.query)

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
