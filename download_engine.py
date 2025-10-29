"""
自动下载Pikafish引擎的脚本
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path


def download_file(url, dest_path):
    """
    下载文件并显示进度
    """
    print(f"正在下载: {url}")
    
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            s = f"\r下载进度: {percent:5.1f}% {readsofar:,} / {totalsize:,} bytes"
            sys.stderr.write(s)
            if readsofar >= totalsize:
                sys.stderr.write("\n")
        else:
            sys.stderr.write(f"\r已下载: {readsofar:,} bytes")
    
    urllib.request.urlretrieve(url, dest_path, reporthook)
    print(f"下载完成: {dest_path}")


def extract_zip(zip_path, extract_to):
    """
    解压zip文件
    """
    print(f"正在解压: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"解压完成: {extract_to}")


def setup_pikafish():
    """
    下载并设置Pikafish引擎
    """
    print("="*60)
    print("Pikafish 引擎自动下载工具")
    print("="*60)
    
    # 创建engine目录
    engine_dir = Path("engine")
    engine_dir.mkdir(exist_ok=True)
    
    # Pikafish下载链接（这里使用一个示例链接，实际需要从GitHub获取最新版本）
    # 注意：需要根据实际情况更新链接
    print("\n请手动下载Pikafish引擎:")
    print("1. 访问: https://github.com/official-pikafish/Pikafish/releases")
    print("2. 下载最新的Windows版本 (pikafish-*-windows-x86-64.zip)")
    print("3. 解压后将 pikafish.exe 或 pikafish-windows-x86-64.exe 放入 engine/ 目录")
    print("4. 重命名为 pikafish.exe")
    
    print(f"\n目标路径: {engine_dir.absolute()}")
    
    # 检查是否已存在
    possible_names = ["pikafish.exe", "pikafish-windows-x86-64.exe"]
    for name in possible_names:
        engine_file = engine_dir / name
        if engine_file.exists():
            print(f"\n✓ 找到引擎文件: {engine_file}")
            
            # 如果不是标准名称，重命名
            if name != "pikafish.exe":
                new_name = engine_dir / "pikafish.exe"
                engine_file.rename(new_name)
                print(f"✓ 已重命名为: {new_name}")
            
            print("\n引擎设置完成！")
            return True
    
    print(f"\n✗ 未找到引擎文件")
    print("请按照上述步骤手动下载并放置引擎文件")
    return False


def main():
    try:
        success = setup_pikafish()
        if success:
            print("\n可以运行 chess_assistant.py 开始使用了！")
        else:
            print("\n请手动完成引擎设置后再运行程序")
    except Exception as e:
        print(f"\n出错: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

