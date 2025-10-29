@echo off
chcp 65001 >nul
echo ====================================
echo 中国象棋助手 - 一键打包工具
echo ====================================
echo.

REM 清理旧文件
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "发行版" rmdir /s /q "发行版"

echo 正在打包GUI版本...
echo.

pyinstaller --name=中国象棋助手 --onefile --windowed --icon=NONE --add-data=README.md;. --add-data=USAGE.md;. --add-data=QUICK_REFERENCE.md;. --hidden-import=PIL._tkinter_finder --collect-all=cv2 --collect-all=numpy --noconfirm chess_gui.py

if %errorlevel% neq 0 (
    echo.
    echo 打包失败！请检查错误信息。
    pause
    exit /b 1
)

echo.
echo 创建发行包...
echo.

REM 创建发行版目录
mkdir "发行版"
mkdir "发行版\engine"

REM 复制exe文件
copy "dist\中国象棋助手.exe" "发行版\"

REM 复制引擎（如果存在）
if exist "engine\pikafish.exe" (
    copy "engine\pikafish.exe" "发行版\engine\"
    echo 已复制引擎文件
) else (
    echo 引擎文件不存在，请手动下载到 发行版\engine\ 目录
)

REM 复制文档
copy "README.md" "发行版\" >nul
copy "START_HERE.md" "发行版\" >nul
copy "USAGE.md" "发行版\" >nul
copy "QUICK_REFERENCE.md" "发行版\" >nul
copy "LICENSE" "发行版\" >nul

REM 创建使用说明
echo 中国象棋助手 v1.0.0 使用说明 > "发行版\使用说明.txt"
echo ================================ >> "发行版\使用说明.txt"
echo. >> "发行版\使用说明.txt"
echo 快速开始 >> "发行版\使用说明.txt"
echo -------- >> "发行版\使用说明.txt"
echo 1. 如果engine目录下没有pikafish.exe，请下载： >> "发行版\使用说明.txt"
echo    https://github.com/official-pikafish/Pikafish/releases >> "发行版\使用说明.txt"
echo. >> "发行版\使用说明.txt"
echo 2. 双击"中国象棋助手.exe"启动程序 >> "发行版\使用说明.txt"
echo. >> "发行版\使用说明.txt"
echo 3. 打开象棋对弈界面，按Ctrl+S开始分析 >> "发行版\使用说明.txt"
echo. >> "发行版\使用说明.txt"
echo 快捷键 >> "发行版\使用说明.txt"
echo ------ >> "发行版\使用说明.txt"
echo Ctrl + S : 开始/停止分析 >> "发行版\使用说明.txt"
echo Ctrl + Q : 退出程序 >> "发行版\使用说明.txt"
echo. >> "发行版\使用说明.txt"
echo 详细文档请查看其他.md文件 >> "发行版\使用说明.txt"

echo.
echo ====================================
echo 打包成功！
echo ====================================
echo.
echo 发行包位置: 发行版\
echo 可执行文件: 发行版\中国象棋助手.exe
echo.
if not exist "发行版\engine\pikafish.exe" (
    echo [重要] 请下载Pikafish引擎到 发行版\engine\ 目录
    echo 下载地址: https://github.com/official-pikafish/Pikafish/releases
)
echo.
pause

