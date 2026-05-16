#!/bin/bash
# AI小说和短剧剧本智能体 - Web服务启动脚本

echo "============================================================"
echo "AI小说和短剧剧本智能体 - Web界面"
echo "============================================================"

cd "$(dirname "$0")"

echo ""
echo "启动Web服务..."
echo "访问地址: http://localhost:5001"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
