#!/usr/bin/env python3
"""
Lobster Article - 文章处理工具（基于三大黄金法则）

三大黄金法则：
1. 精确检索原则（拒绝长篇大论）
2. 语义纯粹原则（保持卡片纯粹）
3. 未来复用原则（剥离特定语境）
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

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


# =============================================================================
# 三大黄金法则检验器
# =============================================================================

class GoldenRulesValidator:
    """三大黄金法则检验器"""

    @staticmethod
    def validate_precision(title: str, content: str) -> Tuple[bool, List[str]]:
        """
        法则一：精确检索检验
        返回: (是否通过, 违规原因列表)
        """
        violations = []

        # 检查标题长度（10-25字最佳，不超过30字）
        title_len = len(title)
        if title_len < 10:
            violations.append(f"标题过短({title_len}字)，建议10-25字")
        elif title_len > 30:
            violations.append(f"标题过长({title_len}字)，建议不超过30字")

        # 检查标题是否为完整陈述句
        if not title.strip().endswith(('。', '.', '！', '！', '？', '？')):
            violations.append("标题不是完整陈述句")

        # 检查是否包含泛化词
        vague_words = ['关于', '几点', '思考', '分析', '总结', '整理', '记录']
        for word in vague_words:
            if word in title:
                violations.append(f"标题包含泛化词「{word}」，建议使用具体主张")
                break

        # 检查正文长度（不超过300字）
        content_len = len(content.strip())
        if content_len > 300:
            violations.append(f"正文过长({content_len}字)，建议不超过300字")

        # 检查核心概念词密度（标题应包含核心概念）
        # 简化处理：标题应该至少有一个实质性名词
        if not re.search(r'[\u4e00-\u9fa5]{2,}', title):
            violations.append("标题缺少核心概念词")

        return len(violations) == 0, violations

    @staticmethod
    def validate_purity(content: str, card_type: str) -> Tuple[bool, List[str]]:
        """
        法则二：语义纯粹检验
        返回: (是否通过, 违规原因列表)
        """
        violations = []

        # 检查是否包含连接词（信号：可能混合多个语义）
        mixed_signals = ['以及', '另外', '同时', '此外', '加之', '而且', '并且']
        for signal in mixed_signals:
            if signal in content:
                violations.append(f"包含混合语义信号词「{signal}」，建议拆分")
                break

        # 检查是否有"第一、第二、第三"（并列关系信号）
        if re.search(r'第[一二三四五]、', content):
            violations.append("包含并列关系(第一、第二)，建议拆成多张卡")

        # 检查是否有上下文指代词
        context_refs = ['上文', '前述', '上述', '正如前', '如前所述']
        for ref in context_refs:
            if ref in content:
                violations.append(f"包含上下文指代词「{ref}」，使用[[wikilink]]明确链接")
                break

        # 检查是否有特定语境词（法则三的一部分）
        context_words = ['本文作者', '这篇文章', '该文认为', '书中提到']
        for word in context_words:
            if word in content:
                violations.append(f"包含特定语境词「{word}」，建议去除")
                break

        return len(violations) == 0, violations

    @staticmethod
    def validate_reusability(title: str, content: str) -> Tuple[bool, List[str]]:
        """
        法则三：未来复用检验
        返回: (是否通过, 违规原因列表)
        """
        violations = []

        # 检查特定语境词
        context_markers = [
            '本文作者', '这篇文章', '该文认为', '书中提到',
            '在XX领域', '在XX行业', '对于XX产品'
        ]
        for marker in context_markers:
            if marker in content or marker in title:
                violations.append(f"包含特定语境词「{marker}」，建议抽象为通用原则")
                break

        # 检查是否包含具体时间或年份（可能限制复用）
        # 注意：有些判断确实需要时间条件，这是合理的
        if re.search(r'20\d{2}年', content) and '适用条件' not in content:
            violations.append("包含具体时间但未标注适用条件，建议添加")

        # 检查是否有具体产品名但未抽象
        # 简化处理：如果有具体品牌但无"适用条件"字段
        brand_words = ['抖音', '微信', 'Nike', 'Apple', 'Tesla']
        has_brand = any(brand in content for brand in brand_words)
        if has_brand and '适用条件' not in content:
            violations.append("包含具体品牌案例但未标注适用条件，建议抽象")

        return len(violations) == 0, violations

    @classmethod
    def validate_all(cls, title: str, content: str, card_type: str) -> Dict[str, any]:
        """
        执行全部三层检验
        返回: {
            'passed': bool,
            'precision': (bool, List[str]),
            'purity': (bool, List[str]),
            'reusability': (bool, List[str])
        }
        """
        precision_result = cls.validate_precision(title, content)
        purity_result = cls.validate_purity(content, card_type)
        reusability_result = cls.validate_reusability(title, content)

        all_passed = all([
            precision_result[0],
            purity_result[0],
            reusability_result[0]
        ])

        return {
            'passed': all_passed,
            'precision': precision_result,
            'purity': purity_result,
            'reusability': reusability_result,
            'total_violations': (
                len(precision_result[1]) +
                len(purity_result[1]) +
                len(reusability_result[1])
            )
        }


# =============================================================================
# 卡片创建器（带三大法则检验）
# =============================================================================

class CardCreator:
    """卡片创建器 - 集成三大黄金法则"""

    def __init__(self, vault):
        self.vault = vault
        self.validator = GoldenRulesValidator()
        self.created_count = {'判断卡': 0, '方法卡': 0, '案例卡': 0, 'information': 0}
        self.failed_count = {'判断卡': 0, '方法卡': 0, '案例卡': 0, 'information': 0}
        self.validation_log = []

    def _sanitize_content(self, content: str) -> str:
        """自动修正一些常见的法则违规"""
        # 去除特定语境词
        content = re.sub(r'本文作者(认为|指出|说)', '', content)
        content = re.sub(r'这篇文章(认为|指出|提到)', '', content)
        content = re.sub(r'该文(认为|指出)', '', content)

        # 去除"第一、第二"格式，尝试用换行代替
        content = re.sub(r'第([一二三四五])、', r'\n\1. ', content)

        return content.strip()

    def create_card(
        self,
        card_type: str,
        title: str,
        content: str,
        metadata: dict,
        auto_fix: bool = True
    ) -> Optional[dict]:
        """
        创建卡片，自动执行三大法则检验

        Args:
            card_type: 卡片类型 (判断卡/方法卡/案例卡/information)
            title: 卡片标题
            content: 卡片内容
            metadata: 元数据
            auto_fix: 是否自动修正可修复的问题

        Returns:
            创建的卡片信息，如果检验失败则返回None
        """
        # 自动修正
        if auto_fix:
            content = self._sanitize_content(content)

        # 执行三大法则检验
        validation_result = self.validator.validate_all(title, content, card_type)

        # 记录检验结果
        self.validation_log.append({
            'title': title,
            'type': card_type,
            'validation': validation_result
        })

        # 如果检验未通过，记录失败
        if not validation_result['passed']:
            self.failed_count[card_type] += 1
            return None

        # 创建卡片
        try:
            card = self.vault.create_note(card_type, title, content, metadata)
            self.created_count[card_type] += 1
            return {
                'type': card_type,
                'title': title,
                'path': card.get('path', ''),
                'validation': validation_result
            }
        except Exception as e:
            print(f"创建卡片失败: {e}", file=sys.stderr)
            self.failed_count[card_type] += 1
            return None

    def get_statistics(self) -> dict:
        """获取统计信息"""
        total_created = sum(self.created_count.values())
        total_failed = sum(self.failed_count.values())

        return {
            'created': self.created_count,
            'failed': self.failed_count,
            'total_created': total_created,
            'total_failed': total_failed,
            'success_rate': total_created / (total_created + total_failed) if (total_created + total_failed) > 0 else 0
        }

    def print_validation_report(self):
        """打印检验报告"""
        if not self.validation_log:
            print("无检验记录")
            return

        print("\n" + "="*60)
        print("三大黄金法则检验报告")
        print("="*60)

        passed = sum(1 for log in self.validation_log if log['validation']['passed'])
        total = len(self.validation_log)

        print(f"\n总计: {passed}/{total} 通过 ({passed/total*100:.1f}%)")

        # 按类型统计
        for card_type in ['判断卡', '方法卡', '案例卡', 'information']:
            type_logs = [log for log in self.validation_log if log['type'] == card_type]
            if type_logs:
                type_passed = sum(1 for log in type_logs if log['validation']['passed'])
                print(f"  {card_type}: {type_passed}/{len(type_logs)} 通过")

        # 显示失败详情
        failed_logs = [log for log in self.validation_log if not log['validation']['passed']]
        if failed_logs:
            print("\n失败详情:")
            for log in failed_logs[:5]:  # 只显示前5个
                print(f"\n  [{log['type']}] {log['title']}")
                violations = []
                for rule_name in ['precision', 'purity', 'reusability']:
                    rule_passed, rule_violations = log['validation'][rule_name]
                    if not rule_passed:
                        violations.extend([f"    - {v}" for v in rule_violations])
                for v in violations[:3]:  # 每张卡只显示前3条
                    print(v)

            if len(failed_logs) > 5:
                print(f"\n  ... 还有 {len(failed_logs) - 5} 张卡片未通过检验")

        print("="*60 + "\n")


# =============================================================================
# 洞见提取器（待集成AI）
# =============================================================================

def extract_insights(content: str, url: str = "") -> Dict[str, List[dict]]:
    """
    从文章内容中提取洞见

    TODO: 集成 Claude API 或其他 AI 服务
    当前返回示例结构
    """
    insights = {
        '判断卡': [
            {
                'title': '示例判断卡',
                'content': '这是一个示例判断卡内容。',
                'confidence': 'medium',
                'tags': ['示例'],
                'applicable_conditions': ['示例条件'],
                'inapplicable_conditions': ['示例不适用条件']
            }
        ],
        '方法卡': [],
        'cases': [],
        'information': []
    }

    return insights


# =============================================================================
# 主程序
# =============================================================================

def create_cards_from_insights(
    insights: Dict[str, List[dict]],
    source_url: str = "",
    title: str = "文章摘录",
    strict_mode: bool = True
) -> Tuple[List[dict], CardCreator]:
    """
    从洞见创建卡片（集成三大法则检验）

    Args:
        insights: 提取的洞见数据
        source_url: 来源URL
        title: 文章标题
        strict_mode: 严格模式 - 未通过检验的卡片不会创建

    Returns:
        (创建的卡片列表, CardCreator实例)
    """
    vault = lobster_utils.LobsterVault()
    creator = CardCreator(vault)
    created_cards = []

    # 创建判断卡
    for judgment in insights['判断卡']:
        content = judgment.get('content', '')

        # 添加适用条件字段（如果缺失）
        if '适用条件' not in content and judgment.get('applicable_conditions'):
            conditions = judgment['applicable_conditions']
            content += f"\n\n## 适用条件\n{', '.join(conditions)}"

        metadata = {
            'type': '判断卡',
            'confidence': judgment.get('confidence', 'low'),
            'tags': judgment.get('tags', []),
            'sources': [source_url]
        }

        card = creator.create_card(
            '判断卡',
            judgment.get('title', '判断'),
            content,
            metadata
        )
        if card:
            created_cards.append(card)

    # 创建方法卡
    for method in insights['方法卡']:
        metadata = {
            'type': '方法卡',
            'confidence': method.get('confidence', 'medium'),
            'tags': method.get('tags', []),
            'sources': [source_url]
        }

        card = creator.create_card(
            '方法卡',
            method.get('title', '方法'),
            method.get('content', ''),
            metadata
        )
        if card:
            created_cards.append(card)

    # 创建案例卡
    for case in insights['cases']:
        metadata = {
            'type': '案例卡',
            'confidence': 'medium',
            'tags': case.get('tags', []),
            'sources': [source_url]
        }

        card = creator.create_card(
            '案例卡',
            case.get('title', '案例'),
            case.get('content', ''),
            metadata
        )
        if card:
            created_cards.append(card)

    # 创建信息卡（谨慎创建）
    for info in insights['information']:
        metadata = {
            'type': 'information',
            'confidence': 'high',
            'tags': info.get('tags', []),
            'sources': [source_url]
        }

        card = creator.create_card(
            'information',
            info.get('title', '信息'),
            info.get('content', ''),
            metadata
        )
        if card:
            created_cards.append(card)

    return created_cards, creator


def main():
    parser = argparse.ArgumentParser(
        description='处理网页文章并提取知识卡片（基于三大黄金法则）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
三大黄金法则：
  1. 精确检索原则（拒绝长篇大论）
  2. 语义纯粹原则（保持卡片纯粹）
  3. 未来复用原则（剥离特定语境）

使用示例:
  python article.py https://example.com/article
  python article.py https://example.com/article --title "文章标题"
  python article.py https://example.com/article --output result.json
  python article.py https://example.com/article --strict  # 严格模式
        '''
    )

    parser.add_argument('url', help='文章 URL')
    parser.add_argument('--title', '-t', help='文章标题（默认自动提取）')
    parser.add_argument('--content', '-c', help='直接提供内容（跳过 URL 抓取）')
    parser.add_argument('--output', '-o', help='输出结果到 JSON 文件')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='分析但不创建卡片')
    parser.add_argument('--strict', '-s', action='store_true',
                       help='严格模式：未通过三大法则检验的卡片不创建')
    parser.add_argument('--no-auto-fix', action='store_true',
                       help='禁用自动修正功能')
    parser.add_argument('--show-report', '-r', action='store_true',
                       help='显示详细检验报告')

    args = parser.parse_args()

    # 获取文章内容
    if args.content:
        content = args.content
        title = args.title or "手动输入"
    else:
        print(f"正在抓取: {args.url}")
        # TODO: 集成 web reader 或其他工具
        print("注意: 需要集成 web reader MCP server 才能抓取 URL")
        print("或者使用 --content 参数直接提供内容")
        return 1

    # 提取洞见
    print("正在分析文章...")
    insights = extract_insights(content, args.url)

    # 统计
    total = sum(len(v) for v in insights.values())
    print(f"\n提取到 {total} 个洞见:")
    print(f"  判断卡: {len(insights['判断卡'])} 个")
    print(f"  方法卡: {len(insights['方法卡'])} 个")
    print(f"  案例卡: {len(insights['cases'])} 个")
    print(f"  信息卡: {len(insights['information'])} 个")

    if args.dry_run:
        print("\n[DRY RUN] 未创建卡片")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(insights, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {args.output}")
        return 0

    # 创建卡片（集成三大法则检验）
    print("\n正在创建卡片（执行三大法则检验）...")
    title = args.title or "文章摘录"

    cards, creator = create_cards_from_insights(
        insights,
        args.url,
        title,
        strict_mode=args.strict
    )

    # 获取统计信息
    stats = creator.get_statistics()

    print(f"\n✓ 成功创建 {stats['total_created']} 张卡片:")
    for card_type, count in stats['created'].items():
        if count > 0:
            print(f"  [{card_type}] {count} 张")

    if stats['total_failed'] > 0:
        print(f"\n✗ {stats['total_failed']} 张卡片未通过检验:")
        for card_type, count in stats['failed'].items():
            if count > 0:
                print(f"  [{card_type}] {count} 张")

    # 显示详细报告
    if args.show_report or stats['total_failed'] > 0:
        creator.print_validation_report()

    print(f"\n通过率: {stats['success_rate']*100:.1f}%")

    if args.output:
        result = {
            'statistics': stats,
            'cards': cards,
            'validation_log': creator.validation_log
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
