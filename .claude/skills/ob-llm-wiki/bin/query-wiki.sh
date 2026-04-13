#!/bin/bash
# LLM Wiki 查询辅助脚本
# 用法: ./query-wiki.sh "你的问题"

QUESTION="$1"

if [ -z "$QUESTION" ]; then
    echo "用法: $0 \"你的问题\""
    echo ""
    echo "示例:"
    echo "  $0 \"什么是机器学习？\""
    echo "  $0 \"对比深度学习和传统机器学习\""
    exit 1
fi

echo "🔍 查询 Wiki: $QUESTION"
echo ""
echo "将此问题发送给 LLM："
echo ""
echo "查询 wiki：$QUESTION"
echo ""
echo "或者，如果你想查看相关页面："
echo "1. 查看 wiki/index.md 找到相关页面"
echo "2. 使用 grep 搜索: grep -r \"$QUESTION\" wiki/"
