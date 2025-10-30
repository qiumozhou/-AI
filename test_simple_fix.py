#!/usr/bin/env python3
"""
测试引擎分析修复
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def test_engine_variations():
    """测试引擎对不同棋局的分析"""
    print("测试引擎分析修复")
    print("=" * 50)
    
    try:
        from chess_assistant import ChineseChessAssistant
        
        print("1. 初始化引擎...")
        assistant = ChineseChessAssistant()
        
        if not assistant.engine_path:
            print("x 引擎未就绪")
            return
        
        print("+ 引擎初始化成功")
        
        # 测试3个明显不同的棋局
        test_cases = [
            # 标准开局
            "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1",
            # 兵卒对进
            "rnbakabnr/9/1c5c1/p1p3p1p/6p2/2P6/P3P1P1P/1C5C1/9/RNBAKABNR w - - 0 1",
            # 马跳局面  
            "r1bakabnr/9/1cn4c1/p1p1p1p1p/9/9/P1P1P1P1P/1C1N2C2/9/R1BAKABNR w - - 0 1"
        ]
        
        print(f"\n2. 测试不同棋局...")
        
        results = []
        for i, fen in enumerate(test_cases):
            print(f"\n--- 测试 {i+1} ---")
            
            # 使用深度4进行快速测试
            both_moves = assistant.analyze_both_sides(fen, depth=4)
            
            red_move = both_moves.get('red', 'ERROR')
            black_move = both_moves.get('black', 'ERROR')
            
            results.append((red_move, black_move))
            print(f"红方: {red_move}, 黑方: {black_move}")
        
        print(f"\n3. 结果分析...")
        print("-" * 30)
        
        # 检查是否有变化
        red_moves = [r[0] for r in results]
        black_moves = [r[1] for r in results]
        
        red_unique = len(set(red_moves))
        black_unique = len(set(black_moves))
        
        print(f"红方走法种类: {red_unique}/{len(red_moves)}")
        print(f"黑方走法种类: {black_unique}/{len(black_moves)}")
        
        if red_unique > 1 or black_unique > 1:
            print("\n+ 修复成功！引擎能给出不同走法")
        else:
            print(f"\n- 仍有问题，所有走法相同：")
            print(f"  红方总是: {red_moves[0]}")
            print(f"  黑方总是: {black_moves[0]}")
        
        print(f"\n详细结果:")
        for i, (red, black) in enumerate(results, 1):
            print(f"  棋局{i}: 红{red} 黑{black}")
            
    except Exception as e:
        print(f"x 测试失败: {e}")

if __name__ == "__main__":
    test_engine_variations()














