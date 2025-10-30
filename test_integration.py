"""
测试深度学习识别集成到主程序
"""

import sys
import cv2
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

from chess_assistant import ChineseChessAssistant

def test_integrated_recognition():
    """测试集成后的识别功能"""
    print("="*60)
    print("测试主程序集成 - 深度学习识别")
    print("="*60)
    print()
    
    # 初始化助手（会自动加载所有识别器）
    assistant = ChineseChessAssistant()
    
    print("\n" + "="*60)
    print("测试图片识别")
    print("="*60)
    
    # 测试图片
    test_image = "images/1.png"
    if not Path(test_image).exists():
        print(f"✗ 测试图片不存在: {test_image}")
        return
    
    # 读取图片
    image = cv2.imread(test_image)
    print(f"\n图片: {test_image}")
    print(f"尺寸: {image.shape[1]}x{image.shape[0]}")
    
    # 使用主程序的识别方法
    print("\n" + "-"*60)
    print("开始识别...")
    print("-"*60)
    fen = assistant.recognize_pieces(image)
    
    # 显示结果
    print("\n" + "="*60)
    print("识别结果")
    print("="*60)
    print(f"FEN: {fen}")
    
    # 验证FEN
    if assistant._validate_fen(fen):
        print("✓ FEN验证通过（包含将帅）")
    else:
        print("⚠ FEN可能不完整")
    
    # 显示棋盘
    print("\n棋盘状态:")
    display_board(fen)
    
    # 如果有引擎，尝试分析
    if assistant.engine_path:
        print("\n" + "="*60)
        print("引擎分析")
        print("="*60)
        try:
            best_move = assistant.analyze_position(fen)
            print(f"最佳走法: {best_move}")
            move_desc = assistant.format_move(best_move)
            print(f"走法说明: {move_desc}")
        except Exception as e:
            print(f"分析失败: {e}")


def display_board(fen):
    """显示棋盘"""
    piece_symbols = {
        'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将',
        'c': '炮', 'p': '卒',
        'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅',
        'C': '砲', 'P': '兵'
    }
    
    position = fen.split()[0]
    rows = position.split('/')
    
    print("  " + "─"*27)
    for i, row in enumerate(rows):
        line = f"{i+1:2d}│"
        
        for char in row:
            if char.isdigit():
                line += " · " * int(char)
            else:
                symbol = piece_symbols.get(char, char)
                line += f" {symbol} "
        
        print(line)
    print("  " + "─"*27)


if __name__ == "__main__":
    test_integrated_recognition()

