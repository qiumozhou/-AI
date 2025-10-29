"""
打包脚本 - 将Python程序打包成Windows可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build_files():
    """清理之前的打包文件"""
    print("清理旧的打包文件...")
    
    dirs_to_remove = ['build', 'dist']
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  已删除: {d}/")
    
    # 删除spec文件
    spec_files = ['chess_gui.spec', 'chess_assistant.spec']
    for f in spec_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"  已删除: {f}")


def build_gui_version():
    """打包GUI版本"""
    print("\n" + "="*60)
    print("正在打包GUI版本...")
    print("="*60)
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--name=中国象棋助手',  # 程序名称
        '--onefile',  # 打包成单个exe文件
        '--windowed',  # 不显示控制台窗口（GUI程序）
        '--icon=NONE',  # 图标（如果有的话）
        '--add-data=README.md;.',  # 添加README
        '--add-data=USAGE.md;.',  # 添加使用说明
        '--add-data=QUICK_REFERENCE.md;.',  # 添加快速参考
        '--hidden-import=PIL._tkinter_finder',  # 隐藏导入
        '--collect-all=cv2',  # 收集OpenCV所有文件
        '--collect-all=numpy',  # 收集NumPy所有文件
        'chess_gui.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ GUI版本打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ GUI版本打包失败: {e}")
        return False


def build_cli_version():
    """打包命令行版本"""
    print("\n" + "="*60)
    print("正在打包命令行版本...")
    print("="*60)
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--name=中国象棋助手-命令行',
        '--onefile',  # 打包成单个exe文件
        '--console',  # 显示控制台窗口
        '--icon=NONE',
        '--add-data=README.md;.',
        '--add-data=USAGE.md;.',
        '--collect-all=cv2',
        '--collect-all=numpy',
        'chess_assistant.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ 命令行版本打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 命令行版本打包失败: {e}")
        return False


def create_distribution_package():
    """创建发行包"""
    print("\n" + "="*60)
    print("创建发行包...")
    print("="*60)
    
    # 创建发行目录
    dist_dir = Path("发行版")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # 复制可执行文件
    gui_exe = Path("dist/中国象棋助手.exe")
    cli_exe = Path("dist/中国象棋助手-命令行.exe")
    
    if gui_exe.exists():
        shutil.copy(gui_exe, dist_dir / "中国象棋助手.exe")
        print(f"  ✓ 复制: {gui_exe.name}")
    
    if cli_exe.exists():
        shutil.copy(cli_exe, dist_dir / "中国象棋助手-命令行.exe")
        print(f"  ✓ 复制: {cli_exe.name}")
    
    # 创建engine目录
    engine_dir = dist_dir / "engine"
    engine_dir.mkdir()
    
    # 复制引擎README
    if Path("engine/README.md").exists():
        shutil.copy("engine/README.md", engine_dir)
    
    # 复制文档
    docs = [
        "README.md",
        "START_HERE.md",
        "USAGE.md",
        "QUICK_REFERENCE.md",
        "setup_guide.md",
        "LICENSE",
        "VERSION"
    ]
    
    for doc in docs:
        if Path(doc).exists():
            shutil.copy(doc, dist_dir)
            print(f"  ✓ 复制: {doc}")
    
    # 创建使用说明
    create_usage_txt(dist_dir)
    
    print(f"\n发行包已创建在: {dist_dir.absolute()}")


def create_usage_txt(dist_dir):
    """创建使用说明文本"""
    usage_text = """
中国象棋助手 v1.0.0 使用说明
================================

感谢使用中国象棋助手！

快速开始
--------
1. 下载Pikafish引擎
   访问: https://github.com/official-pikafish/Pikafish/releases
   下载最新Windows版本，解压后将 pikafish.exe 放入 engine/ 目录

2. 运行程序
   双击 "中国象棋助手.exe" 启动GUI版本（推荐）
   或双击 "中国象棋助手-命令行.exe" 启动命令行版本

3. 使用方法
   - 打开象棋对弈界面（网页或软件）
   - 点击"开始分析"按钮或按 Ctrl+S
   - 查看走法建议

快捷键
------
Ctrl + S  : 开始/停止分析
Ctrl + Q  : 退出程序

详细文档
--------
- START_HERE.md - 新手入门指南
- USAGE.md - 详细使用教程  
- QUICK_REFERENCE.md - 快速参考
- README.md - 完整项目文档

注意事项
--------
⚠️ 本程序仅供学习研究使用
✓ 允许: 个人学习、复盘分析、研究象棋
✗ 禁止: 线上排位作弊、正式比赛使用

技术支持
--------
GitHub: https://github.com/qiumozhou/-AI
问题反馈: https://github.com/qiumozhou/-AI/issues

版本信息
--------
版本: v1.0.0
更新日期: 2025-10-29
许可协议: MIT License

================================
祝您使用愉快！
"""
    
    with open(dist_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(usage_text)
    
    print("  ✓ 创建: 使用说明.txt")


def main():
    print("="*60)
    print("中国象棋助手 - 打包工具")
    print("="*60)
    
    # 清理旧文件
    clean_build_files()
    
    # 询问用户要打包哪个版本
    print("\n选择打包版本:")
    print("1. GUI版本（推荐）")
    print("2. 命令行版本")
    print("3. 两个都打包")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    success = True
    
    if choice == "1":
        success = build_gui_version()
    elif choice == "2":
        success = build_cli_version()
    elif choice == "3":
        success = build_gui_version() and build_cli_version()
    else:
        print("无效选择！")
        return 1
    
    if success:
        # 创建发行包
        create_distribution_package()
        
        print("\n" + "="*60)
        print("打包完成！")
        print("="*60)
        print("\n可执行文件位置:")
        print(f"  发行版/中国象棋助手.exe")
        if choice == "3":
            print(f"  发行版/中国象棋助手-命令行.exe")
        print(f"\n完整发行包: 发行版/ 目录")
        print("\n提示: 使用前请先下载Pikafish引擎到 engine/ 目录")
        print("="*60)
    else:
        print("\n打包失败！请检查错误信息。")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

