"""
测试识别图片中的棋局
"""

import cv2
import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 导入识别器
try:
    from universal_chess_detector import UniversalChessDetector
    detector = UniversalChessDetector()
    print("[OK] OCR检测器加载成功")
except Exception as e:
    print(f"[FAIL] OCR检测器加载失败: {e}")
    print("请安装: pip install paddleocr")
    detector = None

def recognize_image(image_path):
    """识别图片中的棋局"""
    
    print(f"\n{'='*60}")
    print(f"识别图片: {image_path}")
    print('='*60)
    
    # 读取图片
    if not Path(image_path).exists():
        print(f"[FAIL] 图片不存在: {image_path}")
        return None
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"[FAIL] 无法读取图片: {image_path}")
        return None
    
    print(f"[OK] 图片读取成功，尺寸: {image.shape[1]}x{image.shape[0]}")
    
    # 使用OCR识别
    if detector and detector.ocr:
        print("\n使用OCR识别棋子...")
        fen = detector.recognize_from_image(image)
        
        if fen:
            print(f"\n{'='*60}")
            print("识别结果")
            print('='*60)
            print(f"FEN: {fen}")
            
            # 显示棋盘
            print("\n棋盘状态:")
            display_board_from_fen(fen)
            return fen
        else:
            print("[FAIL] OCR识别失败")
    else:
        print("[FAIL] OCR未初始化")
        print("请运行: pip install paddleocr")
    
    return None

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

def main():
    """主函数"""
    
    # 测试图片
    image_path = "images/1.png"
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    fen = recognize_image(image_path)
    
    if fen:
        print(f"\n{'='*60}")
        print("[SUCCESS] 识别成功！")
        print('='*60)
        print(f"\n可以使用此FEN进行分析:")
        print(f"  {fen}")
        
        # 如果有引擎，可以分析
        try:
            from chess_assistant import ChineseChessAssistant
            assistant = ChineseChessAssistant()
            
            if assistant.engine_path:
                print(f"\n{'='*60}")
                print("引擎分析")
                print('='*60)
                print("正在分析...")
                
                best_move = assistant.analyze_position(fen)
                print(f"\n最佳走法: {best_move}")
                print(f"走法说明: {assistant.format_move(best_move)}")
        except Exception as e:
            pass
    else:
        print(f"\n{'='*60}")
        print("[FAIL] 识别失败")
        print('='*60)
        print("\n可能的原因:")
        print("1. OCR未安装: pip install paddleocr")
        print("2. 图片中没有清晰的棋盘")
        print("3. 棋子上的汉字不清晰")
        
        print("\n建议:")
        print("- 确保图片中棋盘清晰可见")
        print("- 棋子上的汉字清晰")
        print("- 尝试手动FEN输入（100%准确）")

if __name__ == "__main__":
    main()

