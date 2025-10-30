#!/usr/bin/env python3
"""
测试修复后的完整输出
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def test_complete_output():
    """测试修复后的完整输出"""
    print("🎯 测试修复后的完整引擎输出")
    print("=" * 60)
    
    try:
        from chess_assistant import ChineseChessAssistant
        
        assistant = ChineseChessAssistant()
        
        if not assistant.engine_path:
            print("❌ 引擎未就绪")
            return
        
        print("✅ 引擎初始化成功")
        
        # 用户的测试FEN
        test_fen = "5a3/3ka4/5n3/9/9/9/9/9/9/4K1R2 w"
        
        print(f"\n测试FEN: {test_fen}")
        print(f"用户直接调用得到: b2e2 (炮二平五)")
        print(f"分析深度: 6")
        print(f"期望获得: 6行info depth分析 + bestmove")
        
        print(f"\n开始分析...")
        print("=" * 50)
        
        # 使用修复后的程序
        result = assistant.analyze_position(test_fen, 'w', 6)
        
        print("=" * 50)
        print(f"\n📊 最终结果: {result}")
        
        if result == 'b2e2':
            print("🎉 完美匹配用户结果！")
        elif result and result != 'a3a4':
            print(f"🔍 不同走法，但至少不是固定的a3a4了")
        else:
            print(f"🤔 仍需调试")
        
        # 获取中文描述
        if result and result not in ['未找到最佳走法', '引擎错误', '分析超时']:
            try:
                desc = assistant.format_move(result, test_fen)
                print(f"📝 中文描述: {desc}")
            except:
                print("📝 中文描述获取失败")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_output()





