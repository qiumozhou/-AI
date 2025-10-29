"""
基础功能测试脚本
"""

import sys
import os
import cv2
import numpy as np
from pathlib import Path

# 设置UTF-8编码以支持中文和特殊字符
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def test_imports():
    """测试依赖包是否正确安装"""
    print("测试依赖包...")
    
    packages = [
        ("PIL", "pillow"),
        ("numpy", "numpy"),
        ("cv2", "opencv-python"),
        ("pyautogui", "pyautogui"),
        ("keyboard", "keyboard"),
    ]
    
    success = True
    for module, package in packages:
        try:
            __import__(module)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [FAIL] {package} - 未安装")
            success = False
    
    return success


def test_screenshot():
    """测试截图功能"""
    print("\n测试截图功能...")
    
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        print(f"  [OK] 截图成功，尺寸: {screenshot.size}")
        
        # 保存测试截图
        screenshot.save("test_screenshot.png")
        print(f"  [OK] 测试截图已保存: test_screenshot.png")
        return True
    except Exception as e:
        print(f"  [FAIL] 截图失败: {str(e)}")
        return False


def test_opencv():
    """测试OpenCV功能"""
    print("\n测试OpenCV...")
    
    try:
        # 创建测试图像
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        test_img[:] = (255, 0, 0)  # 蓝色
        
        cv2.imwrite("test_opencv.png", test_img)
        print("  [OK] OpenCV图像保存成功")
        
        # 读取图像
        read_img = cv2.imread("test_opencv.png")
        if read_img is not None:
            print("  [OK] OpenCV图像读取成功")
            return True
        else:
            print("  [FAIL] OpenCV图像读取失败")
            return False
            
    except Exception as e:
        print(f"  [FAIL] OpenCV测试失败: {str(e)}")
        return False


def test_engine():
    """测试引擎配置"""
    print("\n测试引擎配置...")
    
    engine_dir = Path("engine")
    engine_file = engine_dir / "pikafish.exe"
    
    if engine_file.exists():
        print(f"  [OK] 引擎文件存在: {engine_file}")
        return True
    else:
        print(f"  [FAIL] 引擎文件不存在: {engine_file}")
        print("    请运行: python download_engine.py")
        return False


def test_assistant():
    """测试助手类"""
    print("\n测试ChineseChessAssistant...")
    
    try:
        from chess_assistant import ChineseChessAssistant
        
        assistant = ChineseChessAssistant()
        print("  [OK] ChineseChessAssistant初始化成功")
        
        # 测试FEN识别
        initial_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
        print(f"  [OK] 初始FEN: {initial_fen[:30]}...")
        
        return True
    except Exception as e:
        print(f"  [FAIL] 助手类测试失败: {str(e)}")
        return False


def cleanup():
    """清理测试文件"""
    print("\n清理测试文件...")
    
    test_files = ["test_screenshot.png", "test_opencv.png"]
    for f in test_files:
        path = Path(f)
        if path.exists():
            path.unlink()
            print(f"  [OK] 已删除: {f}")


def main():
    print("="*60)
    print("中国象棋辅助程序 - 基础功能测试")
    print("="*60)
    
    results = []
    
    # 运行测试
    results.append(("依赖包", test_imports()))
    results.append(("截图功能", test_screenshot()))
    results.append(("OpenCV", test_opencv()))
    results.append(("引擎配置", test_engine()))
    results.append(("助手类", test_assistant()))
    
    # 清理
    cleanup()
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {name:12s} : {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] 所有测试通过！程序可以正常使用。")
        print("\n运行程序:")
        print("  - GUI版本: python chess_gui.py")
        print("  - 命令行版本: python chess_assistant.py")
    else:
        print("[WARNING] 部分测试失败，请按照提示解决问题。")
        print("\n常见解决方法:")
        print("  - 安装依赖: pip install -r requirements.txt")
        print("  - 配置引擎: python download_engine.py")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

