#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lobster Note - 笔记管理工具
快速创建 Obsidian 知识库中的笔记卡片
"""

import sys
import os
import argparse
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


def create_note(card_type, title, content="", tags=None, confidence="low"):
    """创建新笔记"""
    vault = lobster_utils.LobsterVault()

    metadata = {
        'type': card_type,
        'confidence': confidence,
        'tags': tags or []
    }

    # 如果没有提供内容，使用模板内容
    if not content:
        template_path = vault_path / "templates" / f"{card_type}.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

    note = vault.create_note(card_type, title, content, metadata)
    return note


def main():
    parser = argparse.ArgumentParser(
        description='Obsidian 知识库笔记管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python note.py 判断卡 "价格敏感度判断" --content "降价10%增加30%销量"
  python note.py 方法卡 "A/B测试流程" --confidence high
  python note.py 案例卡 "客户转化案例" --tags 营销,转化
  python note.py 信息卡 "产品参数" --confidence high
        '''
    )

    parser.add_argument('type', choices=['判断卡', '方法卡', '案例卡', '信息卡'],
                       help='卡片类型')
    parser.add_argument('title', help='笔记标题')
    parser.add_argument('--content', '-c', default='', help='笔记内容')
    parser.add_argument('--tags', help='标签，逗号分隔')
    parser.add_argument('--confidence', choices=['low', 'medium', 'high'],
                       default='low', help='信心程度')

    args = parser.parse_args()

    # 解析标签
    tags = []
    if args.tags:
        tags = [t.strip() for t in args.tags.split(',')]

    note = create_note(args.type, args.title, args.content, tags, args.confidence)

    print(f"✓ 笔记已创建: {note.filepath}")
    print(f"  类型: {args.type}")
    print(f"  标题: {args.title}")
    if tags:
        print(f"  标签: {', '.join(tags)}")

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
