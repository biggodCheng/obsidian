#!/bin/bash
# LLM Wiki 健康检查脚本
# 用法: ./lint-wiki.sh

echo "🔍 Wiki 健康检查"
echo ""
echo "正在检查 wiki 目录..."
echo ""

WIKI_DIR="${WIKI_DIR:-wiki}"

if [ ! -d "$WIKI_DIR" ]; then
    echo "❌ 错误: wiki 目录不存在"
    echo "提示: 请在 wiki 根目录运行此脚本，或设置 WIKI_DIR 环境变量"
    exit 1
fi

# 统计信息
echo "📊 统计信息:"
echo "  实体页面: $(find "$WIKI_DIR/entities" -name "*.md" 2>/dev/null | wc -l)"
echo "  概念页面: $(find "$WIKI_DIR/concepts" -name "*.md" 2>/dev/null | wc -l)"
echo "  摘要页面: $(find "$WIKI_DIR/summaries" -name "*.md" 2>/dev/null | wc -l)"
echo "  综合页面: $(find "$WIKI_DIR/synthesis" -name "*.md" 2>/dev/null | wc -l)"
echo ""

# 检查孤立页面
echo "🔗 检查孤立页面..."
echo "提示: 将此请求发送给 LLM 进行完整检查:"
echo ""
echo "对 wiki 进行健康检查，包括："
echo "1. 检查页面之间的矛盾"
echo "2. 找出孤立页面（没有入站链接）"
echo "3. 识别缺失的交叉引用"
echo "4. 检查过时内容"
echo "5. 建议新的源文件或调查方向"
echo ""

# 检查日志格式
if [ -f "$WIKI_DIR/log.md" ]; then
    echo "📝 最近的日志条目:"
    grep "^## \[" "$WIKI_DIR/log.md" 2>/dev/null | tail -5 || echo "  无日志条目"
    echo ""
fi

# 快速检查
echo "⚡ 快速检查:"

# 检查是否有未链接的文件
unlinked_files=$(find "$WIKI_DIR" -name "*.md" -type f | while read file; do
    basename=$(basename "$file" .md)
    if ! grep -qr "\[\[$basename\]\]" "$WIKI_DIR" 2>/dev/null; then
        echo "$file"
    fi
done)

if [ -n "$unlinked_files" ]; then
    echo "  ⚠️  可能的孤立页面:"
    echo "$unlinked_files" | head -5 | sed 's/^/    /'
    if [ $(echo "$unlinked_files" | wc -l) -gt 5 ]; then
        echo "    ... (还有更多)"
    fi
else
    echo "  ✅ 没有明显的孤立页面"
fi

echo ""
echo "💡 提示: 将完整的健康检查请求发送给 LLM 以获得详细报告"
