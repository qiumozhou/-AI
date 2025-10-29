@echo off
chcp 65001 >nul
echo ====================================
echo 中国象棋辅助程序
echo ====================================
echo.
echo 选择运行模式:
echo 1. GUI图形界面版本 (推荐)
echo 2. 命令行版本
echo 3. 下载/配置引擎
echo 4. 安装依赖
echo 5. 退出
echo.
set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" (
    echo.
    echo 启动GUI版本...
    python chess_gui.py
) else if "%choice%"=="2" (
    echo.
    echo 启动命令行版本...
    python chess_assistant.py
) else if "%choice%"=="3" (
    echo.
    echo 配置引擎...
    python download_engine.py
) else if "%choice%"=="4" (
    echo.
    echo 安装依赖...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    echo 安装完成！
    pause
) else if "%choice%"=="5" (
    exit
) else (
    echo.
    echo 无效选项！
    pause
)

pause

