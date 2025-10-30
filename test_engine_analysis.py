#!/usr/bin/env python3
"""
测试引擎对奇怪FEN的分析结果
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def test_engine_analysis():
    """测试引擎分析"""
    print("🔍 测试引擎分析不同FEN")
    print("=" * 50)
    
    try:
        from chess_assistant import ChineseChessAssistant
        
        print("1. 初始化引擎...")
        assistant = ChineseChessAssistant()
        
        if not assistant.engine_path:
            print("✗ 引擎未就绪")
            return
        
        print("✓ 引擎初始化成功")
        
        # 测试不同的FEN
        test_fens = [
            # 标准开局
            "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1",
            # 测试中发现的FEN
            "4k4/9/9/9/9/9/8P/9/9/4k4 w - - 0 1",
            "4k4/9/9/9/9/9/9/9/9/4k4 w - - 0 1",
            # 只有将帅的FEN
            "4k4/9/9/9/9/9/9/9/9/4K4 w - - 0 1"
        ]
        
        fen_names = [
            "标准开局",
            "测试FEN1", 
            "测试FEN2",
            "只有将帅"
        ]
        
        print(f"\n2. 测试 {len(test_fens)} 个不同FEN的引擎分析...")
        
        for i, (fen, name) in enumerate(zip(test_fens, fen_names)):
            print(f"\n--- {name} ---")
            print(f"FEN: {fen}")
            
            try:
                both_moves = assistant.analyze_both_sides(fen)
                red_move = both_moves.get('red', '未找到')
                black_move = both_moves.get('black', '未找到')
                
                print(f"🔴 红方走法: {red_move}")
                print(f"⚫ 黑方走法: {black_move}")
                
                # 检查是否总是返回 a3a4 和 a6a5
                if red_move == "a3a4" and black_move == "a6a5":
                    print("⚠️ 警告：返回了固定的走法！")
                elif red_move == "a3a4" or black_move == "a6a5":
                    print("⚠️ 部分走法是固定的")
                else:
                    print("✓ 走法正常变化")
                    
            except Exception as e:
                print(f"✗ 分析出错: {e}")
        
        print(f"\n3. 结论...")
        print("如果所有FEN都返回相同的走法，说明：")
        print("1. 引擎可能对无效/简单的FEN总是返回默认走法")
        print("2. 识别器识别出的FEN可能都是无效或过于简单的")
        print("3. 需要改善识别器的准确性或添加FEN验证")
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine_analysis()

















