#!/usr/bin/env python3
"""
最终测试：验证引擎分析修复
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def display_board_from_fen(fen, title="棋局"):
    """从FEN字符串显示棋盘"""
    print(f"\n📋 {title}")
    print("=" * 50)
    
    # 解析FEN
    fen_parts = fen.split()
    position = fen_parts[0] if fen_parts else fen
    side_to_move = fen_parts[1] if len(fen_parts) > 1 else 'w'
    
    # 棋子映射（Unicode象棋符号）
    piece_symbols = {
        'K': '帅', 'k': '将',  # 王/将
        'A': '仕', 'a': '士',  # 士
        'B': '相', 'b': '象',  # 象/相  
        'N': '马', 'n': '马',  # 马
        'R': '车', 'r': '车',  # 车
        'C': '炮', 'c': '炮',  # 炮
        'P': '兵', 'p': '卒'   # 兵/卒
    }
    
    # 解析棋盘位置
    rows = position.split('/')
    board = []
    
    for row_str in rows:
        row = []
        for char in row_str:
            if char.isdigit():
                # 数字表示连续的空格
                row.extend([' '] * int(char))
            else:
                # 棋子
                symbol = piece_symbols.get(char, char)
                # 红方用红色标记，黑方用普通显示
                if char.isupper():  # 红方
                    row.append(f'\033[91m{symbol}\033[0m')  # 红色
                else:  # 黑方
                    row.append(f'\033[94m{symbol}\033[0m')  # 蓝色
        board.append(row)
    
    # 显示棋盘
    print("    a b c d e f g h i")
    print("  ┌─────────────────────┐")
    
    for i, row in enumerate(board):
        row_num = i
        print(f"{row_num} │ ", end="")
        for j, piece in enumerate(row):
            print(f"{piece} ", end="")
        print("│")
        
        # 在第4行和第5行之间画河界
        if i == 4:
            print("  ├─────────────────────┤")
            print("  │     楚河    汉界     │")
            print("  ├─────────────────────┤")
    
    print("  └─────────────────────┘")
    
    # 显示当前走棋方
    side_name = "🔴 红方(帅)" if side_to_move == 'w' else "⚫ 黑方(将)"
    print(f"\n当前走棋: {side_name}")
    
    # 统计棋子
    red_pieces = sum(1 for char in position if char.isupper())
    black_pieces = sum(1 for char in position if char.islower())
    print(f"棋子统计: 红方 {red_pieces} 子, 黑方 {black_pieces} 子")
    print(f"完整FEN: {fen}")
    print("=" * 50)

def test_engine_fix():
    """测试引擎分析修复"""
    print("🔧 最终测试：验证引擎分析修复")
    print("=" * 60)
    
    try:
        from chess_assistant import ChineseChessAssistant
        
        print("1. 初始化引擎...")
        assistant = ChineseChessAssistant()
        
        if not assistant.engine_path:
            print("✗ 引擎未就绪")
            return
        
        print("✓ 引擎初始化成功")
        
        # 测试不同的棋局，确保引擎能给出不同的走法
        test_cases = [
            # {
            #     "name": "标准开局",
            #     "fen": "3akab2/2R3Cc1/2n2r3/p2nC3p/2p3pc1/9/P1P1P1P1P/2N5N/9/2BAKAB2 w"
            # },
            {
                "name": "22222", 
                "fen": "5a3/3ka4/5n3/9/9/9/9/9/9/4K1R2 w"
            },
            # {
            #     "name": "中局复杂",
            #     "fen": "r1bakab2/4a4/2n1c1n2/p1p2cp1p/4r4/6P2/P1P2C2P/2N2N3/4A4/2BAKAB2 w - - 0 32"
            # }
        ]
        
        print(f"\n2. 测试 {len(test_cases)} 个不同棋局（深度6）...")
        
        results = []
        for test_case in test_cases:
            print(f"\n--- {test_case['name']} ---")
            fen = test_case['fen']
            
            # 显示棋局
            display_board_from_fen(fen, f"{test_case['name']} - 棋局显示")
            
            try:
                # 使用深度6进行快速分析
                both_moves = assistant.analyze_both_sides(fen, depth=6)
                
                red_move = both_moves.get('red', '未找到')
                black_move = both_moves.get('black', '未找到')
                
                # 获取中文走法描述
                red_desc = assistant.format_move(red_move, fen) if red_move != '未找到' else '未找到'
                black_desc = assistant.format_move(black_move, fen) if black_move != '未找到' else '未找到'
                
                results.append({
                    'name': test_case['name'],
                    'red': red_move,
                    'black': black_move,
                    'red_desc': red_desc,
                    'black_desc': black_desc
                })
                
                print(f"\n🎯 引擎分析结果:")
                print(f"  🔴 红方最佳: {red_move} ({red_desc})")
                print(f"  ⚫ 黑方最佳: {black_move} ({black_desc})")
                
            except Exception as e:
                print(f"✗ 分析出错: {e}")
                results.append({
                    'name': test_case['name'],
                    'red': f"错误: {e}",
                    'black': f"错误: {e}",
                    'red_desc': '分析失败',
                    'black_desc': '分析失败'
                })
        
        print(f"\n3. 分析结果汇总...")
        print("=" * 60)
        
        # 检查结果多样性
        red_moves = [r['red'] for r in results if not r['red'].startswith('错误')]
        black_moves = [r['black'] for r in results if not r['black'].startswith('错误')]
        
        print("红方走法:")
        for i, move in enumerate(red_moves):
            print(f"  {i+1}. {move}")
        
        print("黑方走法:")
        for i, move in enumerate(black_moves):
            print(f"  {i+1}. {move}")
        
        # 检查多样性
        red_unique = len(set(red_moves))
        black_unique = len(set(black_moves))
        
        print(f"\n结果多样性:")
        print(f"  红方: {red_unique}/{len(red_moves)} 种不同走法")
        print(f"  黑方: {black_unique}/{len(black_moves)} 种不同走法")
        
        if red_unique > 1 or black_unique > 1:
            print("✅ 修复成功！引擎能根据不同棋局给出不同走法")
        else:
            print("⚠️ 引擎仍返回相同走法，可能需要进一步调整")
            
        print(f"\n📊 详细对比:")
        print("-" * 80)
        for result in results:
            name = result['name']
            red = result.get('red', '未知')
            black = result.get('black', '未知')
            red_desc = result.get('red_desc', '')
            black_desc = result.get('black_desc', '')
            
            print(f"【{name}】")
            print(f"  🔴 红方: {red:8s} - {red_desc}")
            print(f"  ⚫ 黑方: {black:8s} - {black_desc}")
            print()
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine_fix()







