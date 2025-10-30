"""
中国象棋棋盘识别 - 统一入口
支持两种识别方式：深度学习 和 OCR
"""

import sys
import cv2
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


def display_board_from_fen(fen):
    """从FEN显示棋盘"""
    
    piece_symbols = {
        'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将',
        'c': '炮', 'p': '卒',
        'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅',
        'C': '砲', 'P': '兵'
    }
    
    # 解析FEN
    position = fen.split()[0]
    rows = position.split('/')
    
    print("\n" + "="*60)
    print("棋盘状态")
    print("="*60)
    print("  " + "─"*27)
    for i, row in enumerate(rows):
        line = f"{i+1:2d}│"
        
        for char in row:
            if char.isdigit():
                # 数字表示空格数量
                line += " · " * int(char)
            else:
                # 棋子
                symbol = piece_symbols.get(char, char)
                line += f" {symbol} "
        
        print(line)
    print("  " + "─"*27)
    print()


def recognize_with_deep_learning(image_path):
    """使用深度学习方案识别"""
    try:
        from cchess_deep_recognizer import CChessDeepRecognizer
        
        print("\n使用方案: 深度学习识别（推荐）")
        print("="*60)
        
        recognizer = CChessDeepRecognizer()
        
        if recognizer.pose_model is None:
            print("⚠ 模型未加载，切换到OCR方案")
            return None
        
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"✗ 无法读取图片: {image_path}")
            return None
        
        # 识别
        fen = recognizer.recognize(image)
        
        return fen
        
    except Exception as e:
        print(f"✗ 深度学习识别失败: {e}")
        return None


def recognize_with_ocr(image_path):
    """使用OCR方案识别"""
    try:
        from universal_chess_detector import UniversalChessDetector
        
        print("\n使用方案: OCR识别")
        print("="*60)
        
        detector = UniversalChessDetector(debug=False)
        
        if not detector.ocr:
            print("✗ OCR未初始化")
            return None
        
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"✗ 无法读取图片: {image_path}")
            return None
        
        print(f"图片尺寸: {image.shape[1]}x{image.shape[0]}")
        
        # 识别
        fen = detector.recognize_from_image(image)
        
        return fen
        
    except Exception as e:
        print(f"✗ OCR识别失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='中国象棋棋盘识别')
    parser.add_argument('image', help='输入图片路径')
    parser.add_argument('--method', choices=['deep', 'ocr', 'auto'], default='auto',
                        help='识别方法: deep(深度学习), ocr(OCR), auto(自动选择，默认)')
    parser.add_argument('--analyze', action='store_true', help='识别后进行引擎分析')
    
    args = parser.parse_args()
    
    image_path = args.image
    
    # 检查图片是否存在
    if not Path(image_path).exists():
        print(f"✗ 图片不存在: {image_path}")
        return
    
    print("="*60)
    print("中国象棋棋盘识别")
    print("="*60)
    print(f"输入图片: {image_path}")
    
    fen = None
    
    # 根据选择的方法进行识别
    if args.method == 'deep':
        fen = recognize_with_deep_learning(image_path)
    elif args.method == 'ocr':
        fen = recognize_with_ocr(image_path)
    else:  # auto
        # 先尝试深度学习，失败则用OCR
        print("\n智能识别模式：优先使用深度学习")
        fen = recognize_with_deep_learning(image_path)
        
        if fen is None:
            print("\n深度学习识别失败，切换到OCR方案...")
            fen = recognize_with_ocr(image_path)
    
    # 显示结果
    if fen:
        print("\n" + "="*60)
        print("✓ 识别成功！")
        print("="*60)
        print(f"\nFEN: {fen}")
        
        # 显示棋盘
        display_board_from_fen(fen)
        
        # 如果需要分析
        if args.analyze:
            try:
                from chess_assistant import ChineseChessAssistant
                
                print("="*60)
                print("引擎分析")
                print("="*60)
                
                assistant = ChineseChessAssistant()
                if assistant.engine_path:
                    print("正在分析...")
                    best_move = assistant.analyze_position(fen)
                    print(f"\n最佳走法: {best_move}")
                    print(f"走法说明: {assistant.format_move(best_move)}")
                else:
                    print("⚠ 引擎未安装")
                    
            except Exception as e:
                print(f"✗ 分析失败: {e}")
    else:
        print("\n" + "="*60)
        print("✗ 识别失败")
        print("="*60)
        print("\n可能的原因:")
        print("1. 图片中没有清晰的棋盘")
        print("2. 棋子不清晰或摆放不正")
        print("3. 模型未下载或加载失败")
        print("\n建议:")
        print("- 确保图片清晰")
        print("- 尝试不同的识别方法: --method ocr 或 --method deep")
        print("- 查看 RECOGNITION_GUIDE.md 了解详情")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 没有参数，显示帮助
        print("="*60)
        print("中国象棋棋盘识别")
        print("="*60)
        print("\n用法:")
        print("  python recognize_board.py <图片路径> [选项]")
        print("\n示例:")
        print("  python recognize_board.py images/1.png")
        print("  python recognize_board.py images/1.png --method deep")
        print("  python recognize_board.py images/1.png --method ocr")
        print("  python recognize_board.py images/1.png --analyze")
        print("\n选项:")
        print("  --method deep/ocr/auto  选择识别方法（默认auto）")
        print("  --analyze               识别后进行引擎分析")
        print("\n" + "="*60)
    else:
        main()

