#!/usr/bin/env python3
"""
简单的Pikafish测试脚本
只调用用户指定的两个命令，打印所有输出
"""

import subprocess
import sys
from pathlib import Path
import time

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    CREATE_NO_WINDOW = 0x08000000

def test_simple_pikafish_call():
    """调用用户指定的命令并显示所有输出"""
    print("🎯 Pikafish引擎简单测试")
    print("=" * 50)
    
    engine_path = Path("D:/chess/engine/pikafish.exe")
    engine_dir = engine_path.parent
    
    if not engine_path.exists():
        print(f"❌ 引擎文件不存在: {engine_path}")
        return
    
    print(f"引擎路径: {engine_path}")
    print(f"工作目录: {engine_dir}")
    
    try:
        # 启动引擎进程
        startupinfo = None
        creationflags = 0
        
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            creationflags = CREATE_NO_WINDOW
        
        process = subprocess.Popen(
            [str(engine_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore',
            bufsize=0,  # 无缓冲，立即输出
            cwd=str(engine_dir),
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        
        # 等待引擎启动
        time.sleep(0.1)
        
        # 用户指定的命令
        commands = [
            "position 5a3/3ka4/5n3/9/9/9/9/9/9/4K1R2 w",
            "go depth 6",
            "quit"
        ]
        
        print(f"\n📤 发送命令:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd}")
        
        # 将命令组合成输入
        input_text = '\n'.join(commands) + '\n'
        
        print(f"\n📥 Pikafish引擎输出:")
        print("=" * 60)
        
        # 发送命令并获取输出（增加超时时间，确保获取完整分析）
        stdout, stderr = process.communicate(input=input_text, timeout=60)
        
        # 打印完整输出
        if stdout:
            print(stdout)
        else:
            print("(无输出)")
        
        if stderr:
            print(f"\n❌ 错误输出:")
            print(stderr)
        
        print("=" * 60)
        
        # 解析关键信息
        lines = stdout.split('\n') if stdout else []
        
        info_lines = []
        best_move = None
        ponder_move = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('info'):
                info_lines.append(line)
            elif line.startswith('bestmove'):
                parts = line.split()
                best_move = parts[1] if len(parts) >= 2 else None
                if 'ponder' in line:
                    ponder_idx = parts.index('ponder')
                    ponder_move = parts[ponder_idx + 1] if ponder_idx + 1 < len(parts) else None
        
        # 汇总分析
        print(f"\n📊 输出分析:")
        print(f"  总输出行数: {len(lines)}")
        print(f"  info行数: {len(info_lines)}")
        print(f"  最佳走法: {best_move}")
        if ponder_move:
            print(f"  预期对手走法: {ponder_move}")
        
        # 显示分析过程
        if info_lines:
            print(f"\n📋 分析过程 ({len(info_lines)}行):")
            for i, line in enumerate(info_lines, 1):
                print(f"  {i:2d}. {line}")
        else:
            print(f"\n⚠️ 没有找到分析过程信息")
        
        # 与用户结果对比
        print(f"\n🎯 与用户结果对比:")
        print(f"  用户报告: f0f5 (有详细info分析)")
        print(f"  我们得到: {best_move} ({len(info_lines)}行分析)")
        
        if best_move == 'f0f5':
            print("✅ 完全匹配！")
        elif best_move and best_move.startswith('f'):
            print("🔍 接近！同样是f列的走法")
        elif best_move:
            print("🤔 不同的走法，但至少不是a3a4了")
        else:
            print("❌ 没有得到有效走法")
            
        # 检查是否有详细分析
        if len(info_lines) >= 6:
            print("✅ 获得了详细的分析过程")
        elif len(info_lines) > 0:
            print("🔍 获得了部分分析信息")
        else:
            print("⚠️ 没有获得分析过程，可能有问题")
        
    except subprocess.TimeoutExpired:
        print("⏰ 引擎响应超时")
        try:
            process.kill()
        except:
            pass
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_pikafish_call()

