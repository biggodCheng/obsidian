#!/usr/bin/env python3
"""
Lobster Article - 文章处理工具
抓取 URL 内容并使用 AI 拆分为知识卡片
"""

import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime

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


def extract_insights(content, url=""):
    """
    从文章内容中提取洞见
    返回各类型卡片的内容列表
    """
    insights = {
        'judgments': [],
        'methods': [],
        'cases': [],
        'information': []
    }

    # 这里应该调用 AI 来分析内容
    # 目前返回一个示例结构
    # 实际使用时，需要集成 Claude API 或其他 AI 服务

    return insights


def create_cards_from_insights(insights, source_url="", title="文章摘录"):
    """从洞见创建卡片"""
    vault = lobster_utils.LobsterVault()
    created_cards = []

    # 创建源文章信息卡
    source_content = f"""
## 原文信息

- **来源**: {source_url}
- **处理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 文章摘要

从这篇文章中提取了以下知识卡片。
"""
    source_metadata = {
        'type': 'information',
        'confidence': 'high',
        'tags': ['来源文章'],
        'source_url': source_url
    }

    source_card = vault.create_note('information', f"来源: {title}", source_content, source_metadata)
    created_cards.append(('source', source_card))

    # 创建判断卡
    for i, judgment in enumerate(insights['judgments'], 1):
        card = vault.create_note(
            'judgment',
            f"判断: {judgment.get('title', f'判断{i}')}",
            judgment.get('content', ''),
            {
                'confidence': judgment.get('confidence', 'low'),
                'tags': judgment.get('tags', []),
                'source': source_url
            }
        )
        created_cards.append(('judgment', card))

    # 创建方法卡
    for i, method in enumerate(insights['methods'], 1):
        card = vault.create_note(
            'method',
            f"方法: {method.get('title', f'方法{i}')}",
            method.get('content', ''),
            {
                'confidence': method.get('confidence', 'medium'),
                'tags': method.get('tags', []),
                'source': source_url
            }
        )
        created_cards.append(('method', card))

    # 创建案例卡
    for i, case in enumerate(insights['cases'], 1):
        card = vault.create_note(
            'case',
            f"案例: {case.get('title', f'案例{i}')}",
            case.get('content', ''),
            {
                'confidence': 'medium',
                'tags': case.get('tags', []),
                'source': source_url
            }
        )
        created_cards.append(('case', card))

    # 创建信息卡
    for i, info in enumerate(insights['information'], 1):
        card = vault.create_note(
            'information',
            f"信息: {info.get('title', f'信息{i}')}",
            info.get('content', ''),
            {
                'confidence': 'high',
                'tags': info.get('tags', []),
                'source': source_url
            }
        )
        created_cards.append(('information', card))

    return created_cards


def main():
    parser = argparse.ArgumentParser(
        description='处理网页文章并提取知识卡片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python article.py https://example.com/article
  python article.py https://example.com/article --title "文章标题"
  python article.py https://example.com/article --output result.json
        '''
    )

    parser.add_argument('url', help='文章 URL')
    parser.add_argument('--title', '-t', help='文章标题（默认自动提取）')
    parser.add_argument('--content', '-c', help='直接提供内容（跳过 URL 抓取）')
    parser.add_argument('--output', '-o', help='输出结果到 JSON 文件')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='分析但不创建卡片')

    args = parser.parse_args()

    # 获取文章内容
    if args.content:
        content = args.content
        title = args.title or "手动输入"
    else:
        print(f"正在抓取: {args.url}")
        # 这里需要使用 web reader 或其他工具抓取内容
        # 示例代码，实际需要集成具体工具
        print("注意: 需要集成 web reader MCP server 才能抓取 URL")
        print("或者使用 --content 参数直接提供内容")
        return 1

    # 提取洞见
    print("正在分析文章...")
    insights = extract_insights(content, args.url)

    # 统计
    total = sum(len(v) for v in insights.values())
    print(f"\n提取到 {total} 个洞见:")
    print(f"  判断卡: {len(insights['judgments'])} 个")
    print(f"  方法卡: {len(insights['methods'])} 个")
    print(f"  案例卡: {len(insights['cases'])} 个")
    print(f"  信息卡: {len(insights['information'])} 个")

    if args.dry_run:
        print("\n[DRY RUN] 未创建卡片")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(insights, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {args.output}")
        return 0

    # 创建卡片
    print("\n正在创建卡片...")
    title = args.title or "文章摘录"
    cards = create_cards_from_insights(insights, args.url, title)

    print(f"\n✓ 成功创建 {len(cards)} 张卡片:")
    for card_type, card in cards:
        print(f"  [{card_type}] {card.title}")

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
