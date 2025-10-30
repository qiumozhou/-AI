#!/usr/bin/env python3
"""
测试不同的引擎初始化状态
"""

import subprocess
import sys
from pathlib import Path
import time

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def test_initialization_states():
    """测试不同的引擎初始化状态"""
    print("🔍 测试引擎初始化状态对输出的影响")
    print("=" * 60)
    
    engine_path = Path("D:/chess/engine/pikafish.exe")
    engine_dir = engine_path.parent
    
    test_fen = "5a3/3ka4/5n3/9/9/9/9/9/9/4K1R2 w"
    
    scenarios = [
        {
            "name": "场景1: 直接调用（无初始化）",
            "commands": [
                f"position {test_fen}",
                "go depth 6",
                "quit"
            ]
        },
        {
            "name": "场景2: 预初始化引擎",
            "commands": [
                "uci",
                "isready",
                f"position {test_fen}",
                "go depth 6", 
                "quit"
            ]
        },
        {
            "name": "场景3: 完整初始化",
            "commands": [
                "uci",
                "isready",
                "ucinewgame",
                f"position {test_fen}",
                "go depth 6",
                "quit"
            ]
        },
        {
            "name": "场景4: 用户的2线程设置",
            "commands": [
                "uci",
                "setoption name Threads value 2",
                "isready", 
                f"position {test_fen}",
                "go depth 6",
                "quit"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        try:
            process = subprocess.run(
                [str(engine_path)],
                input='\n'.join(scenario['commands']) + '\n',
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(engine_dir)
            )
            
            print("发送命令:")
            for i, cmd in enumerate(scenario['commands'], 1):
                print(f"  {i}. {cmd}")
            
            if process.stdout:
                lines = process.stdout.split('\n')
                
                # 统计不同类型的行
                startup_lines = [line for line in lines if 'Pikafish' in line or 'id name' in line]
                info_lines = [line for line in lines if line.strip().startswith('info')]
                info_depth_lines = [line for line in lines if line.strip().startswith('info depth')]
                bestmove_lines = [line for line in lines if line.strip().startswith('bestmove')]
                
                print(f"\n📊 输出统计:")
                print(f"  总行数: {len(lines)}")
                print(f"  启动信息: {len(startup_lines)} 行")
                print(f"  info行: {len(info_lines)} 行")
                print(f"  info depth行: {len(info_depth_lines)} 行")
                print(f"  bestmove行: {len(bestmove_lines)} 行")
                
                if bestmove_lines:
                    final_move = bestmove_lines[-1].strip().split()[1] if len(bestmove_lines[-1].strip().split()) > 1 else 'NONE'
                    print(f"  最佳走法: {final_move}")
                    
                    if final_move == 'b2e2':
                        print("🎯 匹配用户结果！")
                
                # 显示详细分析（如果有）
                if info_depth_lines:
                    print(f"\n📋 分析过程:")
                    for line in info_depth_lines:
                        print(f"  {line.strip()}")
                else:
                    print(f"\n⚠️ 没有详细分析过程")
                
                # 如果输出很短，显示完整内容
                if len(lines) <= 10:
                    print(f"\n📄 完整输出:")
                    for i, line in enumerate(lines, 1):
                        if line.strip():
                            print(f"  {i}. {line.strip()}")
            
        except subprocess.TimeoutExpired:
            print("⏰ 超时")
        except Exception as e:
            print(f"❌ 失败: {e}")

def test_manual_simulation():
    """手动模拟用户的操作步骤"""
    print(f"\n🎯 手动模拟用户操作")
    print("=" * 40)
    
    engine_path = Path("D:/chess/engine/pikafish.exe")
    engine_dir = engine_path.parent
    
    print("这个测试将启动一个持续的引擎进程")
    print("您可以手动发送命令来对比结果")
    print("(5秒后自动退出)")
    
    try:
        process = subprocess.Popen(
            [str(engine_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(engine_dir)
        )
        
        # 发送用户的命令
        commands = "position 5a3/3ka4/5n3/9/9/9/9/9/9/4K1R2 w\ngo depth 6\nquit\n"
        
        print(f"发送命令:")
        print(f"  position 5a3/3ka4/5n3/9/9/9/9/9/9/4K1R2 w") 
        print(f"  go depth 6")
        print(f"  quit")
        print()
        
        stdout, stderr = process.communicate(input=commands, timeout=30)
        
        print(f"📥 引擎输出:")
        print("=" * 50)
        if stdout:
            print(stdout)
        print("=" * 50)
        
        if stderr:
            print(f"\n❌ 错误:")
            print(stderr)
        
        # 检查是否包含用户报告的特征
        if stdout:
            has_depth_info = 'info depth' in stdout
            has_b2e2 = 'b2e2' in stdout
            has_detailed_analysis = stdout.count('info depth') >= 5
            
            print(f"\n🔍 特征检查:")
            print(f"  包含info depth: {has_depth_info}")
            print(f"  包含b2e2: {has_b2e2}")
            print(f"  详细分析(≥5行): {has_detailed_analysis}")
            
            if has_b2e2 and has_detailed_analysis:
                print("🎉 完美匹配用户的输出特征！")
            elif has_depth_info:
                print("🔍 部分匹配，有分析信息")
            else:
                print("❌ 输出特征不匹配")
    
    except Exception as e:
        print(f"❌ 手动模拟失败: {e}")

if __name__ == "__main__":
    test_initialization_states()
    test_manual_simulation()





