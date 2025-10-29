#!/usr/bin/env python3
"""
快速启动脚本
一键检查环境并启动程序
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """检查Python版本"""
    print("\n检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """检查依赖是否安装"""
    print("\n检查依赖包...")
    
    required_packages = [
        "PIL",
        "numpy", 
        "cv2",
        "pyautogui",
        "keyboard",
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages


def install_dependencies():
    """安装依赖"""
    print("\n是否自动安装依赖？")
    choice = input("输入 y 确认，其他键跳过: ").lower()
    
    if choice == 'y':
        print("\n正在安装依赖...")
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                "requirements.txt",
                "-i",
                "https://pypi.tuna.tsinghua.edu.cn/simple"
            ])
            print("✓ 依赖安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败")
            return False
    return False


def check_engine():
    """检查引擎"""
    print("\n检查引擎...")
    engine_path = Path("engine/pikafish.exe")
    
    if engine_path.exists():
        print(f"✓ 引擎已配置: {engine_path}")
        return True
    else:
        print("❌ 引擎未配置")
        return False


def setup_engine():
    """设置引擎"""
    print("\n是否配置引擎？")
    choice = input("输入 y 确认，其他键跳过: ").lower()
    
    if choice == 'y':
        try:
            subprocess.check_call([sys.executable, "download_engine.py"])
            return check_engine()
        except:
            return False
    return False


def run_tests():
    """运行测试"""
    print("\n是否运行测试？")
    choice = input("输入 y 确认，其他键跳过: ").lower()
    
    if choice == 'y':
        print("\n运行测试...")
        try:
            result = subprocess.call([sys.executable, "test_basic.py"])
            return result == 0
        except:
            return False
    return True


def choose_mode():
    """选择运行模式"""
    print_header("选择运行模式")
    print("\n1. GUI图形界面版本（推荐）")
    print("2. 命令行版本")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ")
    
    if choice == "1":
        print("\n启动GUI版本...")
        subprocess.call([sys.executable, "chess_gui.py"])
    elif choice == "2":
        print("\n启动命令行版本...")
        print("提示: 使用 Ctrl+S 开始/停止, Ctrl+Q 退出\n")
        subprocess.call([sys.executable, "chess_assistant.py"])
    elif choice == "3":
        print("\n再见！")
        return
    else:
        print("\n无效选择")


def main():
    """主函数"""
    print_header("中国象棋辅助程序 - 快速启动")
    
    # 检查Python版本
    if not check_python_version():
        print("\n请升级Python版本后重试")
        return 1
    
    # 检查依赖
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print(f"\n缺少以下依赖: {', '.join(missing)}")
        if not install_dependencies():
            print("\n请手动安装依赖:")
            print("  pip install -r requirements.txt")
            return 1
        # 重新检查
        deps_ok, _ = check_dependencies()
        if not deps_ok:
            return 1
    
    # 检查引擎
    engine_ok = check_engine()
    if not engine_ok:
        print("\n引擎未配置，程序可以运行但无法提供走法建议")
        if not setup_engine():
            print("\n你可以稍后运行以下命令配置引擎:")
            print("  python download_engine.py")
    
    # 运行测试
    run_tests()
    
    # 选择模式
    choose_mode()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(0)

