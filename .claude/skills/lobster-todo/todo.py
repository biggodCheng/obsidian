#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lobster Todo - 任务管理工具
创建、查看、更新 Obsidian 知识库中的任务卡片
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
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


def create_task(title, description="", priority="medium", due=None, tags=None):
    """创建新任务"""
    vault = lobster_utils.LobsterVault()

    metadata = {
        'type': 'todo',
        'status': 'pending',
        'priority': priority,
        'tags': tags or []
    }

    if due:
        metadata['due'] = due

    content = f"## 任务描述\n{description}\n\n## 子任务\n\n- [ ] \n\n## 备注\n"

    note = vault.create_note('todo', title, content, metadata)
    return note


def list_tasks(status=None, show_completed=False):
    """列出任务"""
    vault = lobster_utils.LobsterVault()

    filters = {'type': 'todo'}

    if not show_completed:
        filters['status'] = ['pending', 'in_progress']
    elif status:
        filters['status'] = status

    notes = vault.list_notes(filters)

    # 按截止日期和优先级排序
    def sort_key(note):
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        due = note.frontmatter.get('due', '9999-12-31')
        return (due, priority_order.get(note.frontmatter.get('priority', 'medium'), 1))

    notes.sort(key=sort_key)

    return notes


def update_task_status(filepath, new_status):
    """更新任务状态"""
    note = lobster_utils.NoteCard(filepath)

    # 读取文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换状态
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('status:'):
            lines[i] = f'status: {new_status}'
            break
    else:
        # 没有 status 字段，添加到 frontmatter
        for i, line in enumerate(lines):
            if line == '---':
                lines.insert(i + 1, f'status: {new_status}')
                break

    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Obsidian 知识库任务管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python todo.py add "明天开会" --description "下午3点产品会议"
  python todo.py add "完成报告" --priority high --due 2026-04-01
  python todo.py list
  python todo.py list --status pending
  python todo.py complete "任务文件路径"
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # add 命令
    add_parser = subparsers.add_parser('add', help='添加新任务')
    add_parser.add_argument('title', help='任务标题')
    add_parser.add_argument('--description', '-d', default='', help='任务描述')
    add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'],
                           default='medium', help='优先级')
    add_parser.add_argument('--due', help='截止日期 (YYYY-MM-DD)')
    add_parser.add_argument('--tags', help='标签，逗号分隔')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--status', '-s', choices=['pending', 'in_progress', 'completed', 'cancelled'],
                            help='按状态过滤')
    list_parser.add_argument('--all', '-a', action='store_true',
                            help='显示所有任务（包括已完成）')

    # complete 命令
    complete_parser = subparsers.add_parser('complete', help='标记任务为完成')
    complete_parser.add_argument('filepath', help='任务文件路径')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'add':
        # 解析标签
        tags = []
        if args.tags:
            tags = [t.strip() for t in args.tags.split(',')]

        note = create_task(args.title, args.description, args.priority, args.due, tags)
        print(f"✓ 任务已创建: {note.filepath}")
        return 0

    elif args.command == 'list':
        notes = list_tasks(args.status, show_completed=args.all)

        if not notes:
            print("没有找到任务")
        else:
            print(f"\n找到 {len(notes)} 个任务:\n")
            for i, note in enumerate(notes, 1):
                print(f"[{i}] {note.title}")
                print(f"    状态: {note.status} | 优先级: {note.frontmatter.get('priority', 'medium')}")

                due = note.frontmatter.get('due')
                if due:
                    print(f"    截止: {due}")

                if note.tags:
                    print(f"    标签: {', '.join(note.tags)}")

                print()

        return 0

    elif args.command == 'complete':
        if update_task_status(args.filepath, 'completed'):
            print(f"✓ 任务已标记为完成")
            return 0
        else:
            print("✗ 更新失败")
            return 1


if __name__ == '__main__':
    sys.exit(main() or 0)
