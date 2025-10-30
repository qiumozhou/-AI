#!/usr/bin/env python3
"""
简单的引擎测试工具
"""

import subprocess
import sys
from pathlib import Path

def test_engine():
    """测试引擎是否正常工作"""
    print("=" * 50)
    print("Pikafish引擎简单测试")
    print("=" * 50)
    
    engine_path = "engine/pikafish.exe"
    
    if not Path(engine_path).exists():
        print("✗ 引擎文件不存在")
        return False
    
    if not Path("engine/pikafish.nnue").exists():
        print("✗ NNUE文件不存在")
        return False
    
    try:
        # 准备测试FEN
        test_fen = "rnbakab1r/9/1c4nc1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR w - - 0 1"
        
        print("测试FEN:", test_fen)
        print()
        print("引擎输出:")
        print("-" * 30)
        
        # 启动引擎
        process = subprocess.Popen(
            [engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="engine",  # 设置工作目录
            creationflags=0x08000000 if sys.platform == 'win32' else 0
        )
        
        # 发送命令，包括设置NNUE文件路径
        nnue_path = Path("engine/pikafish.nnue").absolute()
        commands = f"""uci
isready
setoption name EvalFile value {nnue_path}
position fen {test_fen}
go depth 6
quit
"""
        
        stdout, stderr = process.communicate(input=commands.encode(), timeout=20)
        
        output = stdout.decode('utf-8', errors='ignore')
        print("标准输出:")
        print(output)
        
        if stderr:
            error_output = stderr.decode('utf-8', errors='ignore')
            if error_output.strip():
                print("\n错误输出:")
                print(error_output)
        
        print("-" * 30)
        
        # 查找最佳走法
        lines = output.split('\n')
        bestmove_found = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('bestmove'):
                print(f"✓ 找到最佳走法: {line}")
                bestmove_found = True
                parts = line.split()
                if len(parts) >= 2:
                    move = parts[1]
                    print(f"✓ 解析结果: {move}")
                    return True
        
        if not bestmove_found:
            print("✗ 输出中未找到 'bestmove' 行")
            
        return bestmove_found
        
    except subprocess.TimeoutExpired:
        print("✗ 引擎响应超时")
        process.kill()
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    if test_engine():
        print("\n✅ 引擎测试成功！")
    else:
        print("\n❌ 引擎测试失败")
