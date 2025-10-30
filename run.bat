@echo off
chcp 65001 >nul
title 中国象棋识别助手

echo ==========================================
echo     中国象棋识别助手 - 图形界面版
echo ==========================================
echo.

REM 检查Python环境
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ✗ 未找到Python，请先安装Python 3.8+
    echo.
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查虚拟环境
if exist ".venv\Scripts\python.exe" (
    echo ✓ 使用虚拟环境
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo ⚠ 未找到虚拟环境，使用系统Python
    set PYTHON_CMD=python
)

REM 检查必要文件
if not exist "chess_gui.py" (
    echo ✗ 未找到程序文件 chess_gui.py
    pause
    exit /b 1
)

if not exist "models\cchess_recognition\rtmpose-t-cchess_4.onnx" (
    echo ⚠ 未找到ONNX模型文件
    echo 正在下载模型...
    %PYTHON_CMD% download_nnue.py
    if %errorlevel% neq 0 (
        echo ✗ 模型下载失败，请手动运行: python download_nnue.py
        pause
        exit /b 1
    )
)

if not exist "engine\pikafish.nnue" (
    echo ⚠ 未找到引擎评估文件
    echo 正在下载引擎文件...
    %PYTHON_CMD% download_nnue.py
    if %errorlevel% neq 0 (
        echo ✗ 引擎文件下载失败
        pause
        exit /b 1
    )
)

echo ✓ 环境检查完成，正在启动图形界面...
echo.

REM 启动GUI程序
%PYTHON_CMD% chess_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ✗ 程序运行出错
    echo.
    echo 如果是首次运行，请先安装依赖:
    echo   pip install -r requirements.txt
    echo.
    echo 如果问题持续存在，请检查:
    echo 1. Python版本是否为 3.8+
    echo 2. 是否正确安装了所有依赖
    echo 3. ONNX模型文件是否完整下载
    echo.
    pause
)