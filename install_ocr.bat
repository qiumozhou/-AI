@echo off
chcp 65001 >nul
echo ====================================
echo 安装PaddleOCR识别模块
echo ====================================
echo.
echo 这将安装OCR识别功能，无需训练模型即可识别棋子！
echo.
pause

echo.
echo 正在安装PaddleOCR...
echo.

pip install paddleocr paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple

if %errorlevel% neq 0 (
    echo.
    echo 安装失败！尝试不使用镜像源...
    pip install paddleocr paddlepaddle
)

echo.
echo ====================================
echo 安装完成！
echo ====================================
echo.
echo 现在可以使用OCR自动识别棋子了！
echo 运行程序: python chess_gui.py
echo.
pause

