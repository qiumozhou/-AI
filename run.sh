#!/bin/bash

echo "===================================="
echo "中国象棋辅助程序"
echo "===================================="
echo ""
echo "选择运行模式:"
echo "1. GUI图形界面版本 (推荐)"
echo "2. 命令行版本"
echo "3. 下载/配置引擎"
echo "4. 安装依赖"
echo "5. 退出"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "启动GUI版本..."
        python3 chess_gui.py
        ;;
    2)
        echo ""
        echo "启动命令行版本..."
        python3 chess_assistant.py
        ;;
    3)
        echo ""
        echo "配置引擎..."
        python3 download_engine.py
        ;;
    4)
        echo ""
        echo "安装依赖..."
        pip3 install -r requirements.txt
        echo ""
        echo "安装完成！"
        ;;
    5)
        exit 0
        ;;
    *)
        echo ""
        echo "无效选项！"
        ;;
esac

read -p "按任意键继续..."

