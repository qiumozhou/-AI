"""
测试Pikafish引擎是否正常工作
"""

import sys
import subprocess
import time
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def test_engine():
    """测试引擎基本功能"""
    print("="*60)
    print("Pikafish引擎测试")
    print("="*60)
    
    # 查找引擎
    engine_path = Path("engine/pikafish.exe")
    
    if not engine_path.exists():
        print(f"✗ 引擎文件不存在: {engine_path.absolute()}")
        return
    
    print(f"✓ 找到引擎: {engine_path.absolute()}")
    print()
    
    # 测试1: 启动引擎
    print("测试1: 启动引擎...")
    try:
        # 尝试使用二进制模式，避免编码问题
        process = subprocess.Popen(
            [str(engine_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0  # 无缓冲
        )
        
        time.sleep(0.5)
        
        if process.poll() is not None:
            stderr_output = process.stderr.read()
            print(f"✗ 引擎启动后立即退出")
            print(f"  退出码: {process.returncode}")
            if stderr_output:
                print(f"  错误信息: {stderr_output}")
            return
        
        print("✓ 引擎启动成功")
    except Exception as e:
        print(f"✗ 引擎启动失败: {e}")
        return
    
    # 测试2: UCI通信
    print("\n测试2: UCI通信...")
    try:
        # 发送UCI命令 (二进制模式)
        process.stdin.write(b"uci\n")
        process.stdin.flush()
        
        # 读取响应（最多5秒）
        uci_output = []
        start_time = time.time()
        
        while time.time() - start_time < 5:
            if process.poll() is not None:
                print("✗ 引擎在UCI通信过程中退出")
                break
            
            line = process.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            try:
                line = line.decode('utf-8', errors='ignore').strip()
            except:
                continue
                
            if line:
                print(f"  引擎: {line}")
                uci_output.append(line)
                
                if "uciok" in line.lower():
                    print("\n✓ UCI通信成功")
                    break
        else:
            print("\n⚠ 未收到uciok响应（可能超时）")
    
    except Exception as e:
        print(f"✗ UCI通信失败: {e}")
        process.terminate()
        return
    
    # 测试3: 分析简单局面
    print("\n测试3: 分析初始局面...")
    try:
        # 使用标准的初始FEN
        test_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
        
        commands = [
            "isready",
            "ucinewgame",
            f"position fen {test_fen}",
            "go depth 5"
        ]
        
        for cmd in commands:
            process.stdin.write(f"{cmd}\n".encode('utf-8'))
            process.stdin.flush()
            print(f"  发送: {cmd}")
            time.sleep(0.1)
        
        # 读取分析结果
        print("\n  等待分析结果...")
        start_time = time.time()
        best_move = None
        
        while time.time() - start_time < 10:
            if process.poll() is not None:
                print("  ✗ 引擎在分析过程中退出")
                break
            
            line = process.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            try:
                line = line.decode('utf-8', errors='ignore').strip()
            except:
                continue
            
            if line.startswith("info"):
                # 简化输出，只显示关键信息
                if "depth" in line:
                    parts = line.split()
                    try:
                        depth_idx = parts.index("depth")
                        depth = parts[depth_idx + 1]
                        print(f"  分析深度: {depth}")
                    except:
                        pass
            
            elif line.startswith("bestmove"):
                best_move = line.split()[1]
                print(f"\n✓ 分析完成")
                print(f"  最佳走法: {best_move}")
                break
        
        if not best_move:
            print("\n⚠ 未找到最佳走法")
    
    except Exception as e:
        print(f"✗ 分析失败: {e}")
    
    finally:
        # 关闭引擎
        try:
            process.stdin.write(b"quit\n")
            process.stdin.flush()
            process.wait(timeout=2)
            print("\n✓ 引擎正常关闭")
        except:
            process.terminate()
            print("\n⚠ 引擎被强制终止")
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


if __name__ == "__main__":
    test_engine()

